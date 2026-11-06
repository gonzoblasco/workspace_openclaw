#!/usr/bin/env python3
"""
ops-commit.py - commitea SOLO los archivos de kanam-ops.

Por que existe
--------------
El 2026-11-06 paso dos veces: `kanam-mind` commiteo con `git add` amplio y se
llevo 4 archivos de OPS dentro de un commit suyo, y en la otra direccion mi
propio commit se llevo 5 archivos de DEV y los borro del repo. El contenido
sobrevivio, pero el historial quedo mintiendo: el mensaje no describe lo que el
commit toca.

Un repo compartido por siete agentes no se arregla con disciplina: se arregla
con una herramienta que no tenga como equivocarse.

Que hace
--------
1. Descubre SOLO las rutas que le pertenecen a OPS (por defecto `agents/kanam-ops/`).
2. Se niega a continuar si hay cualquier otra cosa staged. No desetapéa archivos
   ajenos a la fuerza: avisa y sale, porque desetapear el trabajo de otro agente
   es otra forma de romperle el commit.
3. Rechaza paths peligrosos (`.env`, `*.db`, credenciales) aunque esten dentro
   de la carpeta de OPS.
4. Dry-run por defecto. `--apply` es lo unico que escribe.

Uso
---
    ops-commit.py                     # dry run: que se commitearia
    ops-commit.py --apply -m "mensaje"
    ops-commit.py --apply -m "..." --no-verify   # saltear hook, con motivo

Exit codes
----------
    0  todo bien (dry run valido, o commit hecho)
    1  hay archivos ajenos staged, o paths peligrosos, o nada para commitear
    2  error de uso o de git
"""
from __future__ import annotations

import argparse
import subprocess
import sys

OWNED_PREFIX = "agents/kanam-ops/"

# Se rechazan aunque vivan dentro de la carpeta de OPS: no son codigo, son
# datos locales o credenciales.
DANGEROUS_SUFFIXES = (".db", ".sqlite", ".db-wal", ".db-shm", ".env", ".pem", ".key")
DANGEROUS_NAMES = (".env", "id_rsa", "id_ed25519", "credentials.json")


def git(*args: str) -> tuple[int, str, str]:
    p = subprocess.run(["git", *args], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def staged_paths() -> list[str]:
    rc, out, err = git("diff", "--cached", "--name-only")
    if rc != 0:
        print("ERROR: no se pudo leer el indice: %s" % err.strip(), file=sys.stderr)
        sys.exit(2)
    return [l for l in out.splitlines() if l.strip()]


def changed_paths() -> list[str]:
    """Modificados, sin trackear y borrados, sin duplicar."""
    paths: set[str] = set()
    for args in (("diff", "--name-only"), ("ls-files", "--others", "--exclude-standard")):
        rc, out, _ = git(*args)
        if rc != 0:
            continue
        for line in out.splitlines():
            if line.strip():
                paths.add(line.strip())
    return sorted(paths)


def is_owned(path: str) -> bool:
    return path.startswith(OWNED_PREFIX)


def is_dangerous(path: str) -> bool:
    name = path.rsplit("/", 1)[-1]
    return name in DANGEROUS_NAMES or path.endswith(DANGEROUS_SUFFIXES)


def main() -> int:
    ap = argparse.ArgumentParser(description="Commitea solo los archivos de kanam-ops.")
    ap.add_argument("-m", "--message", help="mensaje del commit")
    ap.add_argument("--apply", action="store_true", help="ejecutar de verdad")
    ap.add_argument("--no-verify", action="store_true", help="saltear los hooks")
    args = ap.parse_args()

    rc, _, _ = git("rev-parse", "--git-dir")
    if rc != 0:
        print("ERROR: no es un repo git.", file=sys.stderr)
        return 2

    already = staged_paths()
    foreign_staged = [p for p in already if not is_owned(p)]
    if foreign_staged:
        print("ABORTA: hay archivos AJENOS ya en el indice.")
        print("No los desetapeo yo: eso rompe el commit de otro agente.")
        print("")
        for p in foreign_staged:
            print("  ! %s" % p)
        print("")
        print("Salida: que el otro agente los commitee, o desetapealos a mano")
        print("sabiendo que son suyos:")
        print("  git restore --staged <ruta>")
        return 1

    candidates = [p for p in changed_paths() if is_owned(p)]
    dangerous = [p for p in candidates if is_dangerous(p)]
    if dangerous:
        print("ABORTA: hay paths peligrosos dentro de %s." % OWNED_PREFIX)
        for p in dangerous:
            print("  ! %s" % p)
        print("No se commitean datos locales ni credenciales, ni con --apply.")
        return 1

    if not candidates:
        print("Nada de OPS para commitear. Indice limpio.")
        return 1

    print("Commiteables de OPS (%d):" % len(candidates))
    for p in candidates:
        print("  + %s" % p)
    print("")
    print("Intactos: %d archivo(s) de otros agentes en el working tree." %
          (len([p for p in changed_paths() if not is_owned(p)])))

    if not args.apply:
        print("")
        print("DRY RUN. Nada escrito. Agregar --apply -m \"...\" para commitear.")
        return 0

    if not args.message:
        print("ERROR: --apply necesita -m con el mensaje.", file=sys.stderr)
        return 2

    rc, _, err = git("add", "--", *candidates)
    if rc != 0:
        print("ERROR al agregar: %s" % err.strip(), file=sys.stderr)
        return 2

    # Verificacion post-add: el indice tiene que ser exactamente lo previsto.
    # Si algo mas se colo, se saca del indice antes de commitear.
    now_staged = staged_paths()
    unexpected = [p for p in now_staged if p not in candidates]
    if unexpected:
        print("ABORTA tras add: se colaron archivos no previstos.")
        for p in unexpected:
            print("  ! %s" % p)
        git("restore", "--staged", "--", *unexpected)
        return 1

    cmd = ["commit", "-m", args.message]
    if args.no_verify:
        cmd.append("--no-verify")
    rc, out, err = git(*cmd)
    print(out.strip() or err.strip())
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
