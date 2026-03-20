# Phase 4: Vendor & Integration Analysis

## Purpose

Understand what the breached third-party vendor/product actually does, what access it legitimately needs, and how affected organizations were using it. This is foundational context — without it, you cannot properly assess whether permissions were excessive, whether the blast radius was avoidable, or what the victim could have done differently.

**This phase is mandatory.** Every supply chain or third-party incident involves a product or service that was doing something for the victim. Understanding that "something" is essential before proceeding to timeline reconstruction or gap analysis.

## When to Run This Phase

- **Always** when the incident involves a third-party vendor, integration, SaaS product, or supply chain component
- **Even for direct breaches** — briefly assess what the compromised product/service does and what data it naturally touches
- Skip only if the incident is purely internal with no third-party dimension (rare for cloud incidents)

## Process

### Step 1: Research the Vendor/Product

Search for and document:

1. **What does this product do?** — Core function in plain language (e.g., "Drift is a chatbot that captures website visitor info and routes leads to sales teams")
2. **Who are its customers?** — Market segment, typical company size, industry verticals
3. **What integrations does it offer?** — Which platforms does it connect to? (Salesforce, Google Workspace, Slack, etc.)
4. **What data does it process in normal operation?** — What information flows through it as part of its core function?
5. **What access does it request during setup?** — OAuth scopes, API permissions, data access grants. Check the vendor's integration documentation if available.

Use web search and the vendor's own documentation/marketing pages. The vendor's website will describe the product optimistically, but the integration setup docs reveal what permissions it actually requests.

### Step 2: Determine Minimum Viable Access

Based on the product's core function, determine:

1. **What data access does it legitimately need?** — The minimum set of permissions required for the product to do its job
2. **What data access did it actually have?** — What the incident reveals about the actual permissions granted
3. **The gap between needed and granted** — This is the over-permissioning that enabled the breach's scope

Present this as a comparison table:

| Capability | Needed for Core Function? | Actually Granted? | Risk If Compromised |
|-----------|--------------------------|-------------------|---------------------|
| (e.g., Read Contacts) | Yes — chatbot needs to check if visitor is known | Yes | Low — public business contact info |
| (e.g., Read Cases/Support Tickets) | No — chatbot doesn't interact with support | Yes | **High** — contains credentials, configs, internal details |
| (e.g., Bulk API access) | No — chatbot processes one visitor at a time | Yes | **Critical** — enables mass data export |

### Step 3: Verify "Available But Unused" Control Claims

Before concluding that a security control was available but not used, verify each claim against primary vendor documentation. This prevents a common error: claiming a control was available for years when the specific sub-capability relevant to this incident was only recently added.

For each control you identify as "available but unused":

1. **Verify the specific capability's availability date** — Check the vendor's own release notes, changelog, or "what's new" documentation. Not secondary blog posts or general feature announcements — the primary vendor documentation for the specific sub-capability relevant to this incident.
2. **Verify the capability covers the specific action that was exploited** — A feature may be generally available for some actions but not others (e.g., Multi-Admin Approval may cover app deployments but not device wipe actions, or vice versa, depending on the version).
3. **State the verified date and source in the analysis** — "MAA for device wipe actions was available since [date] per [vendor documentation URL]" rather than "MAA was available since [date]."
4. **Adjust blame framing accordingly** — "Available for 7 months and not enabled" tells a materially different story than "available for 2.5 years and not enabled." Both are failures, but the severity of the governance failure is different.

If you cannot verify a specific capability's availability date against primary documentation, say so explicitly and tag the "available but unused" claim as **Inferred** rather than Confirmed.

### Step 4: Analyze How Customers Were Using It

Research and document:

1. **What was the typical deployment?** — How did organizations like the victim integrate this product?
2. **Were there safer configuration options available?** — Could the victim have restricted access, used IP allowlists, set session limits, disabled unnecessary API access?
3. **Did the vendor's setup documentation encourage broad permissions?** — Some vendors request "all access" during setup and never tell customers they can scope it down
4. **Were there alternative products or approaches with a smaller blast radius?** — Could the business need have been met with less risk?

### Step 5: Assess Shared Responsibility

For each party involved, assess their contribution to the exposure:

- **The breached vendor** — What security failures on their end enabled the compromise? (e.g., secrets in code repos, no token rotation, insufficient monitoring)
- **The victim organization** — What could they have done to limit the impact? (e.g., scoped permissions, IP restrictions, monitoring OAuth app behavior, periodic access reviews)
- **The platform provider** (e.g., Salesforce, Google) — Did the platform provide adequate tools for restricting third-party access? Were security features available but not used?

## Teaching Moment (if teaching mode is on)

> **Why this matters more than you think:** The biggest lesson in most supply chain breaches isn't "the vendor got hacked" — it's "the vendor had access to things it didn't need, and nobody noticed." A chatbot that can export your entire support ticket history via Bulk API isn't a security-conscious integration. But most organizations grant whatever permissions the vendor's setup wizard requests and never revisit them.
>
> **The "setup wizard" trap:** Vendors optimize their setup flow for speed, not security. "Grant all permissions" is one click. "Configure least-privilege scopes" requires reading documentation and making decisions. Most customers take the fast path — and inherit the risk.
>
> **Shared responsibility in SaaS:** Cloud and SaaS vendors love the shared responsibility model when it shifts blame to customers. But when a vendor requests excessive permissions during onboarding and doesn't document how to restrict them, the "shared responsibility" framing obscures a design failure.

## Output

Present to the analyst:

1. **Vendor/Product Profile** — what it does, who uses it, what integrations it has
2. **Access Comparison Table** — needed vs. granted permissions with risk ratings
3. **Customer Usage Assessment** — how the victim was using it and what safer alternatives existed
4. **Shared Responsibility Assessment** — who bears what portion of the exposure

This phase feeds directly into Phase 7 (gap analysis), where the over-permissioning findings become specific, actionable gap items.

Proceed to Phase 5 after presenting — no separate pause needed here. The analyst will review findings at the Phase 6 pause (impact assessment) and Phase 7 pause (gap analysis).
