#!/usr/bin/env python3
"""Practica U0.2 - ASCII a mano, verificado por maquina.

Decodificar bytes sin mirar la tabla, y descubrir POR QUE mayuscula y
minuscula difieren en 32: porque son un solo bit.
Uso: python3 e2-ascii.py
"""
import sys

# Lo que pensamos a mano leyendo la tabla de la clase.
HAND = {
    (72, 73, 33): "HI!",
    (104, 105, 33): "hi!",
}

# Bytes crudos, tal como salen de un archivo o de la red.
BYTES = {
    "HI!": b"\x48\x49\x21",   # 72 73 33
    "hi!": b"\x68\x69\x21",   # 104 105 33
}


def main() -> int:
    bad = 0
    print("== decodificacion a mano ==")
    for raw, hand in HAND.items():
        real = bytes(raw).decode("ascii")
        ok = real == hand
        bad += not ok
        print(f"{' '.join(map(str, raw)):>12} -> {real!r:<6} (mano: {hand!r}) {'OK' if ok else 'MAL'}")

    print("\n== el descubrimiento: un solo bit ==")
    for label, raw in BYTES.items():
        text = raw.decode("ascii")
        bits = " ".join(format(c, "08b") for c in raw)
        print(f"{label:>4}: {text!r:<6} bytes={list(raw)} bits={bits}")

    dist = ord("a") - ord("A")
    xor = ord("a") ^ ord("A")
    print(f"\nord('a') - ord('A') = {dist}")
    print(f"ord('a') ^ ord('A') = {xor} = {xor:b} b  -> un bit encendido")
    print(f"Ese bit es 2^{xor.bit_length() - 1} = {xor}")

    # La consecuencia PRACTICA: cambiar caja es una operacion de un bit.
    # Por eso tolower()/toupper() son baratos, y por eso ASCII los pone ahi.
    check = chr(ord("A") | xor)
    print(f"\nchr(ord('A') | 32) = {check!r}  <- caja tocando un bit")
    if check != "a":
        print("MAL: la propiedad de un bit no se sostiene")
        bad += 1

    print("\n== se ve mejor asi ==")
    print(f"A  {ord('A'):08b}")
    print(f"a  {ord('a'):08b}")
    print(f"^  {xor:08b}  <- un unico bit distinto")

    if bad:
        print(f"\n{bad} error(es).")
        return 1
    print("\nTodo correcto: mayuscula y minuscula son el mismo caracter con un bit distinto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
