# Confidence/Provenance Framework

Use this framework to classify every claim, fact, and assertion in the incident analysis. Tag each item with one of these levels.

| Level | Meaning | When to Use | Example |
|-------|---------|-------------|---------|
| **Confirmed** | Vendor-acknowledged AND multiple independent sources agree | Official disclosure plus independent verification | "We experienced unauthorized access to customer data" — in vendor blog post, confirmed by security researcher's independent analysis |
| **Corroborated** | 2+ independent sources agree, no contradiction | Multiple reporters citing different sources | Three news outlets quoting different internal employees with consistent accounts |
| **Reported** | Single credible source, uncontradicted | Sole reporter but has a track record | Krebs on Security exclusive, no other coverage yet but no contradicting information |
| **Inferred** | Logical deduction from confirmed/corroborated facts | Deduction, not direct evidence | "They rotated all API keys within 24 hours" → credential compromise is highly likely |
| **Speculative** | Opinion, theory, single anonymous source, or pattern-matching | Weak evidence, community discussion, guesswork | HN commenter claiming insider knowledge, Reddit theories, analyst extrapolation |
| **Disputed** | Sources actively contradict each other | Direct conflict between accounts | Vendor says "no customer data was accessed," security researcher publishes exfiltrated records |

## Usage Rules

1. Every factual claim in the analysis must have a confidence tag
2. AI-generated inferences and assessments (primarily Phases 6, 7, and 8) are always tagged **Inferred** or **Speculative** and prefixed with "Analyst/AI assessment:"
3. When a claim's confidence changes based on new sources, update the tag and note why
4. **Disputed** items should present both sides with reasoning about which is more credible
5. Default to the lower confidence level when uncertain between two adjacent levels
