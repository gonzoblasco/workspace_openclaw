#!/usr/bin/env python3
"""Práctica 3 — inferencia por enumeración: la respuesta exacta y su precio.

Pregunta: con la red lluvia -> mojado / resbalón, ¿cuál es P(R | W=T)?

Inferencia por enumeración es la respuesta EXACTA: se suman las probabilidades
de todos los mundos donde la evidencia se cumple, y se normaliza. Es también la
definición de la regla de Bayes, ejecutada sobre la conjunta.

Después se mide el costo: enumerar visita 2^n mundos, y con evidencia se
descarta la mayoría. La práctica 4 (sampling) hace lo mismo sin enumerar.
"""
import itertools
import sys

sys.path.insert(0, '.')
from p2_red_bayesiana import VARS, VALUES, joint_factorized


def enumerate_ask(query_var, evidence):
    """Devuelve la distribución de query_var dada la evidencia, y el trabajo hecho."""
    worlds = 0
    kept = 0
    dist = {v: 0.0 for v in VALUES}
    for combo in itertools.product(VALUES, repeat=len(VARS)):
        a = dict(zip(VARS, combo))
        worlds += 1
        if any(a[k] != v for k, v in evidence.items()):
            continue
        kept += 1
        dist[a[query_var]] += joint_factorized(a)
    z = sum(dist.values())        # normalización
    return {k: v / z for k, v in dist.items()}, worlds, kept


def main():
    evidence = {'W': 'T'}
    print(f'Pregunta: P(R | W={evidence["W"]})')
    print('  "me mojé; ¿llovió?"')
    print()

    dist, worlds, kept = enumerate_ask('R', evidence)
    print('=== La respuesta exacta ===\n')
    for v in VALUES:
        print(f'  P(R={v} | W=T) = {dist[v]:.4f}')
    print()
    print(f'  mundos enumerados: {worlds}')
    print(f'  mundos que sobreviven a la evidencia: {kept}')
    print(f'  fracción que se conserva: {kept / worlds:.0%}')
    print()

    print('=== Por qué no es 0.90 ===')
    print('  P(W=T | R=T) = 0.90, pero la pregunta es P(R=T | W=T).')
    print('  0.90 es "si llueve, me mojo casi seguro". La respuesta a "si me')
    print('  mojé, ¿llovió?" es distinta porque llover es raro (30%): la')
    print('  mayoría de las veces que te mojaste, no llovía.')
    print()

    # La misma cuenta con la otra evidencia: si llueve, P(W)
    dist2, _, _ = enumerate_ask('W', {'R': 'T'})
    print(f'  Contraste: P(W=T | R=T) = {dist2["T"]:.4f}')
    print(f'  Y P(R=T | W=T)         = {dist["T"]:.4f}')
    print('  Bayes invierte la condicional; no son el mismo número.')
    print()

    # --- el precio --------------------------------------------------------
    print('=== El precio: enumerar es exacto y no escala ===')
    print(f'  {"variables":<12} {"mundos 2^n":<16} {"sobreviven con 1 evidencia"}')
    for n in (3, 6, 10, 15, 20):
        # evidencia sobre la primera variable: sobrevive la mitad
        print(f'  {n:<12} {2 ** n:<16} {2 ** (n - 1)}')
    print()
    print('  Enumerar es exacto siempre, y con 20 variables son un millón de')
    print('  mundos por consulta. Con 30, mil millones. La práctica 4 va a')
    print('  cambiar exactitud por velocidad: eso es sampling.')

    print()
    ok = abs(dist['T'] + dist['F'] - 1.0) < 1e-9 and abs(dist["T"] - 0.6585) < 0.001
    print('RESULTADO: PASA' if ok else f'RESULTADO: FALLA (P(R=T|W=T)={dist["T"]:.4f})')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
