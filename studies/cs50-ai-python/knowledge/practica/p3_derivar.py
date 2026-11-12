#!/usr/bin/env python3
"""Práctica 3 — derivar vs enumerar: el mismo resultado, otro costo.

model checking ENCUENTRA: recorre todos los modelos y verifica.
Una regla de inferencia DERIVA: da un paso y produce conocimiento nuevo.

La pregunta de la práctica no es "¿cuál está bien?" — los dos están bien y
deben coincidir siempre. La pregunta es cuánto cuesta cada uno, y cuándo la
diferencia importa.

Se implementan dos reglas:
  Modus ponens          α -> β , α  ⊢  β
  Conjunction elimination  α and β  ⊢  α

Y se mide: cuántos pasos da el encadenamiento para llegar a la consulta, contra
los 2^n modelos del model checking.

Al final se agrega la trampa: una regla que parece válida y no lo es
(afirmar el consecuente). Si el encadenador la usara, derivaría cualquier cosa.
"""
import sys
import time

sys.path.insert(0, '.')
from p2_model_checking import (AND, IMP, NOT, OR, entails, evaluate, sym,
                               symbols_in)


def is_conjunction(s):
    return s[0] == 'and'


def is_implication(s):
    return s[0] == 'imp'


def modus_ponens(kb):
    """Devuelve la lista de nuevos hechos derivables en UN paso."""
    derived = []
    known = set(_atoms(kb))
    for s in kb:
        if is_implication(s):
            ant, cons = s[1], s[2]
            if _render(ant) in known:
                derived.append(cons)
    return derived


def conjunction_elimination(kb):
    derived = []
    for s in kb:
        if is_conjunction(s):
            derived.extend(s[1])
    return derived


def _atoms(kb):
    for s in kb:
        yield _render(s)


def _render(s):
    """Representación canónica, para comparar oraciones por igualdad."""
    if s[0] == 'sym':
        return s[1]
    if s[0] == 'not':
        return ('not', _render(s[1]))
    if s[0] in ('and', 'or'):
        return (s[0], tuple(_render(x) for x in s[1]))
    return (s[0], _render(s[1]), _render(s[2]))


def forward_chain(kb, query, max_steps=200):
    """Encadenamiento hacia adelante: aplica reglas hasta que no haya nada nuevo.

    Devuelve (derivado, pasos, kb_final) donde `pasos` es la cantidad de hechos
    nuevos que se agregaron: la medida del costo de DERIVAR.
    """
    facts = list(kb)
    seen = {_render(f) for f in facts}
    steps = 0
    changed = True
    while changed and steps < max_steps:
        changed = False
        new = modus_ponens(facts) + conjunction_elimination(facts)
        for n in new:
            key = _render(n)
            if key not in seen:
                seen.add(key)
                facts.append(n)
                steps += 1
                changed = True
        if _render(query) in seen:
            break
    return _render(query) in seen, steps, facts


def main():
    A, B, C, D = sym('A'), sym('B'), sym('C'), sym('D')

    # Cadena de 4 pasos: A -> B, B -> C, C -> D, y A.
    KB = [IMP(A, B), IMP(B, C), IMP(C, D), A]

    print('KB:  A->B,  B->C,  C->D,  A')
    print('Consulta: D')
    print()

    # camino 1: derivar
    t0 = time.perf_counter()
    found, steps, facts = forward_chain(KB, D)
    t_derive = (time.perf_counter() - t0) * 1000
    print(f'  DERIVAR (modus ponens encadenado):')
    print(f'    ¿se deriva D? {"sí" if found else "no"}')
    print(f'    hechos nuevos derivados: {steps}  (A->B, B->C, C->D, A son 4 axiomas)')
    print(f'    hechos en la KB final: {len(facts)}')
    print(f'    tiempo: {t_derive:.3f} ms')
    print(f'    trazabilidad: cada hecho nuevo tiene un paso que lo justifica')
    print()

    # camino 2: enumerar
    t0 = time.perf_counter()
    result, total, kb_models = entails(KB, D)
    t_enum = (time.perf_counter() - t0) * 1000
    print(f'  ENUMERAR (model checking):')
    print(f'    ¿KB ⊨ D? {"sí" if result else "no"}')
    print(f'    modelos revisados: {total}')
    print(f'    modelos donde la KB es cierta: {kb_models}')
    print(f'    tiempo: {t_enum:.3f} ms')
    print(f'    trazabilidad: ninguna. Sabés que se sigue, no por qué')
    print()

    if found != result:
        print('FALLA: derivar y enumerar no coinciden. Uno de los dos está roto.')
        return 1
    print('  OK  Los dos caminos dan el mismo resultado. La diferencia es el costo')
    print('      y la trazabilidad, no la verdad.')
    print()

    # --- cuándo la diferencia explota --------------------------------------
    print('=== Con una KB larga ===')
    print(f'  {"cadena":<10} {"pasos (derivar)":<20} {"modelos (enumerar)"}')
    n = 2
    while n <= 20:
        syms = [sym(f'X{i}') for i in range(n)]
        kb = [IMP(syms[i], syms[i + 1]) for i in range(n - 1)] + [syms[0]]
        found, steps, _ = forward_chain(kb, syms[-1])
        print(f'  {n:<10} {steps:<20} {2 ** n}')
        n *= 2
    print()
    print('  Derivar crece lineal en la longitud de la cadena; enumerar, exponencial.')
    print('  Con 20 símbolos: 19 pasos contra 1.048.576 modelos.')

    # --- la trampa ----------------------------------------------------------
    print()
    print('=== La regla que parece válida y no lo es ===')
    print('  Afirmar el consecuente:  A->B , B  ⊢  A')
    print()
    # Construir el "motor" con la regla inválida y ver qué deriva
    kb = [IMP(A, B), B]
    known_B = _render(B)
    fake_derived = []
    for s in kb:
        if is_implication(s) and _render(s[2]) == known_B:
            fake_derived.append(s[1])
    real, _, _ = entails(kb, A)
    print(f'  con la regla inválida se derivaría: A   ({"deriva" if fake_derived else "no deriva"})')
    print(f'  ¿A se sigue de verdad? {"sí" if real else "NO"}')
    if fake_derived and not real:
        print('  OK  La regla inválida deriva algo que no se sigue.')
        print('      Es el error que hace que un gate "derive" que un cambio es seguro')
        print('      porque el chequeo pasó, sin que el chequeo cubra ese caso.')
        print('      De "si llueve me mojo" + "me mojé" no se sigue "llovió".')
        return 0
    print('  FALLA: el caso trampa no se comportó como se esperaba.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
