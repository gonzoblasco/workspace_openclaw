#!/usr/bin/env python3
"""Gate del Módulo 7 (Language): corre las cuatro prácticas."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PRACTICES = [
    ('p1_ngram.py', 'los n-gramas generan texto plausible y sin sentido'),
    ('p2_naive_bayes.py', 'bag of words + Bayes clasifica sin entender'),
    ('p3_secuencia.py', 'RNN es lineal y secuencial; attention, cuadrática y paralela'),
    ('p4_posicional.py', 'sin posición, el orden de las palabras se pierde'),
]


def main():
    failed = []
    for script, claim in PRACTICES:
        proc = subprocess.run([sys.executable, script], cwd=HERE,
                              capture_output=True, text=True)
        ok = proc.returncode == 0
        print(f'{"PASA" if ok else "FALLA":<6} {script:<26} {claim}')
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
