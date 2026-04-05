# CWE Analysis Plugin — Future Work

## Phase 7: Cross-Model Validation

Add a validation phase (after Phase 6 Report) that submits the CWE assignment to independent AI models (Codex, Gemini) for adversarial review. Same pattern as the incident-analysis plugin's Phase 10.

**What to validate:**
- Is this the most specific CWE that fits?
- Does the CWE description actually match the vulnerability?
- Is the chain causal flow logical?
- Are there CWEs the primary model missed?
- Is the abstraction level correct?

**Implementation:** Adapt incident-analysis `validate-report.sh` pattern. Requires codex CLI and/or gemini CLI installed.

## Enhanced Phase 2: GitHub Code Pattern Search

After tracing the vulnerable code path in Phase 2, optionally search GitHub for similar vulnerable patterns. Uses `gh` CLI (assumes locally authenticated).

**Value:**
- Shows prevalence — the analyst isn't the only one who wrote this vulnerable pattern
- May find other projects with the same unpatched vulnerability
- Validates the CWE assignment by showing the pattern is widely recognized

**Implementation:**
- Extract the vulnerable code pattern (abstract away project-specific names)
- Use `gh search code` or GitHub code search API to find similar patterns
- Present matches with repo names, file paths, and whether they appear patched
- Keep searches targeted — a few specific patterns, not broad sweeps

**Prerequisite:** `gh` CLI authenticated. The plugin should note this requirement and skip gracefully if unavailable.

## SecID Integration

Use [SecID](https://github.com/CloudSecurityAlliance/SecID) identifiers in the plugin output for precise, cross-referenceable identifiers.

**CWE references in reports:**
- Instead of just "CWE-89", output `secid:weakness/mitre.org/cwe#CWE-89`
- Enables machine-readable cross-referencing with CVEs, ATT&CK techniques, controls

**GitHub commit references:**
- New SecID reference type: `secid:reference/github.com/commit` for linking vulnerability-fixing or vulnerability-introducing commits to CWE assignments
- Example: `secid:reference/github.com/commit#742ad9425bdfc8191a89a47065fb056f45a331a7` could link a specific fix commit to the CWE analysis
- Enables searching GitHub for commits by hash: `https://github.com/search?q=<hash>&type=commits`
- Pairs with the code pattern search — when you find a vulnerable pattern, you can also find the commits that fixed it elsewhere

**CVE cross-references:**
- Link CWE assignments to CVE records: `secid:advisory/mitre.org/cve#CVE-2024-XXXXX`
- When the analyst provides a CVE ID, output the SecID alongside it

**SecID MCP server:** The plugin could optionally use the SecID MCP server at `https://secid.cloudsecurityalliance.org/mcp` for resolution and lookup.

## CVE-to-Code Mapping (Research)

There is no comprehensive public database linking CVE IDs to specific vulnerable code. The closest things are:
- **OSV** (Open Source Vulnerabilities) — has affected version ranges, sometimes commit hashes for fixes
- **GitHub Advisory Database** — links advisories to repos
- **NVD** — has CPE entries (product/version) but not code-level references

**Future exploration:**
- Could the plugin build a local index of CVE → fix commit mappings from OSV/GHSA data?
- Could SecID's reference type enable community-contributed CVE-to-commit mappings?
- Would a `cwe-tool.py cve-examples` subcommand that enriches the Observed Examples field with commit links be useful?

This is a research direction, not a near-term feature.

## Worked Examples

Three end-to-end examples showing the plugin workflow:

1. **Classic web vulnerability** — SQL injection, straightforward single CWE assignment (CWE-89), clear code path, high confidence
2. **Ambiguous case** — vulnerability where confidence stays Uncertain, two plausible CWEs, analyst judgment needed to resolve
3. **AI-specific chain** — CWE-1427 (Prompt Injection) → CWE-1426 (Output Validation Failure) → CWE-78 (Command Injection), full chain with AI relevance overlay

Would go in `skills/cwe-analysis/examples/` or a single `references/worked-examples.md`. Valuable for teaching mode and for testing the methodology end-to-end.

## Tool Improvements

- ~~**Parsed structured fields in candidates/search output**~~ — Done. Search and candidates now show compact parsed Consequences and Related Weaknesses instead of raw blobs.
- ~~**`cwe-tool.py similar <CWE-ID>`**~~ — Done. Finds PeerOf and sibling CWEs for disambiguation.
- **`cwe-tool.py cve-lookup <CVE-ID>`** — if OSV or NVD API is available, look up what CWE was assigned to a given CVE (requires network)
