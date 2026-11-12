#!/usr/bin/env python3
"""Práctica 2 — funciones de activación: qué decide que la red sea no lineal.

Un perceptrón con umbral es una recta. Para aprender una curva hace falta una
no linealidad. Las tres del curso:

  sigmoid σ(z) = 1 / (1 + e^-z)       suave, 0 a 1
  ReLU  R(z)  = max(0, z)             lineal por tramos
  softmax(z)_i = e^{z_i} / Σ e^{z_j}  una distribución entre varias clases

La práctica muestra cada una, su derivada, y después mide lo importante: una
red SIN activación no lineal es una regresión lineal, por más capas que tenga.

Esa es la afirmación que hay que verificar, y se verifica con álgebra.
"""
import math
import sys


def sigmoid(z):
    return 1 / (1 + math.exp(-z)) if z > -700 else 0.0


def relu(z):
    return max(0.0, z)


def softmax(zs):
    m = max(zs)
    exps = [math.exp(z - m) for z in zs]
    total = sum(exps)
    return [e / total for e in exps]


def d_sigmoid(z):
    s = sigmoid(z)
    return s * (1 - s)


def d_relu(z):
    return 1.0 if z > 0 else 0.0


def main():
    print('=== 1. Las tres activaciones ===')
    print(f'  {"z":<8} {"sigmoid":<12} {"relu":<10} {"d(sigmoid)":<14} {"d(relu)"}')
    print('-' * 60)
    for z in (-3, -2, -1, -0.5, 0, 0.5, 1, 2, 3):
        print(f'  {z:<8} {sigmoid(z):<12.4f} {relu(z):<10.2f} '
              f'{d_sigmoid(z):<14.4f} {d_relu(z):.2f}')
    print()
    print('  Sigmoid: suave, saturada en los extremos. Derivada máxima en 0 (0.25).')
    print('  ReLU: lineal por tramos, derivada 0 o 1. Más barata y sin saturación.')
    print('  En el curso la sigmoid es la que se usa; ReLU es la que usa todo el')
    print('  resto del mundo desde 2011.')
    print()

    print('=== 2. Softmax: la activación de la última capa ===')
    for zs in ([2, 1, 0], [5, 1, 0], [1, 1, 1], [0, 0, 10]):
        p = softmax(zs)
        print(f'  z={str(zs):<14} -> p={[round(v, 4) for v in p]}  suma={sum(p):.4f}')
    print()
    print('  Softmax convierte cualquier vector en una distribución que suma 1.')
    print('  Con z=[1,1,1] da [1/3, 1/3, 1/3]: la red no se decide.')
    print('  Con z=[0,0,10] da casi [0,0,1]: la red está segura.')
    print()

    print('=== 3. La prueba que importa: sin no-linealidad, N capas = 1 capa ===')
    print('  Una capa sin activación calcula:  y = W₂ · (W₁ · x + b₁) + b₂')
    print('  Expandido:                        y = (W₂ W₁) · x + (W₂ b₁ + b₂)')
    print('  Que es exactamente:              y = W · x + b')
    print('  Dos capas lineales son UNA capa lineal. Y eso vale para cualquier N.')
    print()
    # Verificación numérica: red de 2 capas vs una sola capa equivalente
    import random
    rng = random.Random(3)
    W1 = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(4)]
    b1 = [rng.uniform(-1, 1) for _ in range(4)]
    W2 = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(2)]
    b2 = [rng.uniform(-1, 1) for _ in range(2)]

    def matmul(A, v):
        return [sum(a * x for a, x in zip(row, v)) for row in A]

    def net_2layers(x):
        h = [sum(w * xi for w, xi in zip(row, x)) + b for row, b in zip(W1, b1)]
        return [sum(w * hi for w, hi in zip(row, h)) + b for row, b in zip(W2, b2)]

    def matmul_mat(A, B):
        # A (m x n) · B (n x p); B es lista de FILAS de n elementos.
        p = len(B[0])
        n = len(B)
        return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)]
                for i in range(len(A))]

    # y = W2 · (W1 · x + b1) + b2 = (W2 · W1) · x + (W2 · b1 + b2)
    # W1 ya es lista de filas (4 x 3), así que W2·W1 se compone directo.
    W = matmul_mat(W2, W1)
    b = [sum(w * bb for w, bb in zip(row, b1)) + b2i for row, b2i in zip(W2, b2)]

    def net_1layer(x):
        return [sum(w * xi for w, xi in zip(row, x)) + bi for row, bi in zip(W, b)]

    print('  Verificación numérica (3 entradas, 4 ocultas, 2 salidas):')
    print(f'  {"x":<18} {"2 capas lineales":<30} {"1 capa equivalente"}')
    print('-' * 76)
    ok = True
    for x in ([0.1, 0.5, -0.3], [1.0, -1.0, 0.0], [0.3, 0.3, 0.3]):
        a = net_2layers(x)
        c = net_1layer(x)
        same = all(abs(p - q) < 1e-9 for p, q in zip(a, c))
        ok = ok and same
        print(f'  {str(x):<18} {str([round(v, 6) for v in a]):<30} '
              f'{str([round(v, 6) for v in c])}')
    print()
    if ok:
        print('  Idénticas en las tres entradas. La segunda capa no agregó nada.')
    else:
        print('  FALLA: hubo diferencia. El álgebra está mal.')
        return 1
    print()
    print('  Y con una activación no lineal entre las capas, la igualdad se rompe:')
    print('  σ(W₁x) no es una combinación lineal de x, y la red puede representar')
    print('  funciones que la recta no alcanza.')

    print()
    # --- el gradiente que se desvanece -----------------------------------
    print('=== 4. Por qué la sigmoid satura ===')
    print('  La derivada máxima es 0.25, en z=0. Fuera de [-4, 4] es casi cero.')
    print('  En backpropagation los gradientes se MULTIPLICAN capa por capa:')
    for depth in (2, 4, 6, 10):
        grad = 0.25 ** depth
        print(f'    {depth:>2} capas con derivada 0.25 -> gradiente {grad:.2e}')
    print()
    print('  Con 10 capas, el gradiente que llega a la primera es 10^-6 del que')
    print('  salió de la última: la red deja de aprender en las capas de abajo.')
    print('  Es el gradient vanishing. ReLU lo evita porque su derivada es 1, no 0.25,')
    print('  donde la neurona está activa.')

    print()
    ok2 = ok and abs(sum(softmax([1, 1, 1])) - 1) < 1e-12
    print('RESULTADO: PASA' if ok2 else 'RESULTADO: FALLA')
    return 0 if ok2 else 1


if __name__ == '__main__':
    sys.exit(main())
