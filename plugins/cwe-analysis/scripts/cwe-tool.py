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
        related = mitre_row.get("Related Weaknesses", "").strip()
        consequences = mitre_row.get("Common Consequences", "").strip()
        mitigations = mitre_row.get("Potential Mitigations", "").strip()
        observed = mitre_row.get("Observed Examples", "").strip()

        print(f"\nAbstraction : {abstraction or '(none)'}")
        print(f"Status      : {status or '(none)'}")
        print(f"\n-- Description --")
        print(_truncate(description))
        print(f"\n-- Related Weaknesses --")
        print(_truncate(related))
        print(f"\n-- Common Consequences --")
        print(_truncate(consequences))
        print(f"\n-- Potential Mitigations --")
        print(_truncate(mitigations))
        print(f"\n-- Observed Examples --")
        print(_truncate(observed))

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
        print(f"CWE-{cwe_id}: {name}")
        print(f"  Abstraction: {abstraction}")
        print(f"  {desc}\n")


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
        consequences = _truncate(row.get("Common Consequences", ""), 120)
        print(f"CWE-{cwe_id}: {name}")
        print(f"  Abstraction: {abs_val}")
        print(f"  Consequences: {consequences}\n")


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
    """Find all CWEs that are children of the given CWE-ID (via ChildOf relationships)."""
    target_id = _strip_prefix(cwe_id_input)
    mitre_data = load_mitre_csv()

    children = []
    for cwe_id, row in mitre_data.items():
        related = row.get("Related Weaknesses", "")
        if not related:
            continue
        rels = _parse_related_weaknesses(related)
        for nature, rel_cwe_id, _view_id in rels:
            if nature == "ChildOf" and rel_cwe_id == target_id:
                children.append(row)
                break

    if not children:
        parent_row = mitre_data.get(target_id)
        if parent_row:
            print(f"CWE-{target_id}: {parent_row.get('Name', '')} — 0 children found.")
        else:
            print(f"No children found for CWE-{target_id}.")
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
    print(f"CWE-{target_id}: {parent_name} — {len(children)} children\n")
    for row in children:
        cwe_id = row.get("CWE-ID", "")
        name = row.get("Name", "")
        abstraction = row.get("Weakness Abstraction", "")
        print(f"  CWE-{cwe_id}: {name} [{abstraction}]")
    print()


def cmd_chain(cwe_ids, as_json):
    """Analyze a chain of CWEs and show relationships between them."""
    if len(cwe_ids) < 2:
        print("Error: chain requires at least 2 CWE IDs.", file=sys.stderr)
        sys.exit(1)

    ids = [_strip_prefix(c) for c in cwe_ids]
    mitre_data = load_mitre_csv()
    ai_data = load_ai_csv()

    # Load entries
    entries = []
    for cid in ids:
        entry = {"id": cid, "mitre": mitre_data.get(cid), "ai": ai_data.get(cid)}
        entries.append(entry)

    # Find relationships between pairs
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
        for nature, rel_cwe_id, _view_id in rels:
            if rel_cwe_id in id_set and rel_cwe_id != entry["id"]:
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

    print(f"\n-- Relationships Found --")
    if relationships:
        for rel in relationships:
            print(f"  CWE-{rel['from']} --[{rel['nature']}]--> CWE-{rel['to']}")
    else:
        print("  No direct taxonomic relationships found between these CWEs.")

    print(f"\nNote: CWE relationships are taxonomic. Absence of a relationship "
          f"does not mean these CWEs are unrelated in an exploit chain.\n")


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


if __name__ == "__main__":
    main()
