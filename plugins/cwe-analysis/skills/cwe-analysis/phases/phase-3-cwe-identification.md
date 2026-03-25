# Phase 3: CWE Identification

## Purpose

Search the bundled CWE data for candidate CWEs that match the vulnerability identified in Phases 1-2. This is the core analytical phase.

## Prerequisites

Before starting, read:
- `references/confidence-framework.md` — the 6-level confidence system
- `references/abstraction-guide.md` — Pillar/Class/Base/Variant selection rules

## Critical Constraint

**Do NOT filter candidates by AI category or AI relevance score.** Identify the correct weakness first based on weakness properties only. AI relevance is applied as annotation in Phase 4/6, never as a candidate filter. The correct CWE may not be AI-tagged.

## Process

### Step 1: Initial Search

Based on the vulnerability type, impact, and code patterns from Phases 1-2:

1. Use `cwe-tool.py search "<keywords>"` with terms from the vulnerability description
2. Use `cwe-tool.py candidates --impact "<impact type>"` to find CWEs with matching consequences
3. Review the results for plausible matches

### Step 2: Refine to Most Specific

For each plausible candidate:

1. Use `cwe-tool.py children <CWE-ID>` to check for more specific children
2. If children exist that better match the vulnerability, drill down
3. Use `cwe-tool.py lookup <CWE-ID>` to examine each candidate in detail
4. Check the Description, Extended Description, and Observed Examples fields

### Step 3: Verify the Match

For the top candidates:

1. Does the CWE Description match what's wrong with the code (not just the impact)?
2. Do the Observed Examples describe similar vulnerabilities?
3. Is the Abstraction level appropriate? (Base or Variant preferred — see abstraction-guide.md)
4. Check Related Weaknesses — are there parent/child/peer CWEs that might be better fits?

### Step 4: Tag with Confidence

For each candidate, assign a confidence level from the confidence framework:
- **Confirmed** — code analysis in Phase 2 proved this weakness exists
- **Strong** — impact, description, and examples all align
- **Supported** — description matches but evidence is incomplete
- **Inferred** — logical deduction, not direct evidence
- **Best Fit** — closest available CWE, but not an exact match
- **Uncertain** — can't distinguish between candidates

### Step 5: Rank and Present

Present 3-5 candidates ranked by fit. For each:
- CWE-ID and Name
- Confidence level
- Why this CWE matches (cite specific evidence from Phases 1-2)
- Why it might NOT be the right choice (honest assessment)
- Abstraction level

## Teaching Moment

> **The "First Match" trap:** The first CWE you find that seems to fit is rarely the best one. CWE-74 (Injection) matches almost any injection vulnerability — but CWE-89, CWE-78, or CWE-79 are almost always more accurate. Always check for children of your first match.
>
> **The "Name Match" trap:** Matching by name alone is dangerous. "Server-Side Template Injection" sounds like it maps to CWE-1336 (Improper Neutralization of Special Elements Used in a Template Engine), and it usually does — but verify by reading the full CWE description and checking Observed Examples.

## Output

Present a ranked candidate list:

| Rank | CWE | Name | Confidence | Reasoning |
|------|-----|------|------------|-----------|
| 1 | CWE-XXX | ... | Strong | ... |
| 2 | CWE-YYY | ... | Supported | ... |
| ... | ... | ... | ... | ... |

Then pause: "Here are my top candidates with confidence levels. Do any miss the mark, or should any confidence levels be adjusted?"

If the analyst wants to stop here (single CWE assignment), proceed to Phase 5 (Validation). If they want chain analysis, proceed to Phase 4.
