#!/usr/bin/env python3
"""Práctica 1 — tokenización y n-gramas: el modelo de lenguaje más simple.

El curso arranca NLP por lo más chico: partir el texto en tokens y mirar qué
secuencias aparecen.

  unigram  = una palabra
  bigram   = dos palabras seguidas
  trigram  = tres

Con eso solo, un modelo de Markov puede **generar** texto: elige la palabra
siguiente según la que acaba de escribir.

Esta práctica:
  1. tokeniza un corpus,
  2. cuenta unigramas, bigramas y trigramas,
  3. genera texto con una cadena de Markov y muestra por qué se estanca.
"""
import random
import re
import sys


CORPUS = """
the cat sat on the mat the cat ate the fish and the cat slept on the mat
the dog sat on the mat and the dog ate the bone and the dog slept
the cat and the dog sat on the mat and then the cat ate the fish
a cat sat on a mat and a dog sat on a mat and then they slept
the mat was on the floor and the floor was in the house and the house had a door
"""


def tokenize(text):
    return re.findall(r"[a-z']+", text.lower())


def ngrams(tokens, n):
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def counts(items):
    out = {}
    for it in items:
        out[it] = out.get(it, 0) + 1
    return out


def build_markov(tokens, n):
    """Modelo de Markov de orden n: P(próximo | últimos n-1 tokens)."""
    model = {}
    for gram in ngrams(tokens, n):
        prefix, nxt = gram[:-1], gram[-1]
        model.setdefault(prefix, []).append(nxt)
    return model


def generate(model, seed_text, length=15, rng=None):
    rng = rng or random.Random(0)
    order = len(next(iter(model)))
    tokens = tokenize(seed_text)
    out = tokens[:]
    while len(out) < length:
        prefix = tuple(out[-order:])
        choices = model.get(prefix)
        if not choices:
            # back-off: usar el último token solo, si hay bigramas
            if order > 1:
                prefix2 = (out[-1],)
                choices = model.get(prefix2)
            if not choices:
                break
        out.append(rng.choice(choices))
    return ' '.join(out)


def main():
    tokens = tokenize(CORPUS)
    print(f'=== 1. Tokenización ===')
    print(f'  palabras: {len(tokens)}')
    print(f'  vocabulario: {len(set(tokens))} tokens distintos')
    print(f'  vocabulario: {sorted(set(tokens))}')
    print()

    print('=== 2. Los n-gramas más frecuentes ===')
    for n in (1, 2, 3):
        c = counts(ngrams(tokens, n))
        top = sorted(c.items(), key=lambda kv: -kv[1])[:5]
        print(f'  {n}-gramas: {len(c)} distintos')
        for gram, k in top:
            print(f'    {k:>3}x  {" ".join(gram)}')
        print()

    print('=== 3. Generar texto con Markov (bigramas) ===')
    model2 = build_markov(tokens, 2)
    for seed, s in enumerate(['the cat', 'a dog', 'the mat'], start=1):
        print(f'  semilla "{s}":')
        print(f'    {generate(model2, s, length=16, rng=random.Random(seed))}')
    print()
    print('  El texto es gramatical localmente y sin sentido global: cada palabra es')
    print('  plausible dada la anterior, y la frase no va a ningún lado.')
    print()

    print('=== 4. Trigramas: menos opciones, más coherencia local ===')
    model3 = build_markov(tokens, 3)
    for seed, s in enumerate(['the cat sat', 'the dog sat', 'a cat sat'], start=1):
        print(f'  semilla "{s}":')
        print(f'    {generate(model3, s, length=16, rng=random.Random(seed))}')
    print()
    print('  Con orden 3, cada prefijo tiene menos continuaciones: el texto es más')
    print('  predecible y se repite más. Es el intercambio entre variedad y coherencia,')
    print('  y sigue sin entender nada.')

    print()
    print('=== 5. El problema del vocabulario cero ===')
    unseen = 'the cat danced on a purple mat'
    hit = sum(1 for g in ngrams(tokenize(unseen), 3) if g in counts(ngrams(tokens, 3)))
    total = len(ngrams(tokenize(unseen), 3))
    print(f'  frase inédita: "{unseen}"')
    print(f'  trigramas que el modelo ya vio: {hit}/{total}')
    print(f'  Con {hit}/{total}, la probabilidad del modelo es CERO. No es "poco probable": es')
    print('  imposible. De ahí la suavización (additive smoothing) del curso.')
    print('  Y con corpus más grande el problema no desaparece: el vocabulario crece')
    print('  más rápido que el corpus.')

    print()
    ok = hit < total
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
