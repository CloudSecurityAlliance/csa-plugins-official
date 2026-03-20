# Phase 3: Source Analysis & Synthesis

## Purpose

Compare all collected sources. Classify confidence levels. Identify where sources agree, disagree, or leave gaps. Surface source biases.

## Prerequisites

Before starting this phase, read:
- `references/confidence-framework.md` — the 6-level classification system
- `references/bias-framework.md` — source motivation analysis

## Process

### Step 1: Extract Claims

Go through each source and extract the key factual claims it makes. For each claim, note:
- What is being claimed
- Which source(s) make this claim
- The date of the claim

Focus on claims about:
- What happened (attack vector, scope, data affected)
- When things happened (discovery, disclosure, remediation dates)
- Who was affected (number of users, types of data, geographic scope)
- How it was discovered (internal detection, external researcher, attacker disclosure)
- What was the response (remediation actions, customer notification, regulatory filing)

### Step 2: Cross-Reference and Classify

For each claim, determine its confidence level using the confidence framework:

- Do multiple independent sources agree? → **Confirmed** or **Corroborated**
- Is it from a single credible source? → **Reported**
- Is it a logical deduction from other confirmed facts? → **Inferred**
- Is it speculation or from an anonymous/unverifiable source? → **Speculative**
- Do sources directly contradict each other? → **Disputed**

### Step 3: Identify Conflicts

Where sources disagree, create a conflicts table:
- What they disagree about
- Source A's version (with source name)
- Source B's version (with source name)
- Each source's possible motivation for their version (use bias framework)
- Your assessment of which is more likely accurate, and why

### Step 4: Vendor Disclosure Cross-Check

After cross-referencing external sources against each other, do a dedicated pass checking external claims against the vendor's own disclosure. This catches a common failure mode: external sources (journalists, researchers, community) make a specific claim, multiple external sources agree, so the claim gets tagged Corroborated — but the vendor's own statement directly contradicts or qualifies it, which would make it Disputed.

For each claim rated Corroborated or higher from external sources:
1. **Does the vendor's disclosure address this specific topic?** If yes, does it agree, qualify, or contradict?
2. **If the vendor contradicts an external claim**, downgrade to **Disputed** and present both sides with bias analysis (the vendor has incentive to minimize; external sources may have incomplete information or be over-interpreting)
3. **If the vendor qualifies an external claim** (e.g., "LIFENET is functioning normally; interruptions are from third-party ePCR vendors, not our system"), note the qualification and adjust the confidence level or add nuance
4. **If the vendor is silent on a topic**, note the silence — it may be addressed in Phase 7 (gap analysis) as a missing disclosure

This step requires reading the vendor disclosure carefully for specific product/system statements, not just the general narrative. Vendor updates often contain per-product or per-system clarifications buried in later updates that contradict external reporting's broader claims.

### Step 5: Assess Coverage

Create a coverage matrix showing which aspects of the incident each source addresses. This reveals:
- What everyone agrees on (high confidence)
- What only one source covers (lower confidence, but potentially unique insight)
- What nobody covers (gaps — input for Phase 7)

## Teaching Moment (if teaching mode is on)

> **Why sources disagree:** Two honest sources can report different things because they have different access to information, different definitions of scope, or different incentive structures. A vendor saying "no customer data was accessed" and a researcher saying "we found customer records in the attacker's dump" might both be technically correct if the vendor defines "accessed" narrowly.
>
> **The bias question:** For every source, ask yourself: "Who benefits from this version of events?" A vendor minimizing scope benefits from lower liability. A researcher dramatizing severity benefits from attention. Neither is lying — they're selecting which truths to emphasize.

## Output

Present to the analyst:

1. **Unified Fact Sheet** — every claim, tagged with confidence level and source(s)
2. **Conflicts Table** — where sources disagree, with bias analysis
3. **Coverage Matrix** — which sources cover which aspects

Then pause: "Here's what the sources agree and disagree on. Do you want to adjust any confidence levels, add context, or flag anything before I proceed to deep analysis?"
