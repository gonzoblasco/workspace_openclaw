#!/usr/bin/env python3
"""
tts-kokoro.py — motor Kokoro-82M para español. Sin autoregresión, sin cola alucinada.

Por qué este motor: Kokoro es un modelo acústico no autoregresivo. No genera token por
token, así que no puede "seguir inventando" cuando el texto termina. Medido contra
Chatterbox en el mismo fragmento: 11 s contra 268 s, y 0,40 s de cola contra 7,6 s.

Por qué hay tres registros: la novela no es solo narración. Tiene diálogo (guion largo)
y pensamiento interior (párrafo entero en cursiva). Un narrador no los lee igual, y el
manuscrito ya lo dice con markup. El script no inventa emoción: **respeta la que el texto
declara**. Eso es distinto de etiquetar cada frase con "miedo" o "sorpresa", que produce
un actor haciendo sketches en vez de un narrador.

Las notas de producción (`*POV: ...*`, `*Fin del capítulo.*`) NO se narran: son metadata
del autor, no parte del libro.

Uso:
    python3 scripts/tts-kokoro.py capitulo.md --out salida.m4a
    python3 scripts/tts-kokoro.py capitulo.md --out salida.m4a --plano   # sin registros
    python3 scripts/tts-kokoro.py capitulo.md --out x.m4a --voz em_santa

Requiere: .venvs/kokoro (kokoro + soundfile)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np
import soundfile as sf
from kokoro import KPipeline

SAMPLE_RATE = 24000
MAX_CHARS = 400

# Prefijos de notas de producción. Se comparan sobre el texto de un párrafo que está
# entero en cursiva. Si coincide, el párrafo no es del libro y no se narra.
META_PREFIJOS = (
    "POV",
    "Nota",
    "TODO",
    "Escrito con",
    "Fin del Acto",
    "Fin del capítulo",
)


def drop_metadata(text: str) -> str:
    """Quita las notas de producción. Hay que hacerlo ANTES de sacar el markdown:
    una vez que se borran los asteriscos, la nota ya no se distingue del pensamiento."""
    out = []
    for linea in text.split("\n"):
        s = linea.strip()
        if len(s) > 2 and s.startswith("*") and s.endswith("*") and not s[1:-1].strip().startswith("*"):
            interior = s.strip("*").strip()
            if interior.startswith(META_PREFIJOS):
                continue
        out.append(linea)
    return "\n".join(out)


def strip_markdown(text: str) -> str:
    t = re.sub(r"^#+\s*", "", text, flags=re.M)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = t.replace("---", " ")
    # La raya de diálogo NO puede llegar al fonemizador: produce un fonema que el modelo
    # no conoce y lo rellena con un sonido fantasma de ~60 ms antes de la vocal ("Ah"
    # suena "nahh"). En este manuscrito las 1432 rayas están al inicio de párrafo, así
    # que el límite de párrafo ya separa los turnos y la raya no aporta nada.
    t = re.sub(r"^\s*[—–]\s*", "", t, flags=re.M)
    t = t.replace("\u00bf", "").replace("\u00a1", "")
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def clasificar(text: str):
    """Devuelve [(registro, parrafo)]. Los tres registros de la novela:
    pensamiento (párrafo entero en cursiva), dialogo (guion largo), narracion."""
    segs = []
    for par in re.split(r"\n\s*\n", text):
        par = par.strip()
        if not par:
            continue
        s = par.strip()
        if len(s) > 2 and s.startswith("*") and s.endswith("*"):
            segs.append(("pensamiento", s.strip("*").strip()))
        elif s.startswith("—") or s.startswith("- "):
            segs.append(("dialogo", s))
        else:
            segs.append(("narracion", s))
    return segs


def chunk_por_parrafo(text: str, max_chars: int):
    """Parte por párrafo y, si un párrafo es muy largo, por oración.
    Nunca corta en medio de una palabra: ese era el bug que ensuciaba a Chatterbox."""
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


def cadena_tono(semitono: float, grano: float, aire: float):
    f = 2 ** (semitono / 12)
    pasos = [
        f"asetrate={SAMPLE_RATE}*{f:.6f}",
        f"aresample={SAMPLE_RATE}",
        f"atempo={1 / f:.6f}",
        "equalizer=f=150:t=q:w=1.1:g=3.5",
        "equalizer=f=3500:t=q:w=1.4:g=-1.5",
    ]
    if grano > 0:
        pasos.append(f"treble=g={aire}" if aire else "anull")
    return ",".join(pasos)


def aplicar_tono(path: str, semitono: float, grano: float, aire: float):
    """Baja el tono y da cuerpo. El grano va en un segundo paso porque el filtro
    `chorus` de ffmpeg rompe a 24 kHz y el reemplazo (asplit+adelay+amix) no se puede
    encadenar en la misma línea de filtros."""
    if semitono == 0 and grano == 0:
        return
    cad = cadena_tono(semitono, grano, aire)
    tmp1 = path + ".dry.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", path,
                    "-af", cad, tmp1], check=True)
    tmp2 = path + ".pp.wav"
    if grano > 0:
        extra = f",treble=g={aire}" if aire else ""
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", tmp1,
                        "-af", "asplit=2[g1][g2];[g2]adelay=28[g2d];"
                               f"[g1][g2d]amix=inputs=2:weights=1 {grano:.2f}:normalize=0{extra}",
                        tmp2], check=True)
        os.remove(tmp1)
    else:
        os.replace(tmp1, tmp2)
    os.replace(tmp2, path)


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

    # Registros. Por defecto van encendidos: el manuscrito declara el registro con
    # markup y ignorarlo es perder lo que el texto ya dice.
    ap.add_argument("--plano", action="store_true",
                    help="leer todo con el mismo registro (desactiva pensamiento/dialogo)")
    ap.add_argument("--pensamiento-velocidad", type=float, default=0.94,
                    help="ritmo del pensamiento interior, relativo a la narración")
    ap.add_argument("--pensamiento-semitono", type=float, default=-1.0,
                    help="semitonos extra para el pensamiento (más cerca, más adentro)")
    ap.add_argument("--pensamiento-aire", type=float, default=0.22,
                    help="segundos de silencio antes y después del pensamiento")
    ap.add_argument("--dialogo-velocidad", type=float, default=1.02,
                    help="ritmo del diálogo (la gente habla más rápido que el narrador)")
    ap.add_argument("--dialogo-semitono", type=float, default=0.5,
                    help="semitonos extra para el diálogo")
    args = ap.parse_args()

    raw = open(args.source, encoding="utf-8").read()
    raw = drop_metadata(raw)
    if args.limit_chars:
        raw = raw[: args.limit_chars]

    registros = {}
    if args.plano:
        registros["narracion"] = ("", 1.0, 0.0)
    else:
        registros["narracion"] = ("", 1.0, 0.0)
        registros["pensamiento"] = ("", args.pensamiento_velocidad, args.pensamiento_semitono)
        registros["dialogo"] = ("", args.dialogo_velocidad, args.dialogo_semitono)

    segs = clasificar(raw) if not args.plano else [("narracion", raw)]
    trabajo = []
    for reg, texto in segs:
        if reg not in registros:
            reg = "narracion"
        limpio = strip_markdown(texto)
        for c in chunk_por_parrafo(limpio, MAX_CHARS):
            trabajo.append((reg, c))

    print(f"{len(trabajo)} tramos · voz {args.voz} · velocidad {args.velocidad}"
          + (" · plano" if args.plano else " · con registros"))

    pipeline = KPipeline(lang_code="e", repo_id="hexgrad/Kokoro-82M")
    work = tempfile.mkdtemp(prefix="kok-")
    wavs = []
    t0 = time.time()

    for i, (reg, c) in enumerate(trabajo, 1):
        _, vel_rel, semi_rel = registros[reg]
        pedazos = []
        for _, _, audio in pipeline(c, voice=args.voz, speed=args.velocidad * vel_rel):
            pedazos.append(audio.numpy() if hasattr(audio, "numpy") else np.asarray(audio))
        audio = np.concatenate(pedazos) if pedazos else np.zeros(SAMPLE_RATE // 10, dtype=np.float32)
        path = os.path.join(work, f"{i:04d}.wav")
        sf.write(path, audio, SAMPLE_RATE)
        if semi_rel != 0 or args.semitono != 0 or args.grano > 0:
            aplicar_tono(path, args.semitono + semi_rel, args.grano, args.aire)
        # El silencio es lo que de verdad distingue el pensamiento: un narrador toma
        # un tiempo antes y después de entrar en la cabeza del personaje. El cambio de
        # tono solo refuerza; medido, son ~3 Hz y no se percibe solo.
        if reg == "pensamiento" and args.pensamiento_aire > 0 and not args.plano:
            pad = np.zeros(int(SAMPLE_RATE * args.pensamiento_aire), dtype=np.float32)
            a = sf.read(path, dtype="float32")[0]
            sf.write(path, np.concatenate([pad, a, pad]), SAMPLE_RATE)
        wavs.append(path)
        if i % 10 == 0 or i == len(trabajo):
            el = time.time() - t0
            print(f"{i}/{len(trabajo)} · {el:.0f}s · ~{el / i * (len(trabajo) - i):.0f}s restantes",
                  flush=True)

    listfile = os.path.join(work, "list.txt")
    open(listfile, "w", encoding="utf-8").write("".join(f"file '{w}'\n" for w in wavs))
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", listfile,
                    "-af", "loudnorm=I=-17:TP=-1.8:LRA=9",
                    "-ar", str(SAMPLE_RATE), "-c:a", "aac", "-b:a", "96k", args.out],
                   check=True)
    shutil.rmtree(work, ignore_errors=True)
    print("listo:", args.out)


if __name__ == "__main__":
    main()
