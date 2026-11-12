#!/usr/bin/env python3
"""Práctica 4 — CSP: backtracking vs forward checking, contando nodos.

El ejercicio del outline: resolver el mismo CSP de dos formas y comparar cuánto
trabajo costó cada una. La prueba es que la segunda explore estrictamente menos
y devuelva la misma asignación.

Dos CSP:

  1. **Horarios de examen** (el de la clase). 4 estudiantes, 3 días, restricciones
     de no-coincidencia. Chico, y **el forward checking no gana nada**: la primera
     rama que prueba ya es solución. Ese es el primer resultado honesto, y el que
     más enseña: la inferencia no ayuda donde el backtracking no se equivoca.

  2. **Coloreado de grafo** con 9 nodos y 3 colores. Acá sí hay backtracking de
     verdad, y el forward checking recorta el árbol.

La lección no es "forward checking es mejor". Es que la inferencia sirve cuando
hay errores que cometer, y no antes.
"""
import sys


def make_solver(n, edges, order=None):
    order = order or list(range(n))

    def neighbors(v):
        return [b for a, b in edges if a == v] + [a for a, b in edges if b == v]

    def backtracking(assign=None, count=None, values=None):
        assign = dict(assign or {})
        count = count if count is not None else {'nodes': 0}
        count['nodes'] += 1
        if len(assign) == n:
            return assign, count
        var = next(v for v in order if v not in assign)
        for value in values:
            if all(assign.get(w) != value for w in neighbors(var)):
                assign[var] = value
                result, count = backtracking(assign, count, values)
                if result:
                    return result, count
                del assign[var]
        return None, count

    def forward_checking(assign=None, domains=None, count=None, values=None):
        assign = dict(assign or {})
        domains = {k: list(v) for k, v in
                   (domains or {v: list(values) for v in range(n)}).items()}
        count = count if count is not None else {'nodes': 0, 'prunes': 0}
        count['nodes'] += 1
        if len(assign) == n:
            return assign, count
        var = next(v for v in order if v not in assign)
        for value in domains[var]:
            if any(assign.get(w) == value for w in neighbors(var)):
                continue
            new_domains = {k: list(v) for k, v in domains.items()}
            new_domains[var] = [value]
            assign[var] = value
            ok = True
            for other in neighbors(var):
                if other in assign:
                    continue
                pruned = [d for d in new_domains[other] if d != value]
                count['prunes'] += len(new_domains[other]) - len(pruned)
                new_domains[other] = pruned
                if not pruned:
                    ok = False          # dominio vacío: retroceder AHORA
                    break
            if ok:
                result, count = forward_checking(assign, new_domains, count, values)
                if result:
                    return result, count
            del assign[var]
        return None, count

    return backtracking, forward_checking, neighbors


def run_case(name, n, edges, values, order=None):
    backtracking, forward_checking, _ = make_solver(n, edges, order)
    sol_bt, c_bt = backtracking(values=values)
    sol_fc, c_fc = forward_checking(values=values)

    print(f'=== {name} ===')
    print(f'  {"método":<30} {"nodos":<10} {"podas":<10} solución')
    print('-' * 76)
    print(f'  {"backtracking puro":<30} {c_bt["nodes"]:<10} {"-":<10} {sol_bt}')
    print(f'  {"backtracking + forward":<30} {c_fc["nodes"]:<10} '
          f'{c_fc["prunes"]:<10} {sol_fc}')
    if sol_bt != sol_fc:
        print('  FALLA: no devuelven la misma asignación.')
        return None
    print(f'  OK  misma solución. Factor: {c_bt["nodes"] / c_fc["nodes"]:.2f}x')
    print()
    return c_bt['nodes'], c_fc['nodes']


def main():
    # --- caso 1: horarios (el de la clase) --------------------------------
    labels = ['A', 'B', 'C', 'D']
    days = ['Lun', 'Mar', 'Mie']
    exam_edges = [(0, 1), (1, 2), (2, 3), (0, 3)]
    bt, fc, _ = make_solver(4, exam_edges)
    s1, c1 = bt(values=days)
    s2, c2 = fc(values=days)
    print('=== Horarios de examen (A≠B, B≠C, C≠D, A≠D) ===')
    print(f'  {"método":<30} {"nodos":<10} {"podas":<10} solución')
    print('-' * 76)
    print(f'  {"backtracking puro":<30} {c1["nodes"]:<10} {"-":<10} '
          f'{[s1[i] for i in range(4)]}')
    print(f'  {"backtracking + forward":<30} {c2["nodes"]:<10} '
          f'{c2["prunes"]:<10} {[s2[i] for i in range(4)]}')
    print()
    print('  Acá el forward checking NO gana: la primera rama que prueba ya es')
    print('  solución y el backtracking nunca se equivoca. La inferencia no hace')
    print('  nada porque no hay nada que podar. Ese resultado es el punto:')
    print('  **una poda no mejora un árbol que no tiene ramas muertas**.')
    print()

    # --- caso 2: coloreado de grafo, donde sí hay backtracking ------------
    graph_edges = [
        (0, 3), (0, 4), (0, 8), (1, 5), (1, 7), (2, 7), (2, 8), (3, 4),
        (3, 6), (3, 7), (4, 7), (4, 8), (5, 6), (5, 7), (7, 8),
    ]
    r = run_case('Coloreado de grafo: 9 nodos, 3 colores', 9, graph_edges, [0, 1, 2])
    if r is None:
        return 1
    bt_nodes, fc_nodes = r

    # --- la escala: aquí la diferencia sí crece --------------------------
    print('=== Cuando hay que retroceder, la diferencia crece ===')
    print(f'  {"caso":<34} {"backtracking":<14} {"forward":<10} {"factor"}')
    print('-' * 74)
    print(f'  {"horarios (4, 3 días)":<34} {c1["nodes"]:<14} {c2["nodes"]:<10} '
          f'{c1["nodes"] / c2["nodes"]:.2f}x')
    print(f'  {"coloreado (9, 3 colores)":<34} {bt_nodes:<14} {fc_nodes:<10} '
          f'{bt_nodes / fc_nodes:.2f}x')
    print()
    print('  El horario de 4 estudiantes se resuelve por la primera rama: no hay')
    print('  error que evitar. El coloreado sí tiene ramas muertas, y ahí el')
    print('  forward checking las corta en el momento en que aparecen.')

    print()
    ok = c1['nodes'] == c2['nodes'] and fc_nodes < bt_nodes
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
