# Style: Supportive Relationship Mapping (B2)

NIST IR 8477 §4.2

## Definition

Supportive relationship mapping indicates **how** a supporting concept can or does help achieve a supported concept.

## Relationship Types

| Type | Meaning | Directional? |
|------|---------|-------------|
| **Supports** | A can be applied alone or in combination with others to achieve B in whole or in part | Yes (A→B) |
| **Is supported by** | A is achieved through B alone or in combination with others | Yes (A←B) |
| **Identical** | A and B use exactly the same wording | No |
| **Equivalent** | A and B have the same meaning but different wording | No |
| **Contrary** | One or more elements of A contradict one or more elements of B. Contradictions may be opposites but don't have to be. | No |
| **No relationship** | A and B are not related or not sufficiently related | No |

## Relationship Properties (Optional — Supports and Is Supported By only)

| Property | Meaning | Test |
|----------|---------|------|
| **Example of** | C is one way of achieving D in whole or in part. D could be achieved without C. | Can you accomplish D without C? If yes → example of |
| **Integral to** | C is integral to and a component of D. C must be applied as part of achieving D. | Can you accomplish D without C? If no → integral to |
| **Precedes** | C must be achieved before D. C is a prerequisite for D but is not part of D. | Must C happen first? Is C not itself a component of D? If both yes → precedes |

**No properties exist** for Identical, Equivalent, Contrary, or No Relationship.

## Evaluation Process

For each concept pair:

1. **Read both concepts fully** — understand the full text of each
2. **Check for identical/equivalent first** — if the wording is the same (identical) or the meaning is the same (equivalent), that's the simplest classification
3. **Check for contrary** — do any elements contradict? This is independent of whether they also overlap.
4. **Determine support direction** — does A help achieve B (supports), or does B help achieve A (is supported by)?
5. **Assign property** (optional) — for supports/is-supported-by, determine if the relationship is example-of, integral-to, or precedes. If none fit well, omit the property.
6. **Document justification** — cite specific text from both concepts that supports your classification
7. **Tag confidence**

## Context Sensitivity Warning

"The relationship types and properties are unlikely to have exactly the same meaning in different mappings because each use case will be different." [NIST §4.2]

Always interpret types and properties in the context of THIS mapping's use case. Don't assume "supports" means the same thing here as in a different mapping with different assumptions.

## Common Pitfalls

- **Confusing supports with is-supported-by**: Direction matters. "A supports B" means A helps achieve B, not the reverse.
- **Forcing a property**: Properties are optional. If none of the three (example of, integral to, precedes) fits cleanly, omit the property rather than forcing one.
- **Missing contrary relationships**: Two concepts can overlap (supports) AND contradict (contrary) on different elements. Check for both.
- **Ignoring identical/equivalent**: If the wording or meaning is the same, say so. Don't force a supports/is-supported-by when identical or equivalent is accurate.

## Output Format

Follow the full record format specified in `references/evaluation-protocol.md`. That document defines the required fields for both positive and negative pairs. The canonical schema is in `references/output-formats/internal-format.md`. Do not use a simplified per-pair format — produce the full rich record from pair one.
