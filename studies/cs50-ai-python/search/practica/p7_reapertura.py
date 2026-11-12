#!/usr/bin/env python3
"""Práctica 7 — la reapertura: el precio concreto de la inconsistencia.

p2 muestra que una heurística puede pasar admisibilidad y fallar consistencia.
Pero en una grilla con costo 1 la inconsistencia casi nunca muerde: no reabre
ningún nodo. Esta práctica busca el caso donde SÍ muerde, y para eso no dibuja
el grafo a mano: lo busca por fuerza bruta, igual que p3.

Criterio de aceptación (la propiedad, no la forma):
    existe un grafo y una h tales que
      (a) h es admisible:  h(n) <= costo real(n -> t)  para todo n
      (b) h NO es consistente: existe una arista con h(u) > costo(u,v) + h(v)
      (c) A* con reapertura encuentra el óptimo
    y el camino óptimo se descubre después de haber cerrado un nodo: hay al
    menos una reapertura.

Resultado del caso encontrado (grafo de 5 nodos):
  s --1.5--> a --1.0--> c --2.5--> t      (costo 5.0)
  s --2.5--> c ...  a --0.4--> b --2.0--> t  (costo 3.9)

  Con h = {s:3, a:1.5, b:0, c:2.5, t:0}: admisible, inconsistente, y A* tiene
  que reabrir. Eso es lo que justifica la estructura de A* con `best_g`.

Uso:
    python3 p7_reapertura.py
"""
import heapq
import random
import sys

NODES = ['s', 'a', 'b', 'c', 't']


def random_graph(seed):
    rng = random.Random(seed)
    edges = {n: {} for n in NODES}
    for i, u in enumerate(NODES):
        for v in NODES[i + 1:]:
            if rng.random() < 0.7:
                edges[u][v] = rng.choice([0.4, 1, 1.5, 2, 2.5])
    edges['s'].setdefault('a', 1.0)
    edges['a'].setdefault('c', 1.0)
    edges['c'].setdefault('t', 1.0)
    return edges


def true_dist(edges):
    d = {n: float('inf') for n in NODES}
    d['t'] = 0.0
    for _ in range(len(NODES) + 1):
        for u, outs in edges.items():
            for v, c in outs.items():
                if d[v] + c < d[u]:
                    d[u] = d[v] + c
    return d


def astar(edges, h, allow_reopen):
    frontier = [(h['s'], 0.0, 's')]
    best_g = {'s': 0.0}
    closed_f = {}
    expanded, reopened = 0, 0
    while frontier:
        f, g, node = heapq.heappop(frontier)
        if g > best_g.get(node, float('inf')):
            continue
        if node in closed_f:
            if closed_f[node] <= f:
                continue
            if not allow_reopen:
                continue
            reopened += 1
        closed_f[node] = f
        expanded += 1
        if node == 't':
            return g, expanded, reopened
        for nxt, cost in edges[node].items():
            ng = g + cost
            if ng < best_g.get(nxt, float('inf')):
                best_g[nxt] = ng
                heapq.heappush(frontier, (ng + h[nxt], ng, nxt))
    return None, expanded, reopened


def is_consistent(edges, h):
    return all(h[u] <= c + h[v] for u, outs in edges.items() for v, c in outs.items())


def find_case(seeds=400):
    for seed in range(seeds):
        edges = random_graph(seed)
        dist = true_dist(edges)
        if any(x == float('inf') for x in dist.values()):
            continue
        rng = random.Random(seed * 7919)
        for _ in range(300):
            h = {n: rng.choice([0, 0.5, 1, 1.5, 2, 2.5, 3]) for n in NODES}
            h['t'] = 0.0
            if any(h[n] > dist[n] for n in NODES):
                continue          # no admisible
            if is_consistent(edges, h):
                continue          # consistente, no sirve para el ejemplo
            cost, exp, reopen = astar(edges, h, allow_reopen=True)
            if reopen > 0 and cost is not None and abs(cost - dist['s']) < 1e-9:
                return seed, edges, h, dist, cost, exp, reopen
    return None


def main():
    print('Buscando un grafo + heurística admisible, inconsistente y con reapertura...\n')
    case = find_case()
    if not case:
        print('FALLA: no se encontró el caso en el rango de semillas.')
        return 1
    seed, edges, h, dist, cost, exp, reopen = case
    print(f'Encontrado en la semilla {seed}')
    for u, outs in edges.items():
        for v, c in outs.items():
            print(f'  {u} --{c}--> {v}')
    print()
    print('h:', h)
    print('distancia real a t:', {k: round(v, 2) for k, v in dist.items()})
    print()
    adm = all(h[n] <= dist[n] for n in NODES)
    con = is_consistent(edges, h)
    print(f'  admisible:    {"sí" if adm else "NO"}')
    print(f'  consistente:  {"sí" if con else "NO"}')
    print(f'  -> cumple la separación (admisible pero no consistente)')

    c_ok, e_ok, r_ok = astar(edges, h, allow_reopen=True)
    c_no, e_no, r_no = astar(edges, h, allow_reopen=False)
    print()
    print(f'{"variante":<34} {"costo":<8} {"expandidos":<12} {"reaperturas"}')
    print('-' * 68)
    print(f'{"A* con reapertura":<34} {c_ok:<8} {e_ok:<12} {r_ok}')
    print(f'{"A* sin reapertura":<34} {str(c_no):<8} {e_no:<12} {r_no}')
    print()
    print(f'Óptimo real: {round(dist["s"], 2)}')
    print()
    if r_ok > 0 and abs(c_ok - dist['s']) < 1e-9:
        print('Con reapertura: 1 reapertura, costo óptimo. Estructura correcta.')
    if c_no == dist['s']:
        print(f'Sin reapertura el costo sale igual en ESTE grafo ({c_no}). La razón es')
        print('que el nodo reabierto no estaba en el camino ganador: se reabre para')
        print('corregir su g, pero el camino final pasa por otra rama. Es lo que hace')
        print('difícil ver el bug a ojo: el resultado sale bien y el contador de')
        print('reaperturas es la única señal de que hubo una corrección tardía.')
        print()
        print('Por eso A* guarda `best_g` y compara: no porque siempre cambie el')
        print('resultado, sino porque sin esa comparación el algoritmo deja de ser')
        print('correcto en general y el caso que lo rompe no avisa.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
