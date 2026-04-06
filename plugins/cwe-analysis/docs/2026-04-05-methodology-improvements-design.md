# CWE Skill Methodology Improvements

**Date:** 2026-04-05
**Scope:** Content-only changes to 5 Markdown files in the cwe-analysis skill. No code changes.

## 1. Chain Format Standardization

**Problem:** Phase 4 uses `↓` arrows with newline-separated labels; Phase 6 uses `→` arrows with nested indentation. Neither is copy-paste friendly.

**Fix:** Standardize on flat `→` format with descriptive labels. No nested indentation — every `→` line at the same level. Used identically in Phase 4 and Phase 6.

**Linear chain format:**
```
Root Cause: CWE-1287 (Improper Validation of Specified Type of Input) [Confirmed]
→ enables: CWE-89 (SQL Injection) [Strong]
→ leads to: CWE-200 (Exposure of Sensitive Information) [Inferred]
→ Impact: Data exfiltration
```

**Compound weakness format:**
```
Contributing: CWE-362 (Race Condition) [Confirmed]
Contributing: CWE-22 (Path Traversal) [Strong]
→ combined effect: CWE-434 (Unrestricted Upload) [Strong]
→ Impact: Arbitrary code execution
```

**Independent weaknesses format:**
```
Independent #1: CWE-89 (SQL Injection) [Confirmed]
Independent #2: CWE-79 (Cross-site Scripting) [Strong]
```

**Files:**
- `phases/phase-4-chain-analysis.md` — replace output section (lines 60-72)
- `phases/phase-6-report.md` — replace chain notation in Weakness Chain section

## 2. Confidence Framework Sharpening

**Problem:** "Best Fit" confidence level has unclear boundaries with "Supported" and "Uncertain." The framework doesn't distinguish evidence quality from taxonomy precision.

**Fix:** Three additions to `references/confidence-framework.md`:

### 2a. IC-inspired framing note

Insert after the opening paragraph ("Every CWE assignment carries uncertainty..."), before the Confidence Levels table:

```markdown
## Two Dimensions of Uncertainty

Adapted from intelligence community analytic standards (ICD 203), this framework
distinguishes between *evidence quality* (how good is your information?) and
*taxonomy precision* (how well does the CWE vocabulary cover this weakness?).

Most confidence levels reflect evidence quality — you have more or less evidence
that a specific CWE matches. "Best Fit" is the only level that reflects a taxonomy
gap — the evidence about the weakness itself may be strong, but the CWE system
doesn't have a precise match.

Don't confuse "we're not sure which CWE" (Uncertain — an evidence problem) with
"no CWE precisely fits" (Best Fit — a taxonomy problem).
```

### 2b. Rewritten "Best Fit" table row

Replace the existing Best Fit row:

| Level | Meaning | When to Use | Example |
|-------|---------|-------------|---------|
| **Best Fit** | The CWE taxonomy doesn't precisely cover this weakness. You've searched children, peers, and siblings; nothing fits better. The evidence about the weakness itself may be strong — the gap is in CWE's vocabulary, not in your analysis. | Always accompanied by: what specifically doesn't fit, and what a hypothetical better CWE would describe | Vulnerability involves a novel AI attack pattern where the model's training data is poisoned through a feedback loop; CWE-1039 (Automated Recognition Mechanism with Inadequate Detection or Handling of Adversarial Input Perturbations) is closest but doesn't capture the feedback loop mechanism. A better CWE would describe "implicit training data manipulation through adversarial feedback." |

### 2c. Justification guidance section

Insert after the "Usage Rules" section, before "Over-Confidence Anti-Patterns":

```markdown
## Justification Guidance

Every confidence tag answers two questions: *what do you know?* and *how do you
know it?* State both. The goal is that a reviewer reading your justification can
independently assess whether they agree with your confidence level.

- **Confirmed** — You're saying: "I can point to the exact code that proves this."
  Cite the specific file, line, and mechanism.
- **Strong** — You're saying: "Multiple independent evidence types all point to
  the same CWE." Name which types (code, description match, observed examples,
  patch analysis).
- **Supported** — You're saying: "The evidence I have points here, but I haven't
  fully verified it." State what evidence you have and what's missing.
- **Inferred** — You're saying: "I'm reasoning from confirmed facts to a logical
  conclusion." State the confirmed facts and the reasoning step.
- **Best Fit** — You're saying: "I understand the weakness well, but CWE doesn't
  have an exact match." Describe what the weakness actually is and why the chosen
  CWE is the closest approximation.
- **Uncertain** — You're saying: "I have multiple plausible CWEs and can't
  distinguish between them yet." List the candidates and what information would
  resolve the ambiguity.
```

**File:** `references/confidence-framework.md`

## 3. Multi-CWE Patterns in Phase 4

**Problem:** Phase 4 only covers linear chains. No guidance for compound weaknesses (two bugs that combine) or independent weaknesses (two unrelated bugs in same CVE).

**Fix:** Add new Step 5b in Phase 4 after "Check Against Common Patterns" and before "AI Relevance Overlay":

```markdown
### Step 5b: Multi-Weakness Topologies

Not all vulnerabilities follow a linear chain. Three patterns exist:

**Linear chain** (covered above): A enables B enables C. Root cause → enabling →
exploited → impact.

**Compound weakness**: Two or more weaknesses that are individually benign (or
low-severity) but become exploitable in combination. Neither alone is sufficient —
the vulnerability exists at their intersection.

    Contributing: CWE-362 (Race Condition) [Confirmed]
    Contributing: CWE-22 (Path Traversal) [Strong]
    → combined effect: CWE-434 (Unrestricted Upload) [Strong]
    → Impact: Arbitrary code execution

Tag each contributing weakness independently. The "combined effect" CWE describes
what becomes possible when both are present. If no single CWE captures the combined
effect, note this as a Best Fit situation.

**Independent weaknesses**: Two or more unrelated weaknesses in the same software,
reported under the same CVE or advisory. These are not a chain — they don't enable
each other. Assign each separately with its own confidence level.

    Independent #1: CWE-89 (SQL Injection) [Confirmed]
    Independent #2: CWE-79 (Cross-site Scripting) [Strong]

If independent weaknesses are bundled in a single CVE, note that the CVE covers
multiple distinct weaknesses. Some CNAs prefer separate CVEs for separate
weaknesses — flag this for the analyst.
```

And add Pattern 8 to `references/chain-patterns.md`:

```markdown
## Pattern 8: Compound Weakness (Convergent)

**Topology:** CWE-362 (Concurrent Execution Using Shared Resource with Improper
Synchronization) + CWE-22 (Path Traversal) → CWE-434 (Unrestricted Upload of File
with Dangerous Type)

**Causal flow:** A race condition in the upload handler allows a brief window where
path validation has completed but the file hasn't been written yet. A concurrent
request exploiting a path traversal during this window writes the file to an
unintended location. Neither the race condition alone (the upload directory is safe)
nor the path traversal alone (it's caught by validation) would be exploitable — the
vulnerability exists only at the intersection.

**Key difference from linear chains:** In a linear chain, each link is exploitable
in sequence. In a compound weakness, the individual weaknesses may be unexploitable
on their own. The chain notation uses "Contributing" rather than "Root Cause →
Enabling" to signal convergence rather than sequence.

**When to suspect compound weaknesses:** The vulnerability description says "only
exploitable when..." or "requires... combined with..." or the patch fixes two
seemingly unrelated issues.
```

**Files:**
- `phases/phase-4-chain-analysis.md` — new Step 5b
- `references/chain-patterns.md` — new Pattern 8

## 4. Phase 2 Sampling Note

**Problem:** No guidance on whether to sample or fully trace code in large codebases.

**Fix:** Add one sentence to `phases/phase-2-code-analysis.md` process section, at the beginning of the code tracing instructions:

```markdown
With AI-assisted analysis, the default approach is to trace the full code path in
depth rather than sampling. Only fall back to sampling if the codebase is too large
to fit in context or the analyst directs you to focus on specific components.
```

**File:** `phases/phase-2-code-analysis.md`

## 5. Out of Scope

- Worked examples (separate effort, listed in TODO.md)
- Cross-model validation Phase 7 (separate effort)
- AI relevance scope clarification (minor, can be addressed later)
- Evidence quality tiers (IC-inspired concept, worth exploring separately)
- Code changes of any kind
