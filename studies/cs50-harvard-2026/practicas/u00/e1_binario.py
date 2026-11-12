#!/usr/bin/env python3
"""Practica U0.1 - binario a mano, verificado por maquina.

Escribe la respuesta como si la hicieras en papel y despues comprobalo.
La idea del ejercicio (Malan, U0): no se cuentan dedos, se cuentan patrones.
Uso: python3 e1-binario.py
"""
import sys

# Respuestas pensadas a mano: decimal -> string de 8 bits.
HAND = {
    1:   "00000001",  # 2^0
    7:   "00000111",  # 4+2+1
    65:  "01000001",  # 64+1 = 'A'
    128: "10000000",  # 2^7, solo el bit alto
    255: "11111111",  # 8 bits todos encendidos
}


def to_binary(n: int, width: int = 8) -> str:
    """La verdad, no la memoria: format() con relleno a cero."""
    return format(n, f"0{width}b")


def main() -> int:
    bad = 0
    print(f"{'dec':>4}  {'mano':>8}  {'maquina':>8}  ok")
    for n, hand in HAND.items():
        real = to_binary(n)
        ok = hand == real
        bad += not ok
        print(f"{n:>4}  {hand:>8}  {real:>8}  {'OK' if ok else 'MAL'}")

    # Por que 255 y no 256: 8 bits dan 2^8 = 256 combinaciones,
    # pero una es la de todo apagado (0), asi que el maximo es 255.
    combos = 2 ** 8
    print(f"\n2^8 = {combos} combinaciones, desde 0 -> maximo {combos - 1}")
    print(f"256 no entra en 8 bits sin un bit mas: maximo representable = {2**8 - 1}")

    if bad:
        print(f"\n{bad} respuesta(s) mal. No es el formato: revisa el peso de los bits.")
        return 1
    print("\nTodas correctas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
