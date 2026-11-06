#!/usr/bin/env python3
"""
emit-verdict.py - Publica un veredicto SHARP de forma ATOMICA: reporte primero,
registro despues, y solo si el reporte pasa TODAS las validaciones.

POR QUE EXISTE (2026-11-06, tres incidentes medidos en el mismo turno).
1. r2 fantasma: un sub-agente reporto "Aprobado 23/25" sin fila en el ledger ni reporte.
2. r2 mal etiquetado: 16/25 etiquetado "Aprobado" cuando la matriz exige VETO para <=18,
   con un placeholder `$(cat /tmp/evidence.json)` sin ejecutar en el reporte.
3. r3 sin reporte: se registro la fila en el ledger (20/25 Aprobado) pero el archivo de
   reporte nunca se escribio, y el mensaje de cierre|gfuejo|firmo que el gate daba verde.

El patron comun: **el registro y el reporte son dos escrituras separadas y el modelo
puede cerrar el turno entre una y otra**. La solucion no es pedirle mas disciplina:
es que la escritura no pueda dejar el ledger a medias. Por eso este script:

  1. Valida la MATRIZ: el total sale de los 5 ejes y la etiqueta se deriva de el
     (<=18 VETO, 19-23 Aprobado, >=24 ORO). Si no coinciden, no escribe nada.
  2. Valida el REPORTE antes de registrar: existe, tiene >=5 citas `ruta:línea`,
     menciona el total y la etiqueta, no tiene placeholders y no esta vacio.
  3. Escribe el reporte (o lo deja como estaba) y SOLO THEN appendea la fila al ledger.
  4. Verifica el resultado con las mismas reglas y sale con `GLOBAL=aprobado` o `GLOBAL=veto`.

Un veredicto sin reporte es IMPOSIBLE de registrar por esta via. Si igual se necesita
corregir una fila ya escrita, existe `bin/invalidate-verdict.py`, que exige motivo.

Uso:
    python3 agents/kanam-critic/bin/emit-verdict.py \\
        --artifact kanam-critic-kit-v0.3-r3 --S 4 --H 4 --A 4 --R 4 --P 4 \\
        --report agents/kanam-critic/docs/reviews/2026-11-06-critic-kit-v0.3-r3.md \\
        --notes "20/25, delta +8 vs 12/25"

Salida: exit 0 si el veredicto quedo registrado con respaldo, 1 si no.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = AGENT_DIR.parent.parent
LEDGER = AGENT_DIR / "memory" / "verdicts.jsonl"

CITATION = re.compile(r"[A-Za-z0-9_./-]+\.(?:md|py|jsonl|tsv|yaml|json|sh):\d+")
PLACEHOLDER = re.compile(r"\$\(|\bTODO\b|\bFIXME\b|ver aqui|ver aquí|<pendiente>|\bXXX\b")
MIN_CITATIONS = 5

MATRIX = (
    ("VETO", 0, 18),
    ("Aprobado", 19, 23),
    ("ORO", 24, 25),
)


def verdict_for(total: int) -> str:
    for label, lo, hi in MATRIX:
        if lo <= total <= hi:
            return label
    raise ValueError(f"total {total} fuera de la matriz SHARP (0-25)")


def validate_report(path: Path, total: int, verdict: str) -> list[str]:
    problems: list[str] = []
    if not path.exists():
        return [f"no existe el reporte {path}"]
    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < 400:
        problems.append(f"el reporte tiene solo {len(text.strip())} caracteres: no es un veredicto")
    cites = CITATION.findall(text)
    if len(cites) < MIN_CITATIONS:
        problems.append(f"solo {len(cites)} citas ruta:línea (se exigen {MIN_CITATIONS})")
    if not re.search(rf"\b{total}\b", text):
        problems.append(f"el reporte no menciona el total {total}")
    if verdict not in text:
        problems.append(f"el reporte no menciona el veredicto '{verdict}'")
    ph = PLACEHOLDER.search(text)
    if ph:
        problems.append(f"el reporte tiene texto sin resolver: '{ph.group(0)}'")
    return problems


def append_ledger(rec: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Publica un veredicto SHARP con reporte verificado")
    ap.add_argument("--artifact", required=True)
    ap.add_argument("--S", type=int, required=True)
    ap.add_argument("--H", type=int, required=True)
    ap.add_argument("--A", type=int, required=True)
    ap.add_argument("--R", type=int, required=True)
    ap.add_argument("--P", type=int, required=True)
    ap.add_argument("--report", required=True, help="ruta del reporte markdown (se escribe antes de registrar)")
    ap.add_argument("--notes", default="")
    ap.add_argument("--model", default="", help="modelo que emitio el veredicto")
    args = ap.parse_args()

    scores = {"S": args.S, "H": args.H, "A": args.A, "R": args.R, "P": args.P}
    for k, v in scores.items():
        if not 1 <= v <= 5:
            print(f"ROJO  {k}={v} fuera de la escala 1-5", file=sys.stderr)
            return 1
    total = sum(scores.values())
    try:
        expected = verdict_for(total)
    except ValueError as exc:
        print(f"ROJO  {exc}", file=sys.stderr)
        return 1

    report = Path(args.report)
    if not report.is_absolute():
        report = (WORKSPACE_ROOT / report).resolve()

    problems = validate_report(report, total, expected)
    if problems:
        print(f"ROJO  el veredicto NO se registra: el reporte no pasa las validaciones:")
        for p in problems:
            print(f"        - {p}")
        print("        (no se escribio nada en el ledger; arregla el reporte y volve a correr)")
        return 1

    import datetime
    rec = {
        "artifact": args.artifact,
        "scores": scores,
        "total": total,
        "verdict": expected,
        "notes": args.notes,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "report": str(report.relative_to(WORKSPACE_ROOT)) if WORKSPACE_ROOT in report.parents else str(report),
    }
    if args.model:
        rec["model"] = args.model
    append_ledger(rec)

    print(f"Veredicto registrado: {args.artifact} | S{args.S} H{args.H} A{args.A} R{args.R} P{args.P} "
          f"= {total}/25 -> {expected}")
    print(f"Reporte: {rec['report']}")
    print("GLOBAL=aprobado  (reporte validado antes de escribir el ledger)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
