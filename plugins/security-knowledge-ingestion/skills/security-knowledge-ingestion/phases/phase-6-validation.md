# Phase 6: Validation

## Purpose

Cross-model adversarial review of decomposition quality. Independent AI models check the structured output for errors that the producing model might not catch.

Read `references/validation-prompt.md` before running the validation script.

## Prerequisites

At least one external AI CLI tool must be installed and authenticated:
- **Codex CLI** (OpenAI) — `npm install -g @openai/codex`
- **Gemini CLI** (Google) — `npm install -g @google/gemini-cli`

## Skip Condition

If neither tool is available, inform the user:

> "Cross-model validation requires codex and/or gemini CLI. Neither is installed. Skipping validation — you can install them and validate later. Proceeding to export."

Validation is valuable but not blocking. Proceed to Phase 7.

## Steps

### Step 1: Check Tool Availability

```bash
command -v codex && echo "Codex available" || echo "Codex not installed"
command -v gemini && echo "Gemini available" || echo "Gemini not installed"
```

### Step 2: Run the Validation Script

The validation script is at `scripts/validate-decomposition.sh` relative to the plugin root. Resolve the plugin root from this skill's location (up two directories from `skills/security-knowledge-ingestion/`).

```bash
<plugin-root>/scripts/validate-decomposition.sh /path/to/structured-output.json
```

The script sends the structured output along with a review prompt (from `references/validation-prompt.md`) to all available models in parallel. Each model independently reviews for these error patterns:

- **Completeness**: Did the decomposition miss concepts from the source?
- **Phantom concepts**: Did it create concepts that don't exist in the source?
- **Merging errors**: Were two distinct concepts merged into one?
- **Splitting errors**: Was one concept split into multiple?
- **Hierarchy accuracy**: Is the parent-child structure correct?
- **Metadata accuracy**: Are concept types, IDs, and descriptions faithful to the source?
- **Boundary accuracy**: Are concept boundaries drawn where the source draws them?

### Step 3: Read and Synthesize Reviews

After the script completes, read each review file:
- `<output-name>.codex-review.md`
- `<output-name>.gemini-review.md`

Synthesize:

1. **Both models agree** — high-confidence error. Present as: "Both Codex and Gemini flagged this."
2. **One model only** — warrants investigation. Present as: "Flagged by [model] only."
3. **Contradictions** — one says it's wrong, the other says it's fine. Note the disagreement.

For each finding, assess:
- Is this a valid correction? (Reviewing models can also be wrong.)
- Does it require changing the structured output?
- Does it require re-checking the source document?

### Step 4: Apply Corrections

For validated findings:
- **Missing concept**: Add it to the structured output
- **Phantom concept**: Remove it
- **Merge/split error**: Restructure to match the source
- **Hierarchy error**: Fix parent-child relationships
- **Metadata error**: Correct the specific field
- **Unclear finding**: Flag for the user's judgment

After corrections, update the recipe (Phase 5 output) to note what was corrected and why.

### Step 5: Present to User

> "Validation complete:
> - {N} findings from Codex, {M} from Gemini
> - {X} findings both models agreed on (highest confidence)
> - {Y} corrections applied
> - {Z} findings flagged for your review
>
> Would you like to review any findings in detail?"

Wait for the user's response before proceeding.

## Output

- Validated structured data (with corrections applied)
- Validation report (findings, corrections, flagged items)
- Updated recipe (noting corrections)

## Teaching Moment (if teaching mode is on)

> **Why different models matter:** Using different AI models from different providers for validation is deliberate. Each model has its own training data, knowledge cutoffs, and reasoning patterns. An error that one model reproduces (because it shares the same blind spot) may be caught by another model that doesn't. This is the same principle behind using diverse tools in security testing — a single scanner misses things that a diverse set catches.
>
> **The "both agree" signal:** When two independent models flag the same issue, that's a strong signal it's a real error. Treat these as near-certain corrections. Single-model findings are worth investigating but may be false positives.
