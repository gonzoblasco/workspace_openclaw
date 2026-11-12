#!/usr/bin/env python3
"""Práctica 5 — el mismo problema, dos familias de algoritmo.

El outline del módulo deja un candidato de adopción que vale la pena convertir en
script: distinguir si importa el CAMINO (search) o sólo el RESULTADO (local
search). Acá se hace sobre el problema real del workspace: enrutar walkers.

Un mapa con obstáculos, un origen y un destino:

  A* (Módulo 1)        contesta "cómo llego": devuelve el camino.
  Hill climbing (aquí) contesta "qué tan bueno es": sólo el valor final.
  Annealing            lo mismo, con escapes.

El experimento no es de rendimiento: es de **qué se puede preguntar**. Un
algoritmo de búsqueda de caminos no acepta "mejorá esta ruta existente" sin
cambiar de algoritmo, y al revés tampoco.

Es la distinción que importa cuando se elige modelo para una tarea: un plan y un
informe no se mejoran con el mismo método.
"""
import math
import random
import sys

sys.path.insert(0, '.')


# --- el mapa: una grilla con paredes ---------------------------------------

MAP = """
##########################
#S          #            #
# ###### ## # ######## # #
#      #    #        #   #
###### ########### ## # #
#      #         #    # #
# ###### ####### #### # #
#        #     #      # #
# ###### # ### # #### # #
#      # #   # #    #  G#
##########################
"""


def load():
    rows = [list(r) for r in MAP.strip('\n').split('\n') if r.strip()]
    start = goal = None
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c == 'S':
                start = (x, y)
            elif c == 'G':
                goal = (x, y)
    return rows, start, goal


def is_free(rows, p):
    x, y = p
    return 0 <= y < len(rows) and 0 <= x < len(rows[0]) and rows[y][x] != '#'


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# --- familia 1: búsqueda de caminos ---------------------------------------

def astar(rows, start, goal):
    import heapq
    frontier = [(manhattan(start, goal), 0, start)]
    best = {start: 0}
    came = {}
    expanded = 0
    while frontier:
        f, g, node = heapq.heappop(frontier)
        if g > best.get(node, 1 << 30):
            continue
        expanded += 1
        if node == goal:
            path = [node]
            while path[-1] in came:
                path.append(came[path[-1]])
            return list(reversed(path)), expanded
        x, y = node
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            nxt = (x + dx, y + dy)
            if not is_free(rows, nxt):
                continue
            ng = g + 1
            if ng < best.get(nxt, 1 << 30):
                best[nxt] = ng
                came[nxt] = node
                heapq.heappush(frontier, (ng + manhattan(nxt, goal), ng, nxt))
    return None, expanded


# --- familia 2: búsqueda local, sin camino --------------------------------

def objective(rows, goal, path_nodes):
    """Qué tan buena es una ruta: longitud + penalidad por atravesar paredes.

    Ojo: una ruta que NO es un camino válido puede puntuar mejor si sólo se mide
    la distancia. Ese es justo el punto: el objetivo tiene que codificar el
    problema, y si lo codifica mal, el optimizador encuentra el atajo imposible.
    """
    score = 0.0
    for i, p in enumerate(path_nodes):
        if not is_free(rows, p):
            score -= 100.0                 # atravesar una pared
        if i > 0:
            a, b = path_nodes[i - 1], p
            score += 1.0                   # un paso cuesta 1
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
                score += 50.0              # salto no adyacente: inválido
    score += 2.0 * manhattan(path_nodes[-1], goal)
    return -score


def hill_climb_path(rows, start, goal, n_nodes=14, iterations=200, seed=3):
    """Búsqueda local sobre una RUTA: mueve un punto intermedio a un vecino."""
    rng = random.Random(seed)
    path = [start] + [start] * (n_nodes - 2) + [goal]
    best = objective(rows, goal, path)
    for _ in range(iterations):
        i = rng.randrange(1, len(path) - 1)
        x, y = path[i]
        cand = path[:]
        cand[i] = (x + rng.choice([-1, 0, 1]), y + rng.choice([-1, 0, 1]))
        score = objective(rows, goal, cand)
        if score > best:
            path, best = cand, score
    return path, best


def main():
    rows, start, goal = load()
    print(f'Mapa {len(rows[0])}x{len(rows)}  S={start}  G={goal}')
    print()

    path, expanded = astar(rows, start, goal)
    print('=== Familia 1: búsqueda de caminos (A*) ===')
    if path is None:
        print('  Sin solución.')
        return 1
    print(f'  camino encontrado: {len(path) - 1} pasos')
    print(f'  nodos expandidos: {expanded}')
    print(f'  primera mitad: {path[:len(path) // 2]}')
    print()
    print('  Lo que devuelve es el CAMINO. Se puede dibujar, seguir y verificar.')
    print()

    print('=== Familia 2: búsqueda local (hill climbing sobre la ruta) ===')
    p2, score = hill_climb_path(rows, start, goal)
    valid = all(is_free(rows, p) for p in p2)
    steps = sum(1 for i in range(1, len(p2)))  # 14 puntos, 13 transiciones
    print(f'  puntos en la ruta: {len(p2)}')
    print(f'  ruta válida (sin paredes): {"sí" if valid else "NO"}' +
          ('' if valid else '   <- el puntaje no garantiza validez'))
    print(f'  objetivo: {score:.1f}')
    print(f'  el algoritmo nunca construyó un camino: movió puntos y midió un puntaje')
    print()
    print('  Lo que devuelve NO es un camino: es un puntaje y una lista de puntos')
    print('  que, si el objetivo está bien escrito, se parece a un camino. Si el')
    print('  objetivo está mal escrito —por ejemplo, que sólo mida la distancia al')
    print('  destino— devuelve una recta que atraviesa las paredes con puntaje')
    print('  perfecto. El optimizador no sabe qué es una pared: sólo maximiza.')

    print()
    print('=== La diferencia que importa ===')
    print(f'  {"pregunta":<44} {"A*":<14} {"hill climbing"}')
    print('-' * 74)
    print(f'  {"¿cuál es el camino más corto?":<44} {"sí":<14} {"no"}')
    print(f'  {"¿los pasos son adyacentes y válidos?":<44} {"por construcción":<14} {"por el objetivo"}')
    print(f'  {"¿cuánto pesa cada paso?":<44} {"sí (g+h)":<14} {"sí (en el objetivo)"}')
    print(f'  {"¿mejorar una ruta existente?":<44} {"no":<14} {"sí"}')
    print(f'  {"garantía de óptimo":<44} {"con h admisible":<14} {"ninguna"}')
    print()
    print('  Lo mismo se aplica a un agente: "escribí el plan" es búsqueda;')
    print('  "mejorá este plan" es búsqueda local. Elegir uno y esperar del otro')
    print('  lo que no puede dar es el error más común al montar un pipeline.')

    print()
    ok = path is not None and len(path) > 1
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
