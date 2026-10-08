#!/usr/bin/env python3
"""
validate.py — Compara la salida de `evidence-hunter` contra los esperados.

Para cada caso definido en `cases.py`, exige:
  1. Coincidencia EXACTA de `status` con `expected_status`.
  2. Que `evidence` exista y (si hay patrón definido) matchee el regex.

Si `evidence_pattern` es None, basta con que el campo exista y no sea
None (cita mínima).

Falsos verdes prevenidos:
  - Si el JSON no carga o `details` falta/viene vacío, devuelve
    `GLOBAL=bloqueado` con código 1.
  - Si el status coincide pero la cita no, marca `PASS` con flag `+` en
    la columna STATUS sólo cuando el patrón lo permite; en caso contrario
    imprime `CITAFALLA` en RESULT para distinguirlo del acierto total.
  - En el Caso 2 (parcial esperado), si el hunter devuelve `bloqueado`
    con cita `command not found`, lo distingue como `BLOCKED-NOT-PARTIAL`
    (pytest ausente) en lugar de un FAIL genérico.

Uso:
    python3 validate.py /tmp/evidence.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cases  # type: ignore  # noqa: E402


def load_evidence(path: Path) -> list[dict]:
    """Devuelve la lista `details` del JSON del hunter. Si falla, []."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    details = payload.get("details") if isinstance(payload, dict) else None
    return details if isinstance(details, list) else []


def evaluate() -> int:
    if len(sys.argv) < 2:
        print("validate.py <ruta a evidence.json>", file=sys.stderr)
        return 2

    evidence_path = Path(sys.argv[1]).expanduser().resolve()
    details = load_evidence(evidence_path)

    # --- Guarda de verde falso: si no hay detalles, no es verde. ---
    if not details:
        print("GLOBAL=bloqueado  (no se pudo cargar evidence.json)")
        return 1

    rows: list[list[str]] = []
    all_pass = True

    for case in cases.CASES:
        cid = case.id
        name = case.name
        exp_status = case.expected_status
        pattern = case.evidence_pattern

        if cid >= len(details):
            rows.append([name, exp_status, "—", "—", "MISSING"])
            all_pass = False
            continue

        d = details[cid]
        actual_status = d.get("status", "—")
        actual_evidence = d.get("evidence")  # puede ser None o ruta o texto

        # 1) Validar status
        status_ok = actual_status == exp_status

        # 2) Validar evidencia
        if pattern is None:
            # Cita mínima: debe existir y no ser None.
            cita_ok = actual_evidence is not None and actual_evidence != ""
        else:
            cita_ok = (
                actual_evidence is not None
                and re.search(pattern, str(actual_evidence)) is not None
            )

        # 3) Distinguir Caso 2: pytest ausente produce bloqueado, no parcial.
        result = "PASS"
        if not status_ok:
            # Caso especial: parcial esperado + bloqueado por pytest ausente.
            if (
                cid == 1
                and exp_status == "parcial"
                and actual_status == "bloqueado"
                and actual_evidence is not None
                and "command not found" in str(actual_evidence)
            ):
                result = "BLOCKED-NOT-PARTIAL"
            else:
                result = "FAIL"
        elif not cita_ok:
            result = "CITAFALLA"

        if result != "PASS":
            all_pass = False

        ev_short = (
            "—" if actual_evidence is None
            else (str(actual_evidence)[:40] + ("…" if len(str(actual_evidence)) > 40 else ""))
        )
        rows.append([name, exp_status, actual_status, ev_short, result])

    # --- Tabla final ---
    name_w = max(len(r[0]) for r in rows)
    print(f"{'CASO'.ljust(name_w)}  {'ESPERADO':<14}  {'HUNTER':<14}  {'CITA':<42}  RESULT")
    print("-" * (name_w + 2 + 14 + 2 + 14 + 2 + 42 + 2 + 18))
    for name, expected, actual, ev, result in rows:
        print(f"{name.ljust(name_w)}  {expected:<14}  {actual:<14}  {ev:<42}  {result}")

    print()
    if all_pass:
        print("GLOBAL=aprobado  (5/5 casos en estado y cita esperados)")
        return 0
    print("GLOBAL=veto      (al menos un caso NO coincide)")
    return 1


if __name__ == "__main__":
    sys.exit(evaluate())