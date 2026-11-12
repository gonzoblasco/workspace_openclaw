#!/usr/bin/env python3
"""Práctica 4 — holdout cross-validation: la única forma de saber si un modelo sirve.

El curso dice:

  "the key idea is separating the training data from the testing data"

Esta práctica toma el clasificador de p3 y lo evalúa de tres formas:

  1. **Sin separar:** medir sobre los mismos datos con los que se ajustó.
     Da un número alto y no significa nada.
  2. **Holdout simple:** entrenar con el 70%, medir con el 30%.
  3. **k-fold:** partir en k bloques, entrenar con k-1 y medir con el restante.
     Da un número estable y una medida de su variabilidad.

Después aplica lo mismo al caso que el workspace ya adoptó: el gate de citas de
las clases (`heldout.py`). La pregunta es la misma: ¿qué mide un verde cuando el
gate corre sobre los datos con las que se escribió el artefacto?

Esa parte no es metáfora: es el mismo cálculo.
"""
import random
import sys

sys.path.insert(0, '.')
from p1_knn import distance, knn_predict, make_data
from p3_confusion import metrics


def accuracy(pairs):
    if not pairs:
        return 0.0
    return sum(1 for real, pred in pairs if real == pred) / len(pairs)


def holdout(train, test, k=5):
    pairs = []
    for point, label in test:
        pred = knn_predict(train, point, k)
        pairs.append((label, pred))
    return accuracy(pairs)


def kfold(data, k=5, k_nn=5):
    folds = [[] for _ in range(k)]
    for i, item in enumerate(data):
        folds[i % k].append(item)
    scores = []
    for i in range(k):
        test = folds[i]
        train = [x for j, f in enumerate(folds) if j != i for x in f]
        scores.append(holdout(train, test, k_nn))
    return scores


def main():
    data = make_data(n=200, seed=21)
    print(f'Dataset: {len(data)} puntos 2D, dos clases')
    print()

    print('=== 1. Sin separar: medir sobre lo de entrenamiento ===')
    acc_in = holdout(data, data, k=1)
    print(f'  nearest neighbor (k=1) entrenado y medido sobre los mismos puntos:')
    print(f'  accuracy = {acc_in:.4f}')
    print()
    print('  Con k=1, cada punto ES su propio vecino más cercano. El modelo se')
    print('  memoriza a sí mismo y siempre acierta. **Ese 100% no dice si generaliza.**')
    print('  Es el mismo problema que el polinomio de grado 7 de p2.')
    print()

    print('=== 2. Holdout simple (70/30) ===')
    rng = random.Random(1)
    shuffled = data[:]
    rng.shuffle(shuffled)
    cut = int(len(shuffled) * 0.7)
    train, test = shuffled[:cut], shuffled[cut:]
    acc_ho = holdout(train, test, k=5)
    print(f'  accuracy en test = {acc_ho:.4f}')
    print()

    print('=== 3. k-fold (k=5) ===')
    scores = kfold(data, k=5)
    print(f'  particiones: {[f"{s:.4f}" for s in scores]}')
    mean = sum(scores) / len(scores)
    var = sum((s - mean) ** 2 for s in scores) / len(scores)
    print(f'  media = {mean:.4f}   desvío = {var ** 0.5:.4f}')
    print()
    print('  k-fold no da un número mejor: da un número con ERROR CONOCIDO.')
    print('  Un holdout simple puede haber tenido suerte con el corte; k-fold dice')
    print('  cuánto depende del corte.')
    print()

    print('=== 4. La comparación ===')
    print(f'  {"evaluación":<32} {"accuracy":<12} {"creíble?"}')
    print('-' * 62)
    print(f'  {"sobre los mismos datos (k=1)":<32} {acc_in:<12.4f} {"no"}')
    print(f'  {"holdout 70/30":<32} {acc_ho:<12.4f} {"sí"}')
    print(f'  {"5-fold (media)":<32} {mean:<12.4f} {"sí, con varianza"}')
    print()
    print('  La diferencia entre 1.0000 y 0.85 no es de calidad del modelo: es de')
    print('  calidad de la pregunta. Un número medido sobre los datos de entrenamiento')
    print('  no responde "¿este modelo generaliza?".')

    print()
    print('=== 5. Lo mismo, sobre el gate del workspace ===')
    print('  `studies/cs50-ai-python/heldout.py` verifica dos cosas:')
    print('    a) que cada cita del outline exista LITERALMENTE en el transcript,')
    print('    b) que el timestamp sea el inicio del bloque que la contiene.')
    print()
    print('  Ese es el caso correcto: el transcript es un corpus que el outline NO')
    print('  usó como señal para escribirse. Es el test set, y no el train set.')
    print('  Y por eso rechazó 62 de 79 timestamps la primera vez.')
    print()
    print('  Lo que sería el "accuracy sobre train":')
    print('    - un gate que revisa el mismo archivo que escribió (lint de formato)')
    print('    - un test escrito copiando la salida actual del código')
    print('    - un chequeo que nunca se corrió contra un caso que debería fallar')
    print('  Los tres dan verde. Los tres miden si el artefacto es igual a sí mismo.')

    print()
    ok = acc_in > 0.99 and 0.5 < acc_ho < 0.95 and 0.5 < mean < 0.95
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
