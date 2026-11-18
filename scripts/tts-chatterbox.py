#!/usr/bin/env python3
"""
tts-chatterbox.py — motor local, con emoción.

Chatterbox multilingual corriendo en la GPU de la Mac. Lento (varias veces el tiempo real)
pero con una perilla que edge-tts no tiene: `exaggeration`, que exagera o aplana la entonación.

Uso:
    python3 scripts/tts-chatterbox.py archivo.md --out /tmp/escena.m4a
    python3 scripts/tts-chatterbox.py archivo.md --out /tmp/x.m4a --exaggeration 0.8
    python3 scripts/tts-chatterbox.py archivo.md --out /tmp/x.m4a --limit-chars 900

Requiere: .venvs/chatterbox (chatterbox-tts + torch + resemble-perth)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

import perth
from perth import DummyWatermarker

# El watermarker neural de Perth no importa en este entorno; el dummy es suficiente
# para uso local (el watermark es de procedencia, no de calidad).
perth.PerthImplicitWatermarker = DummyWatermarker

import torch
import torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib.machinery import SourceFileLoader
tts = SourceFileLoader("tts", os.path.join(os.path.dirname(os.path.abspath(__file__)), "tts-render.py")).load_module()

MAX_CHARS = 240          # frases cortas: el modelo pierde el hilo en tramos largos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", required=True)
    ap.add_argument("--exaggeration", type=float, default=0.5)
    ap.add_argument("--cfg", type=float, default=0.5)
    ap.add_argument("--limit-chars", type=int, default=0)
    ap.add_argument("--deep", action="store_true",
                    help="voz adulta: -2 semitonos (formantes incluidos) + 3 dB en 180 Hz, -1,5 dB en 3,2 kHz")
    args = ap.parse_args()

    text = open(args.source, encoding="utf-8").read()
    if args.limit_chars:
        text = text[:args.limit_chars]
    clean = tts.strip_markdown(text)

    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    model = ChatterboxMultilingualTTS.from_pretrained(device=dev)

    chunks = tts.chunk(clean, MAX_CHARS)
    work = tempfile.mkdtemp(prefix="cbx-")
    wavs = []
    t0 = time.time()
    for i, c in enumerate(chunks, 1):
        wav = model.generate(c, language_id="es", exaggeration=args.exaggeration,
                             cfg_weight=args.cfg)
        path = os.path.join(work, f"{i:04}.wav")
        torchaudio.save(path, wav, model.sr)
        wavs.append(path)
        if i % 5 == 0 or i == len(chunks):
            el = time.time() - t0
            print(f"{i}/{len(chunks)} tramos · {el:.0f}s · ~{el/i*(len(chunks)-i):.0f}s restantes",
                  flush=True)

    listfile = os.path.join(work, "list.txt")
    open(listfile, "w", encoding="utf-8").write("".join(f"file '{w}'\n" for w in wavs))
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
                    "-c:a", "aac", "-b:a", "64k", args.out],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    shutil.rmtree(work, ignore_errors=True)

    if args.deep:
        f = 2 ** (-2 / 12)
        tmp = args.out + ".tmp.m4a"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", args.out,
                        "-af", f"asetrate={model.sr}*{f:.6f},aresample={model.sr},atempo={1/f:.6f},"
                               "equalizer=f=180:t=q:w=1.2:g=3,equalizer=f=3200:t=q:w=1.5:g=-1.5",
                        "-c:a", "aac", "-b:a", "96k", tmp], check=True)
        os.replace(tmp, args.out)

    print("listo:", args.out)


if __name__ == "__main__":
    main()
