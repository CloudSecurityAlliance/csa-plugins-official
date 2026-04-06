# Phase 6: Report

## Purpose

Generate the final CWE assignment in a concise, CNA-ready format. This is the deliverable — a text block that can go directly into a CVE record's justification or an internal vulnerability report.

## Output Format

The canonical output is a **CNA-ready text block** — concise prose suitable for CVE record justification. Structured JSON output (CVE 5.0 schema) is a planned future addition.

## Process

### Step 1: Assemble the Report

Compile from prior phases:

**Primary CWE Assignment:**
```
CWE-[ID]: [Name] [Confidence Level]
```

**Justification:**
A concise paragraph (3-5 sentences) explaining why this CWE was selected. Cite specific evidence: vulnerability description, code analysis findings, CWE description match, observed examples. This paragraph should be understandable by a CNA reviewer who has not seen the prior analysis.

**Weakness Chain** (if Phase 4 was completed):
```
Root Cause: CWE-[ID] ([Name]) [Confidence]
→ enables: CWE-[ID] ([Name]) [Confidence]
→ leads to: CWE-[ID] ([Name]) [Confidence]
→ Impact: [description]
```

For compound weaknesses:
```
Contributing: CWE-[ID] ([Name]) [Confidence]
Contributing: CWE-[ID] ([Name]) [Confidence]
→ combined effect: CWE-[ID] ([Name]) [Confidence]
→ Impact: [description]
```

**Abstraction Level:**
Confirm the assigned CWE is at the appropriate level (Base or Variant preferred). Note if this is the most specific CWE available.

**AI Relevance** (if applicable, labeled as supplementary context):
```
AI Relevance: View1=[N] (Attacks ON AI), View2=[N] (Attacks VIA AI)
Category: [category], Attack Surface: [surface]
```

**Data Currency:**
```
Analysis based on CWE data version [version], exported [date].
```

**References:**
Links to CWE documentation for each assigned CWE:
`https://cwe.mitre.org/data/definitions/[ID].html`

**Unresolved Items** (if any):
Any Uncertain assignments with competing candidates and what information would resolve them.

### Step 2: Review the Report

Before presenting to the analyst, verify:
- Is the justification paragraph self-contained and clear?
- Are all confidence levels included?
- Are CWE documentation links correct?
- Does the report accurately reflect the analysis from prior phases?

### Step 3: Present to the Analyst

Display the full report. Ask: "Here's the CWE assignment report. Would you like to:"
- Display as-is (already shown)
- Write to a file (ask for path)
- Revise anything before finalizing

## Teaching Moment

> **What makes a good CWE justification:** A CNA reviewer should be able to read your justification paragraph and immediately understand: (1) what the vulnerability is, (2) why this specific CWE was chosen over alternatives, and (3) what evidence supports the choice. "This vulnerability is a SQL injection" is too vague. "Unsanitized user input in the `search` parameter is concatenated into a SQL query at line 142 of `api/search.py`, allowing attacker-controlled SQL execution (CWE-89)" is actionable.

## Output

The complete CNA-ready report as described above. This is the final deliverable of the analysis workflow.
