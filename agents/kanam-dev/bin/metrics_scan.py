#!/usr/bin/env python3
"""
metrics_scan.py - U4 de code-metrics: medir, normalizar y comparar contra umbral.

El problema que resuelve: la skill `code-metrics` pide "correr la herramienta",
"normalizar a una tabla" y "marcar contra umbral". Sin ejecutable, eso depende de
que cada sesion improvise el formato y la comparacion. El resultado es un numero
suelto ("cobertura 65 %") que no dice si el proyecto esta sano.

Que hace, en una pasada:
  1. Detecta el stack del proyecto.
  2. Corre la herramienta de cobertura que exista, sin instalar nada.
  3. Normaliza el resultado a filas (metrica, valor, unidad, umbral, estado).
  4. Escribe el resumen y la salida cruda en `metrics/`.

Exit codes:
  0  todas las metricas medidas cumplen su umbral
  1  al menos una viola el umbral
  2  no se pudo medir (herramienta ausente, stack desconocido, suite roja)

Un 2 nunca es verde: si la cobertura no se pudo medir, no se sabe si cumple.

Cero dependencias. Solo stdlib.

Uso:
    metrics_scan.py <dir> [--threshold 80] [--json] [--out metrics/] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Row:
    metric: str
    value: float | None
    unit: str
    threshold: float | None
    status: str  # cumple | viola | sin-medir
    evidence: str


# ---------------------------------------------------------------------------
# Deteccion de stack y de la herramienta de cobertura disponible.
# ---------------------------------------------------------------------------


def detect_stack(repo: Path) -> tuple[str, str | None]:
    """Devuelve (stack, herramienta de cobertura). No instala nada."""
    pkg = repo / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return "node", None
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        # Vitest presente NO alcanza: --coverage exige @vitest/coverage-v8 aparte.
        # Verificado en preflight, donde vitest existe y el paquete de cobertura no,
        # y el runner sale con "MISSING DEPENDENCY: @vitest/coverage-v8".
        if "@vitest/coverage-v8" in deps:
            return "node", "vitest"
        if "c8" in deps:
            return "node", "c8"
        if "nyc" in deps:
            return "node", "nyc"
        return "node", None

    if (repo / "pyproject.toml").exists() or (repo / "setup.py").exists():
        try:
            proc = subprocess.run(
                [sys.executable, "-c", "import coverage; print('ok')"],
                capture_output=True, text=True,
            )
            return "python", "coverage" if proc.returncode == 0 else None
        except OSError:
            return "python", None

    return "desconocido", None


# ---------------------------------------------------------------------------
# Correr y parsear. El parseo es puro: se prueba sin toolchain.
# ---------------------------------------------------------------------------


def parse_coverage_total(text: str) -> tuple[float | None, str]:
    """Extrae el porcentaje total de cobertura de salidas conocidas. Pura.

    Soporta:
      - c8 / nyc:  "All files | 85.71 | ..."  (tabla)
      - vitest:    "Statements   : 85.71% ( ... )" o "All files | 85.71"
      - coverage:  "TOTAL  1234  567  85%"
    Devuelve (valor, razon_vacia_o_por_que_no).
    """
    clean = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text)

    # coverage.py: linea TOTAL con el porcentaje al final o en una columna.
    m = re.search(r"^TOTAL\s+.*?(\d{1,3}(?:\.\d+)?)%", clean, re.MULTILINE)
    if m:
        return float(m.group(1)), ""

    # c8/nyc tabla: "All files  |  85.71 |  80 | ..."
    m = re.search(r"^All files\s*\|\s*(\d{1,3}(?:\.\d+)?)", clean, re.MULTILINE)
    if m:
        return float(m.group(1)), ""

    # vitest: "Statements   : 85.71% ( 12/14 )"
    m = re.search(r"Statements\s*:\s*(\d{1,3}(?:\.\d+)?)%", clean)
    if m:
        return float(m.group(1)), ""

    # vitest sin tabla: "Coverage 85.71%"
    m = re.search(r"Coverage[^\d]{0,10}(\d{1,3}(?:\.\d+)?)%", clean, re.IGNORECASE)
    if m:
        return float(m.group(1)), ""

    return None, "la salida no trae un porcentaje de cobertura reconocible"


def build_row(stack: str, tool: str | None, value: float | None, run: dict) -> Row:
    """Arma la fila normalizada. Pura: no ejecuta nada."""
    if value is None:
        return Row(
            metric="coverage",
            value=None,
            unit="%",
            threshold=run.get("threshold"),
            status="sin-medir",
            evidence=run.get("reason", "sin medicion"),
        )
    threshold = run.get("threshold")
    status = "cumple"
    if threshold is not None and value < threshold:
        status = "viola"
    return Row(
        metric="coverage",
        value=value,
        unit="%",
        threshold=threshold,
        status=status,
        evidence=f"{tool} ({stack}) exit={run.get('exit')}",
    )


# ---------------------------------------------------------------------------
# Ejecucion.
# ---------------------------------------------------------------------------


def run_coverage(repo: Path, stack: str, tool: str, out_dir: Path) -> dict:
    """Corre la herramienta y guarda la salida cruda. Devuelve el crudo y el exit."""
    if stack == "node" and tool == "vitest":
        cmd = ["npx", "vitest", "run", "--coverage"]
    elif stack == "node" and tool == "c8":
        cmd = ["npx", "c8", "--reporter=text", "npm", "test"]
    elif stack == "node" and tool == "nyc":
        cmd = ["npx", "nyc", "--reporter=text", "npm", "test"]
    elif stack == "python" and tool == "coverage":
        cmd = [sys.executable, "-m", "coverage", "run", "-m", "pytest", "-q"]
    else:
        return {"exit": None, "raw": "", "reason": f"sin comando para {stack}/{tool}"}

    try:
        proc = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True)
    except OSError as exc:
        return {"exit": None, "raw": "", "reason": f"no se pudo ejecutar {cmd[0]}: {exc}"}

    raw = proc.stdout + proc.stderr
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "raw" ).mkdir(exist_ok=True)
    (out_dir / "raw" / f"{tool}-coverage.txt").write_text(raw, encoding="utf-8")

    if stack == "python" and tool == "coverage" and proc.returncode == 0:
        rep = subprocess.run(
            [sys.executable, "-m", "coverage", "report", "-m"],
            cwd=str(repo), capture_output=True, text=True,
        )
        raw += rep.stdout + rep.stderr

    return {"exit": proc.returncode, "raw": raw, "reason": ""}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="metrics_scan.py",
        description="Mide cobertura, la normaliza contra umbral y escribe la evidencia.",
    )
    ap.add_argument("dir", nargs="?", default=".", help="repo a medir")
    ap.add_argument("--threshold", type=float, default=80.0, help="umbral de cobertura en % (default 80)")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    ap.add_argument("--out", default="metrics", help="directorio de evidencia (default metrics/)")
    ap.add_argument("--dry-run", action="store_true", help="detecta stack y herramienta, no ejecuta")
    args = ap.parse_args(argv)

    repo = Path(args.dir).resolve()
    if not repo.exists():
        print(f"[INFRA] no existe: {repo}", file=sys.stderr)
        return 2

    stack, tool = detect_stack(repo)
    if stack == "desconocido":
        print(f"[INFRA] stack desconocido en {repo}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"stack: {stack} | herramienta: {tool or 'NINGUNA'}")
        if tool is None:
            print("[INFRA] no hay herramienta de cobertura instalada; no se puede medir")
            return 2
        return 0

    if tool is None:
        print(f"[INFRA] stack {stack} sin herramienta de cobertura instalada", file=sys.stderr)
        return 2

    out_dir = repo / args.out
    run = run_coverage(repo, stack, tool, out_dir)
    run["threshold"] = args.threshold

    if run.get("reason"):
        row = build_row(stack, tool, None, run)
    else:
        value, why = parse_coverage_total(run["raw"])
        run["reason"] = why
        row = build_row(stack, tool, value, run)

    # La suite roja explica por que no hay numero: casi todos los runners
    # suprimen el reporte de cobertura cuando un test falla.
    if row.status == "sin-medir" and run.get("exit") not in (0, None):
        raw = run.get("raw", "")
        missing = re.search(r"MISSING DEPENDENCY\s+(\S+)", raw)
        if missing:
            print(f"[INFRA] falta la dependencia de cobertura {missing.group(1)}; "
                  f"instalarla o medir con otra herramienta. No se sabe si cumple el umbral.",
                  file=sys.stderr)
        else:
            print(f"[INFRA] la suite salio con exit {run['exit']}: sin cobertura medible",
                  file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)
    summary = out_dir / "summary.md"
    lines = [
        "# Cobertura medica (metrics_scan.py)",
        "",
        f"Stack: {stack} | Herramienta: {tool} | Umbral: {args.threshold}%",
        "",
        "| metrica | valor | unidad | umbral | estado | evidencia |",
        "|---|---|---|---|---|---|",
        f"| {row.metric} | {row.value if row.value is not None else 'n/a'} | {row.unit} "
        f"| {row.threshold} | {row.status} | {row.evidence} |",
    ]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps({"row": asdict(row), "stack": stack, "tool": tool},
                         ensure_ascii=False, indent=2))
    else:
        print(f"stack={stack} tool={tool} umbral={args.threshold}%")
        print(f"{row.metric}: {row.value if row.value is not None else 'n/a'}{row.unit}"
              f" -> {row.status}")
        print(f"resumen: {summary}")

    if row.status == "sin-medir":
        return 2
    return 0 if row.status == "cumple" else 1


if __name__ == "__main__":
    sys.exit(main())
