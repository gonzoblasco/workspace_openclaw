#!/usr/bin/env python3
"""
test_skill_units.py - Una skill con pasos pero sin verificacion es una receta.

Por que existe: las siete skills del arbol de kanam-dev tenian procedimiento
numerado, resultado esperado y regla dura, pero ninguna decia cuando el trabajo
esta terminado. Un humano con criterio sabe cortar; un modelo sin el contexto del
autor, no. La skill describe el viaje y no el destino.

Regla que verifica, sobre `agents/*/skills/*/SKILL.md`:
  1. Existe una seccion `## Verificacion` (o `## Verification`).
  2. Esa seccion tiene al menos 3 items verificables (checkbox o vineta).
  3. Al menos un item menciona un COMANDO o un ARCHIVO concreto: un criterio que
     solo dice "esta bien documentado" no se puede verificar.

No valida la calidad del criterio (eso necesita leer), valida que exista y que
tenga forma verificable.

  python3 scripts/test_skill_units.py [--all] [--verbose]

Exit 0 = todas las skills del scope tienen verificacion. Exit 1 = falta en alguna.
Exit 2 = no pudo medir.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERIF_HEADING = re.compile(r"^##\s+(Verificaci[oó]n|Verification)\b", re.MULTILINE | re.IGNORECASE)
ANY_HEADING = re.compile(r"^##\s+(.+)$", re.MULTILINE)
ITEM = re.compile(r"^\s*(?:-\s*\[[ xX]\]|[-*])\s+\S", re.MULTILINE)
# Un comando (`...`), un path con slash, un archivo con extension, o un exit code.
CONCRETE = re.compile(
    r"`[^`]+`"          # comando o nombre en backticks
    r"|\b[\w./-]+/[\w./-]+"   # ruta con barra
    r"|\b\w+\.(?:md|py|sh|mjs|js|json|yml|yaml|tsv)\b"  # archivo con extension
    r"|\bexit\s*\d"     # exit code
    r"|\b(?:ls|cat|git|npm|pytest|python3?|node|bash|docker)\b"  # invocacion
)

MIN_ITEMS = 3


def sections(text: str) -> list[tuple[str, str]]:
    """Divide el markdown en (titulo, cuerpo) por `## `. Pura."""
    marks = [(m.start(), m.group(1).strip()) for m in ANY_HEADING.finditer(text)]
    out: list[tuple[str, str]] = []
    for i, (start, title) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        out.append((title, text[start:end]))
    return out


def check_skill(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    found = None
    for title, body in sections(text):
        if re.match(r"(Verificaci[oó]n|Verification)\b", title, re.IGNORECASE):
            found = body
            break

    if found is None:
        return ["sin seccion de verificacion"]

    items = ITEM.findall(found)
    if len(items) < MIN_ITEMS:
        problems.append(f"la verificacion tiene {len(items)} item(s), minimo {MIN_ITEMS}")

    if not CONCRETE.search(found):
        problems.append("ningun item cita un comando, un archivo o un exit code")

    return problems


def _in_scope(skill_md: Path) -> bool:
    """En el scope por defecto: solo las siete auditadas del arbol de dev."""
    return skill_md.parent.name in AUDITED


def main(argv: list[str]) -> int:
    verbose = "--verbose" in argv
    args_all = "--all" in argv

    roots = [ROOT / "skills"] + sorted((ROOT / "agents").glob("*/skills"))
    if not args_all:
        roots = [ROOT / "agents" / "kanam-dev" / "skills"]

    if not any(r.exists() for r in roots):
        print("[INFRA] no hay arboles de skills para revisar", file=sys.stderr)
        return 2

    failures: list[str] = []
    checked = 0

    for root in roots:
        if not root.exists():
            continue
        for skill_md in sorted(root.glob("*/SKILL.md")):
            if not args_all and not _in_scope(skill_md):
                continue
            checked += 1
            problems = check_skill(skill_md)
            if problems:
                rel = skill_md.relative_to(ROOT)
                failures.append(f"{rel}: {'; '.join(problems)}")
            elif verbose:
                print(f"[ok] {skill_md.relative_to(ROOT)}")

    if failures:
        for f in failures:
            print(f"[SIN VERIFICACION] {f}")
        print(f"\n{len(failures)} de {checked} skill(s) sin criterio de parada verificable")
        return 1

    print(f"[OK] las {checked} skill(s) del scope tienen criterio de parada verificable")
    return 0


# Scope por defecto: las SIETE skills que la auditoria de unidades marco como
# defectuosas. No todo el arbol: 30 de las 44 no tienen seccion de verificacion, y
# bloquear por eso convertiria el gate en ruido que empuja al --no-verify. El
# alcance crece cuando alguien arregla esas 30, no antes. `--all` barre todo para
# que el CI y una sesion futura sepan cuanto falta.
AUDITED = (
    "api-integration-test",
    "chaos-engineering",
    "code-metrics",
    "compatibility-testing",
    "dependency-advisor",
    "performance-benchmark",
    "threat-modeling",
)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
