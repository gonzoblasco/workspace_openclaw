#!/usr/bin/env python3
"""Gate del Módulo 5 (Learning): corre las cinco prácticas."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PRACTICES = [
    ('p1_knn.py', 'la maldición crece con la dimensión'),
    ('p2_regresion.py', 'α no cambia el óptimo; el grado sí cambia el test'),
    ('p3_confusion.py', 'accuracy sola premia un clasificador que no detecta nada'),
    ('p4_heldout.py', 'medir sobre train da 1.0 y no dice si generaliza'),
    ('p5_qlearning.py', 'explorar y explotar se miden'),
]


def main():
    failed = []
    for script, claim in PRACTICES:
        proc = subprocess.run([sys.executable, script], cwd=HERE,
                              capture_output=True, text=True)
        ok = proc.returncode == 0
        print(f'{"PASA" if ok else "FALLA":<6} {script:<24} {claim}')
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
