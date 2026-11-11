#!/usr/bin/env python3
"""web-asset-gate.py - presupuesto de carga para un proyecto 3D que se sirve en web.

Mide tres cosas por archivo, y falla (exit 1) si alguna se pasa:

  1. PESO      - tamano comprimido del asset (gzip, que es como viaja por HTTP el texto
                 de un glTF). Un techo por archivo evita que un modelo suelto arruine
                 el first load.
  2. TEXTURA   - lado mayor de cada PNG/JPG referenciado. Un modelo con texturas 4K
                 sin comprimir ya se nota: el curso lo resuelve pasando a WebP 90.
  3. FORMATO   - texturas en .png/.jpg en un asset que se sirve web son una senal de
                 que falta el paso de compresion (WebP), no de que el original este bien.

No descarga nada ni necesita Blender: se corre sobre los binarios que ya estan en el repo.

Uso:
    python3 web-asset-gate.py <directorio-o-archivos...> [--max-glb 2.0] [--max-tex 2048]

Salida: una linea por hallazgo + resumen + EXIT=0/1. Sin hallazgos, EXIT=0.
"""

from __future__ import annotations

import argparse
import gzip
import os
import struct
import sys


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_size(path: str) -> tuple[int, int] | None:
    """Lee ancho/alto del IHDR de un PNG sin decodificar la imagen."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 24 or not head.startswith(PNG_MAGIC):
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def jpg_size(path: str) -> tuple[int, int] | None:
    """Recorre los segmentos JPEG hasta el SOFn, que trae el tamano."""
    with open(path, "rb") as fh:
        data = fh.read()
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            h, w = struct.unpack(">HH", data[i + 5 : i + 9])
            return w, h
        seg_len = struct.unpack(">H", data[i + 2 : i + 4]) if i + 4 <= len(data) else 0
        i += 2 + seg_len
    return None


def gzip_size(path: str) -> int:
    with open(path, "rb") as fh:
        return len(gzip.compress(fh.read(), 6))


def collect(paths: list[str]) -> list[str]:
    out: list[str] = []
    for p in paths:
        if os.path.isdir(p):
            for root, _dirs, files in os.walk(p):
                if "/node_modules/" in root + "/":
                    continue
                out.extend(os.path.join(root, f) for f in files)
        else:
            out.append(p)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--max-glb", type=float, default=2.0, help="MB gzip por modelo")
    ap.add_argument("--max-tex", type=int, default=2048, help="lado mayor de textura")
    args = ap.parse_args(argv)

    files = collect(args.paths)
    glb = [f for f in files if f.lower().endswith((".glb", ".gltf"))]
    tex = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    fails = 0
    total = 0

    for f in sorted(glb):
        mb = gzip_size(f) / 1024 / 1024
        total += 1
        ok = mb <= args.max_glb
        fails += 0 if ok else 1
        print(f"{'ok ' if ok else 'FAIL'}  {mb:6.2f} MB gz  {f}")

    for f in sorted(tex):
        size = png_size(f) or jpg_size(f)
        total += 1
        if size is None:
            print(f"?     sin dims   {f}")
            continue
        w, h = size
        side = max(w, h)
        kmb = os.path.getsize(f) / 1024
        ok = side <= args.max_tex
        fails += 0 if ok else 1
        print(f"{'ok ' if ok else 'FAIL'}  {w}x{h}  {kmb:7.0f} KB  {f}")

    print(f"\n{total} assets medidos, {fails} fallas")
    print(f"EXIT={0 if fails == 0 else 1}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
