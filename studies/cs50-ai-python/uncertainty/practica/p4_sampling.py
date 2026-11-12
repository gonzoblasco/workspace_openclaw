#!/usr/bin/env python3
"""Práctica 4 — sampling: cambiar exactitud por velocidad.

La práctica 3 contesta exacto en 8 mundos. Con 20 variables son un millón;
con 30, mil millones. Sampling abandona la exactitud: mira una muestra y estima.

Tres métodos, del peor al mejor:
  1. Prior sampling: genera muestras de la conjunta y filtra por la evidencia.
     Simple, y desperdicia casi todo si la evidencia es rara.
  2. Rejection sampling: igual, pero descarta explícitamente lo que no coincide.
     Es lo mismo, con nombre.
  3. Likelihood weighting: fija la evidencia y pesa cada muestra por su
     probabilidad. No descarta nada: aprovecha todas las muestras.

Se mide el error de cada uno contra la respuesta exacta, con el mismo presupuesto
de muestras. Eso es todo el argumento.
"""
import random
import sys

sys.path.insert(0, '.')
from p2_red_bayesiana import CPT, PADRES, VARS, VALUES
from p3_enumeracion import enumerate_ask


def sample_from_topological(assignment, rng):
    """Prior sampling: recorre las variables en orden topológico y sortea."""
    a = dict(assignment)
    for var in VARS:                    # VARS ya está en orden topológico
        key = tuple(a[p] for p in PADRES[var])
        dist = CPT[var][key]
        a[var] = 'T' if rng.random() < dist['T'] else 'F'
    return a


def prior_sampling(query, evidence, n=20000, seed=1):
    """Genera n muestras completas y se queda con las que coinciden."""
    rng = random.Random(seed)
    counts = {v: 0 for v in VALUES}
    used = 0
    for _ in range(n):
        a = sample_from_topological(evidence, rng)
        if all(a[k] == v for k, v in evidence.items()):
            counts[a[query]] += 1
            used += 1
    if used == 0:
        return {v: float('nan') for v in VALUES}, used
    return {k: c / used for k, c in counts.items()}, used


def likelihood_weighting(query, evidence, n=20000, seed=1):
    """Fija la evidencia y pondera cada muestra por su probabilidad.

    La clave: cuando una variable es evidencia, NO se sortea: se fija su valor
    y se multiplica el peso por la probabilidad de que tomara ese valor dado
    lo ya asignado. Así todas las muestras sirven.
    """
    rng = random.Random(seed)
    weights = {v: 0.0 for v in VALUES}
    for _ in range(n):
        a = {}
        w = 1.0
        for var in VARS:
            key = tuple(a.get(p) for p in PADRES[var])
            dist = CPT[var][key]
            if var in evidence:
                a[var] = evidence[var]
                w *= dist[evidence[var]]
            else:
                a[var] = 'T' if rng.random() < dist['T'] else 'F'
        weights[a[query]] += w
    total = sum(weights.values())
    if total == 0:
        return {v: float('nan') for v in VALUES}, 0
    return {k: v / total for k, v in weights.items()}, n


def main():
    query, evidence = 'R', {'W': 'T'}
    true, _, _ = enumerate_ask(query, evidence)
    print(f'Verdad exacta: P(R=T | W=T) = {true["T"]:.4f}\n')

    print(f'{"método":<24} {"estimación":<14} {"muestras usadas":<18} {"error absoluto"}')
    print('-' * 76)

    results = {}
    for name, fn in [
        ('prior sampling', prior_sampling),
        ('likelihood weighting', likelihood_weighting),
    ]:
        est, used = fn(query, evidence)
        err = abs(est['T'] - true['T'])
        results[name] = (est, used, err)
        print(f'{name:<24} {est["T"]:<14.4f} {used:<18} {err:.4f}')

    print()
    print('=== Por qué likelihood weighting gana ===')
    prior_used = results['prior sampling'][1]
    print(f'  Prior sampling usó {prior_used} de 20000 muestras ({prior_used / 200:.1f}%).')
    print('  Cada muestra es un mundo completo y sólo sirve si coincide con la')
    print('  evidencia. Con más evidencia, la fracción útil se desploma.')
    print(f'  Likelihood weighting usó las 20000 y pesó cada una.')
    print()

    # --- evidencia rara: ahí se ve el desplome ----------------------------
    print('=== Con evidencia rara, prior sampling se queda sin muestras ===')
    rare = {'S': 'T', 'W': 'T'}      # resbaló Y se mojó
    true2, _, _ = enumerate_ask('R', rare)
    print(f'  Verdad: P(R=T | S=T, W=T) = {true2["T"]:.4f}')
    print()
    print(f'  {"método":<24} {"estimación":<14} {"muestras usadas":<18} {"error"}')
    print('-' * 76)
    for name, fn in [
        ('prior sampling', prior_sampling),
        ('likelihood weighting', likelihood_weighting),
    ]:
        est, used = fn('R', rare)
        err = abs(est['T'] - true2['T'])
        print(f'{name:<24} {est["T"]:<14.4f} {used:<18} {err:.4f}')
    print()
    print('  Con dos condiciones raras simultáneas, prior sampling conserva una')
    print('  fracción minúscula de sus muestras. La estimación se vuelve inútil o')
    print('  directamente imposible ("no vi ningún caso").')
    print('  Likelihood weighting no descarta nada: baja el peso de las muestras')
    print('  improbables. Es la diferencia entre filtrar y ponderar.')
    print()

    lw_err = results['likelihood weighting'][2]
    print('=== La honestidad del método ===')
    print('  Likelihood weighting NO es exacto. Su error baja como 1/sqrt(n):')
    print(f'  con 20000 muestras el error típico es del orden de {1 / 20000 ** 0.5:.4f}.')
    print(f'  Acá dio {lw_err:.4f}. Cuatro ceros decimales de exactitud exigen cien')
    print('  millones de muestras. Sampling es más rápido, no más verdadero.')

    print()
    ok = lw_err < 0.02 and abs(true['T'] + true['F'] - 1) < 1e-9
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
