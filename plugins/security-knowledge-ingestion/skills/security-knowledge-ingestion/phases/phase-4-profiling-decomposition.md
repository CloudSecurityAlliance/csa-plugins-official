# Phase 4: Profiling & Decomposition

## Purpose

AI-driven comprehension. This is where the document is *understood*, not just cleaned. Classify the document, identify its structure, and decompose it into individually addressable concepts.

Read `references/concept-types.md` and `references/confidence-framework.md` before starting this phase.

## Two Modes

This phase operates differently depending on what arrived from Phase 2/3:

- **Full processing**: Input is clean markdown — do everything below.
- **Verification**: Input is already-structured data (JSON/CSV from user or SecID v2) — verify the structure is correct, flag issues, and proceed. Don't redo work that's already done unless the user asks.

## Steps (Full Processing)

### Step 1: Profile the Document

Classify along these dimensions:

**Document type:**
- Standard (defines requirements/controls for conformance)
- Regulation (legally binding requirements)
- Framework (organizes practices/controls, not necessarily for conformance)
- Guidance (recommendations, best practices, how-to)
- Benchmark (specific configuration/implementation requirements)
- Methodology (process for producing analysis/scores/mappings)
- Reference (informational, no requirements)

**Concept types present** (may have multiple — see `references/concept-types.md`):
- Controls, requirements, outcomes, capabilities, recommendations, articles, clauses, sections, techniques, procedures, functions, categories

**Hierarchy model:**
- Flat list (e.g., a simple control catalog)
- Two-level (e.g., domains → controls)
- Three-level (e.g., functions → categories → subcategories)
- Deep hierarchy (e.g., chapters → articles → sections → paragraphs)
- Mixed (different parts of the document use different structures)

Tag each classification with a confidence level per `references/confidence-framework.md`.

### Step 2: Identify the Hierarchy

Map out the document's structure before decomposing:

1. What are the top-level groupings? (chapters, domains, functions, etc.)
2. What are the leaf-level concepts? (individual controls, requirements, articles, etc.)
3. How many levels are there between top and leaf?
4. Are there cross-references within the document? (e.g., "see also control X")
5. Are there concepts at multiple levels that are independently addressable?

Draw out the hierarchy. For example:

```
NIST CSF 2.0:
  Functions (6)
    └── Categories (22)
        └── Subcategories (106)

CCM 4.1:
  Domains (17)
    └── Controls (207)

EU AI Act:
  Titles (13)
    └── Chapters (variable)
        └── Articles (113)
            └── Paragraphs (variable)
```

### Step 3: Decompose into Individual Concepts

For each leaf-level concept (and meaningful intermediate levels), extract:

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Identifier as used in the source — preserve exactly | `AC-2`, `IAM-12`, `Art. 6(1)(a)` |
| `title` | Name/title if the source provides one | "Account Management", "Identity & Access Management" |
| `description` | Full text of the concept | The complete control text, requirement text, or article text |
| `concept_type` | What kind of concept this is | `control`, `requirement`, `article`, `subcategory` |
| `hierarchy_level` | Where in the hierarchy this sits | `domain`, `control`, `function`, `category` |
| `parent_id` | ID of the parent concept (null for top-level) | `IAM` (for `IAM-12`), `Title III` (for `Art. 6`) |
| `metadata` | Any additional structured information from the source | Applicability notes, CSP/CSC perspective, effective dates |
| `cross_references` | References to other concepts within the same document | `["AC-3", "AC-6"]` |

**Rules:**
- **Preserve source identifiers exactly.** If the source says `A.5.1`, use `A.5.1`. Don't normalize to `A.05.01` or `A-5-1`.
- **Include all addressable levels.** If the source has both domains and controls, include both as concepts — don't skip the domains.
- **Canonical concepts match the source structure.** If the source treats something as one control, it's one canonical concept. The source document is authoritative on its own structure.
- **Derived sub-concepts are optional.** When a single source concept contains multiple distinct requirements (common in legal/regulatory text — e.g., one article with 5 sub-paragraphs), you may create derived sub-concepts in addition to the canonical concept. Derived sub-concepts must link back to their canonical parent and be clearly marked as derived (not source-level). This supports downstream mapping precision without misrepresenting the source structure.
- **When in doubt, match the source.** Canonical concepts always exist. Derived sub-concepts are added only when the user confirms they're useful for their downstream use case.

### Step 4: Tag with Confidence

Every AI-produced decision carries a confidence level (see `references/confidence-framework.md`):

- Document type classification: typically High (clear from the document itself)
- Hierarchy identification: typically High for well-structured documents, Medium for documents with inconsistent structure
- Concept decomposition: varies — High for clearly delineated controls, Medium for prose-heavy regulations where concept boundaries are interpretive
- ID extraction: High when IDs are explicit, Medium when inferred from numbering
- Cross-reference detection: Medium (may miss implicit references)

### Step 5: Record Prompts Used

For the recipe (Phase 5), record:
- The prompts used for profiling and decomposition (exact text)
- Any iterative refinements (if you re-prompted after reviewing initial results)
- Decisions you made about ambiguous structures and why

## Steps (Verification Mode)

When input is already-structured data:

1. **Spot-check concept count**: Does the number of concepts match what you'd expect from the source?
2. **Verify hierarchy**: Does the parent-child structure match the source document's organization?
3. **Check a sample**: Read 5-10 concepts and compare against the source — are IDs, titles, and descriptions faithful?
4. **Flag issues**: If anything looks wrong, tell the user. Don't silently accept.
5. **If the user wants full re-processing**: Treat the structured data as a reference and do full processing from the markdown.

## Pause

Present the decomposition to the user:

> "Here's the decomposition:
> - Document type: {type} [confidence]
> - Hierarchy: {N levels} — {description}
> - Concepts found: {total} ({breakdown by level})
> - Sample (first 5 at each level):
>   {show a few examples}
>
> Does this look right? Anything missing or miscategorized?"

Wait for the user's response. Correct anything they flag before proceeding.

## Output

Structured data (JSON or YAML) with:
- Document-level metadata (title, publisher, version, type, hierarchy description)
- Array of concepts, each with: id, title, description, concept_type, hierarchy_level, parent_id, metadata, cross_references
- Confidence tags on AI-produced classifications

## Teaching Moment (if teaching mode is on)

> **Why decomposition matters:** A 200-page standard is useful to humans who read it front to back. But for mapping, searching, cross-referencing, and automated analysis, you need individual concepts you can point at. "NIST 800-53 control AC-2" is actionable. "Page 47 of a PDF" is not. Decomposition turns documents into databases of addressable knowledge — which is exactly what SecID, mapping engines, and compliance tools need.
