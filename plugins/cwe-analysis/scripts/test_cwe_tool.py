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

if __name__ == "__main__":
    test_lookup_known_cwe()
    print("  PASS: test_lookup_known_cwe")
    test_lookup_known_cwe_json()
    print("  PASS: test_lookup_known_cwe_json")
    test_lookup_nonexistent()
    print("  PASS: test_lookup_nonexistent")
    print("All lookup tests passed")
