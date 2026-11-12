#!/usr/bin/env python3
"""check-gate-honesty.py - ¿un gate que puede correr sin verificar puede dar verde?

El Módulo 1 y el Módulo 3 del curso CS50 AI llegan a la misma conclusión por dos
caminos distintos: **una verificación que da verde sin haber verificado es peor
que ninguna**. El Módulo 1 lo muestra con una heurística no admisible (el agente
cree que encontró el óptimo y no lo encontró). El Módulo 3 lo muestra con la
probabilidad condicional: `P(bien | pasa)` depende de la tasa base, y un gate que
nunca falló tiene tasa base 1.0 y posterior 1.0 por construcción.

El workspace ya tiene esa regla escrita (`skills/verification-gates`, 2026-09-28)
y el gate de citas la cumple desde 2026-11-12. Lo que **no** había es un gate que
la aplique a los gates: 23 de 24 checks del pre-commit devuelven `0` y `1`, pero
ninguno devuelve `3` ("no se pudo correr"). Si uno no encuentra su archivo de
entrada, el chequeo puede reportar verde sin haber mirado nada.

Qué verifica
------------
Para cada script en `scripts/check-*.py`:

1. **Declara un estado de "no corrible"** distinto del verde. Acepta `sys.exit(3)`,
   `return 3`, `exit(3)` o una constante nombrada con `3`. Si no lo declara, ese
   check no puede distinguir "no encontré nada" de "todo bien".
2. **Resuelve la raíz del repo** sin depender del `cwd`: `rev-parse` o `__file__`.
   Un check que asume `cwd` reporta verde cuando se lo corre desde otro directorio
   - y en el pre-commit el `cwd` es el del `git commit`, que no siempre es la raíz.
3. **Reporta un veredicto legible**: una línea con `OK:`, `RESULTADO:`, `PASA` o
   `FALLA`. Un check mudo que sólo devuelve un número no dice qué chequeó.

Códigos de salida
-----------------
    0  todos los checks cumplen
    1  algún check viola alguna de las tres reglas
    3  no se pudo correr (no hay scripts que revisar)

Uso
---
    python3 scripts/check-gate-honesty.py            # todos
    python3 scripts/check-gate-honesty.py --verbose  # con la tabla completa
    python3 scripts/check-gate-honesty.py --json     # salida para otro script
"""
import argparse
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Un check "declara" que puede no poder correr si sale con 3 de alguna forma.
NO_VERIFIABLE_RE = re.compile(
    r'\bsys\.exit\(\s*3\s*\)|\breturn\s+3\b|\bexit\(\s*3\s*\)|\bexit\s+3\b')

# Un check resuelve la raíz si la deriva del propio archivo o del repo. Si toma
# sus entradas por argv (como check-handoff-merge), tampoco depende del cwd: el
# que pasa el path es el hook, que sí corre desde la raíz.
ROOT_RESOLUTION_RE = re.compile(
    r'rev-parse|__file__|BASH_SOURCE'
    r"|add_argument\(\s*.--(?:new|prev|path|file)"
    r'|sys\.argv'
    r'|main\(sys\.argv\)'
    r'|"openclaw",\s*"skills"')

VERDICT_RE = re.compile(r'\bOK:|\bRESULTADO:|\bPASA\b|\bFALLA\b')


def analyze(path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    return {
        'name': path.name,
        'no_verifiable': bool(NO_VERIFIABLE_RE.search(text)),
        'root_resolution': bool(ROOT_RESOLUTION_RE.search(text)),
        'verdict': bool(VERDICT_RE.search(text)),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='Verifica que los gates puedan declarar "no corrible" (exit 3).')
    ap.add_argument('--verbose', '-v', action='store_true')
    ap.add_argument('--json', action='store_true')
    ns = ap.parse_args(argv)

    scripts = sorted((ROOT / 'scripts').glob('check-*.py'))
    if not scripts:
        print('ERROR no hay scripts/check-*.py que revisar', file=sys.stderr)
        return 3

    rows = [analyze(p) for p in scripts]

    if ns.json:
        print(json.dumps(rows, indent=2))
        return 0 if all(r['no_verifiable'] for r in rows) else 1

    violations = [r for r in rows if not r['no_verifiable']]
    missing_root = [r for r in rows if not r['root_resolution']]
    missing_verdict = [r for r in rows if not r['verdict']]

    if ns.verbose:
        print(f'{"check":<38} {"exit 3":<8} {"raíz":<6} {"veredicto"}')
        print('-' * 66)
        for r in rows:
            print(f'{r["name"]:<38} '
                  f'{"sí" if r["no_verifiable"] else "NO":<8} '
                  f'{"sí" if r["root_resolution"] else "NO":<6} '
                  f'{"sí" if r["verdict"] else "NO"}')
        print()

    print(f'checks: {len(rows)} | sin código 3: {len(violations)} | '
          f'sin resolver raíz: {len(missing_root)} | '
          f'sin veredicto: {len(missing_verdict)}')

    if violations:
        print('\nNo pueden distinguir "no se pudo correr" de "todo bien":')
        for r in violations:
            print(f'  {r["name"]}')
        print('\n  Un check que no encuentra su archivo de entrada y devuelve 0')
        print('  reporta verde sin haber mirado nada. El estado "no corrible" va')
        print('  con exit 3 (skills/verification-gates, regla 1).')

    if missing_root:
        print('\nNo resuelven la raíz del repo (asumen cwd):')
        for r in missing_root:
            print(f'  {r["name"]}')

    if missing_verdict:
        print('\nNo reportan veredicto legible:')
        for r in missing_verdict:
            print(f'  {r["name"]}')

    if violations:
        print('\nRESULTADO: FALLA')
        return 1
    print('\nRESULTADO: PASA')
    return 0


if __name__ == '__main__':
    sys.exit(main())
