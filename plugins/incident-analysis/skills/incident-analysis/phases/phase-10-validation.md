# Phase 10: Cross-Model Validation

## Purpose

Submit the completed report to independent AI models from different providers for adversarial review. Each model independently checks for factual errors, confidence level inflation, attribution mistakes, and unsupported conclusions. Using multiple models reduces the risk of shared blind spots that occur when a single model both creates and validates work.

## Why Cross-Model Validation

A single AI model reviewing its own work tends to reproduce the same blind spots that created the errors. Different models have different training data, different reasoning patterns, and different knowledge gaps. When two independent models flag the same issue, confidence that it's a real error is high. When only one model flags something, it still warrants investigation but may be a false positive.

This phase is not a substitute for human review — it's a systematic pre-check that catches mechanical errors (wrong dates, wrong MITRE IDs, inflated confidence levels) before they reach the analyst.

## Prerequisites

At least one external AI CLI tool must be installed and authenticated:
- **Codex CLI** (OpenAI) — `npm install -g @openai/codex`
- **Gemini CLI** (Google) — `npm install -g @google/gemini-cli`

The validation script checks for tool availability and runs whatever is installed. If neither is available, this phase is skipped with a note to the analyst.

## Process

### Step 1: Check Tool Availability

Before running validation, check whether the external AI tools are installed:

```bash
command -v codex && echo "Codex available" || echo "Codex not installed"
command -v gemini && echo "Gemini available" || echo "Gemini not installed"
```

If neither tool is available, inform the analyst:
- "Cross-model validation requires codex CLI and/or gemini CLI. Neither is installed. Skipping validation — you can install them and run the validation script manually later."

If at least one tool is available, proceed.

### Step 2: Run the Validation Script

The validation script is at `../../scripts/validate-report.sh` relative to SKILL.md's directory (following the plugin's path convention). At runtime, resolve this from the plugin's installed location — the same base path used to load this skill.

Run it with the absolute path to the report:

```bash
<plugin-root>/scripts/validate-report.sh /absolute/path/to/report.md
```

The script:
1. Reads the full report content
2. Prepends a structured review prompt targeting known error patterns
3. Sends the combined prompt to all available models in parallel
4. Saves each model's review as `<report-name>.<model>-review.md` alongside the report

The review prompt specifically targets these error patterns (derived from real analysis failures):
- **Factual accuracy** — dates, version numbers, feature availability for specific sub-capabilities
- **Confidence level inflation** — inference-from-outcome treated as confirmed, community sources treated as corroboration
- **Attribution specificity** — general actor TTPs presented as incident-specific observations
- **Vendor disclosure contradictions** — external claims not checked against the vendor's own statements
- **Logical consistency** — conclusions that outrun the evidence
- **Missing caveats** — important limitations or counter-arguments omitted

### Step 3: Read and Synthesize Reviews

After the script completes, read each review file and present a synthesis to the analyst:

1. **Findings where both models agree** — These are high-confidence errors. Present them as "Both Codex and Gemini flagged this."
2. **Findings from only one model** — Present these as "Flagged by [model] only — warrants investigation."
3. **Contradictions between models** — If one model says something is wrong and the other says it's fine, note the disagreement.

For each finding, assess:
- Is this a valid correction? (The reviewing models can also be wrong)
- Does it require a change to the report?
- Does it require re-checking a source?

### Step 4: Apply Corrections

For each validated finding:
- If it's a factual error: correct it and update the confidence level
- If it's a confidence level issue: downgrade to the appropriate level with a note
- If it's a missing caveat: add the caveat
- If it's unclear whether the finding is valid: flag it for the analyst's judgment

After applying corrections, note in the report: "This report was validated using cross-model review (Codex, Gemini). [N] corrections were applied based on validation findings."

### Step 5: Present to Analyst

Tell the analyst:
- How many findings each model produced, by severity
- Which findings both models agreed on (highest confidence)
- Which corrections were applied to the report
- Any findings you chose not to apply, and why
- "Would you like to review any of the validation findings in detail?"

## When Validation is Unavailable

If no external AI tools are installed:
1. Note this in the report: "Cross-model validation was not performed (external AI tools not available)."
2. Recommend the analyst install the tools for future analyses
3. Proceed to finalize the report — validation is valuable but not blocking

## Teaching Moment (if teaching mode is on)

> **Why different models matter:** Using different AI models from different providers (OpenAI, Google) for validation is deliberate. Each model has its own training data, knowledge cutoffs, reasoning patterns, and blind spots. An error that one model reproduces (because it shares the same training data or reasoning pattern) may be caught by another model that doesn't. This is the same principle behind using diverse tools in security testing — a single scanner misses things that a diverse set catches.
>
> **The "both agree" signal:** When two independent models from different providers flag the same issue, that's a strong signal. It means the error is visible from multiple analytical perspectives, not an artifact of one model's quirks. Treat "both agree" findings as near-certain errors that require correction.
>
> **Validation is not infallible:** The reviewing models can also be wrong. They may flag something as an error when it's actually correct, or miss errors entirely. Validation is a systematic pre-check, not a guarantee. The analyst's judgment remains the final authority.

## Output

Present to the analyst:
1. **Validation summary** — models used, findings count by severity
2. **High-confidence findings** — issues flagged by multiple models
3. **Single-model findings** — issues flagged by only one model
4. **Corrections applied** — what was changed in the report
5. **Findings not applied** — what was flagged but not corrected, and why
