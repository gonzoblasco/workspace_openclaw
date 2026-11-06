#!/usr/bin/env python3
"""review-charts.py - Graficos de una resena de modelo a partir de mediciones.jsonl.

Tres figuras cubren casi cualquier resena (ver model-review-documentation):
  1. latencia por prueba, con la media marcada
  2. perfil de veredictos (cuantas correctas, falsas, incompletas, sin entrega)
  3. tokens de salida vs segundos, para ver si la longitud explica el tiempo

Paleta fija: verde para lo que funciona, rojo para el fallo unico, ambar para lo dudoso.

Uso:
    review-charts.py --mediciones <mediciones.jsonl> --out <dir> [--veredicto veredicto.md]

Salida: fig1_latencia.png, fig2_veredictos.png, fig3_tokens.png en <dir>.
Exit: 0 ok, 2 uso invalido, 4 faltan datos.
"""
import argparse
import json
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ACC = "#2f6f4f"
DARK = "#1d1f1e"
GREY = "#8a8f8c"
LIGHT = "#dfe3e0"
RED = "#a8432f"
AMBER = "#b07d2a"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": "#c8ccc9",
})

ETIQUETAS = {
    "p1_funcion_simple": "Función\nsimple",
    "p2_explicacion": "Explicación",
    "p3_debug": "Debug",
    "p4_refactor": "Refactor",
    "p5_complejo": "Algoritmo\ncomplejo",
    "p6_trampa": "Pregunta\ntrampa",
    "p7_local": "Soporte\nusuario",
}


def cargar(path):
    recs = []
    with open(path, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            try:
                recs.append(json.loads(linea))
            except json.JSONDecodeError:
                # Compatibilidad con archivos viejos escritos multilinea.
                pass
    if not recs:
        # segundo intento: parsear el archivo entero como secuencia de objetos
        buf, acc = "", []
        for linea in open(path, encoding="utf-8"):
            buf += linea
            try:
                acc.append(json.loads(buf))
                buf = ""
            except json.JSONDecodeError:
                continue
        recs = acc
    return recs


def veredictos(path):
    """Lee la tabla de veredictos del evaluador. Devuelve {id: veredicto}."""
    if not path or not os.path.exists(path):
        return {}
    texto = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^\|\s*([cp]\d+_\w+)\s*\|\s*(\w+)\s*\|", texto, re.M):
        out[m.group(1)] = m.group(2).upper()
    return out


def fig_latencia(recs, out, vered):
    ids = [r["id"] for r in recs if r.get("secs")]
    if not ids:
        return None
    secs = [r["secs"] for r in recs if r.get("secs")]
    color = []
    for i in ids:
        v = vered.get(i, "")
        color.append(RED if v in ("FALSO", "NO_ENTREGA") else ACC)

    fig, ax = plt.subplots(figsize=(7.2, 3.0), dpi=200)
    barras = ax.bar([ETIQUETAS.get(i, i) for i in ids], secs, color=color, width=0.62)
    for b, t in zip(barras, secs):
        ax.text(b.get_x() + b.get_width() / 2, t + max(secs) * 0.02, f"{t:.1f}s",
                ha="center", va="bottom", fontsize=9, color=DARK, fontweight="bold")
    ax.axhline(sum(secs) / len(secs), color=GREY, ls=":", lw=1)
    ax.set_ylabel("segundos", color=DARK)
    ax.set_ylim(0, max(secs) * 1.18)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=DARK, labelsize=8.5)
    ax.text(len(ids) - 0.5, sum(secs) / len(secs) + max(secs) * 0.03,
            f"media {sum(secs)/len(secs):.1f}s", fontsize=8, color=GREY, ha="right")
    ax.set_title("Latencia por prueba", fontsize=11, color=DARK, pad=12,
                 loc="left", fontweight="bold")
    plt.tight_layout()
    p = os.path.join(out, "fig1_latencia.png")
    plt.savefig(p, facecolor="white")
    plt.close()
    return p


def fig_veredictos(vered, out):
    if not vered:
        return None
    orden = ["CORRECTO", "INCOMPLETO", "NO_VERIFICABLE", "FALSO", "NO_ENTREGA"]
    cuenta = {k: 0 for k in orden}
    for v in vered.values():
        clave = "NO_ENTREGA" if v in ("NO_ENTREGA", "NO_ENTREGO") else v
        if clave in cuenta:
            cuenta[clave] += 1
    presentes = [k for k in orden if cuenta[k] > 0]
    if not presentes:
        return None

    colores = {"CORRECTO": ACC, "INCOMPLETO": AMBER, "NO_VERIFICABLE": GREY,
               "FALSO": RED, "NO_ENTREGA": DARK}
    vals = [cuenta[k] for k in presentes]

    fig, ax = plt.subplots(figsize=(7.2, 2.2), dpi=200)
    izq = 0
    for k, v in zip(presentes, vals):
        ax.barh([0], [v], left=izq, color=colores[k], height=0.5,
                edgecolor="white", linewidth=1.5)
        ax.text(izq + v / 2, 0, f"{k}\n{v}", ha="center", va="center",
                fontsize=9, color="white", fontweight="bold")
        izq += v
    ax.set_xlim(0, sum(vals))
    ax.set_yticks([])
    ax.set_xlabel("pruebas", color=DARK)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(colors=DARK, labelsize=8.5)
    ax.set_title("Perfil de veredictos", fontsize=11, color=DARK, pad=12,
                 loc="left", fontweight="bold")
    plt.tight_layout()
    p = os.path.join(out, "fig2_veredictos.png")
    plt.savefig(p, facecolor="white")
    plt.close()
    return p


def fig_tokens(recs, out, vered):
    pares = [(r.get("tokens_out"), r.get("secs"), r["id"]) for r in recs
             if r.get("tokens_out") and r.get("secs")]
    if len(pares) < 2:
        return None

    fig, ax = plt.subplots(figsize=(7.2, 3.0), dpi=200)
    for tok, sec, i in pares:
        c = RED if vered.get(i, "") in ("FALSO", "NO_ENTREGA") else ACC
        ax.scatter(tok, sec, s=70, color=c, edgecolor="white", linewidth=1.6, zorder=3)
        ax.annotate(ETIQUETAS.get(i, i).replace("\n", " "), (tok, sec),
                    textcoords="offset points", xytext=(7, 5), fontsize=7.5, color=GREY)
    ax.set_xlabel("tokens de salida", color=DARK)
    ax.set_ylabel("segundos", color=DARK)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=DARK, labelsize=8.5)
    ax.grid(color=LIGHT, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_title("¿La longitud explica el tiempo?", fontsize=11, color=DARK,
                 pad=12, loc="left", fontweight="bold")
    plt.tight_layout()
    p = os.path.join(out, "fig3_tokens.png")
    plt.savefig(p, facecolor="white")
    plt.close()
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mediciones", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--veredicto", default="")
    a = ap.parse_args()

    if not os.path.exists(a.mediciones):
        print(f"review-charts: no existe {a.mediciones}", file=sys.stderr)
        return 4
    os.makedirs(a.out, exist_ok=True)

    recs = cargar(a.mediciones)
    # Si el archivo es un JSON array (formato de recuperacion), aplanarlo.
    if len(recs) == 1 and isinstance(recs[0], list):
        recs = recs[0]
    if not recs:
        print("review-charts: no pude leer ninguna medicion", file=sys.stderr)
        return 4
    vered = veredictos(a.veredicto)

    hechas = []
    for fn in (fig_latencia, fig_veredictos, fig_tokens):
        try:
            p = fn(recs, a.out, vered) if fn is not fig_veredictos else fn(vered, a.out)
            if p:
                hechas.append(p)
        except Exception as e:  # una figura rota no debe tirar el resto
            print(f"review-charts: fallo {fn.__name__}: {e}", file=sys.stderr)

    for p in hechas:
        print(p)
    if not hechas:
        print("review-charts: sin datos suficientes para ninguna figura", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
