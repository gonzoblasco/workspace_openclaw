#!/usr/bin/env python3
"""Módulo 1 - Search: BFS vs greedy best-first vs A* sobre laberintos en texto.

La clase define un problema de búsqueda por cinco piezas: estado inicial, acciones,
modelo de transición, test de objetivo y costo de camino. Todo lo demás es el
algoritmo: cómo se ordena la frontier decide DFS (LIFO), BFS (FIFO), greedy
(heurística sola) y A* (costo pagado + estimación).

La prueba del ejercicio es que A* expanda estrictamente menos que BFS en ambos
mapas y devuelva exactamente el mismo costo de camino.

Uso:
    python3 astar.py                 # corre los dos mapas del curso
    python3 astar.py mapas/x.txt     # corre un mapa propio

Mapa: '#' pared, ' ' libre, 'A' inicio, 'B' objetivo. Todas las acciones cuestan 1.
"""
import heapq
import sys
from collections import deque


def load_map(text):
    grid = [list(line.rstrip('\n')) for line in text.strip('\n').split('\n') if line.strip()]
    start = goal = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'A':
                start = (x, y)
            elif cell == 'B':
                goal = (x, y)
    if start is None or goal is None:
        raise ValueError('el mapa necesita un inicio A y un objetivo B')
    return grid, start, goal


def neighbors(grid, cell):
    x, y = cell
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != '#':
            yield (nx, ny)


def manhattan(a, b):
    """La heurística de la clase: distancia horizontal más vertical, ignorando paredes.
    Es admisible porque cada movimiento cambia la distancia en exactamente 1 y nunca
    puede sobreestimar el costo real."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def inflated(weight):
    """Variante NO admisible: w * h. Con w>1 puede sobreestimar y A* deja de garantizar
    optimalidad. Sirve para ver el precio de mentirle al algoritmo."""
    def h(a, b):
        return weight * manhattan(a, b)
    return h


def reconstruct(came_from, cell):
    path = [cell]
    while cell in came_from:
        cell = came_from[cell]
        path.append(cell)
    return list(reversed(path))


def search(grid, start, goal, order, heuristic=None):
    """order: 'fifo' (BFS), 'greedy', 'astar'. Devuelve (path, expanded, cost)."""
    h = heuristic or manhattan
    frontier = {start}
    if order == 'fifo':
        container = deque([start])
    elif order == 'greedy':
        container = [(h(start, goal), start)]
    elif order == 'astar':
        container = [(h(start, goal), start)]
    else:
        raise ValueError(order)

    came_from = {}
    reached = set()
    expanded = 0

    while container:
        if order == 'fifo':
            node = container.popleft()
            priority = None
        else:
            priority, node = heapq.heappop(container)
        frontier.discard(node)
        if node in reached:      # ya expandido con un costo menor o igual
            continue
        reached.add(node)
        expanded += 1

        if node == goal:
            path = reconstruct(came_from, node)
            return path, expanded, len(path) - 1

        children = list(neighbors(grid, node))
        # Orden estable: el orden de vecinos no debe decidir el resultado de un empate.
        children.sort()
        for child in children:
            if child in reached:
                continue
            if child not in frontier:
                came_from[child] = node
                frontier.add(child)
                g = g_of(child, came_from)
                if order == 'fifo':
                    container.append(child)
                elif order == 'greedy':
                    heapq.heappush(container, (h(child, goal), child))
                elif order == 'astar':
                    heapq.heappush(container, (g + h(child, goal), child))
            # BFS/greedy no reabren: alcanza con haberlo visto. A* sí necesita el
            # chequeo de costo si el grafo tuviera costos distintos; acá son todos 1.

    return None, expanded, None


def g_of(cell, came_from):
    """Costo pagado hasta `cell` siguiendo el árbol de padres."""
    cost = 0
    while cell in came_from:
        cell = came_from[cell]
        cost += 1
    return cost


def render(grid, path):
    out = [row[:] for row in grid]
    for x, y in path[1:-1]:
        out[y][x] = '.'
    return '\n'.join(''.join(row) for row in out)


def solve_one(name, text):
    grid, start, goal = load_map(text)
    print(f'== {name} ({len(grid[0])}x{len(grid)}) ==')
    results = {}
    for order in ('fifo', 'greedy', 'astar'):
        path, expanded, cost = search(grid, start, goal, order)
        results[order] = (path, expanded, cost)
        label = {'fifo': 'BFS', 'greedy': 'greedy best-first', 'astar': 'A*'}[order]
        if path is None:
            print(f'  {label:<20} sin solución        expandidos={expanded}')
        else:
            print(f'  {label:<20} costo={cost:<3} expandidos={expanded:<4} '
                  f'ruta={path[0]} -> {path[len(path)//2]} -> {path[-1]} ({len(path)-1} pasos)')
    print()
    best = results['astar'][0] or results['fifo'][0]
    if best:
        print(render(grid, best))
        print()
    return results


def check(name, grid, start, goal, results):
    """La prueba del outline: A* expande menos que BFS y cuesta lo mismo."""
    bfs_cost = results['fifo'][2]
    astar_cost = results['astar'][2]
    bfs_expanded = results['fifo'][1]
    astar_expanded = results['astar'][1]
    ok = True
    if bfs_cost is None:
        print(f'  FAIL {name}: BFS no encontró solución; el mapa de prueba no sirve')
        return False
    if astar_cost != bfs_cost:
        print(f'  FAIL {name}: A* costo {astar_cost} != BFS costo {bfs_cost}')
        ok = False
    if not astar_expanded < bfs_expanded:
        print(f'  FAIL {name}: A* expandió {astar_expanded}, BFS {bfs_expanded} (A* no ahorró)')
        ok = False
    greedy_cost = results['greedy'][2]
    if greedy_cost is not None:
        # Greedy NO es óptimo: puede devolver un costo mayor que A* (eso es esperable).
        # Lo imposible sería que devolviera uno menor que el óptimo.
        if greedy_cost < astar_cost:
            print(f'  FAIL {name}: greedy devolvió un costo imposible ({greedy_cost} < óptimo {astar_cost})')
            ok = False
        elif greedy_cost > astar_cost:
            print(f'  nota {name}: greedy costó {greedy_cost} vs óptimo {astar_cost} (subóptimo, como predice la clase)')
    # Nota pedagógica, no fallo: con w>1 A* deja de ser óptimo. Que dé distinto es lo
    # que prueba que la admisibilidad no es un tecnicismo.
    for weight in (1.5, 2.0):
        _, expanded, cost = search(grid, start, goal, 'astar', heuristic=inflated(weight))
        if cost != bfs_cost:
            print(f'  nota {name}: A* con w={weight} devolvió {cost} en vez del óptimo {bfs_cost} '
                  f'- la heurística inadmisible rompe la garantía')

    # La heurística inflada: qué pasa cuando se rompe la admisibilidad.
    for weight in (1.5, 2.0):
        _, expanded, cost = search(grid, start, goal, 'astar', heuristic=inflated(weight))
        ratio = expanded / astar_expanded
        verdict = 'óptimo' if cost == bfs_cost else f'SUBÓPTIMO (+{cost - bfs_cost})'
        print(f'  A* w={weight:<4} costo={cost:<3} expandidos={expanded:<4} '
              f'({ratio:.2f}× los de A* admisible) {verdict}')

    if ok:
        ratio = bfs_expanded / astar_expanded
        print(f'  OK {name}: A* costó {astar_cost} (= BFS) y expandió {astar_expanded} vs {bfs_expanded} (×{ratio:.1f} menos)')
    return ok


MAP_A = open(__file__.replace("astar.py","maps/maze-a.txt")).read()

MAP_B = open(__file__.replace("astar.py","maps/maze-b.txt")).read()


def main():
    maps = [('maze-a', MAP_A), ('maze-b', MAP_B)]
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            maps.append((path, open(path).read()))

    all_ok = True
    print('BFS vs greedy vs A*  —  acciones de costo 1, heurística Manhattan (admisible)\n')
    for name, text in maps:
        results = solve_one(name, text)
        all_ok = check(name, *load_map(text), results) and all_ok
        print()
    print('RESULTADO:', 'PASA' if all_ok else 'FALLA')
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
