#!/bin/bash
#
# validate-decomposition.sh — Cross-model validation for security knowledge decompositions
#
# Sends a structured decomposition output to multiple AI models (Codex/OpenAI, Gemini/Google)
# with a structured review prompt. Each model independently reviews for completeness, phantom
# concepts, merging/splitting errors, hierarchy accuracy, and metadata fidelity.
#
# Using multiple models from different providers reduces the risk of shared blind spots
# that a single model might have when both creating and reviewing the same work.
#
# Usage:
#   ./validate-decomposition.sh <path-to-structured-output.json>
#   ./validate-decomposition.sh output/nist-800-53-r5.json
#
# Requirements (at least one must be installed):
#   - codex CLI (codex-cli) — npm install -g @openai/codex
#   - gemini CLI — npm install -g @google/gemini-cli
#
# Output:
#   - Creates <output-name>.codex-review.md and/or <output-name>.gemini-review.md
#     in the same directory as the input file
#   - Exit code 0 if at least one review succeeded, 1 if all failed

set -uo pipefail

# --- Argument validation ---

if [ $# -lt 1 ]; then
    echo "Usage: $0 <path-to-structured-output.json>"
    echo ""
    echo "Runs cross-model validation on a security knowledge decomposition."
    echo "Requires at least one of: codex CLI, gemini CLI"
    exit 1
fi

OUTPUT_PATH="$1"

if [ ! -f "$OUTPUT_PATH" ]; then
    echo "Error: File not found: $OUTPUT_PATH"
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
    echo "Error: No validation tools available."
    echo "Install at least one of:"
    echo "  npm install -g @openai/codex"
    echo "  npm install -g @google/gemini-cli"
    exit 1
fi

# --- Setup ---

OUTPUT_DIR="$(dirname "$OUTPUT_PATH")"
OUTPUT_NAME="$(basename "$OUTPUT_PATH" .json)"

CODEX_OUTPUT="${OUTPUT_DIR}/${OUTPUT_NAME}.codex-review.md"
GEMINI_OUTPUT="${OUTPUT_DIR}/${OUTPUT_NAME}.gemini-review.md"

# --- Review prompt ---
# Same prompt for all models so results are directly comparable.
# Targets decomposition-specific error patterns.

REVIEW_PROMPT="$(cat <<'PROMPT_EOF'
You are an expert reviewer of security knowledge decomposition outputs. Your job is to verify that a document has been correctly broken down into individually addressable concepts with accurate hierarchy, metadata, and boundaries.

Review the structured decomposition output below. For each finding, provide:
- The specific concept(s) affected (by ID)
- Which error pattern applies (see list below)
- Why it's problematic
- What the correction should be

Focus on these specific error patterns:

1. **Completeness**: Are there concepts in the source that are missing from the output? Count concepts and compare. Pay special attention to appendices, annexes, and enhancement sections.

2. **Phantom concepts**: Are there concepts in the output that don't exist in the source? Check that every concept ID corresponds to a real item in the source document.

3. **Merging errors**: Were two distinct concepts merged into one? Look for unusually long descriptions or concepts covering multiple distinct topics.

4. **Splitting errors**: Was one concept split into multiple? Look for concepts that seem to be fragments of a larger whole.

5. **Hierarchy accuracy**: Does the parent-child structure match the source? Are children under the right parents? Is the hierarchy depth correct?

6. **Metadata accuracy**: Are concept types correct (control vs requirement vs recommendation)? Are IDs preserved exactly as the source uses them? Are descriptions faithful to source text?

7. **Boundary accuracy**: Are concept boundaries drawn where the source draws them, not where the AI thinks they should be?

Structure your review as:

## Findings

Number each finding. For each:
- **Error type**: Which of the 7 patterns above
- **Severity**: Critical (wrong concepts) / Important (wrong structure) / Minor (wrong metadata)
- **Location**: Concept ID(s) affected
- **Evidence**: What the source says vs what the output says
- **Correction**: What should change

## Summary

After all findings:
- Total findings by severity
- Total findings by error type
- The 3 most important corrections
- Overall assessment of decomposition quality

---

HERE IS THE STRUCTURED DECOMPOSITION TO REVIEW:

PROMPT_EOF
)"

# Combine prompt and output content
OUTPUT_CONTENT="$(cat "$OUTPUT_PATH")"
FULL_PROMPT="${REVIEW_PROMPT}

${OUTPUT_CONTENT}"

# --- Run reviews ---

echo ""
echo "Validating decomposition: $OUTPUT_PATH"
TOOLS_RUNNING=""

if [ "$HAS_CODEX" = true ]; then
    echo "  Starting Codex review..."
    codex exec --ephemeral -o "$CODEX_OUTPUT" - <<< "$FULL_PROMPT" &
    CODEX_PID=$!
    TOOLS_RUNNING="${TOOLS_RUNNING}codex "
else
    CODEX_PID=""
fi

if [ "$HAS_GEMINI" = true ]; then
    echo "  Starting Gemini review..."
    gemini -p "$FULL_PROMPT" -o text > "$GEMINI_OUTPUT" 2>/dev/null &
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
