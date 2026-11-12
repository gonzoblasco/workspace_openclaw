#!/usr/bin/env python3
"""Gate del Módulo 3 (Uncertainty): corre las seis prácticas."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PRACTICES = [
    ('p1_probabilidad.py', 'tres identidades verificadas por simulación'),
    ('p2_red_bayesiana.py', 'la factorización coincide y ahorra exponencial'),
    ('p3_enumeracion.py', 'P(R|W) exacta y distinta de P(W|R)'),
    ('p4_sampling.py', 'likelihood weighting usa todas las muestras'),
    ('p5_hmm.py', 'el filtrado recursivo coincide con la fuerza bruta'),
    ('p6_gate_bayes.py', 'un verde no vale nada sin tasa base'),
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
