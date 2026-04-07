# Style Selection Guide

Decision logic for choosing relationship style(s) based on the documented use case. Based on NIST IR 8477 §4, Table 2.

## Decision Table

| Your use case looks like... | Recommended style |
|----------------------------|------------------|
| "Point me to related information in B" | **Crosswalk** |
| Diverse concept types at consistent level | **Crosswalk** |
| Weakly related concept types across sources | **Crosswalk** |
| Exploratory first draft | **Crosswalk** (upgrade later) |
| Similar concept types (controls ↔ controls) | **Supportive** |
| Different but strongly related types (requirements ↔ outcomes) | **Supportive** |
| "How does A help achieve B?" | **Supportive** |
| "How similar are these two sets of concepts?" | **Set Theory** |
| Version-to-version comparison | **Set Theory** |
| Most pairs are equal/subset/superset | **Set Theory** |
| Capture hierarchy within a source | **Structural** |

## Common Compositions

| Combination | Use When |
|------------|----------|
| Structural + Supportive | Capture hierarchy then map cross-source relationships |
| Set Theory + Crosswalk | Measure overlap for strong pairs, crosswalk for weak ones |
| Supportive → Crosswalk downgrade | Start detailed, fall back for hard-to-characterize pairs |

## Quick Decision Flow

1. Do you need to characterize HOW concepts relate? → Supportive or Set Theory
2. Do you just need to know THAT they relate? → Crosswalk
3. Are you comparing two similar things? → Set Theory
4. Are you mapping different but related things? → Supportive
5. Do you need the source's internal structure? → Add Structural
