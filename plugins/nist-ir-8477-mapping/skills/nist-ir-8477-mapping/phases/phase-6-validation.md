# Phase 6: Cross-Model Validation

## Purpose

Adversarial review of mapping quality by independent AI models. Different models have different reasoning patterns — errors that one model reproduces may be caught by another.

Read `references/validation-prompt.md` before running the validation script.

## Prerequisites

At least one external AI CLI tool must be installed and authenticated:
- **Codex CLI** (OpenAI) — `npm install -g @openai/codex`
- **Gemini CLI** (Google) — `npm install -g @google/gemini-cli`

## Skip Condition

If neither tool is available:

> "Cross-model validation requires codex and/or gemini CLI. Neither is installed. Skipping validation — you can install them and validate later. Proceeding to export."

Validation is valuable but not blocking.

## Steps

### Step 1: Check Tool Availability

```bash
command -v codex && echo "Codex available" || echo "Codex not installed"
command -v gemini && echo "Gemini available" || echo "Gemini not installed"
```

### Step 2: Run the Validation Script

The validation script is at `scripts/validate-mapping.sh` relative to the plugin root.

```bash
<plugin-root>/scripts/validate-mapping.sh /path/to/mapping-output.json [/path/to/focal-source.json] [/path/to/reference-source.json]
```

The second and third arguments (source files) are optional but strongly recommended. When source files are provided, the reviewers can verify relationship accuracy against the actual source text. When omitted, the validation report explicitly flags reduced confidence.

The script:
1. Loads the review prompt from `references/validation-prompt.md` (not hardcoded)
2. Appends the mapping output and source files (if provided)
3. Writes to a temp file (avoids CLI argument-size limits)
4. Sends to available models in parallel via stdin
5. Saves reviews alongside the output file

### Step 3: Synthesize Reviews

After the script completes, read each review file:
- `<output-name>.codex-review.md`
- `<output-name>.gemini-review.md`

Synthesize:
1. **Both models agree** — high-confidence finding. Present as: "Both Codex and Gemini flagged this."
2. **One model only** — warrants investigation. Present as: "Flagged by [model] only."
3. **Contradictions** — note the disagreement.

### Step 4: Apply Corrections

For validated findings:
- **Type misclassification**: Change the relationship type
- **Directionality error**: Flip the relationship direction
- **Rationale inconsistency**: Correct the rationale
- **Missing "no relationship"**: Add the documentation
- **Unclear finding**: Flag for user judgment

### Step 5: Present to User

> "Validation complete:
> - [N] findings from Codex, [M] from Gemini
> - [X] findings both models agreed on (highest confidence)
> - [Y] corrections applied
> - [Z] findings flagged for your review
>
> Would you like to review any findings in detail?"

## Output

- Validated mapping with corrections applied
- Validation report
- Updated source observations (if validation revealed issues)
