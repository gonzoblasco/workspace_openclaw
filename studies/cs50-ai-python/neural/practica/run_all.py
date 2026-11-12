#!/usr/bin/env python3
"""Gate del Módulo 6 (Neural Networks): corre las cuatro prácticas."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PRACTICES = [
    ('p1_perceptron.py', 'el perceptrón no puede con XOR y no converge'),
    ('p2_activaciones.py', 'sin no-linealidad, N capas = 1 capa'),
    ('p3_backprop.py', 'el gradiente analítico coincide con el numérico'),
    ('p4_gradient_descent.py', 'batch y SGD gastan el mismo cómputo distinto'),
]


def main():
    failed = []
    for script, claim in PRACTICES:
        proc = subprocess.run([sys.executable, script], cwd=HERE,
                              capture_output=True, text=True)
        ok = proc.returncode == 0
        print(f'{"PASA" if ok else "FALLA":<6} {script:<28} {claim}')
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
