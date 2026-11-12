#!/usr/bin/env python3
"""Ejercicio 8.1 del Modulo 1 - la tabla de crecimiento, a mano.

Uso:
    python3 ejercicio-8.1.py            # imprime la tabla para revisar a mano
    python3 ejercicio-8.1.py --check    # corrige un archivo de respuestas

Formato del archivo de respuestas (respuestas-8.1.txt):
    n=1000
    O(1)        =
    O(log n)    =
    O(n)        =
    O(n log n)  =
    O(n^2)      =
    ratio       =
"""
import math
import re
import sys

EXPECTED_N = 1000

# Las respuestas se aceptan si caen dentro del 5% del valor exacto. La pregunta
# es de orden de magnitud, no de calculo exacto: 10.000 y 9.966 son la misma
# respuesta. 1.000 no lo es.
TOLERANCIA = 0.05


def tabla(n=EXPECTED_N):
    return {
        "O(1)": 1,
        "O(log n)": math.log2(n),
        "O(n)": n,
        "O(n log n)": n * math.log2(n),
        "O(n^2)": n ** 2,
    }


def parsear_numero(s):
    s = s.strip().lower().replace(" ", "")
    if not s:
        return None
    mult = 1
    if s.endswith("millones"):
        mult, s = 10 ** 6, s[: -len("millones")]
    elif s.endswith("millon"):
        mult, s = 10 ** 6, s[: -len("millon")]
    elif s.endswith("mil"):
        mult, s = 1000, s[: -len("mil")]
    s = s.replace(",", "").replace("_", "")
    try:
        return float(s) * mult
    except ValueError:
        return None


def mostrar_tabla():
    t = tabla()
    print(f"Tabla de crecimiento para n = {EXPECTED_N}\n")
    print(f"{'Complejidad':<12} {'Operaciones':>18}")
    print("-" * 32)
    for k, v in t.items():
        print(f"{k:<12} {v:>18,.0f}")
    ratio = t["O(n^2)"] / t["O(n log n)"]
    print("\n¿Cuántas veces más lento es O(n^2) que O(n log n)?")
    print(f"  {t['O(n^2)']:,.0f} / {t['O(n log n)']:,.0f} = {ratio:.1f} veces")
    print("\nPara comparar, a n = 10.000 el mismo ratio es:")
    n = 10000
    r2 = n ** 2 / (n * math.log2(n))
    print(f"  {n**2:,.0f} / {n*math.log2(n):,.0f} = {r2:.1f} veces")


def corregir(path):
    texto = open(path, encoding="utf-8").read()
    t = tabla()
    ok, bad = 0, 0
    for linea in texto.splitlines():
        if "=" not in linea:
            continue
        izq, der = linea.split("=", 1)
        clave = izq.strip()
        if clave == "n":
            continue
        if clave == "ratio":
            esperado = t["O(n^2)"] / t["O(n log n)"]
        else:
            normalizada = clave.replace("²", "^2").replace(" ", "")
            match = [k for k in t if k.replace(" ", "") == normalizada]
            if not match:
                print(f"  ?  {clave!r} no es una fila de la tabla")
                continue
            esperado = t[match[0]]
        dado = parsear_numero(der)
        if dado is None:
            print(f"  ?  {clave}: no pude leer {der.strip()!r}")
            bad += 1
            continue
        error = abs(dado - esperado) / esperado
        if error <= TOLERANCIA:
            print(f"  OK {clave}: {dado:,.0f} (exacto {esperado:,.0f})")
            ok += 1
        else:
            print(f"  X  {clave}: {dado:,.0f} (exacto {esperado:,.0f})")
            bad += 1
    print(f"\n{ok} bien, {bad} con problemas")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        if len(sys.argv) < 3:
            sys.exit("uso: ejercicio-8.1.py --check <archivo-respuestas>")
        sys.exit(corregir(sys.argv[2]))
    mostrar_tabla()
