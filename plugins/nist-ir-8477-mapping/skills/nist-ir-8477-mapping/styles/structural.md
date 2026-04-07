# Style: Structural Relationship Mapping (B4)

NIST IR 8477 §4.4

## Definition

Structural relationship mapping captures an inherent hierarchical structure of concepts, usually defined within a single source. The relationship type is **parent-child** only.

## How B4 Works in This Plugin

In a two-source mapping engagement, structural mapping serves a supplementary role:

- **Capture the hierarchy** of one or both sources as scaffolding
- **Complement cross-source styles** (B1-B3) by providing the structural context that cross-source relationships sit within

Structural mapping does not characterize cross-source relationships — that's what the other styles do. B4 tells you "IAM-12 is a child of the IAM domain" not "IAM-12 relates to AC-2."

In **exploratory mode** (Phase 1, one source), structural mapping is the primary output — profiling the source's hierarchy for planning purposes.

## Relationship Types

| Type | Meaning |
|------|---------|
| **Parent-child** | Child concept is part of parent concept |

Parent-child does not specify whether the child is required or optional for achieving the parent.

## Key Properties

- **Fully objective**: Based only on the source's intrinsic published structure. No interpretation involved.
- **Single-source**: Captures hierarchy within one document, not between two.
- **Complementary**: A second mapping using B1, B2, or B3 supplements structural relationships with cross-source meaning.

## Evaluation Process

For each concept in the source:

1. **Identify the parent** — what grouping does this concept belong to in the source document?
2. **Record the parent-child relationship** — concept X is a child of concept Y
3. **Verify against the source** — the hierarchy must match what the source document declares, not what seems more logical
4. **Note irregularities** — some documents have inconsistent hierarchy (e.g., some controls are at level 2, others at level 3 with no apparent pattern)

## Common Pitfalls

- **Inventing hierarchy**: If the source document has a flat list, it's a flat list. Don't impose groupings that aren't there.
- **Confusing document structure with concept structure**: A heading in the PDF is not necessarily a parent concept. Check whether the source treats it as a grouping or just a formatting choice.
- **Depth inconsistency**: Some frameworks have different depths in different sections. Capture what's there, don't normalize to a uniform depth.

## Output Format

Per relationship:
```json
{
  "source": "secid:control/nist.gov/csf@2.0",
  "parent_concept": "DE.AE",
  "child_concept": "DE.AE-07",
  "relationship": "parent-child",
  "confidence": "High"
}
```

For a complete hierarchy:
```json
{
  "source": "secid:control/nist.gov/csf@2.0",
  "hierarchy": [
    {
      "concept": "DE",
      "level": "function",
      "children": [
        {
          "concept": "DE.AE",
          "level": "category",
          "children": [
            {"concept": "DE.AE-01", "level": "subcategory"},
            {"concept": "DE.AE-07", "level": "subcategory"}
          ]
        }
      ]
    }
  ]
}
```
