#!/usr/bin/env python3
"""
tts-chatterbox.py — motor Chatterbox con clonación de voz. La voz del audiolibro (ADR-116).

Por qué este motor y no Kokoro: Kokoro es limpio y rapidísimo, pero es no autoregresivo y
calcula la entonación de la estructura del texto. Medido: "Viste a Vera." y "Viste a Vera?"
dan el MISMO contorno (154->103 y 154->105 Hz). No hace preguntas. En una novela con 1.432
líneas de diálogo eso deja todo el diálogo plano.

Este motor sí entona, porque genera token por token y decide la prosodia en el momento. El
precio es que puede alucinar una cola cuando el texto se corta mal: por eso acá se corta
SIEMPRE por párrafo y se recorta la cola por energía.

La voz: `em_alex` de Kokoro, con la referencia bajada 4 semitonos (100 Hz de mediana). Se
baja el tono de la REFERENCIA y no del resultado para que el modelo genere de cero a 24 kHz:
así el resultado es grave Y conserva 11,5 kHz de agudos. Bajar el audio final, en cambio,
cuesta 3 kHz de banda y suena apagado.

Uso:
    .venvs/chatterbox/bin/python scripts/tts-chatterbox.py capitulo.md --out cap.m4a
    ... --ref otra-referencia.wav --exaggeration 0.6
    ... --limit-chars 900        # prueba corta
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np
import torch
import torchaudio

import perth
from perth import DummyWatermarker

# El watermarker neural de Perth no importa en este entorno; el dummy alcanza para uso
# local (el watermark es de procedencia, no de calidad).
perth.PerthImplicitWatermarker = DummyWatermarker

from chatterbox.mtl_tts import ChatterboxMultilingualTTS

REF_POR_DEFECTO = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets/voces/baritono-jazz/referencia.wav",
)
VOCES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/voces"
)


def resolver_voz(nombre):
    """Resuelve una voz por nombre contra assets/voces/<nombre>/. Devuelve
    (ruta_referencia, exaggeration, cfg). El manifiesto es la fuente de verdad de la voz:
    así el mismo narrador sirve en cualquier proyecto sin copiar parámetros a mano."""
    base = os.path.join(VOCES_DIR, nombre)
    manifiesto = os.path.join(base, "voz.json")
    if not os.path.isdir(base):
        disponibles = sorted(
            d for d in os.listdir(VOCES_DIR)
            if os.path.isdir(os.path.join(VOCES_DIR, d))
        ) if os.path.isdir(VOCES_DIR) else []
        sys.exit(f"no existe la voz '{nombre}'. Disponibles: {', '.join(disponibles) or 'ninguna'}")
    cfg = {"exaggeration": 0.5, "cfg_weight": 0.5}
    if os.path.exists(manifiesto):
        with open(manifiesto, encoding="utf-8") as fh:
            cfg.update({k: v for k, v in json.load(fh).items() if k in cfg})
    ref = os.path.join(base, "referencia.wav")
    if not os.path.exists(ref):
        sys.exit(f"la voz '{nombre}' no tiene referencia.wav en {base}")
    return ref, cfg["exaggeration"], cfg["cfg_weight"]

MAX_CHARS = 400          # por oración; un párrafo largo se parte acá, nunca a mitad de palabra
COLA_MAX = 0.35          # segundos que se conservan después del último fonema
UMBRAL_COLA = 0.006      # por debajo de esto se considera silencio

META_PREFIJOS = ("POV", "Nota", "TODO", "Escrito con", "Fin del Acto", "Fin del capítulo")


def drop_metadata(text: str) -> str:
    """Quita las notas de producción del autor. Debe correr ANTES de sacar el markdown:
    una vez borrados los asteriscos, la nota no se distingue del pensamiento interior."""
    out = []
    for linea in text.split("\n"):
        s = linea.strip()
        if len(s) > 2 and s.startswith("*") and s.endswith("*"):
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
    # Las rayas NO pueden llegar al fonemizador: produce un fonema que el modelo no conoce
    # y rellena con ~60 ms de sonido fantasma ("Ah" suena "nahh"). Cada raya se traduce
    # según su función en el texto, no se borra a ciegas:
    #   inicio de línea     -> el límite de párrafo ya separa los turnos
    #   antes de un punto   -> cierra la cita: se descarta, el punto queda
    #   antes de minúscula  -> atribución ("—dijo"): es una coma
    #   antes de mayúscula  -> vuelve la voz: es un punto
    t = re.sub(r"^\s*[—–]\s*", "", t, flags=re.M)
    t = re.sub(r"\s*[—–]\s*\.", ".", t)
    t = re.sub(r"\s*[—–]\s*(?=[a-záéíóúñü])", ", ", t)
    t = re.sub(r"\s*[—–]\s*(?=[A-ZÁÉÍÓÚÑ])", ". ", t)
    t = re.sub(r"\s*[—–]\s*", ", ", t)
    # Pregunta cerrada seguida de atribución: "afuera?, preguntó" -> "afuera? preguntó".
    t = re.sub(r"([?!])\s*,\s*", r"\1 ", t)
    # El signo de apertura tampoco aporta: el cierre ya marca la pregunta, y medido da la
    # misma curva de entonación con y sin él.
    t = t.replace("\u00bf", "").replace("\u00a1", "")
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def chunk_por_parrafo(text: str, max_chars: int):
    """Parte por párrafo; si uno es muy largo, por oración. Nunca a mitad de palabra:
    ese era el bug que hacía alucinar la cola de 7,6 segundos."""
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


def recortar_cola(wav: np.ndarray, sr: int) -> np.ndarray:
    """Corta el silencio/ruido residual del final del tramo.

    Chatterbox cierra cada tramo con lo que sea: a veces silencio, a veces respiraciones
    y chasquidos de baja energía. Se recorta en el último punto con energía real y se
    dejan COLA_MAX segundos de gracia para no cortar el decay de la última sílaba."""
    if wav.size == 0:
        return wav
    absv = np.abs(wav)
    ventana = max(1, int(sr * 0.01))
    n = len(absv) // ventana
    if n == 0:
        return wav
    rms = np.sqrt(np.mean(absv[: n * ventana].reshape(n, ventana) ** 2, axis=1))
    con_energia = np.where(rms > UMBRAL_COLA)[0]
    if len(con_energia) == 0:
        return wav
    fin = (con_energia[-1] + 1) * ventana
    fin = min(len(wav), fin + int(sr * COLA_MAX))
    return wav[:fin]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", required=True)
    ap.add_argument("--voz", default="baritono-jazz",
                    help="nombre de la voz en assets/voces/ (por defecto baritono-jazz)")
    ap.add_argument("--ref", default=None, help="ruta de referencia; pisa a --voz")
    ap.add_argument("--exaggeration", type=float, default=None)
    ap.add_argument("--cfg", type=float, default=None)
    ap.add_argument("--limit-chars", type=int, default=0)
    ap.add_argument("--sin-recorte", action="store_true", help="no recortar la cola")
    args = ap.parse_args()

    ref_voz, exh_voz, cfg_voz = resolver_voz(args.voz)
    args.ref = args.ref or ref_voz
    args.exaggeration = exh_voz if args.exaggeration is None else args.exaggeration
    args.cfg = cfg_voz if args.cfg is None else args.cfg

    if not os.path.exists(args.ref):
        sys.exit(f"falta la referencia: {args.ref}")

    raw = drop_metadata(open(args.source, encoding="utf-8").read())
    if args.limit_chars:
        raw = raw[: args.limit_chars]
    limpio = strip_markdown(raw)
    chunks = chunk_por_parrafo(limpio, MAX_CHARS)
    print(f"{len(chunks)} tramos por párrafo · voz {args.voz} · "
          f"exaggeration {args.exaggeration}", flush=True)

    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    model = ChatterboxMultilingualTTS.from_pretrained(device=dev)
    model.prepare_conditionals(args.ref, exaggeration=args.exaggeration)

    work = tempfile.mkdtemp(prefix="cbx-")
    wavs = []
    t0 = time.time()
    for i, c in enumerate(chunks, 1):
        wav = model.generate(c, language_id="es", exaggeration=args.exaggeration,
                             cfg_weight=args.cfg)
        audio = wav.squeeze(0).cpu().numpy() if hasattr(wav, "cpu") else np.asarray(wav).squeeze()
        if not args.sin_recorte:
            audio = recortar_cola(audio, model.sr)
        path = os.path.join(work, f"{i:04d}.wav")
        torchaudio.save(path, torch.from_numpy(audio).unsqueeze(0), model.sr)
        wavs.append(path)
        if i % 5 == 0 or i == len(chunks):
            el = time.time() - t0
            print(f"{i}/{len(chunks)} · {el:.0f}s · ~{el / i * (len(chunks) - i):.0f}s restantes",
                  flush=True)

    listfile = os.path.join(work, "list.txt")
    open(listfile, "w", encoding="utf-8").write("".join(f"file '{w}'\n" for w in wavs))
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", listfile,
                    "-af", "loudnorm=I=-17:TP=-1.8:LRA=9",
                    "-c:a", "aac", "-b:a", "96k", args.out],
                   check=True)
    shutil.rmtree(work, ignore_errors=True)
    print("listo:", args.out)


if __name__ == "__main__":
    main()
