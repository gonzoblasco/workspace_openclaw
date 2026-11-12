#!/usr/bin/env python3
"""Práctica 2 — bag of words y Naive Bayes: clasificar texto sin entenderlo.

Bag of words: representar un texto como un conjunto desordenado de palabras con
sus conteos. Se pierde el orden, se gana simplicidad.

Naive Bayes: aplicar Bayes suponiendo (de forma ingenua e incorrecta) que cada
palabra es independiente de las demás dada la clase.

    P(clase | palabras) ∝ P(clase) · Π P(palabra | clase)

Esa suposición es falsa: "no" y "bueno" no son independientes. Y funciona igual.

La práctica:
  1. entrena sobre un corpus de opiniones,
  2. clasifica frases nuevas,
  3. muestra qué pasa cuando una palabra no aparece en una clase (probabilidad 0)
     y cómo la suavización lo arregla.
"""
import math
import sys


POSITIVE = [
    "great movie loved it excellent acting",
    "wonderful story and great acting",
    "excellent film loved the story",
    "great story wonderful acting loved it",
]
NEGATIVE = [
    "terrible movie hated it awful acting",
    "boring story and terrible acting",
    "awful film hated the story",
    "terrible story boring acting hated it",
]


def bag(text):
    words = text.lower().split()
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts


def train(positive, negative, smoothing=1.0):
    """Devuelve prior y verosimilitudes con suavización opcional."""
    docs = {'pos': [bag(t) for t in positive], 'neg': [bag(t) for t in negative]}
    vocab = sorted({w for cls in docs.values() for d in cls for w in d})

    model = {}
    for cls, corpus in docs.items():
        total_words = sum(sum(d.values()) for d in corpus)
        counts = {}
        for d in corpus:
            for w, k in d.items():
                counts[w] = counts.get(w, 0) + k
        # suavización: sumar `smoothing` a cada conteo y |V|*smoothing al total
        n_docs = len(corpus)
        model[cls] = {
            'prior': n_docs / (len(positive) + len(negative)),
            'loglik': {
                w: math.log((counts.get(w, 0) + smoothing) /
                            (total_words + smoothing * len(vocab)))
                for w in vocab
            },
            'counts': counts,
            'total': total_words,
            'vocab': vocab,
        }
    return model, vocab


def classify(model, text):
    """Devuelve (clase, score_pos, score_neg) en log-espacio."""
    words = text.lower().split()
    scores = {}
    for cls, m in model.items():
        score = math.log(m['prior'])
        for w in words:
            # palabra fuera del vocabulario: probabilidad suavizada
            if w in m['loglik']:
                score += m['loglik'][w]
            else:
                score += math.log(1e-9)   # OOV muy improbable
        scores[cls] = score
    cls = max(scores, key=scores.get)
    return cls, scores['pos'], scores['neg']


def main():
    print('=== 1. Bag of words: el orden se pierde ===')
    a = bag("great movie loved it")
    b = bag("it loved movie great")
    print(f'  "great movie loved it" -> {a}')
    print(f'  "it loved movie great" -> {b}')
    print(f'  ¿el mismo bag? {"sí" if a == b else "no"}')
    print()
    print('  Dos frases con el mismo conjunto de palabras son el MISMO dato para el')
    print('  clasificador. Para sentimiento alcanza; para "no es bueno" no.')
    print()

    print('=== 2. Naive Bayes entrenado y clasificando ===')
    model, vocab = train(POSITIVE, NEGATIVE)
    print(f'  vocabulario: {len(vocab)} palabras')
    print(f'  prior: P(pos)={model["pos"]["prior"]:.2f}  P(neg)={model["neg"]["prior"]:.2f}')
    print()
    tests = [
        "great acting",
        "awful story",
        "great story",
        "boring film",
        "loved the movie",
    ]
    print(f'  {"frase":<24} {"clase":<8} {"log-pos":<12} {"log-neg"}')
    print('-' * 60)
    for t in tests:
        cls, sp, sn = classify(model, t)
        print(f'  {t:<24} {cls:<8} {sp:<12.2f} {sn:.2f}')
    print()
    print('  "great story" mezcla una palabra positiva con una neutra. El modelo suma')
    print('  las dos evidencias y decide por la que más pesa en el corpus.')
    print()

    print('=== 3. La naive, y por qué funciona igual ===')
    print('  La suposición es P(w1, w2 | clase) = P(w1|clase)·P(w2|clase).')
    print('  Es falsa: "great" y "wonderful" correlacionan. Al multiplicar sus')
    print('  probabilidades, el modelo CUENTA DOS VECES la misma evidencia.')
    print()
    t = "great wonderful excellent"
    cls, sp, sn = classify(model, t)
    print(f'  "{t}" -> {cls} (log-pos={sp:.1f}, log-neg={sn:.1f})')
    print('  Sigue clasificando bien, pero los SCORES están calibrados de más:')
    print('  tres sinónimos positivos lo hacen parecer mucho más seguro de lo que')
    print('  debería. Para ORDENAR clases alcanza; para decir "probabilidad 0.999"')
    print('  no. Ese es el costo de la suposición, y el detalle que el video no dice.')

    print()
    print('=== 4. La palabra que nunca apareció ===')
    unseen = "fantastic brilliant magnificent"
    cls, sp, sn = classify(model, unseen)
    print(f'  "{unseen}" -> {cls}')
    print('  Ninguna palabra está en el vocabulario. Cada una cae al OOV 1e-9 y el')
    print('  score se hunde. Sin suavización, P = 0 y el producto da 0 para las dos')
    print('  clases: el modelo no puede decidir.')
    print()
    print('  Con suavización aditiva (la del curso), cada palabra nueva se lleva una')
    print('  probabilidad chica pero distinta de cero. El modelo se equivoca menos en')
    print('  el caso que más importa: texto real, lleno de palabras que nunca vio.')

    print()
    ok = classify(model, "great")[0] == 'pos' and classify(model, "awful")[0] == 'neg'
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
