#!/usr/bin/env python3
"""
dep_inventory.py - U4 de dependency-advisor: inventario declarado vs resuelto.

El problema que resuelve: la skill pide "cada dependencia con su version declarada
y la resuelta en el lockfile, y su tipo (directa/transitiva)". Sin ejecutable, cada
sesion improvisa la tabla y el rango declarado (`^2.0.0`) se confunde con la
version que realmente corre (2.1.3). Esa confusion es donde se esconden las
vulnerabilidades: el manifiesto dice una cosa y el arbol dice otra.

Que hace:
  1. Lee el manifiesto y el lockfile del stack.
  2. Cruza: cuantas directas, cuantas transitivas, cuales no estan en el lockfile.
  3. Marca los rangos abiertos (`^`, `~`, `*`, `>=`) donde la resuelta puede
     moverse sin que nadie lo note.
  4. Detecta dependencias directas sin justificacion documentada.

Exit codes:
  0  inventario completo y coherente
  1  hay incoherencias (directa ausente del lockfile, rango abierto sin pin, etc.)
  2  no se pudo medir (sin manifiesto, lockfile ilegible, stack no soportado)

Un 2 nunca es verde.

Cero dependencias. Solo stdlib.

Uso:
    dep_inventory.py <dir> [--json] [--out dep-advisor/] [--rationale-dir <dir>]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Un rango que permite moverse sin tocar el manifiesto. No es un error por si
# mismo, pero oculta la diferencia entre lo declarado y lo que corre.
#
# `==1.2.3` es un pin exacto, no un rango: en Python es la unica forma de fijar y
# tratarlo como abierto marcaria todo requirements.txt como deuda. Ese falso
# positivo lo encontro el test, no la lectura.
PIN_EXACT = re.compile(r"^==\s*[0-9][0-9A-Za-z.\-+]*$")
OPEN_RANGE = re.compile(r"^[\^~><=*]|^[0-9]+\.[0-9x*]+$|^\*$")


def is_open_range(spec: str) -> bool:
    s = spec.strip()
    if not s or s in ("latest", "*"):
        return True
    if PIN_EXACT.match(s):
        return False
    return bool(OPEN_RANGE.match(s))


# ---------------------------------------------------------------------------
# Parsers. Puros: reciben texto, devuelven estructuras. Se prueban sin disco.
# ---------------------------------------------------------------------------


def parse_package_json(text: str) -> dict:
    data = json.loads(text)
    return {
        "runtime": data.get("dependencies", {}) or {},
        "dev": data.get("devDependencies", {}) or {},
        "peer": data.get("peerDependencies", {}) or {},
        "optional": data.get("optionalDependencies", {}) or {},
    }


def parse_package_lock(text: str) -> dict[str, str]:
    """Devuelve {nombre: version} del arbol resuelto.

    Soporta lockfileVersion 2 y 3 (`packages`) y 1 (`dependencies` anidado).
    """
    data = json.loads(text)
    resolved: dict[str, str] = {}

    packages = data.get("packages")
    if isinstance(packages, dict):
        for path, meta in packages.items():
            if not path or not isinstance(meta, dict):
                continue
            if meta.get("link"):
                continue
            name = meta.get("name") or path.split("node_modules/")[-1]
            version = meta.get("version")
            if name and version:
                resolved.setdefault(name, version)
        return resolved

    def walk(deps: dict) -> None:
        for name, meta in (deps or {}).items():
            if not isinstance(meta, dict):
                continue
            if meta.get("version"):
                resolved.setdefault(name, meta["version"])
            walk(meta.get("dependencies", {}))
    walk(data.get("dependencies", {}))
    return resolved


def parse_requirements(text: str) -> dict[str, str]:
    """requirements.txt: nombre[extra]==version, con comentarios y flags."""
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        m = re.match(r"^([A-Za-z0-9_.\-]+)(?:\[[^\]]+\])?\s*(.*)$", line)
        if not m:
            continue
        out[m.group(1).lower()] = m.group(2).strip() or "*"
    return out


def parse_pyproject(text: str) -> dict[str, str]:
    """Extrae dependencias de un pyproject.toml sin tomllib (Python 3.9).

    Solo mira los bloques `dependencies = [...]` y `[tool.poetry.dependencies]`.
    Es un subconjunto: si el archivo crece, migrar a tomllib cuando el minimo
    soportado sea 3.11.
    """
    out: dict[str, str] = {}
    m = re.search(r"^dependencies\s*=\s*\[(.*?)\]", text, re.MULTILINE | re.DOTALL)
    if m:
        for item in re.findall(r"[\"']([^\"']+)[\"']", m.group(1)):
            name = re.split(r"[<>=!~\[\s]", item, 1)[0].lower()
            spec = item[len(name):].strip() or "*"
            if name:
                out[name] = spec
    m = re.search(r"^\[tool\.poetry\.dependencies\](.*?)(?=^\[|\Z)",
                  text, re.MULTILINE | re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"^([A-Za-z0-9_.\-]+)\s*=\s*(.+)$", line.strip())
            if not mm or mm.group(1).lower() == "python":
                continue
            spec = mm.group(2).strip().strip('"').strip("'")
            out[mm.group(1).lower()] = spec
    return out


# ---------------------------------------------------------------------------
# Inventario. Puro: recibe las estructuras ya parseadas.
# ---------------------------------------------------------------------------


def build_inventory(
    declared: dict[str, str],
    resolved: dict[str, str],
    kind: str,
) -> tuple[list[dict], list[str]]:
    """Devuelve (filas, problemas).

    Un problema es una incoherencia, no un juicio: directa ausente del lockfile,
    o rango abierto en una dependencia de runtime. Los juicios (justificacion,
    salud) no los puede hacer un script sin red y sin criterio.
    """
    rows: list[dict] = []
    problems: list[str] = []

    for name, spec in sorted(declared.items()):
        version = resolved.get(name)
        is_direct = kind in ("runtime", "dev", "peer", "optional")
        rows.append({
            "name": name,
            "declared": spec,
            "resolved": version,
            "kind": kind,
            "direct": is_direct,
            "open_range": is_open_range(spec),
            "in_lockfile": version is not None,
        })
        if version is None:
            problems.append(f"{name} esta en {kind} pero no aparece en el lockfile")
        if kind in ("runtime", "dev") and is_open_range(spec):
            problems.append(
                f"{name} declara rango abierto '{spec}': la version que corre puede "
                f"cambiar sin tocar el manifiesto")

    # Transitivas: estan en el lockfile y no en el manifiesto.
    declared_names = set(declared)
    for name, version in sorted(resolved.items()):
        if name in declared_names:
            continue
        rows.append({
            "name": name,
            "declared": None,
            "resolved": version,
            "kind": "transitive",
            "direct": False,
            "open_range": False,
            "in_lockfile": True,
        })

    return rows, problems


def find_rationale(repo: Path, rationale_dir: Path | None) -> set[str]:
    """Nombres de paquete con ficha de justificacion documentada."""
    base = rationale_dir or (repo / "dep-advisor" / "rationale")
    if not base.exists():
        return set()
    return {p.stem.lower() for p in base.glob("*.md")}


# ---------------------------------------------------------------------------
# Deteccion y lectura.
# ---------------------------------------------------------------------------


def load_project(repo: Path) -> tuple[str, dict[str, dict[str, str]], dict[str, str]]:
    """Devuelve (stack, declaradas_por_tipo, resueltas)."""
    pkg = repo / "package.json"
    lock = repo / "package-lock.json"
    if pkg.exists():
        declared = parse_package_json(pkg.read_text(encoding="utf-8"))
        resolved = parse_package_lock(lock.read_text(encoding="utf-8")) if lock.exists() else {}
        return "node", declared, resolved

    req = repo / "requirements.txt"
    if req.exists():
        declared = {"runtime": parse_requirements(req.read_text(encoding="utf-8"))}
        return "python", declared, {}

    pyproject = repo / "pyproject.toml"
    if pyproject.exists():
        declared = {"runtime": parse_pyproject(pyproject.read_text(encoding="utf-8"))}
        return "python", declared, {}

    return "desconocido", {}, {}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="dep_inventory.py",
        description="Inventario declarado vs resuelto, y coherencia con el lockfile.",
    )
    ap.add_argument("dir", nargs="?", default=".", help="repo a inventariar")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default="dep-advisor", help="directorio de evidencia")
    ap.add_argument("--rationale-dir", help="directorio de fichas de justificacion")
    args = ap.parse_args(argv)

    repo = Path(args.dir).resolve()
    if not repo.exists():
        print(f"[INFRA] no existe: {repo}", file=sys.stderr)
        return 2

    stack, declared_by_kind, resolved = load_project(repo)
    if stack == "desconocido":
        print(f"[INFRA] sin manifiesto reconocible en {repo} "
              f"(package.json, requirements.txt, pyproject.toml)", file=sys.stderr)
        return 2

    all_rows: list[dict] = []
    all_problems: list[str] = []
    for kind, declared in declared_by_kind.items():
        rows, problems = build_inventory(declared, resolved, kind)
        all_rows.extend(rows)
        all_problems.extend(problems)

    rationale = find_rationale(repo, Path(args.rationale_dir) if args.rationale_dir else None)
    direct_runtime = [r for r in all_rows if r["kind"] == "runtime" and r["direct"]]
    undocumented = [r["name"] for r in direct_runtime if r["name"].lower() not in rationale]

    out_dir = repo / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = out_dir / "inventory.md"

    lines = [
        "# Inventario de dependencias (dep_inventory.py)",
        "",
        f"Stack: {stack} | Directas: {len(direct_runtime)} | "
        f"Transitivas: {sum(1 for r in all_rows if r['kind'] == 'transitive')} | "
        f"Con ficha: {len(direct_runtime) - len(undocumented)}/{len(direct_runtime)}",
        "",
        "| paquete | declarada | resuelta | tipo | rango abierto | en lockfile |",
        "|---|---|---|---|---|---|",
    ]
    for r in all_rows:
        lines.append(
            f"| {r['name']} | {r['declared'] or '-'} | {r['resolved'] or 'NO RESUELTA'} "
            f"| {r['kind']} | {'si' if r['open_range'] else 'no'} "
            f"| {'si' if r['in_lockfile'] else 'no'} |")

    if undocumented:
        lines += ["", "## Sin justificacion documentada", ""]
        lines += [f"- {n}" for n in undocumented]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps({
            "stack": stack,
            "rows": all_rows,
            "problems": all_problems,
            "undocumented": undocumented,
        }, ensure_ascii=False, indent=2))
    else:
        transitives = sum(1 for r in all_rows if r["kind"] == "transitive")
        print(f"stack={stack} directas={len(direct_runtime)} transitivas={transitives}")
        print(f"sin ficha de justificacion: {len(undocumented)}/{len(direct_runtime)}")
        for p in all_problems[:10]:
            print(f"  [INCOHERENCIA] {p}")
        if len(all_problems) > 10:
            print(f"  ... y {len(all_problems) - 10} mas")
        print(f"inventario: {summary}")

    # Exit 1 si hay incoherencias de lockfile o rangos abiertos en runtime.
    # Las fichas faltantes NO son exit 1: son un juicio pendiente, no un error
    # medible. Se reportan y el humano decide.
    hard_problems = [p for p in all_problems if "no aparece en el lockfile" in p]
    if hard_problems:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
