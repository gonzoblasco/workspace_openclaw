#!/usr/bin/env python3
"""glb-budget.py — presupuesto de assets 3D antes de meterlos en el repo.

Sale del Módulo 7 del curso "Creative Web Development with Three.js and Blender"
(02:18:52): preparar el modelo, borrar caras que nunca se ven, exportar solo lo
seleccionado. El criterio del curso no es estético, es de peso: «the browser is
very, very weak compared to like Blender software or game engines» (00:23:14).

Este script no modela ni exporta: mide un `.gltf`/`.glb` y falla si pasa los
presupuestos, para que el asset no entre al repo por default.

Uso:
    python3 glb-budget.py <archivo.gltf|.glb> [--tris N] [--mb N] [--anims N]

Defaults: --tris 20000 --mb 5 --anims 20

Salidas:
    exit 0  → dentro de presupuesto
    exit 1  → excede presupuesto
    exit 2  → no se pudo leer el archivo
"""
import argparse
import base64
import json
import os
import struct
import sys


def load_gltf(path):
    """Devuelve (json_gltf, tamano_total_bytes). Soporta .gltf y .glb."""
    size = os.path.getsize(path)
    if path.lower().endswith(".glb"):
        with open(path, "rb") as f:
            magic, version, length = struct.unpack("<4sII", f.read(12))
            if magic != b"glTF":
                raise ValueError("no es un GLB: cabecera inválida")
            chunk_len, chunk_type = struct.unpack("<I4s", f.read(8))
            if chunk_type != b"JSON":
                raise ValueError("el primer chunk no es JSON")
            doc = json.loads(f.read(chunk_len).decode("utf-8"))
        return doc, size
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), size


def embedded_bytes(doc):
    """Bytes de buffers e imágenes embebidos (base64 inline o bufferViews)."""
    total = 0
    for buf in doc.get("buffers", []):
        uri = buf.get("uri", "")
        if uri.startswith("data:"):
            b64 = uri.split(",", 1)[1] if "," in uri else ""
            total += len(base64.b64decode(b64))
        else:
            total += buf.get("byteLength", 0)
    for img in doc.get("images", []):
        if "uri" in img:
            total += img.get("byteLength", 0)
        elif "bufferView" in img:
            bv = doc.get("bufferViews", [])[img["bufferView"]]
            total += bv.get("byteLength", 0)
    return total


def geometry(doc):
    acc = doc.get("accessors", [])
    verts = tris = 0
    for mesh in doc.get("meshes", []):
        for prim in mesh.get("primitives", []):
            pos = prim.get("attributes", {}).get("POSITION")
            if pos is not None and pos < len(acc):
                verts += acc[pos].get("count", 0)
            idx = prim.get("indices")
            if idx is not None and idx < len(acc):
                tris += acc[idx].get("count", 0) // 3
    return verts, tris


def main():
    ap = argparse.ArgumentParser(description="Presupuesto de un asset glTF/GLB")
    ap.add_argument("path")
    ap.add_argument("--tris", type=int, default=20000)
    ap.add_argument("--mb", type=float, default=5.0)
    ap.add_argument("--anims", type=int, default=20)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    try:
        doc, size = load_gltf(args.path)
    except Exception as exc:  # noqa: BLE001 - queremos el mensaje crudo
        print(f"ERROR {args.path}: {exc}")
        return 2

    verts, tris = geometry(doc)
    mb = size / (1024 * 1024)
    payload_mb = embedded_bytes(doc) / (1024 * 1024)
    anims = len(doc.get("animations", []))
    meshes = len(doc.get("meshes", []))
    mats = len(doc.get("materials", []))

    if not args.quiet:
        print(f"archivo   {os.path.basename(args.path)}")
        print(f"tamano    {mb:6.2f} MB  (payload embebido {payload_mb:.2f} MB)")
        print(f"geometria {verts:7d} verts / {tris:7d} tris / {meshes} meshes / {mats} mats")
        print(f"anim      {anims} clips")

    fails = []
    if tris > args.tris:
        fails.append(f"tris {tris} > {args.tris}")
    if mb > args.mb:
        fails.append(f"tamano {mb:.2f} MB > {args.mb} MB")
    if anims > args.anims:
        fails.append(f"clips {anims} > {args.anims}")

    if fails:
        print("FAIL     " + "; ".join(fails))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
