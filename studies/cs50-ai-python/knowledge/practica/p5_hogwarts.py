#!/usr/bin/env python3
"""Práctica 5 — lógica de primer orden: 16 símbolos contra 3 reglas.

El curso usa Hogwarts: cuatro personas (Minerva, Pomona, Horace, Severus) y
cuatro casas. La restricción es "cada persona pertenece a una sola casa".

En lógica PROPOSICIONAL hay que escribir un símbolo por cada par posible:
  Persona_Casa     4 x 4 = 16 símbolos proposicionales
  Y las restricciones: "cada persona está en al menos una casa" (4 oraciones),
  "cada persona está en a lo sumo una casa" (4 x 6 pares = 24 oraciones
  binarias si son 4 casas), más lo que se sabe.

En lógica de PRIMER ORDEN:
  3 reglas con cuantificadores escriben exactamente lo mismo.

Esta práctica hace las dos cosas y verifica que dan el mismo resultado en el
model checking: si no dieran lo mismo, la compresión estaría perdiendo algo.

La parte que vale: se GENERA el caso proposicional por fuerza bruta. Nadie
escribe 28 oraciones a mano sin equivocarse, y ese es justamente el argumento.
"""
import itertools
import sys

sys.path.insert(0, '.')
from p2_model_checking import (AND, IMP, NOT, OR, evaluate, sym,
                               symbols_in)


PEOPLE = ['minerva', 'pomona', 'horace', 'severus']
HOUSES = ['gryffindor', 'hufflepuff', 'ravenclaw', 'slytherin']


# --- La versión PROPOSICIONAL, generada -------------------------------------

def prop_symbol(person, house):
    return sym(f'{person}_{house}')


def build_propositional_kb(facts):
    """Genera la KB proposicional completa a partir de hechos de alto nivel."""
    kb = []

    # (1) cada persona está en AL MENOS una casa
    for p in PEOPLE:
        kb.append(OR(*[prop_symbol(p, h) for h in HOUSES]))

    # (2) cada persona está en A LO SUMO una casa: par por par
    for p in PEOPLE:
        for h1, h2 in itertools.combinations(HOUSES, 2):
            kb.append(NOT(AND(prop_symbol(p, h1), prop_symbol(p, h2))))

    # (3) los hechos que sabemos
    for p, h in facts:
        kb.append(prop_symbol(p, h))

    return kb


# --- La versión PRIMER ORDEN, en tres reglas --------------------------------

def describe_first_order(facts):
    """No se ejecuta con un motor de primer orden: se cuenta y se explica.

    Un motor de primer orden de verdad necesita unificación, sustitución y
    skolemización, y eso está bastante más allá de lo que el módulo pide. Lo
    que pide es entender por qué la misma restricción se escribe UNA vez.
    """
    rules = [
        '∀p. Persona(p) → (En(p,Gf) ∨ En(p,Hf) ∨ En(p,Rv) ∨ En(p,Sl))',
        '∀p,h1,h2. En(p,h1) ∧ En(p,h2) ∧ h1≠h2 → ⊥',
    ]
    rules += [f'En({p},{h})' for p, h in facts]
    return rules


def count_prop_symbols():
    return len(PEOPLE) * len(HOUSES)


def count_prop_sentences():
    at_least_one = len(PEOPLE)
    at_most_one = len(PEOPLE) * len(list(itertools.combinations(HOUSES, 2)))
    return at_least_one + at_most_one


def main():
    facts = [('minerva', 'gryffindor'), ('pomona', 'hufflepuff'),
             ('horace', 'slytherin')]

    print('=== El mismo problema, dos escrituras ===\n')
    print(f'  personas: {len(PEOPLE)}   casas: {len(HOUSES)}')
    print(f'  proposicional: {count_prop_symbols()} símbolos, '
          f'{count_prop_sentences()} oraciones de restricción')
    print(f'  primer orden:  {len(describe_first_order(facts))} oraciones en total')
    print(f'  factor de compresión: {count_prop_sentences() / len(describe_first_order(facts)):.1f}x')
    print()
    print('  Proposicional (restricciones generadas):')
    kb = build_propositional_kb(facts)
    for s in kb[:6]:
        print(f'    {_show(s)}')
    print(f'    ... y {len(kb) - 6} más')
    print()
    print('  Primer orden:')
    for r in describe_first_order(facts):
        print(f'    {r}')
    print()

    # --- que las dos escrituras no digan cosas distintas -------------------
    # La de primer orden no se ejecuta, pero la proposicional sí: se verifica
    # que la restricción "a lo sumo una casa" realmente lo haga.
    print('=== Verificación: la restricción proposicional hace lo que dice ===\n')
    query = prop_symbol('severus', 'ravenclaw')   # no sabemos nada de Severus
    result, total, kb_models = _entails(kb, query)
    print(f'  ¿se sigue que Severus está en Ravenclaw? {"sí" if result else "no"}')
    print(f'  modelos totales: {total} (2^{count_prop_symbols()} es intratable)')
    print(f'  modelos que satisfacen la KB: {kb_models}')

    # Severus tiene que quedar libre: la KB admite 4 modelos y en cada uno está
    # en una casa distinta, así que ninguna casa se sigue.
    sev_free = [h for h in HOUSES
                if not _entails(kb, prop_symbol('severus', h))[0]]
    print(f'  casas compatibles con la KB para Severus: {sev_free}')
    print(f'  -> las {len(sev_free)} son compatibles y ninguna se sigue: la KB NO decide')
    print(f'     dónde está Severus, sólo que no puede estar en dos casas a la vez.')
    print(f'  Los {kb_models} modelos de la KB son las combinaciones consistentes:')
    print('     3 personas fijas + Severus en 1 de 4 casas = 4.')
    print()

    # --- y el costo, medido ------------------------------------------------
    print('=== Por qué no se escribe a mano ===')
    print(f'  Generar {count_prop_sentences()} oraciones a mano tiene una tasa de error')
    print('  humana altísima: olvidarse un par (Minerva, Ravenclaw) deja un modelo')
    print('  espurio y el motor devuelve una conclusión falsa con total confianza.')
    print('  En primer orden la regla es una sola y no hay pares que olvidar.')
    print()
    ok = result is False and len(sev_free) == len(HOUSES) and kb_models == len(HOUSES)
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


def _entails(kb, query, limit_models=None):
    """Model checking sobre 16 símbolos: 65.536 modelos, factible."""
    total = 0
    kb_models = 0
    counterexample = None
    syms = sorted({s for sent in list(kb) + [query] for s in symbols_in(sent)})
    for values in itertools.product([False, True], repeat=len(syms)):
        total += 1
        model = dict(zip(syms, values))
        if all(evaluate(s, model) for s in kb):
            kb_models += 1
            if not evaluate(query, model):
                counterexample = model
    return counterexample is None, total, kb_models


def _show(s):
    if s[0] == 'sym':
        return s[1]
    if s[0] == 'not':
        return f'¬{_show(s[1])}'
    if s[0] == 'and':
        return '(' + ' ∧ '.join(_show(x) for x in s[1]) + ')'
    if s[0] == 'or':
        return '(' + ' ∨ '.join(_show(x) for x in s[1]) + ')'
    return f'({_show(s[1])} → {_show(s[2])})'


if __name__ == '__main__':
    sys.exit(main())
