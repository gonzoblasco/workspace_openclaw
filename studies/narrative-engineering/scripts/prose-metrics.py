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

paras = [p.strip() for p in re.split(r"\n", t) if p.strip()]
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
dl = [p for p in paras if p.startswith('"')]
print("parrafos de dialogo:", len(dl), "/", len(paras), "=", round(100 * len(dl) / len(paras)), "%")
print("palabras en dialogo:", round(100 * sum(len(p.split()) for p in dl) / sum(pw)), "%")
print()
print("em dashes:", t.count("\u2014"))
print("guion doble (--):", t.count("--"))
print("punto y coma:", t.count(";"))
print("adverbios -ly:", len(re.findall(r"\b\w+ly\b", t)))
