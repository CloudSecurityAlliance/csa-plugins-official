# Phase 3b: Gap & Inference Analysis

## Purpose

Read between the lines. Identify what's NOT being said, what can be inferred, and where standard disclosure expectations aren't met. This is the most speculative phase — label everything clearly.

## Important: Confidence Rules

All output from this phase is labeled either:
- **Inferred** — logical deduction from confirmed/corroborated facts
- **Speculative** — weaker reasoning, pattern-matching, or single-signal analysis

Every item is prefixed with **"Analyst/AI assessment:"** to distinguish it from source-derived information.

When an AI inference contradicts a vendor's official statement, present both side-by-side with reasoning for why the inference may be warranted. Do not replace the official account — supplement it.

## This Phase is Inherently Speculative

Gap analysis is high-value but high-risk for false positives. That's acceptable:
- Label everything with confidence levels
- Skilled analysts will steer you toward what's actually significant
- Missing some gaps is OK — this is a value-added capability, not a completeness guarantee
- False positives are better than false negatives here — it's easier for the analyst to dismiss a bad inference than to notice a gap you didn't flag

## Expected Information Gap Analysis

Go through each category systematically:

### Missing Disclosures
What would we normally expect to see in a disclosure of this type that's absent?
- Number of affected users/accounts
- Types of data accessed or exfiltrated
- Customer notification timeline
- Remediation completion date
- Third-party forensic investigation results
- Insurance/legal implications

### Careful Non-Answers
What questions does the official statement carefully avoid answering?
- Look for passive voice that obscures agency ("access was obtained" vs. "the attacker accessed")
- Look for scope limitations that are suspiciously precise
- Look for forward-looking statements that substitute for factual disclosure

### Suspicious Specificity
What scope limitations are suspiciously precise?
- "Only X was affected" — how do they know? What about Y?
- "No evidence of exfiltration" — absence of evidence vs. evidence of absence
- Specific date ranges that conveniently exclude certain periods

### Remediation Gaps
What remediation actions are mentioned vs. what would be standard practice?
- Password resets mentioned? If not, why not?
- Key rotation? Service isolation? Vendor review?
- Compare actual remediation to what NIST, SANS, or industry standard incident response frameworks would recommend

### Vendor Function & Least Privilege Analysis

**This section builds on the findings from Phase 2b.** Take the access comparison table and shared responsibility assessment from Phase 2b and turn them into specific, actionable gap findings.

For each over-permissioned access grant identified in Phase 2b:
- What was the excess permission?
- What damage did it enable in this specific incident?
- What would the blast radius have been if least-privilege had been enforced?
- What specific configuration change would have prevented or limited the damage?

Key questions to answer:
- **Could the victim have achieved the same business outcome with less access granted to the vendor?** If yes, describe the minimum-viable integration.
- **Did the vendor's onboarding process encourage over-permissioning?** If the "easy path" grants excessive access, that's a design failure worth calling out.
- **Were platform-level controls available but unused?** (e.g., Salesforce Connected App IP restrictions, OAuth scope limitations, Bulk API disablement for integration users)
- **What vendor risk management practices would have caught this before the breach?** (e.g., periodic OAuth scope reviews, integration inventories, automated permission drift detection)

This is often the most actionable section of the entire analysis — it answers "what should we do differently tomorrow?"

### Non-Best-Practices
What activities or configurations described in the incident are obvious deviations from security best practices?
- Excessive data retention
- Overly broad access permissions
- Missing MFA
- Unencrypted sensitive data
- Third-party access without proper controls
- Missing logging or monitoring

## Teaching Moment (if teaching mode is on)

> **How to read between the lines:** Official disclosures almost always specify the number of affected users. The absence of this number suggests either they don't know (concerning — implies inadequate monitoring) or the number is large enough that disclosing it would be damaging.
>
> **The "no evidence" tell:** "We found no evidence of data exfiltration" is one of the most common and most misleading phrases in incident disclosures. It might mean they looked carefully and found nothing. Or it might mean they don't have the logging to detect exfiltration. Or their forensic investigation was limited in scope. The phrase tells you almost nothing without knowing the quality of their detection capabilities.
>
> **Pattern recognition:** If you've seen similar incidents before, name the pattern. "This looks like a classic supply chain compromise where a trusted third party with excessive access gets breached, and the downstream impact is proportional to how much data was shared." Naming patterns helps analysts build mental models.

## Output

Present to the analyst:
1. **Gap Analysis** — each gap/inference with its category, confidence tag, and reasoning
2. **Pattern Assessment** — if this matches known incident patterns, name them
3. **Key Inferences** — the 3-5 most significant "reading between the lines" findings

Then pause: "Here's my deep analysis. These are explicitly speculative assessments — do you agree with these inferences, or would you like to revise any before I generate the report?"

Skilled analysts may significantly revise this section based on domain knowledge. Follow their lead.
