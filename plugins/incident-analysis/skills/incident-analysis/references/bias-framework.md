# Source Motivation & Bias Framework

Every source has incentives that shape what they report and how. Use this framework to explicitly surface those incentives when analyzing sources.

## Source Types and Their Motivations

| Source Type | Primary Motivation | Common Bias Patterns | What to Watch For |
|------------|-------------------|---------------------|-------------------|
| **Vendor/Company** | Minimize scope, liability, stock/reputation impact | Downplay severity, narrow scope definitions, delay disclosure, emphasize remediation | "Only X was affected" (how do they know?), vague timelines, passive voice ("was discovered" vs. "we discovered") |
| **Security Researchers** | Credit, recognition, career advancement | May overstate novelty or severity, dramatize findings, rush to publish | Severity inflation, "first to report" emphasis, technically accurate but contextually misleading |
| **News Outlets** | Engagement, readership, ad revenue | Sensationalize, simplify complex technical details, amplify uncertainty | Alarming headlines vs. article content, unnamed sources, speculative language presented as fact |
| **Community (HN/Reddit)** | Discussion, speculation, insider venting | Mix of genuine insiders and uninformed speculation, impossible to distinguish without corroboration | Claims of insider knowledge, "I used to work there" comments, technically plausible but unverified theories |
| **Regulators/Government** | Establish precedent, enforce compliance | Focus on compliance failures, may oversimplify technical details, political considerations | SEC filings are legally constrained, CISA advisories focus on mitigation over blame |
| **Competitors** | Market advantage | May amplify negative coverage, offer "alternatives," FUD | "Our product prevents this" messaging disguised as analysis |

## Key Question for Every Source

**"Who benefits from this version of events?"**

Apply this question to every source. If a source's account conveniently aligns with their interests, increase skepticism. If a source reports something against their own interest (e.g., a vendor admitting a wider scope than required), increase confidence.

## Cross-Source Conflict Resolution

When sources disagree:
1. Identify each source's incentive for their version
2. Check if independent sources corroborate either version
3. Look for sources reporting against their own interest (higher credibility)
4. Note the conflict explicitly rather than choosing one version silently
