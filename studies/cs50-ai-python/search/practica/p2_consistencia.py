#!/usr/bin/env python3
"""Práctica 2 — admisibilidad vs consistencia, y por qué la segunda evita reabrir.

Definiciones, sobre grilla 4-direcciones con costo 1:
  admisible   h(n) <= costo real de n al objetivo       (nunca sobreestima)
  consistente h(n) <= 1 + h(n')  para todo vecino n'    (monotonía)

Admisible es más débil: la consistencia es admisibilidad + una condición local.
El script mide, para cada heurística, tres cosas:
  1. ¿alguna vez h(n) > costo real?  -> admisibilidad
  2. ¿alguna vez h(n) > 1 + h(n')?   -> consistencia
  3. ¿A* con esa heurística reabrió algún nodo?  -> la consecuencia práctica

Reabrir un nodo = sacarlo de la frontier con f menor que el f con el que se
expandió. Con heurística consistente no puede pasar; con una admisible pero
inconsistente, sí.
"""
import heapq
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import astar  # noqa: E402


def true_cost(grid, goal):
    """BFS desde el objetivo: distancia real de cada celda libre al objetivo."""
    dist = {goal: 0}
    q = [goal]
    while q:
        nxt = []
        for cell in q:
            for ch in astar.neighbors(grid, cell):
                if ch not in dist:
                    dist[ch] = dist[cell] + 1
                    nxt.append(ch)
        q = nxt
    return dist


def check_admissible(h, dist):
    bad = [c for c in dist if h(c) > dist[c]]
    return bad


def check_consistent(grid, h):
    bad = []
    for cell in grid_cells(grid):
        for n in astar.neighbors(grid, cell):
            if h(cell) > 1 + h(n):
                bad.append((cell, n, h(cell), h(n)))
    return bad


def grid_cells(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != '#':
                yield (x, y)


def expansions_with_reopening(grid, start, goal, h):
    """A* que cuenta reaperturas y devuelve (costo, expandidos, reaperturas)."""
    frontier = [(h(start, goal), 0, start)]
    best_g = {start: 0}
    expanded_at = {}
    expanded = reopen = 0
    came_from = {}
    while frontier:
        f, g, node = heapq.heappop(frontier)
        if g > best_g.get(node, 1 << 30):
            continue  # entrada vieja
        if node in expanded_at:
            if expanded_at[node] <= f:
                continue
            reopen += 1
        expanded_at[node] = f
        expanded += 1
        if node == goal:
            cost = g
            return cost, expanded, reopen
        for child in astar.neighbors(grid, node):
            ng = g + 1
            if ng < best_g.get(child, 1 << 30):
                best_g[child] = ng
                came_from[child] = node
                heapq.heappush(frontier, (ng + h(child, goal), ng, child))
    return None, expanded, reopen


def main():
    grid, start, goal = astar.load_map((Path(__file__).resolve().parent.parent / 'maps' / 'maze-b.txt').read_text())
    dist = true_cost(grid, goal)
    optimal = dist[start]

    print(f'Mapa: maze-b  óptimo real = {optimal}\n')

    # (nombre, función, ¿admitimos que sobreestime?)
    heuristics = [
        ('manhattan', astar.manhattan, True),
        ('cero (sin info)', lambda a, b: 0, False),
        ('manhattan*1.5', lambda a, b: 1.5 * astar.manhattan(a, b), False),
        ('manhattan al cuadrado/20', lambda a, b: int(astar.manhattan(a, b) ** 2 / 20), False),
    ]

    print(f'{"heurística":<26} {"admisible?":<12} {"consistente?":<14} {"costo":<7} {"expandidos":<11} {"reaperturas"}')
    print('-' * 92)
    for name, h, _ in heuristics:
        adm_bad = check_admissible(lambda c: h(c, goal), dist)
        con_bad = check_consistent(grid, lambda c: h(c, goal))
        cost, exp, reopen = expansions_with_reopening(grid, start, goal, lambda a, b: h(a, b))
        print(f'{name:<26} {"sí" if not adm_bad else f"NO ({len(adm_bad)})":<12} '
              f'{"sí" if not con_bad else f"NO ({len(con_bad)})":<14} '
              f'{str(cost):<7} {exp:<11} {reopen}')

    print()
    print('--- el caso que separa las dos definiciones ---')
    # Una heurística admisible pero INCONSISTENTE: h sube al alejarse del objetivo
    # en una zona donde el costo real también sube, pero el salto entre vecinos es
    # mayor que el costo del paso. Admisible (nunca sobreestima) y, aun así,
    # viola h(n) <= 1 + h(n'), que es la condición de consistencia.
    def bumpy(a, b):
        d = astar.manhattan(a, b)
        # En la esquina superior izquierda h se desploma: 0 en (1,1) y el valor
        # real en (1,2)/(2,1). Cada arista que toca el inicio viola la desigualdad.
        if a == (1, 1):
            return 0
        return d

    peak = (1, 1)

    adm_bad = check_admissible(lambda c: bumpy(c, goal), dist)
    con_bad = check_consistent(grid, lambda c: bumpy(c, goal))
    cost, exp, reopen = expansions_with_reopening(grid, start, goal, bumpy)
    print(f'heurística admisible con desnivel en {peak}:')
    print(f'  admisible:   {"sí" if not adm_bad else f"NO ({len(adm_bad)} celdas sobreestiman)"}')
    print(f'  consistente: {"sí" if not con_bad else f"NO ({len(con_bad)} violaciones)"}')
    print(f'  costo={cost} (óptimo {optimal})  expandidos={exp}  reaperturas={reopen}')
    print()
    print('Que una heurística pase la prueba de admisibilidad NO implica que sea')
    print('consistente: la admisibilidad se verifica contra el costo real al objetivo,')
    print('la consistencia contra los vecinos. La consistencia implica admisibilidad,')
    print('nunca al revés. Por eso A* se implementa con el chequeo de reapertura:')
    print('con heurística inconsistente el camino óptimo puede hallarse tarde.')

if __name__ == '__main__':
    sys.exit(main())
