#!/usr/bin/env python3
"""Gate de contraste para CSS con variables.

Idea del curso (M9/M6 del outline, 00:01:00-00:06:57): cuando el texto va
encima de un fondo animado o de un asset visual, el error de contraste no se
ve hasta que el fondo cambia. El ponente lo arregla con una sombra; una sombra
es un parche, no una medida.

Este gate lee un CSS, resuelve las variables `--x: #hex` y verifica cada par
(texto, fondo) contra WCAG AA. Falla con exit 1 cuando un par baja de 4.5:1.

Uso:
    python3 contrast-gate.py <archivo.css> [archivo2.css ...]
    python3 contrast-gate.py --pairs "texto:fondo" <archivo.css>
    python3 contrast-gate.py --pairs "texto:fondo,borde:fondo" <archivo.css>

Sin --pairs, verifica todos los pares de --text-* contra --bg-*. Un par que
no se puede resolver (falta la variable o no es un hex) es un FALLA: un gate
que se saltea lo que no entiende no es un gate.

Ojo con el falso positivo: `--text-on-accent` se declara para ir encima de
`--accent`, no de `--bg-*`. Contra un fondo oscuro da 1:1 y el gate lo marca
como falla. Esa pareja se pasa explícita con --pairs; el modo automático mide
contraste, no intención de uso.
"""
import re
import sys

HEX = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")


def load_vars(path):
    css = open(path, encoding="utf-8").read()
    vars_ = {}
    for name, value in re.findall(r"(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);", css):
        m = HEX.search(value)
        if m:
            vars_[name] = m.group(1)
    return vars_


def to_rgb(h):
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def luminance(h):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (ch(c) for c in to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    pairs = None
    if argv[0] == "--pairs":
        pairs = [p.split(":") for p in argv[1].split(",")]
        argv = argv[2:]
    failed = 0
    checked = 0
    for path in argv:
        vars_ = load_vars(path)
        if not vars_:
            print(f"FAIL {path}: no se encontró ninguna variable con color hex")
            failed += 1
            continue
        if pairs:
            todo = pairs
        else:
            todo = [
                [t, b] for t in vars_ if t.startswith("--text-") for b in vars_ if b.startswith("--bg-")
            ]
        for t, b in todo:
            if t not in vars_ or b not in vars_:
                print(f"FAIL {path}: falta {t if t not in vars_ else b}")
                failed += 1
                continue
            r = ratio(vars_[t], vars_[b])
            checked += 1
            status = "ok  " if r >= 4.5 else "FAIL"
            if r < 4.5:
                failed += 1
            print(f"{status} {r:4.2f}:1  {t:20s} {vars_[t]}  sobre  {b:14s} {vars_[b]}  ({path})")
    print(f"\n{checked} pares verificados, {failed} fallas")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
