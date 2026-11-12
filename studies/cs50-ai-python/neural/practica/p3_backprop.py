#!/usr/bin/env python3
"""Práctica 3 — backpropagation a mano, y la verificación numérica.

El curso dice que backpropagation propaga el error hacia atrás. Hacerlo a mano
obliga a entender qué se propaga y por qué.

Red: 2 entradas → 2 ocultas → 1 salida, sigmoid en las tres.

Derivación (cross-entropy binaria + sigmoid, la del curso):
    δ_salida = ŷ - y                      la maravilla del sigmoid + BCE
    δ_oculta = (W₂ᵀ δ_salida) ⊙ σ'(z₁)
    ∂L/∂W₂  = δ_salida · hᵀ
    ∂L/∂W₁  = δ_oculta · xᵀ

**La verificación:** el gradiente analítico tiene que coincidir con el
numérico (diferencia central) en cada peso. Si no coincide en los 9 parámetros,
el backprop está mal.

Esa verificación es lo único que convierte "creo que está bien" en "está bien".
"""
import math
import random
import sys


def sigmoid(z):
    return 1 / (1 + math.exp(-z)) if z > -700 else 0.0


def forward(x, W1, b1, W2, b2):
    """Devuelve (z1, h, z2, y_hat)."""
    # zip(W1, b1) empareja filas de pesos con sesgos; `b` aquí es el sesgo.
    # Antes se llamaba `w` a la fila del zip exterior y shadoweaba el peso.
    z1 = [sum(wi * xi for wi, xi in zip(row, x)) + bias
          for row, bias in zip(W1, b1)]
    h = [sigmoid(z) for z in z1]
    z2 = sum(wi * hi for wi, hi in zip(W2, h)) + b2
    return z1, h, z2, sigmoid(z2)


def loss(x, y, W1, b1, W2, b2):
    """Cross-entropy binaria."""
    _, _, _, yh = forward(x, W1, b1, W2, b2)
    eps = 1e-12
    return -(y * math.log(yh + eps) + (1 - y) * math.log(1 - yh + eps))


def backward(x, y, W1, b1, W2, b2):
    """Gradientes analíticos de todos los parámetros."""
    z1, h, _, yh = forward(x, W1, b1, W2, b2)

    delta_out = yh - y                              # sigmoid + BCE
    dW2 = [delta_out * hi for hi in h]
    db2 = delta_out

    # δ_oculta[k] = (W2[k] · delta_out) · σ'(z1[k])
    delta_h = [W2[k] * delta_out * (h[k] * (1 - h[k])) for k in range(len(h))]
    dW1 = [[delta_h[k] * xi for xi in x] for k in range(len(h))]
    db1 = [d for d in delta_h]

    return dW1, db1, dW2, db2


def numeric_gradient(x, y, W1, b1, W2, b2, eps=1e-5):
    """Diferencia central en cada peso. El oráculo."""
    dW1 = [[0.0] * len(x) for _ in W1]
    db1 = [0.0] * len(b1)
    dW2 = [0.0] * len(W2)
    db2 = 0.0

    for k in range(len(W1)):
        for j in range(len(x)):
            orig = W1[k][j]
            W1[k][j] = orig + eps
            lp = loss(x, y, W1, b1, W2, b2)
            W1[k][j] = orig - eps
            lm = loss(x, y, W1, b1, W2, b2)
            W1[k][j] = orig
            dW1[k][j] = (lp - lm) / (2 * eps)

    for k in range(len(b1)):
        orig = b1[k]
        b1[k] = orig + eps
        lp = loss(x, y, W1, b1, W2, b2)
        b1[k] = orig - eps
        lm = loss(x, y, W1, b1, W2, b2)
        b1[k] = orig
        db1[k] = (lp - lm) / (2 * eps)

    for k in range(len(W2)):
        orig = W2[k]
        W2[k] = orig + eps
        lp = loss(x, y, W1, b1, W2, b2)
        W2[k] = orig - eps
        lm = loss(x, y, W1, b1, W2, b2)
        W2[k] = orig
        dW2[k] = (lp - lm) / (2 * eps)

    orig = b2
    b2 = orig + eps
    lp = loss(x, y, W1, b1, W2, b2)
    b2 = orig - eps
    lm = loss(x, y, W1, b1, W2, b2)
    db2 = (lp - lm) / (2 * eps)
    return dW1, db1, dW2, db2


def xor_net(epochs=20000, lr=2.0, seed=4):
    """Entrena la red de 2-2-1 en XOR. Vuelve (parámetros, historia de loss)."""
    rng = random.Random(seed)
    W1 = [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(2)]
    b1 = [rng.uniform(-1, 1) for _ in range(2)]
    W2 = [rng.uniform(-1, 1) for _ in range(2)]
    b2 = rng.uniform(-1, 1)
    X = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
    hist = []
    for ep in range(epochs):
        total = 0.0
        for x, y in X:
            dW1, db1, dW2, db2 = backward(x, y, W1, b1, W2, b2)
            for k in range(len(W1)):
                for j in range(len(x)):
                    W1[k][j] -= lr * dW1[k][j]
                b1[k] -= lr * db1[k]
            for k in range(len(W2)):
                W2[k] -= lr * dW2[k]
            b2 -= lr * db2
            total += loss(x, y, W1, b1, W2, b2)
        hist.append(total / 4)
        if ep % 500 == 0 and ep:
            if hist[-1] < 1e-4:
                break
    return (W1, b1, W2, b2), hist


def main():
    rng = random.Random(9)
    W1 = [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(2)]
    b1 = [rng.uniform(-1, 1) for _ in range(2)]
    W2 = [rng.uniform(-1, 1) for _ in range(2)]
    b2 = rng.uniform(-1, 1)
    x, y = [0.6, 0.3], 1

    print('=== 1. Backpropagation analítico vs numérico ===')
    dW1, db1, dW2, db2 = backward(x, y, W1, b1, W2, b2)
    nW1, nb1, nW2, nb2 = numeric_gradient(x, y, W1, b1, W2, b2)

    print(f'  entrada x={x}  etiqueta y={y}')
    print()
    print(f'  {"parámetro":<14} {"analítico":<18} {"numérico":<18} {"Δ"}')
    print('-' * 68)
    worst = 0.0
    for k in range(2):
        for j in range(2):
            d = abs(dW1[k][j] - nW1[k][j])
            worst = max(worst, d)
            print(f'  {"W1["+str(k)+","+str(j)+"]":<14} {dW1[k][j]:<18.10f} '
                  f'{nW1[k][j]:<18.10f} {d:.2e}')
    for k in range(2):
        d = abs(db1[k] - nb1[k])
        worst = max(worst, d)
        print(f'  {"b1["+str(k)+"]":<14} {db1[k]:<18.10f} {nb1[k]:<18.10f} {d:.2e}')
    for k in range(2):
        d = abs(dW2[k] - nW2[k])
        worst = max(worst, d)
        print(f'  {"W2["+str(k)+"]":<14} {dW2[k]:<18.10f} {nW2[k]:<18.10f} {d:.2e}')
    d = abs(db2 - nb2)
    worst = max(worst, d)
    print(f'  {"b2":<14} {db2:<18.10f} {nb2:<18.10f} {d:.2e}')
    print()
    print(f'  diferencia máxima: {worst:.2e}')
    if worst > 1e-6:
        print('  FALLA: el gradiente analítico no coincide con el numérico.')
        return 1
    print('  OK  Coinciden en los 9 parámetros. El backprop está bien derivado.')
    print()

    # --- el truco del siglo -----------------------------------------------
    print('=== 2. La simplificación que hace esto tratable ===')
    print('  En la capa de salida:')
    print('    δ = ∂L/∂z₂ = (ŷ - y)')
    print('  Con sigmoid + cross-entropy, la derivada de la activación se CANCELA')
    print('  contra la del loss. No queda σ\'(z) y no hay que calcularla.')
    print()
    print('  Eso no es magia: es la razón por la que cross-entropy reemplazó a')
    print('  error cuadrático en clasificación. Con MSE, δ = (ŷ-y)·σ\'(z), y con')
    print('  σ\' ≤ 0.25 el gradiente se achica un 4x por capa desde el principio.')
    print()

    # --- entrenar XOR -----------------------------------------------------
    print('=== 3. La red de 2-2-1 aprende XOR ===')
    params, hist = xor_net(epochs=4000)
    # renombrar para no pisar las variables del bloque 1 (que se usan abajo)
    W1n, b1n, W2n, b2n = params
    print(f'  loss por época: {hist[0]:.4f} -> {hist[-1]:.6f} '
          f'en {len(hist)} épocas')
    print()
    print(f'  {"x":<10} {"y":<6} {"ŷ":<10} {"predicción"}')
    print('-' * 36)
    for pair in (([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)):
        xv, yv = pair
        _, _, _, yh = forward(xv, W1n, b1n, W2n, b2n)
        print(f'  {str(xv):<10} {yv:<6} {yh:<10.4f} {"1" if yh > 0.5 else "0"}')
    print()
    print('  XOR resuelto con DOS neuronas ocultas. Las dos rectas que el perceptrón')
    print('  no podía dibujar las construye la capa oculta; la salida las combina.')

    print()
    # verificar las salidas
    ok = True
    for pair in (([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)):
        xv, yv = pair
        _, _, _, yh = forward(xv, W1n, b1n, W2n, b2n)
        if (yh > 0.5) != bool(yv):
            ok = False
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
