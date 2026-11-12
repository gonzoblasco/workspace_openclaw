#!/usr/bin/env python3
"""Corre las 6 prácticas del Módulo 1 y resume el resultado de cada una.

Cada práctica es autocontenida y devuelve 0 si la propiedad que afirma se
cumple. `run_all.py` es el gate del módulo: si alguna falla, el módulo no está
aprendido — está leído.

Uso:
    python3 run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PRACTICES = [
    ('p1_frontier.py', 'la estructura de la frontier decide el algoritmo'),
    ('p2_consistencia.py', 'admisible != consistente, y la diferencia se mide'),
    ('p3_adversarial.py', 'un mapa adversarial se genera por propiedad, no se dibuja'),
    ('p4_costos.py', 'BFS deja de ser óptimo con costos distintos'),
    ('p5_agente.py', 'la heurística no admisible cambia el plan, no la velocidad'),
    ('p6_minimax.py', 'alpha-beta poda sin cambiar el valor de la raíz'),
    ('p7_reapertura.py', 'admisibilidad sin consistencia obliga a reabrir'),
]


def main():
    failed = []
    for script, claim in PRACTICES:
        proc = subprocess.run([sys.executable, str(HERE / script)],
                              capture_output=True, text=True)
        ok = proc.returncode == 0
        mark = 'PASA' if ok else 'FALLA'
        print(f'{mark:<6} {script:<22} {claim}')
        if not ok:
            failed.append((script, proc.stdout[-500:], proc.stderr[-500:]))

    print()
    if failed:
        for script, out, err in failed:
            print(f'--- {script} ---')
            print(out or err)
        print(f'RESULTADO: FALLA ({len(failed)} de {len(PRACTICES)})')
        return 1
    print(f'RESULTADO: PASA ({len(PRACTICES)} de {len(PRACTICES)})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
