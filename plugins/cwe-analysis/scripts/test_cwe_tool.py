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

# --- children tests ---

def test_children_of_injection():
    """CWE-74 children in view 1000 include CWE-77, CWE-79 but NOT CWE-89 (which is under CWE-943)."""
    out = run(["children", "74"])
    assert "CWE-77" in out or "CWE-79" in out
    # CWE-89 is a child of CWE-943 in view 1000, not CWE-74
    assert "CWE-89" not in out

def test_children_of_leaf():
    out = run(["children", "5"])
    assert "0 children" in out

def test_children_nonexistent():
    """Children of a nonexistent CWE should error, not silently return empty."""
    run(["children", "999999"], expect_rc=1)

# --- chain tests ---

def test_chain_two_cwes():
    out = run(["chain", "20", "89"])
    assert "CWE-20" in out
    assert "CWE-89" in out

def test_chain_three_cwes():
    out = run(["chain", "502", "94", "78"])
    assert "CWE-502" in out
    assert "CWE-94" in out
    assert "CWE-78" in out

def test_chain_single_cwe_error():
    run(["chain", "79"], expect_rc=1)

def test_chain_nonexistent_cwe():
    """Chain with a nonexistent CWE should error, not show blank entry."""
    run(["chain", "79", "999999"], expect_rc=1)

# --- ai-relevant tests ---

def test_ai_relevant_default():
    out = run(["ai-relevant"])
    assert "CWE-" in out

def test_ai_relevant_high_score():
    out = run(["ai-relevant", "--min-score", "4"])
    assert "CWE-1427" in out or "CWE-77" in out

def test_ai_relevant_json():
    out = run(["ai-relevant", "--min-score", "4", "--json"])
    data = json.loads(out)
    ids = [str(e.get("CWE_ID", "")) for e in data]
    assert "1427" in ids
    assert "77" in ids or "78" in ids
    assert len(data) >= 4

# --- lookup parsed output tests ---

def test_lookup_parsed_related():
    """Lookup should show parsed relationships, not raw :: blobs."""
    out = run(["lookup", "89"])
    # Should show parsed ChildOf with CWE name, not raw ::NATURE:ChildOf:...
    assert "ChildOf" in out
    assert "CWE-943" in out
    assert "::NATURE:" not in out  # raw format should not appear

def test_lookup_parsed_consequences():
    """Lookup should show parsed consequences, not raw :: blobs."""
    out = run(["lookup", "79"])
    # Should show parsed scope/impact, not raw ::SCOPE:...
    assert "Confidentiality" in out or "Integrity" in out or "Availability" in out

def test_version():
    out = run(["version"])
    assert "CWE Version" in out
    assert "Export Date" in out

def test_candidates_parsed_consequences():
    """Candidates output should show parsed consequences, not raw :: blobs."""
    out = run(["candidates", "--impact", "code execution"])
    assert "::SCOPE:" not in out, "Raw blob found in candidates output"
    assert "Confidentiality" in out or "Integrity" in out or "Availability" in out

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
        test_children_of_injection,
        test_children_of_leaf,
        test_children_nonexistent,
        test_chain_two_cwes,
        test_chain_three_cwes,
        test_chain_single_cwe_error,
        test_chain_nonexistent_cwe,
        test_ai_relevant_default,
        test_ai_relevant_high_score,
        test_ai_relevant_json,
        test_lookup_parsed_related,
        test_lookup_parsed_consequences,
        test_version,
        test_candidates_parsed_consequences,
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
