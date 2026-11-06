#!/usr/bin/env python3
"""
docs_sync.py - Detecta donde la documentacion contradice la realidad medida (F1).

El problema que resuelve: un README que dice "156 tests" cuando hay 168, o un
DESIGN.md que declara un token que mide 1.40:1. El documento miente y no falla
nada. Este script mide y compara.

Que NO hace: no reescribe prosa. `--fix` solo toca numeros aislados que el
propio script puede volver a medir; cualquier otra reescritura exige `--force`
explicito y muestra el diff antes.

Extraccion (pura, con tests propios):
  - conteo de tests declarado en el doc
  - tokens de color `--nombre: #hex` en el doc vs el CSS
  - comandos `npm run x` / `node scripts/y` citados
  - rutas relativas citadas entre backticks

Exit codes:
  0  sin desalineaciones
  1  hay desalineaciones (las lista con archivo:linea, doc dice X, realidad es Y)
  2  no se pudo medir (no hay suite, no hay CSS, el archivo no existe)

Un 2 nunca es verde: si no se pudo medir, no se sabe.

Cero dependencias. Solo stdlib.

Uso:
    docs_sync.py <dir>                 # informe
    docs_sync.py <dir> --check         # exit 1 si hay drift (para el pipeline)
    docs_sync.py <dir> --json
    docs_sync.py <dir> --fix           # solo conteos, muestra el cambio
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

DOC_NAMES = ("README.md", "STATUS.md", "DESIGN.md", "HANDOFF.md", "ROADMAP.md")
DOC_GLOBS = ("docs/**/*.md", ".knowledge/**/*.md")


# ---------------------------------------------------------------------------
# Extractores puros. Cada uno devuelve lo que el doc DECLARA, con su linea.
# ---------------------------------------------------------------------------


@dataclass
class Claim:
    kind: str
    doc: str
    line: int
    declared: str
    raw: str


TEST_COUNT_RE = re.compile(
    r"\b(\d{1,5})\s+(?:tests?|pruebas?)\b|\b(?:tests?|pruebas?)\s*[:=]\s*(\d{1,5})\b",
    re.IGNORECASE,
)

TOKEN_RE = re.compile(r"(--[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,8})")

COMMAND_RE = re.compile(r"`((?:npm run|node scripts/|python3? scripts/|bash scripts/)[^`]+)`")

PATH_RE = re.compile(r"`((?:src|test|tests|scripts|docs|\.knowledge)/[^`\s]*)`")


# Lineas que mencionan un numero de tests pero NO declaran el total de la suite.
# Verificado sobre kanam-fixer, donde el extractor greedy produjo 8 falsos
# positivos: conteos por etapa ("Commit x. 7 tests."), conteos de otro producto
# ("llego con 102 tests") y deltas ("quedo 5 tests atras").
NOT_A_SUITE_CLAIM = re.compile(
    r"\b(commit\b|qued[oó]\b|atr[aá]s\b|atras\b|faltan\b|diferencia\b|se agregaron\b"
    r"|llego\b|lleg[oó]\b|nacio\b|murio\b|antes\b|era\b|suma\b|delta\b"
    # Conteos por etapa o por archivo: "7 tests, incluidos 3", "8 tests de
    # caracterizacion", "51 tests pasaban". Declaran un subconjunto, no el total.
    r"|incluid\w*|caracterizaci[oó]n|pasaban\b)",
    re.IGNORECASE,
)

# Un doc que dice explicitamente que mide otra cosa que el repo actual tampoco
# declara el total de la suite. `.knowledge/AUDIT.md` hace justamente eso.
_NOT_THIS_REPO = re.compile(r"\.knowledge/|otro producto|otro repo|a11y-fixer", re.IGNORECASE)


def extract_test_claims(doc_path: Path, text: str) -> list[Claim]:
    """Conteos de tests declarados en el doc.

    Se ignoran lineas que hablan de un archivo de test puntual ("1 test" al lado
    de `test_foo.py` no es un conteo de suite), de un conteo por etapa, de un
    delta o del total de otro producto. Un falso positivo aca hace que el doctor
    grite cuando el doc esta bien, y eso es tan malo como no medir.
    """
    claims: list[Claim] = []
    for i, line in enumerate(text.splitlines(), start=1):
        if "test_" in line or ".test." in line:
            continue
        if NOT_A_SUITE_CLAIM.search(line) or _NOT_THIS_REPO.search(line):
            continue
        for m in TEST_COUNT_RE.finditer(line):
            value = m.group(1) or m.group(2)
            if value:
                claims.append(Claim("test_count", doc_path.name, i, value, line.strip()))
    return claims


def extract_token_claims(doc_path: Path, text: str) -> list[Claim]:
    claims: list[Claim] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for m in TOKEN_RE.finditer(line):
            claims.append(Claim("token", doc_path.name, i, f"{m.group(1)}={m.group(2)}", line.strip()))
    return claims


def extract_command_claims(doc_path: Path, text: str) -> list[Claim]:
    claims: list[Claim] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for m in COMMAND_RE.finditer(line):
            claims.append(Claim("command", doc_path.name, i, m.group(1).strip(), line.strip()))
    return claims


def extract_path_claims(doc_path: Path, text: str) -> list[Claim]:
    claims: list[Claim] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for m in PATH_RE.finditer(line):
            claims.append(Claim("path", doc_path.name, i, m.group(1).strip(), line.strip()))
    return claims


# ---------------------------------------------------------------------------
# Medidores: la realidad. Cada uno devuelve (valor, error). error != None => exit 2.
# ---------------------------------------------------------------------------


def measure_test_count(repo: Path) -> tuple[int | None, str | None]:
    """Corre la suite y cuenta.

    Por que el conteo real y no un numero cacheado: el doc tiene que reflejar lo
    que pasa hoy, no lo que paso la ultima vez que alguien lo actualizo.
    """
    pkg = repo / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return None, f"package.json ilegible: {exc}"
        if "test" not in data.get("scripts", {}):
            return None, "no hay script de test en package.json"
        # Sin --silent: el flag de npm suprime justamente el resumen
        # "Tests N passed" que hay que leer. Verificado sobre kanam-fixer: con
        # --silent la salida no trae el conteo y el doctor queda ciego.
        proc = subprocess.run(
            ["npm", "test"], cwd=str(repo), capture_output=True, text=True
        )
        # vitest emite secuencias ANSI aun sin TTY: sin limpiarlas el regex
        # no matchea "Tests  22 passed" y el conteo queda ilegible.
        text = ANSI_RE.sub("", proc.stdout + proc.stderr)
        # vitest: "Tests  22 passed | 4 skipped (26)"
        m = re.search(r"Tests\s+(\d+)\s+passed(?:\s*\|\s*(\d+)\s+skipped)?(?:\s*\((\d+)\))?", text)
        if m:
            if m.group(3):
                return int(m.group(3)), None
            return int(m.group(1)) + int(m.group(2) or 0), None
        # node --test: "# pass 168"
        m = re.search(r"^#\s*pass\s+(\d+)", text, re.MULTILINE)
        if m:
            return int(m.group(1)), None
        if proc.returncode == 0:
            return None, "la suite paso pero no se pudo leer el conteo de la salida"
        return None, f"la suite fallo (exit {proc.returncode})"

    pyproject = repo / "pyproject.toml"
    if pyproject.exists():
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"], cwd=str(repo), capture_output=True, text=True
        )
        m = re.search(r"(\d+)\s+passed", ANSI_RE.sub("", proc.stdout + proc.stderr))
        if m:
            return int(m.group(1)), None
        return None, "pytest no reporto un conteo de tests pasados"

    return None, "no reconozco el stack para medir tests"


def measure_tokens(repo: Path) -> tuple[dict[str, str], str | None]:
    """Lee los tokens del CSS real. La fuente de verdad es el CSS, no el doc."""
    candidates = [repo / "src" / "ui" / "styles.css", repo / "src" / "styles.css"]
    for path in candidates:
        if path.exists():
            text = path.read_text(encoding="utf-8")
            return {m.group(1): m.group(2).lower() for m in TOKEN_RE.finditer(text)}, None
    css = list(repo.glob("**/*.css"))
    if not css:
        return {}, "no se encontro ningun CSS para comparar tokens"
    text = css[0].read_text(encoding="utf-8")
    return {m.group(1): m.group(2).lower() for m in TOKEN_RE.finditer(text)}, None


def measure_paths(repo: Path) -> tuple[set[str], str | None]:
    """Todo lo que existe: archivos Y directorios.

    Un doc que cita `docs/adr/` esta citando un directorio. Compararlo contra un
    set de archivos lo marca como roto cuando esta bien. Se incluyen los dos y se
    normaliza sin barra final.
    """
    out: set[str] = set()
    for p in repo.rglob("*"):
        if ".git" in p.parts:
            continue
        out.add(str(p.relative_to(repo)))
    return out, None


def measure_commands(repo: Path) -> tuple[dict[str, str], str | None]:
    pkg = repo / "package.json"
    scripts: dict[str, str] = {}
    if pkg.exists():
        try:
            scripts = json.loads(pkg.read_text(encoding="utf-8")).get("scripts", {})
        except (OSError, json.JSONDecodeError):
            return {}, "package.json ilegible"
    return scripts, None


# ---------------------------------------------------------------------------
# Comparacion: claim declarado vs realidad medida.
# ---------------------------------------------------------------------------


def compare(repo: Path, doc_files: list[Path]) -> tuple[list[dict], list[str]]:
    """Devuelve (drift, errores_de_medicion). Un error de medicion es exit 2."""
    drift: list[dict] = []
    errors: list[str] = []

    claims_by_kind: dict[str, list[Claim]] = {}
    for doc in doc_files:
        text = doc.read_text(encoding="utf-8")
        for claim in (
            extract_test_claims(doc, text)
            + extract_token_claims(doc, text)
            + extract_command_claims(doc, text)
            + extract_path_claims(doc, text)
        ):
            claims_by_kind.setdefault(claim.kind, []).append(claim)

    if claims_by_kind.get("test_count"):
        actual, err = measure_test_count(repo)
        if err:
            errors.append(f"test_count: {err}")
        elif actual is not None:
            for claim in claims_by_kind["test_count"]:
                if int(claim.declared) != actual:
                    drift.append(_entry(claim, str(actual)))

    if claims_by_kind.get("token"):
        actual_tokens, err = measure_tokens(repo)
        if err:
            errors.append(f"token: {err}")
        else:
            for claim in claims_by_kind["token"]:
                name, _, value = claim.declared.partition("=")
                real = actual_tokens.get(name)
                if real and real.lower() != value.lower():
                    drift.append(_entry(claim, real))

    if claims_by_kind.get("command"):
        scripts, err = measure_commands(repo)
        if err is None:
            for claim in claims_by_kind["command"]:
                m = re.match(r"npm run\s+(\S+)", claim.declared)
                if m and m.group(1) not in scripts:
                    drift.append(_entry(claim, "no existe ese script en package.json"))

    if claims_by_kind.get("path"):
        files, err = measure_paths(repo)
        if err is None:
            for claim in claims_by_kind["path"]:
                # Comparar sin la barra final: `docs/adr/` y `docs/adr` son el
                # mismo camino, y el doc cita el primero.
                declared = claim.declared.rstrip("/")
                if declared not in files:
                    drift.append(_entry(claim, "la ruta no existe en disco"))

    return drift, errors


def _entry(claim: Claim, actual: str) -> dict:
    d = asdict(claim)
    d["actual"] = actual
    return d


# ---------------------------------------------------------------------------
# Descubrimiento de docs.
# ---------------------------------------------------------------------------


def find_docs(repo: Path) -> list[Path]:
    found: list[Path] = []
    for name in DOC_NAMES:
        p = repo / name
        if p.exists():
            found.append(p)
    for pattern in DOC_GLOBS:
        found.extend(sorted(repo.glob(pattern)))
    # Unicos, preservando orden.
    seen: set[Path] = set()
    out: list[Path] = []
    for p in found:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="docs_sync.py",
        description="Compara lo que la documentacion declara contra lo que el repo mide.",
    )
    parser.add_argument("dir", nargs="?", default=".", help="repo a auditar")
    parser.add_argument("--check", action="store_true", help="exit 1 si hay drift")
    parser.add_argument("--json", action="store_true", help="salida JSON")
    parser.add_argument("--fix", action="store_true", help="corrige SOLO conteos de tests")
    args = parser.parse_args(argv)

    repo = Path(args.dir).resolve()
    if not repo.exists():
        print(f"[INFRA] no existe: {repo}", file=sys.stderr)
        return 2

    docs = find_docs(repo)
    if not docs:
        print(f"[INFRA] no hay documentos que auditar en {repo}", file=sys.stderr)
        return 2

    drift, errors = compare(repo, docs)

    if args.json:
        print(json.dumps({"drift": drift, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        print(f"docs-sync: {repo} ({len(docs)} documento/s)")
        if errors:
            print("")
            print("[INFRA] no se pudo medir:")
            for err in errors:
                print(f"  {err}")
        if drift:
            print("")
            print(f"[DRIFT] {len(drift)} desalineacion(es):")
            for d in drift:
                print(f"  {d['doc']}:{d['line']}  {d['kind']}")
                print(f"      doc dice: {d['declared']}")
                print(f"      realidad: {d['actual']}")
        if not drift and not errors:
            print("[OK] la documentacion coincide con lo medido")

    if args.fix:
        return _fix(repo, drift, docs)

    if errors:
        return 2
    return 1 if drift and args.check else 0


def _fix(repo: Path, drift: list[dict], docs: list[Path]) -> int:
    """Corrige SOLO conteos de tests. Cualquier otro drift es manual.

    Por que tan acotado: reescribir prosa automaticamente es como se rompe un
    documento que estaba bien. Un numero medido se puede reponer; una frase no.
    """
    counts = [d for d in drift if d["kind"] == "test_count"]
    if not counts:
        print("(nada que corregir automaticamente)")
        return 1 if drift else 0

    by_doc: dict[str, list[dict]] = {}
    for d in counts:
        by_doc.setdefault(d["doc"], []).append(d)

    for name, items in by_doc.items():
        path = next(p for p in docs if p.name == name)
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        for item in items:
            idx = item["line"] - 1
            if 0 <= idx < len(lines):
                lines[idx] = re.sub(
                    r"\b" + re.escape(item["declared"]) + r"\b",
                    item["actual"],
                    lines[idx],
                )
        path.write_text("".join(lines), encoding="utf-8")
        print(f"[FIX] {name}: {len(items)} conteo(s) actualizado(s)")

    remaining = [d for d in drift if d["kind"] != "test_count"]
    if remaining:
        print(f"[MANUAL] {len(remaining)} desalineacion(es) que el fix no toca (requieren decision)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
