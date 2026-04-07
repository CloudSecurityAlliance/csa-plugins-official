# Style Conversion

NIST IR 8477 §4.6 defines how relationship styles can be converted between each other. This enables interoperability when combining mappings from different styles.

## Conversion Table

### Set Theory → Supportive (mostly automatic)

| Set Theory | Supportive Equivalent |
|------------|----------------------|
| Subset of | Supports (integral to) |
| Equal | Equivalent |
| Superset of | Is supported by (integral to) |
| Intersects with | **Cannot be automatically converted** |

**Intersects with** can either:
- Be downgraded to a crosswalk (losing the overlap information), or
- Be manually re-evaluated by an SME as a supportive relationship

### Any Style → Crosswalk (always possible)

All styles can be trivially downgraded to crosswalks by stripping all relationship types and properties. Only concept pairs remain.

### Crosswalk → Other Styles (manual only)

Upgrading from crosswalk to a more detailed style requires manual re-evaluation of every pair. The crosswalk provides no relationship metadata to convert from.

## Context Warning

"When converting mappings in a way that attempts to preserve relationship meaning, it is important to consider the assumptions and other context captured related to the mapping being converted." [NIST §4.6]

Conversion is mechanical — but the MEANING may shift between contexts. A "subset of" in a syntactic set-theory mapping converts to "supports (integral to)" in supportive, but the supportive relationship carries different connotations in a different use case.
