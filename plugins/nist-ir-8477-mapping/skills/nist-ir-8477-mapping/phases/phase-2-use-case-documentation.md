# Phase 2: Use Case Documentation

## Purpose

Document the five NIST IR 8477 §3 assumptions before any mapping begins. This is mandatory — you cannot proceed to mapping without a documented use case.

Read `references/relationship-types.md` if you need to understand the available styles while discussing concept types and direction.

## Why This Matters

"Mapping is often conducted as an abstract exercise without explicitly determining, documenting, or communicating the mapping's purpose, use cases, scope, audience, or other assumptions. As a result, people who use the mapping must guess at its meaning and context." — NIST IR 8477 §1

The use case is the foundation everything else builds on. Style selection, exhaustiveness, direction — all flow from the use case.

## Steps

Walk through each assumption interactively. For each, explain what it means, present options where applicable, and let the user decide.

### Assumption 1: Intended Users

> "Who will use this mapping? What skills and knowledge do they have?"

Examples:
- CISOs and risk officers evaluating compliance overlap
- Security engineers implementing controls
- Auditors verifying conformance
- GRC tool vendors building automated crosswalks
- Tools and technologies (machine consumption)

Document the expected skills and knowledge level — a mapping for auditors needs different depth than one for automation tools.

### Assumption 2: Purpose

> "Why would someone use this mapping? What question does it answer?"

Prompt the user to complete: "[Target audience] need to [action] by [using this mapping to...]"

Examples:
- "CISOs need to determine how meeting standard A requirements helps satisfy standard B recommendations"
- "Engineers need to know which controls in framework A correspond to controls in framework B"
- "Auditors need to verify that compliance with standard A provides evidence for standard B"

### Assumption 3: Concept Types

> "What types of concepts are being mapped from each source?"

Check what the sources contain (from Phase 1 profiling) and confirm with the user:

- Are you mapping controls to controls? Controls to requirements? Requirements to outcomes?
- If both sources have multiple concept types, are you mapping all of them or a specific subset?
- "Combining multiple concept types from each source into a single mapping may be more confusing than defining multiple use cases and having a separate mapping for each one." [NIST §3]

Also discuss **granularity**: at what level are you mapping?
- "Just because you can map at the lowest level does not mean you should." [NIST §3]
- If a source has 10 high-level concepts, 100 mid-level, and 1000 low-level, mapping all 1000 may be impractical and unnecessary for the audience.

### Assumption 4: Direction

> "Which direction? A→B, B→A, or both?"

Explain:
- Some mappings have an obvious direction (source A supports target B)
- Some are inherently directionless (crosswalk)
- Even if mapping in one direction, examining pairs in the opposite direction "will identify previously unknown relationships" [NIST §5]

If the user is unsure, recommend: "Start with A→B. We can always examine B→A later."

### Assumption 5: Exhaustiveness

> "How exhaustive should this mapping be? We recommend capturing the strongest direct relationships only."

"Mapping indirect or tenuous relationships would create so many mappings that they would lose their value. Instead, we recommend capturing the strongest direct relationships between concepts." [NIST §3]

Options:
- **Strongest direct only** (recommended): Map only clear, direct relationships. Keeps the mapping focused and useful.
- **Primary + secondary**: Two tiers — strong relationships in a primary mapping, weaker relationships in a separate secondary mapping.
- **Exhaustive**: Map everything including tenuous relationships. Rarely appropriate.

## Output

A use case document containing all five assumptions. Format:

```markdown
## Use Case: [Brief Title]

**Intended users**: [who, with what skills]
**Purpose**: [the question this mapping answers]
**Concept types**: [what's being mapped from each source, at what granularity]
**Direction**: [A→B / B→A / Both]
**Exhaustiveness**: [strongest-direct-only / primary+secondary / exhaustive]

**Use case statement**: [one sentence combining the above — e.g., "CISOs and risk officers need to determine how meeting CCM 4.1 control requirements helps satisfy NIST 800-53r5 control recommendations, mapping at the individual control level in the CCM→NIST direction, capturing the strongest direct relationships."]
```

Save this document — it's referenced throughout all subsequent phases.

## Teaching Moment (if teaching mode is on)

> **Why document all five?** Each assumption narrows the mapping. Without them, you'd map everything to everything in every direction — producing thousands of relationships where most are tenuous. The use case is a filter: it tells you what to map, how deep to go, and when to stop. It also tells anyone who uses the mapping later exactly what it does and doesn't cover.
