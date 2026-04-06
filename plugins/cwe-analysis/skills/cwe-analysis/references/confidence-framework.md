# Confidence Framework for CWE Assignments

Every CWE assignment carries uncertainty. This framework makes that uncertainty explicit and traceable rather than hidden.

## Two Dimensions of Uncertainty

Adapted from intelligence community analytic standards (ICD 203), this framework distinguishes between *evidence quality* (how good is your information?) and *taxonomy precision* (how well does the CWE vocabulary cover this weakness?).

Most confidence levels reflect evidence quality — you have more or less evidence that a specific CWE matches. "Best Fit" is the only level that reflects a taxonomy gap — the evidence about the weakness itself may be strong, but the CWE system doesn't have a precise match.

Don't confuse "we're not sure which CWE" (Uncertain — an evidence problem) with "no CWE precisely fits" (Best Fit — a taxonomy problem).

## Confidence Levels

| Level | Meaning | When to Use | Example |
|-------|---------|-------------|---------|
| **Confirmed** | Code analysis proves this exact weakness exists | Direct evidence from source code inspection | Traced unsanitized user input through to SQL query construction — this is CWE-89 |
| **Strong** | Multiple evidence types agree on this CWE | Impact matches, description matches, observed examples match | Impact is command execution via user input, CWE-78 description and examples both fit, code shows shell invocation |
| **Supported** | Evidence supports this CWE but not definitively | Description matches well, but code wasn't available or fully traced | Vulnerability description matches CWE-502 deserialization, but couldn't inspect the loading code directly |
| **Inferred** | Logical deduction from other confirmed facts | Deduction, not direct evidence | "The attack achieves RCE through model loading" — likely CWE-502, but could be another deserialization path |
| **Best Fit** | The CWE taxonomy doesn't precisely cover this weakness. You've searched children, peers, and siblings; nothing fits better. The gap is in CWE's vocabulary, not in your analysis. | Always accompanied by: what specifically doesn't fit, and what a hypothetical better CWE would describe | Vulnerability involves a novel AI attack pattern where the model's training data is poisoned through a feedback loop; CWE-1039 is closest but doesn't capture the feedback loop mechanism. A better CWE would describe "implicit training data manipulation through adversarial feedback." |
| **Uncertain** | Multiple CWEs are plausible, can't determine which | Insufficient information to differentiate | Could be CWE-22 (path traversal) or CWE-73 (external control of filename) — need more detail about path construction |

## Usage Rules

1. **Every CWE assignment must have a confidence tag.** No exceptions. If you cannot determine confidence, use "Uncertain" — that itself is a valid and useful signal.

2. **AI-generated assessments prefixed with "AI assessment:"** This distinguishes automated analysis from human-verified assignments. Example: "AI assessment: Strong — CWE-89 based on description matching SQL injection pattern and observed examples."

3. **Chain links tagged independently.** In a chain like CWE-20 → CWE-89 → CWE-200, each link gets its own confidence. The first link might be Confirmed while the last is Inferred.

4. **Default to lower level when uncertain.** If you're torn between Strong and Supported, choose Supported. Over-confidence is more harmful than under-confidence because it discourages further investigation.

5. **Uncertain assignments must list competing candidates.** "Uncertain" alone is not enough. List all plausible CWEs and what evidence would distinguish them. Example: "Uncertain — CWE-22 or CWE-73. Need to determine whether the attacker controls the full path or just the filename."

6. **Confidence can be upgraded during analysis.** Start conservative and upgrade as evidence accumulates. A CWE that begins as Inferred can become Strong if additional evidence is found during chain analysis or cross-referencing.

## Justification Guidance

Every confidence tag answers two questions: *what do you know?* and *how do you know it?* State both. The goal is that a reviewer reading your justification can independently assess whether they agree with your confidence level.

- **Confirmed** — You're saying: "I can point to the exact code that proves this." Cite the specific file, line, and mechanism.
- **Strong** — You're saying: "Multiple independent evidence types all point to the same CWE." Name which types (code, description match, observed examples, patch analysis).
- **Supported** — You're saying: "The evidence I have points here, but I haven't fully verified it." State what evidence you have and what's missing.
- **Inferred** — You're saying: "I'm reasoning from confirmed facts to a logical conclusion." State the confirmed facts and the reasoning step.
- **Best Fit** — You're saying: "I understand the weakness well, but CWE doesn't have an exact match." Describe what the weakness actually is and why the chosen CWE is the closest approximation.
- **Uncertain** — You're saying: "I have multiple plausible CWEs and can't distinguish between them yet." List the candidates and what information would resolve the ambiguity.

## Over-Confidence Anti-Patterns

### 1. "Impact Implies Weakness" Trap

**The mistake:** "The impact is remote code execution, so the CWE must be CWE-94 (Code Injection)."

**Why it's wrong:** Many different weaknesses can lead to code execution — deserialization (CWE-502), command injection (CWE-78), file upload (CWE-434), and others. The impact tells you what the attacker achieves, not what is wrong with the code. Working backward from impact to weakness skips the actual analysis.

**The fix:** Identify the weakness mechanism first, then verify that it leads to the observed impact. The CWE should describe what is broken in the software, not what the attacker accomplishes.

### 2. "Name Match" Trap

**The mistake:** "The advisory says 'improper input validation,' so the CWE must be CWE-20 (Improper Input Validation)."

**Why it's wrong:** CWE-20 is a Class-level abstraction that covers dozens of specific weaknesses. Nearly every injection vulnerability involves improper input validation at some level. Matching on the name alone produces overly abstract assignments that are useless for understanding or fixing the vulnerability.

**The fix:** Look past the name to the actual mechanism. What specific type of input validation is missing? What does the unsanitized input reach? That downstream effect determines the specific CWE.

### 3. "First Match" Trap

**The mistake:** Assigning the first CWE whose description seems relevant without checking for more specific alternatives.

**Why it's wrong:** The CWE hierarchy goes from abstract to specific. The first match is often a parent category, not the precise weakness. Stopping at the first match is like diagnosing "illness" when you could diagnose "bacterial pneumonia."

**The fix:** After finding a candidate CWE, always check its children using `cwe-tool.py children <ID>`. If a child CWE matches better, use it. Repeat until you reach the most specific applicable CWE.

### 4. "Vendor Says So" Trap

**The mistake:** Accepting the CWE assignment from a CVE record or vendor advisory without verification.

**Why it's wrong:** Vendor-assigned CWEs are frequently wrong, overly abstract, or use placeholder values like CWE-NVD-noinfo. NVD analysts face volume pressure and may assign broad categories. The vendor's CWE is a starting point for investigation, not a conclusion.

**The fix:** Treat vendor CWEs as hypotheses. Verify against the vulnerability description, any available code, and the CWE hierarchy. Upgrade or correct the assignment and document your reasoning with an appropriate confidence level.
