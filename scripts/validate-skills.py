#!/usr/bin/env python3
"""Validate agentskills.io skills, templates, symlinks, and markdown links."""

import json
import pathlib
import re
import sys


def parse_frontmatter(text: str) -> dict[str, str]:
    """Extract simple key-value pairs from YAML frontmatter."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            fields[key.strip()] = val.strip()
    return fields


def main() -> int:
    """Run all repository skill and link validations."""
    root = pathlib.Path(__file__).resolve().parent.parent
    errors: list[str] = []

    # 1. Validate symlinks
    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_symlink() and not path.exists():
            errors.append(f"Broken symlink: {path.relative_to(root)}")

    # 2. Validate markdown relative links
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for md in root.rglob("*.md"):
        if ".git" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target_path = (md.parent / target.split("#")[0]).resolve()
            if not target_path.exists():
                errors.append(f"Broken link in {md.relative_to(root)}: {target}")

    # 3. Validate skills under .agents/skills/*/SKILL.md
    skills_dir = root / ".agents" / "skills"
    if not skills_dir.is_dir():
        errors.append("Missing .agents/skills directory")
    else:
        for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
            text = skill_md.read_text(encoding="utf-8")
            lines = text.splitlines()
            if len(lines) > 300:
                errors.append(f"{skill_md.relative_to(root)} exceeds 300 lines ({len(lines)})")
            fm = parse_frontmatter(text)
            expected_name = skill_md.parent.name
            if fm.get("name") != expected_name:
                errors.append(
                    f"{skill_md.relative_to(root)}: frontmatter name {fm.get('name')!r} != {expected_name!r}"
                )
            if not fm.get("description"):
                errors.append(f"{skill_md.relative_to(root)}: missing frontmatter description")

    # 4. Validate state-template.json
    state_tpl = skills_dir / "sdd" / "references" / "state-template.json"
    try:
        data = json.loads(state_tpl.read_text(encoding="utf-8"))
        if "acquired_skills" not in data:
            errors.append("state-template.json missing 'acquired_skills'")
    except Exception as exc:
        errors.append(f"Invalid state-template.json: {exc}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print("All skills, templates, symlinks, and markdown links verified OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
