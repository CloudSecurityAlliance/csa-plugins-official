# cwe-tool.py Improvements: Parsed List Output + Similar Subcommand

**Date:** 2026-04-05
**Scope:** Two improvements to `scripts/cwe-tool.py`, plus doc updates to SKILL.md and TODO.md. No changes to skill phases or plugin.json.

## 1. Compact Parsed Output for List Views

### Problem

The `candidates` command displays raw `::KEY:val::` blobs for Common Consequences:
```
Consequences: ::SCOPE:Availability:IMPACT:DoS: Crash, Exit, or Restart:IMPACT:DoS: Resource Consumption (CPU)::
```
This is unreadable for humans and wastes tokens / risks misinterpretation when Claude consumes the output during analysis.

The `search` command shows plain-text Description (which is fine) but lacks Consequences and Related Weaknesses, making it harder to evaluate results without running `lookup` on each one.

### Solution

Add two compact formatter functions alongside the existing multi-line formatters:

- `_compact_consequences(raw)` — Parses `::KEY:val::` blobs into a single line.
  - Output: `"Confidentiality (Read Data), Integrity (Modify Data), Availability (DoS: Crash)"`
  - Format: `"Scope (Impact1, Impact2), Scope2 (Impact3)"`
  - Deduplicates impacts within each scope (the raw data sometimes has duplicates like `DoS, DoS`).
  - Uses `_parse_kv_segments()` (existing, proven parser).

- `_compact_related(raw, mitre_data)` — Parses Related Weaknesses into a single line, view 1000 only.
  - Output: `"ChildOf CWE-943, PeerOf CWE-564"`
  - Format: `"Nature CWE-ID, Nature CWE-ID"` (no names — too long for one line).

### Changes to `cmd_search`

Current output per result:
```
CWE-89: Improper Neutralization of Special Elements used in an SQL Command
  Abstraction: Base
  The product constructs all or part of an SQL command...
```

New output per result:
```
CWE-89: Improper Neutralization of Special Elements used in an SQL Command
  Abstraction: Base
  The product constructs all or part of an SQL command...
  Consequences: Confidentiality (Read Data), Integrity (Modify Data)
  Related: ChildOf CWE-943
```

Description stays (it shows why the result matched). Consequences and Related are added below.

### Changes to `cmd_candidates`

Current output per result:
```
CWE-121: Stack-based Buffer Overflow
  Abstraction: Variant
  Consequences: ::SCOPE:Availability:IMPACT:Modify Memory:IMPACT:DoS: Crash...
```

New output per result:
```
CWE-121: Stack-based Buffer Overflow
  Abstraction: Variant
  Consequences: Availability (Modify Memory, DoS: Crash, DoS: Resource Consumption), Confidentiality (Read Memory)
  Related: ChildOf CWE-788, ChildOf CWE-787
```

Note: CWE-121 has two parents in view 1000. The compact format lists all relationships.

Raw blob replaced with compact parsed version. Related Weaknesses added.

### JSON output

Unchanged for both commands. JSON consumers can parse the raw fields themselves.

## 2. `similar` Subcommand

### Purpose

Find CWEs that could be confused with a given CWE, for disambiguation during Phase 3 (CWE Identification). An analyst choosing between CWE-89 and CWE-564 can run `similar 89` to see the full disambiguation space.

### CLI

```
cwe-tool.py similar <CWE-ID> [--json]
```

### Logic

Given a target CWE, find:

1. **Parents** — CWEs the target is ChildOf in view 1000.
2. **Peers** — CWEs with a PeerOf relationship to the target in view 1000. Bidirectional: checks both the target's PeerOf entries AND other CWEs that list PeerOf the target.
3. **Siblings** — For each parent, find all other CWEs that are ChildOf the same parent in view 1000. Excludes the target itself.

### Human-readable output

```
============================================================
Similar to CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
Abstraction: Base
============================================================

Parents:
  CWE-943: Improper Neutralization of Special Elements in Data Query Logic [Class]

Peers:
  (none in view 1000)

Siblings (children of CWE-943):
  CWE-90: Improper Neutralization of Special Elements used in an LDAP Query [Base]
  CWE-643: Improper Neutralization of Data within XPath Expressions [Base]
  CWE-652: Improper Neutralization of Data within XQuery Expressions [Base]
```

### JSON output

```json
{
  "target": {
    "CWE-ID": "89",
    "Name": "Improper Neutralization of Special Elements used in an SQL Command",
    "Weakness Abstraction": "Base"
  },
  "parents": [
    {"CWE-ID": "943", "Name": "...", "Weakness Abstraction": "Class"}
  ],
  "peers": [],
  "siblings": [
    {"CWE-ID": "90", "Name": "...", "Weakness Abstraction": "Base", "parent": "943"},
    {"CWE-ID": "643", "Name": "...", "Weakness Abstraction": "Base", "parent": "943"},
    {"CWE-ID": "652", "Name": "...", "Weakness Abstraction": "Base", "parent": "943"}
  ]
}
```

### Edge cases

- **No peers, no siblings:** "No similar CWEs found." (CWE has no PeerOf relationships and its parent has no other children.)
- **Multiple parents:** Collect siblings from all parents. Each sibling entry includes which parent it shares.
- **Nonexistent CWE:** Print error to stderr, exit code 1.
- **CWE with only AI data (no MITRE row):** Relationships live in MITRE data, so no peers/siblings can be found. Show the CWE info and "No relationship data available (CWE not in MITRE Research Concepts view)."

## 3. Tests

### New tests in `test_cwe_tool.py`

**Parsed list output (2 tests):**
- `test_search_parsed_output` — Search "injection", verify the new Consequences and Related lines are parsed (no `::SCOPE:` or `::NATURE:` raw blobs), and that readable fields like "Confidentiality" or "Availability" appear.
- `test_candidates_parsed_consequences` — Candidates with `--impact "code execution"`, verify readable consequence text appears (e.g., "Confidentiality" or "Availability"), no `::SCOPE:` raw blobs.

**Similar subcommand (5 tests):**
- `test_similar_known_cwe` — `similar 89`, verify parent CWE-943 appears and at least one sibling (CWE-90, 643, or 652).
- `test_similar_with_peers` — `similar 79`, verify CWE-352 appears in peers (confirmed PeerOf relationship).
- `test_similar_json` — `similar 79 --json`, verify valid JSON with `target`, `parents`, `peers`, `siblings` keys.
- `test_similar_nonexistent` — `similar 999999`, expect exit code 1.
- `test_similar_no_peers` — `similar 89`, verify peers section is empty (CWE-89 has no PeerOf relationships), siblings section is populated.
- `test_similar_pillar_no_results` — `similar 284` (Pillar, no parents, no one peers to it), verify graceful "No similar CWEs found" message.

**New doc truth test in `test_doc_truth.py`:**
- `test_cwe79_similar_includes_352` — Run `similar 79`, verify CWE-352 appears. Guards against data regressions in PeerOf relationships.

**Total: 8 new tests (27 → 35).**

## 4. Documentation Updates

**SKILL.md** — Add `similar` to the "Available subcommands" list in the CWE Data Tool section:
```
- `similar <CWE-ID>` — find PeerOf and sibling CWEs for disambiguation
```

**TODO.md** — Mark the two completed items (parsed fields, similar subcommand) as done. Keep `cve-lookup` as future work.

## 5. Out of Scope

- `cve-lookup` subcommand (requires network — deferred)
- Cross-model validation Phase 7 (separate effort)
- JSON output schema changes for search/candidates
- Changes to skill phases or reference material
