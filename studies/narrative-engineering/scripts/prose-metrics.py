#!/usr/bin/env python3
"""Metricas de prosa para el Eje 5 (Voz y Prosa) del estudio de ingenieria narrativa.

Uso:
    python3 prose-metrics.py <archivo.txt|.md> [--perfil card|rowling|katzenbach]

Reporta por separado NARRACION y DIALOGO, con distribucion por bandas de longitud de
frase. La separacion es obligatoria: aplicada al texto entero, una escena de pelea
familiar da 45% de frases cortas solo porque los personajes hablan corto, y el
diagnostico sale invertido.

Perfiles de referencia (bandas <=6 / 7-15 / 16-30 / 31+, sobre NARRACION):
    card       9 mediana   | 35 / 47 / 16 / 1     (Caso 04, Ender's Game, narracion)
    rowling    16,5 mediana | 14 / 35 / 38 / 12  (Caso 05, Azkaban)
    katzenbach 12 mediana  | 24 / 41 / 27 / 8     (Caso 06, La sombra, narracion, es)
    echeverria 20,5 mediana | 14 / 25 / 30 / 31   (Caso 07, El matadero, 1838)

Nota de honestidad: las bandas de Card se recontaron el 2026-11-17 sobre la NARRACION
(155 frases). La version anterior de este script traia 65/33/2/0,9, que confundia el
porcentaje de frases <=10 palabras (65) con la banda <=6. Corregido.
"""
import re
import statistics
import sys

PROFILES = {
    "card": {
        "median": 9,
        "bands": (35, 47, 16, 1),
        "note": "bandas sobre narracion del Ch. 1 (155 frases), excluyendo dialogo",
    },
    "rowling": {
        "median": 16.5,
        "bands": (14, 35, 38, 12),
        "note": "bandas sobre narracion, excluyendo dialogo y documentos",
    },
    "echeverria": {
        "median": 20.5,
        "bands": (14, 25, 30, 31),
        "note": "bandas sobre narracion de El matadero (S.XIX, es); muestra con parrafo estimado",
    },
    "katzenbach": {
        "median": 12,
        "bands": (24, 41, 27, 8),
        "note": "bandas sobre narracion del fragmento es (228 frases); thriller en espanol",
    },
}

BANDS = [(1, 6), (7, 15), (16, 30), (31, 10**6)]
BAND_LABELS = ["<=6", "7-15", "16-30", "31+"]

DIALOGUE_PREFIXES = ('"', "\u201c", "\u2014", "--", "\u00ab")

# Atribuciones: verbos de decir en espanol e ingles.
ATTR = re.compile(
    r"\b(dijo|dice|pregunt[oó]|respondi[oó]|contest[oó]|grit[oó]|susurr[oó]|a[nñ]adi[oó]|"
    r"repiti[oó]|murmur[oó]|exclam[oó]|empez[oó]|sigui[oó]|"
    r"said|asked|replied|whispered|shouted|cried|muttered|bellowed|roared|answered)\b",
    re.IGNORECASE,
)


def load(path):
    text = open(path, encoding="utf-8").read()
    if "\n\n" in text:
        raw = re.split(r"\n\s*\n", text)
    else:
        raw = re.split(r"\n", text)
    paras = [" ".join(x.strip() for x in p.split("\n") if x.strip()) for p in raw]
    return [p for p in paras if p.strip()]


def is_dialogue(p):
    return p.startswith(DIALOGUE_PREFIXES)


def sentences(paras):
    out = []
    for p in paras:
        out += [s for s in re.split(r'(?<=[.!?\u201d"])\s+', p) if len(s.split()) > 1]
    return out


def band_distribution(lengths):
    total = len(lengths) or 1
    return [100 * sum(1 for x in lengths if lo <= x <= hi) / total for lo, hi in BANDS]


def report(label, sents):
    if not sents:
        print(f"  {label}: sin frases")
        return None
    lengths = [len(s.split()) for s in sents]
    bands = band_distribution(lengths)
    print(f"  {label}")
    print(f"    frases: {len(lengths)} | mediana: {statistics.median(lengths)} "
          f"| media: {round(statistics.mean(lengths), 1)} | max: {max(lengths)}")
    print("    bandas: " + " | ".join(
        f"{BAND_LABELS[i]}: {bands[i]:.0f}%" for i in range(4)
    ))
    return {"median": statistics.median(lengths), "bands": bands, "n": len(lengths)}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    profile = None
    if "--perfil" in sys.argv:
        i = sys.argv.index("--perfil")
        if i + 1 >= len(sys.argv):
            print(f"falta el valor de --perfil (opciones: {', '.join(PROFILES)})")
            sys.exit(1)
        profile = sys.argv[i + 1]

    paras = load(path)
    narration = [p for p in paras if not is_dialogue(p)]
    dialogue = [p for p in paras if is_dialogue(p)]
    words = sum(len(p.split()) for p in paras)
    if not words:
        print("archivo vacio")
        sys.exit(1)

    print(f"archivo: {path}")
    print(f"palabras: {words} | parrafos: {len(paras)} "
          f"| mediana palabras/parrafo: {statistics.median([len(p.split()) for p in paras])}")
    print()

    narr = report("NARRACION", sentences(narration))
    dia = report("DIALOGO", sentences(dialogue))

    print()
    print(f"  parrafos de dialogo: {len(dialogue)}/{len(paras)} "
          f"= {100 * len(dialogue) / len(paras):.0f}%")
    print(f"  palabras en dialogo: "
          f"{100 * sum(len(p.split()) for p in dialogue) / words:.0f}%")
    print()

    attr = ATTR.findall(" ".join(dialogue)) if dialogue else []
    dlg_words = sum(len(p.split()) for p in dialogue)
    print(f"  atribuciones: {len(attr)}")
    if attr and dlg_words:
        print(f"    por 1000 palabras de dialogo: {1000 * len(attr) / dlg_words:.1f}")

    joined = " ".join(paras)
    n_mente = len(re.findall(r"\b\w+mente\b", joined))
    n_ly = len(re.findall(r"\b\w+ly\b", joined))
    n_semicolon = joined.count(";")
    n_guillemet = joined.count("\u00ab")
    print()
    print(f"  punto y coma: {n_semicolon}")
    print(f"  adverbios -mente: {n_mente}")
    print(f"  adverbios -ly (ingles): {n_ly}")
    print(f"  comillas angulares: {n_guillemet}")

    # Pensamiento: cursiva entre asteriscos (convencion propia) o primera persona suelta.
    italic = re.findall(r"\*[^*\n]{8,}\*", "\n\n".join(paras))
    FP = (r"\b(yo|nosotros|nosotras)\b"
          r"|\b(soy|estoy|tengo|dije|pens[eé]|quise|supe|vine)\b"
          r"|\bno\s+s[eé]\b")
    fp = [p for p in narration if re.search(FP, p, re.IGNORECASE)]
    print()
    print(f"  pensamiento en cursiva: {len(italic)} "
          f"({100 * len(italic) / words:.2f} por 100 palabras)")
    print(f"  primera persona suelta en narracion: {len(fp)} parrafos "
          f"({100 * len(fp) / words:.2f} por 100 palabras)")

    if profile:
        ref = PROFILES.get(profile)
        if not ref:
            print(f"\n  perfil desconocido: {profile} (opciones: {', '.join(PROFILES)})")
            return
        if not narr:
            return
        print()
        print(f"  --- comparacion con perfil {profile} ---")
        print(f"  {ref['note']}")
        print(f"    mediana   ref {ref['median']:<6} texto {narr['median']:<6} "
              f"delta {narr['median'] - ref['median']:+.1f}")
        for i in range(4):
            d = narr["bands"][i] - ref["bands"][i]
            flag = "OK" if abs(d) <= 7 else ("alto" if d > 0 else "bajo")
            print(f"    {BAND_LABELS[i]:<6} ref {ref['bands'][i]:>5.1f}%  "
                  f"texto {narr['bands'][i]:>5.1f}%  delta {d:+5.1f}  {flag}")


if __name__ == "__main__":
    main()
