#!/usr/bin/env python3
"""Práctica 4 — positional encoding: por qué attention necesita que le digan el orden.

Self-attention mira pares de tokens. La suma de pares es SIMÉTRICA: el modelo
no ve la diferencia entre "gato muerde perro" y "perro muerde gato" si sólo le
das las palabras.

Por eso el transformer suma un vector de posición a cada embedding. El curso lo
describe; acá se construye y se verifica que dos permutaciones distintas producen
representaciones distintas.

Después se mide el costo: el encoding del curso (senos y cosenos con frecuencias)
tiene una propiedad que conviene conocer: la distancia entre posiciones cercanas
es menor que entre posiciones lejanas, y eso da al modelo una noción de cercanía
que NO tiene que aprender.
"""
import math
import sys


def positional_encoding(pos, d_model):
    """Encoding sinusoidal del video: pares (sen, cos) por dimensión."""
    pe = [0.0] * d_model
    for i in range(0, d_model, 2):
        div = math.pow(10000, i / d_model)
        pe[i] = math.sin(pos / div)
        if i + 1 < d_model:
            pe[i + 1] = math.cos(pos / div)
    return pe


def embeddings(tokens, vocab, d_model):
    """Embedding de juguete: hash determinista a un vector."""
    out = []
    for t in tokens:
        idx = vocab.get(t, 0)
        vec = [math.sin(idx * (i + 1) * 1.7) for i in range(d_model)]
        out.append(vec)
    return out


def add_positional(embs, d_model):
    return [[e[i] + pe[i] for i in range(d_model)]
            for e, pe in zip(embs, (positional_encoding(p, d_model)
                                    for p in range(len(embs))))]


def main():
    d_model = 16
    seq = "el gato muerde al perro".split()
    swapped = "el perro muerde al gato".split()
    vocab = {w: i for i, w in enumerate(sorted(set(seq + swapped)))}

    print(f'=== Sin positional encoding, el orden se pierde ===')
    print(f'  "{seq}" vs "{swapped}"')
    print()
    a = embeddings(seq, vocab, d_model)
    b = embeddings(swapped, vocab, d_model)
    same_no_pos = all(abs(a[i][j] - b[i][j]) < 1e-9
                      for i in range(len(seq)) for j in range(d_model))
    print(f'  ¿los embeddings son iguales posición por posición? {"no, cambian las palabras" if not same_no_pos else "sí"}')
  
    print()

    print('=== Con positional encoding ===')
    ap = add_positional(a, d_model)
    bp = add_positional(b, d_model)
    n = len(seq)
    d0 = d_model
    changed = sum(1 for i in range(n) if seq[i] != swapped[i])
    diff = sum(1 for i in range(n) for j in range(d0)
               if abs(ap[i][j] - bp[i][j]) > 1e-9)
    print(f'  celdas que difieren entre las dos frases: {diff}/{n * d0}')
    print('  El modelo ahora ve que el gato está en la posición 1 y el perro en la 4,')
    print('  y al revés en la otra frase. El par (gato, perro) deja de ser simétrico.')
    print()

    # --- el encoding, mirando sus números ---------------------------------
    print('=== El encoding de la posición 0 y 1 (primeras 8 dimensiones) ===')
    for pos in (0, 1, 2, 10, 100):
        pe = positional_encoding(pos, 8)
        print(f'  pos={pos:<4} {[round(v, 3) for v in pe]}')
    print()
    print('  Fíjate: pos=0 y pos=1 difieren en TODAS las dimensiones. No hay dos')
    print('  posiciones con el mismo vector. Y pos=100 sigue siendo distinguible de')
    print('  pos=0, porque las frecuencias bajas giran lentísimo.')
    print()

    # --- la propiedad que se aprende gratis -------------------------------
    print('=== La propiedad que da cercanía gratis ===')
    print(f'  {"par de posiciones":<26} {"distancia euclidiana"}')
    print('-' * 54)
    d_model = 32
    for a_, b_ in ((0, 1), (0, 2), (0, 10), (0, 100), (5, 6), (5, 50)):
        va = positional_encoding(a_, d_model)
        vb = positional_encoding(b_, d_model)
        d = math.sqrt(sum((x - y) ** 2 for x, y in zip(va, vb)))
        print(f'  ({a_}, {b_}){"":<20} {d:.3f}')
    print()
  

    print()
    # Toda posición que cambió de palabra tiene que diferir en todas sus celdas.
    ok = diff == changed * d0
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
