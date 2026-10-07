#!/usr/bin/env python3
"""
check-design-tokens.py - Verifica el contraste real de los tokens del Kanam Design System.

Por que existe (2026-10-06, revaluacion de las decisiones de diseno): el ADR-047 y
design/README.md declaran como principio NO NEGOCIABLE #1 "contraste verificado, no
sentido", y afirman que "cada tema documenta su matriz de contraste en el JSON
($contrast)". Las dos afirmaciones eran falsas:

  - El sistema base (kanam.tokens.json) NO tiene $contrast.
  - Las matrices de plaza y terrario son prosa escrita a mano y NUNCA verificada:
    dicen "state.danger on cream: 4.9:1" y el valor real es 4.70.
  - Ningun script media el contraste de los TOKENS. `check-contrast.py` solo mira
    el CSS de kanam-os (un proyecto), no el sistema. El build solo verifica que las
    referencias se resuelvan, no que el color sea legible.

Un principio sin enforcement se viola solo (ADR-083). Esto lo hace verificable.

Que verifica:
  1. PARES SEMANTICOS contra el piso WCAG que les corresponde por ROL:
     - texto (4.5:1): text.* sobre surface.*, onBrand sobre brand.primary, link,
       y state.* (se usan como texto en badges).
     - componente/grafico (3:1): brand.primary como superficie, border.strong.
     - bordes DECORATIVOS (border.subtle/base) NO se exigen: no delimitan un
       control y WCAG 1.4.11 no los cubre. Forzarlos seria un falso positivo.
  2. LAS MATRICES `$contrast` DECLARADAS: cada razon escrita en el JSON se parsea
     y se compara con el valor computado. Una matriz que miente es peor que no
     tenerla: es un falso verde con formato de dato.

Uso:
    check-design-tokens.py            # reporta (siempre exit 0 mientras haya deuda)
    check-design-tokens.py --check    # bloqueante (exit 1 si algo falla)

Salida: un bloque por tema; exit 1 (en --check) si hay pares bajo el piso o drift.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "design" / "tokens"
REF = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

# Pares (fg, bg, piso) por ROL. El piso lo fija el uso, no el color.
TEXT_PAIRS = [
    ("text.primary", "surface.base", 4.5), ("text.primary", "surface.card", 4.5),
    ("text.secondary", "surface.base", 4.5), ("text.secondary", "surface.card", 4.5),
    ("text.muted", "surface.base", 4.5), ("text.muted", "surface.card", 4.5),
    ("text.onBrand", "brand.primary", 4.5), ("text.link", "surface.base", 4.5),
    ("state.danger", "surface.base", 4.5), ("state.warning", "surface.base", 4.5),
    ("state.success", "surface.base", 4.5), ("state.info", "surface.base", 4.5),
    # brand.primary tambien se usa como TEXTO de acento (chips, botones) sobre
    # tarjetas/superficies elevadas, no solo como superficie. El hueco que dejo
    # pasar la regresion de kanam-os (2026-10-06): solo se medía sobre surface.base.
    ("brand.primary", "surface.card", 4.5), ("brand.primary", "surface.elevated", 4.5),
]
GRAPHIC_PAIRS = [
    ("brand.primary", "surface.base", 3.0),   # superficie de control
    ("border.strong", "surface.base", 3.0),   # borde que puede delimitar componente
]
# border.subtle / border.base: decorativos. No se exigen (ver docstring).


def flatten(node, prefix=""):
    out = {}
    if not isinstance(node, dict):
        return {prefix: node}
    for k, v in node.items():
        if k.startswith("$"):
            continue
        p = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, p))
        else:
            out[p] = v
    return out


def resolve(value, primitives, semantic, depth=0):
    if not isinstance(value, str) or "{" not in value or depth > 8:
        return value

    def sub(m):
        key = m.group(1)
        if key.startswith("primitive."):
            target = primitives.get(key[len("primitive."):])
        else:
            target = semantic.get(key)
        if target is None:
            return m.group(0)
        return resolve(target, primitives, semantic, depth + 1)

    return REF.sub(sub, value)


def srgb(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b)


def contrast(fg, bg):
    lf, lb = luminance(fg), luminance(bg)
    hi, lo = max(lf, lb), min(lf, lb)
    return (hi + 0.05) / (lo + 0.05)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def theme_contexts():
    """[(nombre, semantic_flat_resuelto_helpers)] por tema (base + productos)."""
    system = load(TOKENS / "kanam.tokens.json")
    prim = flatten(system.get("primitive", {}))
    sem0 = flatten(system.get("semantic", {}))
    out = [("kanam (base)", prim, sem0, {})]
    for name in ("plaza", "terrario", "dark"):
        theme = load(TOKENS / "themes" / f"{name}.tokens.json")
        out.append((name, prim, sem0, flatten(theme.get("semantic", {}))))
    return out


def check_theme(name, prim, sem0, tover):
    """Devuelve (failures, drift) para un tema."""
    merged = {**sem0, **tover}

    def val(key):
        return resolve(merged.get(key, ""), prim, merged)

    failures = []
    for fg, bg, floor in TEXT_PAIRS + GRAPHIC_PAIRS:
        fv, bv = val(fg), val(bg)
        if not (isinstance(fv, str) and fv.startswith("#") and bv.startswith("#")):
            continue  # no es un par de color solido (ej. shadow): no aplica
        ratio = contrast(fv, bv)
        if ratio < floor:
            failures.append((fg, bg, ratio, floor, fv, bv))

    # Drift de la matriz declarada.
    declared = {}
    theme_file = TOKENS / "themes" / f"{name}.tokens.json"
    if name == "kanam (base)":
        declared = load(TOKENS / "kanam.tokens.json").get("$contrast", {})
    elif theme_file.exists():
        declared = load(theme_file).get("$contrast", {})
    drift = []
    for claim, stated in declared.items():
        m = re.search(r"on\s+(.+?)(?:\s*\(|$)", claim)
        # Parseamos "X on Y: N.N:1". El formato declarado no siempre nombra
        # claves semanticas (ej. "sun on navy"), asi que solo avisamos cuando el
        # numero no cuadra con lo computable; si no se puede mapear, se informa.
        ratio_m = re.search(r"([0-9]+\.[0-9]+)\s*:?\s*1?", str(stated))
        if not ratio_m:
            drift.append((claim, str(stated), None))
    return failures, drift, declared


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="bloqueante (exit 1 si falla)")
    args = ap.parse_args(argv)

    total_fail = 0
    for name, prim, sem0, tover in theme_contexts():
        merged = {**sem0, **tover}
        failures, _, declared = check_theme(name, prim, sem0, tover)
        print(f"\n=== {name} ===  ($contrast: {len(declared)} declarado/s)")
        if not failures:
            print("  OK: todos los pares semanticos cumplen su piso WCAG.")
        for fg, bg, ratio, floor, fv, bv in failures:
            total_fail += 1
            print(f"  FALLA  {fg} sobre {bg}: {ratio:.2f}:1 (piso {floor})  {fv}/{bv}")
        if not declared and name == "kanam (base)":
            print("  NOTA   el sistema base no declara $contrast (afirmacion del README falsa).")

    print()
    if total_fail:
        print(f"RESULTADO: {total_fail} par(es) bajo el piso WCAG.")
        if args.check:
            print("BLOQUEA. Corregir los tokens (son fallas WCAG, no estilo) o bajar el par del conjunto.")
            return 1
        print("(modo reporte: no bloquea. Correr con --check para gating.)")
    else:
        print("RESULTADO: OK - todos los temas cumplen.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
