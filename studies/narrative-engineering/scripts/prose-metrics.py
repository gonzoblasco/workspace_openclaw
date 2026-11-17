#!/usr/bin/env python3
"""Metricas de prosa para el Eje 5 (Voz y Prosa) del estudio de ingenieria narrativa.

Uso:
    python3 prose-metrics.py <archivo.txt>

Mide ritmo, dialogo, atribuciones y marcas de estilo del texto.
Referencia de calibracion: caso-04-enders-game.md (Ch. 1, Card 1985).
"""
import re
import statistics
import sys

path = sys.argv[1]
t = open(path, encoding="utf-8").read()

_raw = re.split(r"\n\s*\n", t) if "\n\n" in t else re.split(r"\n", t)
paras = [" ".join(x.strip() for x in p.split("\n") if x.strip()) for p in _raw]
paras = [p for p in paras if p.strip()]
pw = [len(p.split()) for p in paras]
sents = re.split(r'(?<=[.!?"])\s+', " ".join(paras))
sents = [s for s in sents if len(s.split()) > 2]
sw = [len(s.split()) for s in sents]

print("palabras:", sum(pw))
print("parrafos:", len(paras), "| mediana palabras/parrafo:", statistics.median(pw), "| max:", max(pw))
print()
print("frases:", len(sw))
print("mediana palabras/frase:", statistics.median(sw))
print("media palabras/frase:", round(statistics.mean(sw), 1))
print("frase mas larga:", max(sw))
print("<=6 palabras:", round(100 * sum(1 for x in sw if x <= 6) / len(sw)), "%")
print("<=10 palabras:", round(100 * sum(1 for x in sw if x <= 10) / len(sw)), "%")
print(">=30 palabras:", round(100 * sum(1 for x in sw if x >= 30) / len(sw), 1), "%")
print()
# Dialogo: comillas (convencion Card) o raya (convencion de docs/stories).
dl = [
    p for p in paras
    if p.startswith('"') or p.startswith("\u201c") or p.startswith("\u2014") or p.startswith("--")
]
print("parrafos de dialogo:", len(dl), "/", len(paras), "=", round(100 * len(dl) / len(paras)), "%")
print("palabras en dialogo:", round(100 * sum(len(p.split()) for p in dl) / sum(pw)), "%")
print()
print("em dashes:", t.count("\u2014"))
print("guion doble (--):", t.count("--"))
print("punto y coma:", t.count(";"))
print("adverbios -ly (ingles):", len(re.findall(r"\b\w+ly\b", t)))
print("adverbios -mente (espanol):", len(re.findall(r"\b\w+mente\b", t)))
print()
# Pensamiento interno: parrafo entero en cursiva entre asteriscos (convencion propia),
# o primera persona suelta dentro de la prosa (convencion Card).
bold_thoughts = re.findall(r"\*[^*\n]{8,}\*", t)
words = sum(pw)
print("pensamientos en cursiva:", len(bold_thoughts), "| por 100 palabras:", round(len(bold_thoughts) * 100 / words, 1))

# Primera persona suelta en la narracion (convencion Card, sin comillas ni cursiva).
# Solo formas inequivocas: en espanol la mayoria de los verbos de primera persona son
# homografos de tercera ("miraba", "sabia", "iba"), asi que se exigen marcas fuertes:
# el pronombre "yo", el verbo "soy", la -e/-i de primera ("dije", "tengo") y "no se".
FP_STRONG = (
    r"\b(yo|nosotros|nosotras)\b"
    r"|\b(soy|estoy|tengo|dije|pens[eé]|quise|supe|vi|vine)\b"
    r"|\bno\s+s[eé]\b"
)
fp_paras = []
for p in paras:
    if p.startswith(('"', "\u201c", "\u2014", "--", "*")):
        continue
    if re.search(FP_STRONG, p, re.IGNORECASE):
        fp_paras.append(p)
print("parrafos con primera persona suelta:", len(fp_paras), "| por 100 palabras:", round(len(fp_paras) * 100 / words, 1))
