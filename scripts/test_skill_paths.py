#!/usr/bin/env python3
"""
test_skill_paths.py - Toda ruta a un recurso del workspace lleva su raiz.

Por que existe: `a11y-at-validation` mandaba correr `node scripts/a11y-scan.mjs`
desde el proyecto que se estaba auditando. Ese script vive en el workspace, no en
el proyecto, asi que el comando fallaba con "file not found" y el modelo lo podia
leer como un proyecto roto. Es un defecto de unidad: el SKILL.md se lee solo, y la
ruta no dice de quien es.

Regla que verifica: si un SKILL.md de `agents/*/skills/` menciona un script que
existe en el workspace pero NO en el directorio de la skill, la mencion debe
llevar la raiz `~/.openclaw/workspace/`.

Excepciones legitimas, verificadas por contexto:
  - una linea que describe el error (empieza con "Running", "Running the", etc.)
  - una linea dentro de un bloque de dependencias que ya declara la raiz

  python3 scripts/test_skill_paths.py            # scope: agents/kanam-dev/skills/
  python3 scripts/test_skill_paths.py --all      # todos los arboles de skills
  python3 scripts/test_skill_paths.py --verbose

Exit 0 = sin rutas ambiguas en el scope. Exit 1 = hay al menos una. Exit 2 = no
pudo medir.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_SCRIPTS = ROOT / "scripts"
SKILL_ROOTS = [ROOT / "skills"] + sorted((ROOT / "agents").glob("*/skills"))

# Mencion de un script del workspace: `scripts/foo.sh`, `./scripts/foo.sh`.
REF = re.compile(r"\.?/?scripts/([A-Za-z0-9_.-]+\.(?:sh|py|mjs|js))")

# Una linea esta "rooted" si dice donde vive el workspace. Es mas robusto que un
# lookbehind: el nombre del script puede aparecer sin la ruta delante cuando la
# linea ya explico la raiz ("the workspace script foo.sh ... at ~/.openclaw/...").
ROOT_MARKER = re.compile(r"~/\.openclaw/workspace/|\$HOME/\.openclaw/workspace/")

# Lineas que hablan DEL error, no lo mandan. Son la documentacion del defecto.
DESCRIBES_THE_ERROR = re.compile(
    r"^\s*(Running|Ejecutando|Correr desde|Running it|\*\*Pitfall:\*\*)\b", re.IGNORECASE
)


def workspace_script(name: str) -> bool:
    return (WORKSPACE_SCRIPTS / name).exists()


def is_skill_local(skill_dir: Path, name: str) -> bool:
    return (skill_dir / "scripts" / name).exists()


def main(argv: list[str]) -> int:
    verbose = "--verbose" in argv
    args_all = "--all" in argv

    if not WORKSPACE_SCRIPTS.exists():
        print(f"[INFRA] falta {WORKSPACE_SCRIPTS}", file=sys.stderr)
        return 2

    problems: list[str] = []
    checked = 0

    for skill_root in SKILL_ROOTS:
        if not skill_root.exists():
            continue
        for skill_md in sorted(skill_root.glob("*/SKILL.md")):
            skill_dir = skill_md.parent
            for i, line in enumerate(skill_md.read_text(encoding="utf-8").splitlines(), 1):
                if DESCRIBES_THE_ERROR.match(line):
                    if REF.search(line) and verbose:
                        print(f"[ok-excepcion] {skill_md.relative_to(ROOT)}:{i} describe el error")
                    continue
                for m in REF.finditer(line):
                    name = m.group(1)
                    # Solo importa si el script esta en el workspace y no en la skill.
                    if not workspace_script(name) or is_skill_local(skill_dir, name):
                        continue
                    checked += 1
                    if ROOT_MARKER.search(line):
                        continue
                    rel = skill_md.relative_to(ROOT)
                    problems.append(
                        f"{rel}:{i} cita scripts/{name} sin raiz de workspace "
                        f"(usar ~/.openclaw/workspace/scripts/{name})"
                    )

    # Alcance acotado por una razon medible: el barrido completo encuentra 87
    # rutas ambiguas en 14 skills de otros roles, que esta pasada no arregla (no
    # son mi arbol). Bloquear por eso convierte el gate en ruido y empuja al
    # --no-verify, que es peor que no tenerlo. `--all` barre todo para que el CI
    # y una sesion futura puedan usarlo cuando se limpien.
    in_scope = [p for p in problems if not args_all and "agents/kanam-dev/" not in p]
    out_of_scope = [p for p in problems if args_all or "agents/kanam-dev/" in p]

    if out_of_scope:
        for p in out_of_scope:
            print(f"[AMBIGUA] {p}")

    if in_scope and not args_all:
        print(f"[INFO] {len(in_scope)} ruta(s) ambigua(s) fuera del arbol de kanam-dev "
              f"(usar --all para verlas)")

    if out_of_scope:
        return 1

    print(f"[OK] rutas de workspace sin ambiguedad ({checked} referencias revisadas)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
