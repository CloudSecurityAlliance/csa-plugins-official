# Phase 4: Mapping Execution (Sample)

## Purpose

Map a representative sample of concept pairs to validate the approach before committing to a full run. Per NIST §5: "start a new mapping by documenting a representative sample."

Load the appropriate style file(s) from `styles/` before starting. The style file contains the specific relationship types, evaluation guidance, and pitfalls for the selected style.

## Steps

### Step 1: Select the Sample

Choose 10-20 concept pairs that represent the breadth of the mapping:

- Include pairs from different areas of both sources (don't cluster in one domain)
- Include pairs where the relationship seems strong AND pairs where it seems weak or absent
- Include pairs at different hierarchy levels if applicable
- If the sources are large, sample proportionally across sections

### Step 2: Evaluate Each Pair

For each concept pair, follow the style-specific evaluation process (detailed in the loaded `styles/*.md` file). Regardless of style, every evaluation produces:

| Field | Description |
|-------|-------------|
| **Focal concept** | ID and title from the focal document |
| **Reference concept** | ID and title from the reference document |
| **Relationship type** | The style-specific type (e.g., "supports", "subset of", or just "related" for crosswalk) |
| **Rationale** | (Set theory only) Syntactic, semantic, or functional |
| **Property** | (Supportive only, optional) Example of, integral to, or precedes |
| **Justification** | WHY this relationship type was chosen — citing evidence from both sources |
| **Confidence** | High, Medium, or Low (see `references/confidence-framework.md`) |
| **Source observations** | Any ambiguities, granularity issues, or wording problems noticed |

### Step 3: Document "No Relationship" Findings

For pairs considered but found unrelated, document them explicitly:

- Which pair was considered
- Why no relationship exists (different scope, different abstraction level, genuinely unrelated)
- "No relationship" is a finding, not an absence of a finding

### Step 4: Capture Source Observations

During mapping, you'll notice things about the sources:

- Ambiguous wording that could be interpreted multiple ways
- Granularity mismatches between the two sources
- Duplicate or overlapping concepts within a single source
- Terminology differences that obscure real relationships
- Missing concepts that you'd expect to find

Record all of these. Per NIST §5: "Mapping can highlight ambiguities with wording, differences in granularity, duplication of concepts, and other issues within either of the sources being mapped. Be sure to capture and share these observations."

### Step 5: Record Prompts

For the reproducibility recipe, record:
- The prompts used for evaluation (exact text or reference to versioned prompt)
- Any iterative refinements made during the sample

## Output

Sample mapping (10-20 pairs) with typed, justified relationships. Proceed to Phase 5 for review before completing the full mapping.

## Teaching Moment (if teaching mode is on)

> **Why sample first?** Systematic errors compound. If your interpretation of "supports" is subtly wrong on pair #3, it'll be wrong on all 200 pairs. Catching that on a 15-pair sample saves you from redoing the whole mapping. This isn't a shortcut — it's how NIST recommends doing it. The sample also helps calibrate: after 15 pairs, you develop a feel for how the two sources relate, which makes the full run faster and more consistent.
