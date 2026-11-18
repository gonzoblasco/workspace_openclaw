#!/usr/bin/env python3
"""
tts-kokoro.py — motor Kokoro-82M para español. Sin autoregresión, sin cola alucinada.

Por qué este motor y no Chatterbox: Kokoro es un modelo acústico no autoregresivo.
No genera token por token, así que no puede "seguir inventando" cuando el texto termina.
El precio es menos emoción por frase; el beneficio es que un audiolibro de 17 capítulos
no necesita cirugía de audio en cada tramo.

Uso:
    python3 scripts/tts-kokoro.py archivo.md --out salida.m4a
    python3 scripts/tts-kokoro.py archivo.md --out salida.m4a --voz em_alex
    python3 scripts/tts-kokoro.py archivo.md --out salida.m4a --semitono -3 --grano 0.25

Requiere: .venvs/kokoro (kokoro + soundfile)
"""

import argparse
import os
import re
import subprocess
import sys
import time

import numpy as np
import soundfile as sf
from kokoro import KPipeline

SAMPLE_RATE = 24000
MAX_CHARS = 400  # Kokoro maneja tramos más largos sin desbordar


def strip_markdown(text: str) -> str:
    t = re.sub(r"^#+\s*", "", text, flags=re.M)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = t.replace("---", " ")
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def chunk_por_parrafo(text: str, max_chars: int):
    """Parte por párrafo y, si un párrafo es muy largo, por oración.
    Nunca corta en medio de una palabra: es el bug que ensuciaba a Chatterbox."""
    out = []
    for par in re.split(r"\n\s*\n", text):
        par = par.strip()
        if not par:
            continue
        if len(par) <= max_chars:
            out.append(par)
            continue
        buf = ""
        for frase in re.split(r"(?<=[.!?…])\s+", par):
            if len(buf) + len(frase) + 1 <= max_chars:
                buf = f"{buf} {frase}".strip()
            else:
                if buf:
                    out.append(buf)
                buf = frase
        if buf:
            out.append(buf)
    return out


def postproceso(path: str, semitono: float, grano: float, aire: float):
    """Cadena opcional de color: baja el tono y agrega un poco de cuerpo."""
    if semitono == 0 and grano == 0:
        return
    f = 2 ** (semitono / 12)
    cadena = [
        f"asetrate={SAMPLE_RATE}*{f:.6f}",
        f"aresample={SAMPLE_RATE}",
        f"atempo={1 / f:.6f}",
        "equalizer=f=150:t=q:w=1.1:g=3.5",
        "equalizer=f=3500:t=q:w=1.4:g=-1.5",
    ]
    # El filtro `chorus` de ffmpeg rompe a 24 kHz (delay más corto que su buffer).
    # El mismo efecto se arma con un desdoble adelantado y una mezcla con peso.
    if grano > 0:
        # rama seca: el desdoble con adelay no puede mezclarse después de otros filtros
        # en la misma cadena lineal, así que el grano va en su propio paso.
        tmp1 = path + ".dry.wav"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", path,
                        "-af", ",".join(cadena), tmp1], check=True)
        tmp = path + ".pp.wav"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", tmp1,
                        "-af", "asplit=2[g1][g2];[g2]adelay=28[g2d];"
                              f"[g1][g2d]amix=inputs=2:weights=1 {grano:.2f}:normalize=0"
                              + (f",treble=g={aire}" if aire else ""),
                        tmp], check=True)
        os.remove(tmp1)
    else:
        tmp = path + ".pp.wav"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", path,
                        "-af", ",".join(cadena), tmp], check=True)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", required=True)
    ap.add_argument("--voz", default="em_alex", help="em_alex, em_santa, ef_dora")
    ap.add_argument("--velocidad", type=float, default=1.075,
                    help="1.075 es la voz oficial (10%% más rápida que 0.92)")
    ap.add_argument("--semitono", type=float, default=-3.0, help="negativo = más grave")
    ap.add_argument("--grano", type=float, default=0.25, help="0 a 0.6, desdoble de voz")
    ap.add_argument("--aire", type=float, default=1.0, help="dB de agudos")
    ap.add_argument("--limit-chars", type=int, default=0)
    args = ap.parse_args()

    text = strip_markdown(open(args.source, encoding="utf-8").read())
    if args.limit_chars:
        text = text[: args.limit_chars]

    chunks = chunk_por_parrafo(text, MAX_CHARS)
    print(f"{len(chunks)} tramos por párrafo, voz {args.voz}, velocidad {args.velocidad}")

    pipeline = KPipeline(lang_code="e", repo_id="hexgrad/Kokoro-82M")

    pedazos = []
    t0 = time.time()
    for i, c in enumerate(chunks, 1):
        for _, _, audio in pipeline(c, voice=args.voz, speed=args.velocidad):
            pedazos.append(audio.numpy() if hasattr(audio, "numpy") else np.asarray(audio))
        if i % 5 == 0 or i == len(chunks):
            el = time.time() - t0
            print(f"{i}/{len(chunks)} · {el:.0f}s · ~{el / i * (len(chunks) - i):.0f}s restantes",
                  flush=True)

    audio = np.concatenate(pedazos) if pedazos else np.zeros(SAMPLE_RATE // 2, dtype=np.float32)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    wav = args.out + ".raw.wav"
    sf.write(wav, audio, SAMPLE_RATE)

    postproceso(wav, args.semitono, args.grano, args.aire)

    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", wav,
                    "-af", "loudnorm=I=-17:TP=-1.8:LRA=9",
                    "-ar", str(SAMPLE_RATE), "-c:a", "aac", "-b:a", "96k", args.out],
                   check=True)
    os.remove(wav)
    print("listo:", args.out)


if __name__ == "__main__":
    main()
