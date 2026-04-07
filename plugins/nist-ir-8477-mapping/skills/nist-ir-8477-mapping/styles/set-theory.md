# Style: Set Theory Relationship Mapping (B3)

NIST IR 8477 §4.3

## Definition

Set theory relationship mapping is derived from mathematical set theory. Each mapping includes both a **rationale** and a **relationship type**. These are inseparable — a type without a rationale is invalid.

## Rationale (choose one per concept pair)

| Rationale | Question It Answers | Method |
|-----------|-------------------|--------|
| **Syntactic** | How similar is the wording? | Word-for-word analysis. No interpretation of meaning. |
| **Semantic** | How similar are the meanings? | Involves interpretation of each concept's language. |
| **Functional** | How similar are the execution results? | Requires understanding what happens if both concepts are implemented. |

**Multiple rationales may apply.** The evaluator chooses the most useful one for the use case, or may create multiple evaluations for the same pair using different rationales.

**The same pair can have different types under different rationales.** Example: two concepts may "intersect" syntactically (different wording with some overlap) but be "equal" semantically (same meaning despite different words).

## Relationship Types

| Type | Meaning | Symmetric? |
|------|---------|-----------|
| **Subset of** | A is a subset of B. B contains everything A does and more. | No (A⊂B) |
| **Intersects with** | A and B overlap, but each includes content the other does not. | Yes (A∩B) |
| **Equal** | A and B are the same (not necessarily identical wording). | Yes (A=B) |
| **Superset of** | A is a superset of B. A contains everything B does and more. | No (A⊃B) |
| **No relationship** | A and B are unrelated; content does not overlap. | Yes |

## Critical: Intersects With

"Intersects with" is the hardest type and the one most likely to need manual review:

- It's the **only** set theory type that cannot be automatically converted to a supportive relationship (see `references/style-conversion.md`)
- It only tells you there's overlap — not the nature of that overlap
- If most of your pairs are "intersects with," consider whether supportive mapping would serve the use case better

## Evaluation Process

For each concept pair:

1. **Choose the rationale** — syntactic, semantic, or functional. Choose based on what the use case needs.
2. **Read both concepts** through the lens of that rationale:
   - Syntactic: look at the actual words
   - Semantic: interpret the meaning
   - Functional: consider what happens if each is implemented
3. **Determine the set relationship** — is A a subset of B? Do they intersect? Are they equal? Is A a superset? No relationship?
4. **Document both rationale and type** — these are inseparable
5. **Document justification** — explain WHY this type under this rationale
6. **Tag confidence**

## Common Pitfalls

- **Omitting the rationale**: A bare "subset of" is meaningless. Subset syntactically? Semantically? Functionally? Always specify.
- **Mixing rationales within a pair**: If you start with syntactic analysis, finish with a syntactic judgment. Don't switch to semantic reasoning mid-evaluation.
- **Overusing "intersects with"**: This is the vaguest type. If most pairs are "intersects with," the mapping isn't very informative. Consider a different rationale or style.
- **Confusing subset with superset**: Subset means A is SMALLER — B contains everything A does and more. Superset means A is BIGGER.

## Output Format

Per pair:
```json
{
  "focal_concept": "PR.AC-1",
  "reference_concept": "PR.AC-P1",
  "rationale": "semantic",
  "relationship_type": "equal",
  "justification": "Both concepts require identity and credential management for authorized entities. 'Users' (CSF) and 'individuals' (Privacy Framework) have the same meaning in their respective contexts...",
  "confidence": "High"
}
```
