#!/usr/bin/env python3
"""CWE Analysis Tool — query bundled CWE CSV data.

Uses only Python stdlib: csv, argparse, json, os, sys, re.
"""
import argparse
import csv
import json
import os
import sys
import re

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

MITRE_CSV = os.path.join(DATA_DIR, "CWE-Research-Concepts-1000.csv")
AI_CSV = os.path.join(DATA_DIR, "CWE-AI-Classifications.csv")


def load_mitre_csv():
    """Read CWE-Research-Concepts-1000.csv.

    Returns a dict keyed by CWE-ID string (plain number, no 'CWE-' prefix).
    Each value is the full row as a dict.
    """
    data = {}
    with open(MITRE_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cwe_id = row.get("CWE-ID", "").strip()
            if cwe_id:
                data[cwe_id] = dict(row)
    return data


def load_ai_csv():
    """Read CWE-AI-Classifications.csv.

    Returns a dict keyed by CWE_ID string (plain number, no 'CWE-' prefix).
    Each value is the full row as a dict.
    """
    data = {}
    with open(AI_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cwe_id = row.get("CWE_ID", "").strip()
            if cwe_id:
                data[cwe_id] = dict(row)
    return data


def _strip_prefix(cwe_id_input):
    """Strip 'CWE-' prefix if present and return the plain number string."""
    s = cwe_id_input.strip()
    if re.match(r'^CWE-\d+$', s, re.IGNORECASE):
        return s.split("-", 1)[1]
    return s


def _truncate(text, max_len=500):
    """Truncate long text for human-readable display."""
    if not text:
        return "(none)"
    text = text.strip()
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


def _parse_kv_segments(raw):
    """Parse a ``::KEY:val:KEY:val::`` encoded string into a list of dicts.

    Each ``::``-delimited segment is split on ``:`` into consecutive key/value
    pairs.  Returns a list of dicts, one per non-empty segment.
    """
    results = []
    segments = raw.split("::")
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        parts = seg.split(":")
        kv = {}
        i = 0
        while i < len(parts) - 1:
            key = parts[i].strip()
            val = parts[i + 1].strip()
            if key:
                # Some keys repeat (e.g. SCOPE, IMPACT) – collect as list
                if key in kv:
                    existing = kv[key]
                    if isinstance(existing, list):
                        existing.append(val)
                    else:
                        kv[key] = [existing, val]
                else:
                    kv[key] = val
            i += 2
        if kv:
            results.append(kv)
    return results


def _format_related_weaknesses(raw, mitre_data):
    """Format Related Weaknesses, showing only view-1000 entries with resolved names."""
    if not raw or not raw.strip():
        return "(none)"
    segments = _parse_kv_segments(raw)
    taxonomic = {"ChildOf", "ParentOf", "MemberOf", "HasMember", "PeerOf"}
    lines = []
    for kv in segments:
        view_id = kv.get("VIEW ID", "")
        if view_id != "1000":
            continue
        nature = kv.get("NATURE", "")
        cwe_id = kv.get("CWE ID", "")
        if not nature or not cwe_id:
            continue
        # Resolve name from mitre_data
        target_row = mitre_data.get(cwe_id, {})
        name = target_row.get("Name", "(unknown)")
        kind = "taxonomic" if nature in taxonomic else "directional"
        lines.append(f"  {nature} CWE-{cwe_id}: {name} (view 1000, {kind})")
    return "\n".join(lines) if lines else "(none in view 1000)"


def _format_consequences(raw):
    """Format Common Consequences into readable scope/impact lines."""
    if not raw or not raw.strip():
        return "(none)"
    segments = _parse_kv_segments(raw)
    lines = []
    for kv in segments:
        scope = kv.get("SCOPE", "")
        impact = kv.get("IMPACT", "")
        # Normalise to list
        if isinstance(scope, list):
            scope = ", ".join(scope)
        if isinstance(impact, list):
            impact = ", ".join(impact)
        parts = []
        if scope:
            parts.append(f"Scope: {scope}")
        if impact:
            parts.append(f"Impact: {impact}")
        if parts:
            lines.append("  " + " | ".join(parts))
    return "\n".join(lines) if lines else "(none)"


def _format_observed_examples(raw):
    """Format Observed Examples into CVE: description lines."""
    if not raw or not raw.strip():
        return "(none)"
    segments = _parse_kv_segments(raw)
    lines = []
    for kv in segments:
        ref = kv.get("REFERENCE", "")
        desc = kv.get("DESCRIPTION", "")
        if ref:
            lines.append(f"  {ref}: {desc}" if desc else f"  {ref}")
    return "\n".join(lines) if lines else "(none)"


def _format_mitigations(raw):
    """Format Potential Mitigations into [Phase] description lines."""
    if not raw or not raw.strip():
        return "(none)"
    segments = _parse_kv_segments(raw)
    lines = []
    for kv in segments:
        phase = kv.get("PHASE", "")
        if isinstance(phase, list):
            phase = ", ".join(phase)
        desc = kv.get("DESCRIPTION", "")
        effectiveness = kv.get("EFFECTIVENESS", "")
        line = f"  [{phase}] " if phase else "  "
        line += _truncate(desc, 300)
        if effectiveness:
            line += f" (Effectiveness: {effectiveness})"
        lines.append(line)
    return "\n".join(lines) if lines else "(none)"


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


def cmd_lookup(cwe_id_input, as_json):
    """Look up a CWE by ID and display its details."""
    cwe_id = _strip_prefix(cwe_id_input)

    mitre_data = load_mitre_csv()
    ai_data = load_ai_csv()

    mitre_row = mitre_data.get(cwe_id)
    ai_row = ai_data.get(cwe_id)

    if mitre_row is None and ai_row is None:
        print(f"Error: CWE-{cwe_id} not found.", file=sys.stderr)
        sys.exit(1)

    if as_json:
        merged = {}
        if mitre_row:
            merged.update(mitre_row)
        if ai_row:
            # Prefix AI-specific keys to avoid collision, but keep CWE-ID readable
            for k, v in ai_row.items():
                if k == "CWE_ID":
                    merged["CWE-ID"] = v
                elif k not in merged:
                    merged[k] = v
                else:
                    merged[f"ai_{k}"] = v
        print(json.dumps(merged, indent=2))
        return

    # Human-readable output
    name = (mitre_row or ai_row).get("Name", "(unknown)")
    print(f"{'=' * 60}")
    print(f"CWE-{cwe_id}: {name}")
    print(f"{'=' * 60}")

    if mitre_row:
        abstraction = mitre_row.get("Weakness Abstraction", "").strip()
        status = mitre_row.get("Status", "").strip()
        description = mitre_row.get("Description", "").strip()
        ext_description = mitre_row.get("Extended Description", "").strip()
        related = mitre_row.get("Related Weaknesses", "").strip()
        consequences = mitre_row.get("Common Consequences", "").strip()
        mitigations = mitre_row.get("Potential Mitigations", "").strip()
        observed = mitre_row.get("Observed Examples", "").strip()

        print(f"\nAbstraction : {abstraction or '(none)'}")
        print(f"Status      : {status or '(none)'}")
        print(f"\n-- Description --")
        print(_truncate(description))
        if ext_description:
            print(f"\n-- Extended Description --")
            print(_truncate(ext_description))
        print(f"\n-- Related Weaknesses --")
        print(_format_related_weaknesses(related, mitre_data))
        print(f"\n-- Common Consequences --")
        print(_format_consequences(consequences))
        print(f"\n-- Potential Mitigations --")
        print(_format_mitigations(mitigations))
        print(f"\n-- Observed Examples --")
        print(_format_observed_examples(observed))

    if ai_row:
        print(f"\n-- AI Relevance --")
        print(f"Is AI Relevant  : {ai_row.get('Is_AI_Relevant', '').strip()}")
        print(f"AI Category     : {ai_row.get('AI_Category', '').strip()}")
        print(f"Attack Type     : {ai_row.get('Attack_Type', '').strip()}")
        print(f"Attack Surface  : {ai_row.get('Attack_Surface', '').strip()}")
        print(f"View1 Score     : {ai_row.get('View1_Score', '').strip()}")
        print(f"View2 Score     : {ai_row.get('View2_Score', '').strip()}")
        print(f"Max Score       : {ai_row.get('Max_Score', '').strip()}")
        view1_reasoning = ai_row.get("View1_Reasoning", "").strip()
        view2_reasoning = ai_row.get("View2_Reasoning", "").strip()
        if view1_reasoning:
            print(f"\nView1 Reasoning : {_truncate(view1_reasoning, 300)}")
        if view2_reasoning:
            print(f"View2 Reasoning : {_truncate(view2_reasoning, 300)}")
        ai_impact = ai_row.get("AI_Impact", "").strip()
        if ai_impact:
            print(f"\nAI Impact       : {_truncate(ai_impact, 300)}")

    print()


def cmd_search(keywords, as_json):
    """Search CWE entries by keywords (AND logic, case-insensitive)."""
    mitre_data = load_mitre_csv()
    keywords_lower = [kw.lower() for kw in keywords]

    matches = []
    for cwe_id, row in mitre_data.items():
        name = row.get("Name", "")
        desc = row.get("Description", "")
        combined = (name + " " + desc).lower()
        if all(kw in combined for kw in keywords_lower):
            matches.append(row)

    if not matches:
        print(f"No matches found for: {' '.join(keywords)}")
        return

    if as_json:
        out = []
        for row in matches:
            out.append({
                "CWE-ID": row.get("CWE-ID", ""),
                "Name": row.get("Name", ""),
                "Weakness Abstraction": row.get("Weakness Abstraction", ""),
                "Description": row.get("Description", ""),
            })
        print(json.dumps(out, indent=2))
        return

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


_SPECIFICITY_ORDER = {"Variant": 0, "Base": 1, "Class": 2, "Pillar": 3}


def cmd_candidates(impact, abstraction, as_json):
    """Find candidate CWEs filtered by impact and/or abstraction (MITRE only)."""
    mitre_data = load_mitre_csv()

    matches = []
    for cwe_id, row in mitre_data.items():
        if impact:
            consequences = row.get("Common Consequences", "").lower()
            if impact.lower() not in consequences:
                continue
        if abstraction:
            row_abs = row.get("Weakness Abstraction", "").strip()
            if row_abs != abstraction:
                continue
        matches.append(row)

    # Sort by specificity: Variant (0) > Base (1) > Class (2) > Pillar (3)
    matches.sort(key=lambda r: (
        _SPECIFICITY_ORDER.get(r.get("Weakness Abstraction", "").strip(), 4),
        r.get("CWE-ID", ""),
    ))

    if not matches:
        print("No candidates found.")
        return

    if as_json:
        out = []
        for row in matches:
            out.append({
                "CWE-ID": row.get("CWE-ID", ""),
                "Name": row.get("Name", ""),
                "Weakness Abstraction": row.get("Weakness Abstraction", ""),
                "Common Consequences": row.get("Common Consequences", ""),
            })
        print(json.dumps(out, indent=2))
        return

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


def _parse_related_weaknesses(related_str):
    """Parse the Related Weaknesses field into a list of (nature, cwe_id, view_id) tuples."""
    results = []
    # Format: ::NATURE:ChildOf:CWE ID:74:VIEW ID:1000:ORDINAL:Primary::
    segments = related_str.split("::")
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        parts = seg.split(":")
        # Build a key-value map from consecutive pairs
        kv = {}
        i = 0
        while i < len(parts) - 1:
            key = parts[i].strip()
            val = parts[i + 1].strip()
            if key:
                kv[key] = val
            i += 2
        nature = kv.get("NATURE", "")
        cwe_id = kv.get("CWE ID", "")
        view_id = kv.get("VIEW ID", "")
        if nature and cwe_id:
            results.append((nature, cwe_id, view_id))
    return results


def cmd_children(cwe_id_input, as_json):
    """Find all CWEs that are children of the given CWE-ID (via ChildOf relationships in view 1000)."""
    target_id = _strip_prefix(cwe_id_input)
    mitre_data = load_mitre_csv()

    # Validate the target CWE exists
    if target_id not in mitre_data:
        print(f"Error: CWE-{target_id} not found.", file=sys.stderr)
        sys.exit(1)

    children = []
    for cwe_id, row in mitre_data.items():
        related = row.get("Related Weaknesses", "")
        if not related:
            continue
        rels = _parse_related_weaknesses(related)
        for nature, rel_cwe_id, view_id in rels:
            if nature == "ChildOf" and rel_cwe_id == target_id and view_id == "1000":
                children.append(row)
                break

    if not children:
        parent_row = mitre_data.get(target_id)
        print(f"CWE-{target_id}: {parent_row.get('Name', '')} — 0 children found (view 1000).")
        return

    if as_json:
        out = []
        for row in children:
            out.append({
                "CWE-ID": row.get("CWE-ID", ""),
                "Name": row.get("Name", ""),
                "Weakness Abstraction": row.get("Weakness Abstraction", ""),
            })
        print(json.dumps(out, indent=2))
        return

    parent_row = mitre_data.get(target_id)
    parent_name = parent_row.get("Name", "") if parent_row else ""
    print(f"CWE-{target_id}: {parent_name} — {len(children)} children (view 1000)\n")
    for row in children:
        cwe_id = row.get("CWE-ID", "")
        name = row.get("Name", "")
        abstraction = row.get("Weakness Abstraction", "")
        print(f"  CWE-{cwe_id}: {name} [{abstraction}]")
    print()


def cmd_chain(cwe_ids, as_json):
    """Analyze a chain of CWEs and show relationships between them (view 1000 only)."""
    if len(cwe_ids) < 2:
        print("Error: chain requires at least 2 CWE IDs.", file=sys.stderr)
        sys.exit(1)

    ids = [_strip_prefix(c) for c in cwe_ids]
    mitre_data = load_mitre_csv()
    ai_data = load_ai_csv()

    # Validate all IDs exist
    for cid in ids:
        if cid not in mitre_data and cid not in ai_data:
            print(f"Error: CWE-{cid} not found.", file=sys.stderr)
            sys.exit(1)

    # Load entries
    entries = []
    for cid in ids:
        entry = {"id": cid, "mitre": mitre_data.get(cid), "ai": ai_data.get(cid)}
        entries.append(entry)

    # Find relationships between pairs (view 1000 only)
    relationships = []
    id_set = set(ids)
    for entry in entries:
        mitre_row = entry["mitre"]
        if not mitre_row:
            continue
        related = mitre_row.get("Related Weaknesses", "")
        if not related:
            continue
        rels = _parse_related_weaknesses(related)
        for nature, rel_cwe_id, view_id in rels:
            if rel_cwe_id in id_set and rel_cwe_id != entry["id"] and view_id == "1000":
                relationships.append({
                    "from": entry["id"],
                    "to": rel_cwe_id,
                    "nature": nature,
                })

    if as_json:
        out = []
        for entry in entries:
            item = {"CWE-ID": entry["id"]}
            mitre_row = entry["mitre"]
            if mitre_row:
                item["Name"] = mitre_row.get("Name", "")
                item["Weakness Abstraction"] = mitre_row.get("Weakness Abstraction", "")
                item["Description"] = mitre_row.get("Description", "")
            ai_row = entry["ai"]
            if ai_row:
                item["View1_Score"] = ai_row.get("View1_Score", "")
                item["View2_Score"] = ai_row.get("View2_Score", "")
                item["AI_Category"] = ai_row.get("AI_Category", "")
            out.append(item)
        result = {"chain": out, "relationships": relationships}
        print(json.dumps(result, indent=2))
        return

    # Human-readable output
    print(f"{'=' * 60}")
    print(f"CWE Chain Analysis: {' -> '.join('CWE-' + c for c in ids)}")
    print(f"{'=' * 60}")

    for entry in entries:
        cid = entry["id"]
        mitre_row = entry["mitre"]
        ai_row = entry["ai"]
        name = ""
        if mitre_row:
            name = mitre_row.get("Name", "")
        elif ai_row:
            name = ai_row.get("Name", "")
        print(f"\nCWE-{cid}: {name}")
        if mitre_row:
            print(f"  Abstraction: {mitre_row.get('Weakness Abstraction', '')}")
            print(f"  {_truncate(mitre_row.get('Description', ''), 200)}")
        if ai_row:
            v1 = ai_row.get("View1_Score", "").strip()
            v2 = ai_row.get("View2_Score", "").strip()
            cat = ai_row.get("AI_Category", "").strip()
            if v1 or v2:
                print(f"  AI Relevance: View1={v1}, View2={v2}, Category={cat}")

    print(f"\n-- Relationships Found (view 1000) --")
    if relationships:
        taxonomic = {"ChildOf", "ParentOf", "MemberOf", "HasMember", "PeerOf"}
        for rel in relationships:
            nature = rel['nature']
            kind = "taxonomic" if nature in taxonomic else "directional"
            print(f"  CWE-{rel['from']} --[{nature}]--> CWE-{rel['to']}  ({kind})")
    else:
        print("  No direct relationships found between these CWEs in view 1000.")

    print(f"\nNote: Absence of a relationship does not mean these CWEs are "
          f"unrelated in an exploit chain. Taxonomic relationships (ChildOf, PeerOf) "
          f"describe classification. Directional relationships (CanPrecede, CanFollow, "
          f"Requires) describe potential causal flow.\n")


def cmd_version():
    """Print the CWE data version from VERSION.txt."""
    version_file = os.path.join(DATA_DIR, "VERSION.txt")
    if not os.path.isfile(version_file):
        print("Error: VERSION.txt not found.", file=sys.stderr)
        sys.exit(1)
    with open(version_file, encoding="utf-8") as f:
        print(f.read().strip())


def cmd_ai_relevant(min_score, as_json):
    """List AI-relevant CWEs filtered by minimum Max_Score."""
    ai_data = load_ai_csv()

    matches = []
    for cwe_id, row in ai_data.items():
        try:
            max_score = int(row.get("Max_Score", "0").strip())
        except ValueError:
            continue
        if max_score >= min_score:
            matches.append(row)

    # Sort by Max_Score descending, then CWE_ID ascending
    def sort_key(row):
        try:
            ms = int(row.get("Max_Score", "0").strip())
        except ValueError:
            ms = 0
        try:
            cid = int(row.get("CWE_ID", "0").strip())
        except ValueError:
            cid = 0
        return (-ms, cid)

    matches.sort(key=sort_key)

    if not matches:
        print(f"No AI-relevant CWEs found with Max_Score >= {min_score}.")
        return

    if as_json:
        out = []
        for row in matches:
            out.append({
                "CWE_ID": row.get("CWE_ID", ""),
                "Name": row.get("Name", ""),
                "View1_Score": row.get("View1_Score", ""),
                "View2_Score": row.get("View2_Score", ""),
                "Max_Score": row.get("Max_Score", ""),
                "AI_Category": row.get("AI_Category", ""),
                "Attack_Surface": row.get("Attack_Surface", ""),
            })
        print(json.dumps(out, indent=2))
        return

    print(f"{len(matches)} AI-relevant CWEs with Max_Score >= {min_score}\n")
    for row in matches:
        cwe_id = row.get("CWE_ID", "")
        name = row.get("Name", "")
        v1 = row.get("View1_Score", "").strip()
        v2 = row.get("View2_Score", "").strip()
        cat = row.get("AI_Category", "").strip()
        surface = row.get("Attack_Surface", "").strip()
        print(f"CWE-{cwe_id}: {name}")
        print(f"  View1={v1}, View2={v2}, Category={cat}, Surface={surface}\n")


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


def main():
    parser = argparse.ArgumentParser(
        prog="cwe-tool",
        description="Query bundled CWE data.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # lookup subcommand
    lookup_parser = subparsers.add_parser(
        "lookup",
        help="Look up a CWE by ID.",
    )
    lookup_parser.add_argument(
        "cwe_id",
        help="CWE ID (e.g. '79' or 'CWE-79').",
    )
    lookup_parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Output as JSON.",
    )

    # search subcommand
    search_parser = subparsers.add_parser(
        "search",
        help="Search CWE entries by keywords (AND logic).",
    )
    search_parser.add_argument(
        "keywords",
        nargs="+",
        help="Keywords to search for in Name and Description.",
    )
    search_parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Output as JSON.",
    )

    # candidates subcommand
    candidates_parser = subparsers.add_parser(
        "candidates",
        help="Find candidate CWEs by impact and/or abstraction level.",
    )
    candidates_parser.add_argument(
        "--impact",
        default=None,
        help="Filter by Common Consequences (case-insensitive substring).",
    )
    candidates_parser.add_argument(
        "--abstraction",
        default=None,
        help="Filter by Weakness Abstraction (exact match: Variant, Base, Class, Pillar).",
    )
    candidates_parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Output as JSON.",
    )

    # children subcommand
    children_parser = subparsers.add_parser(
        "children",
        help="Find all children of a CWE (entries with ChildOf relationship).",
    )
    children_parser.add_argument(
        "cwe_id",
        help="Parent CWE ID (e.g. '74' or 'CWE-74').",
    )
    children_parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Output as JSON.",
    )

    # chain subcommand
    chain_parser = subparsers.add_parser(
        "chain",
        help="Analyze a chain of CWEs and show relationships.",
    )
    chain_parser.add_argument(
        "cwe_ids",
        nargs="+",
        help="Two or more CWE IDs (e.g. '20 89' or 'CWE-20 CWE-89').",
    )
    chain_parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Output as JSON.",
    )

    # ai-relevant subcommand
    ai_parser = subparsers.add_parser(
        "ai-relevant",
        help="List AI-relevant CWEs by minimum score.",
    )
    ai_parser.add_argument(
        "--min-score",
        type=int,
        default=2,
        help="Minimum Max_Score threshold (default: 2).",
    )
    ai_parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Output as JSON.",
    )

    # version subcommand
    subparsers.add_parser(
        "version",
        help="Print CWE data version information.",
    )

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

    args = parser.parse_args()

    if args.command == "lookup":
        cmd_lookup(args.cwe_id, args.as_json)
    elif args.command == "search":
        cmd_search(args.keywords, args.as_json)
    elif args.command == "candidates":
        cmd_candidates(args.impact, args.abstraction, args.as_json)
    elif args.command == "children":
        cmd_children(args.cwe_id, args.as_json)
    elif args.command == "chain":
        cmd_chain(args.cwe_ids, args.as_json)
    elif args.command == "ai-relevant":
        cmd_ai_relevant(args.min_score, args.as_json)
    elif args.command == "version":
        cmd_version()
    elif args.command == "similar":
        cmd_similar(args.cwe_id, args.as_json)


if __name__ == "__main__":
    main()
