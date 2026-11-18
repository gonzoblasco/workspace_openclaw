#!/usr/bin/env python3
"""
tts-render.py — convierte un texto markdown en un archivo de voz.

Diseñado para el flujo de la casa: un capítulo, un archivo, reproducible.
La voz y los parámetros son flags porque el día que aparezca una mejor,
cambiar de voz tiene que ser una línea y no una migración.

Uso:
    python3 scripts/tts-render.py docs/stories/las_tres_sabanas/manuscript/capitulo_1-definitivo.md \
        --out docs/stories/las_tres_sabanas/audio/capitulo-1.m4a

    # muestra corta, para elegir voz
    python3 scripts/tts-render.py archivo.md --limit-chars 1800 --out /tmp/muestra.m4a

    python3 scripts/tts-render.py --voices          # voces en español disponibles

Requiere: edge-tts (pip, en .venvs/tts) y ffmpeg.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PY = os.path.join(REPO, ".venvs", "tts", "bin", "python")

# El perfil vigente. Cambiar acá cambia el default de todo el flujo.
VOICE = "es-AR-TomasNeural"
RATE = "-4%"
PITCH = "-2Hz"
MAX_CHARS = 2200          # edge-tts corta bien hasta ~4k; 2.2k da margen y permite concatenar limpio


def edge_tts_cmd():
    """Devuelve el ejecutable de edge-tts, prefiriendo el venv del workspace."""
    for cand in (os.path.join(REPO, ".venvs", "tts", "bin", "edge-tts"),
                 shutil.which("edge-tts")):
        if cand and os.path.exists(cand):
            return cand
    sys.exit("edge-tts no está instalado. Ver skills/text-to-speech/SKILL.md")


def strip_markdown(text):
    """Deja el texto listo para leer: sin marcas, con pausas en los diálogos."""
    out = []
    for line in text.split("\n"):
        s = line.rstrip()
        if s.startswith("#"):                 # encabezados
            continue
        if s.strip() in ("---", "***", "___"):
            out.append("")
            continue
        if s.startswith("*") and s.endswith("*") and len(s) > 2:
            s = s[1:-1]                      # pensamiento del POV: se lee, no se marca
        s = s.replace("**", "").replace("`", "")
        out.append(s)
    text = "\n".join(out)

    # Diálogo con raya: "—Hola —dijo." → ", Hola, dijo."
    text = text.replace("—", ", ")
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\.\s*,", ".", text)
    text = re.sub(r",\s*\.", ".", text)
    text = re.sub(r"^\s*,\s*", "", text, flags=re.M)
    # Comillas de énfasis y corchetes no aportan nada al oído
    text = text.replace("«", '"').replace("»", '"')
    return text


def chunk(text, max_chars):
    """Corta en párrafos enteros, sin partir frases."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if len(p) > max_chars:               # párrafo monstruoso: se parte por oraciones
            parts = re.split(r"(?<=[.!?…])\s+", p)
            for part in parts:
                if len(cur) + len(part) + 2 > max_chars and cur:
                    chunks.append(cur.strip()); cur = ""
                cur += part + " "
            continue
        if len(cur) + len(p) + 2 > max_chars and cur:
            chunks.append(cur.strip()); cur = ""
        cur += p + "\n\n"
    if cur.strip():
        chunks.append(cur.strip())
    return chunks


def render(text, out_path, voice, rate, pitch):
    binary = edge_tts_cmd()
    work = tempfile.mkdtemp(prefix="tts-")
    pieces = []
    parts = chunk(strip_markdown(text), MAX_CHARS)
    for i, part in enumerate(parts, 1):
        src = os.path.join(work, f"p{i}.txt")
        dst = os.path.join(work, f"p{i}.mp3")
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(part)
        subprocess.run([binary, "--voice", voice, f"--rate={rate}", f"--pitch={pitch}",
                        "-f", src, "--write-media", dst], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        pieces.append(dst)

    listfile = os.path.join(work, "list.txt")
    with open(listfile, "w", encoding="utf-8") as fh:
        for p in pieces:
            fh.write(f"file '{p}'\n")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
                    "-c:a", "aac", "-b:a", "64k", out_path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    shutil.rmtree(work, ignore_errors=True)
    return len(parts)


def main():
    ap = argparse.ArgumentParser(description="Texto markdown → archivo de voz")
    ap.add_argument("source", nargs="?", help="archivo markdown de entrada")
    ap.add_argument("--out", help="archivo de salida (.m4a)")
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--rate", default=RATE)
    ap.add_argument("--pitch", default=PITCH)
    ap.add_argument("--limit-chars", type=int, default=0, help="recorta la entrada (para muestras)")
    ap.add_argument("--force", action="store_true", help="re-renderizar aunque exista")
    ap.add_argument("--voices", action="store_true", help="lista las voces en español")
    args = ap.parse_args()

    if args.voices:
        out = subprocess.run([edge_tts_cmd(), "--list-voices"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if "es-AR" in line or "es-MX" in line or "es-ES" in line:
                print(line)
        return

    if not args.source or not args.out:
        ap.error("hacen falta el archivo de entrada y --out")

    text = open(args.source, encoding="utf-8").read()
    if args.limit_chars:
        text = text[:args.limit_chars]

    if os.path.exists(args.out) and not args.force:
        meta_path = args.out + ".json"
        if os.path.exists(meta_path):
            meta = json.load(open(meta_path, encoding="utf-8"))
            digest = hashlib.sha256(text.encode()).hexdigest()[:16]
            if (meta.get("sha") == digest and meta.get("voice") == args.voice
                    and meta.get("rate") == args.rate and meta.get("pitch") == args.pitch):
                print(f"ya existe y no cambió: {args.out}")
                return

    n = render(text, args.out, args.voice, args.rate, args.pitch)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", args.out],
                         capture_output=True, text=True).stdout.strip()
    meta = {
        "source": os.path.relpath(os.path.abspath(args.source), REPO),
        "voice": args.voice, "rate": args.rate, "pitch": args.pitch,
        "chunks": n, "seconds": round(float(dur or 0), 1),
        "sha": hashlib.sha256(text.encode()).hexdigest()[:16],
    }
    with open(args.out + ".json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    print(f"listo: {args.out}  ({n} tramos, {int(float(dur or 0)//60)}:{int(float(dur or 0)%60):02d})")


if __name__ == "__main__":
    main()
