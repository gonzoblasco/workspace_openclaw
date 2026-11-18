#!/usr/bin/env python3
"""
tts-dramatize.py — una voz por personaje, turno por turno.

No es magia: reparte las voces por atribución ("—dijo Vera") y une los tramos con
ffmpeg. La ironía no la resuelve: eso depende del proveedor, no del reparto.

Uso:
    python3 scripts/tts-dramatize.py archivo.md --out /tmp/escena.m4a --map cast.json
    python3 scripts/tts-dramatize.py archivo.md --out /tmp/x.m4a --print-map   # solo ver el reparto
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib.machinery import SourceFileLoader
tts = SourceFileLoader("tts", os.path.join(os.path.dirname(os.path.abspath(__file__)), "tts-render.py")).load_module()

# Elenco por defecto: una voz por personaje y una para el narrador.
CAST = {
    "narrador": {"voice": "es-MX-JorgeNeural", "rate": "-0%", "pitch": "+0Hz"},
    "Néstor":   {"voice": "es-AR-TomasNeural", "rate": "-0%", "pitch": "-2Hz"},
    "Vera":     {"voice": "es-AR-ElenaNeural", "rate": "-2%", "pitch": "-1Hz"},
    "Adán":     {"voice": "es-ES-AlvaroNeural", "rate": "-4%", "pitch": "-4Hz"},
}

NAMES = list(CAST.keys())[1:]
VERBS = r"(?:dijo|dice|preguntó|contestó|respondió|agregó|repitió|murmuró|gritó|siguió|empezó)"


FEMALE = {"Vera"}
VERB_ONLY = re.compile(rf"^\s*(?:{VERBS})\b")


def split_turn(para, who):
    """Parte un turno en lo que dice el personaje y lo que dice el narrador.

    "— No —dijo ella—. Se lo digo ahora."  →  [("Vera","No"), ("narrador","dijo ella"),
                                             ("Vera","Se lo digo ahora.")]
    """
    if "—" not in para:
        return [(who, para.strip())] if para.strip() else []
    pieces = para.split("—")
    out = []
    for i, piece in enumerate(pieces):
        piece = piece.strip(" ,;")
        if not piece:
            continue
        # Atribución: arranca con verbo de decir, o con un nombre seguido de verbo.
        if VERB_ONLY.match(piece) or re.match(rf"^(?:{'|'.join(NAMES)})\s+{VERBS}", piece):
            out.append(("narrador", piece))
            continue
        piece = piece.lstrip(". ").strip()
        if piece:
            out.append((who, piece))
    return out


def speaker_of(para, current, previous):
    """Quién habla: por atribución; por pronombre ("dijo ella"); si no, alterna."""
    for n in NAMES:
        if re.search(rf"{VERBS}\s+{n}\b", para) or re.search(rf"{n}\s+{VERBS}", para):
            return n
    if re.search(rf"{VERBS}\s+ella\b|ella\s+{VERBS}", para):
        return "Vera"
    if re.search(rf"{VERBS}\s+él\b|él\s+{VERBS}", para):
        for n in NAMES:
            if n not in FEMALE and n != current:
                return n
        return current
    # Sin atribución: en un intercambio, responde el que no habló en el turno anterior.
    if previous not in ("narrador", current):
        return previous
    return current


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", required=True)
    ap.add_argument("--map", help="json con el elenco; si falta, usa el default")
    ap.add_argument("--limit", type=int, default=0, help="cuántos párrafos dramatizar")
    ap.add_argument("--print-map", action="store_true")
    ap.add_argument("--fix", default="", help="correcciones a mano: '9:Néstor,12:Vera' (índice de turno)")
    args = ap.parse_args()

    cast = CAST
    if args.map and os.path.exists(args.map):
        cast = json.load(open(args.map, encoding="utf-8"))

    text = open(args.source, encoding="utf-8").read()
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    paras = [p for p in paras if p != "---" and not p.startswith("#")]
    if args.limit:
        paras = paras[:args.limit]

    turns = []
    current, previous = "narrador", "narrador"
    for p in paras:
        if p.startswith("—") or p.startswith(", "):
            who = speaker_of(p, current, previous)
            previous, current = current, who
            turns.append(("dialogo", who, p))
        else:
            turns.append(("narracion", "narrador", p))

    if args.fix:
        fixes = dict(item.split(":") for item in args.fix.split(",") if ":" in item)
        for idx, who in fixes.items():
            i = int(idx) - 1
            if 0 <= i < len(turns):
                turns[i] = (turns[i][0], who.strip(), turns[i][2])

    if args.print_map:
        for i, (kind, who, p) in enumerate(turns, 1):
            print(f"{i:3} [{who:9}] {p[:60]}")
        return

    work = tempfile.mkdtemp(prefix="drama-")
    pieces = []
    seq = []
    for kind, who, p in turns:
        if kind == "dialogo":
            for sub_who, sub_text in split_turn(p, who):
                seq.append((sub_who, sub_text))
        else:
            seq.append((who, p))

    for i, (who, p) in enumerate(seq, 1):
        cfg = cast.get(who, cast["narrador"])
        clean = tts.strip_markdown(p).strip().rstrip(",")
        if not clean or not re.search(r"\w", clean):
            continue
        src = os.path.join(work, f"{i}.txt")
        dst = os.path.join(work, f"{i}.mp3")
        open(src, "w", encoding="utf-8").write(clean)
        subprocess.run([tts.edge_tts_cmd(), "--voice", cfg["voice"],
                        f"--rate={cfg['rate']}", f"--pitch={cfg['pitch']}",
                        "-f", src, "--write-media", dst],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        pieces.append(dst)

    listfile = os.path.join(work, "list.txt")
    open(listfile, "w", encoding="utf-8").write("".join(f"file '{p}'\n" for p in pieces))
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
                    "-c:a", "aac", "-b:a", "64k", args.out],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    shutil.rmtree(work, ignore_errors=True)
    print(f"listo: {args.out} ({len(pieces)} turnos)")


if __name__ == "__main__":
    main()
