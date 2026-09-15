#!/usr/bin/env python3
"""Validate the versioned prompts in prompts/.

Each prompt is a markdown file in prompts/ with YAML frontmatter:
  ---
  id: <slug>            # must match the filename  <slug>.md
  version: N            # positive integer
  scope: <scope>        # one of: workspace | project | global
  tags: [a, b]          # non-empty list
  ---
  <body>                # the actual prompt

Rules enforced:
  - every prompts/*.md has valid frontmatter with id/version/scope/tags
  - id matches the filename
  - version is a positive integer
  - scope is one of the allowed values
  - tags is a non-empty list
  - ids are unique across files

Exit 0 if all valid, 1 otherwise (prints the problems).

The YAML frontmatter lives between leading '---' lines. The complexity-scorer
script reads the body via grep, so adding frontmatter must not change the body
scoring rules.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"

ALLOWED_SCOPES = {"workspace", "project", "global"}

FRONT = re.compile(r"^---\s*$")


def parse_frontmatter(text):
    """Return (frontmatter_dict, body) or (None, None) on bad/unparseable."""
    lines = text.splitlines()
    if not lines or not FRONT.match(lines[0]):
        return None, None
    # find the closing ---
    end = None
    for i in range(1, len(lines)):
        if FRONT.match(lines[i]):
            end = i
            break
    if end is None:
        return None, None
    fm = lines[1:end]
    body = "\n".join(lines[end + 1:]).strip()
    data = {}
    for ln in fm:
        if ":" not in ln:
            continue
        key, _, val = ln.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            val = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
        elif val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        elif val.startswith("'") and val.endswith("'"):
            val = val[1:-1]
        data[key] = val
    return data, body


def main():
    problems = []
    files = sorted(PROMPTS.glob("*.md"))
    if not files:
        print("OK: no prompts to validate (prompts/ vacio).")
        return 0

    seen_ids = {}
    for f in files:
        slug = f.stem
        text = f.read_text(encoding="utf-8")
        data, body = parse_frontmatter(text)
        if data is None:
            problems.append(f"{f.name}: frontmatter invalido o ausente (esperado '---' + id/version/scope/tags + '---')")
            continue
        # id
        pid = data.get("id")
        if pid is None:
            problems.append(f"{f.name}: falta 'id' en frontmatter")
        elif pid != slug:
            problems.append(f"{f.name}: id '{pid}' no coincide con el nombre del archivo (slug '{slug}')")
        else:
            if pid in seen_ids:
                problems.append(f"{f.name}: id '{pid}' duplicado (tambien en {seen_ids[pid]})")
            seen_ids[pid] = f.name
        # version
        ver = data.get("version")
        if ver is None or not (isinstance(ver, str) and ver.isdigit() and int(ver) >= 1):
            problems.append(f"{f.name}: version invalida ('{ver}', esperado entero >= 1)")
        # scope
        sc = data.get("scope")
        if sc is None or sc not in ALLOWED_SCOPES:
            problems.append(f"{f.name}: scope invalido ('{sc}', esperado uno de {sorted(ALLOWED_SCOPES)})")
        # tags
        tags = data.get("tags")
        if tags is None or not isinstance(tags, list) or not tags:
            problems.append(f"{f.name}: tags invalido ('{tags}', esperado lista no vacia)")
        # body present
        if not body:
            problems.append(f"{f.name}: cuerpo vacio")

    if problems:
        print("Problemas en prompts versionados:")
        for p in problems:
            print("  - " + p)
        print(f"\n{len(problems)} problema(s) en {len(files)} archivo(s).")
        return 1

    print(f"OK: {len(files)} prompt(s) versionado(s) validos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
