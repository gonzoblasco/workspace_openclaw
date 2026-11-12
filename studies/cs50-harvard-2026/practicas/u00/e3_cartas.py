#!/usr/bin/env python3
"""Practica U0.3 - ordenar 8 cartas en pseudocodigo, y verlo correr.

El ejercicio del outline: escribir los pasos EN CASTELLANO, sin usar
"ordenar" como paso. Este archivo hace tres cosas:
  1. imprime el pseudocodigo que escribimos a mano,
  2. lo ejecuta sobre 8 cartas reales imprimiendo cada intercambio,
  3. verifica que el resultado este ordenado.

La version "de papel" es la seccion PSEUDOCODIGO de abajo: eso es lo que
se escribe sin computadora. El resto es la prueba de que el algoritmo
funciona. En la Unidad 3 esto se va a llamar SELECTION SORT.
Uso: python3 e3-cartas.py [--shuffle-seed N]
"""
import argparse
import random
import sys

PSEUDOCODIGO = """\
para cada posicion i desde 0 hasta 6:
    asumir que la carta en i es la mas chica
    mirar cada carta j desde i+1 hasta 7:
        si la carta j es menor que la "mas chica" recordada:
            recordar esa posicion como la nueva mas chica
    si la posicion recordada no es i:
        intercambiar la carta de i con la de esa posicion

Por que funciona: al terminar la vuelta i, las posiciones 0..i estan
definitivamente ordenadas, porque cada vuelta trae la menor que queda.
"""


def ordenar_cartas(cartas: list[int], verbose: bool = True) -> list[int]:
    cartas = list(cartas)  # no mutar la entrada
    n = len(cartas)
    swaps = 0
    for i in range(n - 1):
        mas_chica = i
        for j in range(i + 1, n):
            if cartas[j] < cartas[mas_chica]:
                mas_chica = j
        if mas_chica != i:
            cartas[i], cartas[mas_chica] = cartas[mas_chica], cartas[i]
            swaps += 1
            if verbose:
                print(f"  vuelta {i}: cambio pos {i}<->{mas_chica} -> {cartas}")
        elif verbose:
            print(f"  vuelta {i}: pos {i} ya estaba bien -> {cartas}")
    if verbose:
        print(f"  total de intercambios: {swaps}")
    return cartas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shuffle-seed", type=int, default=None)
    args = ap.parse_args()

    if args.shuffle_seed is not None:
        random.seed(args.shuffle_seed)

    print("== PSEUDOCODIGO (lo que se escribe a mano) ==")
    print(PSEUDOCODIGO)

    cartas = random.sample(range(1, 14), 8)  # 8 cartas distintas de un mazo
    print(f"== cartas iniciales ==\n  {cartas}\n")

    ordenadas = ordenar_cartas(cartas)

    print(f"\n== resultado ==\n  {ordenadas}")
    if ordenadas != sorted(cartas):
        print("MAL: no quedo ordenado")
        return 1
    print("OK: ordenado de menor a mayor, y son las mismas 8 cartas.")

    # El costo, que en la U3 va a ser O(n^2):
    n = len(cartas)
    comparaciones = n * (n - 1) // 2
    print(f"\ncomparaciones: {comparaciones} = n(n-1)/2 con n={n}  -> O(n^2)")
    print("Para 8 cartas da igual. Para 10.000, son ~50.000.000.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
