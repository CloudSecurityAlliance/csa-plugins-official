# Style: Concept Crosswalk (B1)

NIST IR 8477 §4.1

## Definition

A concept crosswalk indicates that a relationship exists between two concepts **without any additional characterization**. A relationship statement only says "concept A and concept B are related" — nothing more.

## Relationship Types

None. There are no relationship types in a crosswalk. Just pairs.

## When This Style Was Selected

Crosswalk is appropriate when:
- Pointing to additional information on a topic (informative references)
- Documenting diverse concept types at a consistent level when relationship strength varies significantly
- Mapping two sources with different and weakly related concept types
- As an exploratory first draft before applying a more detailed style

## Evaluation Process

For each concept pair:

1. **Read both concepts fully** — understand what each one says
2. **Determine if a relationship exists** — are these two concepts related in any way that serves the documented use case?
3. **If yes**: Record the pair. No further characterization needed.
4. **If no**: Document as "considered, no relationship found" with a brief note why.
5. **Document justification**: Even though the relationship is uncharacterized, explain WHY you paired these two concepts. The use case documentation is the only context users will have.

## Critical Rule

Because crosswalks carry zero relationship metadata, the **use case documentation from Phase 2 is the only source of contextual information** about what the relationships mean. Make the use case document clear and complete — it carries all the weight.

## Common Pitfalls

- **Over-mapping**: Including every tangential connection. The use case's exhaustiveness setting is your guide.
- **Under-documenting justification**: "They're related" is not a justification. Say WHY they're related.
- **Assuming the user knows**: The person using this crosswalk may not have your context. The use case + justification must stand on their own.

## Upgrade Path

A crosswalk can be upgraded to a more detailed style later:
- Add relationship types → becomes supportive mapping
- Add rationale + types → becomes set theory mapping
- This is why crosswalk works as an exploratory first draft

## Output Format

Follow the full record format specified in `references/evaluation-protocol.md`. That document defines the required fields for both positive and negative pairs. The canonical schema is in `references/output-formats/internal-format.md`. Do not use a simplified per-pair format — produce the full rich record from pair one.

Note for crosswalk (B1): `relationship_type` is `null` — that is the point of a crosswalk. The `style` field identifies this as a crosswalk entry. Include `evaluation_steps` documenting the decision to pair the concepts, and `justification` explaining why they are related.
