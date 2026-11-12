#!/usr/bin/env python3
"""Práctica 3 — RNN vs self-attention: qué cambia en el costo, no en el resultado.

El curso compara dos formas de procesar una secuencia:

  RNN:          procesa token por token, guardando un estado oculto.
                Tiene MEMORIA del pasado, y por eso NO se puede paralelizar:
                el token n necesita el estado del n-1.

  self-attention: cada token mira a TODOS los demás del input a la vez.
                No tiene orden inherente (por eso el positional encoding) pero
                se puede paralelizar.

La práctica hace lo que el curso sólo describe: mide cuántas operaciones hace
cada uno como función de la longitud de la secuencia.

El resultado no es "uno es mejor", es que tienen forma de costo DISTINTA:

  RNN:           O(n · d²)     lineal en la longitud, pero secuencial
  self-attention: O(n² · d)    cuadrática en la longitud, pero paralelo

Para n=10 gana el RNN. Para n=1.000.000, ninguno. Para n=100.000, attention
es imposible sin trucos.
"""
import sys


def rnn_ops(n, d):
    """Operaciones de una RNN simple: n pasos, cada uno con d×d de pesos."""
    return n * d * d


def attention_ops(n, d):
    """Operaciones de self-attention: Q·Kᵀ es n×n, luego por V."""
    return n * n * d + n * n * d


def main():
    d = 64
    print(f'=== Operaciones por capa, dimensión oculta d={d} ===\n')
    print(f'  {"n (tokens)":<14} {"RNN (n·d²)":<18} {"attention (n²·d)":<22} {"gana"}')
    print('-' * 70)
    rows = []
    for n in (10, 100, 1000, 10_000, 100_000):
        r = rnn_ops(n, d)
        a = attention_ops(n, d)
        rows.append((n, r, a))
        winner = 'RNN' if r < a else 'attention'
        print(f'  {n:<14} {r:<18,} {a:<22,} {winner}')
    print()

    # punto de cruce
    crossing = None
    for n in range(1, 100000):
        if attention_ops(n, d) > rnn_ops(n, d):
            crossing = n
            break
    print(f'  Punto de cruce: n={crossing}. Con menos tokens, el RNN hace menos')
    print(f'  trabajo; con más, attention hace más.')
    print()

    print('=== Pero el costo no es la única medida ===')
    print('  La RNN es SECUENCIAL: el paso n depende del n-1. No hay forma de')
    print('  computar dos pasos a la vez. En una GPU con miles de núcleos, eso es')
    print('  desperdiciar el hardware.')
    print()
    print('  Attention computa todos los pares (i,j) a la vez: es una multiplicación')
    print('  de matrices, que es exactamente lo que una GPU hace bien.')
    print()
    print('  Por eso el transformer ganó aunque, para secuencias cortas, haga MÁS')
    print('  operaciones: el paralelismo lo compensa con creces. El cruce a d=64')
    print('  está en n=33 tokens, y todo texto real es más largo.')
    print()

    print('=== El problema real de attention, que el curso no menciona ===')
    print('  n²·64 operaciones. Con n=100.000:')
    print(f'    {attention_ops(100_000, d):,} operaciones SOLO en una capa.')
    print('  Con 32 capas, eso es intratable. De ahí que TODO modelo de contexto')
    print('  largo (2026) use alguna variante que rompe el n²: sparse attention,')
    print('  sliding window, o aproximaciones. El transformer del video es el')
    print('  punto de partida, no el que corre en producción hoy.')

    print()
    print('=== Y lo que el RNN hacía mejor ===')
    print('  El RNN tiene un estado que acumula TODA la historia. Attention tiene')
    print('  un límite fijo: no puede mirar más allá de su ventana (el contexto).')
    print('  Por eso "olvidar" una instrucción de la mitad de la conversación es un')
    print('  problema de atención, no de memoria: el modelo no la está mirando.')

    print()
    # La propiedad: el cruce existe y para n grande attention hace más operaciones.
    ok = rows[-1][2] > rows[-1][1] and crossing > 0
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
