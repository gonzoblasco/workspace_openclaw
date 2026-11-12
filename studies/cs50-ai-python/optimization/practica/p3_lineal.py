#!/usr/bin/env python3
"""Práctica 3 — programación lineal: la fábrica del curso, resuelta a mano.

El curso resuelve esta fábrica con `scipy.optimize.linprog`. scipy no está
instalado acá, así que la práctica hace lo que hace un solver: recorre los
vértices del poliedro factible y se queda con el mejor.

Eso vale más que llamar a la librería, porque expone lo que la librería
esconde: en un programa lineal, el óptimo SIEMPRE está en un vértice. Si
entendés eso, entendés por qué linprog no busca en el interior.

Problema (el de la clase):
  Maximizar 40·X + 30·Y
  sujeto a
     X + Y   <= 12      (horas de máquina)
     2X + Y  <= 16      (operarios)
     X, Y    >= 0
"""
import itertools
import sys


VARS = ['X', 'Y']
C = {'X': 40, 'Y': 30}
CONSTRAINTS = [
    ({'X': 1, 'Y': 1}, 12),     # <=
    ({'X': 2, 'Y': 1}, 16),     # <=
]


def feasible(point):
    for coeffs, bound in CONSTRAINTS:
        if sum(coeffs[v] * point[v] for v in VARS) > bound + 1e-9:
            return False
    return all(point[v] >= -1e-9 for v in VARS)


def vertices():
    """Intersección de cada par de rectas (restricciones + ejes)."""
    # rectas: ax + by = b
    lines = []
    for coeffs, bound in CONSTRAINTS:
        lines.append((coeffs.get('X', 0), coeffs.get('Y', 0), bound))
    lines.append((1, 0, 0))   # x = 0
    lines.append((0, 1, 0))   # y = 0

    pts = []
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(lines, 2):
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-12:
            continue                      # paralelas
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        pts.append({'X': x, 'Y': y})
    return pts


def objective(p):
    return sum(C[v] * p[v] for v in VARS)


def main():
    print('Maximizar  40·X + 30·Y')
    print('sujeto a')
    print('   X +  Y <= 12')
    print('   2X + Y <= 16')
    print('   X, Y  >= 0')
    print()

    pts = vertices()
    print(f'=== Los {len(pts)} vértices del cruce de rectas ===')
    print(f'  {"X":<10} {"Y":<10} {"40X+30Y":<12} {"factible"}')
    print('-' * 48)
    order = sorted(pts, key=lambda p: (p['X'], p['Y']))
    best = None
    for p in order:
        z = objective(p)
        ok = feasible(p)
        print(f'  {p["X"]:<10.2f} {p["Y"]:<10.2f} {z:<12.2f} {"sí" if ok else "no"}')
        if ok and (best is None or z > best[2]):
            best = (p['X'], p['Y'], z)
    print()

    print(f'Óptimo: X={best[0]:.2f}  Y={best[1]:.2f}  Z={best[2]:.2f}')
    print()

    # --- verificación 1: que ningún interior mejore -----------------------
    print('=== ¿Podría haber algo mejor adentro? No ===')
    print('  Barrido de 100x100 puntos factibles; el mejor z encontrado:')
    best_z = -1e18
    best_at = None
    for i in range(101):
        for j in range(101):
            p = {'X': i * 0.2, 'Y': j * 0.2}
            if feasible(p):
                z = objective(p)
                if z > best_z:
                    best_z, best_at = z, p
    print(f'    grid: Z={best_z:.2f} en ({best_at["X"]:.1f}, {best_at["Y"]:.1f})')
    print(f'    vértice: Z={best[2]:.2f} en ({best[0]:.1f}, {best[1]:.1f})')
    print(f'    el vértice gana o empata: {"sí" if best[2] >= best_z - 1e-6 else "NO"}')
    print()
    print('  Eso es un teorema, no una coincidencia: el objetivo es LINEAL y el')
    print('  dominio es un POLÍGONO convexo. Una función lineal sobre un polígono')
    print('  no tiene máximo interior. Por eso linprog puede recorrer vértices y')
    print('  terminar: no le falta buscar, no hay nada que buscar adentro.')
    print()

    # --- y dónde esto deja de funcionar -----------------------------------
    print('=== Dónde se rompe ===')
    print('  Si la restricción fuera "X·Y <= 12" (no lineal), el óptimo podría')
    print('  estar en el interior y el recorrido de vértices daría una respuesta')
    print('  falsa con la misma seguridad. Y en programación ENTERA (X, Y enteros)')
    print('  el óptimo puede no ser un vértice del poliedro relajado.')
    print()
    print('  Es el límite que el curso no toca y que cualquier problema real')
    print('  encuentra: la formulación lineal es una elección, no una propiedad')
    print('  del problema.')

    print()
    ok = abs(best[2] - 400) < 1e-6 and best[2] >= best_z - 1e-6
    print('RESULTADO: PASA' if ok else f'RESULTADO: FALLA (Z={best[2]:.2f})')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
