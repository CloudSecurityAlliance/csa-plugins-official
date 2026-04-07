# Phase 1: Intake

## Purpose

Load source(s) and establish mapping context. Two modes: exploratory (one source) or mapping (two sources).

## Exploratory Mode (One Source)

The user has one structured source and wants to understand it before mapping.

### Steps

1. Load the structured data file (JSON/CSV with identified concepts)
2. Verify structure: concepts identified, hierarchy present, concept types labeled
3. Profile the source:
   - How many concepts? At what hierarchy levels?
   - What concept types? (controls, requirements, outcomes, articles, etc.)
   - What granularity levels are available?
   - Is the hierarchy well-defined or irregular?
4. Run structural analysis (B4): capture the parent-child hierarchy
5. Recommend mapping approaches:
   - What styles would work well with this source?
   - What kinds of second sources would pair well? (e.g., "similar control catalog → set theory; related but different concept types → supportive")
6. Present findings

### Pause

> "Here's what I found about your source:
> - [N] concepts across [M] hierarchy levels
> - Concept types: [types]
> - Hierarchy: [description]
> - Recommended styles: [styles with brief rationale]
>
> When you have a second source, we can proceed with mapping."

### Output

Source profile with structural analysis and style recommendations. Can proceed to partial Phase 2 (documenting what's known about the use case).

## Mapping Mode (Two Sources)

Full mapping engagement.

### Steps

1. Accept two structured data files
2. Verify each has: identified concepts, hierarchy, concept types
3. If either is not structured: "This file doesn't appear to have structured concepts. Try the `security-knowledge-ingestion` plugin to convert it first."
4. Establish roles:
   - **Focal document**: The primary document being mapped to (in NIST OLIR context, this is the NIST publication)
   - **Reference document**: The second publication being mapped to the focal document
   - If both are non-NIST, ask the user which is focal and which is reference
5. Present summary

### Pause

> "Ready to map:
> - **Focal**: [title] — [N] concepts ([concept types])
> - **Reference**: [title] — [M] concepts ([concept types])
>
> Proceed to use case documentation?"

### Output

Two validated source files with roles assigned.

## Teaching Moment (if teaching mode is on)

> **Focal vs Reference**: In NIST's OLIR system, the focal document is the one you're mapping TO — typically a NIST publication like SP 800-53 or the CSF. The reference document is the one you're mapping FROM. This matters because the direction of the mapping is documented in the use case, and some relationship types are directional (supports vs. is supported by). If you're not submitting to OLIR, the choice of focal vs. reference is less rigid — but you still need to pick a consistent direction.
