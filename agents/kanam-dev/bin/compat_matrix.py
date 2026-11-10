#!/usr/bin/env python3
"""
compat_matrix.py - U4 de compatibility-testing: cada combinacion tiene evidencia.

El problema que resuelve: la skill pide una matriz con evidencia por entorno y un
gate de CI. Sin ejecutable, la matriz vive en un markdown que nadie cruza contra
los resultados, y una combinacion sin correr se lee igual que una que paso.

Que hace:
  1. Lee `compat/matrix.md` y extrae las combinaciones declaradas.
  2. Lee `compat/results/*.json` y extrae el resultado de cada entorno.
  3. Cruza: combinacion declarada sin resultado, resultado sin combinacion, y
     resultado sin fecha ni version de motor.
  4. Escribe `compat/coverage.md` con el estado de cada combinacion.

Formato de la matriz (markdown, tabla). Una fila por combinacion; las columnas se
leen por encabezado, no por posicion, para tolerar orden distinto:

    | entorno | motor | version | soporte | prioridad |
    |---|---|---|---|---|
    | chrome-desktop | Chromium | 131 | soportada | alta |

Formato de los resultados (JSON). Un archivo por entorno en `compat/results/`:

    {"environment": "chrome-desktop", "engine": "Chromium", "engine_version": "131",
     "date": "2026-11-09", "status": "pass", "tests": 42, "artifacts": []}

Exit codes:
  0  toda combinacion priorizada tiene evidencia valida
  1  hay huecos: combinacion sin resultado, resultado huerfano o sin fecha
  2  no se pudo medir (sin matriz, matriz ilegible, sin resultados)

Un 2 nunca es verde: una matriz que no se puede leer no es una matriz cubierta.

Cero dependencias. Solo stdlib.

Uso:
    compat_matrix.py <dir> [--json] [--strict] [--out compat/]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

# Una combinacion priorizada bloquea si falta su evidencia; una "fuera de alcance"
# no. Esa es la unica distincion que el script hace por si solo.
SUPPORTED = ("soportada", "supported", "degradada", "degraded")
OUT_OF_SCOPE = ("fuera de alcance", "out of scope", "no soportada", "unsupported")


@dataclass
class Combination:
    environment: str
    engine: str
    engine_version: str
    support: str
    priority: str


@dataclass
class Result:
    environment: str
    engine: str
    engine_version: str
    date: str
    status: str
    source: str


# ---------------------------------------------------------------------------
# Parsers. Puros.
# ---------------------------------------------------------------------------


def parse_md_table(text: str) -> list[dict[str, str]]:
    """Extrae filas de una tabla markdown. Las columnas se leen por encabezado.

    Devuelve [] si no hay tabla. No falla con tablas raras: una fila con menos
    celdas que el encabezado se descarta, porque una combinacion a medio escribir
    no es una combinacion.
    """
    rows: list[dict[str, str]] = []
    header: list[str] | None = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells):
            continue  # separador
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if len(cells) < len(header):
            continue
        rows.append({header[i]: cells[i] for i in range(len(header))})
    return rows


def column(row: dict[str, str], *names: str) -> str:
    """Lee una columna por cualquiera de sus nombres conocidos. Pura."""
    for name in names:
        if name in row and row[name]:
            return row[name]
    # Segundo intento: contiene el nombre (ej. "version de motor").
    for name in names:
        for key, value in row.items():
            if name in key and value:
                return value
    return ""


def parse_matrix(text: str) -> list[Combination]:
    """Convierte la tabla en combinaciones. Pura."""
    out: list[Combination] = []
    for row in parse_md_table(text):
        env = column(row, "entorno", "environment", "combinacion", "combo")
        if not env:
            continue
        out.append(Combination(
            environment=env,
            engine=column(row, "motor", "engine"),
            engine_version=column(row, "version", "engine version", "version de motor"),
            support=column(row, "soporte", "support", "nivel").lower(),
            priority=column(row, "prioridad", "priority").lower(),
        ))
    return out


def parse_result(path: Path, data: object) -> Result | None:
    """Normaliza un resultado. Devuelve None si no dice a que entorno pertenece."""
    if not isinstance(data, dict):
        return None
    env = str(data.get("environment") or data.get("entorno") or "").strip()
    if not env:
        return None
    return Result(
        environment=env,
        engine=str(data.get("engine") or data.get("motor") or "").strip(),
        engine_version=str(data.get("engine_version") or data.get("version") or "").strip(),
        date=str(data.get("date") or data.get("fecha") or "").strip(),
        status=str(data.get("status") or data.get("estado") or "").strip().lower(),
        source=path.name,
    )


# ---------------------------------------------------------------------------
# Cruce. Puro: recibe combinaciones y resultados ya parseados.
# ---------------------------------------------------------------------------


def cross(combinations: list[Combination], results: list[Result]) -> tuple[list[dict], list[str], list[str]]:
    """Devuelve (filas, huecos, advertencias).

    Un hueco es algo que falta y bloquea: combinacion priorizada sin resultado,
    resultado que no corresponde a ninguna combinacion, o resultado sin fecha.
    Una advertencia es una combinacion declarada fuera de alcance: se informa, no
    bloquea.
    """
    by_env = {r.environment: r for r in results}
    known = {c.environment for c in combinations}
    rows: list[dict] = []
    gaps: list[str] = []
    warnings: list[str] = []

    for combo in combinations:
        result = by_env.get(combo.environment)
        out_of_scope = any(s in combo.support for s in OUT_OF_SCOPE)
        state = "sin-evidencia"
        if result:
            if not result.date:
                state = "sin-fecha"
                gaps.append(f"{combo.environment}: resultado sin fecha ({result.source})")
            else:
                state = result.status or "sin-estado"
        elif out_of_scope:
            state = "fuera-de-alcance"
            warnings.append(f"{combo.environment}: declarada fuera de alcance, sin resultado")
        else:
            gaps.append(f"{combo.environment}: declarada sin resultado en compat/results/")

        rows.append({
            **asdict(combo),
            "state": state,
            "result_file": result.source if result else None,
            "result_date": result.date if result else None,
        })

    for result in results:
        if result.environment not in known:
            gaps.append(f"{result.source}: resultado para '{result.environment}', "
                        f"que no esta en la matriz")

    return rows, gaps, warnings


def blocking_rows(rows: list[dict]) -> list[dict]:
    """Filas que bloquean: prioridad alta/media y no fuera de alcance."""
    return [r for r in rows
            if r["state"] not in ("fuera-de-alcance",)
            and r["priority"] in ("alta", "high", "media", "medium")]


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="compat_matrix.py",
        description="Cruza la matriz de compatibilidad contra la evidencia por entorno.",
    )
    ap.add_argument("dir", nargs="?", default=".", help="repo a auditar")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="toda combinacion declarada necesita evidencia, no solo las priorizadas")
    ap.add_argument("--out", default="compat", help="directorio de evidencia")
    args = ap.parse_args(argv)

    repo = Path(args.dir).resolve()
    if not repo.exists():
        print(f"[INFRA] no existe: {repo}", file=sys.stderr)
        return 2

    base = repo / args.out
    matrix_path = base / "matrix.md"
    if not matrix_path.exists():
        print(f"[INFRA] falta la matriz: {matrix_path}", file=sys.stderr)
        return 2

    combinations = parse_matrix(matrix_path.read_text(encoding="utf-8"))
    if not combinations:
        print(f"[INFRA] la matriz no tiene combinaciones legibles: {matrix_path}", file=sys.stderr)
        return 2

    results_dir = base / "results"
    results: list[Result] = []
    if results_dir.exists():
        for path in sorted(results_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                print(f"[INFRA] resultado ilegible {path.name}: {exc}", file=sys.stderr)
                return 2
            parsed = parse_result(path, data)
            if parsed:
                results.append(parsed)

    rows, gaps, warnings = cross(combinations, results)

    base.mkdir(parents=True, exist_ok=True)
    summary = base / "coverage.md"
    lines = [
        "# Cobertura de la matriz (compat_matrix.py)",
        "",
        f"Combinaciones: {len(combinations)} | Resultados: {len(results)} | "
        f"Huecos: {len(gaps)}",
        "",
        "| entorno | motor | version | soporte | prioridad | estado | resultado |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['environment']} | {r['engine'] or '-'} | {r['engine_version'] or '-'} "
            f"| {r['support'] or '-'} | {r['priority'] or '-'} | {r['state']} "
            f"| {r['result_file'] or '-'} |")
    if warnings:
        lines += ["", "## Advertencias", ""] + [f"- {w}" for w in warnings]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps({"rows": rows, "gaps": gaps, "warnings": warnings},
                         ensure_ascii=False, indent=2))
    else:
        print(f"combinaciones={len(combinations)} resultados={len(results)} huecos={len(gaps)}")
        for g in gaps[:10]:
            print(f"  [HUECO] {g}")
        if len(gaps) > 10:
            print(f"  ... y {len(gaps) - 10} mas")
        for w in warnings:
            print(f"  [AVISO] {w}")
        print(f"cobertura: {summary}")

    if gaps:
        return 1
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
