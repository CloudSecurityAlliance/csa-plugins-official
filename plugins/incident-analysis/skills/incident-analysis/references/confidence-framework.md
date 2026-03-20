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

## Common Over-Confidence Mistakes

These anti-patterns produce systematically inflated confidence levels. Watch for them throughout the analysis.

### 1. "Inference from Outcome" Trap

**The mistake:** "The attack succeeded in a way consistent with control X being absent, therefore control X was confirmed absent."

**Why it's wrong:** An attack outcome is consistent with many possible configurations. The victim's actual security posture — which MFA they used, which features were enabled, how BYOD was enrolled — is an internal detail that external analysis can only infer, not confirm. You need the victim or their forensic investigators to publicly confirm a specific configuration for it to be Confirmed.

**The fix:** Claims about a victim's internal security posture (controls absent, features not enabled, configurations not applied) are **Inferred** unless the victim, regulators, or forensic investigators have publicly confirmed them. Tag as: "Analyst/AI assessment: [claim]. This is inferred from the attack's success, not confirmed by the victim. [Inferred]"

### 2. "Actor Does X Generally" Trap

**The mistake:** A threat intelligence report describes an actor's general TTPs. The analysis attributes those TTPs to the specific incident as if the report confirmed they were used here.

**Why it's wrong:** A threat actor's known capabilities are context about what they *can* do, not evidence of what they *did* in this specific incident. An actor known for VPN brute-force may have used phishing in this case. A TTP report that doesn't name the victim as the target of specific activities is describing the actor, not the incident.

**The fix:** When citing threat intelligence about actor TTPs, explicitly distinguish:
- "Handala is known to conduct VPN brute-force attacks against organizational targets [Confirmed — about the actor]"
- "Handala conducted VPN brute-force attacks against Stryker specifically [Reported/Inferred — only if the source specifically names the victim]"

General actor patterns belong in threat actor background sections. Only attribute specific TTPs to the incident when sources confirm they were used against this target.

### 3. "Source Quantity Over Quality" Trap

**The mistake:** Multiple anonymous or community sources (HN comments, Reddit posts) are treated as Corroborated because "2+ independent sources agree."

**Why it's wrong:** The Corroborated level is designed for independent sources with some degree of accountability — reporters citing different named employees, multiple news outlets with independent sourcing. Anonymous community posts may all derive from the same rumor, cannot be verified, and carry no editorial accountability. Volume of anonymous claims is not the same as independent corroboration.

**The fix:** Corroboration requires at least one source with editorial oversight or named attribution (journalist, security researcher, vendor, regulator). Multiple anonymous or pseudonymous community reports can support **Reported (with anecdotal community support)** but do not constitute full Corroboration on their own. Community sources are most valuable when they corroborate claims already established by accountable sources, not as the primary evidence for a claim.

### 4. "Feature Exists = Specific Capability Exists" Trap

**The mistake:** A security feature is described as "available since [date]" based on its general availability announcement. The analysis concludes that a specific sub-capability of that feature was available at the same date.

**Why it's wrong:** Enterprise security features ship incrementally. A feature may be generally available for some actions but not others. Multi-Admin Approval might cover app deployments in 2023 but not add device wipe coverage until 2025. Claiming a specific capability was "available for 2.5 years" when it was actually available for 7 months materially changes the blame assessment.

**The fix:** When claiming a control was "available but unused" — especially when this drives a blame or responsibility conclusion — verify the specific capability's availability date against the vendor's own release notes, changelog, or "what's new" documentation. Not secondary blog posts, not general feature announcements — the primary vendor documentation for the specific sub-capability relevant to this incident. State the verified date and source in the analysis.
