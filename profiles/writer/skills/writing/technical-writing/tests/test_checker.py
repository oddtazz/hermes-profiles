#!/usr/bin/env python3
"""Fixture tests for tech_article_check.py. Run: python3 -I tests/test_checker.py"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "tech_article_check.py"


def run(path):
    p = subprocess.run([sys.executable, "-I", str(SCRIPT), str(path), "--json"],
                       capture_output=True, text=True)
    return p.returncode, p.stdout


def main():
    import json
    fails = 0

    code, out = run(HERE / "fixtures" / "bad.md")
    r = json.loads(out)
    checks = {f["check"] for f in r["findings"] if f["severity"] == "hard"}
    expected = {"preamble-opener", "sequel-opener", "assumption-word", "marketing",
                "link-text", "code-unexplained"}
    if code != 1 or r["hard"] != 8 or not expected <= checks:
        print(f"FAIL bad.md: exit={code} hard={r['hard']} checks={sorted(checks)}"); fails += 1
    else:
        print("ok   bad.md flagged (8 hard)")

    code, out = run(HERE / "fixtures" / "good.md")
    r = json.loads(out)
    if code != 0 or r["hard"] or r["soft"]:
        print(f"FAIL good.md: exit={code} findings={r['findings']}"); fails += 1
    else:
        print("ok   good.md clean")

    code, out = run(HERE / "fixtures" / "mentions.md")
    r = json.loads(out)
    hits = [f for f in r["findings"] if f["check"] == "assumption-word"]
    if code != 1 or len(hits) != 1 or "simply" not in hits[0]["message"]:
        print(f"FAIL mentions.md: quoted mentions must pass, real use must flag: {hits}"); fails += 1
    else:
        print("ok   mentions.md: quoted words exempt, real 'Simply put' flagged")

    code, _ = run(HERE / "fixtures" / "does-not-exist.md")
    if code != 2:
        print(f"FAIL missing file exit={code}"); fails += 1
    else:
        print("ok   missing file exits 2")

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
