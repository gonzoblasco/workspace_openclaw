#!/usr/bin/env python3
"""Gate del Módulo 4 (Optimization): corre las cinco prácticas."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PRACTICES = [
    ('p1_hill_climbing.py', 'hill climbing queda atrapado la mayoría de las veces'),
    ('p2_annealing.py', 'aceptar lo peor a propósito llega más al global'),
    ('p3_lineal.py', 'el óptimo de un programa lineal está en un vértice'),
    ('p4_csp.py', 'forward checking gana solo cuando hay ramas muertas'),
    ('p5_camino_vs_resultado.py', 'camino y resultado no son la misma pregunta'),
]


def main():
    failed = []
    for script, claim in PRACTICES:
        proc = subprocess.run([sys.executable, script], cwd=HERE,
                              capture_output=True, text=True)
        ok = proc.returncode == 0
        print(f'{"PASA" if ok else "FALLA":<6} {script:<30} {claim}')
        if not ok:
            failed.append((script, proc.stdout[-700:], proc.stderr[-700:]))
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
