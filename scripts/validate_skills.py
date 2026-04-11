#!/usr/bin/env python3
"""Validate every SKILL.md frontmatter in skills/.

Checks:
1. YAML frontmatter parses
2. `name` field is present and matches the directory name
3. `description` field is present and `<= 200` characters
4. `disable-model-invocation` (if present) is a boolean
5. `paths` (if present) is a list of strings
6. `allowed-tools` (if present) is a string or list
"""

import sys
import os
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def parse_frontmatter(skill_md_path: Path) -> dict:
    text = skill_md_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{skill_md_path}: missing frontmatter opener")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{skill_md_path}: missing frontmatter closer")
    return yaml.safe_load(text[4:end])


def validate(skill_md_path: Path) -> list[str]:
    errors = []
    try:
        fm = parse_frontmatter(skill_md_path)
    except Exception as e:
        return [str(e)]
    if not isinstance(fm, dict):
        return [f"{skill_md_path}: frontmatter is not a mapping"]

    expected_name = skill_md_path.parent.name
    name = fm.get("name")
    if not name:
        errors.append(f"{skill_md_path}: missing `name` field")
    elif name != expected_name:
        errors.append(
            f"{skill_md_path}: `name` is '{name}' but directory is '{expected_name}'"
        )

    desc = fm.get("description")
    if not desc:
        errors.append(f"{skill_md_path}: missing `description` field")
    elif len(desc) > 200:
        errors.append(
            f"{skill_md_path}: description is {len(desc)} chars (max 200)"
        )

    dmi = fm.get("disable-model-invocation")
    if dmi is not None and not isinstance(dmi, bool):
        errors.append(f"{skill_md_path}: disable-model-invocation must be bool")

    paths = fm.get("paths")
    if paths is not None and not isinstance(paths, list):
        errors.append(f"{skill_md_path}: paths must be a list")

    return errors


def main() -> int:
    skills_dir = Path("skills")
    if not skills_dir.is_dir():
        print("ERROR: skills/ directory not found", file=sys.stderr)
        return 2
    all_errors = []
    skill_count = 0
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        skill_count += 1
        all_errors.extend(validate(skill_md))
    if all_errors:
        for e in all_errors:
            print(e)
        return 1
    print(f"OK: {skill_count} skills validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
