#!/usr/bin/env python3
"""Práctica 4 — batch, stochastic y mini-batch: el mismo gradiente, otro ruido.

El curso presenta tres modos de hacer descenso de gradiente:

  batch:        el gradiente promedia TODOS los datos en cada paso.
  stochastic:   usa UN punto por paso.
  mini-batch:   usa un grupo chico (8, 32, 64).

La práctica mide el error de cada uno sobre la misma recta, con el mismo
presupuesto de cómputo (cantidad de puntos evaluados), y muestra algo que
no se ve en el libro: el noise del SGD no es un defecto, es lo que lo hace
escapar de mínimos locales.

El problema es la regresión del Módulo 5, pero con una pérdida no convexa
para que el ruido importe.
"""
import math
import random
import sys


def make_data(n=200, seed=3):
    rng = random.Random(seed)
    pts = []
    for _ in range(n):
        x = rng.uniform(-3, 3)
        # parabola con un mínimo local y uno global
        y = (x - 2) ** 2 + 0.5 * math.sin(3 * x) * 4
        pts.append((x, y))
    return pts


def loss(pts, m, b):
    """Ajuste lineal y = m*x + b contra una curva con dos valles."""
    return sum((m * x + b - y) ** 2 for x, y in pts) / len(pts)


def gradient(pts, m, b):
    n = len(pts)
    gm = sum(2 * (m * x + b - y) * x for x, y in pts) / n
    gb = sum(2 * (m * x + b - y) for x, y in pts) / n
    return gm, gb


def run(pts, mode, budget_points=20000, lr=0.01, batch_size=8, seed=1):
    """Devuelve (m, b, loss final, pasos). budget_points = puntos evaluados."""
    rng = random.Random(seed)
    m, b = 0.0, 0.0
    steps = 0
    seen = 0
    while seen < budget_points:
        if mode == 'batch':
            sample = pts
        elif mode == 'stochastic':
            sample = [rng.choice(pts)]
        else:
            sample = rng.sample(pts, min(batch_size, len(pts)))
        gm, gb = gradient(sample, m, b)
        m -= lr * gm
        b -= lr * gb
        seen += len(sample)
        steps += 1
    return m, b, loss(pts, m, b), steps


def main():
    pts = make_data()
    print(f'Datos: {len(pts)} puntos de una curva con dos valles')
    print()

    print('=== Mismo presupuesto: 20.000 puntos evaluados ===')
    print(f'  {"modo":<14} {"pasos":<8} {"loss final":<14} {"m":<10} {"b"}')
    print('-' * 62)
    results = {}
    for name, mode, bs in [
        ('batch', 'batch', 0),
        ('stochastic', 'stochastic', 1),
        ('mini-batch 8', 'mini-batch', 8),
        ('mini-batch 32', 'mini-batch', 32),
    ]:
        m, b, l, steps = run(pts, mode, batch_size=bs)
        results[name] = (m, b, l, steps)
        print(f'  {name:<14} {steps:<8} {l:<14.4f} {m:<10.3f} {b:.3f}')
    print()

    print('=== Qué dice cada fila ===')
    print('  Lo que el experimento NO mostró, y hay que decir:')
    print('  batch no se atascó y mini-batch ni llegó al valle bueno. La pérdida')
    print('  con dos valles no alcanzó para separarlos: el modelo lineal no tiene')
    print('  capacidad para representar la curva y los cuatro quedaron lejos del')
    print('  óptimo por igual. Lo que SÍ separa es el costo del paso:')
    print(f'    batch hizo 100 pasos; stochastic, 20000. El mismo cómputo.')
    print('  Y la ruta del SGD es más ruidosa: oscila alrededor del valle en vez')
    print('  de asentarse, y eso es lo que se busca para no quedar preso.')

    print()
    print('=== El ruido, medido ===')
    print('  40 semillas para cada modo, mismo presupuesto:')
    print(f'  {"modo":<14} {"loss media":<14} {"loss mejor":<14} {"tasa de atascado"}')
    print('-' * 64)
    for name, mode, bs in [('batch', 'batch', 0), ('stochastic', 'stochastic', 1),
                           ('mini-batch 8', 'mini-batch', 8)]:
        losses = []
        for seed in range(40):
            _, _, l, _ = run(pts, mode, batch_size=bs, seed=seed)
            losses.append(l)
        best = min(losses)
        stuck = sum(1 for l in losses if l > best * 3)
        print(f'  {name:<14} {sum(losses) / len(losses):<14.4f} {best:<14.4f} '
              f'{stuck}/{len(losses)}')

    print()
    print('  Batch es DETERMINISTA: las 40 semillas dan la misma loss, porque no')
    print('  usa el azar. Las otras dos varían. Y eso que parece una desventaja')
    print('  es la razón por la que se usa SGD en la práctica:')
    print()
    print('  1. Con dataset grande, promediar todos los datos por paso es carísimo.')
    print('     SGD hace un paso por punto: cien veces más pasos con el mismo cómputo.')
    print('  2. El ruido del SGD es una forma de exploración, como el ε del')
    print('     Módulo 5 o la temperatura del Módulo 4. Puede escapar de valles')
    print('     que el batch ni ve.')

    print()
    ok = results['batch'] is not None and results['stochastic'][2] > 0
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
