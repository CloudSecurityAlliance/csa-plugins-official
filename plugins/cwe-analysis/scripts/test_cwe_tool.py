"""Tests for cwe-tool.py — run from the scripts/ directory."""
import subprocess
import json
import sys
import os

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cwe-tool.py")

def run(args, expect_rc=0):
    result = subprocess.run(
        [sys.executable, TOOL] + args,
        capture_output=True, text=True
    )
    assert result.returncode == expect_rc, f"Exit {result.returncode}: {result.stderr}\nStdout: {result.stdout}"
    return result.stdout

def test_lookup_known_cwe():
    out = run(["lookup", "79"])
    assert "CWE-79" in out
    assert "Cross-site Scripting" in out or "Web Page Generation" in out

def test_lookup_known_cwe_json():
    out = run(["lookup", "79", "--json"])
    data = json.loads(out)
    assert str(data.get("CWE-ID", "")) == "79" or str(data.get("cwe_id", "")) == "79"

def test_lookup_nonexistent():
    run(["lookup", "999999"], expect_rc=1)

# --- search tests ---

def test_search_injection():
    out = run(["search", "injection"])
    assert "CWE-" in out
    assert out.count("CWE-") > 5

def test_search_multiple_keywords():
    out = run(["search", "sql", "injection"])
    assert "CWE-89" in out

def test_search_no_results():
    out = run(["search", "xyznonexistentkeywordxyz"])
    assert "No matches" in out or "0 matches" in out

# --- candidates tests ---

def test_candidates_by_impact():
    out = run(["candidates", "--impact", "code execution"])
    assert "CWE-" in out

def test_candidates_by_abstraction():
    out = run(["candidates", "--abstraction", "Variant"])
    assert "CWE-" in out
    assert "Variant" in out

def test_candidates_sorted_by_specificity():
    out = run(["candidates", "--impact", "injection", "--json"])
    data = json.loads(out)
    if len(data) > 1:
        abstractions = [e.get("Weakness Abstraction", "") for e in data]
        specificity = {"Variant": 0, "Base": 1, "Class": 2, "Pillar": 3}
        scores = [specificity.get(a, 4) for a in abstractions]
        assert scores == sorted(scores)

if __name__ == "__main__":
    tests = [
        test_lookup_known_cwe,
        test_lookup_known_cwe_json,
        test_lookup_nonexistent,
        test_search_injection,
        test_search_multiple_keywords,
        test_search_no_results,
        test_candidates_by_impact,
        test_candidates_by_abstraction,
        test_candidates_sorted_by_specificity,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS: {t.__name__}")
        except Exception as e:
            print(f"  FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    if failed:
        sys.exit(1)
