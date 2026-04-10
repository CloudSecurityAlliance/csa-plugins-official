# Evaluation Protocol

Per-pair evaluation process for cross-source styles: B1 (Crosswalk), B2 (Supportive), B3 (Set Theory). Read this file before evaluating any concept pair in Phase 4a. Do not start mapping without reading it.

This file defines the **process** only. The complete output schema — all field names, types, and structure — is in `references/output-formats/internal-format.md`. Produce the full record as defined there; do not use a simplified format.

## Positive Pair Protocol (9 Steps)

For each candidate concept pair:

### Step 1: Read both concepts fully

Read the complete text of both concepts before classification. Do not skim. Misclassification almost always traces to reading a concept partially.

### Step 2: Capture source text

Quote the relevant portion of each concept verbatim. For licensed content (ISO standards, etc.), quote the minimum excerpt needed to support your justification. Set `reference_concept_text` to `"[licensed — not reproduced]"` and put excerpts in `text_evidence[].excerpt`.

### Step 3: Check identical

Is the wording the same word-for-word? If yes: classify as `identical`, record in `evaluation_steps`, stop. No further checks needed.

### Step 4: Check equivalent

Is the meaning the same despite different wording? If yes: classify as `equivalent`, record in `evaluation_steps`, stop.

### Step 5: Check contrary

Do any elements contradict each other? This is independent of whether the pair also has a supportive relationship — a pair can be both `supports` and `contrary` on different elements. Check contrary even if you already found a supportive relationship.

### Step 6: Determine support direction

Does A help achieve B (A **supports** B), or does B help achieve A (A **is supported by** B)?

Direction matters. "A supports B" means A is the enabler. Ask: *which concept is the goal being achieved?* That concept is B.

### Step 7: Assign property (supportive style only, optional)

- **Example of**: A is one way of achieving B; B could be achieved without A
- **Integral to**: A is a component of B; B cannot be achieved without A
- **Precedes**: A must happen before B; A is a prerequisite but not a component

If none fit cleanly, omit the property. Do not force one.

### Step 8: Record alternatives considered

List each other relationship type you considered and specifically why it was rejected. At minimum, record the direction you did not choose.

### Step 9: Tag confidence and source observations

- **High**: Clear textual evidence, unambiguous relationship
- **Medium**: Reasonable interpretation, some ambiguity
- **Low**: Judgment call, significant uncertainty

Capture ambiguities, granularity mismatches, or wording problems in `source_observations[]`.

---

## evaluation_steps Format

String array. Each step follows: `"<check>: <result> — <reason>"`. All checks must be recorded, even when the result is "no":

```json
[
  "identical: no — wording differs significantly",
  "equivalent: no — A is narrower in scope, addressing only provisioning not full lifecycle",
  "contrary: no — no contradicting elements found",
  "direction: A supports B — A's requirements are a component of achieving B; B is the goal",
  "property: integral to — B cannot be achieved without A's controls being in place"
]
```

## alternatives_considered Format

```json
[
  {"type": "is supported by", "rejected_because": "B does not help achieve A; A is the enabler, not the other way around"},
  {"type": "equivalent", "rejected_because": "A is narrower — covers only identity provisioning, not full access governance"}
]
```

Always include at least one entry — the direction or type you did not choose.

## text_evidence Format

```json
[
  {"source": "focal", "excerpt": "The organization shall establish procedures for provisioning and de-provisioning user accounts including approval, assignment of privileges, and periodic review..."},
  {"source": "reference", "excerpt": "[licensed — minimum excerpt] ...identity lifecycle management including provisioning, de-provisioning, and periodic review..."}
]
```

For licensed reference content, quote only what is necessary to substantiate the justification. When even excerpt reproduction is uncertain, omit the reference entry from `text_evidence` and note in `source_observations[]`.

---

## Negative Pair Protocol (5 Steps)

For each concept pair determined to have no relationship:

### Step 1: Read both concepts fully

### Step 2: Identify the closest possible relationship

What would this pair be if it *did* qualify? Name the relationship type and direction.

### Step 3: Explain why the closest relationship is insufficient

Be specific. Cite the content difference that disqualifies it. "Different domains" is not enough — say what specifically is different and why it matters.

### Step 4: Record the counterfactual

What would need to be true for a relationship to exist? Record as an `evaluation_steps[]` string:
`"counterfactual: a relationship would exist if A included organizational governance requirements, which it does not"`

### Step 5: Tag confidence

- **High**: The absence of a relationship is clear — the two concepts address entirely different security concerns with no substantive overlap
- **Medium**: The absence is reasonable but there is some thematic similarity that required judgment to dismiss
- **Low**: The pair is genuinely ambiguous — a different evaluator might find a weak relationship

Record as the `confidence` field of the `no_relationships[]` entry.

---

Output from the negative pair protocol goes into the `no_relationships[]` array in the output document (not into `mappings[]`). The field names and structure for no_relationship records are defined in `references/output-formats/internal-format.md`.

## Negative evaluation_steps Format

```json
[
  "closest considered: supports (A→B)",
  "rejected because: A addresses data residency requirements (where data is stored); B addresses access authentication (who can access it) — different operational domains with no content overlap",
  "counterfactual: a relationship would exist if A included authentication requirements or B included data locality requirements, which neither does"
]
```

## closest_relationship_considered Format

```json
{
  "type": "supports",
  "considered_because": "both involve data handling at the technical level",
  "rejected_because": "A is about where data is stored (residency/sovereignty); B is about who can access it (authentication) — different operational concerns with no substantive overlap"
}
```

---

## B4 Structural Note

This protocol applies to cross-source styles (B1, B2, B3) only. For structural (B4) mapping — which captures hierarchy within a single source — use this single `evaluation_steps` entry:

```json
["hierarchy captured: parent [concept X], child [concept Y] — verified against [section/heading name] of source document"]
```

B4 entries are exempt from `alternatives_considered` and `text_evidence`.
