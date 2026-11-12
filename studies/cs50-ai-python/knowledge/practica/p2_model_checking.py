#!/usr/bin/env python3
"""Práctica 2 — model checking: la definición de entailment, ejecutada.

`KB ⊨ α` significa: en TODO modelo donde KB es verdadera, α también lo es.
No hay interpretación posible donde la base sea cierta y la consulta falsa.

Acá se implementa literalmente:
  1. enumerar los 2^n modelos (asignaciones de verdad a cada símbolo),
  2. quedarse con los modelos donde TODAS las oraciones de KB son verdaderas,
  3. preguntar si α es verdadera en todos ellos.

El caso es el de la clase: Harry visitó Hogwarts, Harry visitó a Hagrid o a
Dumbledore (no a los dos), y no visitó a Hagrid el día de hoy. ¿Visitó a
Dumbledore?

Se mide el costo real: 2^n modelos crece como la peste, y ese es el argumento
del módulo a favor de resolver con reglas de inferencia en vez de enumerar.
"""
import itertools
import sys
import time


# --- Un mini lenguaje de oraciones, en vez de Python crudo -------------------
# Usar Python (`and`, `or`, `not`) y una lambda por oración es correcto pero
# esconde la estructura: no se pueden manipular las oraciones (pasarlas a CNF,
# negarlas, aplicarle resolution). Acá las oraciones son DATOS.
#
# Una oración es una tupla:
#   ('sym', 'P')                    el símbolo proposicional P
#   ('not', s)                      no s
#   ('and', [s1, s2, ...])          conjunción
#   ('or',  [s1, s2, ...])          disyunción
#   ('imp', s1, s2)                 s1 -> s2
#   ('iff', s1, s2)                 s1 <-> s2


def sym(name):
    return ('sym', name)


def NOT(s):
    return ('not', s)


def AND(*ss):
    return ('and', list(ss))


def OR(*ss):
    return ('or', list(ss))


def IMP(a, b):
    return ('imp', a, b)


def IFF(a, b):
    return ('iff', a, b)


def evaluate(s, model):
    """Verdad de una oración bajo un modelo (dict símbolo -> bool)."""
    op = s[0]
    if op == 'sym':
        return model[s[1]]
    if op == 'not':
        return not evaluate(s[1], model)
    if op == 'and':
        return all(evaluate(x, model) for x in s[1])
    if op == 'or':
        return any(evaluate(x, model) for x in s[1])
    if op == 'imp':
        return (not evaluate(s[1], model)) or evaluate(s[2], model)
    if op == 'iff':
        return evaluate(s[1], model) == evaluate(s[2], model)
    raise ValueError(f'operador desconocido: {op}')


def symbols_in(s, acc=None):
    acc = acc if acc is not None else set()
    if s[0] == 'sym':
        acc.add(s[1])
    elif s[0] == 'not':
        symbols_in(s[1], acc)
    elif s[0] in ('and', 'or'):
        for x in s[1]:
            symbols_in(x, acc)
    else:
        symbols_in(s[1], acc)
        symbols_in(s[2], acc)
    return acc


def all_models(sentences):
    """Genera todos los modelos posibles sobre los símbolos en juego."""
    syms = set()
    for s in sentences:
        symbols_in(s, syms)
    ordered = sorted(syms)
    for values in itertools.product([False, True], repeat=len(ordered)):
        yield dict(zip(ordered, values))


def entails(kb, query, verbose=False):
    """Model checking. Devuelve (resultado, modelos_totales, modelos_de_la_kb)."""
    sentences = list(kb) + [query]
    total = 0
    kb_models = 0
    counterexample = None
    for model in all_models(sentences):
        total += 1
        if all(evaluate(s, model) for s in kb):
            kb_models += 1
            if not evaluate(query, model):
                counterexample = model
    if verbose and counterexample:
        print(f'    contraejemplo: {counterexample}')
    return counterexample is None, total, kb_models


# --- El caso de la clase ----------------------------------------------------

HOGWARTS = sym('Hogwarts')
HAGRID = sym('Hagrid')
DUMBLEDORE = sym('Dumbledore')

KB = [
    HOGWARTS,
    OR(AND(HAGRID, NOT(DUMBLEDORE)), AND(NOT(HAGRID), DUMBLEDORE)),
    NOT(HAGRID),
]


def main():
    print('KB:')
    print('  1. Harry visitó Hogwarts')
    print('  2. Harry visitó a Hagrid o a Dumbledore, pero no a los dos')
    print('  3. Harry NO visitó a Hagrid')
    print()
    print('Consulta: ¿visitó a Dumbledore?')
    print()

    result, total, kb_models = entails(KB, DUMBLEDORE)
    print(f'  modelos totales (2^n): {total}')
    print(f'  modelos donde la KB es verdadera: {kb_models}')
    print(f'  ¿KB ⊨ Dumbledore? {"sí — en TODOS los modelos de la KB es verdadera" if result else "no"}')
    print()

    # Y la contracara: una consulta que NO se sigue
    fake = sym('Snape')
    result2, total2, _ = entails(KB, fake, verbose=True)
    print(f'  ¿KB ⊨ Snape? {"sí" if result2 else "no — hay modelos de la KB donde Snape es falso"}')
    print('  Eso es la diferencia entre lo que se deriva y lo que uno quiere creer.')
    print()

    # --- el costo -----------------------------------------------------------
    print('=== El costo de enumerar ===')
    print(f'  {"símbolos":<10} {"modelos":<12} {"tiempo"}')
    for n in range(1, 19):
        syms = [sym(f'P{i}') for i in range(n)]
        kb = [NOT(AND(*syms[:max(1, n - 1)]))]
        t0 = time.perf_counter()
        entails(kb, syms[0])
        dt = (time.perf_counter() - t0) * 1000
        if n in (1, 4, 8, 12, 16, 18):
            print(f'  {n:<10} {2 ** n:<12} {dt:>6.1f} ms')
        if dt > 1500 and n < 18:
            print(f'  (se corta acá: {n} símbolos ya tardan {dt:.0f} ms)')
            break

    print()
    print('  Cada símbolo nuevo duplica el trabajo. Con 30 símbolos son mil millones')
    print('  de modelos: la lógica sigue siendo correcta y el algoritmo ya es inútil.')
    print('  De ahí las reglas de inferencia del módulo: no cambian qué es verdad,')
    print('  cambian cuánto cuesta llegar a saberlo.')
    print()
    print('RESULTADO: PASA' if result and not result2 else 'RESULTADO: FALLA')
    return 0 if result and not result2 else 1


if __name__ == '__main__':
    sys.exit(main())
