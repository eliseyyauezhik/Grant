#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--resources scripts,references,assets]

Examples:
    init_skill.py my-new-skill --path .agents/skills
    init_skill.py my-new-skill --path .agents/skills --resources scripts,references
"""

import argparse
import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}

SKILL_TEMPLATE = """---
name: {skill_name}
description: "[TODO: What this skill does]. Use when [TODO: triggers]. Do NOT use for [TODO: negative triggers]."
---

# {skill_title}

## Overview
[TODO: 1-2 sentences explaining what this skill enables]

## [TODO: Main section — choose structure from patterns.md]

Step-by-step instructions here. Use imperative voice.

## Common Mistakes
[TODO: What goes wrong + how to fix]
"""

REFERENCE_TEMPLATE = """# Reference Documentation for {skill_title}

[TODO: Add detailed reference content here]
"""


def normalize_skill_name(skill_name):
    normalized = skill_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def title_case_skill_name(skill_name):
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def parse_resources(raw_resources):
    if not raw_resources:
        return []
    resources = [item.strip() for item in raw_resources.split(",") if item.strip()]
    invalid = sorted({item for item in resources if item not in ALLOWED_RESOURCES})
    if invalid:
        print(f"[ERROR] Unknown resource type(s): {', '.join(invalid)}")
        sys.exit(1)
    return list(dict.fromkeys(resources))  # dedupe preserving order


def init_skill(skill_name, path, resources):
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"[ERROR] Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"[ERROR] Error creating directory: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)

    skill_md_path = skill_dir / "SKILL.md"
    try:
        skill_md_path.write_text(skill_content, encoding="utf-8")
        print("[OK] Created SKILL.md")
    except Exception as e:
        print(f"[ERROR] Error creating SKILL.md: {e}")
        return None

    for resource in resources:
        resource_dir = skill_dir / resource
        resource_dir.mkdir(exist_ok=True)
        if resource == "references":
            ref_file = resource_dir / "reference.md"
            ref_file.write_text(
                REFERENCE_TEMPLATE.format(skill_title=skill_title),
                encoding="utf-8",
            )
        print(f"[OK] Created {resource}/")

    print(f"\n[OK] Skill '{skill_name}' initialized at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md — complete the TODO items")
    print("2. Run eval_skill.py when ready to check")
    return skill_dir


def main():
    parser = argparse.ArgumentParser(description="Create a new skill directory.")
    parser.add_argument("skill_name", help="Skill name (normalized to kebab-case)")
    parser.add_argument("--path", required=True, help="Output directory")
    parser.add_argument("--resources", default="", help="Comma-separated: scripts,references,assets")
    args = parser.parse_args()

    skill_name = normalize_skill_name(args.skill_name)
    if not skill_name:
        print("[ERROR] Skill name must include at least one letter or digit.")
        sys.exit(1)
    if len(skill_name) > MAX_SKILL_NAME_LENGTH:
        print(f"[ERROR] Name too long ({len(skill_name)} chars, max {MAX_SKILL_NAME_LENGTH}).")
        sys.exit(1)

    resources = parse_resources(args.resources)
    result = init_skill(skill_name, args.path, resources)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
