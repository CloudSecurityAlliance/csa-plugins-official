# cwe-tool.py Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add compact parsed output to search/candidates list views and a new `similar` subcommand to cwe-tool.py.

**Architecture:** Two compact formatter functions (`_compact_consequences`, `_compact_related`) replace raw blob display in list commands. A new `cmd_similar` function queries PeerOf + sibling relationships for disambiguation. All changes are in one file (`cwe-tool.py`) plus tests and doc updates.

**Tech Stack:** Python 3 stdlib only (csv, argparse, json, os, sys, re). No external dependencies.

**Spec:** `plugins/cwe-analysis/docs/2026-04-05-cwe-tool-improvements-design.md`

---

### Task 1: Compact consequences formatter — test and implement

**Files:**
- Modify: `plugins/cwe-analysis/scripts/cwe-tool.py` (insert after `_format_mitigations` at line ~181)
- Modify: `plugins/cwe-analysis/scripts/test_cwe_tool.py` (append test)

- [ ] **Step 1: Write the failing test for candidates parsed output**

Append to `test_cwe_tool.py`, before the `if __name__` block:

```python
def test_candidates_parsed_consequences():
    """Candidates output should show parsed consequences, not raw :: blobs."""
    out = run(["candidates", "--impact", "code execution"])
    assert "::SCOPE:" not in out, "Raw blob found in candidates output"
    assert "Confidentiality" in out or "Integrity" in out or "Availability" in out
```

Add `test_candidates_parsed_consequences` to the `tests` list inside `if __name__ == "__main__"`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 plugins/cwe-analysis/scripts/test_cwe_tool.py`
Expected: `test_candidates_parsed_consequences` FAILS because candidates still outputs raw `::SCOPE:` blobs.

- [ ] **Step 3: Implement `_compact_consequences`**

Add to `cwe-tool.py` after the `_format_mitigations` function (after line 181):

```python
def _compact_consequences(raw):
    """Format Common Consequences as a single compact line.

    Groups impacts by scope, deduplicates, returns e.g.:
    "Confidentiality (Read Data), Availability (DoS: Crash, DoS: Resource Consumption)"
    """
    if not raw or not raw.strip():
        return "(none)"
    segments = _parse_kv_segments(raw)
    # Group impacts by scope, dedup
    scope_impacts = {}
    for kv in segments:
        scope = kv.get("SCOPE", "")
        impact = kv.get("IMPACT", "")
        if isinstance(scope, list):
            scopes = scope
        else:
            scopes = [scope] if scope else []
        if isinstance(impact, list):
            impacts = impact
        else:
            impacts = [impact] if impact else []
        for s in scopes:
            s = s.strip()
            if not s:
                continue
            if s not in scope_impacts:
                scope_impacts[s] = []
            for imp in impacts:
                imp = imp.strip()
                if imp and imp not in scope_impacts[s]:
                    scope_impacts[s].append(imp)
    if not scope_impacts:
        return "(none)"
    parts = []
    for scope, impacts in scope_impacts.items():
        if impacts:
            parts.append(f"{scope} ({', '.join(impacts)})")
        else:
            parts.append(scope)
    return ", ".join(parts)
```

- [ ] **Step 4: Wire `_compact_consequences` into `cmd_candidates`**

Replace the human-readable output section of `cmd_candidates` (lines 349-357):

```python
    print(f"{len(matches)} candidates found\n")
    for row in matches:
        cwe_id = row.get("CWE-ID", "")
        name = row.get("Name", "")
        abs_val = row.get("Weakness Abstraction", "")
        consequences = _compact_consequences(row.get("Common Consequences", ""))
        print(f"CWE-{cwe_id}: {name}")
        print(f"  Abstraction: {abs_val}")
        print(f"  Consequences: {consequences}\n")
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python3 plugins/cwe-analysis/scripts/test_cwe_tool.py`
Expected: ALL tests pass including `test_candidates_parsed_consequences`.

- [ ] **Step 6: Commit**

```bash
git add plugins/cwe-analysis/scripts/cwe-tool.py plugins/cwe-analysis/scripts/test_cwe_tool.py
git commit -m "feat(cwe-analysis): add compact consequences parser, wire into candidates"
```

---

### Task 2: Compact related weaknesses formatter — test and implement

**Files:**
- Modify: `plugins/cwe-analysis/scripts/cwe-tool.py` (insert after `_compact_consequences`)
- Modify: `plugins/cwe-analysis/scripts/test_cwe_tool.py` (append test)

- [ ] **Step 1: Write the failing test for search parsed output**

Append to `test_cwe_tool.py`, before the `if __name__` block:

```python
def test_search_parsed_output():
    """Search output should include parsed Consequences and Related, no raw blobs."""
    out = run(["search", "injection"])
    # After adding Consequences/Related to search, verify they're parsed
    assert "::SCOPE:" not in out, "Raw consequence blob found in search output"
    assert "::NATURE:" not in out, "Raw related blob found in search output"
    assert "Consequences:" in out
    assert "Related:" in out
```

Add `test_search_parsed_output` to the `tests` list inside `if __name__ == "__main__"`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 plugins/cwe-analysis/scripts/test_cwe_tool.py`
Expected: `test_search_parsed_output` FAILS because search doesn't output Consequences or Related lines yet.

- [ ] **Step 3: Implement `_compact_related`**

Add to `cwe-tool.py` after `_compact_consequences`:

```python
def _compact_related(raw, mitre_data):
    """Format Related Weaknesses as a single compact line (view 1000 only).

    Returns e.g.: "ChildOf CWE-943, PeerOf CWE-564"
    """
    if not raw or not raw.strip():
        return "(none)"
    segments = _parse_kv_segments(raw)
    parts = []
    for kv in segments:
        view_id = kv.get("VIEW ID", "")
        if view_id != "1000":
            continue
        nature = kv.get("NATURE", "")
        cwe_id = kv.get("CWE ID", "")
        if nature and cwe_id:
            parts.append(f"{nature} CWE-{cwe_id}")
    return ", ".join(parts) if parts else "(none in view 1000)"
```

- [ ] **Step 4: Wire compact formatters into `cmd_search` and `cmd_candidates`**

Update `cmd_search` human-readable output (lines 297-305) to add Consequences and Related:

```python
    print(f"{len(matches)} matches for: {' '.join(keywords)}\n")
    for row in matches:
        cwe_id = row.get("CWE-ID", "")
        name = row.get("Name", "")
        abstraction = row.get("Weakness Abstraction", "")
        desc = _truncate(row.get("Description", ""), 120)
        consequences = _compact_consequences(row.get("Common Consequences", ""))
        related = _compact_related(row.get("Related Weaknesses", ""), mitre_data)
        print(f"CWE-{cwe_id}: {name}")
        print(f"  Abstraction: {abstraction}")
        print(f"  {desc}")
        print(f"  Consequences: {consequences}")
        print(f"  Related: {related}\n")
```

Update `cmd_candidates` human-readable output to also add Related (the Consequences was wired in Task 1):

```python
    print(f"{len(matches)} candidates found\n")
    for row in matches:
        cwe_id = row.get("CWE-ID", "")
        name = row.get("Name", "")
        abs_val = row.get("Weakness Abstraction", "")
        consequences = _compact_consequences(row.get("Common Consequences", ""))
        related = _compact_related(row.get("Related Weaknesses", ""), mitre_data)
        print(f"CWE-{cwe_id}: {name}")
        print(f"  Abstraction: {abs_val}")
        print(f"  Consequences: {consequences}")
        print(f"  Related: {related}\n")
```

- [ ] **Step 5: Run all tests to verify everything passes**

Run: `python3 plugins/cwe-analysis/scripts/test_cwe_tool.py`
Expected: ALL tests pass including `test_search_parsed_output` and `test_candidates_parsed_consequences`.

- [ ] **Step 6: Commit**

```bash
git add plugins/cwe-analysis/scripts/cwe-tool.py plugins/cwe-analysis/scripts/test_cwe_tool.py
git commit -m "feat(cwe-analysis): add compact related parser, wire into search and candidates"
```

---

### Task 3: `similar` subcommand — test and implement

**Files:**
- Modify: `plugins/cwe-analysis/scripts/cwe-tool.py` (add `cmd_similar` after `cmd_ai_relevant`, add argparse subcommand, add dispatch)
- Modify: `plugins/cwe-analysis/scripts/test_cwe_tool.py` (append 6 tests)

- [ ] **Step 1: Write the failing tests for `similar`**

Append to `test_cwe_tool.py`, before the `if __name__` block:

```python
def test_similar_known_cwe():
    """similar 89 should show parent CWE-943 and siblings."""
    out = run(["similar", "89"])
    assert "CWE-943" in out
    # At least one sibling (CWE-90, 643, or 652)
    assert "CWE-90" in out or "CWE-643" in out or "CWE-652" in out

def test_similar_with_peers():
    """similar 79 should show CWE-352 as a peer."""
    out = run(["similar", "79"])
    assert "CWE-352" in out

def test_similar_json():
    """similar 79 --json should return valid JSON with expected keys."""
    out = run(["similar", "79", "--json"])
    data = json.loads(out)
    assert "target" in data
    assert "parents" in data
    assert "peers" in data
    assert "siblings" in data
    # CWE-352 should be in peers
    peer_ids = [str(p.get("CWE-ID", "")) for p in data["peers"]]
    assert "352" in peer_ids

def test_similar_nonexistent():
    """similar with nonexistent CWE should error."""
    run(["similar", "999999"], expect_rc=1)

def test_similar_no_peers():
    """similar 89 should have empty peers but populated siblings."""
    out = run(["similar", "89"])
    assert "(none" in out.split("Siblings")[0]  # "none" appears in Peers section before Siblings
    assert "CWE-90" in out  # sibling exists

def test_similar_pillar_no_results():
    """similar on a Pillar CWE with no peers should report no similar CWEs."""
    out = run(["similar", "284"])
    assert "No similar" in out or "no similar" in out
```

Add all six tests to the `tests` list inside `if __name__ == "__main__"`.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 plugins/cwe-analysis/scripts/test_cwe_tool.py`
Expected: All 6 new `test_similar_*` tests FAIL because the `similar` subcommand doesn't exist yet.

- [ ] **Step 3: Implement `cmd_similar`**

Add to `cwe-tool.py` after the `cmd_ai_relevant` function (after line ~601):

```python
def cmd_similar(cwe_id_input, as_json):
    """Find similar CWEs for disambiguation: PeerOf relationships + siblings (same parent)."""
    target_id = _strip_prefix(cwe_id_input)
    mitre_data = load_mitre_csv()

    if target_id not in mitre_data:
        print(f"Error: CWE-{target_id} not found.", file=sys.stderr)
        sys.exit(1)

    target_row = mitre_data[target_id]
    target_related = target_row.get("Related Weaknesses", "")
    target_rels = _parse_related_weaknesses(target_related)

    # 1. Find parents (ChildOf in view 1000)
    parents = []
    for nature, rel_id, view_id in target_rels:
        if nature == "ChildOf" and view_id == "1000":
            parent_row = mitre_data.get(rel_id)
            if parent_row:
                parents.append(parent_row)

    # 2. Find peers (PeerOf in view 1000, bidirectional)
    peer_ids = set()
    # Forward: target lists PeerOf X
    for nature, rel_id, view_id in target_rels:
        if nature == "PeerOf" and view_id == "1000":
            peer_ids.add(rel_id)
    # Reverse: X lists PeerOf target
    for cwe_id, row in mitre_data.items():
        if cwe_id == target_id:
            continue
        related = row.get("Related Weaknesses", "")
        if not related:
            continue
        rels = _parse_related_weaknesses(related)
        for nature, rel_id, view_id in rels:
            if nature == "PeerOf" and rel_id == target_id and view_id == "1000":
                peer_ids.add(cwe_id)
    peers = [mitre_data[pid] for pid in sorted(peer_ids) if pid in mitre_data]

    # 3. Find siblings (other children of same parents in view 1000)
    parent_ids = set()
    for nature, rel_id, view_id in target_rels:
        if nature == "ChildOf" and view_id == "1000":
            parent_ids.add(rel_id)
    siblings = []
    if parent_ids:
        for cwe_id, row in mitre_data.items():
            if cwe_id == target_id:
                continue
            related = row.get("Related Weaknesses", "")
            if not related:
                continue
            rels = _parse_related_weaknesses(related)
            for nature, rel_id, view_id in rels:
                if nature == "ChildOf" and view_id == "1000" and rel_id in parent_ids:
                    siblings.append({"row": row, "parent": rel_id})
                    break

    if as_json:
        result = {
            "target": {
                "CWE-ID": target_id,
                "Name": target_row.get("Name", ""),
                "Weakness Abstraction": target_row.get("Weakness Abstraction", ""),
            },
            "parents": [
                {
                    "CWE-ID": r.get("CWE-ID", ""),
                    "Name": r.get("Name", ""),
                    "Weakness Abstraction": r.get("Weakness Abstraction", ""),
                }
                for r in parents
            ],
            "peers": [
                {
                    "CWE-ID": r.get("CWE-ID", ""),
                    "Name": r.get("Name", ""),
                    "Weakness Abstraction": r.get("Weakness Abstraction", ""),
                }
                for r in peers
            ],
            "siblings": [
                {
                    "CWE-ID": s["row"].get("CWE-ID", ""),
                    "Name": s["row"].get("Name", ""),
                    "Weakness Abstraction": s["row"].get("Weakness Abstraction", ""),
                    "parent": s["parent"],
                }
                for s in siblings
            ],
        }
        print(json.dumps(result, indent=2))
        return

    # Human-readable output
    name = target_row.get("Name", "")
    abstraction = target_row.get("Weakness Abstraction", "")
    print(f"{'=' * 60}")
    print(f"Similar to CWE-{target_id}: {name}")
    print(f"Abstraction: {abstraction}")
    print(f"{'=' * 60}")

    if not parents and not peers and not siblings:
        print("\nNo similar CWEs found. This CWE has no PeerOf relationships")
        print("and no siblings in view 1000.")
        print()
        return

    print(f"\nParents:")
    if parents:
        for r in parents:
            pid = r.get("CWE-ID", "")
            pname = r.get("Name", "")
            pabs = r.get("Weakness Abstraction", "")
            print(f"  CWE-{pid}: {pname} [{pabs}]")
    else:
        print("  (none — this is a top-level CWE)")

    print(f"\nPeers:")
    if peers:
        for r in peers:
            pid = r.get("CWE-ID", "")
            pname = r.get("Name", "")
            pabs = r.get("Weakness Abstraction", "")
            print(f"  CWE-{pid}: {pname} [{pabs}]")
    else:
        print("  (none in view 1000)")

    print(f"\nSiblings:")
    if siblings:
        # Group by parent for display
        by_parent = {}
        for s in siblings:
            pid = s["parent"]
            if pid not in by_parent:
                by_parent[pid] = []
            by_parent[pid].append(s["row"])
        for pid, rows in by_parent.items():
            parent_row = mitre_data.get(pid, {})
            parent_name = parent_row.get("Name", "")
            print(f"  (children of CWE-{pid}: {parent_name})")
            for r in rows:
                sid = r.get("CWE-ID", "")
                sname = r.get("Name", "")
                sabs = r.get("Weakness Abstraction", "")
                print(f"    CWE-{sid}: {sname} [{sabs}]")
    else:
        print("  (none in view 1000)")

    print()
```

- [ ] **Step 4: Add argparse subcommand and dispatch**

Add the `similar` subparser in `main()`, after the `ai-relevant` subparser block (after line ~715):

```python
    # similar subcommand
    similar_parser = subparsers.add_parser(
        "similar",
        help="Find PeerOf and sibling CWEs for disambiguation.",
    )
    similar_parser.add_argument(
        "cwe_id",
        help="CWE ID (e.g. '79' or 'CWE-79').",
    )
    similar_parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Output as JSON.",
    )
```

Add the dispatch case in the `if/elif` chain at the end of `main()`, after the `version` case:

```python
    elif args.command == "similar":
        cmd_similar(args.cwe_id, args.as_json)
```

- [ ] **Step 5: Run all tests to verify everything passes**

Run: `python3 plugins/cwe-analysis/scripts/test_cwe_tool.py`
Expected: ALL tests pass (22 original + 2 from Tasks 1-2 + 6 new = 30 total, no failures).

Also run doc truth tests to make sure nothing broke:
Run: `python3 plugins/cwe-analysis/scripts/test_doc_truth.py`
Expected: ALL 5 doc truth tests pass.

- [ ] **Step 6: Commit**

```bash
git add plugins/cwe-analysis/scripts/cwe-tool.py plugins/cwe-analysis/scripts/test_cwe_tool.py
git commit -m "feat(cwe-analysis): add similar subcommand for CWE disambiguation"
```

---

### Task 4: Doc truth test for similar + PeerOf regression guard

**Files:**
- Modify: `plugins/cwe-analysis/scripts/test_doc_truth.py` (append test)

- [ ] **Step 1: Write the doc truth test**

Append to `test_doc_truth.py`, before the `if __name__` block:

```python
def test_cwe79_similar_includes_352():
    """CWE-79 PeerOf CWE-352 should be discoverable via the similar command."""
    out = run(["similar", "79"])
    assert "CWE-352" in out, "CWE-352 should appear as peer of CWE-79"
```

Add `test_cwe79_similar_includes_352` to the `tests` list inside `if __name__ == "__main__"`.

- [ ] **Step 2: Run doc truth tests**

Run: `python3 plugins/cwe-analysis/scripts/test_doc_truth.py`
Expected: ALL 6 tests pass (5 existing + 1 new).

- [ ] **Step 3: Commit**

```bash
git add plugins/cwe-analysis/scripts/test_doc_truth.py
git commit -m "test(cwe-analysis): add doc truth test for PeerOf regression guard"
```

---

### Task 5: Documentation updates

**Files:**
- Modify: `plugins/cwe-analysis/skills/cwe-analysis/SKILL.md` (line ~42, add similar to subcommand list)
- Modify: `plugins/cwe-analysis/TODO.md` (mark completed items)

- [ ] **Step 1: Update SKILL.md**

In `skills/cwe-analysis/SKILL.md`, add `similar` to the "Available subcommands" list after the `ai-relevant` entry (after line 42):

```
- `similar <CWE-ID>` — find PeerOf and sibling CWEs for disambiguation
```

- [ ] **Step 2: Update TODO.md**

In `TODO.md`, under the "Tool Improvements" section, mark the two completed items. Change:

```markdown
## Tool Improvements

- **Parsed structured fields in candidates/search output** — same treatment as lookup (currently only lookup parses the raw blobs)
- **`cwe-tool.py cve-lookup <CVE-ID>`** — if OSV or NVD API is available, look up what CWE was assigned to a given CVE (requires network)
- **`cwe-tool.py similar <CWE-ID>`** — find CWEs that are PeerOf or otherwise closely related, useful for disambiguation
```

To:

```markdown
## Tool Improvements

- ~~**Parsed structured fields in candidates/search output**~~ — Done. Search and candidates now show compact parsed Consequences and Related Weaknesses instead of raw blobs.
- ~~**`cwe-tool.py similar <CWE-ID>`**~~ — Done. Finds PeerOf and sibling CWEs for disambiguation.
- **`cwe-tool.py cve-lookup <CVE-ID>`** — if OSV or NVD API is available, look up what CWE was assigned to a given CVE (requires network)
```

- [ ] **Step 3: Run all tests one final time**

Run: `python3 plugins/cwe-analysis/scripts/test_cwe_tool.py && python3 plugins/cwe-analysis/scripts/test_doc_truth.py`
Expected: ALL 36 tests pass (30 tool tests + 6 doc truth tests).

- [ ] **Step 4: Commit**

```bash
git add plugins/cwe-analysis/skills/cwe-analysis/SKILL.md plugins/cwe-analysis/TODO.md
git commit -m "docs(cwe-analysis): update SKILL.md and TODO.md for new tool features"
```

- [ ] **Step 5: Push**

```bash
git push
```
