#!/usr/bin/env python3
"""
Estado REAL de la fase local de la cata de harnesses, celda por celda.

Por que existe: el driver de la local corre UN harness por invocacion
(CATA_HARNESS=claude, luego opencode, luego openhands) y cada una es un proceso
distinto de runner.py. Antes del fix del merge, cada invocacion escribia
results.json desde cero con SOLO sus filas, y la ultima celda (openhands)
borra las de claude y opencode. Medido: nova-2b quedo con 1 de 3 filas, y las
dos perdidas eran celdas que SI se habian ejecutado (203 s y 100 s).

Ademas, el sello LOCAL-DONE se ponia sin comprobar que la medicion quedara
completa: un modelo con 0 entregables (todos los harnesses sin informe) queda
sellado igual, y su celdas se pierden en silencio.

Este script dice, por modelo local:
  - que harnesses tienen fila en results.json (con la TAREA pedida)
  - si hay entregable archivado
  - si el modelo necesita REMEDICION

Uso:  python3 scripts/cata-local-state.py [--json]
"""
from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any, Dict, List

OUT = pathlib.Path("/tmp/cata-harnesses")

# (modelo, slug). El slug es el nombre del directorio: tr ':/' -> '__'.
LOCALES = [
    ("nova-2b:latest", "hf.co_ModernoTech_nova-2b_latest"),
    ("ornith-1.5:9b", "ornith-1.5_9b"),
    ("gemma4:12b-mlx", "gemma4_12b-mlx"),
    ("qwen3.5:9b-mlx", "qwen3.5_9b-mlx"),
]
HARNESSES = ("claude", "opencode", "openhands")


def filas(slug: str) -> List[Dict[str, Any]]:
    p = OUT / slug / "results.json"
    if not p.exists():
        return []
    try:
        rows = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return []
    return rows if isinstance(rows, list) else []


def entregables(slug: str, tarea: str) -> Dict[str, int]:
    """harness -> bytes del entregable archivado."""
    out: Dict[str, int] = {}
    d = OUT / slug / "artefactos" / tarea
    if not d.exists():
        return out
    for h in HARNESSES:
        p = d / f"{h}.md"
        out[h] = p.stat().st_size if p.exists() else 0
    return out


def estado(tarea: str = "T1") -> List[Dict[str, Any]]:
    res: List[Dict[str, Any]] = []
    for modelo, slug in LOCALES:
        d = OUT / slug
        rows = [r for r in filas(slug) if r.get("task_id") == tarea]
        por_harness = {r.get("harness"): r for r in rows}
        arts = entregables(slug, tarea)
        sellado = (d / "LOCAL-DONE").exists()
        faltan = [h for h in HARNESSES if h not in por_harness]
        res.append(
            {
                "modelo": modelo,
                "slug": slug,
                "tarea": tarea,
                "filas": len(por_harness),
                "harnesses": sorted(por_harness.keys()),
                "faltan": faltan,
                "entregables": arts,
                "con_entregable": sum(1 for v in arts.values() if v > 0),
                "sellado": sellado,
                # Remediar = falta alguna celda en results.json. Un modelo con
                # 3 filas esta completo, tenga o no entregable (la ausencia de
                # entregable es un 0 legitimo, no un dato faltante).
                "necesita_remedicion": bool(faltan),
            }
        )
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--tarea", default="T1")
    a = ap.parse_args()

    st = estado(a.tarea)
    if a.json:
        print(json.dumps(st, indent=1, default=str))
        return 0

    print(f"{'MODELO':<18} {'FILAS':<7} {'ENTREGABLES':<13} {'FALTAN':<26} {'SELLO':<8} REMEDICION")
    remediar = []
    for e in st:
        print(
            f"{e['modelo']:<18} {e['filas']}/3     "
            f"{e['con_entregable']}/3          "
            f"{','.join(e['faltan']) or '-':<26} "
            f"{'si' if e['sellado'] else 'no':<8} "
            f"{'SI' if e['necesita_remedicion'] else 'no'}"
        )
        if e["necesita_remedicion"]:
            remediar.append(e["slug"])
    print()
    print(f"  a remediar: {', '.join(remediar) if remediar else 'ninguno'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
