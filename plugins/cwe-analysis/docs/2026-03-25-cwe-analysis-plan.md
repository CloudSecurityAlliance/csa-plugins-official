# CWE Analysis Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the cwe-analysis Claude Code plugin — a guided CWE assignment tool for CNAs, security researchers, and vendors.

**Architecture:** A Claude Code plugin with bundled CWE data (~944 entries as CSV), a Python indexing script (`cwe-tool.py`), and a progressive-disclosure skill with 6 phases, 5 reference docs, and analyst pause points. All files are markdown or Python stdlib. No build step, no external dependencies.

**Tech Stack:** Python 3 (stdlib only: csv, argparse, json, os, sys, re), Markdown, Claude Code plugin format

**Spec:** `docs/2026-03-25-cwe-analysis-plugin-design.md`

**Working directory:** `/Users/kurt/GitHub/CloudSecurityAlliance/csa-plugins-official/plugins/cwe-analysis/`

---

## File Map

### Already exists (data bundle)
- `data/CWE-AI-Classifications.csv` — AI relevance scores (944 rows)
- `data/CWE-Research-Concepts-1000.csv` — full MITRE CWE data (944 rows)
- `data/MITRE-CWE-LICENSE.txt` — MITRE terms of use
- `data/VERSION.txt` — data version metadata
- `LICENSE` — Apache 2.0
- `README.md` — plugin overview
- `docs/2026-03-25-cwe-analysis-plugin-design.md` — design spec

### To create
- `plugin.json` — plugin manifest
- `FEEDBACK.md` — issue reporting instructions
- `scripts/cwe-tool.py` — CWE data indexing tool (6 subcommands)
- `skills/cwe-analysis/SKILL.md` — main skill router
- `skills/cwe-analysis/phases/phase-1-intake.md`
- `skills/cwe-analysis/phases/phase-2-code-analysis.md`
- `skills/cwe-analysis/phases/phase-3-cwe-identification.md`
- `skills/cwe-analysis/phases/phase-4-chain-analysis.md`
- `skills/cwe-analysis/phases/phase-5-validation.md`
- `skills/cwe-analysis/phases/phase-6-report.md`
- `skills/cwe-analysis/references/confidence-framework.md`
- `skills/cwe-analysis/references/quality-framework.md`
- `skills/cwe-analysis/references/abstraction-guide.md`
- `skills/cwe-analysis/references/chain-patterns.md`
- `skills/cwe-analysis/references/ai-relevance-guide.md`

---

## Task 1: Plugin Manifest and Feedback

**Files:**
- Create: `plugin.json`
- Create: `FEEDBACK.md`

- [ ] **Step 1: Create plugin.json**

```json
{
  "name": "cwe-analysis",
  "description": "CWE assignment and vulnerability chain analysis for CNAs, security researchers, and vendors. Guides analysts through vulnerability understanding, code examination, CWE identification, chain mapping, and quality validation.",
  "version": "0.1.0",
  "author": {
    "name": "Kurt Seifried",
    "email": "kseifried@cloudsecurityalliance.org"
  },
  "skills": [
    "skills/cwe-analysis/SKILL.md"
  ]
}
```

- [ ] **Step 2: Create FEEDBACK.md**

Follow the incident-analysis plugin template. Replace `[incident-analysis]` with `[cwe-analysis]`. Remove the methodology-rationale reference (this plugin doesn't have one yet). Keep everything else identical.

Reference: `../incident-analysis/FEEDBACK.md`

- [ ] **Step 3: Verify JSON is valid**

Run: `python3 -c "import json; json.load(open('plugin.json'))"`
Expected: no output (valid JSON)

- [ ] **Step 4: Commit**

```bash
git add plugin.json FEEDBACK.md
git commit -m "feat(cwe-analysis): add plugin manifest and feedback template"
```

---

## Task 2: cwe-tool.py — Data Loading and Lookup

The script is built incrementally: data loading first, then one subcommand at a time. Each subcommand gets a test before implementation.

**Files:**
- Create: `scripts/cwe-tool.py`
- Create: `scripts/test_cwe_tool.py`

- [ ] **Step 1: Write test for data loading and lookup**

```python
"""Tests for cwe-tool.py — run from the scripts/ directory."""
import subprocess
import json
import sys
import os

TOOL = os.path.join(os.path.dirname(__file__), "cwe-tool.py")

def run(args, expect_rc=0):
    result = subprocess.run(
        [sys.executable, TOOL] + args,
        capture_output=True, text=True
    )
    assert result.returncode == expect_rc, f"Exit {result.returncode}: {result.stderr}"
    return result.stdout

def test_lookup_known_cwe():
    out = run(["lookup", "79"])
    assert "CWE-79" in out
    assert "Cross-site Scripting" in out or "Web Page Generation" in out

def test_lookup_known_cwe_json():
    out = run(["lookup", "79", "--json"])
    data = json.loads(out)
    assert data["CWE-ID"] == "79" or data["CWE-ID"] == 79

def test_lookup_nonexistent():
    out = run(["lookup", "999999"], expect_rc=1)

if __name__ == "__main__":
    test_lookup_known_cwe()
    test_lookup_known_cwe_json()
    test_lookup_nonexistent()
    print("All lookup tests passed")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd scripts && python3 test_cwe_tool.py`
Expected: FAIL — cwe-tool.py doesn't exist yet

- [ ] **Step 3: Implement data loading and lookup subcommand**

Create `scripts/cwe-tool.py` with:
- `DATA_DIR` resolved via `os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")`
- `load_mitre_csv()` — reads CWE-Research-Concepts-1000.csv into a dict keyed by CWE-ID (string, no prefix)
- `load_ai_csv()` — reads CWE-AI-Classifications.csv into a dict keyed by CWE_ID
- `cmd_lookup(cwe_id, as_json)` — looks up by ID in both CSVs, prints combined output
- `argparse` main with `lookup` subcommand accepting positional CWE-ID and `--json` flag
- Human-readable output format: section headers (Description, Abstraction, Related Weaknesses, etc.) with values. AI scores shown if present.

CSV headers to match exactly:
- MITRE: `CWE-ID,Name,Weakness Abstraction,Status,Description,Extended Description,Related Weaknesses,...`
- AI: `CWE_ID,Name,MITRE_AI_Tagged,View1_Score,View2_Score,...`

Note: MITRE CSV uses `CWE-ID` with hyphen, AI CSV uses `CWE_ID` with underscore.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd scripts && python3 test_cwe_tool.py`
Expected: All lookup tests passed

- [ ] **Step 5: Commit**

```bash
git add scripts/cwe-tool.py scripts/test_cwe_tool.py
git commit -m "feat(cwe-analysis): add cwe-tool.py with data loading and lookup"
```

---

## Task 3: cwe-tool.py — Search Subcommand

**Files:**
- Modify: `scripts/cwe-tool.py`
- Modify: `scripts/test_cwe_tool.py`

- [ ] **Step 1: Write tests for search**

Add to `test_cwe_tool.py`:

```python
def test_search_injection():
    out = run(["search", "injection"])
    assert "CWE-" in out
    # Should find multiple injection-related CWEs
    assert out.count("CWE-") > 5

def test_search_multiple_keywords():
    out = run(["search", "sql", "injection"])
    assert "CWE-89" in out

def test_search_no_results():
    out = run(["search", "xyznonexistentkeywordxyz"])
    assert "No matches" in out or "0 matches" in out
```

- [ ] **Step 2: Run tests — search tests should fail**

Run: `cd scripts && python3 test_cwe_tool.py`

- [ ] **Step 3: Implement search subcommand**

Add to `cwe-tool.py`:
- `cmd_search(keywords, as_json)` — searches Name and Description fields for all keywords (AND logic, case-insensitive). Returns matching CWE-IDs with Name, Abstraction, and truncated Description.
- Register `search` subparser with positional `keywords` (nargs="+") and `--json` flag

- [ ] **Step 4: Run tests — all should pass**

Run: `cd scripts && python3 test_cwe_tool.py`

- [ ] **Step 5: Commit**

```bash
git add scripts/cwe-tool.py scripts/test_cwe_tool.py
git commit -m "feat(cwe-analysis): add search subcommand to cwe-tool.py"
```

---

## Task 4: cwe-tool.py — Candidates Subcommand

**Files:**
- Modify: `scripts/cwe-tool.py`
- Modify: `scripts/test_cwe_tool.py`

- [ ] **Step 1: Write tests for candidates**

```python
def test_candidates_by_impact():
    out = run(["candidates", "--impact", "code execution"])
    assert "CWE-" in out

def test_candidates_by_abstraction():
    out = run(["candidates", "--abstraction", "Variant"])
    assert "CWE-" in out
    assert "Variant" in out

def test_candidates_sorted_by_specificity():
    """Variants should appear before Base, Base before Class."""
    out = run(["candidates", "--impact", "injection", "--json"])
    data = json.loads(out)
    if len(data) > 1:
        abstractions = [e.get("Weakness Abstraction", "") for e in data]
        # Just verify we got results sorted — Variant before Class
        specificity = {"Variant": 0, "Base": 1, "Class": 2, "Pillar": 3}
        scores = [specificity.get(a, 4) for a in abstractions]
        assert scores == sorted(scores)
```

- [ ] **Step 2: Run tests — candidates tests should fail**

- [ ] **Step 3: Implement candidates subcommand**

Add to `cwe-tool.py`:
- `cmd_candidates(impact, abstraction, as_json)` — filters MITRE data only (no AI classification filters)
  - `--impact` filters on Common Consequences field (case-insensitive substring)
  - `--abstraction` filters on Weakness Abstraction field (exact match)
  - Sort by specificity: Variant > Base > Class > Pillar
- Register `candidates` subparser with `--impact`, `--abstraction`, `--json`

- [ ] **Step 4: Run tests — all should pass**

- [ ] **Step 5: Commit**

```bash
git add scripts/cwe-tool.py scripts/test_cwe_tool.py
git commit -m "feat(cwe-analysis): add candidates subcommand to cwe-tool.py"
```

---

## Task 5: cwe-tool.py — Children Subcommand

**Files:**
- Modify: `scripts/cwe-tool.py`
- Modify: `scripts/test_cwe_tool.py`

- [ ] **Step 1: Write tests for children**

```python
def test_children_of_injection():
    """CWE-74 (Injection) should have children like CWE-79, CWE-89, CWE-77."""
    out = run(["children", "74"])
    # These are known children of CWE-74
    assert any(cwe in out for cwe in ["CWE-79", "CWE-89", "CWE-77"])

def test_children_of_leaf():
    """A very specific Variant CWE should have few or no children."""
    out = run(["children", "5"])  # CWE-5: J2EE Misconfiguration
    # May have 0 children — just verify it doesn't crash
    assert "CWE-5" in out or "No children" in out or "0 children" in out
```

- [ ] **Step 2: Run tests — children tests should fail**

- [ ] **Step 3: Implement children subcommand**

Add to `cwe-tool.py`:
- `cmd_children(cwe_id, as_json)` — scans all MITRE entries' Related Weaknesses field for `ChildOf` relationships pointing to the given CWE-ID. The Related Weaknesses field format is `::NATURE:ChildOf:CWE ID:74:VIEW ID:1000:ORDINAL:Primary::` — parse this to extract parent CWE IDs.
- Returns child CWE-IDs with Name, Abstraction level
- Register `children` subparser with positional CWE-ID and `--json`

- [ ] **Step 4: Run tests — all should pass**

- [ ] **Step 5: Commit**

```bash
git add scripts/cwe-tool.py scripts/test_cwe_tool.py
git commit -m "feat(cwe-analysis): add children subcommand to cwe-tool.py"
```

---

## Task 6: cwe-tool.py — Chain Subcommand

**Files:**
- Modify: `scripts/cwe-tool.py`
- Modify: `scripts/test_cwe_tool.py`

- [ ] **Step 1: Write tests for chain**

```python
def test_chain_two_cwes():
    """Show relationship info for CWE-20 and CWE-89."""
    out = run(["chain", "20", "89"])
    assert "CWE-20" in out
    assert "CWE-89" in out

def test_chain_three_cwes():
    out = run(["chain", "502", "94", "78"])
    assert "CWE-502" in out
    assert "CWE-94" in out
    assert "CWE-78" in out

def test_chain_single_cwe_error():
    """Chain requires 2+ CWE IDs."""
    run(["chain", "79"], expect_rc=1)  # custom validation error
```

- [ ] **Step 2: Run tests — chain tests should fail**

- [ ] **Step 3: Implement chain subcommand**

Add to `cwe-tool.py`:
- `cmd_chain(cwe_ids, as_json)` — first validate `len(cwe_ids) >= 2`, print error and `sys.exit(1)` if not. For each CWE ID, load full entry from both CSVs. Then for each pair, check if any relationship exists in the Related Weaknesses field (ChildOf, PeerOf, CanPrecede, CanFollow, etc.).
- Output: for each CWE, show Name, Abstraction, Description (truncated). Then a "Relationships Found" section listing any MITRE-defined relationships between the given CWEs. Include a note: "Note: CWE relationships are taxonomic. Absence of a relationship does not mean these CWEs are unrelated in an exploit chain."
- If AI classifications exist for any of the CWEs, append an "AI Relevance" section with View1/View2 scores.
- Register `chain` subparser with positional `cwe_ids` (nargs="+") and `--json`. Note: argparse `nargs="+"` allows 1 arg, so the `cmd_chain` function must validate length >= 2 explicitly.

- [ ] **Step 4: Run tests — all should pass**

- [ ] **Step 5: Commit**

```bash
git add scripts/cwe-tool.py scripts/test_cwe_tool.py
git commit -m "feat(cwe-analysis): add chain subcommand to cwe-tool.py"
```

---

## Task 7: cwe-tool.py — AI-Relevant Subcommand

**Files:**
- Modify: `scripts/cwe-tool.py`
- Modify: `scripts/test_cwe_tool.py`

- [ ] **Step 1: Write tests for ai-relevant**

```python
def test_ai_relevant_default():
    out = run(["ai-relevant"])
    # Default min-score is 2, should find ~199 entries
    assert "CWE-" in out

def test_ai_relevant_high_score():
    out = run(["ai-relevant", "--min-score", "4"])
    # Score 4 entries: CWE-1427, CWE-1039, CWE-502, CWE-1434, CWE-77, CWE-78, CWE-918, CWE-1426
    assert "CWE-1427" in out or "CWE-77" in out

def test_ai_relevant_json():
    out = run(["ai-relevant", "--min-score", "4", "--json"])
    data = json.loads(out)
    # Verify known score-4 CWEs are present (data-version-dependent count)
    ids = [str(e.get("CWE_ID", "")) for e in data]
    assert "1427" in ids  # Prompt Injection
    assert "77" in ids or "78" in ids  # Command Injection
    assert len(data) >= 4  # at least the 4 View1=4 entries
```

- [ ] **Step 2: Run tests — ai-relevant tests should fail**

- [ ] **Step 3: Implement ai-relevant subcommand**

Add to `cwe-tool.py`:
- `cmd_ai_relevant(min_score, as_json)` — filters AI classifications CSV by Max_Score >= min_score. Returns CWE_ID, Name, View1_Score, View2_Score, AI_Category, Attack_Surface. Sorted by Max_Score descending, then CWE_ID ascending.
- Register `ai-relevant` subparser with `--min-score` (default 2) and `--json`

- [ ] **Step 4: Run tests — all should pass**

- [ ] **Step 5: Run full test suite**

Run: `cd scripts && python3 test_cwe_tool.py`
Expected: All tests passed

- [ ] **Step 6: Commit**

```bash
git add scripts/cwe-tool.py scripts/test_cwe_tool.py
git commit -m "feat(cwe-analysis): add ai-relevant subcommand to cwe-tool.py"
```

---

## Task 8: Reference Documents

These are the analytical frameworks referenced by phase files. Create them before the phases so the phases can reference them.

**Files:**
- Create: `skills/cwe-analysis/references/confidence-framework.md`
- Create: `skills/cwe-analysis/references/quality-framework.md`
- Create: `skills/cwe-analysis/references/abstraction-guide.md`
- Create: `skills/cwe-analysis/references/chain-patterns.md`
- Create: `skills/cwe-analysis/references/ai-relevance-guide.md`

- [ ] **Step 1: Create confidence-framework.md**

Content is fully specified in the design spec under "Reference Materials > confidence-framework.md". Copy the full table (6 levels: Confirmed, Strong, Supported, Inferred, Best Fit, Uncertain), the 6 usage rules, and the 4 over-confidence anti-patterns verbatim from the spec.

- [ ] **Step 2: Create quality-framework.md**

The 5 validation checks. For each, write:
- **What it looks like** — concrete CWE assignment mistake
- **How to detect it** — which `cwe-tool.py` command to run
- **How to fix it** — what to do instead
- **Real-world example** — actual CVE where this went wrong

The 5 checks:
1. Too abstract — e.g., assigning CWE-20 when CWE-89 fits. Detect: `cwe-tool.py children`. Fix: use the most specific child.
2. Wrong abstraction level — e.g., using a Pillar when a Base exists. Detect: `cwe-tool.py lookup` to check abstraction field. Fix: consult abstraction-guide.md.
3. Missing chain links — causal gap between root cause and impact. Detect: review chain for logical leaps. Fix: add intermediate CWEs.
4. Data currency — bundled data may be outdated. Detect: check VERSION.txt date. Fix: note limitation, suggest checking mitre.org.
5. Cause vs. consequence confusion — e.g., labeling the impact (code execution) instead of the weakness (command injection). Detect: verify each CWE describes a weakness, not an outcome. Fix: separate weakness from impact.

- [ ] **Step 3: Create abstraction-guide.md**

Content:
- Definitions: Pillar (highest abstraction, never assign directly), Class (broad categories), Base (most common assignment level), Variant (most specific, preferred when available)
- Decision tree: "Is there a Variant that matches? → Use it. Is there a Base? → Use it. Class? → Use it only if no Base/Variant fits. Pillar? → Never use directly."
- Discouraged CWEs list: CWE-20 (Improper Input Validation), CWE-NVD-noinfo (Insufficient Information), CWE-noinfo, CWE-Other. For each: why it's discouraged and what to use instead.
- MITRE's CNA mapping guidance summary (reference https://cwe.mitre.org/documents/cwe_usage/guidance.html)

- [ ] **Step 4: Create chain-patterns.md**

Common vulnerability chain templates with CWE IDs:

1. **Web injection chain**: CWE-20 (Input Validation) → CWE-89 (SQL Injection) → CWE-200 (Information Exposure)
2. **Command execution chain**: CWE-20 → CWE-78 (OS Command Injection) → CWE-269 (Improper Privilege Management)
3. **XSS chain**: CWE-79 (XSS) → CWE-352 (CSRF) — XSS enables CSRF
4. **AI prompt injection chain**: CWE-1427 (Prompt Injection) → CWE-1426 (Output Validation Failure) → CWE-78 (Command Injection)
5. **Supply chain / model loading**: CWE-494 (Download Without Integrity Check) → CWE-502 (Deserialization) → CWE-94 (Code Injection)
6. **Auth bypass chain**: CWE-287 (Improper Auth) → CWE-862 (Missing Authorization) → CWE-200 (Information Exposure)
7. **Path traversal chain**: CWE-22 (Path Traversal) → CWE-434 (Unrestricted Upload) → CWE-94 (Code Injection)

For each: the chain with CWE IDs, a 2-3 sentence explanation of causal flow, and CWE relationship vocabulary (CanPrecede, etc.) where it exists in MITRE's data.

Include a note: "These are common patterns, not exhaustive. Real vulnerabilities may follow chains not listed here. The chain tool (`cwe-tool.py chain`) can show what MITRE relationships exist between any set of CWEs."

- [ ] **Step 5: Create ai-relevance-guide.md**

Condensed from the dataset repo's CWE-AI-METHODOLOGY.md and AI-ATTACK-SURFACE-MODEL.md:
- The two-view model explained: View 1 (Attacks ON AI) vs View 2 (Attacks VIA AI)
- Scoring scale 0-4 with one-line definitions
- The 8 score-4 CWEs listed with brief explanations
- The four attack surfaces (Infrastructure, AI Core, AI Outputs, Supply Chain) with 1-2 sentence descriptions
- When to apply: "Apply AI relevance scoring only after identifying the correct CWE. This is supplementary context for vulnerabilities in AI systems, not a filter for candidate selection."
- How to use the data: "`cwe-tool.py lookup <ID>` shows AI scores if present. `cwe-tool.py ai-relevant` lists all AI-relevant CWEs."

Reference source files (in the dataset repo, not bundled):
- `frameworks-guidance/industry/MITRE/CWE/CWE-AI-METHODOLOGY.md`
- `frameworks-guidance/industry/MITRE/CWE/AI-ATTACK-SURFACE-MODEL.md`
- `frameworks-guidance/industry/MITRE/CWE/CWE-AI-RELEVANCE-REPORT.md`

- [ ] **Step 6: Commit**

```bash
git add skills/cwe-analysis/references/
git commit -m "feat(cwe-analysis): add reference documents (confidence, quality, abstraction, chains, AI relevance)"
```

---

## Task 9: Phase Files

**Files:**
- Create: `skills/cwe-analysis/phases/phase-1-intake.md`
- Create: `skills/cwe-analysis/phases/phase-2-code-analysis.md`
- Create: `skills/cwe-analysis/phases/phase-3-cwe-identification.md`
- Create: `skills/cwe-analysis/phases/phase-4-chain-analysis.md`
- Create: `skills/cwe-analysis/phases/phase-5-validation.md`
- Create: `skills/cwe-analysis/phases/phase-6-report.md`

Follow the incident-analysis phase file style: Purpose, Process (numbered steps), Teaching Moment (if teaching mode on), Output, Pause text. Each phase file is self-contained — it includes everything needed to execute that phase.

- [ ] **Step 1: Create phase-1-intake.md**

Content from spec Phase 1. Structure:
- Purpose: understand what the analyst knows
- Process: 6 questions (affected system, trigger, impact, source code availability, existing CVE/CWE, AI/ML system?)
- Teaching moment: "CWE assignment quality depends entirely on understanding the vulnerability correctly. A vague description leads to vague CWEs."
- Output: structured vulnerability summary
- Pause text

- [ ] **Step 2: Create phase-2-code-analysis.md**

Content from spec Phase 2. Structure:
- Purpose: examine the code path (optional)
- When to skip: no source code available
- Process: trace input to impact, identify missing validation, note trust boundaries, distinguish root cause from symptom, mark specific lines
- Teaching moment: "Root cause vs. symptom: if user input reaches a SQL query without sanitization, the symptom is SQL injection (CWE-89) but the root cause may be missing input validation at the trust boundary. Both matter for CWE assignment."
- Output: annotated code path
- Pause text

- [ ] **Step 3: Create phase-3-cwe-identification.md**

Content from spec Phase 3. Structure:
- Prerequisites: read confidence-framework.md and abstraction-guide.md
- Purpose: find candidate CWEs
- Process: search with cwe-tool.py (search, candidates, children, lookup), tag each with confidence level, rank by fit
- **Critical constraint**: "Do NOT filter candidates by AI category or AI relevance score. Identify the correct weakness first based on weakness properties only."
- Teaching moment: common mistakes (First Match trap, Name Match trap)
- Output: 3-5 ranked candidates with confidence and justification
- Pause text

- [ ] **Step 4: Create phase-4-chain-analysis.md**

Content from spec Phase 4. Structure:
- Purpose: build weakness chain (optional)
- Process: map root cause → enabling → exploited → impact, use chain tool for relationship info (explicitly note it's information retrieval, not validation), tag each link independently, check chain-patterns.md
- AI relevance overlay: after chain is established, annotate with AI scores if applicable
- Teaching moment: "CWE relationships in MITRE's data are taxonomic (ChildOf, PeerOf), not exploit-flow maps. A valid exploit chain may connect CWEs that have no MITRE relationship. Use the relationships as hints, not proof."
- Output: ordered chain with per-link confidence
- Pause text

- [ ] **Step 5: Create phase-5-validation.md**

Content from spec Phase 5. Structure:
- Purpose: quality checks
- Process: run each of the 5 checks with specific cwe-tool.py commands:
  1. `cwe-tool.py children <ID>` — check for more specific children
  2. `cwe-tool.py lookup <ID>` — verify abstraction level
  3. Review chain for causal gaps
  4. Read data/VERSION.txt — data currency disclosure
  5. Verify each CWE describes a weakness, not an outcome
- Output: validation report (pass/flag per check)
- Flow: if all pass → Phase 6. If flagged → present issues, ask analyst.

- [ ] **Step 6: Create phase-6-report.md**

Content from spec Phase 6. Structure:
- Purpose: generate CNA-ready output
- Output format: concise text block with sections:
  - Primary CWE assignment (ID, Name, confidence level)
  - Justification paragraph
  - Chain (if Phase 4 done) — each link with CWE, role, confidence
  - Abstraction level confirmation
  - AI relevance annotations (if applicable, labeled as supplementary)
  - Data currency note
  - CWE documentation links
  - Uncertain assignments with resolution criteria
- Output options: display or write to file
- Teaching moment: "A good CWE assignment justification should be one paragraph that a CNA reviewer can read and immediately understand why this CWE was chosen. Cite specific evidence."

- [ ] **Step 7: Commit**

```bash
git add skills/cwe-analysis/phases/
git commit -m "feat(cwe-analysis): add phase files (intake through report)"
```

---

## Task 10: SKILL.md — Main Router

**Files:**
- Create: `skills/cwe-analysis/SKILL.md`

- [ ] **Step 1: Create SKILL.md**

The main skill file with:
- YAML frontmatter (name, description from spec)
- Opening paragraph: "You are guiding an analyst through CWE assignment for a vulnerability..."
- Scope section
- Teaching mode section
- Tool access section (cwe-tool.py, file reading, grep — no web required)
- Workflow routing with explicit file paths:
  - Option 1: Full Workflow — all 6 phases with exact `phases/phase-N-*.md` paths and `references/*.md` paths
  - Option 2: Specific Phase
  - Option 3: Continue Previous
- Important section (9 behavioral rules from spec)
- Feedback section

The script invocation pattern in SKILL.md should instruct Claude to resolve the plugin root from the skill file's absolute path, then invoke the script. Write it as:

```
The cwe-tool.py script is located at `scripts/cwe-tool.py` relative to this plugin's root directory. To find the plugin root, resolve this SKILL.md file's absolute path and navigate up two directories (from `skills/cwe-analysis/SKILL.md` to the plugin root). Then invoke:

python3 <resolved-plugin-root>/scripts/cwe-tool.py <subcommand> [args]
```

Do NOT use a hardcoded relative path like `../../scripts/` — Claude Code's working directory is the user's project, not the skill file's directory. The skill must instruct Claude to resolve the absolute path dynamically.

- [ ] **Step 2: Verify all referenced files exist**

Run: `find skills/ scripts/ data/ -type f | sort`
Cross-check every path mentioned in SKILL.md exists.

- [ ] **Step 3: Commit**

```bash
git add skills/cwe-analysis/SKILL.md
git commit -m "feat(cwe-analysis): add SKILL.md main router"
```

---

## Task 11: Marketplace Registration

**Files:**
- Modify: `../../.claude-plugin/marketplace.json`

- [ ] **Step 1: Add cwe-analysis to marketplace**

Add a second entry to the `plugins` array in `.claude-plugin/marketplace.json`:

```json
{
  "name": "cwe-analysis",
  "description": "CWE assignment and vulnerability chain analysis for CNAs, security researchers, and vendors. Guides analysts through vulnerability understanding, code examination, CWE identification, chain mapping, and quality validation.",
  "author": {
    "name": "Cloud Security Alliance",
    "email": "research@cloudsecurityalliance.org"
  },
  "source": "./plugins/cwe-analysis",
  "category": "security",
  "homepage": "https://github.com/CloudSecurityAlliance/csa-plugins-official/tree/main/plugins/cwe-analysis"
}
```

- [ ] **Step 2: Verify JSON is valid**

Run: `python3 -c "import json; json.load(open('../../.claude-plugin/marketplace.json'))"`

- [ ] **Step 3: Commit**

```bash
git add ../../.claude-plugin/marketplace.json
git commit -m "feat(cwe-analysis): register plugin in marketplace"
```

---

## Task 12: Integration Test

**Files:** None (test only)

- [ ] **Step 1: Verify plugin structure matches spec**

Run from plugin root:
```bash
find . -type f | grep -v __pycache__ | grep -v .pyc | sort
```
Cross-check against the Plugin Structure tree in the design spec.

- [ ] **Step 2: Run all cwe-tool.py tests**

Run: `cd scripts && python3 test_cwe_tool.py`
Expected: All tests passed

- [ ] **Step 3: Test each subcommand manually**

```bash
cd scripts
python3 cwe-tool.py lookup 1427
python3 cwe-tool.py search "prompt injection"
python3 cwe-tool.py candidates --impact "code execution" --abstraction Base
python3 cwe-tool.py children 74
python3 cwe-tool.py chain 1427 1426 78
python3 cwe-tool.py ai-relevant --min-score 4
```

Verify each produces reasonable output.

- [ ] **Step 4: Verify plugin.json references valid skill path**

Run: `python3 -c "import json; d=json.load(open('plugin.json')); [print(s) for s in d['skills']]"`
Then verify each printed path exists: `ls -la skills/cwe-analysis/SKILL.md`

- [ ] **Step 5: Final commit if any fixes were needed**

Stage only the specific files that were fixed, then commit:
```bash
git add <specific changed files>
git commit -m "fix(cwe-analysis): integration test fixes"
```
