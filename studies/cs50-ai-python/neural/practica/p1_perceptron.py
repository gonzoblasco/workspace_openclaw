#!/usr/bin/env python3
"""Práctica 1 — el perceptrón: no puede con todo, y lo demuestra.

Un perceptrón es una neurona: suma ponderada de las entradas y una activación
con umbral.

    output = 1 si (w·x + b) > 0  sino 0

Un perceptrón **sólo puede dibujar una recta**. Eso alcanza para OR y para AND,
y no alcanza para XOR.

La práctica:
  1. Entrena un perceptrón con la regla del curso.
  2. Lo corre sobre AND, OR y XOR contando los errores.
  3. Muestra que en XOR NO converge: los errores oscilan para siempre.

Ese es el experimento que el curso cuenta (la crítica de Minsky) y que se puede
ver en 20 líneas.
"""
import random
import sys


def activar(z):
    return 1 if z > 0 else 0


def entrenar_perceptron(data, epochs=100, lr=0.1, seed=1):
    """Regla del perceptrón: w += lr * (y - pred) * x."""
    rng = random.Random(seed)
    w = [rng.uniform(-1, 1) for _ in range(len(data[0][0]))]
    b = rng.uniform(-1, 1)
    history = []
    for ep in range(epochs):
        errors = 0
        for x, y in data:
            pred = activar(sum(wi * xi for wi, xi in zip(w, x)) + b)
            err = y - pred
            if err != 0:
                errors += 1
                for i in range(len(w)):
                    w[i] += lr * err * x[i]
                b += lr * err
        history.append(errors)
        if errors == 0:
            return w, b, history, True
    return w, b, history, False


def main():
    AND = [((0, 0), 0), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)]
    OR_ = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)]
    XOR = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]

    print('=== 1. AND, OR y XOR son el mismo tipo de problema ===')
    print(f'  {"función":<8} {"(0,0)":<8} {"(0,1)":<8} {"(1,0)":<8} {"(1,1)":<8}')
    print('-' * 46)
    for name, data in [('AND', AND), ('OR', OR_), ('XOR', XOR)]:
        vals = {x: y for x, y in data}
        print(f'  {name:<8} {vals[(0,0)]:<8} {vals[(0,1)]:<8} '
              f'{vals[(1,0)]:<8} {vals[(1,1)]:<8}')
    print()

    print('=== 2. El perceptrón, entrenado sobre cada uno ===')
    print(f'  {"función":<8} {"errores finales":<18} {"convergió?":<14} pesos')
    print('-' * 72)
    results = {}
    for name, data in [('AND', AND), ('OR', OR_), ('XOR', XOR)]:
        w, b, hist, ok = entrenar_perceptron(data, epochs=200)
        results[name] = (w, b, hist, ok)
        print(f'  {name:<8} {hist[-1]:<18} {"sí" if ok else "NO":<14} '
              f'w={[round(x, 2) for x in w]} b={b:.2f}')
    print()

    print('=== 3. La firma del fracaso: en XOR los errores no bajan ===')
    print('  (los primeros y últimos 6 de 200 epochs)')
    xor_hist = results['XOR'][2]
    and_hist = results['AND'][2]
    print(f'    AND: {and_hist[:6]} ... {and_hist[-6:]}')
    print(f'    XOR: {xor_hist[:6]} ... {xor_hist[-6:]}')
    print()
    print('  AND converge a cero errores en pocas épocas y se queda.')
    print('  XOR NUNCA llega a cero: el perceptrón oscila entre dos')
    print('  soluciones que siempre se equivocan en otros dos puntos.')
    print()
    print('  No es que el entrenamiento sea corto: cualquier recta que separes los')
    print('  dos puntos positivos de XOR deja un punto en el otro lado. **No hay')
    print('  recta**, y el perceptrón sólo puede trazar una.')
    print()
    print('  Esto es lo que Minsky y Papert señalaron en 1969, y lo que frenó el')
    print('  financiamiento de las redes neuronales por una década.')

    print()
    print('=== 4. La salida del perceptrón es lineal ===')
    print('  Para un perceptrón de 2 entradas, la frontera es:')
    print('    w1·x1 + w2·x2 + b = 0')
    print('  Despejando x2:  x2 = -(w1/w2)·x1 - b/w2')
    print('  Es una RECTA. Nunca una curva, nunca una elipse, nunca un círculo.')
    print('  XOR necesita dos rectas. Se resuelve con una capa oculta y nada más:')
    print('    h1 = OR(x1, x2)   h2 = NAND(x1, x2)   y = AND(h1, h2)')
    print('  Esa composición es lo que hace una red multicapa, y lo que el perceptrón')
    print('  simple no puede hacer por más datos u horas que se le den.')

    print()
    ok = results['AND'][3] and results['OR'][3] and not results['XOR'][3]
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
