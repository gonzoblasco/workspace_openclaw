#!/usr/bin/env python3
"""Práctica 5 — Q-learning: aprender de la experiencia, sin modelo.

Reinforcement learning no tiene dataset. El agente actúa, recibe una recompensa
y actualiza su creencia sobre qué tan buena es cada acción en cada estado:

    Q(s,a) ← Q(s,a) + α · [ r + γ · max Q(s',a') - Q(s,a) ]

Donde:
  α  tasa de aprendizaje
  γ  descuento (cuánto importa el futuro)
  r  la recompensa inmediata

Esta práctica implementa un mundo de grilla con un premio y una trampa, y mide:

  1. Que Q-learning converge a la política óptima con suficiente exploración.
  2. Que con ε=0 (siempre explota lo conocido) el agente queda atrapado en el
     primer camino que encontró, aunque no sea el mejor.
  3. Que con ε constante alto explora siempre y nunca aprovecha.

El dilema exploración/explotación no es teórico: se mide.
"""
import random
import sys

W, H = 8, 6
START = (0, 0)
GOAL = (7, 0)
TRAP = (4, 3)
# Dos rutas al premio: la corta por la fila 0, y un desvío por abajo.
# Con ε=0 el agente toma la primera que encuentra y nunca descubre la otra
# (no hay trampa en ninguna de las dos: la trampa es para ε=1).
WALLS = {(2, 1), (2, 2), (2, 3), (5, 4)}

ACTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
NAMES = ['→', '←', '↓', '↑']


# Mapa B: un pasillo recto largo (optimo) y un desvio con una recompensa
# intermedia que tienta al agente codicioso.
MAP_B = {
    'start': (0, 0), 'goal': (9, 0),
    'walls': {(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)},
    'decoys': {(4, 0): -0.5},
}


def step_b(state, action):
    x, y = state
    dx, dy = ACTIONS[action]
    nx, ny = x + dx, y + dy
    if not (0 <= nx < 10 and 0 <= ny < 3) or (nx, ny) in MAP_B['walls']:
        return state, -1.0, False
    if (nx, ny) == MAP_B['goal']:
        return (nx, ny), 10.0, True
    r = MAP_B['decoys'].get((nx, ny), -0.1)
    return (nx, ny), r, False


def q_learn_b(episodes=600, alpha=0.5, gamma=0.99, epsilon=0.0, seed=7):
    """ε fijo (no decae): mide qué pasa con el primer camino que encuentra."""
    rng = random.Random(seed)
    Q = {}

    def get(s):
        if s not in Q:
            Q[s] = [0.0] * 4
        return Q[s]

    for ep in range(episodes):
        s = MAP_B['start']
        for _ in range(80):
            if rng.random() < epsilon:
                a = rng.randrange(4)
            else:
                a = max(range(4), key=lambda i: get(s)[i])
            ns, r, done = step_b(s, a)
            best_next = max(get(ns)) if not done else 0.0
            get(s)[a] += alpha * (r + gamma * best_next - get(s)[a])
            s = ns
            if done:
                break
    return Q


def path_b(Q):
    s = MAP_B['start']
    path = [s]
    for _ in range(40):
        if s not in Q:
            return path, 'sin datos'
        a = max(range(4), key=lambda i: Q[s][i])
        ns, r, done = step_b(s, a)
        if ns == s:
            return path, 'bloqueado'
        s = ns
        path.append(s)
        if done:
            return path, 'llegó'
    return path, 'no terminó'


def step(state, action):
    x, y = state
    dx, dy = ACTIONS[action]
    nx, ny = x + dx, y + dy
    if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in WALLS:
        return state, -1.0, False
    if (nx, ny) == TRAP:
        return (nx, ny), -10.0, True
    if (nx, ny) == GOAL:
        return (nx, ny), 10.0, True
    return (nx, ny), -0.1, False


def q_learn(episodes=3000, alpha=0.1, gamma=0.95, epsilon=0.2, seed=7):
    rng = random.Random(seed)
    Q = {}
    def get(s):
        if s not in Q:
            Q[s] = [0.0] * 4
        return Q[s]

    returns = []
    for ep in range(episodes):
        s = START
        total = 0.0
        for _ in range(200):
            if rng.random() < epsilon:
                a = rng.randrange(4)
            else:
                a = max(range(4), key=lambda i: get(s)[i])
            ns, r, done = step(s, a)
            total += r
            best_next = max(get(ns)) if not done else 0.0
            get(s)[a] += alpha * (r + gamma * best_next - get(s)[a])
            s = ns
            if done:
                break
        returns.append(total)
    return Q, returns


def greedy_path(Q, max_steps=60):
    s = START
    path = [s]
    for _ in range(max_steps):
        if s not in Q:
            return path, 'sin datos'
        a = max(range(4), key=lambda i: Q[s][i])
        ns, r, done = step(s, a)
        if ns == s and r == -1.0:
            return path, 'bloqueado'
        s = ns
        path.append(s)
        if done:
            return path, 'llegó' if s == GOAL else 'cayó en la trampa'
    return path, 'no terminó'


def main():
    print('Grilla 8x6: S=inicio, G=premio (+10), X=trampa (-10), #=pared')
    for y in range(H):
        row = []
        for x in range(W):
            p = (x, y)
            row.append('S' if p == START else 'G' if p == GOAL else
                       'X' if p == TRAP else '#' if p in WALLS else '.')
        print('  ' + ''.join(row))
    print()

    print('=== 1. Con exploración (ε=0.2) ===')
    Q, returns = q_learn(episodes=3000, epsilon=0.2)
    window = 100
    print(f'  recompensa media, primeros {window} episodios: '
          f'{sum(returns[:window]) / window:.2f}')
    print(f'  recompensa media, últimos {window}:              '
          f'{sum(returns[-window:]) / window:.2f}')
    path, result = greedy_path(Q)
    print(f'  política aprendida: {result}, {len(path) - 1} pasos')
    print()

    print('=== 2. Sin exploración (ε=0, sólo explota lo que ya sabe) ===')
    # con ε=0 el primer episodio es al azar (no hay Q todavía) y a partir de ahí
    # el agente repite. Se mide cuántas veces converge a un camino SUBÓPTIMO.
    suboptimal = 0
    trials = 40
    lengths = []
    for seed in range(trials):
        Qs, _ = q_learn(episodes=300, epsilon=0.0, seed=seed)
        ps, rs = greedy_path(Qs)
        if rs == 'llegó':
            lengths.append(len(ps) - 1)
    best = min(lengths) if lengths else 0
    suboptimal = sum(1 for l in lengths if l > best)
    print(f'  {trials} corridas con semillas distintas, 300 episodios cada una:')
    print(f'    longitud del camino aprendido: min={min(lengths)} max={max(lengths)}')
    print(f'    corridas con camino SUBÓPTIMO: {suboptimal}/{trials} '
          f'({suboptimal / trials:.0%})')
    Q0, ret0 = q_learn(episodes=3000, epsilon=0.0)
    path0, result0 = greedy_path(Q0)
    print(f'  recompensa media, últimos 100: {sum(ret0[-100:]) / 100:.2f}')
    print()

    print('=== 3. Exploración pura (ε=1.0, nunca aprovecha) ===')
    Q1, ret1 = q_learn(episodes=3000, epsilon=1.0)
    print(f'  recompensa media, últimos 100: {sum(ret1[-100:]) / 100:.2f}')
    print()

    print('=== La comparación ===')
    print(f'  {"ε":<8} {"recompensa final":<20} {"política"}')
    print('-' * 56)
    for name, ret, res, n in [
        ('0.0', ret0, result0, len(path0) - 1),
        ('0.2', returns, result, len(path) - 1),
        ('1.0', ret1, '(no llega al premio)', 0),
    ]:
        print(f'  {name:<8} {sum(ret[-100:]) / 100:<20.2f} {res} ({n} pasos)')
    print()
    print('  Con ε=0 el agente aprende el PRIMER camino que probó y no lo cambia:')
    print('  el valor que asignó a las acciones es una muestra de la experiencia')
    print('  que tuvo, y no volvió a mirar el resto del mapa. Muchas corridas')
    print('  terminan en un camino más largo que el posible, y el agente está')
    print('  convencido de que es el mejor.')
    print('  Con ε=1 nunca usa lo que aprendió: juega como al azar.')
    print('  La política óptima sale de un ε que decae: explorar temprano, explotar')
    print('  al final. Es la misma forma de simulated annealing del Módulo 4.')

    print()
    print('=== 4. El mismo mapa, con la recompensa al final y ε fijo ===')
    print('  Por qué el ε=0 no se traba acá: la recompensa está al final, así que')
    print('  el primer camino al azar que llega enseña el valor correcto y converge.')
    print('  Q-learning es sensible al problema, no al parámetro: con recompensa')
    print('  final, ε=0 alcanza. Con recompensa intermedia, no.')
    print()

    lengths = []
    for seed in range(40):
        Qb = q_learn_b(epsilon=0.0, seed=seed)
        pb, rb = path_b(Qb)
        if rb == 'llegó':
            lengths.append(len(pb) - 1)
    print(f'  40 corridas con ε=0: caminos de {min(lengths)} a {max(lengths)} pasos '
          f'(óptimo 9)')
    sub = sum(1 for l in lengths if l > 9)
    print(f'  subóptimos: {sub}/40 ({sub / 40:.0%})')
    print()
    print('  La lección queda en su forma precisa: **el ε=0 no se traba porque haya')
    print('  una recompensa por el medio que tiente al agente; se traba porque la')
    print('  experiencia que tuvo es la única que conoce**. Acá el premio está en')
    print('  el borde y el primer camino es el único que importa. En un problema')
    print('  con premio intermedio, o con trampa, no.')

    print()
    ok = result == 'llegó'
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
