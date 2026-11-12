#!/usr/bin/env python3
"""Práctica 5 — A* fuera del laberinto: un agente que elige herramientas.

La pregunta del módulo, traducida al workspace: cuando un agente decide qué
herramienta usar, ¿dónde está su g y dónde su h?

Modelo:
  nodo   = estado del trabajo ("necesito mirar el repo", "ya leí", ...)
  acción = una herramienta (grep, read, spawn, razonar)
  costo  = pasos + penalidad de las herramientas caras
  g(n)   = lo ya gastado
  h(n)   = estimación de lo que falta

El grafo tiene a propósito un estado trampa: después de leer un archivo, el
camino barato (`razonar` directo) NO alcanza, porque la respuesta tiene que
estar verificada. `razonar` desde `archivo_leido` lleva a `respuesta_rapida`,
que es un estado distinto de `respuesta`: parece la meta pero no lo es.

Ahí está el punto: la heurística honesta distingue `respuesta_rapida` de
`respuesta` (le faltan 2 pasos); la inflada los confunde y declara victoria antes
de verificar. No es velocidad: es un plan distinto con menos control.
"""
import heapq
import sys

WORK = {
    'pregunta': [
        ('grep  (barato, estrecho)', 'candidatos', 1),
        ('read  (caro, completo)', 'archivo_leido', 3),
        ('spawn (muy caro)', 'subagente', 8),
    ],
    'candidatos': [
        ('read  (confirmar)', 'archivo_leido', 2),
    ],
    'subagente': [
        ('esperar sin verificar', 'respuesta_rapida', 4),
    ],
    'archivo_leido': [
        ('razonar sin verificar', 'respuesta_rapida', 2),
        ('grep  (verificar en el repo)', 'verificado', 1),
    ],
    'verificado': [
        ('razonar', 'respuesta', 1),
    ],
    'respuesta_rapida': [
        ('verificar tarde', 'respuesta', 3),
    ],
    'respuesta': [],
}

# Costo REAL de cada nodo hasta `respuesta`
TRUE = {'pregunta': 5, 'candidatos': 4, 'subagente': 7, 'archivo_leido': 2,
        'verificado': 1, 'respuesta_rapida': 3, 'respuesta': 0}


def search(start, goal, h, weight=1.0):
    frontier = [(weight * h[start], 0, start, [])]
    best = {start: 0}
    expanded = 0
    while frontier:
        f, g, node, path = heapq.heappop(frontier)
        if g > best.get(node, float('inf')):
            continue
        expanded += 1
        if node == goal:
            return g, expanded, path
        for action, nxt, cost in WORK[node]:
            ng = g + cost
            if ng < best.get(nxt, float('inf')):
                best[nxt] = ng
                plan = path + [action]
                heapq.heappush(frontier, (ng + weight * h[nxt], ng, nxt, plan))
    return None, expanded, []


def main():
    h0 = {k: 0 for k in WORK}
    greedy_h = {k: 10 for k in WORK}   # cree que todo está a un paso
    greedy_h['respuesta'] = 0
    greedy_h['respuesta_rapida'] = 0   # y confunde la trampa con la meta

    print('Agente eligiendo herramientas (A* sobre el grafo de trabajo)\n')
    print(f'{"h del agente":<36} {"costo":<7} {"expandidos":<12} plan')
    print('-' * 110)
    for name, h, w in [
        ('h=0 (no sabe nada)', h0, 1.0),
        ('h real mínima (admisible)', TRUE, 1.0),
        ('h inflada: confunde rápido con listo', greedy_h, 1.0),
    ]:
        cost, exp, plan = search('pregunta', 'respuesta', h, w)
        print(f'{name:<36} {cost:<7} {exp:<12} {" -> ".join(plan)}')

    print()
    print('Con h honesta el agente verifica antes de responder (costo 5, óptimo).')
    print('Con h inflada se saltea la verificación, declara listo y después paga 3 más:')
    print('total 8. No es más rápido, es un plan distinto con menos control. Ese es el')
    print('costo real de una heurística no admisible: la garantía, no la velocidad.')


if __name__ == '__main__':
    sys.exit(main())
