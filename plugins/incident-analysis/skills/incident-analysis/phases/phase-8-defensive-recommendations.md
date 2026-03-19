# Phase 8: Defensive Recommendations

## Purpose

Translate the analysis into prioritized, actionable defensive recommendations. Every recommendation must trace back to a specific finding from earlier phases. Recommendations without evidence are opinions — this phase produces evidence-based guidance.

## Process

### Step 1: Gather Inputs

Collect the findings that drive recommendations from prior phases:

- **From Phase 4 (Vendor & Integration Analysis):** Over-permissioning gaps, shared responsibility findings, safer configuration options that existed but weren't used
- **From Phase 6 (Impact & Downstream Effects):** Severity ratings per population, cascading effects, differential impact findings
- **From Phase 7 (Gap & Inference Analysis):** Missing controls, remediation gaps, non-best-practices, least-privilege violations, pattern-based findings

Each recommendation must reference the specific phase and finding it addresses.

### Step 2: Generate Recommendations

For each finding that warrants a recommendation, produce:

- **Title** — concise action statement (e.g., "Implement OAuth scope restrictions for third-party integrations")
- **Finding reference** — which phase and finding this addresses (e.g., "Phase 4: Vendor had Bulk API access not required for core function")
- **Who should act** — which role or team owns this (e.g., "Security team + IT procurement" or "Platform administrator")
- **Specific action** — what exactly to do, in enough detail that someone could start implementing it without further research
- **Priority** — Critical / High / Medium / Low, based on impact severity and exploitability
- **Timeline** — how quickly this should be implemented (immediate, 30 days, 90 days, strategic)
- **Confidence** — how confident are we that this would have prevented or materially reduced the impact of this specific incident?

### Step 3: Categorize Recommendations

Group recommendations into these categories:

1. **Preventive** — would have stopped the incident from occurring (e.g., "Enforce least-privilege OAuth scopes for all third-party integrations")
2. **Detective** — would have detected the incident earlier (e.g., "Monitor for anomalous Bulk API usage patterns from integration accounts")
3. **Limiting** — would have reduced the blast radius (e.g., "Segment sensitive data so support ticket content isn't accessible via the same integration as contact data")
4. **Responsive** — would have improved the response (e.g., "Pre-establish communication templates and regulatory notification workflows")
5. **Strategic** — longer-term changes to security posture (e.g., "Implement a vendor risk management program with annual access reviews")

### Step 4: Prioritize into Tiers

Organize recommendations into implementation tiers. **Maximum 5 recommendations per tier** — more than that dilutes focus.

**Tier 1 — Immediate (0-7 days):**
Actions that should be taken right now, either because the vulnerability is still exploitable or because the fix is simple and high-impact.

**Tier 2 — Short-term (1-4 weeks):**
Actions that require some planning or coordination but address critical gaps.

**Tier 3 — Medium-term (1-3 months):**
Actions that require procurement, architectural changes, or organizational process changes.

**Tier 4 — Strategic (3-12 months):**
Foundational improvements that prevent entire categories of similar incidents.

If more than 5 items fall into a single tier, force-rank them. The analyst can disagree, but presenting a prioritized list is more useful than an unprioritized dump.

### Step 5: Reality-Check Recommendations

Before finalizing, review each recommendation against these quality criteria:

- **Specific enough?** — Could someone start implementing this without further research? "Improve security" fails; "Restrict OAuth scopes for Salesforce Connected Apps to read-only contact access" passes.
- **Proportionate?** — Is the recommendation proportionate to the risk? Don't recommend a $500K SIEM deployment to address a low-severity gap.
- **Accounts for constraints?** — Does the recommendation acknowledge real-world constraints (budget, staffing, vendor limitations)? If a recommendation requires capabilities the organization probably doesn't have, say so.
- **Creates new risks?** — Could implementing this recommendation create new problems? (e.g., "Block all third-party integrations" stops the breach but also stops business operations)
- **Traceable?** — Can someone reading just this recommendation trace it back to the specific finding and evidence?

## Teaching Moment (if teaching mode is on)

> **Why recommendations need finding references:** "Implement MFA everywhere" is generic advice you can find in any security blog post. "Implement MFA for Salesforce Connected App administration because this incident demonstrated that a single compromised OAuth token granted access to 15M support tickets" is a recommendation tied to evidence. The finding reference is what makes the recommendation credible and actionable.
>
> **The prioritization problem:** Most incident post-mortems produce a long list of recommendations that nobody implements because there's no clear starting point. Tiered prioritization with hard limits forces you to make the same trade-offs the implementing team will face. If everything is "Critical," nothing is.
>
> **Defensive depth:** Notice how recommendations span preventive, detective, limiting, responsive, and strategic categories. This is intentional — no single control prevents all incidents. The goal is layered defense where each control catches what the others miss.

## Output

Present to the analyst:

1. **Recommendations by Tier** — each recommendation with title, finding reference, owner, action, priority, timeline, and confidence
2. **Category Distribution** — how many recommendations fall into each category (preventive, detective, limiting, responsive, strategic). Note any categories with no recommendations — that's a gap in the defensive posture.
3. **Implementation Dependencies** — if any recommendations depend on others being implemented first, note the dependency chain

Proceed directly to Phase 9 (report generation) — no pause needed here. The recommendations will be included in the final report for analyst review.
