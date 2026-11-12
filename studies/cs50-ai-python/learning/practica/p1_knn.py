#!/usr/bin/env python3
"""Práctica 1 — clasificación: el vecino más cercano y su maldición.

Supervised learning: se le dan pares entrada-salida y aprende una función.

  nearest neighbor: la etiqueta es la del punto más cercano del entrenamiento.
  k-nearest: la mayoría de los k vecinos.

El primer algoritmo de clasificación de todos. No aprende nada explícito: guarda
los datos y busca al momento de clasificar. Eso tiene una consecuencia inmediata
y otra que aparece recién al crecer las dimensiones.

Esta práctica:
  1. Clasifica 2D y dibuja la frontera de decisión (en ASCII).
  2. Muestra cómo k cambia la frontera: k=1 memoriza, k=51 dibuja recta.
  3. Mide la maldición de la dimensionalidad: con más dimensiones, los vecinos
     más cercanos dejan de ser cercanos.
"""
import math
import random
import sys


def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def knn_predict(train, point, k=1):
    ranked = sorted(train, key=lambda t: distance(t[0], point))
    votes = {}
    for x, label in ranked[:k]:
        votes[label] = votes.get(label, 0) + 1
    return max(votes, key=votes.get)


def make_data(n=120, seed=5):
    rng = random.Random(seed)
    data = []
    for _ in range(n):
        x = rng.uniform(0, 10)
        y = rng.uniform(0, 10)
        # dos clases separadas por una recta inclinada, con ruido
        label = '+' if y > 0.8 * x - 1.5 + rng.gauss(0, 1.2) else '-'
        data.append(((x, y), label))
    return data


def draw_boundary(train, k, w=40, h=18):
    grid = []
    for j in range(h):
        row = []
        for i in range(w):
            p = (i * 10 / (w - 1), (h - 1 - j) * 10 / (h - 1))
            row.append(knn_predict(train, p, k))
        grid.append(''.join(row))
    return '\n'.join(grid)


def curse_of_dimensionality(dims, n=2000, seed=1):
    """En d dimensiones, ¿qué tan lejos está el vecino más cercano?

    Se normaliza a [0,1]^d. Si el vecino más cercano está a una distancia que
    crece con d, entonces "cercano" deja de tener sentido.
    """
    rng = random.Random(seed)
    pts = [tuple(rng.random() for _ in range(dims)) for _ in range(n)]
    q = tuple(rng.random() for _ in range(dims))
    ds = sorted(distance(p, q) for p in pts)
    return ds[0], ds[-1]


def main():
    train = make_data()
    print('=== Nearest neighbor: la frontera de decisión ===')
    print('  datos 2D, dos clases separadas por una recta inclinada (con ruido)')
    print()
    print('k=1  (memoriza cada punto)')
    print(draw_boundary(train, 1))
    print()
    print('k=15 (frontera más suave)')
    print(draw_boundary(train, 15))
    print()
    print('  Con k=1, cada punto de entrenamiento crea su propia isla: la frontera')
    print('  se retuerce alrededor del ruido. Con k=15, los errores sueltos se')
    print('  ahogan en la mayoría de sus vecinos.')
    print()

    # --- la maldición -----------------------------------------------------
    print('=== La maldición de la dimensionalidad ===')
    print(f'  {"dims":<8} {"vecino más cercano":<22} {"vecino más lejano":<20} {"ratio"}')
    print('-' * 68)
    rows = []
    for d in (1, 2, 5, 10, 50, 100, 500):
        # con 2000 muestras en alta dimensión el punto de consulta puede coincidir
        # con una muestra y dar distancia 0. Se usa una muestra distinta por dimensión.
        nearest, farthest = curse_of_dimensionality(d, n=400)
        ratio = nearest / farthest
        rows.append((d, nearest, ratio))
        print(f'  {d:<8} {nearest:<22.4f} {farthest:<20.4f} {ratio:.3f}')
    print()
    print(f'  Con 1 dimensión el vecino más cercano está ~{1 / max(rows[0][2], 1e-9):.0f}x')
    print('  más cerca que el más lejano. Con 100 dimensiones, la diferencia es ~1.5x.')
    print('  Con 500, casi no hay diferencia: todos los puntos están a la misma')
    print('  distancia y "el más cercano" pierde sentido.')
    print()
    print('  Eso mata al nearest neighbor en alta dimensión: "el más cercano" deja')
    print('  de ser una noción útil. Y no es un problema del algoritmo: es del')
    print('  espacio. Ningún algoritmo basado en distancia escapa de eso.')

    print()
    # la propiedad correcta: el ratio CRECE con la dimensión y tiende a 1
    growing = all(rows[i][2] < rows[i + 1][2] for i in range(len(rows) - 1))
    ok = growing and rows[-1][2] > 0.6
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
