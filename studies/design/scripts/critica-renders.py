#!/usr/bin/env python3
"""critica-renders.py - Prepara los renders que piden los gates de diseño, sin abrir Photoshop.

Por que existe (2026-11-06): `studies/design/README.md` §4.1 pide criticar con los 6 Output Gates
(grayscale, squint, alignment, spacing, contrast, rank-1). Hacer a mano el gris y el desenfoque es
donde se abandona el metodo en la tercera ficha. Esto lo vuelve un comando.

Que hace:
  1. Descarga la imagen (si es una URL) en `<outdir>/<prefijo>_view.png`.
  2. Genera `<prefijo>_gray.png` (L) y `<prefijo>_squint.png` (resize 1/12 y vuelta).
  3. Mide contraste WCAG contra blanco en la banda central de texto: promedio y **peor pixel**.
     El peor pixel es el que decide en fondos no uniformes (gradientes, glow, fotos).

Uso:
  critica-renders.py --out casos --prefix lin https://ejemplo.com/og.png
  critica-renders.py --out casos --prefix str /ruta/local.jpg --box 0.34,0.40,0.66,0.60

Salida: JSON con rutas y medicion. Solo lectura de red (descarga) y escritura en --out.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    print(json.dumps({"error": "falta Pillow (python3 -m pip install pillow)"}), file=sys.stderr)
    sys.exit(2)


def srgb(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb) -> float:
    r, g, b = (srgb(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_vs_white(rgb) -> float:
    return 1.05 / (luminance(rgb) + 0.05)


def render(src: str, outdir: str, prefix: str) -> dict:
    os.makedirs(outdir, exist_ok=True)
    view = os.path.join(outdir, f"{prefix}_view.png")
    if src.startswith(("http://", "https://")):
        req = urllib.request.Request(src, headers={"User-Agent": "kanam-mind-study/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(view, "wb") as fh:
                fh.write(resp.read())
    else:
        Image.open(src).convert("RGB").save(view)

    im = Image.open(view).convert("RGB")
    w, h = im.size
    gray = os.path.join(outdir, f"{prefix}_gray.png")
    squint = os.path.join(outdir, f"{prefix}_squint.png")
    im.convert("L").save(gray)
    im.resize((max(1, w // 12), max(1, h // 12)), Image.BILINEAR).resize((w, h), Image.BILINEAR).save(squint)
    return {"view": view, "gray": gray, "squint": squint, "size": [w, h]}


def measure(path: str, box: tuple[float, float, float, float]) -> dict:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = int(w * box[0]), int(h * box[1]), int(w * box[2]), int(h * box[3])
    samples = [im.getpixel((x, y)) for x in range(x0, x1, 3) for y in range(y0, y1, 3)]
    bg = [p for p in samples if sum(p) < 720]  # ignora pixeles casi blancos (el glifo)
    if not bg:
        bg = samples
    worst = min(bg, key=contrast_vs_white)
    avg = tuple(int(sum(p[i] for p in bg) / len(bg)) for i in range(3))
    return {
        "samples": len(bg),
        "avg_rgb": avg, "avg_ratio": round(contrast_vs_white(avg), 2),
        "worst_rgb": worst, "worst_ratio": round(contrast_vs_white(worst), 2),
        "passes_large_text_3to1_on_worst": contrast_vs_white(worst) >= 3.0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="URL o archivo")
    ap.add_argument("--out", default="casos")
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--box", default="0.34,0.40,0.66,0.60",
                    help="caja de la banda de texto en fracciones: x0,y0,x1,y1")
    args = ap.parse_args()

    box = tuple(float(v) for v in args.box.split(","))
    r = render(args.source, args.out, args.prefix)
    m = measure(r["view"], box)
    print(json.dumps({**r, "contrast": m, "box": box}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
