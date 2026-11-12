#!/usr/bin/env python3
"""Práctica 1 — probabilidad desde cero: 0 a 1, Bayes y la regla del producto.

Todo el módulo descansa en tres identidades. Si una se entiende mal, la red
bayesiana funciona de casualidad y nadie lo nota.

  1. La suma de probabilidades de un espacio exhaustivo es 1.
  2. P(a ∧ b) = P(a) · P(b|a)      regla del producto
  3. P(b) · P(a|b) = P(a) · P(b|a)  de donde sale Bayes

Acá NO se usan librerías: el punto es que estas tres se pueden verificar
contando. Se estima cada probabilidad con frecuencias de un experimento
aleatorio y se comprueba que las identidades se sostienen dentro del ruido.

Sin numpy: la práctica entera corre con la librería estándar.
"""
import random
import sys


def simulate(trials=200_000, seed=7):
    """Experimento: 30% llueve; si llueve, 90% me mojo; si no, 20% me mojo."""
    rng = random.Random(seed)
    rain = wet = both = neither = 0
    for _ in range(trials):
        r = rng.random() < 0.30
        w = rng.random() < (0.90 if r else 0.20)
        rain += r
        wet += w
        both += r and w
        neither += (not r) and (not w)
    n = trials
    return {
        'P(R)': rain / n,
        'P(W)': wet / n,
        'P(R and W)': both / n,
        'P(R or W)': 1 - neither / n,
        'P(R|W)': both / wet,
        'P(W|R)': both / rain,
    }


def close(a, b, tol=0.01):
    return abs(a - b) <= tol


def main():
    print('=== 1. Las probabilidades viven entre 0 y 1 ===\n')
    for k, v in simulate().items():
        ok = 0.0 <= v <= 1.0
        print(f'  {k:<12} {v:.4f}   {"ok" if ok else "FUERA DE RANGO"}')
        if not ok:
            print('FALLA: una probabilidad fuera de [0,1].')
            return 1
    print()

    p = simulate()

    print('=== 2. Exhaustividad: P(R o W) + P(no R y no W) = 1 ===\n')
    total = p['P(R or W)'] + (1 - p['P(R or W)'])
    print(f'  P(R o W) = {p["P(R or W)"]:.4f}')
    print(f'  P(no R y no W) = {1 - p["P(R or W)"]:.4f}')
    print(f'  suma = {total:.4f}   {"ok" if close(total, 1.0) else "FALLA"}')
    print()

    print('=== 3. Regla del producto: P(R y W) = P(R) * P(W|R) ===\n')
    left = p['P(R and W)']
    right = p['P(R)'] * p['P(W|R)']
    print(f'  P(R y W) medido   = {left:.4f}')
    print(f'  P(R) * P(W|R)     = {right:.4f}')
    ok_prod = close(left, right)
    print(f'  {"ok" if ok_prod else "FALLA"}')
    print()

    print('=== 4. Bayes: P(R|W) sale de P(W|R), no al revés ===\n')
    bayes = p['P(W|R)'] * p['P(R)'] / p['P(W)']
    medido = p['P(R|W)']
    print(f'  P(R|W) medido                = {medido:.4f}')
    print(f'  P(W|R)*P(R)/P(W) (Bayes)     = {bayes:.4f}')
    ok_bayes = close(bayes, medido)
    print(f'  {"ok" if ok_bayes else "FALLA"}')
    print()
    print(f'  Y el punto que rompe la intuición:')
    print(f'    P(W|R) = {p["P(W|R)"]:.4f}   (si llueve, casi seguro me mojo)')
    print(f'    P(R|W) = {p["P(R|W)"]:.4f}   (si me mojé, ¿llovió?)')
    print(f'  Son números muy distintos. Confundirlos es el error de base rate:')
    print(f'  la lluvia es rara (30%), así que la mayoría de las veces que te mojaste')
    print(f'  no había llovido. Bayes corrige por cuán común es la causa.')

    print()
    if ok_prod and ok_bayes:
        print('RESULTADO: PASA — las tres identidades se sostienen en la simulación.')
        return 0
    print('RESULTADO: FALLA')
    return 1


if __name__ == '__main__':
    sys.exit(main())
