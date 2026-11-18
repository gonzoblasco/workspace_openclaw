#!/usr/bin/env python3
"""
voz-jazz-test.py — escalera de voces graves con grano, para elegir la del próximo render.

Toma el WAV limpio de Chatterbox (sin `--deep`) y aplica una cadena de efectos
por escalón, para poder escuchar la progresión y decidir con el oído, no con la teoría.

Cadena:
  1. asetrate/atempo  -> baja el tono N semitonos conservando la duración
  2. equalizer         -> refuerzo del cuerpo (100-220 Hz) y recorte de dureza (3-4 kHz)
  3. compand           -> compresión lenta: aplasta los picos y sube el aire, el "peso"
  4. chorus (suave)    -> desdoble corto, el grano de una voz vieja en un micrófono viejo
  5. highshelf         -> un poco de aire, para que el grano no sea opacidad

Uso:
    python3 scripts/voz-jazz-test.py <entrada.wav> --out-dir /tmp/voz-jazz
"""

import argparse
import os
import subprocess


def cadena(sr, semitonos, cuerpo, dureza, grano, aire, drive):
    f = 2 ** (semitonos / 12)
    pasos = [
        f"asetrate={sr}*{f:.6f}",
        f"aresample={sr}",
        f"atempo={1 / f:.6f}",
        f"equalizer=f=150:t=q:w=1.1:g={cuerpo}",
        f"equalizer=f=3500:t=q:w=1.4:g={dureza}",
        # saturación suave: el grano. drive bajo evita distorsión audible.
        f"volume={drive}dB",
        "alimiter=limit=0.94:level=false",
        f"volume=-{drive}dB",
    ]
    if grano > 0:
        # chorus de 2 voces, delay corto, poca profundidad: solo ensucia
        pasos.append(
            f"chorus=0.55:0.9:44|53:0.25|0.2:{grano:.2f}|{grano * 0.8:.2f}"
        )
    if aire:
        pasos.append(f"treble=g={aire}")
    return ",".join(pasos)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out-dir", default="/tmp/voz-jazz")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    sr_probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=sample_rate", "-of", "default=nw=1:nk=1", args.source],
        capture_output=True, text=True, check=True,
    )
    sr = int(sr_probe.stdout.strip())
    print(f"sample rate: {sr}")

    escalones = [
        # nombre              semi  cuerpo dureza grano aire drive
        ("01-referencia",     0,    0,     0,     0.00, 0,   0),
        ("02-deep-actual",   -2,    3,    -1.5,   0.00, 0,   0),
        ("03-grave",         -3,    4,    -2,     0.00, 0,   0),
        ("04-jazz",          -3,    5,    -2.5,   0.35, 1,   4),
        ("05-jazz-hondo",    -4,    5,    -3,     0.45, 1,   5),
        ("06-jazz-baritono", -5,    6,    -3,     0.55, 2,   5),
    ]

    for nombre, semi, cuerpo, dureza, grano, aire, drive in escalones:
        out = os.path.join(args.out_dir, f"{nombre}.m4a")
        cad = cadena(sr, semi, cuerpo, dureza, grano, aire, drive)
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
               "-i", args.source, "-af", cad,
               "-c:a", "aac", "-b:a", "96k", out]
        subprocess.run(cmd, check=True)
        print(f"{nombre:18s} {semi:+d} st  grano={grano:.2f} -> {out}")


if __name__ == "__main__":
    main()
