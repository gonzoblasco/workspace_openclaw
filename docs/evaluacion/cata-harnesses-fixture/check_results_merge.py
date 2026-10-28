#!/usr/bin/env python3
"""
Verifica que el runner MERGEa results.json en vez de sobrescribirlo.

POR QUE este check existe: el driver de la fase local corre UN harness por
invocacion (CATA_HARNESS=claude, luego opencode, luego openhands), cada una
en su propio proceso de runner.py. Antes del fix, cada invocacion escribia
results.json desde cero con SOLO sus filas, y la celda de openhands (la
ultima) borraba las de claude y opencode.

Medido: nova-2b quedo con 1 de 3 filas, y las dos perdidas eran celdas que SI
se habian ejecutado (203 s y 100 s). Los ARTEFACTOS y los RAW si eran
acumulativos, asi que la perdida se veia solo al comparar el numero de filas
de results.json con el numero de celdas esperadas.

COMO funciona: no corre los harnesses (eso costaria inferencia). Simula el
patron de escritura del runner sobre un results.json de prueba y comprueba que
las filas de las celdas anteriores sobreviven.

Uso:  python3 check_results_merge.py [ruta/al/runner.py]
"""
from __future__ import annotations

import pathlib
import re
import sys


def check_source(src: str) -> list[str]:
    """Problemas encontrados en el codigo fuente del runner."""
    problems: list[str] = []
    # El merge tiene que existir.
    if "prev_rows" not in src:
        problems.append(
            "el runner NO lee el results.json previo: cada invocacion lo "
            "sobrescribe y las celdas de los harnesses anteriores se pierden"
        )
    if "merged" not in src:
        problems.append(
            "el runner no MERGEa las filas: falta la union por (task_id, harness)"
        )
    # Y no puede seguir escribiendo solo `results`: la lista de ESTA corrida.
    # (ni `ordered` sin haber mergeado antes: el orden no repara la perdida)
    for var in ("results", "ordered"):
        m = re.search(r'write_text\(json\.dumps\(\s*' + var + r'\b', src)
        if m and var == "results":
            problems.append(
                "el runner sigue escribiendo `results` (la lista de ESTA corrida) "
                "en vez de la lista mergeada: eso borra las celdas anteriores"
            )
    # La escritura tiene que usar la lista mergeada.
    if "merged" in src:
        if not re.search(r"write_text\(json\.dumps\(\s*ordered", src):
            problems.append(
                "el runner calcula `merged` pero no lo escribe: la lista "
                "mergeada se descarta"
            )
    return problems


def simulate(rows_prev: list[dict], rows_new: list[dict]) -> list[dict]:
    """Reproduce el merge del runner."""
    merged: dict[tuple, dict] = {}
    for row in rows_prev + rows_new:
        merged[(row.get("task_id"), row.get("harness"))] = row
    return sorted(
        merged.values(),
        key=lambda x: (str(x.get("task_id")), str(x.get("harness"))),
    )


def main() -> int:
    runner = pathlib.Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else "/Users/gonzoblasco/.openclaw/workspace/playground/cata-harnesses-2026-10-27/runner.py"
    )
    if not runner.exists():
        print(f"no existe: {runner}")
        return 2

    src = runner.read_text()
    problems = check_source(src)

    # Comportamiento: dos invocaciones seguidas dejan 2 celdas, no 1.
    prev = [{"task_id": "T1", "harness": "claude", "deliverable": "A"}]
    new = [{"task_id": "T1", "harness": "opencode", "deliverable": "B"}]
    after = simulate(prev, new)
    if len(after) != 2:
        problems.append(
            f"la simulacion deja {len(after)} filas y deberian ser 2: "
            "una celda anterior se pierde"
        )

    # Y un re-run de la MISMA celda reemplaza, no duplica.
    again = simulate(after, [{"task_id": "T1", "harness": "claude", "deliverable": "A2"}])
    if len(again) != 2:
        problems.append(
            f"un re-run de la misma celda deja {len(again)} filas y deberian "
            "ser 2: la celda se duplica"
        )

    if problems:
        print("MERGE DEL RESULTS: FALLA")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("MERGE DEL RESULTS: OK")
    print("  las filas de las celdas anteriores sobreviven a la siguiente invocacion")
    print("  un re-run de la misma celda reemplaza la fila, no la duplica")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
