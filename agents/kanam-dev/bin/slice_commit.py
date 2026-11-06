#!/usr/bin/env python3
"""
slice_commit.py - De working tree sucio a commits atomicos (F3).

Agrupa los archivos modificados por intencion, propone mensajes
`type(#issue): descripcion` en ingles y commitea en slices. Nunca pushea.

Por que existe: hoy cortar un arbol sucio en commits atomicos es 100% manual, y
es justo donde se cuelan datos locales (`.env`, `*.db`) porque `git add -A` no
pregunta.

Seguridad primero, en este orden:
  1. Si hay archivos peligrosos (`.env`, `*.db`, `.venv/`, `node_modules/`,
     claves, uploads), el script sale 1 y los lista. No commitea NADA.
  2. Dry run es el default. `--apply` es lo unico que escribe.
  3. Un archivo que no se puede clasificar cae en `chore` y se declara; no se
     omite en silencio.

Exit codes:
  0  plan valido (dry run) o commits aplicados
  1  hay archivos peligrosos, o no hay nada que commitear con --apply
  2  uso invalido, no es repo git, o error de git

Cero dependencias. Solo stdlib.

Uso:
    slice_commit.py <dir>                  # dry run: muestra el plan
    slice_commit.py <dir> --apply          # ejecuta los commits
    slice_commit.py <dir> --json           # plan en JSON
    slice_commit.py <dir> --apply --issue 42
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Datos locales intocables. Bloqueante, no advertencia.
# ---------------------------------------------------------------------------
# Se evalua por ruta, no por contenido: leer `.env` para decidir si es peligroso
# ya seria una fuga. La ruta alcanza.

DANGEROUS_PATTERNS = (
    re.compile(r"(^|/)\.env(\.|$)", re.IGNORECASE),
    re.compile(r"\.(db|sqlite|sqlite3)$", re.IGNORECASE),
    re.compile(r"(^|/)\.venv/"),
    re.compile(r"(^|/)node_modules/"),
    re.compile(r"(^|/)(id_rsa|id_ed25519)(\.pub)?$"),
    re.compile(r"\.(pem|key|p12|pfx)$", re.IGNORECASE),
    re.compile(r"(^|/)(credentials|secrets)\.(json|ya?ml|txt)$", re.IGNORECASE),
    re.compile(r"(^|/)uploads?/"),
)


def is_dangerous(path: str) -> bool:
    return any(p.search(path) for p in DANGEROUS_PATTERNS)


# ---------------------------------------------------------------------------
# Clasificacion por intencion (funcion pura).
# ---------------------------------------------------------------------------
# El orden importa: docs y test ganan sobre el tipo de codigo, porque un cambio
# en un README es docs aunque el repo sea de codigo. Donde no hay senal, `chore`
# es el default declarado, no un cajon silencioso.

CLASS_RULES: list[tuple[str, re.Pattern]] = [
    ("docs", re.compile(r"(^|/)(docs?|\.knowledge)/|\.(md|mdx|rst|txt)$|(^|/)README|CHANGELOG|ADR", re.IGNORECASE)),
    ("test", re.compile(r"(^|/)tests?/|(^|/)test_[^/]*\.py$|\.(test|spec)\.[jt]sx?$", re.IGNORECASE)),
    ("ci", re.compile(r"(^|/)\.github/|(^|/)\.gitlab-ci|(^|/)Dockerfile|(^|/)docker-compose", re.IGNORECASE)),
    ("chore", re.compile(r"(^|/)(package(-lock)?\.json|tsconfig\.json|\.gitignore|\.editorconfig|biome\.json|eslint)", re.IGNORECASE)),
]


def classify(path: str) -> tuple[str, str]:
    """Devuelve (tipo_de_commit, razon). Pura.

    `feat` vs `fix` no se puede saber por ruta: depende de la intencion del
    cambio. Por eso el default de codigo es `fix` solo si el archivo ya existia
    en HEAD (modificacion) y `feat` si es nuevo. Es una heuristica declarada, no
    una adivinanza: la razon viaja al plan para que se pueda corregir a mano.
    """
    for kind, pattern in CLASS_RULES:
        if pattern.search(path):
            return kind, f"ruta matchea regla {kind}"
    return "code", "codigo: se resuelve feat/fix por estado en HEAD"


def code_type(path: str, repo: Path) -> tuple[str, str]:
    """Distingue archivo nuevo (feat) de modificado (fix), mirando HEAD."""
    proc = subprocess.run(
        ["git", "-C", str(repo), "ls-tree", "-r", "--name-only", "HEAD", "--", path],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return "chore", "no se pudo leer HEAD; default chore declarado"
    if proc.stdout.strip():
        return "fix", "archivo existe en HEAD: cambio de codigo existente"
    return "feat", "archivo nuevo en HEAD: se declara feat"


# ---------------------------------------------------------------------------
# Lectura del working tree.
# ---------------------------------------------------------------------------


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def changed_files(repo: Path) -> list[str]:
    """Archivos con cambios staged o unstaged (sin untracked ignorados)."""
    proc = git(repo, "status", "--porcelain")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git status fallo")
    out: list[str] = []
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        if path:
            out.append(path.strip('"'))
    return out


def plan(repo: Path, issue: str | None) -> tuple[list[dict], list[str]]:
    """Construye el plan de commits. Devuelve (plan, peligrosos)."""
    files = changed_files(repo)
    dangerous = [f for f in files if is_dangerous(f)]
    if dangerous:
        return [], dangerous

    buckets: dict[str, list[str]] = {}
    reasons: dict[str, str] = {}
    for path in files:
        kind, reason = classify(path)
        if kind == "code":
            kind, reason = code_type(path, repo)
        buckets.setdefault(kind, []).append(path)
        reasons.setdefault(kind, reason)

    order = ["feat", "fix", "test", "docs", "ci", "chore"]
    commits: list[dict] = []
    for kind in order:
        paths = buckets.get(kind)
        if not paths:
            continue
        scope = _scope_of(paths)
        head = f"{kind}({scope})" if scope else kind
        desc = _describe(kind, paths)
        suffix = f" (#{issue})" if issue else ""
        commits.append({
            "type": kind,
            "files": sorted(paths),
            "message": f"{head}: {desc}{suffix}",
            "reason": reasons.get(kind, ""),
        })
    return commits, []


def _scope_of(paths: list[str]) -> str:
    """Un scope corto derivado del denominador comun. Vacio si no hay uno claro."""
    if len(paths) == 1:
        p = paths[0]
        parts = p.split("/")
        if "src" in parts:
            i = parts.index("src")
            if len(parts) > i + 1:
                return parts[i + 1]
        return Path(p).stem
    parents = {str(Path(p).parent) for p in paths}
    if len(parents) == 1:
        parts = parents.pop().split("/")
        return parts[-1] if parts[-1] not in ("", ".") else ""
    return ""


def _describe(kind: str, paths: list[str]) -> str:
    n = len(paths)
    nouns = {
        "feat": "add", "fix": "correct", "test": "cover",
        "docs": "document", "ci": "wire", "chore": "update",
    }
    verb = nouns.get(kind, "update")
    if n == 1:
        return f"{verb} {Path(paths[0]).stem.replace('_', ' ').replace('-', ' ')}"
    return f"{verb} {n} files"


# ---------------------------------------------------------------------------
# Ejecucion.
# ---------------------------------------------------------------------------


def apply_plan(repo: Path, commits: list[dict]) -> int:
    for commit in commits:
        add = git(repo, "add", "--", *commit["files"])
        if add.returncode != 0:
            print(f"[INFRA] git add fallo: {add.stderr.strip()}", file=sys.stderr)
            return 2
        com = git(repo, "commit", "-m", commit["message"])
        if com.returncode != 0:
            print(f"[INFRA] git commit fallo: {com.stderr.strip()}", file=sys.stderr)
            return 2
        print(f"[OK] {commit['message']}  ({len(commit['files'])} archivo/s)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="slice_commit.py",
        description="Convierte un working tree sucio en commits atomicos. Dry run por defecto.",
    )
    parser.add_argument("dir", nargs="?", default=".", help="repo git")
    parser.add_argument("--apply", action="store_true", help="ejecuta los commits (default: dry run)")
    parser.add_argument("--json", action="store_true", help="plan en JSON")
    parser.add_argument("--issue", help="numero de issue para el sufijo (#N)")
    args = parser.parse_args(argv)

    repo = Path(args.dir).resolve()
    if not (repo / ".git").exists():
        print(f"[INFRA] no es un repo git: {repo}", file=sys.stderr)
        return 2

    try:
        commits, dangerous = plan(repo, args.issue)
    except RuntimeError as exc:
        print(f"[INFRA] {exc}", file=sys.stderr)
        return 2

    if dangerous:
        print("[BLOQUEA] archivos locales peligrosos en el arbol. No se commitea nada:", file=sys.stderr)
        for path in dangerous:
            print(f"  {path}", file=sys.stderr)
        print("Respalda y saca esos archivos del arbol antes de volver a intentar.", file=sys.stderr)
        return 1

    if not commits:
        print("[INFO] no hay cambios para commitear")
        return 0

    if args.json:
        print(json.dumps(commits, ensure_ascii=False, indent=2))
    else:
        print(f"plan: {len(commits)} commit(s) en {repo}")
        for commit in commits:
            print(f"  [{commit['type']}] {commit['message']}")
            for path in commit["files"]:
                print(f"      {path}")

    if not args.apply:
        print("(dry run: nada escrito. Usa --apply para ejecutar)")
        return 0

    return apply_plan(repo, commits)


if __name__ == "__main__":
    sys.exit(main())
