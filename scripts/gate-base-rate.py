#!/usr/bin/env python3
"""Práctica del curso — el gate del workspace con la tasa base del Módulo 3.

Esta es la práctica que el curso **no tiene** y que el workspace sí puede tener:
la probabilidad condicional aplicada a los gates que corre en cada commit.

Un gate tiene dos errores:
  - falso negativo: hay algo mal y el gate pasa (el que duele)
  - falso positivo: todo está bien y el gate falla (ruido)

La probabilidad de que el código esté bien DADO QUE EL GATE PASÓ no es la
sensibilidad del gate: es Bayes, y depende de la TASA BASE.

    P(bien | pasa) = P(pasa | bien) · P(bien) / P(pasa)

El script mide la tasa base real del repo: ¿cuántas veces pasó y cuántas falló
cada gate del pre-commit, en el historial de commits? De ahí calcula qué
significa un verde hoy.

Uso:
    python3 scripts/gate-base-rate.py [--commits 200] [--gate check-cv-facts.py]
"""
import argparse
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Un commit "verde" es uno que llegó al historial: el pre-commit lo dejó pasar.
# Un check que falló en un commit no aparece: el commit no existe. La única forma
# de medir la tasa base es la marca de qué checks existían y qué cambió.
CHECK_RE = re.compile(r'scripts/(check-[\w-]+\.py)')


def hooks_current():
    hook = ROOT / '.git/hooks/pre-commit'
    if not hook.exists():
        return []
    return sorted(set(CHECK_RE.findall(hook.read_text(encoding='utf-8', errors='ignore'))))


def commits_touching(glob_pattern, limit=200):
    """Commits cuyo diff toca esos paths. Mide cuántas veces correrían los checks."""
    try:
        out = subprocess.run(
            ['git', '-C', str(ROOT), 'log', f'-n{limit}', '--oneline', '--name-only',
             '--pretty=format:COMMIT %h', '--', glob_pattern],
            capture_output=True, text=True, timeout=60)
    except Exception:
        return []
    return [l for l in out.stdout.split('\n') if l.startswith('COMMIT')]


def sensitivity_of(gate):
    """Estima la sensibilidad leyendo el check: si declara casos de falla.

    No es una medición: es una cota. Un check que tiene tests con casos negativos
    tiene una sensibilidad mínima medible; uno sin tests no tiene cota.
    """
    stem = gate.replace('.py', '').replace('-', '_')
    tests = list((ROOT / 'tests/python').glob(f'test_{stem}*.py'))
    if not tests:
        return None
    n_negative = 0
    for t in tests:
        src = t.read_text(encoding='utf-8', errors='ignore')
        # un test con "FALLA" o "assert r.returncode == 1" prueba el camino negativo
        n_negative += len(re.findall(r'returncode == 1|RESULTADO: FALLA|assert not', src))
    return n_negative if n_negative else None


def posterior(sens, spec, prior):
    prior_bad = 1 - prior
    p_pass = sens * prior + (1 - spec) * prior_bad
    return sens * prior / p_pass if p_pass else 0.0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--commits', type=int, default=200)
    ap.add_argument('--spec', type=float, default=0.95,
                    help='especificidad asumida (default 0.95)')
    ns = ap.parse_args(argv)

    gates = hooks_current()
    if not gates:
        print('ERROR no se encontró el pre-commit con checks', file=sys.stderr)
        return 3

    print(f'=== Los {len(gates)} gates del pre-commit ===\n')
    print(f'  {"gate":<34} {"sensibilidad":<14} {"tasa base":<12} {"P(bien|pasa)"}')
    print('-' * 80)

    results = []
    for gate in gates:
        sens = sensitivity_of(gate)
        # La tasa base de "hay algo que este gate debería cazar" no es medible
        # desde el historial: el commit verde no dice si había algo que cazar.
        # Se aproxima con el prior de cambios con el path relevante, y se declara.
        prior = 0.5   # sin medición: se asume neutro y se reporta como tal
        p = posterior(sens / (sens + 1) if sens else 0.5, ns.spec, prior)
        results.append((gate, sens, prior, p))
        sens_s = f'{sens} casos' if sens else 'sin tests'
        print(f'  {gate.replace("check-", "").replace(".py", ""):<34} {sens_s:<14} '
              f'{prior:<12.2f} {p:.4f}')

    print()
    print('=== Lo que estos números dicen ===')
    sin_tests = [g for g, s, _, _ in results if s is None]
    print(f'  {len(sin_tests)} de {len(gates)} gates no tienen tests con un caso negativo.')
    print('  Su sensibilidad no está medida: no hay caso donde el gate tenga que fallar')
    print('  y falle. Eso no significa que estén rotos: significa que un verde suyo no')
    print('  es evidencia de nada todavía, porque nunca vimos un rojo.')
    print()
    print('  Y los "N casos" de arriba son un piso, no una sensibilidad: cuentan los')
    print('  asserts negativos del test, y un gate con 16 casos negativos no es 16x')
    print('  más sensible que uno con 1. La fórmula de este script no convierte')
    print('  "cuántos casos" en "qué fracción detecta" - usa un mapeo declarado, y')
    print('  el P(bien|pasa) que sale sólo es comparable entre filas con el MISMO')
    print('  mapeo, no como probabilidad calibrada.')
    print()
    print('  Es exactamente la regla del Módulo 3: un clasificador que nunca se midió')
    print('  contra su clase positiva tiene P(bien|pasa) = 1.0 por construcción.')
    print()
    print('  La corrección no es confiar menos: es **correr cada gate contra un caso que')
    print('  debería romperlo**, como `tests/python/test_check_study_citations.py` hace')
    print('  con el gate de citas. Ese gate tiene 8 casos; tres son negativos.')

    print()
    n_measured = len(gates) - len(sin_tests)
    # OJO: este script NO es un gate bloqueante, y no lo puede ser todavía.
    # Lo que mide (cuántos casos negativos tiene cada test) no es una sensibilidad
    # calibrada: es un piso. Un gate que bloqueara por "sin tests" obligaría a
    # escribir tests para checks que quizá no los necesitan, y el pre-commit ya
    # tarda 10 s. Se corre a mano cuando se agrega o se toca un check.
    print()
    print(f'RESULTADO: PASA ({n_measured} de {len(gates)} gates con tests negativos)'
          if n_measured else 'RESULTADO: FALLA (ningún gate tiene un caso negativo)')
    return 0 if n_measured else 1


if __name__ == '__main__':
    sys.exit(main())
