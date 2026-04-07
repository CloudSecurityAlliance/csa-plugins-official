# Phase 3: Style Selection

## Purpose

Recommend which relationship style(s) to use based on the documented use case.

Read `references/style-selection-guide.md` for the full decision logic. Read `references/relationship-types.md` if you need to explain what each style offers.

## Steps

### Step 1: Analyze the Use Case

Look at the documented use case (Phase 2 output) and match against the style selection criteria:

| Use Case Signal | Points Toward |
|----------------|--------------|
| "How does standard A help satisfy standard B?" | **Supportive** — characterizes how A helps achieve B |
| "How much do these two similar standards overlap?" | **Set Theory** — measures commonality |
| "Point me to related information in standard B" | **Crosswalk** — uncharacterized pointers |
| "What changed between v1.0 and v2.0?" | **Set Theory** — version-to-version comparison |
| "What's the structure of this framework?" | **Structural** — hierarchy capture |
| Sources have similar concept types (controls ↔ controls) | Supportive or Set Theory |
| Sources have different but related types (requirements ↔ outcomes) | Supportive |
| Sources have weakly related types | Crosswalk |
| Exploratory / first draft | Crosswalk (can upgrade later) |

### Step 2: Consider Multiple Styles

NIST §4.6 explicitly supports composing multiple styles on the same source pair:

- **Structural + Supportive**: Capture hierarchy (structural) then map cross-source relationships (supportive). Provides scaffolding plus substance.
- **Set Theory + Crosswalk**: Measure overlap (set theory) for most pairs, fall back to crosswalk for pairs that are weakly related.
- **Supportive → Crosswalk downgrade**: Start with supportive, downgrade to crosswalk for pairs where the relationship exists but can't be well-characterized.

When recommending multiple styles, explain which style serves which purpose.

### Step 3: Present Recommendation

> "Based on your use case, I recommend:
>
> **[Primary style]** because [rationale tied to use case signals]
> [Optional: **+ [Secondary style]** because [rationale]]
>
> Does this feel right, or would you prefer a different approach?"

### Step 4: User Confirms or Overrides

If the user overrides, accept their choice. They may have domain knowledge that changes the calculus.

### Step 5: Load Style Reference

Load the selected style file(s) from `styles/`:
- `styles/crosswalk.md` for B1
- `styles/supportive.md` for B2
- `styles/set-theory.md` for B3
- `styles/structural.md` for B4

Only load the selected style(s) — don't burden the context with styles not being used.

### Multi-Style Composition Rules

When multiple styles are selected:
- **Deduplication**: Same concept pair in multiple styles — keep all, tagged by style
- **Style conversion**: Set theory can convert to supportive (except "intersects with") per `references/style-conversion.md`
- **Richer-wins**: If both a crosswalk and a typed relationship exist for the same pair, the typed relationship is primary

## Output

Selected style(s) with rationale. Style file(s) loaded into context. Ready for Phase 4.

## Teaching Moment (if teaching mode is on)

> **Why not always use the most detailed style?** More detail isn't always better. Crosswalks are fast and useful when you just need pointers. Set theory is great for "how similar are these two things?" but doesn't tell you *how* one helps achieve the other. Supportive is the richest for cross-source relationships but takes the most effort per pair. Match the style to what your audience actually needs — not to what's theoretically most complete.
