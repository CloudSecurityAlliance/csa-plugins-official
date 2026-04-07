# Quality Criteria

What makes a mapping good or bad, synthesized from NIST IR 8477.

## Good Mapping

- Has a documented use case with all five assumptions explicit
- Uses a predefined relationship style appropriate to the use case
- Captures the strongest direct relationships, not every tenuous connection
- Documents rationale for every relationship
- Has been reviewed via representative sample (Phase 5 quality gate)
- Serves its stated audience at the appropriate granularity
- Captures observations about ambiguities and issues in the source documents
- Enables interoperability via consistent terminology and styles
- Documents "no relationship" findings, not just positive relationships

## Bad Mapping

- No documented purpose, use cases, scope, audience, or assumptions — users must guess at meaning
- Uncharacterized relationships ("A is related to B" with no type or rationale)
- Undocumented SME assumptions — perspectives may differ significantly for future users
- Exhaustive mapping of tenuous relationships — loses value through volume
- Inconsistent use of relationship types across the mapping
- Wrong granularity for the audience (too detailed or too coarse)
- No peer/sample review — single-evaluator bias unchecked
- Skipped "no relationship" documentation — gives false impression of completeness
- Direction confused (A supports B recorded as B supports A)

## Warning Signs During Mapping

| Signal | Possible Issue |
|--------|---------------|
| Every pair has a relationship | Were unrelated pairs considered? |
| Every pair is the same type | Is the type being applied too loosely? |
| Everything is High confidence | Is the confidence framework being used critically? |
| Justifications are vague | Are you really evaluating or just pattern-matching? |
| Many "intersects with" results | Would a different style be more informative? |
