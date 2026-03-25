# Phase 5: Validation

## Purpose

Run the CWE assignment through the quality framework's 5 validation checks. This catches the most common CWE mapping errors before they reach a CVE record.

## Prerequisites

Read `references/quality-framework.md` for the full checklist.

## Process

Run each check. Report pass/flag for each.

### Check 1: Too Abstract?

Run `cwe-tool.py children <CWE-ID>` on each assigned CWE.

- If children exist that better describe the weakness → **FLAG**: recommend using a more specific child CWE
- If no children exist, or none match better → **PASS**

### Check 2: Wrong Abstraction Level?

Run `cwe-tool.py lookup <CWE-ID>` and check the Abstraction field.

- If Abstraction is "Pillar" → **FLAG**: Pillars should never be assigned directly
- If Abstraction is "Class" and a Base or Variant alternative exists → **FLAG**: recommend the more specific alternative
- If Abstraction is "Base" or "Variant" → **PASS**

### Check 3: Missing Chain Links?

Review the chain (if Phase 4 was done) for causal gaps:

- Does each link directly enable the next? → **PASS**
- Is there a logical leap between links? → **FLAG**: identify what intermediate CWE is missing
- If no chain was built (single CWE assignment), check: is there an obvious root cause that should be noted? → Note, but not necessarily a flag

### Check 4: Data Currency

Read `data/VERSION.txt` and check the export date.

- If data is less than 6 months old → **PASS** with note: "CWE data current as of [date]"
- If data is more than 6 months old → **FLAG**: "Bundled CWE data is from [date]. Newer CWEs may exist that are not included. Consider checking https://cwe.mitre.org/data/index.html if the vulnerability involves a novel attack pattern."

This is an honest disclosure of the data's limitations, not a claim to have verified currency.

### Check 5: Cause vs. Consequence?

For each assigned CWE, verify it describes a weakness (flaw in the code), not a consequence (what the attacker achieves):

- CWE describes a flaw → **PASS**
- CWE describes an outcome or impact → **FLAG**: find the CWE that describes what's wrong with the code, not what the attacker can do

## Output

Present a validation report:

| Check | Status | Details |
|-------|--------|---------|
| 1. Too Abstract? | PASS/FLAG | ... |
| 2. Abstraction Level? | PASS/FLAG | ... |
| 3. Chain Completeness? | PASS/FLAG/N/A | ... |
| 4. Data Currency | PASS/NOTE | ... |
| 5. Cause vs. Consequence? | PASS/FLAG | ... |

If all checks pass → proceed to Phase 6.

If any checks are flagged → present the issues and ask: "These validation checks flagged potential issues. Would you like to revise the assignment, or accept it as-is with the flags noted?"
