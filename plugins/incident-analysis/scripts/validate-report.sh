#!/bin/bash
#
# validate-report.sh — Cross-model validation for incident analysis reports
#
# Sends a completed incident report to multiple AI models (Codex/OpenAI, Gemini/Google)
# with a structured review prompt. Each model independently reviews the report for
# factual accuracy, confidence level appropriateness, and analytical errors.
#
# Using multiple models from different providers reduces the risk of shared blind spots
# that a single model might have when both creating and reviewing the same work.
#
# Usage:
#   ./validate-report.sh <path-to-report.md>
#   ./validate-report.sh incidents/2026-03-19-stryker-handala-intune-wiper.md
#
# Requirements (at least one must be installed):
#   - codex CLI (codex-cli) — npm install -g @openai/codex
#   - gemini CLI — npm install -g @google/gemini-cli
#
# Output:
#   - Creates <report-name>.codex-review.md and/or <report-name>.gemini-review.md
#     in the same directory as the input report
#   - Exit code 0 if at least one review succeeded, 1 if all failed

set -uo pipefail

# --- Argument validation ---

if [ $# -lt 1 ]; then
    echo "Usage: $0 <path-to-report.md>"
    echo ""
    echo "Runs cross-model validation on an incident analysis report."
    echo "Requires at least one of: codex CLI, gemini CLI"
    exit 1
fi

REPORT_PATH="$1"

if [ ! -f "$REPORT_PATH" ]; then
    echo "Error: File not found: $REPORT_PATH"
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

REPORT_DIR="$(dirname "$REPORT_PATH")"
REPORT_NAME="$(basename "$REPORT_PATH" .md)"
REPORT_CONTENT="$(cat "$REPORT_PATH")"

CODEX_OUTPUT="${REPORT_DIR}/${REPORT_NAME}.codex-review.md"
GEMINI_OUTPUT="${REPORT_DIR}/${REPORT_NAME}.gemini-review.md"

# --- Review prompt ---
# Same prompt for all models so results are directly comparable.
# The prompt encodes the specific error patterns identified through
# experience with incident analysis reports.

REVIEW_PROMPT="$(cat <<'PROMPT_EOF'
You are an expert reviewer of cybersecurity incident analysis reports. Your job is to find factual errors, unsupported conclusions, and analytical weaknesses. Be rigorous and specific — cite the exact claims you're challenging and explain why.

Review the incident analysis report below. For each finding, provide:
- The specific claim or statement you're challenging (quote it)
- Why it's problematic (factual error, unsupported confidence level, logical gap, etc.)
- What the correct statement or confidence level should be, if you can determine it
- Sources or reasoning that support your correction

Focus on these specific error patterns:

1. **Factual accuracy**: Are specific dates, version numbers, feature availability claims, and technical details correct? When the report claims a security feature was "available since [date]," is that accurate for the specific sub-capability relevant to the incident? Check against your knowledge of vendor release timelines.

2. **Confidence level inflation**: The report uses a 6-level confidence framework (Confirmed, Corroborated, Reported, Inferred, Speculative, Disputed). Check whether claims are tagged at the right level:
   - Are claims about the victim's internal security posture (controls absent, features not enabled) tagged as "Inferred" rather than "Confirmed"? These are deductions from the attack outcome, not confirmed facts, unless the victim publicly confirmed their configuration.
   - Are claims supported only by anonymous community sources (HN, Reddit) tagged as "Reported" rather than "Corroborated"? Corroboration requires at least one source with editorial oversight.
   - When the vendor's own disclosure contradicts or qualifies an external claim, is the claim tagged as "Disputed" rather than "Corroborated"?

3. **Attribution specificity**: When the report cites threat intelligence about the threat actor's general TTPs, does it clearly distinguish between "the actor is known to do X" (general) and "the actor did X in this specific incident" (incident-specific)? General actor capabilities should not be presented as confirmed incident details.

4. **Vendor disclosure contradictions**: Does the report check external claims against the vendor's own product-specific statements? Vendor updates sometimes contain per-product clarifications that contradict broader external reporting. If the vendor says "System Y is functioning normally" but the report says "System Y failed," that's a disputed claim, not a confirmed one.

5. **Logical consistency**: Do the conclusions follow from the evidence presented? Are there leaps in reasoning? Does the report draw strong conclusions from weak evidence?

6. **Missing caveats**: Are there important limitations, alternative explanations, or counter-arguments that the report fails to mention?

Structure your review as:

## Findings

Number each finding. For each:
- **Severity**: Critical (factual error that changes conclusions) / Significant (confidence level or attribution error) / Minor (missing caveat or imprecise language)
- **Location**: Quote the specific text
- **Issue**: What's wrong
- **Correction**: What it should say, or what additional verification is needed
- **Sources**: Your basis for the correction (if applicable)

## Summary

After all findings, provide:
- Total number of findings by severity
- Overall assessment of the report's reliability
- The 1-3 most important corrections

---

HERE IS THE REPORT TO REVIEW:

PROMPT_EOF
)"

# Combine prompt and report content
FULL_PROMPT="${REVIEW_PROMPT}

${REPORT_CONTENT}"

# --- Run reviews ---

echo ""
echo "Validating report: $REPORT_PATH"
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
    echo "Review the outputs, then incorporate valid corrections into the report."
    echo "Findings where both models agree are highest confidence."
    exit 0
else
    echo "All validation tools failed. Check authentication and try again."
    exit 1
fi
