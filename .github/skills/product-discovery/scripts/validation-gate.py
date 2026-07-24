#!/usr/bin/env python3
"""validation-gate.py — Check if product discovery outputs are complete.

Usage:
  python3 validation-gate.py [--dir <project-dir>]

Checks BRIEF.md and DEFINITION.md for completeness before
passing from Phase 0.1 to Phase 0.2.
"""

import sys
from pathlib import Path


def check_file(filepath: Path, checks: list[tuple[str, str]]) -> list[str]:
    """Run checks on a file and return failures."""
    if not filepath.exists():
        return [f"❌ {filepath.name} not found"]

    content = filepath.read_text()
    failures = []

    for check_name, pattern in checks:
        if pattern not in content:
            failures.append(f"❌ {filepath.name}: {check_name}")

    return failures


def main():
    project_dir = sys.argv[2] if len(sys.argv) >= 3 and sys.argv[1] == "--dir" else "."
    project_path = Path(project_dir)

    print(f"🔍 Validating product discovery outputs in: {project_dir}")
    print()

    brief_checks = [
        ("Problem statement", "## Problem"),
        ("Target audience", "## Target Audience"),
        ("Solution concept", "## Solution Concept"),
        ("Key features", "## Key Features"),
        ("Success metrics", "## Success Metrics"),
    ]

    definition_checks = [
        ("Feature list", "## Features"),
        ("User personas", "## Personas"),
        ("Technical stack", "## Stack"),
    ]

    failures = []
    failures.extend(check_file(project_path / "BRIEF.md", brief_checks))
    failures.extend(check_file(project_path / "DEFINITION.md", definition_checks))

    if not failures:
        print("✅ All checks passed! Ready for Phase 0.2")
        return

    print("❌ Validation failed:")
    for f in failures:
        print(f"  {f}")

    print()
    print("Fix the issues above before proceeding to Phase 0.2")
    sys.exit(1)


if __name__ == "__main__":
    main()
