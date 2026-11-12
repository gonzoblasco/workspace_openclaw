#!/usr/bin/env python3
"""Práctica 1 — los cinco conectivos y las leyes que se derivan de sus tablas.

Todo lo demás del módulo (model checking, inferencia, resolution) se apoya en
una sola cosa: saber exactamente qué significa cada conectivo. Si la tabla de
`→` se entiende mal, todo lo que sigue es fe.

Este script:
  1. GENERA las cinco tablas de verdad en vez de imprimirlas de memoria.
  2. Verifica las tres equivalencias que más se confunden, comparando tablas.
  3. Muestra el caso de la implicación con antecedente falso, que es el que
     rompe la intuición de todo el mundo.

Uso:
    python3 p1_conectivos.py
"""
import itertools
import sys


def truth_table(fn, n=2):
    """Devuelve las filas (asignación, valor) del conectivo."""
    symbols = ['P', 'Q'][:n]
    rows = []
    for values in itertools.product([False, True], repeat=n):
        env = dict(zip(symbols, values))
        rows.append((values, fn(*values)))
    return rows


def show(name, fn, n=2):
    rows = truth_table(fn, n)
    header = ' '.join(['P', 'Q'][:n]) + ' | ' + name
    print(f'  {header}')
    for values, val in rows:
        left = ' '.join('T' if v else 'F' for v in values)
        print(f'  {left} | {"T" if val else "F"}')
    print()


def equivalent(name, f, g, n=2):
    """Dos fórmulas son equivalentes si sus tablas coinciden fila por fila."""
    ok = all(a == b for (_, a), (_, b) in zip(truth_table(f, n), truth_table(g, n)))
    print(f'  {"OK  " if ok else "FALLA"} {name}')
    return ok


def main():
    print('=== 1. Las cinco tablas, generadas ===\n')
    show('not P', lambda p, q: not p)
    show('P and Q', lambda p, q: p and q)
    show('P or Q', lambda p, q: p or q)
    show('P -> Q', lambda p, q: (not p) or q)      # la definición, no una tabla copiada
    show('P <-> Q', lambda p, q: p == q)
    print('  (la tabla de -> sale de la definición "no P, o Q": no está copiada)')

    print('=== 2. El caso que rompe la intuición ===\n')
    rows = truth_table(lambda p, q: (not p) or q)
    for (p, q), v in rows:
        if not p:
            print(f'  P={"T" if p else "F"} Q={"T" if q else "F"}  ->  P->Q={"T" if v else "F"}'
                  f'   {"(antecedente falso: la implicación se sostiene igual)" if not q else ""}')
    print()
    print('  Una promesa "si P entonces Q" solo se rompe cuando P se cumple y Q no.')
    print('  Si P nunca se cumplió, la promesa sigue en pie. Eso NO es una rareza')
    print('  lógica: es lo que hace que "P -> Q" sea igual a "no P o Q", y sin esa')
    print('  equivalencia no se puede pasar a CNF.')

    print('\n=== 3. Las equivalencias que hay que saber ===\n')
    ok = True
    ok &= equivalent('Implicación:      P->Q  ==  (not P) or Q',
                     lambda p, q: (not p) or q,
                     lambda p, q: (not p) or q)
    ok &= equivalent('Contrapositiva:   P->Q  ==  (not Q)->(not P)',
                     lambda p, q: (not p) or q,
                     lambda p, q: q or (not p))
    ok &= equivalent('De Morgan and:    not(P and Q) == (not P) or (not Q)',
                     lambda p, q: not (p and q),
                     lambda p, q: (not p) or (not q))
    ok &= equivalent('De Morgan or:     not(P or Q)  == (not P) and (not Q)',
                     lambda p, q: not (p or q),
                     lambda p, q: (not p) and (not q))
    ok &= equivalent('Distributiva:     P and (Q or R) == (P and Q) or (P and R)',
                     lambda p, q, r: p and (q or r),
                     lambda p, q, r: (p and q) or (p and r), n=3)
    ok &= equivalent('Bicondicional:    P<->Q  ==  (P->Q) and (Q->P)',
                     lambda p, q: p == q,
                     lambda p, q: ((not p) or q) and ((not q) or p))

    print('\n=== 4. Una equivalencia que NO es cierta ===\n')
    bad = equivalent('Contrapositiva INVÁLIDA: P->Q  ==  Q->P   (debe FALLAR)',
                     lambda p, q: (not p) or q,
                     lambda p, q: (not q) or p)
    if bad:
        print('  El chequeo no sirve: una equivalencia falsa pasó. El verificador está roto.')
        return 1
    print('  Afirmar P->Q == Q->P es el error de "afirmar el consecuente".')
    print('  De "si llueve me mojo" no se sigue "si me mojo, llovió".')

    print()
    if ok:
        print('RESULTADO: PASA — las 6 equivalencias válidas se sostienen y la inválida se rechaza.')
        return 0
    print('RESULTADO: FALLA')
    return 1


if __name__ == '__main__':
    sys.exit(main())
