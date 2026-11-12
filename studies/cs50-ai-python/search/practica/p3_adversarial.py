#!/usr/bin/env python3
"""Práctica 3 — el mapa adversarial se GENERA, no se dibuja a mano.

Dibujar a mano mapas que rompan la heurística es una trampa: uno cree que puso
un desvío donde no está, y el script sale con todos los algoritmos en el mismo
costo. `generate()` hace lo contrario: parte de un laberinto abierto con paredes
sueltas, mide el camino óptimo con BFS, y lo acepta solo si algún caminante
heuristico devuelve un costo peor. Repite hasta encontrarlo.

El criterio de aceptación es la propiedad, no la forma del dibujo:
    adversarial(mapa) := existe w >= 1.5 tal que A*_w devuelve costo > BFS.

Uso:
    python3 p3_adversarial.py            # busca y corre
    python3 p3_adversarial.py --write    # además lo deja en ../maps/
    python3 p3_adversarial.py --seeds 200
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import astar  # noqa: E402


def random_map(rng, w=21, h=15, wall_p=0.33):
    grid = [['#'] * w for _ in range(h)]
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            grid[y][x] = '#' if rng.random() < wall_p else ' '
    start, goal = (1, 1), (w - 2, h - 2)
    grid[start[1]][start[0]] = 'A'
    grid[goal[1]][goal[0]] = 'B'
    return '\n'.join(''.join(r) for r in grid)


def evaluate(text):
    grid, start, goal = astar.load_map(text)
    _, _, bfs_cost = astar.search(grid, start, goal, 'fifo')
    if bfs_cost is None:
        return None
    res = {'bfs': bfs_cost, 'start': start, 'goal': goal}
    for w in (1.0, 1.5, 2.0, 3.0):
        h = None if w == 1.0 else astar.inflated(w)
        _, exp, cost = astar.search(grid, start, goal, 'astar', heuristic=h)
        res[f'w{w}'] = (cost, exp)
    _, exp, cost = astar.search(grid, start, goal, 'greedy')
    res['greedy'] = (cost, exp)
    return res


def is_adversarial(res):
    return any(res[f'w{w}'][0] != res['bfs'] for w in (1.5, 2.0, 3.0))


def generate(seeds=500, w=21, h=15):
    for seed in range(seeds):
        rng = random.Random(seed)
        text = random_map(rng, w, h)
        try:
            res = evaluate(text)
        except ValueError:
            continue
        if res and is_adversarial(res):
            return seed, text, res
    return None, None, None


def main():
    seeds = 500
    if '--seeds' in sys.argv:
        seeds = int(sys.argv[sys.argv.index('--seeds') + 1])
    seed, text, res = generate(seeds)
    if text is None:
        print(f'FALLA: ningún mapa adversarial en {seeds} semillas. Subí --seeds o la densidad de paredes.')
        return 1

    print(f'Mapa adversarial encontrado en la semilla {seed}')
    print(text)
    print()
    print(f'inicio={res["start"]}  objetivo={res["goal"]}  óptimo BFS={res["bfs"]}')
    print()
    print(f'{"algoritmo":<22} {"costo":<7} {"expandidos"}')
    print('-' * 42)
    print(f'{"BFS (óptimo)":<22} {res["bfs"]:<7} -')
    for name, key in [('greedy', 'greedy'), ('A* w=1.0', 'w1.0'), ('A* w=1.5', 'w1.5'),
                      ('A* w=2.0', 'w2.0'), ('A* w=3.0', 'w3.0')]:
        cost, exp = res[key]
        print(f'{name:<22} {str(cost):<7} {exp}')

    if '--write' in sys.argv:
        out = Path(__file__).resolve().parent.parent / 'maps' / 'maze-adversarial.txt'
        out.write_text(text + '\n')
        print(f'\nescrito en {out}')

    print()
    print('La propiedad que lo hace útil: acá la heurística inflada SÍ devuelve un costo')
    print('peor que el óptimo. Un mapa donde nunca pasa no testea nada.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
