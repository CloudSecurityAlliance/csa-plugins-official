# Relationship Types Quick Reference

All four NIST IR 8477 relationship styles in one reference. For detailed evaluation guidance, see the style-specific files in `styles/`.

## B1: Crosswalk (§4.1)

No relationship types. Just concept pairs. Use case documentation provides all context.

## B2: Supportive (§4.2)

| Type | Direction | Meaning |
|------|-----------|---------|
| Supports | A→B | A helps achieve B |
| Is supported by | A←B | A is achieved through B |
| Identical | — | Same wording |
| Equivalent | — | Same meaning, different wording |
| Contrary | — | Elements contradict |
| No relationship | — | Unrelated |

**Properties** (optional, Supports/Is Supported By only): Example of, Integral to, Precedes

## B3: Set Theory (§4.3)

**Rationale** (required): Syntactic, Semantic, or Functional

| Type | Meaning | Symmetric? |
|------|---------|-----------|
| Subset of | A ⊂ B | No |
| Intersects with | A ∩ B ≠ ∅ | Yes |
| Equal | A = B | Yes |
| Superset of | A ⊃ B | No |
| No relationship | A ∩ B = ∅ | Yes |

## B4: Structural (§4.4)

| Type | Meaning |
|------|---------|
| Parent-child | Child is part of parent |

Single-source, fully objective.

## Style Conversion (§4.6)

| Set Theory → | Supportive |
|-------------|-----------|
| Subset of | Supports (integral to) |
| Equal | Equivalent |
| Superset of | Is supported by (integral to) |
| Intersects with | **Cannot auto-convert** |
| All styles | → Crosswalk (strip all types) |
