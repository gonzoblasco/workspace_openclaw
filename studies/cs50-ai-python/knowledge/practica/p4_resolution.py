#!/usr/bin/env python3
"""Práctica 4 — CNF y resolution: probar por contradicción.

Para probar `KB ⊨ α`, resolution no busca afirmaciones: busca una CONTRADICCIÓN
en `KB ∧ ¬α`. Si la hay, α se sigue de KB.

Los cinco pasos, en orden, y cada uno se puede verificar por separado:
  1. Eliminar bicondicionales:  P<->Q  =>  (P->Q) and (Q->P)
  2. Eliminar implicaciones:    P->Q   =>  (not P) or Q
  3. Mover negaciones adentro:  De Morgan
  4. Distribuir:                P and (Q or R) => (P and Q) or (P and R)
  5. Leer las cláusulas: cada disyunción del `and` final es una cláusula

Después, resolution entre cláusulas que comparten un literal opuesto:
  (A or B), (not A or C)  =>  (B or C)      "resolvente"
Si llegás a la cláusula VACÍA, hay contradicción.
"""
import itertools
import sys


# --- oraciones como datos ----------------------------------------------------

def sym(n): return ('sym', n)
def NOT(s): return ('not', s)
def AND(*ss): return ('and', list(ss))
def OR(*ss): return ('or', list(ss))
def IMP(a, b): return ('imp', a, b)
def IFF(a, b): return ('iff', a, b)


def eliminate_iff(s):
    if s[0] == 'sym':
        return s
    if s[0] == 'not':
        return NOT(eliminate_iff(s[1]))
    if s[0] in ('and', 'or'):
        return (s[0], [eliminate_iff(x) for x in s[1]])
    if s[0] == 'iff':
        a, b = eliminate_iff(s[1]), eliminate_iff(s[2])
        return AND(IMP(a, b), IMP(b, a))
    if s[0] == 'imp':
        return IMP(eliminate_iff(s[1]), eliminate_iff(s[2]))
    raise ValueError(s[0])


def eliminate_imp(s):
    if s[0] == 'sym':
        return s
    if s[0] == 'not':
        return NOT(eliminate_imp(s[1]))
    if s[0] in ('and', 'or'):
        return (s[0], [eliminate_imp(x) for x in s[1]])
    if s[0] == 'imp':
        a, b = eliminate_imp(s[1]), eliminate_imp(s[2])
        return OR(NOT(a), b)
    raise ValueError(s[0])


def push_negation(s):
    """De Morgan y doble negación hasta que el `not` toque sólo símbolos."""
    if s[0] == 'sym':
        return s
    if s[0] == 'not':
        inner = s[1]
        if inner[0] == 'sym':
            return s
        if inner[0] == 'not':
            return push_negation(inner[1])           # ~~P = P
        if inner[0] == 'and':
            return OR(*[push_negation(NOT(x)) for x in inner[1]])
        if inner[0] == 'or':
            return AND(*[push_negation(NOT(x)) for x in inner[1]])
    if s[0] in ('and', 'or'):
        return (s[0], [push_negation(x) for x in s[1]])
    raise ValueError(s[0])


def distribute(s):
    """Distribuye OR sobre AND hasta que quede un AND de ORs (CNF)."""
    if s[0] in ('sym', 'not'):
        return s
    if s[0] == 'and':
        return AND(*[distribute(x) for x in s[1]])
    if s[0] == 'or':
        parts = [distribute(x) for x in s[1]]
        # aplanar ORs anidados
        flat = []
        for p in parts:
            if p[0] == 'or':
                flat.extend(p[1])
            else:
                flat.append(p)
        # si algún hijo es un AND, distribuir
        for i, p in enumerate(flat):
            if p[0] == 'and':
                others = [x for j, x in enumerate(flat) if j != i]
                return AND(*[distribute(OR(alt, *others)) for alt in p[1]])
        return OR(*flat)
    raise ValueError(s[0])


def to_cnf(s):
    return distribute(push_negation(eliminate_imp(eliminate_iff(s))))


def clauses(cnf):
    """Lista de cláusulas; cada cláusula es un frozenset de literales.

    Un único literal o una única disyunción es CNF de una cláusula: `not P` no
    viene envuelto en un AND. Aceptarlo es correcto; lo que NO se acepta es un
    OR con un AND adentro.
    """
    if cnf[0] in ('sym', 'not'):
        return [frozenset([_lit(cnf)])]
    if cnf[0] == 'or':
        if any(x[0] == 'and' for x in cnf[1]):
            raise ValueError(f'no está en CNF: OR contiene un AND -> {cnf}')
        return [frozenset(_lit(x) for x in cnf[1])]
    out = []
    for c in cnf[1]:
        if c[0] == 'or':
            if any(x[0] == 'and' for x in c[1]):
                raise ValueError(f'no está en CNF: OR contiene un AND -> {c}')
            lits = c[1]
        else:
            lits = [c]
        out.append(frozenset(_lit(x) for x in lits))
    return out


def _lit(s):
    if s[0] == 'not':
        return ('-', s[1][1])
    return ('+', s[1])


def resolve(c1, c2):
    """Resuelve dos cláusulas. Devuelve la resolvente o None si no aplica."""
    for lit in c1:
        if (lit[0], lit[1]) == ('+', lit[1]) and ('-', lit[1]) in c2:
            rest = (c1 - {lit}) | (c2 - {('-', lit[1])})
            # si la resolvente es una tautología (x y not x), se descarta
            for r in rest:
                if (r[0] == '+' and ('-', r[1]) in rest):
                    return None
            return frozenset(rest)
        if lit[0] == '-' and ('+', lit[1]) in c2:
            rest = (c1 - {lit}) | (c2 - {('+', lit[1])})
            for r in rest:
                if (r[0] == '+' and ('-', r[1]) in rest):
                    return None
            return frozenset(rest)
    return None


def resolution_proof(clauses, verbose=True):
    """Resolución por saturación. Devuelve (derivó_vacía, pasos).

    `pasos` cuenta RESOLVENTES NUEVAS aceptadas, no pares probados: la
    diferencia importa, porque saturar sobre cláusulas viejas genera duplicados
    que no agregan información y hacen ver el algoritmo como más caro de lo que es.
    """
    work = list(clauses)
    tried = set()
    seen = set(work)
    steps = 0
    while True:
        new = []
        for c1, c2 in itertools.combinations(work, 2):
            r = resolve(c1, c2)
            if r is None:
                continue
            pair = (min(c1, c2, key=sorted), max(c1, c2, key=sorted))
            if pair in tried:
                continue
            tried.add(pair)
            steps += 1
            if len(r) == 0:
                if verbose:
                    print(f'    paso {steps}: {_show(c1)} + {_show(c2)} => CLÁUSULA VACÍA')
                return True, steps
            if r not in seen:
                seen.add(r)
                new.append(r)
                if verbose and steps <= 8:
                    print(f'    paso {steps}: {_show(c1)} + {_show(c2)} => {_show(r)}')
        if not new:
            return False, steps
        work.extend(new)


def _show(c):
    if not c:
        return '[]'
    return '{' + ', '.join(('' if o == '+' else 'no ') + n for o, n in sorted(c)) + '}'


def main():
    A, B, C = sym('A'), sym('B'), sym('C')

    # Caso 1: SÍ se sigue. (A or B), (not A or C), (not B or C) |= C
    print('=== Caso 1: KB ⊨ C  (sí se sigue) ===')
    kb = [OR(A, B), OR(NOT(A), C), OR(NOT(B), C)]
    query = C
    cnf_kb = [clauses(to_cnf(s)) for s in kb]
    cnf_q = clauses(to_cnf(NOT(query)))
    all_clauses = [c for group in cnf_kb for c in group] + cnf_q

    print('  KB:  (A or B),  (no A or C),  (no B or C)')
    print('  Consulta: C   ->  negamos y buscamos contradicción')
    print('  Cláusulas:', [_show(c) for c in all_clauses])
    proved, steps = resolution_proof(all_clauses)
    print(f'  derivó la cláusula vacía: {proved}  ({steps} resoluciones)')
    print()

    # Caso 2: NO se sigue. La misma KB, otra consulta
    print('=== Caso 2: KB ⊨ A  (NO se sigue) ===')
    cnf_q = clauses(to_cnf(NOT(A)))
    all_clauses = [c for group in cnf_kb for c in group] + cnf_q
    print('  Consulta: A')
    proved2, steps2 = resolution_proof(all_clauses, verbose=False)
    print(f'  derivó la cláusula vacía: {proved2}  ({steps2} resoluciones)')
    print('  Se agotan todas las resolventes sin contradicción: entonces se puede')
    print('  construir un modelo donde la KB es cierta y A falsa. No es que el')
    print('  motor "no llegó": la ausencia de la cláusula vacía ES la prueba.')
    print()

    # Caso 3: el pipeline CNF sobre una fórmula con bicondicional
    print('=== Caso 3: el pipeline CNF completo ===')
    f = IFF(A, B)
    step1 = eliminate_iff(f)
    step2 = eliminate_imp(step1)
    step3 = push_negation(step2)
    step4 = to_cnf(f)
    print(f'  original:      A <-> B')
    print(f'  sin iff:       {_show_tree(step1)}')
    print(f'  sin imp:       {_show_tree(step2)}')
    print(f'  negaciones in: {_show_tree(step3)}')
    print(f'  CNF:           {_show_tree(step4)}')
    print('  cláusulas:', [_show(c) for c in clauses(step4)])
    print()

    # Caso 4: el que rompe — una fórmula que NO está en CNF si se la fuerza mal
    print('=== Caso 4: la verificación de CNF ===')
    not_cnf = OR(A, AND(B, C))
    cnf_ok = to_cnf(not_cnf)
    print(f'  A or (B and C) => CNF: {_show_tree(cnf_ok)}')
    print('  Si no se distribuye, queda un OR con un AND adentro: no es CNF y')
    print('  `clauses()` lo aceptaría mal produciendo cláusulas incorrectas.')
    print()

    ok = proved and not proved2
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


def _show_tree(s):
    if s[0] == 'sym':
        return s[1]
    if s[0] == 'not':
        return f'no {_show_tree(s[1])}'
    if s[0] in ('and', 'or'):
        op = ' and ' if s[0] == 'and' else ' or '
        return '(' + op.join(_show_tree(x) for x in s[1]) + ')'
    return f'({_show_tree(s[1])} -> {_show_tree(s[2])})'


if __name__ == '__main__':
    sys.exit(main())
