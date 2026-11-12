#!/usr/bin/env python3
"""Práctica 3 — la matriz de confusión: por qué la precisión sola miente.

El curso evalúa un clasificador mirando sensibilidad, especificidad, precisión,
recall, F1 y el costo de los errores. La práctica arma la matriz de confusión
sobre un problema con **clase desbalanceada**, y muestra todas esas métricas.

Y después hace lo importante: muestra que un clasificador **inútil** (que dice
"todo negativo") tiene 99% de precisión. Con ese número, cualquiera lo adopta.

Ese es el mismo error de tasa base del Módulo 3, aplicado a un clasificador.
"""
import random
import sys


def make_dataset(n=2000, prevalence=0.01, seed=4):
    """Clase + rara (prevalence). Devuelve [(label_real, label_predicho)]."""
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        real = '+' if rng.random() < prevalence else '-'
        rows.append(real)
    return rows


def predict_majority(rows):
    """Clasificador trivial: siempre predice '-'. No mira nada."""
    return [(real, '-') for real in rows]


def predict_with_signal(rows, sensitivity=0.90, specificity=0.95, seed=5):
    """Clasificador con la sensibilidad/especificidad del Módulo 3."""
    rng = random.Random(seed)
    out = []
    for real in rows:
        if real == '+':
            pred = '+' if rng.random() < sensitivity else '-'
        else:
            pred = '-' if rng.random() < specificity else '+'
        out.append((real, pred))
    return out


def metrics(pairs):
    tp = sum(1 for r, p in pairs if r == '+' and p == '+')
    fp = sum(1 for r, p in pairs if r == '-' and p == '+')
    fn = sum(1 for r, p in pairs if r == '+' and p == '-')
    tn = sum(1 for r, p in pairs if r == '-' and p == '-')
    total = tp + fp + fn + tn
    acc = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else float('nan')
    recall = tp / (tp + fn) if (tp + fn) else float('nan')
    spec = tn / (tn + fp) if (tn + fp) else float('nan')
    f1 = (2 * precision * recall / (precision + recall)
          if precision and recall else 0.0)
    return {'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
            'accuracy': acc, 'precision': precision, 'recall': recall,
            'specificity': spec, 'f1': f1, 'total': total}


def show(name, m):
    print(f'  {name}')
    print(f'    matriz:  TP={m["tp"]:<5} FP={m["fp"]:<5}')
    print(f'             FN={m["fn"]:<5} TN={m["tn"]:<5}')
    print(f'    accuracy={m["accuracy"]:.4f}  precision={m["precision"]:.4f}  '
          f'recall={m["recall"]:.4f}  specificity={m["specificity"]:.4f}  '
          f'F1={m["f1"]:.4f}')
    print()


def main():
    # Problema: detección de un caso raro (1% de los casos son positivos)
    rows = make_dataset(n=2000, prevalence=0.01)
    positives = sum(1 for r in rows if r == '+')
    print(f'Dataset: {len(rows)} casos, {positives} positivos '
          f'(prevalencia {positives / len(rows):.1%})')
    print()

    print('=== Clasificador trivial: "todo negativo" ===')
    show('siempre predice -', metrics(predict_majority(rows)))
    m0 = metrics(predict_majority(rows))
    print(f'  **{m0["accuracy"]:.1%} de precisión**, y no detecta NI UN caso positivo.')
    print(f'  recall = {m0["recall"]:.2f}, F1 = {m0["f1"]:.2f}')
    print('  La precisión sola no distingue "acierta casi todo" de "no hace nada".')
    print()

    print('=== Clasificador con señal (sensibilidad 0.90, especificidad 0.95) ===')
    m1 = metrics(predict_with_signal(rows))
    show('con señal', m1)
    print(f'  Detecta {m1["recall"]:.0%} de los positivos y acierta {m1["accuracy"]:.1%}.')
    print(f'  Pero de cada {m1["tp"] + m1["fp"]} veces que dice "positivo", '
          f'sólo {m1["precision"]:.0%} lo son.')
    print()

    print('=== La comparación ===')
    print(f'  {"modelo":<24} {"accuracy":<12} {"recall":<10} {"precision":<12} {"F1"}')
    print('-' * 72)
    print(f'  {"trivial (todo negativo)":<24} {m0["accuracy"]:<12.4f} '
          f'{m0["recall"]:<10.1f} {m0["precision"]:<12.1f} {m0["f1"]:.3f}')
    print(f'  {"con señal":<24} {m1["accuracy"]:<12.4f} '
          f'{m1["recall"]:<10.4f} {m1["precision"]:<12.4f} {m1["f1"]:.3f}')
    print()
    print('  El trivial GANA en accuracy (99.2% contra 95.5%) y PIERDE en todo lo demás.')
    print('  Si hubieras elegido el modelo por accuracy, habrías descartado el único')
    print('  que detecta algo.')
    print()

    print('=== Qué métrica usar, y por qué ===')
    print('  - **recall** (sensibilidad): de los casos raros reales, cuántos detecté.')
    print('    Es la métrica cuando un falso negativo cuesta caro (diagnóstico).')
    print('  - **precision**: de los que marqué, cuántos lo eran.')
    print('    Es la métrica cuando un falso positivo cuesta caro (alarma que molesta).')
    print('  - **F1**: el compromiso, sólo cuando ambos errores cuestan parecido.')
    print('  - **accuracy**: casi nunca, con clases desbalanceadas.')
    print()
    print('  Y el costo de cada error no es un número objetivo: se elige. Un sistema')
    print('  de spam prefiere un falso negativo (un spam en la bandeja) a un falso')
    print('  positivo (un email del jefe en la carpeta de spam). Un detector de')
    print('  fraude prefiere lo contrario. La métrica ES la decisión de producto.')

    print()
    ok = m0['accuracy'] > 0.98 and m0['recall'] == 0 and m1['recall'] > 0.8
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
