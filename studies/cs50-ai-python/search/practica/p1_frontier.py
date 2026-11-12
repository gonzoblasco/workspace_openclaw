#!/usr/bin/env python3
"""Práctica 1 — la frontier: cambiá la estructura y cambia el algoritmo.

Pregunta: si la cola de prioridad de A* se reemplaza por una pila, ¿qué algoritmo
tenés? ¿Y si es una fila? No lo deduzcas: corrélo.

El script corre los mismos tres algoritmos sobre un mapa y muestra, para cada
uno, el orden en que saca nodos de la frontier (los primeros 12) y si el camino
resultante es el más corto. La conclusión se lee en la columna 'ordena por'.

Uso:
    python3 p1_frontier.py
"""
import heapq
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import astar  # noqa: E402

MAP = Path(__file__).resolve().parent.parent / 'maps' / 'maze-b.txt'


def trace(grid, start, goal, order, limit=12):
    """Devuelve (primeros `limit` nodos sacados, costo, expandidos)."""
    h = astar.manhattan
    container = deque([start]) if order == 'fifo' else (
        [(h(start, goal), start)] if order in ('greedy', 'astar') else [start])
    seen_order = []
    came_from = {}
    reached = set()
    expanded = 0
    while container:
        if order == 'lifo':
            # PILA: lo último que entró. El hijo recién hallado gana, así que el
            # costo y la heurística no tienen dónde ejercer presión.
            node = container.pop()
        elif order == 'fifo':
            node = container.popleft()
        else:
            _, node = heapq.heappop(container)
        if node in reached:
            continue
        reached.add(node)
        expanded += 1
        if len(seen_order) < limit:
            seen_order.append(node)
        if node == goal:
            path = astar.reconstruct(came_from, node)
            return seen_order, len(path) - 1, expanded
        for child in sorted(astar.neighbors(grid, node)):
            if child in reached:
                continue
            if child not in came_from:
                came_from[child] = node
                g = astar.g_of(child, came_from)
                if order == 'lifo':
                    container.append(child)
                elif order == 'fifo':
                    container.append(child)
                elif order == 'greedy':
                    heapq.heappush(container, (h(child, goal), child))
                else:
                    heapq.heappush(container, (g + h(child, goal), child))
    return seen_order, None, expanded


ORDER_LABEL = {
    'lifo': ('A* con PILA', 'LIFO (costo y h nulas)', 'DFS'),
    'fifo': ('A* con FILA', 'FIFO (costo y h nulas)', 'BFS'),
    'greedy': ('A* solo con h', 'h decreciente', 'greedy best-first'),
    'astar': ('A* real', 'g+h decreciente', 'A*'),
}


def main():
    grid, start, goal = astar.load_map(MAP.read_text())
    print(f'Mapa: {MAP.name}  inicio={start}  objetivo={goal}\n')
    print(f'{"variante":<16} {"ordena por":<26} {"es en realidad":<22} {"costo":<6} {"expandidos"}')
    print('-' * 84)
    optimal = None
    for order in ('lifo', 'fifo', 'greedy', 'astar'):
        nodes, cost, expanded = trace(grid, start, goal, order)
        label, orders, really = ORDER_LABEL[order]
        if order == 'fifo':
            optimal = cost
        mark = '' if cost == optimal else '  <-- NO óptimo'
        print(f'{label:<16} {orders:<26} {really:<22} {str(cost):<6} {expanded}{mark}')
    print()
    print('Primeros 12 nodos sacados de la frontier:')
    for order in ('lifo', 'fifo', 'greedy', 'astar'):
        nodes, _, _ = trace(grid, start, goal, order)
        label = ORDER_LABEL[order][0]
        print(f'  {label:<16} {nodes}')
    print()
    print('Respondé: la estructura decide el orden; el orden decide qué algoritmo es.')
    print('A* con pila no es A*: es DFS, porque el orden de salida es LIFO y el costo')
    print('deja de ordenar nada. A* con fila es BFS. La heurística se vuelve decorativa.')


if __name__ == '__main__':
    sys.exit(main())
