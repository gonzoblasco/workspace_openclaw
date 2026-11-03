#!/usr/bin/env python3
"""Guarda: el `.knowledge/` propio nunca viaja a un repo ajeno.

Por que existe (2026-11-03, pedido de Gonzo): *"nunca subir el .knowledge a los
repos OSS, ese es el unico caso (y quiza los forks ya que tampoco son repos
nuestros). El tema es no ensuciar lo ajeno."*

El riesgo medido: un fork con 9 archivos `.knowledge/` **trackeados** y un remote
`upstream` apuntando al repo del tercero. Hoy no estaban en upstream (0 archivos),
pero un `git push upstream` desde cualquier rama que los contenga los sube. Nada
lo impedia. Y el caso peor no es el push: es el **diff del PR**, que sale de
nuestro fork con el `.knowledge/` adentro.

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

# Clasificacion por PROPOSITO, no por origen del codigo (2026-11-03).
#
# `forks/` y `clones/` existen para **mandar un PR**: un clon descartable del que
# sale un diff que revisa un maintainer. Ahi `.knowledge/` es un contaminante.
#
# `services/` (creado 2026-11-03) es otra cosa: un repo de terceros que **corre**
# como servicio interno y que no se contribuye. Su `.knowledge/` es nuestro y va
# trackeado en NUESTRO fork (gonzoblasco/...), no en el del upstream.
#
# La distincion existe porque `vane` estaba en `forks/` y necesitaba una
# exencion para pasar este check. Una exencion es un olor a clasificacion
# equivocada: el problema era la carpeta, no la regla.
FOREIGN_CONTAINERS = ("forks", "clones")
SERVICE_CONTAINERS = ("services",)

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


def info_exclude(path: Path) -> Path:
    return path / ".git" / "info" / "exclude"


def excluded_knowledge(path: Path) -> bool:
    """`.knowledge/` esta en el exclude privado del clon (no versionado)."""
    try:
        lines = info_exclude(path).read_text(encoding="utf-8").splitlines()
    except OSError:
        return False
    return any(ln.strip().rstrip("/") == ".knowledge" for ln in lines if ln.strip() and not ln.strip().startswith("#"))


def add_info_exclude(path: Path) -> Path:
    """Agrega `.knowledge/` al `.git/info/exclude` del clon.

    Es la unica forma de ignorar el archivo SIN tocar nada versionado del repo
    ajeno: `.gitignore` se commitea y aparece en el diff del PR, que es
    justamente lo que hay que evitar.
    """
    target = info_exclude(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    if excluded_knowledge(path):
        return target
    block = (
        "\n# openclaw: memoria local, nunca se sube al repo de terceros.\n"
        ".knowledge/\n"
    )
    target.write_text(existing + block, encoding="utf-8")
    return target


def untrack_knowledge(path: Path) -> bool:
    """`git rm -r --cached .knowledge`: sale del indice y queda en disco."""
    res = subprocess.run(
        ["git", "rm", "-r", "--cached", "--quiet", ".knowledge"],
        cwd=str(path),
        capture_output=True,
        text=True,
        check=False,
    )
    return res.returncode == 0


def install_hook(path: Path) -> Path:
    hooks = path / ".git" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    hook = hooks / "pre-push"
    hook.write_text(HOOK_BODY, encoding="utf-8")
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return hook


def scan() -> List[dict]:
    results: List[dict] = []
    for container in FOREIGN_CONTAINERS + SERVICE_CONTAINERS:
        root = WORKSPACE / container
        if not root.is_dir():
            continue
        for entry in sorted(root.iterdir()):
            if not entry.is_dir() or not is_repo(entry):
                continue
            rems = remotes(entry)
            tracked = tracked_knowledge(entry)
            third_party = {n: u for n, u in rems.items() if not is_ours(u)}
            rel = str(entry.relative_to(WORKSPACE))
            is_service = container in SERVICE_CONTAINERS
            hook = hook_installed(entry)
            # Un fork con `.knowledge/` trackeado lo mete en el diff de CUALQUIER
            # PR que salga de el: el riesgo es de indice, no de remote, y el
            # hook del pre-push no lo cubre. En un servicio el `.knowledge/` es
            # deliberado y vive en nuestro fork; el unico riesgo es que un push
            # al upstream lo suba, y eso si lo cubre el hook.
            at_risk = (
                bool(tracked) and bool(third_party) and not hook
                if is_service
                else bool(tracked)
            )
            results.append(
                {
                    "repo": rel,
                    "container": container,
                    "is_service": is_service,
                    "remotes": rems,
                    "third_party_remotes": third_party,
                    "tracked_knowledge": tracked,
                    "hook": hook,
                    "excluded": excluded_knowledge(entry),
                    "at_risk": at_risk,
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
            # En un FORK, el `.knowledge/` trackeado es lo que viaja en el diff
            # del PR: se saca del indice (queda en disco) y se oculta al clon.
            # En un SERVICIO se deja trackeado a proposito: es memoria nuestra,
            # en nuestro fork. Lo que se evita es el push al upstream (el hook).
            if not r["is_service"] and r["tracked_knowledge"]:
                untrack_knowledge(path)
                add_info_exclude(path)
        results = scan()

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0 if not _problems(results) else 1

    if not results:
        print("OK: no hay repos de terceros en forks/ ni clones/.")
        return 0

    problems = _problems(results)
    for r in results:
        kind = "servicio" if r["is_service"] else "fork"
        if r["at_risk"]:
            if r["is_service"]:
                print(
                    f"[FALLA ] {r['repo']} ({kind}) - .knowledge trackeado y un "
                    "remote de terceros: un push al upstream lo sube"
                )
            else:
                print(
                    f"[FALLA ] {r['repo']} ({kind}) - {len(r['tracked_knowledge'])} "
                    "archivos .knowledge TRACKEADOS: entran al diff de cualquier PR"
                )
        elif not r["hook"]:
            print(f"[FALTA ] {r['repo']} ({kind}) - sin guarda pre-push")
        elif not r["excluded"] and not r["is_service"]:
            print(f"[AVISO ] {r['repo']} - falta .knowledge/ en .git/info/exclude")
        else:
            print(f"[OK    ] {r['repo']} ({kind})")

    print()
    if problems:
        print("Problemas:")
        for p in problems:
            print(f"  - {p}")
        print()
        print("Arreglar con: scripts/check-foreign-knowledge.py --install")
        return 1

    print(f"OK: {len(results)} repo(s) de terceros sin .knowledge/ expuesto.")
    return 0


def _problems(results: List[dict]) -> List[str]:
    out: List[str] = []
    for r in results:
        if r["is_service"]:
            # En un servicio el .knowledge es deliberado; solo importa el push.
            if r["at_risk"]:
                out.append(
                    f"{r['repo']}: sin guarda pre-push y con remote de terceros "
                    "(.knowledge viajaria en un push al upstream)"
                )
            elif not r["hook"]:
                out.append(f"{r['repo']}: sin guarda pre-push")
            continue
        if r["tracked_knowledge"]:
            out.append(
                f"{r['repo']}: {len(r['tracked_knowledge'])} archivos .knowledge "
                "trackeados (viajarian en el diff de un PR)"
            )
        if not r["hook"]:
            out.append(f"{r['repo']}: sin guarda pre-push")
        if not r["excluded"]:
            out.append(f"{r['repo']}: .knowledge/ no esta en .git/info/exclude")
    return out


if __name__ == "__main__":
    sys.exit(main())
