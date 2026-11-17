#!/usr/bin/env python3
"""check-skill-integrity.py - a skill must have one frontmatter and one body.

The skill review rewrites SKILL.md files automatically. On 2026-11-17
`memory-wiki-vault` came out of one rewrite with 87 lines: the new procedure
(`## Camino A`, `## Camino B`, `## Decision rules`, `## Related`) followed by
the entire old body, its own `## Steps`, a second `## Decision rules` and a
second `## Related`. Nothing failed. An agent reading it got two contradictory
procedures - one saying "align the duplicated keys", the other "enable the
bundled plugin and ingest" - and whichever section it read first won.

The checks are structural, so they catch a merge that no linter sees:

  1. exactly one YAML frontmatter, at the top, closed by `---`
  2. `name:` present and equal to the directory name
  3. `description:` present and non-empty
  4. no top-level heading duplicated (`## Decision rules` twice = two bodies)
  5. a repeated `## Steps`/`## Steps`-style block is reported with the line
  6. no line that looks like a second frontmatter start after the first block

Scope: every SKILL.md under the given roots. Default roots are the agent
skill trees; `--all` includes the workspace `skills/`.

Advisory by design at the pre-commit (warns, never blocks): a skill is
documentation, and a broken one should be loud, not a commit stopper. A gate
that blocks on prose teaches `--no-verify`.

Exit 0 clean (or warnings only), 1 findings in strict mode, 2 no skills.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOME = pathlib.Path.home()

DEFAULT_ROOTS = [
    HOME / ".openclaw" / "agents" / "main" / "agent" / "workshop-skills",
    HOME / ".openclaw" / "agents" / "main" / "agent" / "skills",
    HOME / ".agents" / "skills",
    HOME / ".openclaw" / "plugin-skills",
]

HEADING = re.compile(r"^(##+)\s+(.+?)\s*$")


def find_skills(roots, include_workspace: bool):
    found = []
    paths = list(roots)
    if include_workspace:
        paths.append(ROOT / "skills")
        paths.append(ROOT / "agents")
    for root in paths:
        if not root.is_dir():
            continue
        for p in root.rglob("SKILL.md"):
            if ".git" in p.parts:
                continue
            # .archive/ guarda versiones anteriores con el nombre del skill, no
            # del directorio de la version: comparar `name:` contra el directorio
            # ahi es ruido puro (425 falsos positivos el 2026-11-17).
            if ".archive" in p.parts:
                continue
            found.append(p)
    return sorted(set(found))


def check_skill(path: pathlib.Path):
    """Return (findings, warnings) for one SKILL.md."""
    findings = []
    warnings = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{path}: unreadable ({exc})"], []

    lines = text.splitlines()
    name = path.parent.name

    # 1) frontmatter
    if not lines or lines[0].strip() != "---":
        findings.append("no frontmatter at line 1")
        return findings, warnings
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        findings.append("frontmatter never closed with ---")
        return findings, warnings

    header = "\n".join(lines[1:end])
    m = re.search(r"^name:\s*[\"']?([^\"'\n]+)[\"']?\s*$", header, re.MULTILINE)
    if not m:
        findings.append("frontmatter has no name:")
    elif m.group(1).strip() != name:
        findings.append(f"name '{m.group(1).strip()}' != directory '{name}'")
    d = re.search(r"^description:\s*(.+)$", header, re.MULTILINE)
    if not d or len(d.group(1).strip()) < 20:
        findings.append("frontmatter description missing or too short")

    body = lines[end + 1:]

    # 2) a second frontmatter start inside the body = two documents glued
    for offset, line in enumerate(body, start=end + 2):
        if line.strip() == "---" and offset > end + 3:
            # a horizontal rule is legal; only flag when followed by `name:`
            nxt = body[offset - end - 1: offset - end + 2]
            if any(x.strip().startswith("name:") for x in nxt):
                findings.append(f"line {offset}: second frontmatter inside the body")
                break

    # 3) duplicated top-level headings = two bodies
    seen = {}
    for offset, line in enumerate(body, start=end + 2):
        hm = HEADING.match(line)
        if not hm:
            continue
        key = hm.group(2).strip().lower()
        if key in seen:
            findings.append(
                f"line {offset}: duplicate heading '## {hm.group(2).strip()}' "
                f"(first at line {seen[key]}) - two bodies?"
            )
        else:
            seen[key] = offset

    # 4) advisory: a body that restates the same intro paragraph
    first_sentence = next((l for l in body if len(l) > 60 and not l.startswith(("#", "-", ">", "|"))), "")
    if first_sentence:
        needle = first_sentence.strip()[:60]
        repeats = sum(1 for l in body if needle and needle in l)
        if repeats > 1:
            warnings.append(f"opening paragraph repeated {repeats} times")

    return findings, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="include the workspace skills/ and agents/ trees")
    ap.add_argument("--strict", action="store_true", help="exit 1 on findings (default: advisory)")
    ap.add_argument("paths", nargs="*", help="explicit SKILL.md paths to check")
    args = ap.parse_args()

    if args.paths:
        skills = [pathlib.Path(p).resolve() if not pathlib.Path(p).is_absolute() else pathlib.Path(p)
                  for p in args.paths]
    else:
        skills = find_skills(DEFAULT_ROOTS, args.all)

    if not skills:
        print("No SKILL.md found", file=sys.stderr)
        return 2

    total_findings = 0
    total_warnings = 0
    for path in skills:
        findings, warnings = check_skill(path)
        try:
            shown = path.relative_to(HOME)
        except ValueError:
            shown = path
        if findings or warnings:
            print(f"{shown}")
            for f in findings:
                print(f"  FAIL  {f}")
            for w in warnings:
                print(f"  warn  {w}")
        total_findings += len(findings)
        total_warnings += len(warnings)

    print(f"{len(skills)} skills revisadas: {total_findings} finding(s), {total_warnings} warning(s)")
    if total_findings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
