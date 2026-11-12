#!/usr/bin/env python3
"""Práctica 2 — red bayesiana: la estructura ahorra el cálculo.

Una red bayesiana es un grafo dirigido acíclico donde cada variable tiene una
tabla de probabilidad condicionada a sus PADRES. La gracia es que la red
conjunta completa se factoriza como producto de esas tablas locales:

    P(X1, ..., Xn) = Π P(Xi | padres(Xi))

Esa factorización es el 100% de por qué una red bayesiana sirve: sin ella,
la tabla conjunta de 30 variables binarias tiene 2^30 filas.

Esta práctica:
  1. construte una red (lluvia -> mojado, lluvia -> resbalón),
  2. calcula la conjunta COMPLETA enumerando (la tabla gigante),
  3. calcula la conjunta FACTORIZADA con las tablas locales,
  4. verifica que dan lo mismo,
  5. cuenta cuántos números hay que guardar en cada forma.

El punto 5 es el argumento de todo el módulo.
"""
import itertools
import sys


# --- La red: estructura + tablas -------------------------------------------

# Variable: (nombre, padres)
NODES = [
    ('R', []),          # llovió
    ('W', ['R']),       # me mojé
    ('S', ['R']),       # la calle resbaló
]

# Tabla condicional: P(variable=v | padres=asignación)
CPT = {
    'R': {
        (): {'T': 0.30, 'F': 0.70},
    },
    'W': {
        ('T',): {'T': 0.90, 'F': 0.10},
        ('F',): {'T': 0.20, 'F': 0.80},
    },
    'S': {
        ('T',): {'T': 0.80, 'F': 0.20},
        ('F',): {'T': 0.10, 'F': 0.90},
    },
}

PADRES = {name: parents for name, parents in NODES}
VARS = [name for name, _ in NODES]
VALUES = ['T', 'F']


def local_prob(var, value, assignment):
    key = tuple(assignment[p] for p in PADRES[var])
    return CPT[var][key][value]


def joint_factorized(assignment):
    """P(X1,...,Xn) = producto de las condicionales locales."""
    p = 1.0
    for var in VARS:
        p *= local_prob(var, assignment[var], assignment)
    return p


def count_bruteforce_entries():
    return 2 ** len(VARS)


def count_factorized_entries():
    """Cada CPT necesita 2^(padres+1) - 1 números: la última fila sale de restar 1."""
    total = 0
    for var, parents in NODES:
        total += 2 ** (len(parents) + 1) - 1
    return total


def main():
    print('=== La red ===')
    for var, parents in NODES:
        print(f'  {var} <- {parents if parents else "(ninguno)"}')
    print()
    print('  R: P(llovió) = 0.30')
    print('  W|R:  si llovió, 0.90 de mojarse; si no, 0.20')
    print('  S|R:  si llovió, 0.80 de resbalar; si no, 0.10')
    print()

    print('=== 1. La conjunta completa, calculada ===')
    print(f'  {"R":<3} {"W":<3} {"S":<3} {"P(R,W,S)"}')
    total = 0.0
    for r, w, s in itertools.product(VALUES, repeat=3):
        a = {'R': r, 'W': w, 'S': s}
        p = joint_factorized(a)
        total += p
        print(f'  {r:<3} {w:<3} {s:<3} {p:.4f}')
    print(f'  suma de todas las entradas = {total:.4f}  '
          f'{"ok" if abs(total - 1) < 1e-9 else "FALLA: no suma 1"}')
    print()

    print('=== 2. La factorización da exactamente lo mismo ===')
    print('  P(R=T, W=T, S=T) = P(R) * P(W|R) * P(S|R)')
    a = {'R': 'T', 'W': 'T', 'S': 'T'}
    parts = [(v, local_prob(v, a[v], a)) for v in VARS]
    print('    ' + ' * '.join(f'{v}={p:.2f}' for v, p in parts))
    prod = 1.0
    for _, p in parts:
        prod *= p
    print(f'  = {prod:.4f}   ({"coincide" if abs(prod - joint_factorized(a)) < 1e-12 else "DIFIERE"})')
    print()

    print('=== 3. Cuántos números hay que escribir ===')
    print(f'  {"forma":<34} {"números a guardar"}')
    print('-' * 58)
    # El conteo correcto NO es filas × 2 por fila: como cada fila suma 1, una
    # distribución sobre 2 valores necesita 2^(padres+1) - 1 números. Contar el
    # doble infla la factorizada y esconde la ventaja cuando el grafo es chico.
    print(f'  {"conjunta sin estructura":<34} {count_bruteforce_entries()}')
    print(f'  {"factorizada (las 3 CPTs)":<34} {count_factorized_entries()}')
    print()
    print('  Con 3 variables y padres de a uno, la conjunta entra igual. La ventaja')
    print('  aparece al crecer: la conjunta es 2^n - 1 números; la factorizada es la')
    print('  suma de las tablas locales, y en una cadena cada una tiene 1 padre.')
    print()
    print(f'  {"variables":<12} {"conjunta 2^n":<18} {"cadena con 1 padre":<20} {"factor"}')
    for n in (3, 5, 10, 20, 30):
        conj = 2 ** n
        # cadena: raíz sin padres (1 número) + (n-1) nodos con 1 padre (3 números)
        fact = 1 + 3 * (n - 1)
        print(f'  {n:<12} {conj:<18} {fact:<20} {conj / fact:>10.0f}x')
    print()
    print('  Con 30 variables: mil millones de entradas contra 88 números.')
    print('  Ahí está por qué la notación del curso dice "producto de las')
    print('  condicionales": no es una simplificación para escribir más corto,')
    print('  es la diferencia entre calcular y no poder calcular.')
    print()
    print('  Y el límite del truco: si un nodo tiene 20 padres, su tabla local')
    print('  ya tiene 2^20 filas. La factorización no elimina el exponencial;')
    print('  lo mueve de la cantidad de variables al ancho de la vecindad más grande.')

    print()
    ok = abs(total - 1) < 1e-9 and abs(prod - joint_factorized(a)) < 1e-12
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
