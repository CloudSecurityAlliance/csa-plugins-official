# Quality Framework — 5 Validation Checks

Every CWE assignment should pass these five checks before being considered complete. Run them in order — earlier checks catch the most common problems.

## Check 1: Too Abstract

**What it looks like:** Assigning CWE-20 (Improper Input Validation) when CWE-89 (SQL Injection) is the actual weakness. The assigned CWE is technically correct but so broad that it provides no actionable information.

**How to detect it:** Run `cwe-tool.py children <ID>` — if children exist that match better, you're too abstract. A CWE with dozens of children is almost certainly too broad for a specific vulnerability.

**How to fix it:** Use the most specific child CWE that accurately describes the weakness. Walk down the hierarchy: check children, then check their children, until you reach the most specific CWE that still accurately describes the weakness.

**Real-world example:** Many NVD entries assign CWE-20 to SQL injection vulnerabilities because the root cause involves input validation. But CWE-89 is the specific weakness. CWE-20 describes a broad category, not a specific exploitable condition. Telling a developer "you have improper input validation" is far less useful than "you have SQL injection in the search query handler."

## Check 2: Wrong Abstraction Level

**What it looks like:** Using a Pillar (CWE-284 Improper Access Control) when a Base (CWE-862 Missing Authorization) exists. The assignment is at the wrong level of the CWE hierarchy.

**How to detect it:** Run `cwe-tool.py lookup <ID>` and check the Abstraction field. If it says "Pillar" or "Class", search for more specific alternatives. Pillars should never be assigned directly. Classes should only be used when no Base or Variant fits.

**How to fix it:** Consult abstraction-guide.md. Use Variant if one fits, then Base, then Class. Never use Pillar directly. Document why you chose the abstraction level you did if it's Class or higher.

**Real-world example:** CVE records often use CWE-284 when CWE-862 (Missing Authorization), CWE-863 (Incorrect Authorization), or CWE-287 (Improper Authentication) would be more precise. CWE-284 is a Pillar — it covers the entire domain of access control and is too broad to guide remediation.

## Check 3: Missing Chain Links

**What it looks like:** Jumping from root cause to final impact without intermediate weaknesses. The chain has logical gaps where one weakness doesn't directly enable the next.

**How to detect it:** Review the chain for logical leaps. Does each link directly enable the next? If you need to add "and then somehow..." between two CWEs, there's a missing link.

**How to fix it:** Add intermediate CWEs. If input validation failure leads to code execution, there's usually an injection type in between. The chain should tell a complete causal story: each CWE is either the direct cause or the direct precondition of the next.

**Real-world example:** Mapping a vulnerability as just "CWE-20 -> impact: RCE" misses the injection step (CWE-78, CWE-89, etc.) that makes the input validation failure exploitable. The complete chain might be CWE-20 -> CWE-78 -> CWE-269, where each link has a clear causal connection.

## Check 4: Data Currency

**What it looks like:** Bundled CWE data may not include recently added CWEs. The analysis is limited to what was known at the time of the data export.

**How to detect it:** Check `data/VERSION.txt` for the export date. If older than 6 months, flag it. New CWEs are added regularly, especially for emerging attack categories like AI/ML weaknesses.

**How to fix it:** Note the limitation. Display: "Bundled CWE data is from [date]. Newer CWEs may exist. Consider checking https://cwe.mitre.org/data/index.html for novel attack patterns."

**Note:** This is an honest disclosure, not a claim to have checked for newer CWEs. The plugin cannot know what it doesn't have. Transparency about data limitations is itself a quality signal.

## Check 5: Cause vs. Consequence Confusion

**What it looks like:** Assigning a CWE that describes the consequence (impact) rather than the weakness. The CWE tells you what the attacker achieves, not what is wrong with the software.

**How to detect it:** Verify each CWE describes a flaw in the software, not what the attacker achieves. "Code execution" is a consequence; "command injection" is a weakness. Ask: "Does this CWE describe something the developer did wrong, or something the attacker accomplishes?"

**How to fix it:** The primary CWE should describe what is wrong with the code, not what the attacker can do. Work backward from the impact to find the underlying weakness. The weakness is the fixable software defect; the consequence is what happens if it isn't fixed.

**Real-world example:** Assigning CWE-94 (Code Injection) when the actual weakness is CWE-502 (Deserialization of Untrusted Data). Code execution is what happens; unsafe deserialization is the weakness. Fixing deserialization fixes the vulnerability; "fixing code injection" doesn't tell the developer what to change.
