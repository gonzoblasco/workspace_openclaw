#!/usr/bin/env python3
"""
test_dash_copies.py - Las dos copias de check_em_dash.py no deben divergir.

Por que existe: el 2026-11-09 la decision del dueno retiro el veto del guion largo.
Se actualizaron las dos copias y quedaron distintas: la de agents/kanam-dev
seguia documentando "Exit 1 = encontro guiones largos", que ya no era cierto.
Dos fuentes de verdad para una regla que se acaba de retirar es como vuelve.

Este test compara el CONTENIDO, no solo el comportamiento: si alguien corrige
una copia y no la otra, falla aca y no tres semanas despues.

  python3 scripts/test_dash_copies.py

Exit 0 = identicas. Exit 1 = divergen. Exit 2 = falta una copia.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "scripts" / "check_em_dash.py"
COPIES = [ROOT / "agents" / "kanam-dev" / "scripts" / "check_em_dash.py"]


def main() -> int:
    if not CANONICAL.exists():
        print(f"[INFRA] falta la canonica: {CANONICAL}", file=sys.stderr)
        return 2

    reference = CANONICAL.read_text(encoding="utf-8")
    failures = 0

    for copy in COPIES:
        if not copy.exists():
            print(f"[INFRA] falta la copia: {copy}", file=sys.stderr)
            return 2
        if copy.read_text(encoding="utf-8") != reference:
            rel = copy.relative_to(ROOT)
            print(f"[DIVERGE] {rel} no coincide con scripts/check_em_dash.py")
            failures += 1
        else:
            print(f"[OK] {copy.relative_to(ROOT)} coincide con la canonica")

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
