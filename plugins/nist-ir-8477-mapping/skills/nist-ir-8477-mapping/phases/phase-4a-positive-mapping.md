# Phase 4a: Positive Mapping

Evaluate concept pairs and document positive relationships. This phase covers both the initial sample (10-20 pairs → Phase 5 review) and the full run (all remaining pairs, after Phase 5 approves the approach).

## Mandatory Prerequisites

Read ALL of these before evaluating any pair. The order matters.

1. **`references/evaluation-protocol.md`** — the 9-step positive pair process and required output fields
2. **`references/output-formats/internal-format.md`** — the complete schema every record must conform to
3. **The selected `styles/*.md` file** — relationship types, evaluation guidance, and pitfalls for the chosen style
4. **The use case document from Phase 2** — the exhaustiveness setting determines which pairs to evaluate

Do not evaluate any pair before completing this reading. Missing fields and misclassifications trace almost always to skipping prerequisites.

## Candidate Pair Generation

Before mapping, generate the set of pairs to evaluate. Do NOT evaluate every possible combination — for N focal and M reference concepts, N×M pairs is impractical and mostly noise.

**Pruning strategies:**
- **Concept type matching**: Only pair concepts of compatible types (controls with controls, not controls with domain headings)
- **Exhaustiveness filter**: If the use case says "strongest direct only," pre-filter to pairs with obvious topical overlap (same security domain, similar keywords, related functions)
- **Domain/category pre-filtering**: Group by domain and pair within related groups first
- **Hierarchy-aware pairing**: Match at appropriate hierarchy levels

Document the candidate generation strategy in `metadata.candidate_generation_strategy`.

## Sample vs. Full Run

Phase 4a is used twice:

**Sample run (10-20 pairs):** Select a representative breadth sample — include strong-relationship pairs AND weak-or-absent-relationship pairs, from different domains. After the sample, proceed to Phase 5 review.

**Full run (all remaining pairs):** After Phase 5 approves the approach, map all remaining candidate pairs. Include the sample pairs already mapped — do not redo them unless corrections changed the approach.

The per-pair process is identical for both runs. The only difference is scope.

## Full Rich Record from Pair One

Do not produce a simplified record with intent to upgrade later. Every pair produces the complete record as defined in `references/output-formats/internal-format.md`, including:

- `focal_concept_text` and `reference_concept_text` (full verbatim text)
- `evaluation_steps[]` (all 9 steps documented per `references/evaluation-protocol.md`)
- `alternatives_considered[]` (at least one entry)
- `text_evidence[]` (at least one entry per source)
- `justification` (substantive prose citing both sources — not one sentence)
- `confidence` and `source_observations[]`

## Domain Batching for Large Sources

For sources with 100+ concepts, evaluate one domain batch at a time:

1. Identify all concepts in both sources belonging to Domain X
2. Generate candidate pairs within Domain X
3. Evaluate all pairs in Domain X, producing full rich records
4. Record domain-level source observations before moving to Domain X+1
5. Proceed to next domain

Domain batching provides natural session checkpoints.

## Automation Spectrum

- **Interactive**: Evaluate each pair together, discuss. Best for first-time use or ambiguous sources.
- **Semi-automated**: Batch-process pairs by domain, pause at domain boundaries for review.
- **Fully automated**: Process all pairs, present complete results for review.

## Capturing Source Observations

During mapping, record observations about the sources themselves in `source_observations[]`:
- Ambiguous wording that could be interpreted multiple ways
- Granularity mismatches (one source at control level, the other at domain level)
- Duplicate or overlapping concepts within a single source
- Terminology differences that obscure real relationships

## Output

**After sample run**: Sample mapping (10-20 pairs with full rich records) → Phase 5 review.

**After full run**: Complete positive mapping (all candidate pairs) → Phase 4b negative mapping.
