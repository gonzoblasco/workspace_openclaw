#!/usr/bin/env python3
"""
invalidate-verdict.py - Retira un veredicto del ledger dejando el motivo escrito.

POR QUE EXISTE (2026-11-06). Un veredicto mal emitido no se borra: se retira con
motivo. Borrar la fila seria reescribir la historia; dejarla sin marcar seria un
veredicto que sigue contando como vigente cuando ya no lo es.

Marca la fila con:
    "status": "invalidated"
    "invalidation_reason": "<por que>"

La fila sigue en el ledger (append-only en el sentido de que no se borra), pero
`bin/verify-verdict.py` la excluye del conteo de veredictos validos y exige que el
motivo este escrito.

Uso:
    python3 agents/kanam-critic/bin/invalidate-verdict.py --artifact kanam-critic-kit-v0.3-r2 \\
        --reason "16/25 etiquetado Aprobado: la matriz exige VETO para <=18"
Salida: exit 0 si se marco, 1 si no existe la fila.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LEDGER = Path(__file__).resolve().parent.parent / "memory" / "verdicts.jsonl"


def main() -> int:
    ap = argparse.ArgumentParser(description="Retira un veredicto con motivo escrito")
    ap.add_argument("--artifact", required=True)
    ap.add_argument("--reason", required=True)
    args = ap.parse_args()

    if not LEDGER.exists():
        print(f"ROJO  no existe {LEDGER}", file=sys.stderr)
        return 1

    lines, marked = [], 0
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("artifact") == args.artifact and rec.get("status") != "invalidated":
            rec["status"] = "invalidated"
            rec["invalidation_reason"] = args.reason
            marked += 1
        lines.append(json.dumps(rec, ensure_ascii=False))

    if not marked:
        print(f"ROJO  no hay fila vigente con artifact={args.artifact}", file=sys.stderr)
        return 1

    LEDGER.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Veredicto retirado: {args.artifact}")
    print(f"Motivo: {args.reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
