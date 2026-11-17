#!/usr/bin/env python3
"""Analisis post-hoc de la cata 2026-11-16: agrega y clasifica modo de salida."""
from __future__ import annotations
import json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
d = json.load(open(HERE / "results.json"))

CODE_LINE = re.compile(r"^\s*(import |from |def |class |return |if |elif |else\b|for |while |try\b|except\b|with |raise |async def |@|#|\)|\]|\}|\"\"\"|'''|[A-Za-z_][\w\.\[\], ]*=)")

def classify(content: str, task: str) -> dict:
    if "```" in content:
        blocks = re.findall(r"```(?:python|py)?[^\n]*\n(.*?)```", content, re.S)
        outside = re.sub(r"```.*?```", "", content, flags=re.S)
        has_fence = True
        code = max(blocks, key=len) if blocks else ""
    else:
        has_fence = False
        outside = ""
        code = content
    prose = []
    for line in outside.splitlines():
        if not line.strip():
            continue
        prose.append(line)
    prose_chars = len(" ".join(prose).strip())
    # para code tasks sin fences: lineas que no parecen codigo
    if task.startswith("T") and (task[1] in "12") and not has_fence:
        noncode = [l for l in content.splitlines()
                   if l.strip() and not CODE_LINE.match(l) and not l.strip().startswith(('"""', "'''"))]
        prose_chars = len("\n".join(noncode))
    if task.startswith("T3"):
        i = content.find("TOTAL:")
        prose_chars = len(content[:i].strip()) if i > 0 else (len(content) if i < 0 else 0)
    return {"has_fence": has_fence, "prose_chars": prose_chars,
            "content_chars": len(content)}

rows = []
for c in d["cells"]:
    if "error" in c:
        rows.append(c); continue
    content = c.get("content") or ""
    cl = classify(content, c["task"])
    c["out"] = cl
    c["mode"] = ("sin thinking, razona en el output" if (c["arm"] == "off" and c["thinking_chars"] == 0 and cl["prose_chars"] > 80)
                 else "entrega directa" if cl["prose_chars"] <= 80 else "prosa fuera del entregable")
    rows.append(c)

print(f"{'arm':4s} {'modelo':24s} {'pass':>6s} {'eval':>6s} {'think':>6s} {'t(s)':>6s} {'prosa':>6s}  modo")
for arm in ("low", "off"):
    for model in ["mimo-v2.6-flash:cloud", "mimo-v2.6-pro:cloud", "mistral-large-4:cloud",
                  "muse-spark-open:cloud", "nemotron-3-super:cloud"]:
        cells = [r for r in rows if r["arm"] == arm and r["model"] == model]
        if not cells:
            continue
        if "error" in cells[0]:
            print(f"{arm:4s} {model:24s} {'NO MEDIDO':>6s}  {cells[0]['error']}")
            continue
        p = sum(1 for r in cells if r["pass"])
        ev = sum(r["eval_count"] for r in cells) / len(cells)
        th = sum(r["thinking_chars"] for r in cells) / len(cells)
        t = sum(r["elapsed_s"] for r in cells) / len(cells)
        pr = sum(r["out"]["prose_chars"] for r in cells) / len(cells)
        modes = sorted({r["mode"] for r in cells})
        print(f"{arm:4s} {model:24s} {p}/{len(cells):<4d} {ev:6.0f} {th:6.0f} {t:6.1f} {pr:6.0f}  {', '.join(modes)}")
    print()

json.dump({"cells": rows}, open(HERE / "results_analyzed.json", "w"), indent=1, ensure_ascii=False)
