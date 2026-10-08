#!/usr/bin/env python3
"""Fail if any profile has two SKILL.md files that declare the same skill name.

Hermes refuses a bare skill_view('<name>') when two different skills share a
name in one tier, and identical copies silently diverge on the next bundled
update. Each profile must hold exactly one copy of every skill name.

CI caveat: bundled skills are synced into profiles/<name>/skills/<category>/ only at
runtime and are git-ignored, so on a CI checkout this script sees shared and local
skills only. There, shadowing a bundled skill is caught solely by validate_profiles.py,
and only if the skill is listed under `bundled:` in profile.yaml. Run this locally
against a live install to catch an undeclared shadow.

Usage: scripts/check-skill-collisions.py [profiles_dir]   (exit 1 on collision)
"""
import collections
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^name:\s*['\"]?([^'\"\s]+)", re.M)


def skill_names(skills_root: Path) -> dict:
    found = collections.defaultdict(list)
    for md in skills_root.rglob("SKILL.md"):
        rel = md.relative_to(skills_root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        match = NAME_RE.search(md.read_text(errors="ignore"))
        found[match.group(1) if match else md.parent.name].append(rel.parent.as_posix())
    return found


def main() -> int:
    profiles = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "profiles")
    bad = 0
    for skills_root in sorted(profiles.glob("*/skills")):
        for name, paths in sorted(skill_names(skills_root).items()):
            if len(paths) > 1:
                bad += 1
                print(f"{skills_root.parent.name}: '{name}' at {', '.join(sorted(paths))}")
    if bad:
        print(f"\n{bad} collision(s). Keep one copy per profile: delete the duplicate "
              "(bundled copies stay deleted; sync records them as user-removed).")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
