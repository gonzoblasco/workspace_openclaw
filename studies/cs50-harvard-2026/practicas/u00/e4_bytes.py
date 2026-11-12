#!/usr/bin/env python3
"""Practica U0.4 - el ancla al repo: todo es un array de bytes, MEDIDO.

Malan dice en la U0 que un mensaje es una secuencia de bytes y que las
imagenes son numeros. En vez de creerlo, lo medimos en esta maquina:
  - 'hi!' en ASCII son 3 bytes
  - 'a' con acento NO son 2: depende de la codificacion
  - el hueco del 5.2 de la leccion, demostrado

Uso: python3 e4-bytes.py
"""
import sys


def show(label: str, raw: bytes) -> None:
    hexs = " ".join(f"{b:02x}" for b in raw)
    dec = " ".join(str(b) for b in raw)
    print(f"{label:>14} | {len(raw):>2} bytes | hex: {hexs:<20} | dec: {dec}")


def main() -> int:
    print("== todo es un array de bytes ==\n")

    show("'hi!' ascii", b"hi!")
    show("'HI!' ascii", b"HI!")
    show("'!' ascii", b"!")

    print("\n== el hueco: fuera de ASCII ==")
    show("'a' ascii", "a".encode("ascii"))
    show("'á' utf-8", "á".encode("utf-8"))
    show("'á' latin-1", "á".encode("latin-1"))
    show("'漢' utf-8", "漢".encode("utf-8"))

    n_utf8 = len("á".encode("utf-8"))
    n_chars = len("á")

    print(f"\nlen('á')         = {n_chars}  caracter")
    print(f"len('á'.encode()) = {n_utf8} bytes en utf-8")
    print(f"len('á' latin-1)  = {len('á'.encode('latin-1'))} byte")

    print("\n== por que importa para la Unidad 2 ==")
    texto = "canción"
    print(f"'{texto}' tiene {len(texto)} caracteres y {len(texto.encode('utf-8'))} bytes en utf-8")
    if n_utf8 == 2:
        print("Un programa en C que cuente bytes de este string va a decir "
              f"{len(texto.encode('utf-8'))} y no {len(texto)}.")
        print("Ese es el bug que todavia no tienes, pero ya mediste.")

    print("\n== una imagen tambien == ")
    # Un pixel RGB son 3 bytes. Una imagen de 4x3 = 12 pixeles.
    w, h = 4, 3
    raw_bytes = w * h * 3
    print(f"{w}x{h} RGB = {w*h} pixeles x 3 bytes = {raw_bytes} bytes crudos")
    print(f"Una foto de 1600x900 = {1600*900*3:,} bytes = {1600*900*3/1024/1024:.2f} MiB crudos")
    print("Un JPEG es un acuerdo sobre que se puede tirar sin que se note.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
