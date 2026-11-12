#!/usr/bin/env python3
"""Práctica 6 — minimax y alpha-beta: el rival también decide.

Dos preguntas que se responden corriendo, no leyendo:

  1. ¿Qué pasa con la poda si el árbol está MAL ordenado (peores movimientos
     primero)? ¿Y si está bien ordenado?
  2. ¿Cuántas hojas explora en el mejor caso un árbol de profundidad d y factor b?
     La respuesta de la clase es b^(d/2) en vez de b^d.

Medimos las tres cosas en el mismo árbol: valor de la raíz, hojas visitadas, y
poda. Cambiar el orden de los hijos NO puede cambiar el valor de la raíz (esa es
la garantía), pero sí puede cambiar cuánto trabajo costó. Si el valor cambiara,
alpha-beta estaría mal implementado.
"""
import sys

# Árbol de juguete: cada nodo es (turno, [hijos]).
# turno 'max' = jugamos nosotros, 'min' = el rival.
# Hoja = número (la utilidad).

TREE = ('max', [
    ('min', [
        ('max', [('min', [3, 12, 8]), ('min', [2, 4, 6]), ('min', [14, 5, 2])]),
        ('max', [('min', [5, 6, 7]), ('min', [8, 9, 10]), ('min', [11, 12, 13])]),
        ('max', [('min', [1, 2, 3]), ('min', [4, 5, 6]), ('min', [7, 8, 9])]),
    ]),
    ('min', [
        ('max', [('min', [10, 4, 13]), ('min', [3, 8, 1]), ('min', [6, 7, 2])]),
        ('max', [('min', [9, 8, 7]), ('min', [5, 5, 5]), ('min', [2, 1, 0])]),
        ('max', [('min', [12, 11, 10]), ('min', [4, 3, 2]), ('min', [1, 0, 0])]),
    ]),
    ('min', [
        ('max', [('min', [8, 6, 7]), ('min', [5, 3, 4]), ('min', [2, 1, 3])]),
        ('max', [('min', [7, 7, 7]), ('min', [6, 5, 6]), ('min', [1, 4, 2])]),
        ('max', [('min', [9, 12, 10]), ('min', [11, 10, 12]), ('min', [3, 2, 1])]),
    ]),
])


class Counter:
    def __init__(self):
        self.leaves = 0
        self.nodes = 0
        self.pruned = 0


def is_leaf(node):
    return not isinstance(node, tuple) or len(node) != 2 or not isinstance(node[1], list)


def minimax(node, c):
    c.nodes += 1
    if is_leaf(node):
        c.leaves += 1
        return node
    turn, children = node
    values = [minimax(ch, c) for ch in children]
    return max(values) if turn == 'max' else min(values)


def alpha_beta(node, alpha, beta, c):
    c.nodes += 1
    if is_leaf(node):
        c.leaves += 1
        return node
    turn, children = node
    if turn == 'max':
        v = float('-inf')
        for ch in children:
            v = max(v, alpha_beta(ch, alpha, beta, c))
            alpha = max(alpha, v)
            if beta <= alpha:
                c.pruned += len(children) - children.index(ch) - 1
                break
        return v
    v = float('inf')
    for ch in children:
        v = min(v, alpha_beta(ch, alpha, beta, c))
        beta = min(beta, v)
        if beta <= alpha:
            c.pruned += len(children) - children.index(ch) - 1
            break
    return v


def reorder(node, worst_first):
    """Reordena los hijos de cada nodo para la PODA, no para el resultado.

    En un nodo max conviene explorar primero al hijo de mayor valor; en un nodo
    min, al de menor. `worst_first=True` hace lo contrario en los dos: el orden
    más caro posible para alpha-beta. Los valores no cambian nunca.
    """
    if is_leaf(node):
        return node
    turn, children = node
    reordered = [(minimax(ch, Counter()), i, reorder(ch, worst_first))
                 for i, ch in enumerate(children)]
    # Orden útil para la poda: en max, de mayor a menor; en min, de menor a mayor.
    # `worst_first` invierte ambos.
    if worst_first:
        reordered.sort(key=lambda t: t[0] if turn == 'max' else -t[0])
    else:
        reordered.sort(key=lambda t: -t[0] if turn == 'max' else t[0])
    return (turn, [ch for _, _, ch in reordered])


def main():
    total_leaves = sum(1 for _ in _leaves(TREE))
    print(f'Árbol: profundidad 4, factor ~3, {total_leaves} hojas\n')
    print(f'{"variante":<34} {"valor raíz":<12} {"nodos":<8} {"hojas":<8} {"podadas"}')
    print('-' * 78)

    rows = []
    for name, tree in [
        ('minimax sin poda', TREE),
        ('alpha-beta orden original', TREE),
        ('alpha-beta mejor primero', reorder(TREE, False)),
        ('alpha-beta peor primero', reorder(TREE, True)),
    ]:
        c = Counter()
        if 'sin poda' in name:
            v = minimax(tree, c)
        else:
            v = alpha_beta(tree, float('-inf'), float('inf'), c)
        rows.append((name, v, c))
        print(f'{name:<34} {v:<12} {c.nodes:<8} {c.leaves:<8} {c.pruned}')

    print()
    values = {r[2] and r[1] for r in rows}
    if len(values) == 1:
        print(f'OK: las cuatro variantes dan el mismo valor de raíz ({rows[0][1]}).')
        print('   El orden cambia el trabajo, nunca el resultado. Eso es la garantía')
        print('   de alpha-beta: poda sin perder la respuesta.')
    else:
        print(f'FAIL: el valor de la raíz cambió según el orden ({values}). Alpha-beta está mal.')

    best = next(r for r in rows if 'mejor primero' in r[0])
    worst = next(r for r in rows if 'peor primero' in r[0])
    print()
    print(f'Orden útil para la poda: {best[2].leaves} hojas. Orden adverso: {worst[2].leaves} hojas.')
    print(f'Rango: entre {best[2].leaves} y {worst[2].leaves} hojas para el mismo árbol.')
    print('La poda depende del orden de los hijos, no del tamaño del árbol.')
    print('Con orden perfecto se explora ~b^(d/2) en vez de b^d; con orden adverso,')
    print('alpha-beta se degrada hacia el minimax completo.')
    print()
    print('Para el workspace: cuando un plan de revisión A/B evalúa primero el caso')
    print('más probable de fallar, poda el resto con pocas evaluaciones. Evaluar')
    print('primero los casos triviales es el peor orden: gasta todo y no descarta.')


def _leaves(node):
    if is_leaf(node):
        yield node
        return
    for ch in node[1]:
        yield from _leaves(ch)


if __name__ == '__main__':
    sys.exit(main())
