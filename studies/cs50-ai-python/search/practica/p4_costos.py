#!/usr/bin/env python3
"""Práctica 4 — costos distintos: BFS se rompe y Manhattan deja de ser admisible.

Hasta acá todas las acciones cuestan 1. Esa suposición es la que hace que BFS
sea óptimo y que Manhattan valga. Sacala y las dos cosas caen.

Mapa con terreno: ' ' camino (1), '~' barro (3), '#' pared (∞).
  BFS con cola FIFO      -> optimiza CANTIDAD de pasos, no costo. Ya no es óptimo.
  Costo uniforme (UCS)   -> cola de prioridad por g. Es BFS generalizado y sí es óptimo.
  A* con Manhattan       -> sigue siendo admisible. Cada paso cuesta >= 1, y
                            Manhattan mide pasos: subestima o acierta, nunca
                            sobreestima. Legal.
                          -> pero es DÉBIL: el barro cuesta 3 y la heurística lo
                            trata como 1. Cuanto más caro el terreno, más floja
                            la cota y menos ahorra A* frente a UCS.

La lección fina: cambiar los costos NO rompe la admisibilidad de Manhattan
(porque seguir subestimando sigue siendo legal), pero sí rompe a BFS.
"""
import heapq
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import astar  # noqa: E402

TERRAIN = {
    ' ': 1, '~': 3, 'A': 1, 'B': 1, '.': 1,
}

MAP = """
#########################
#A     ~~~             #
# #####~~~#########     #
#     ~~~          # ~~ #
#####~~~########### ~~ #
#   ~~~   ~~~~~~~~~  ~  #
# ###~~#####~~~~~~ #### #
#   ~~     ~~~   ~~~    #
#####  ####~~~####~~#### #
#     ~~~   ~~  ~~      #
#  ####~~####~~######## #
#      ~~   ~~        B #
#########################
"""


def cost(grid, cell):
    return TERRAIN.get(grid[cell[1]][cell[0]], 1)


def search_cost(grid, start, goal, use_heuristic, heuristic=None):
    """Dijkstra / A* con costos por terreno. Devuelve (cost, expanded)."""
    h = heuristic or (lambda a, b: 0)
    frontier = [(h(start, goal), 0, start)]
    best = {start: 0}
    expanded = 0
    done = set()
    while frontier:
        f, g, node = heapq.heappop(frontier)
        if node in done:
            continue
        if g > best.get(node, float('inf')):
            continue
        done.add(node)
        expanded += 1
        if node == goal:
            return g, expanded
        for child in astar.neighbors(grid, node):
            ng = g + cost(grid, child)
            if ng < best.get(child, float('inf')):
                best[child] = ng
                heapq.heappush(frontier, (ng + h(child, goal), ng, child))
    return None, expanded


def bfs_by_steps(grid, start, goal):
    """BFS clásico: optimiza cantidad de pasos, ignora el costo."""
    from collections import deque
    q = deque([(start, 0)])
    seen = {start}
    while q:
        node, steps = q.popleft()
        if node == goal:
            # reconstruir el costo real del camino hallado
            return steps
        for child in astar.neighbors(grid, node):
            if child not in seen:
                seen.add(child)
                q.append((child, steps + 1))
    return None


def path_cost(grid, path):
    return sum(cost(grid, c) for c in path[1:])


def bfs_path_cost(grid, start, goal):
    """BFS por pasos, devuelve el costo REAL del camino que encontró."""
    from collections import deque
    q = deque([start])
    came = {}
    seen = {start}
    while q:
        node = q.popleft()
        if node == goal:
            path = astar.reconstruct(came, node)
            return len(path) - 1, path_cost(grid, path)
        for child in astar.neighbors(grid, node):
            if child not in seen:
                seen.add(child)
                came[child] = node
                q.append(child)
    return None, None


def main():
    grid, start, goal = astar.load_map(MAP)
    print(f'Mapa con barro (~, costo 3)  inicio={start}  objetivo={goal}')
    print()

    _, bfs_cost = bfs_path_cost(grid, start, goal)
    ucs_cost, ucs_exp = search_cost(grid, start, goal, use_heuristic=False)
    astar_cost, astar_exp = search_cost(grid, start, goal, use_heuristic=True,
                                       heuristic=astar.manhattan)

    print(f'{"algoritmo":<30} {"optimiza":<14} {"costo real":<12} {"expandidos"}')
    print('-' * 74)
    print(f'{"BFS (pasos, ignora costo)":<30} {"pasos":<14} {bfs_cost:<12} -')
    print(f'{"UCS (costo uniforme, g)":<30} {"costo":<14} {ucs_cost:<12} {ucs_exp}')
    print(f'{"A* con Manhattan":<30} {"costo":<14} {astar_cost:<12} {astar_exp}')
    print(f'{"A* peso variable 3*h":<30} {"costo":<14} {"-":<12} -')
    print()
    if bfs_cost != ucs_cost:
        print(f'BFS devolvió costo {bfs_cost} cuando el óptimo es {ucs_cost}: '
              f'{bfs_cost - ucs_cost} de más. BFS minimiza PASOS, no pesos.')
    ratio = ucs_exp / astar_exp if astar_exp else 0
    print(f'Manhattan sigue siendo admisible (subestima, y subestimar es legal), pero')
    print(f'ahorra poco: {ucs_exp} vs {astar_exp} expandidos = ×{ratio:.2f}.')
    print('Con terreno caro la cota de pasos se queda corta. A* con costo variable')
    print('pide una heurística mejor (peso mínimo del terreno × distancia), no la')
    print('misma heurística con otra cola.')


if __name__ == '__main__':
    sys.exit(main())
