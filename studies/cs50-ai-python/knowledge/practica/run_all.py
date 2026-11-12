#!/usr/bin/env python3
"""Gate del Módulo 2 (Knowledge): corre las seis prácticas.

Cada práctica devuelve 0 si la propiedad que afirma se cumple. Si alguna falla,
el módulo no está aprendido — está leído.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PRACTICES = [
    ('p1_conectivos.py', 'las 5 tablas se generan y las 6 equivalencias se verifican'),
    ('p2_model_checking.py', 'entailment = verdad en todos los modelos de la KB'),
    ('p3_derivar.py', 'derivar y enumerar coinciden; la regla inválida no'),
    ('p4_resolution.py', 'resolución deriva la vacía solo cuando hay contradicción'),
    ('p5_hogwarts.py', 'primer orden comprime y la restricción muerde'),
    ('p6_workspace.py', 'una implicación no se lee al revés'),
]


def main():
    failed = []
    for script, claim in PRACTICES:
        proc = subprocess.run([sys.executable, script], cwd=HERE,
                              capture_output=True, text=True)
        ok = proc.returncode == 0
        print(f'{"PASA" if ok else "FALLA":<6} {script:<24} {claim}')
        if not ok:
            failed.append((script, proc.stdout[-600:], proc.stderr[-600:]))

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
