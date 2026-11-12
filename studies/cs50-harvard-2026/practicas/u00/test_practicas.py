#!/usr/bin/env python3
"""Tests de las practicas U0. Probar que el algoritmo SIRVE y que FALLA.

Una practica que solo corre en el caso feliz no ensena nada. Estos tests:
  1. prueban que el orden de las cartas es correcto en muchos casos,
  2. prueban que una implementacion ROTA FALLA (sino, el test no prueba),
  3. prueban que un archivo es realmente bytes (e4).

Uso: python3 test_practicas.py
"""
import sys

sys.path.insert(0, ".")

from e3_cartas import ordenar_cartas


def _roto(cartas: list[int]) -> list[int]:
    """Implementacion rota a proposito: solo una pasada, no ordena."""
    c = list(cartas)
    for i in range(len(c) - 1):
        if c[i] > c[i + 1]:
            c[i], c[i + 1] = c[i + 1], c[i]
    return c


def check_nombre(nombre: str, ok: bool, detalle: str = "") -> int:
    print(f"{'OK ' if ok else 'FAIL'} {nombre}{'  ' + detalle if detalle else ''}")
    return 0 if ok else 1


def main() -> int:
    fails = 0

    # 1. El bueno ordena.
    casos = [
        [3, 1, 2],
        [1, 2, 3],
        [3, 2, 1],
        [5, 5, 4, 4, 3],
        [11, 2, 1, 5, 4, 9, 12, 6],
        list(range(13, 5, -1)),
    ]
    for c in casos:
        got = ordenar_cartas(c, verbose=False)
        fails += check_nombre(f"ordena {c[:5]}{'...' if len(c) > 5 else ''}",
                              got == sorted(c))
        fails += check_nombre(f"  no pierde cartas", sorted(got) == sorted(c))

    # 2. El roto TIENE que fallar: si no fallara, el test no valida nada.
    rotos_que_deberian_fallar = [
        [3, 2, 1],           # una pasada no alcanza
        [5, 1, 4, 2, 3],
    ]
    for c in rotos_que_deberian_fallar:
        got = _roto(c)
        fallo = got != sorted(c)
        fails += check_nombre(f"el roto FALLA en {c}", fallo,
                              f"(dio {got})" if fallo else "(dio ordenado: test inutil)")

    # 3. Input y output no comparten lista (no muta la entrada).
    entrada = [3, 1, 2]
    copia = list(entrada)
    ordenar_cartas(entrada, verbose=False)
    fails += check_nombre("no muta la entrada", entrada == copia)

    # 4. Un string es bytes: la propiedad del e4.
    texto = "canción"
    fails += check_nombre("'canción' son 7 caracteres", len(texto) == 7)
    fails += check_nombre("'canción' son 8 bytes utf-8",
                          len(texto.encode("utf-8")) == 8)
    fails += check_nombre("'á' es 2 bytes utf-8", len("á".encode("utf-8")) == 2)
    fails += check_nombre("'á' es 1 byte latin-1", len("á".encode("latin-1")) == 1)

    print(f"\n{fails} fallo(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
