# Phase 4b: Negative Mapping

Systematically document no-relationship findings at three levels: individual records, domain summaries, and gap analysis. Run after Phase 4a (full run) completes.

This phase is not optional. The positive mapping alone is not complete — it only shows what maps. Phase 4b proves completeness by showing what doesn't map and why.

## Mandatory Prerequisites

Read ALL of these before starting:

1. **`references/no-relationship-protocol.md`** — three-level negative evidence architecture, ID convention, scale guidance
2. **`references/evaluation-protocol.md`** (Negative Pair Protocol section) — 5-step process for negative pairs
3. **`references/output-formats/internal-format.md`** — schema for `no_relationships[]`, `no_relationship_domains[]`, `gap_analysis{}`

## Process

### Step 1: Identify unmapped concepts

From the Phase 4a output, compile:
- **Unmapped focal concepts**: focal concepts that appear in zero `mappings[]` entries
- **Unsupported reference concepts**: reference concepts that appear in zero `mappings[]` entries (on the reference side)

### Step 2: Generate individual no_relationship records

For each unmapped focal concept and each unsupported reference concept, generate `no_relationship` records using the negative pair protocol from `references/evaluation-protocol.md`.

**Scale policy applies here — check `references/no-relationship-protocol.md` Scale Guidance section** before deciding how many records to generate per concept.

Each record must include: `id` (using `"no_rel_{focal_id}_{reference_id}"` convention), `focal_concept_text`, `reference_concept_text`, `evaluation_steps[]`, `closest_relationship_considered`, `reason`, `confidence`.

### Step 3: Generate domain summaries

Group individual records by domain. For each domain with no_relationship records, write one `no_relationship_domains[]` entry:
- `focal_concepts_with_no_relationship` — list of focal concept IDs with no mappings in this domain
- `individual_record_ids` — complete list of all no_relationship record IDs in this domain
- `structural_reason` — why these concepts don't map (prose, 2-4 sentences)
- `gap_type` — out-of-scope / scope-mismatch / abstraction-mismatch / genuine-gap

### Step 4: Synthesize gap analysis

Write `gap_analysis{}`:
1. List `reference_concepts_with_no_support` (IDs, titles, reason)
2. List `focal_concepts_with_no_mapping` (IDs, titles, domain, reason)
3. Compute `coverage_percentage` from the mappings and no_relationships counts
4. Write `structural_findings[]`

**Write `structural_findings[]` before computing statistics.** The findings — interpreting what the negative evidence means about the relationship between the two frameworks — are the product. The coverage percentages are scaffolding. Each finding: 2-5 sentences explaining a pattern.

## Output

The `no_relationships[]`, `no_relationship_domains[]`, and `gap_analysis{}` sections of the internal-format JSON. Merge with the Phase 4a positive mappings to produce the complete mapping document.

After completing this phase, proceed to the enforcement checkpoint in SKILL.md before Phase 6.
