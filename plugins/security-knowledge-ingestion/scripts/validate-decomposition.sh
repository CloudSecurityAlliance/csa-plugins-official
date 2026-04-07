#!/bin/bash
#
# validate-decomposition.sh — Cross-model validation for security knowledge decompositions
#
# Sends a structured decomposition output to multiple AI models (Codex/OpenAI, Gemini/Google)
# with a structured review prompt. Each model independently reviews for completeness, phantom
# concepts, merging/splitting errors, hierarchy accuracy, and metadata fidelity.
#
# The review prompt is loaded from references/validation-prompt.md — edit that file to
# change validation behavior. The prompt is never hardcoded in this script.
#
# Usage:
#   ./validate-decomposition.sh <structured-output.json> [source-document.md]
#
#   Both arguments are file paths:
#     1. (required) The structured decomposition JSON to validate
#     2. (optional) Source document (markdown, text, or any readable format) for comparison
#        If omitted, validation runs without source comparison (less effective)
#
# Examples:
#   ./validate-decomposition.sh output/nist-800-53-r5.json source/nist-800-53-r5.md
#   ./validate-decomposition.sh output/ccm-4.1.json
#
# Requirements (at least one must be installed):
#   - codex CLI — npm install -g @openai/codex
#   - gemini CLI — npm install -g @google/gemini-cli
#
# Output:
#   - Creates <output-name>.codex-review.md and/or <output-name>.gemini-review.md
#     in the same directory as the input file
#   - Exit code 0 if at least one review succeeded OR if no validators are installed (skipped)
#   - Exit code 1 only if validators were available but all failed

set -uo pipefail

# --- Resolve script location (for finding prompt file) ---

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROMPT_FILE="${PLUGIN_ROOT}/skills/security-knowledge-ingestion/references/validation-prompt.md"

# --- Argument validation ---

if [ $# -lt 1 ]; then
    echo "Usage: $0 <structured-output.json> [source-document.md]"
    echo ""
    echo "Runs cross-model validation on a security knowledge decomposition."
    echo "Optionally provide the source document for comparison (more effective)."
    echo "Requires at least one of: codex CLI, gemini CLI"
    exit 1
fi

OUTPUT_PATH="$1"
SOURCE_PATH="${2:-}"

if [ ! -f "$OUTPUT_PATH" ]; then
    echo "Error: Structured output not found: $OUTPUT_PATH"
    exit 1
fi

if [ -n "$SOURCE_PATH" ] && [ ! -f "$SOURCE_PATH" ]; then
    echo "Error: Source document not found: $SOURCE_PATH"
    exit 1
fi

# --- Load prompt from file ---

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Validation prompt not found at: $PROMPT_FILE"
    echo "Expected at: skills/security-knowledge-ingestion/references/validation-prompt.md"
    exit 1
fi

# Extract the prompt from between the ``` fences in the markdown file
REVIEW_PROMPT="$(sed -n '/^```$/,/^```$/p' "$PROMPT_FILE" | sed '1d;$d')"

if [ -z "$REVIEW_PROMPT" ]; then
    echo "Error: Could not extract prompt from $PROMPT_FILE"
    echo "Expected prompt text between \`\`\` fences in the markdown file."
    exit 1
fi

# --- Tool availability checks ---

HAS_CODEX=false
HAS_GEMINI=false

if command -v codex &>/dev/null; then
    CODEX_VERSION="$(codex --version 2>/dev/null || echo "unknown")"
    echo "Found codex: $CODEX_VERSION"
    HAS_CODEX=true
else
    echo "codex CLI not found (install: npm install -g @openai/codex)"
fi

if command -v gemini &>/dev/null; then
    GEMINI_VERSION="$(gemini --version 2>/dev/null || echo "unknown")"
    echo "Found gemini: $GEMINI_VERSION"
    HAS_GEMINI=true
else
    echo "gemini CLI not found (install: npm install -g @google/gemini-cli)"
fi

if [ "$HAS_CODEX" = false ] && [ "$HAS_GEMINI" = false ]; then
    echo ""
    echo "No validation tools available. Skipping validation."
    echo "Install at least one of:"
    echo "  npm install -g @openai/codex"
    echo "  npm install -g @google/gemini-cli"
    echo ""
    echo "STATUS: SKIPPED (no validators installed)"
    exit 0
fi

# --- Setup ---

OUTPUT_DIR="$(dirname "$OUTPUT_PATH")"
OUTPUT_NAME="$(basename "$OUTPUT_PATH" .json)"

CODEX_OUTPUT="${OUTPUT_DIR}/${OUTPUT_NAME}.codex-review.md"
GEMINI_OUTPUT="${OUTPUT_DIR}/${OUTPUT_NAME}.gemini-review.md"

# --- Build the full prompt ---

# Write to a temp file to avoid argument-size limits
TEMP_PROMPT="$(mktemp)"
trap 'rm -f "$TEMP_PROMPT"' EXIT

{
    echo "$REVIEW_PROMPT"
    echo ""
    echo "---"
    echo ""
    echo "HERE IS THE STRUCTURED DECOMPOSITION TO REVIEW:"
    echo ""
    cat "$OUTPUT_PATH"
} > "$TEMP_PROMPT"

if [ -n "$SOURCE_PATH" ]; then
    {
        echo ""
        echo "---"
        echo ""
        echo "HERE IS THE SOURCE DOCUMENT FOR COMPARISON:"
        echo ""
        cat "$SOURCE_PATH"
    } >> "$TEMP_PROMPT"
else
    {
        echo ""
        echo "---"
        echo ""
        echo "NOTE: No source document was provided for comparison. Do your best to validate"
        echo "the decomposition based on internal consistency, plausibility, and your knowledge"
        echo "of the referenced source. Flag anything that looks suspicious but note that you"
        echo "cannot confirm completeness or accuracy without the source."
    } >> "$TEMP_PROMPT"
fi

# --- Run reviews ---

echo ""
echo "Validating decomposition: $OUTPUT_PATH"
[ -n "$SOURCE_PATH" ] && echo "  Source document: $SOURCE_PATH"
[ -z "$SOURCE_PATH" ] && echo "  Source document: not provided (reduced accuracy)"
TOOLS_RUNNING=""

if [ "$HAS_CODEX" = true ]; then
    echo "  Starting Codex review..."
    codex exec --ephemeral -o "$CODEX_OUTPUT" - < "$TEMP_PROMPT" &
    CODEX_PID=$!
    TOOLS_RUNNING="${TOOLS_RUNNING}codex "
else
    CODEX_PID=""
fi

if [ "$HAS_GEMINI" = true ]; then
    echo "  Starting Gemini review..."
    cat "$TEMP_PROMPT" | gemini -o text > "$GEMINI_OUTPUT" 2>/dev/null &
    GEMINI_PID=$!
    TOOLS_RUNNING="${TOOLS_RUNNING}gemini "
else
    GEMINI_PID=""
fi

echo ""
echo "Waiting for reviews to complete (${TOOLS_RUNNING})..."
echo ""

# --- Wait and collect results ---

CODEX_EXIT=0
GEMINI_EXIT=0
ANY_SUCCEEDED=false

if [ -n "$CODEX_PID" ]; then
    wait "$CODEX_PID" || CODEX_EXIT=$?
fi

if [ -n "$GEMINI_PID" ]; then
    wait "$GEMINI_PID" || GEMINI_EXIT=$?
fi

# --- Report results ---

echo "=== Validation Complete ==="
echo ""

if [ "$HAS_CODEX" = true ]; then
    if [ $CODEX_EXIT -eq 0 ] && [ -s "$CODEX_OUTPUT" ]; then
        CODEX_LINES="$(wc -l < "$CODEX_OUTPUT" | tr -d ' ')"
        echo "  Codex review:  $CODEX_OUTPUT ($CODEX_LINES lines)"
        ANY_SUCCEEDED=true
    else
        echo "  Codex review:  FAILED (exit code: $CODEX_EXIT)"
        [ -f "$CODEX_OUTPUT" ] && rm -f "$CODEX_OUTPUT"
    fi
else
    echo "  Codex review:  SKIPPED (not installed)"
fi

if [ "$HAS_GEMINI" = true ]; then
    if [ $GEMINI_EXIT -eq 0 ] && [ -s "$GEMINI_OUTPUT" ]; then
        GEMINI_LINES="$(wc -l < "$GEMINI_OUTPUT" | tr -d ' ')"
        echo "  Gemini review: $GEMINI_OUTPUT ($GEMINI_LINES lines)"
        ANY_SUCCEEDED=true
    else
        echo "  Gemini review: FAILED (exit code: $GEMINI_EXIT)"
        [ -f "$GEMINI_OUTPUT" ] && rm -f "$GEMINI_OUTPUT"
    fi
else
    echo "  Gemini review: SKIPPED (not installed)"
fi

echo ""

if [ "$ANY_SUCCEEDED" = true ]; then
    echo "Review the outputs, then incorporate valid corrections into the structured data."
    echo "Findings where both models agree are highest confidence."
    exit 0
else
    echo "All validation tools failed. Check authentication and try again."
    exit 1
fi
