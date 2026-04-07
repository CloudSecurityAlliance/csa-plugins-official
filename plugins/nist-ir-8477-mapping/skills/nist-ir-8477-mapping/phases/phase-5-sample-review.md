# Phase 5: Sample Review

## Purpose

Quality gate — review the sample mapping before committing to the full run. Per NIST §5: "Have other SMEs review the sample and the use case documentation, and provide feedback on them to help improve the quality of the mapping."

This phase exists to catch systematic errors early, before they propagate through hundreds of concept pairs.

## Steps

### Step 1: Present the Sample

Show the full sample mapping with justification for each pair. Group by relationship type so patterns are visible.

For each pair, show:
- Focal concept → Reference concept
- Relationship type (and rationale/property if applicable)
- Justification (abbreviated — the user can ask for full detail)
- Confidence level

Also show:
- Distribution of relationship types (e.g., "8 supports, 3 no relationship, 2 is supported by, 1 equivalent, 1 contrary")
- Any "no relationship" findings
- Source observations collected so far

### Step 2: Check for Systematic Issues

Look for these patterns (and flag them to the user):

| Issue | Signal | Example |
|-------|--------|---------|
| **Consistency** | Similar pairs getting different treatments | Two controls about access management — one "supports," the other "is supported by" — with no clear reason for the difference |
| **Style drift** | Interpretation of types shifting over the sample | Early pairs use "supports" strictly, later pairs use it loosely |
| **Exhaustiveness drift** | Tenuous relationships creeping in | Use case says "strongest direct only" but sample includes weak indirect relationships |
| **Directionality errors** | A→B confused with B→A | "A supports B" when the evidence shows B supports A |
| **Missing "no relationship"** | No unrelated pairs documented | If every pair has a relationship, were unrelated pairs even considered? |
| **Use case alignment** | Sample doesn't serve the documented purpose | Use case says "for auditors" but relationships are characterized for engineers |
| **Confidence inflation** | Everything tagged High | If every pair is High confidence, the framework isn't being used critically |

### Step 3: User Review

Present findings and ask:

> "Here's the sample ([N] pairs). I [found/didn't find] systematic issues:
> [list any issues]
>
> Does the approach look right before I map the remaining [M] pairs?"

### Step 4: Respond to Feedback

- **Issues found → adjust and re-sample**: Go back to Phase 4, adjust the approach based on feedback, map a new or revised sample. Repeat until the user approves.
- **Approved → proceed to full run**: Move to Phase 4b (full mapping execution).

## Output

- Reviewed sample with any corrections
- Confirmed approach for full run
- Quality assessment

## Phase 4b: Full Mapping Execution

After the sample is approved, complete the full mapping:

1. Apply the validated approach to all remaining concept pairs
2. Same per-pair process: evaluate, assign type, document justification, tag confidence
3. Include the sample pairs already mapped (don't redo them unless corrections changed the approach)
4. Continue capturing source observations
5. Record prompts used

**Automation spectrum** (applies here):
- **Interactive**: Present each pair, discuss, assign together
- **Semi-automated**: Batch process, pause periodically for review
- **Fully automated**: Process all remaining pairs, present complete results

**Output**: Complete mapping with typed, justified relationships for all evaluated concept pairs.
