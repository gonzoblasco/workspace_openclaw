#!/usr/bin/env python3
"""Guarda: el `.knowledge/` propio nunca viaja a un repo ajeno.

Por que existe (2026-11-03, pedido de Gonzo): *"nunca subir el .knowledge a los
repos OSS, ese es el unico caso (y quiza los forks ya que tampoco son repos
nuestros). El tema es no ensuciar lo ajeno."*

El riesgo medido: `forks/vane/` tiene 9 archivos `.knowledge/` **trackeados** y un
remote `upstream` apuntando a `ItzCrazyKns/Vane`. Hoy no estan en upstream (0
archivos), pero un `git push upstream` desde cualquier rama que los contenga los
sube. Nada lo impedia.

La guarda correcta NO es tocar el `.gitignore` del repo ajeno (eso si lo
ensucia) ni mover el `.knowledge/` fuera del fork (se pierde la memoria del
hilo). Es un **hook pre-push local**: vive en `.git/hooks/`, nunca se commitea,
y rechaza el push de cualquier ref que contenga `.knowledge/` hacia un remote
que no sea de `gonzoblasco`.

Uso:
  scripts/check-foreign-knowledge.py            # verifica (exit 1 si falta algo)
  scripts/check-foreign-knowledge.py --install  # instala el hook donde falte
  scripts/check-foreign-knowledge.py --json     # salida para maquinas

Sale 0 cuando todos los repos ajenos tienen la guarda. Corre en el pre-commit
del workspace: un fork nuevo sin hook frena el commit hasta que se instale.
"""
import argparse
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

WORKSPACE = Path(__file__).resolve().parent.parent

# Contenedores con repos de terceros. `projects/` queda afuera a proposito: son
# repos nuestros (bajo gonzoblasco) y ahi el `.knowledge/` ES el proyecto.
FOREIGN_CONTAINERS = ("forks", "clones")

# Un remote es "nuestro" si el owner del path es gonzoblasco. Se compara contra
# la URL, que es lo unico que el hook ve en tiempo de push.
OWNER = "gonzoblasco"

# SHA nulo que git usa para "la ref no existe del otro lado" (rama nueva).
ZERO_SHA = "0" * 40

HOOK_MARKER = "# openclaw: foreign-knowledge-guard"
HOOK_BODY = f"""#!/bin/sh
{HOOK_MARKER}
# Rechaza empujar `.knowledge/` a un remote que no es de {OWNER}.
# Instalado por scripts/check-foreign-knowledge.py. Vive solo en .git/hooks:
# no se commitea, asi que el repo ajeno no se ensucia.
remote_name="$1"
remote_url="$2"
case "$remote_url" in
  *{OWNER}/*) exit 0 ;;
esac
zero="0000000000000000000000000000000000000000"
while read -r local_ref local_sha remote_ref remote_sha; do
  [ "$local_sha" = "$zero" ] && continue
  if [ "$remote_sha" = "$zero" ]; then
    files=$(git ls-tree -r --name-only "$local_sha" 2>/dev/null)
  else
    files=$(git diff --name-only "$remote_sha" "$local_sha" 2>/dev/null)
  fi
  if printf '%s\\n' "$files" | grep -q '^\\.knowledge/'; then
    echo "pre-push: rechazado - esta rama incluye .knowledge/ y el destino" >&2
    echo "          no es un repo de {OWNER} ($remote_url)." >&2
    echo "          Ese contenido es memoria local, no contribucion." >&2
    exit 1
  fi
done
exit 0
"""


def git(args: List[str], cwd: Path) -> str:
    try:
        out = subprocess.run(
            ["git", *args], cwd=str(cwd), capture_output=True, text=True, check=False
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def is_repo(path: Path) -> bool:
    return (path / ".git").exists()


def remotes(path: Path) -> Dict[str, str]:
    raw = git(["remote", "-v"], path)
    found: Dict[str, str] = {}
    for line in raw.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0] not in found:
            found[parts[0]] = parts[1]
    return found


def is_ours(url: str) -> bool:
    return f"{OWNER}/" in url


def tracked_knowledge(path: Path) -> List[str]:
    raw = git(["ls-files", ".knowledge"], path)
    return [ln for ln in raw.splitlines() if ln.strip()]


def hook_installed(path: Path) -> bool:
    hook = path / ".git" / "hooks" / "pre-push"
    try:
        return HOOK_MARKER in hook.read_text(encoding="utf-8")
    except OSError:
        return False


def install_hook(path: Path) -> Path:
    hooks = path / ".git" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    hook = hooks / "pre-push"
    hook.write_text(HOOK_BODY, encoding="utf-8")
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return hook


def scan() -> List[dict]:
    results: List[dict] = []
    for container in FOREIGN_CONTAINERS:
        root = WORKSPACE / container
        if not root.is_dir():
            continue
        for entry in sorted(root.iterdir()):
            if not entry.is_dir() or not is_repo(entry):
                continue
            rems = remotes(entry)
            tracked = tracked_knowledge(entry)
            third_party = {n: u for n, u in rems.items() if not is_ours(u)}
            results.append(
                {
                    "repo": str(entry.relative_to(WORKSPACE)),
                    "remotes": rems,
                    "third_party_remotes": third_party,
                    "tracked_knowledge": tracked,
                    "hook": hook_installed(entry),
                    "at_risk": bool(tracked) and bool(third_party),
                }
            )
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--install", action="store_true", help="instala el hook donde falte")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    args = ap.parse_args()

    results = scan()
    if args.install:
        for r in results:
            path = WORKSPACE / r["repo"]
            if not r["hook"]:
                install_hook(path)
                r["hook"] = True
        results = scan()

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0 if all(r["hook"] for r in results) else 1

    if not results:
        print("OK: no hay repos de terceros en forks/ ni clones/.")
        return 0

    missing = []
    for r in results:
        status = "OK  " if r["hook"] else "FALTA"
        extra = ""
        if r["at_risk"] and not r["hook"]:
            extra = f"  <-- {len(r['tracked_knowledge'])} archivos .knowledge y remote ajeno"
        print(f"[{status}] {r['repo']}{extra}")
        if not r["hook"]:
            missing.append(r["repo"])

    print()
    if missing:
        print("Falta la guarda pre-push en: " + ", ".join(missing))
        print("Instalar con: scripts/check-foreign-knowledge.py --install")
        return 1
    print(f"OK: {len(results)} repo(s) de terceros con guarda pre-push.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
