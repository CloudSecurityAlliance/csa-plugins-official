# CWE Skill Methodology Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the CWE skill methodology: standardize chain format, sharpen confidence framework with IC-inspired framing, add multi-CWE patterns, add justification guidance, and add Phase 2 sampling note.

**Architecture:** Content-only changes to 5 Markdown files. No code, no tests. Each task edits one or two files and commits.

**Tech Stack:** Markdown. That's it.

**Spec:** `plugins/cwe-analysis/docs/2026-04-05-methodology-improvements-design.md`

---

### Task 1: Confidence framework — IC framing, Best Fit rewrite, justification guidance

This is the most important change — it sharpens the definitions that the entire skill relies on.

**Files:**
- Modify: `plugins/cwe-analysis/skills/cwe-analysis/references/confidence-framework.md`

- [ ] **Step 1: Add "Two Dimensions of Uncertainty" section**

In `confidence-framework.md`, insert after line 1 (`# Confidence Framework for CWE Assignments`) and the opening paragraph (line 3: "Every CWE assignment carries uncertainty..."), BEFORE the `## Confidence Levels` heading. Add:

```markdown

## Two Dimensions of Uncertainty

Adapted from intelligence community analytic standards (ICD 203), this framework distinguishes between *evidence quality* (how good is your information?) and *taxonomy precision* (how well does the CWE vocabulary cover this weakness?).

Most confidence levels reflect evidence quality — you have more or less evidence that a specific CWE matches. "Best Fit" is the only level that reflects a taxonomy gap — the evidence about the weakness itself may be strong, but the CWE system doesn't have a precise match.

Don't confuse "we're not sure which CWE" (Uncertain — an evidence problem) with "no CWE precisely fits" (Best Fit — a taxonomy problem).
```

- [ ] **Step 2: Rewrite the "Best Fit" table row**

In the Confidence Levels table, replace the existing Best Fit row:

Old:
```
| **Best Fit** | Closest available CWE, but imperfect match | No CWE precisely describes this weakness | Vulnerability involves a novel AI attack pattern; CWE-1039 is closest but doesn't capture the full mechanism |
```

New:
```
| **Best Fit** | The CWE taxonomy doesn't precisely cover this weakness. You've searched children, peers, and siblings; nothing fits better. The gap is in CWE's vocabulary, not in your analysis. | Always accompanied by: what specifically doesn't fit, and what a hypothetical better CWE would describe | Vulnerability involves a novel AI attack pattern where the model's training data is poisoned through a feedback loop; CWE-1039 is closest but doesn't capture the feedback loop mechanism. A better CWE would describe "implicit training data manipulation through adversarial feedback." |
```

- [ ] **Step 3: Add "Justification Guidance" section**

Insert AFTER the "Usage Rules" section (after rule 6, line 28: "A CWE that begins as Inferred can become Strong..."), BEFORE the "Over-Confidence Anti-Patterns" section. Add:

```markdown

## Justification Guidance

Every confidence tag answers two questions: *what do you know?* and *how do you know it?* State both. The goal is that a reviewer reading your justification can independently assess whether they agree with your confidence level.

- **Confirmed** — You're saying: "I can point to the exact code that proves this." Cite the specific file, line, and mechanism.
- **Strong** — You're saying: "Multiple independent evidence types all point to the same CWE." Name which types (code, description match, observed examples, patch analysis).
- **Supported** — You're saying: "The evidence I have points here, but I haven't fully verified it." State what evidence you have and what's missing.
- **Inferred** — You're saying: "I'm reasoning from confirmed facts to a logical conclusion." State the confirmed facts and the reasoning step.
- **Best Fit** — You're saying: "I understand the weakness well, but CWE doesn't have an exact match." Describe what the weakness actually is and why the chosen CWE is the closest approximation.
- **Uncertain** — You're saying: "I have multiple plausible CWEs and can't distinguish between them yet." List the candidates and what information would resolve the ambiguity.
```

- [ ] **Step 4: Verify the file reads correctly**

Read the full file and confirm:
- "Two Dimensions of Uncertainty" appears before the table
- Best Fit row has the new longer definition
- "Justification Guidance" appears between Usage Rules and Over-Confidence Anti-Patterns
- No broken Markdown formatting

- [ ] **Step 5: Commit**

```bash
git add plugins/cwe-analysis/skills/cwe-analysis/references/confidence-framework.md
git commit -m "docs(cwe-analysis): sharpen confidence framework with IC framing and justification guidance"
```

---

### Task 2: Chain format standardization in Phase 4

**Files:**
- Modify: `plugins/cwe-analysis/skills/cwe-analysis/phases/phase-4-chain-analysis.md`

- [ ] **Step 1: Replace the output section**

In `phase-4-chain-analysis.md`, replace the Output section (lines 59-77). The current content is:

```markdown
## Output

Present the chain:

\```
Root Cause: CWE-XXX (Name) [Confidence]
  ↓ enables
Enabling: CWE-YYY (Name) [Confidence]
  ↓ leads to
Exploited: CWE-ZZZ (Name) [Confidence]
  ↓ results in
Impact: [description of what the attacker achieves]
\```

For each link: CWE ID, Name, role in chain, confidence level, and relationship to adjacent links.

If AI relevance was applied, show annotations separately:
- CWE-XXX: View1=N, View2=N, Category=...

Then pause: "Here's the full chain with confidence levels per link. Does the causal flow make sense?"
```

Replace with:

```markdown
## Output

Present the chain using the standardized flat format:

\```
Root Cause: CWE-XXX (Name) [Confidence]
→ enables: CWE-YYY (Name) [Confidence]
→ leads to: CWE-ZZZ (Name) [Confidence]
→ Impact: [description of what the attacker achieves]
\```

For compound weaknesses (see Step 5b), use the convergent format:

\```
Contributing: CWE-XXX (Name) [Confidence]
Contributing: CWE-YYY (Name) [Confidence]
→ combined effect: [description or CWE] [Confidence]
→ Impact: [description]
\```

For each link: CWE ID, Name, confidence level, and relationship to adjacent links.

If AI relevance was applied, show annotations separately:
- CWE-XXX: View1=N, View2=N, Category=...

Then pause: "Here's the full chain with confidence levels per link. Does the causal flow make sense?"
```

NOTE: The `\``` ` above represents actual triple backticks in the Markdown file. Write actual backticks, not escaped ones.

- [ ] **Step 2: Verify formatting**

Read the file and confirm the output section has `→` arrows (not `↓`), flat format (no nested indentation), and both linear and compound formats.

- [ ] **Step 3: Commit**

```bash
git add plugins/cwe-analysis/skills/cwe-analysis/phases/phase-4-chain-analysis.md
git commit -m "docs(cwe-analysis): standardize chain format in Phase 4 to flat arrows"
```

---

### Task 3: Multi-CWE patterns — Step 5b in Phase 4 + Pattern 8 in chain-patterns.md

**Files:**
- Modify: `plugins/cwe-analysis/skills/cwe-analysis/phases/phase-4-chain-analysis.md`
- Modify: `plugins/cwe-analysis/skills/cwe-analysis/references/chain-patterns.md`

- [ ] **Step 1: Add Step 5b to Phase 4**

In `phase-4-chain-analysis.md`, insert AFTER Step 5 ("Check Against Common Patterns", which ends around line 41: "...verify the match is genuine, not just superficial similarity.") and BEFORE Step 6 ("AI Relevance Overlay"). Add:

```markdown

### Step 5b: Multi-Weakness Topologies

Not all vulnerabilities follow a linear chain. Three patterns exist:

**Linear chain** (covered above): A enables B enables C. Root cause → enabling → exploited → impact.

**Compound weakness**: Two or more weaknesses that are individually benign (or low-severity) but become exploitable in combination. Neither alone is sufficient — the vulnerability exists at their intersection.

```
Contributing: CWE-59 (Improper Link Resolution Before File Access) [Confirmed]
Contributing: CWE-693 (Protection Mechanism Failure) [Confirmed]
→ combined effect: Symlink-following by root in attacker-controlled dir [Best Fit — CWE-59]
→ Impact: Root privilege escalation
```

Tag each contributing weakness independently. The "combined effect" CWE describes what becomes possible when both are present. If no single CWE captures the combined effect, note this as a Best Fit situation.

**Independent weaknesses**: Two or more unrelated weaknesses in the same software, reported under the same CVE or advisory. These are not a chain — they don't enable each other. Assign each separately with its own confidence level.

```
Independent #1: CWE-89 (SQL Injection) [Confirmed]
Independent #2: CWE-79 (Cross-site Scripting) [Strong]
```

If independent weaknesses are bundled in a single CVE, note that the CVE covers multiple distinct weaknesses. Some CNAs prefer separate CVEs for separate weaknesses — flag this for the analyst.
```

- [ ] **Step 2: Add Pattern 8 to chain-patterns.md**

In `references/chain-patterns.md`, append after Pattern 7 (Path Traversal Chain) and before the "CWE Relationship Vocabulary" section:

```markdown

## Pattern 8: Compound Weakness (Convergent)

**Real-world example:** CVE-2026-31979 — Himmelblau symlink privilege escalation

**Topology:** CWE-59 (Improper Link Resolution Before File Access) + CWE-693 (Protection Mechanism Failure) → root privilege escalation

**Causal flow:** The Himmelblau daemon (running as root) writes Kerberos credential cache files to `/tmp/krb5cc_<uid>` without checking for symlinks (CWE-59). Separately, a code change removed `PrivateTmp=true` from the systemd unit, exposing the daemon's `/tmp` to unprivileged users (CWE-693). Neither alone is exploitable: the symlink-following code is harmless when `/tmp` is namespaced (no attacker access), and shared `/tmp` is harmless when the daemon validates symlinks. Combined, an unprivileged user creates a symlink pointing to `/etc/shadow`, and the root daemon follows it — full privilege escalation.

**Key difference from linear chains:** In a linear chain, each link is exploitable in sequence. In a compound weakness, the individual weaknesses may be unexploitable on their own. The chain notation uses "Contributing" rather than "Root Cause → Enabling" to signal convergence rather than sequence. Neither weakness "enables" the other — they are orthogonal (one is a code flaw, the other a configuration flaw).

**When to suspect compound weaknesses:** The vulnerability description says "only exploitable when..." or "requires... combined with..." or the patch fixes two seemingly unrelated issues.
```

- [ ] **Step 3: Verify both files**

Read both files and confirm:
- Phase 4 has Step 5b between Step 5 and Step 6
- chain-patterns.md has Pattern 8 before the Relationship Vocabulary section
- Code block examples render correctly

- [ ] **Step 4: Commit**

```bash
git add plugins/cwe-analysis/skills/cwe-analysis/phases/phase-4-chain-analysis.md plugins/cwe-analysis/skills/cwe-analysis/references/chain-patterns.md
git commit -m "docs(cwe-analysis): add multi-CWE patterns — compound and independent weaknesses"
```

---

### Task 4: Chain format in Phase 6 + Phase 2 sampling note

**Files:**
- Modify: `plugins/cwe-analysis/skills/cwe-analysis/phases/phase-6-report.md`
- Modify: `plugins/cwe-analysis/skills/cwe-analysis/phases/phase-2-code-analysis.md`

- [ ] **Step 1: Update Phase 6 chain notation**

In `phase-6-report.md`, replace the Weakness Chain example (lines 27-30):

Old:
```markdown
**Weakness Chain** (if Phase 4 was completed):
\```
Root Cause: CWE-[ID] ([Name]) [Confidence]
  → Enabling: CWE-[ID] ([Name]) [Confidence]
    → Exploited: CWE-[ID] ([Name]) [Confidence]
      → Impact: [description]
\```
```

New:
```markdown
**Weakness Chain** (if Phase 4 was completed):
\```
Root Cause: CWE-[ID] ([Name]) [Confidence]
→ enables: CWE-[ID] ([Name]) [Confidence]
→ leads to: CWE-[ID] ([Name]) [Confidence]
→ Impact: [description]
\```

For compound weaknesses:
\```
Contributing: CWE-[ID] ([Name]) [Confidence]
Contributing: CWE-[ID] ([Name]) [Confidence]
→ combined effect: CWE-[ID] ([Name]) [Confidence]
→ Impact: [description]
\```
```

NOTE: Write actual triple backticks in the file, not escaped ones.

- [ ] **Step 2: Add sampling note to Phase 2**

In `phase-2-code-analysis.md`, insert after the `## Process` heading (line 15) and before `### Step 1: Locate the Entry Point` (line 16):

```markdown

With AI-assisted analysis, the default approach is to trace the full code path in depth rather than sampling. Only fall back to sampling if the codebase is too large to fit in context or the analyst directs you to focus on specific components.
```

- [ ] **Step 3: Verify both files**

Read both files and confirm:
- Phase 6 chain notation uses flat `→` format with lowercase labels, includes compound format
- Phase 2 has the sampling note before Step 1

- [ ] **Step 4: Commit**

```bash
git add plugins/cwe-analysis/skills/cwe-analysis/phases/phase-6-report.md plugins/cwe-analysis/skills/cwe-analysis/phases/phase-2-code-analysis.md
git commit -m "docs(cwe-analysis): standardize Phase 6 chain format, add Phase 2 sampling note"
```

---

### Task 5: Final verification and push

- [ ] **Step 1: Run existing tests to confirm nothing broke**

```bash
python3 plugins/cwe-analysis/scripts/test_cwe_tool.py && python3 plugins/cwe-analysis/scripts/test_doc_truth.py
```

Expected: 30/30 tool tests, 6/6 doc truth tests. No code was changed, so these should still pass.

- [ ] **Step 2: Push and open PR**

```bash
git push -u origin feat/methodology-improvements
gh pr create --title "docs(cwe-analysis): methodology improvements — confidence framework, chain format, multi-CWE" --body "$(cat <<'EOF'
## Summary

- **Confidence framework sharpened**: IC-inspired (ICD 203) two-dimensions-of-uncertainty framing. "Best Fit" rewritten with clear boundary vs Supported/Uncertain. Justification guidance section added — states the goal/intent of each confidence level.
- **Chain format standardized**: Flat `→` format with descriptive labels, identical in Phase 4 and Phase 6. Copy-paste friendly.
- **Multi-CWE patterns**: New Step 5b in Phase 4 covering compound weaknesses (two bugs that combine, e.g. CVE-2026-31979) and independent weaknesses (two unrelated bugs). Pattern 8 added to chain-patterns.md with real-world example.
- **Phase 2 sampling note**: Default to full code tracing with AI-assisted analysis.

Design spec: `plugins/cwe-analysis/docs/2026-04-05-methodology-improvements-design.md`

## Test plan

- [ ] All 36 existing tests pass (no code changes, content only)
- [ ] Read confidence-framework.md — "Two Dimensions" section present, Best Fit definition sharp, Justification Guidance section present
- [ ] Read phase-4-chain-analysis.md — flat `→` format in output, Step 5b with compound/independent patterns
- [ ] Read phase-6-report.md — chain notation matches Phase 4 format
- [ ] Read chain-patterns.md — Pattern 8 with CVE-2026-31979 example
- [ ] Read phase-2-code-analysis.md — sampling note before Step 1

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```
