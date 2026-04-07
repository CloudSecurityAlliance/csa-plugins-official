# Confidence Framework for Mapping

Tag every relationship evaluation with a confidence level. This helps users know where to focus review effort and where the mapping is most/least certain.

## Confidence Levels

| Level | Meaning | When to Use |
|-------|---------|-------------|
| **High** | Almost certainly correct — clear textual evidence from both sources | Concepts explicitly address the same topic with clear overlap or clear independence |
| **Medium** | Likely correct but involves interpretation | Relationship depends on how you read the concepts, granularity difference makes comparison inexact, or concept boundaries are fuzzy |
| **Low** | Best guess — significant ambiguity | Concepts are in related domains but the specific relationship is unclear, or the sources use very different terminology for potentially similar ideas |

## What Gets Tagged

Every concept pair evaluation gets a confidence level — including "no relationship" findings.

| Evaluation Aspect | Typical Confidence |
|-------------------|-------------------|
| Identical/equivalent (same or very similar wording) | High |
| Clear supports/subset (obvious overlap) | High |
| Contrary (explicit contradiction) | High |
| Supports with property (example of/integral to/precedes) | Medium to High |
| Intersects with (partial overlap) | Medium |
| Cross-granularity relationships | Medium |
| No relationship (clearly different domains) | High |
| No relationship (related domain, judgment call) | Medium |
| Relationships inferred from context not text | Low |

## Rules

1. **Default to the lower level when uncertain** — Medium not High
2. **Explain Low confidence** — why is this uncertain? What would resolve it?
3. **Confidence is about the evaluation, not the source** — a well-written source enables High confidence evaluations
4. **Aggregate confidence matters** — if 60% of your mapping is Medium or Low, the overall mapping may need more review time
