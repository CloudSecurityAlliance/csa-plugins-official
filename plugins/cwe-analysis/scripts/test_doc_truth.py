"""Regression tests verifying reference doc claims match bundled data.

These tests catch factual drift between documentation and CSV data.
Run from the scripts/ directory.
"""
import csv
import os
import re
import sys
import subprocess

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
REFS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills", "cwe-analysis", "references")
TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cwe-tool.py")

MITRE_CSV = os.path.join(DATA_DIR, "CWE-Research-Concepts-1000.csv")
AI_CSV = os.path.join(DATA_DIR, "CWE-AI-Classifications.csv")


def run(args, expect_rc=0):
    """Run cwe-tool.py with given arguments and return stdout."""
    result = subprocess.run(
        [sys.executable, TOOL] + args,
        capture_output=True, text=True
    )
    assert result.returncode == expect_rc, f"Exit {result.returncode}: {result.stderr}\nStdout: {result.stdout}"
    return result.stdout


def load_mitre():
    data = {}
    with open(MITRE_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[row["CWE-ID"].strip()] = row
    return data


def load_ai():
    data = {}
    with open(AI_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[row["CWE_ID"].strip()] = row
    return data


def parse_related(raw):
    """Parse Related Weaknesses into (nature, cwe_id, view_id) tuples."""
    results = []
    for seg in raw.split("::"):
        seg = seg.strip()
        if not seg:
            continue
        parts = seg.split(":")
        kv = {}
        i = 0
        while i < len(parts) - 1:
            k, v = parts[i].strip(), parts[i+1].strip()
            if k:
                kv[k] = v
            i += 2
        if kv.get("NATURE") and kv.get("CWE ID"):
            results.append((kv["NATURE"], kv["CWE ID"], kv.get("VIEW ID", "")))
    return results


# --- Score-4 CWE verification ---

def test_score4_cwe_list():
    """The 8 score-4 CWEs listed in ai-relevance-guide.md must all have Max_Score=4 in the CSV."""
    ai = load_ai()
    # These are the CWEs listed in ai-relevance-guide.md as score-4
    expected_score4 = ["1427", "1039", "502", "1434", "77", "78", "918", "1426"]
    for cwe_id in expected_score4:
        row = ai.get(cwe_id)
        assert row is not None, f"CWE-{cwe_id} listed as score-4 but not in AI CSV"
        score = row.get("Max_Score", "").strip()
        assert score == "4", f"CWE-{cwe_id} listed as score-4 but has Max_Score={score}"


# --- CWE name verification ---

def test_cwe_1434_name():
    """CWE-1434 name in ai-relevance-guide.md must match the CSV."""
    ai = load_ai()
    mitre = load_mitre()
    expected = "Insecure Setting of Generative AI/ML Model Inference Parameters"
    # Check both CSVs
    for source, data in [("AI", ai), ("MITRE", mitre)]:
        row = data.get("1434")
        if row:
            name = row.get("Name", "").strip()
            assert name == expected, f"CWE-1434 name mismatch in {source}: got '{name}'"


# --- Hierarchy verification (view 1000) ---

def test_cwe89_parent_is_943():
    """CWE-89 must be ChildOf CWE-943 in view 1000 (not CWE-74)."""
    mitre = load_mitre()
    row = mitre["89"]
    rels = parse_related(row["Related Weaknesses"])
    view1000_parents = [cid for nature, cid, vid in rels if nature == "ChildOf" and vid == "1000"]
    assert "943" in view1000_parents, f"CWE-89 view-1000 parents: {view1000_parents}"
    assert "74" not in view1000_parents, "CWE-89 should NOT be ChildOf CWE-74 in view 1000"


def test_cwe79_peerof_352():
    """CWE-79 is PeerOf CWE-352 in view 1000 (not CanPrecede)."""
    mitre = load_mitre()
    row = mitre["79"]
    rels = parse_related(row["Related Weaknesses"])
    rels_to_352 = [(nature, vid) for nature, cid, vid in rels if cid == "352"]
    # Should find PeerOf in view 1000
    natures = [n for n, v in rels_to_352 if v == "1000"]
    assert "PeerOf" in natures, f"CWE-79 to CWE-352 relationships in view 1000: {natures}"
    assert "CanPrecede" not in natures, "CWE-79 should NOT CanPrecede CWE-352 in view 1000"


def test_cwe79_childof_74_view1000():
    """CWE-79 is ChildOf CWE-74 in view 1000."""
    mitre = load_mitre()
    row = mitre["79"]
    rels = parse_related(row["Related Weaknesses"])
    view1000_parents = [cid for nature, cid, vid in rels if nature == "ChildOf" and vid == "1000"]
    assert "74" in view1000_parents, f"CWE-79 view-1000 parents: {view1000_parents}"


# --- similar command regression test ---

def test_cwe79_similar_includes_352():
    """CWE-79 PeerOf CWE-352 should be discoverable via the similar command."""
    out = run(["similar", "79"])
    assert "CWE-352" in out, "CWE-352 should appear as peer of CWE-79"


if __name__ == "__main__":
    tests = [
        test_score4_cwe_list,
        test_cwe_1434_name,
        test_cwe89_parent_is_943,
        test_cwe79_peerof_352,
        test_cwe79_childof_74_view1000,
        test_cwe79_similar_includes_352,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS: {t.__name__}")
        except Exception as e:
            print(f"  FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} doc truth tests passed")
    if failed:
        sys.exit(1)
