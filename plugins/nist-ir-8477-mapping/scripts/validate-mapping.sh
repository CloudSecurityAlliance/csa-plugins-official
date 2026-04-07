#!/bin/bash
#
# validate-mapping.sh — Cross-model validation for NIST IR 8477 mapping outputs
#
# Sends mapping output to multiple AI models with a structured review prompt
# targeting mapping-specific error patterns (type misclassification, directionality,
# rationale inconsistency, exhaustiveness drift, missing no-relationship documentation).
#
# Usage:
#   ./validate-mapping.sh <mapping-output.json> [focal-source.json] [reference-source.json]
#
#   Arguments:
#     1. (required) The mapping output JSON to validate
#     2. (optional) Focal document structured data for comparison
#     3. (optional) Reference document structured data for comparison
#     Source files improve validation accuracy — without them, confidence is reduced.
#
# Requirements (at least one must be installed):
#   - codex CLI — npm install -g @openai/codex
#   - gemini CLI — npm install -g @google/gemini-cli
#
# Output:
#   - Creates <output-name>.codex-review.md and/or <output-name>.gemini-review.md
#   - Exit code 0 if at least one review succeeded OR no validators installed (skipped)
#   - Exit code 1 only if validators were available but all failed

set -uo pipefail

# --- Resolve script location (for finding prompt file) ---

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROMPT_FILE="${PLUGIN_ROOT}/skills/nist-ir-8477-mapping/references/validation-prompt.md"

# --- Argument validation ---

if [ $# -lt 1 ]; then
    echo "Usage: $0 <mapping-output.json> [focal-source.json] [reference-source.json]"
    echo ""
    echo "Runs cross-model validation on a NIST IR 8477 mapping output."
    echo "Optionally provide source documents for comparison (improves accuracy)."
    echo "Requires at least one of: codex CLI, gemini CLI"
    exit 1
fi

MAPPING_PATH="$1"
FOCAL_PATH="${2:-}"
REFERENCE_PATH="${3:-}"

if [ ! -f "$MAPPING_PATH" ]; then
    echo "Error: Mapping output not found: $MAPPING_PATH"
    exit 1
fi

if [ -n "$FOCAL_PATH" ] && [ ! -f "$FOCAL_PATH" ]; then
    echo "Error: Focal source not found: $FOCAL_PATH"
    exit 1
fi

if [ -n "$REFERENCE_PATH" ] && [ ! -f "$REFERENCE_PATH" ]; then
    echo "Error: Reference source not found: $REFERENCE_PATH"
    exit 1
fi

# --- Load prompt from file ---

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Validation prompt not found at: $PROMPT_FILE"
    exit 1
fi

REVIEW_PROMPT="$(sed -n '/^```$/,/^```$/p' "$PROMPT_FILE" | sed '1d;$d')"

if [ -z "$REVIEW_PROMPT" ]; then
    echo "Error: Could not extract prompt from $PROMPT_FILE"
    exit 1
fi

# --- Tool availability checks ---

HAS_CODEX=false
HAS_GEMINI=false

if command -v codex &>/dev/null; then
    echo "Found codex: $(codex --version 2>/dev/null || echo "unknown")"
    HAS_CODEX=true
else
    echo "codex CLI not found (install: npm install -g @openai/codex)"
fi

if command -v gemini &>/dev/null; then
    echo "Found gemini: $(gemini --version 2>/dev/null || echo "unknown")"
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

MAPPING_DIR="$(dirname "$MAPPING_PATH")"
MAPPING_NAME="$(basename "$MAPPING_PATH" .json)"

CODEX_OUTPUT="${MAPPING_DIR}/${MAPPING_NAME}.codex-review.md"
GEMINI_OUTPUT="${MAPPING_DIR}/${MAPPING_NAME}.gemini-review.md"

# --- Build the full prompt (temp file to avoid arg-size limits) ---

TEMP_PROMPT="$(mktemp)"
trap 'rm -f "$TEMP_PROMPT"' EXIT

{
    echo "$REVIEW_PROMPT"
    echo ""
    echo "---"
    echo ""
    echo "HERE IS THE MAPPING OUTPUT TO REVIEW:"
    echo ""
    cat "$MAPPING_PATH"
} > "$TEMP_PROMPT"

if [ -n "$FOCAL_PATH" ]; then
    {
        echo ""
        echo "---"
        echo ""
        echo "HERE IS THE FOCAL DOCUMENT (structured data):"
        echo ""
        cat "$FOCAL_PATH"
    } >> "$TEMP_PROMPT"
fi

if [ -n "$REFERENCE_PATH" ]; then
    {
        echo ""
        echo "---"
        echo ""
        echo "HERE IS THE REFERENCE DOCUMENT (structured data):"
        echo ""
        cat "$REFERENCE_PATH"
    } >> "$TEMP_PROMPT"
fi

if [ -z "$FOCAL_PATH" ] && [ -z "$REFERENCE_PATH" ]; then
    {
        echo ""
        echo "---"
        echo ""
        echo "NOTE: No source documents were provided for comparison. Validate based on"
        echo "internal consistency, plausibility, and your knowledge of the referenced sources."
        echo "Flag reduced confidence for completeness and accuracy checks."
    } >> "$TEMP_PROMPT"
fi

# --- Run reviews ---

echo ""
echo "Validating mapping: $MAPPING_PATH"
[ -n "$FOCAL_PATH" ] && echo "  Focal source: $FOCAL_PATH"
[ -n "$REFERENCE_PATH" ] && echo "  Reference source: $REFERENCE_PATH"
[ -z "$FOCAL_PATH" ] && [ -z "$REFERENCE_PATH" ] && echo "  Source documents: not provided (reduced accuracy)"
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
    gemini -p "$(cat "$TEMP_PROMPT")" -o text > "$GEMINI_OUTPUT" 2>/dev/null &
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
    echo "Review the outputs, then incorporate valid corrections into the mapping."
    echo "Findings where both models agree are highest confidence."
    exit 0
else
    echo "All validation tools failed. Check authentication and try again."
    exit 1
fi
