#!/usr/bin/env python3
"""
build_assertions.py — Genera el `assertions.yaml` que consume `evidence-hunter`.

Consume la lista canónica de `cases.py` (fuente única de verdad) y emite
un YAML con un bloque `assertions:` que contiene, para cada caso, sólo
los dos campos que el hunter necesita:

  - description (lo que el autor ficticio declara)
  - source (ruta resuelta contra SANDBOX, no relativa)

El status esperado NO se emite: es metadata del laboratorio, no input
del hunter. El hunter no debe saber qué esperamos — eso es trampa
honesta.

Diseño:
  - Idempotente: corre `scaffold.main()` solo si la sandbox no existe.
  - Importa `cases` en vez de duplicar la lista.

Ejecución:
    python3 build_assertions.py > /tmp/assertions.yaml
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cases  # type: ignore  # noqa: E402
import scaffold  # type: ignore  # noqa: E402


def ensure_sandbox() -> Path:
    """Crea la sandbox si no existe. Devuelve la ruta absoluta."""
    if not scaffold.SANDBOX.exists():
        scaffold.main()
    return scaffold.SANDBOX


def render_yaml() -> str:
    sandbox = ensure_sandbox()
    lines: list[str] = ["assertions:"]
    for c in cases.CASES:
        # description multi-línea (YAML block scalar) — evita escapes.
        lines.append("  - description: |")
        for ln in c.description.splitlines() or [c.description]:
            lines.append(f"      {ln}")
        # source resuelto a ruta absoluta dentro del sandbox.
        abs_source = sandbox / c.source
        lines.append(f"    source: \"{abs_source}\"")
    return "\n".join(lines) + "\n"


def main() -> int:
    sys.stdout.write(render_yaml())
    return 0


if __name__ == "__main__":
    sys.exit(main())