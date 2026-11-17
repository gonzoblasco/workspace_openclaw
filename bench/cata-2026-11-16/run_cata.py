#!/usr/bin/env python3
"""Cata 2026-11-16 - cinco modelos cloud, dos tandas de razonamiento.

- Tanda `low`: el nivel mas bajo NO apagado que cada modelo acepta (SKILL.md step 3).
- Tanda `off`: razonamiento apagado, para clasificar modo (a)/(b)/(c).
- Misma via (/api/chat), mismo prompt verbatim + nonce compartido por celda,
  temperatura 0, num_ctx explicito, auto-escalado de num_predict.
- Suite oculta validada en las dos direcciones (evaluate.py --selftest).
"""
from __future__ import annotations
import json, sys, time, urllib.request, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "work"
RESULTS = HERE / "results.json"
HOST = "http://localhost:11434"
TIMEOUT = 300
BUDGETS = [4096, 8192, 16384, 24576]

MODELS = ["mimo-v2.6-flash:cloud", "mimo-v2.6-pro:cloud", "mistral-large-4:cloud",
          "muse-spark-open:cloud", "nemotron-3-super:cloud"]

# valor efectivo por modelo y tanda; None = el modelo no puede apagar el razonamiento
ARMS = {
    "low": {"mimo-v2.6-flash:cloud": True, "mimo-v2.6-pro:cloud": True,
            "mistral-large-4:cloud": "low", "muse-spark-open:cloud": "low",
            "nemotron-3-super:cloud": True},
    "off": {"mimo-v2.6-flash:cloud": False, "mimo-v2.6-pro:cloud": False,
            "mistral-large-4:cloud": None, "muse-spark-open:cloud": False,
            "nemotron-3-super:cloud": False},
}

sys.path.insert(0, str(HERE))
from evaluate import evaluate  # noqa: E402

TASKS = json.loads((HERE / "tasks.json").read_text())["tasks"]


def call(model, think, prompt, timeout=TIMEOUT):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "stream": False, "think": think,
            "options": {"temperature": 0, "num_ctx": 32768, "num_predict": BUDGETS[0]}}
    req = urllib.request.Request(f"{HOST}/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "elapsed_s": round(time.time() - t0, 1)}
    el = round(time.time() - t0, 1)
    if "error" in d:
        return {"error": d["error"], "elapsed_s": el}
    m = d.get("message", {}) or {}
    return {"content": m.get("content") or "", "thinking": m.get("thinking") or "",
            "done": d.get("done_reason"), "eval_count": d.get("eval_count", 0),
            "prompt_eval_count": d.get("prompt_eval_count", 0), "elapsed_s": el,
            "model_echo": d.get("model"), "budget": body["options"]["num_predict"]}


def call_escalating(model, think, prompt, cell_key):
    """Auto-escalado de num_predict cuando el content vuelve vacio con thinking."""
    attempts = []
    for i, budget in enumerate(BUDGETS):
        body_budget = budget
        nonce = f"{RUN_ID}-{cell_key}-a{i}"
        p = f"[cata-nonce {nonce}]\n{prompt}"
        r = _call_with_budget(model, think, p, body_budget)
        attempts.append({k: r.get(k) for k in ("done", "eval_count", "thinking", "elapsed_s", "error", "budget")})
        if r.get("error"):
            return r, attempts
        if (r["content"].strip() or not r["thinking"].strip()
                or r["eval_count"] < body_budget):
            r["attempts"] = attempts
            return r, attempts
        print(f"      (vacio con thinking, escalando de {body_budget})", flush=True)
    r["attempts"] = attempts
    return r, attempts


def _call_with_budget(model, think, prompt, budget):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "stream": False, "think": think,
            "options": {"temperature": 0, "num_ctx": 32768, "num_predict": budget}}
    req = urllib.request.Request(f"{HOST}/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            d = json.loads(r.read())
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "elapsed_s": round(time.time() - t0, 1)}
    el = round(time.time() - t0, 1)
    if "error" in d:
        return {"error": d["error"], "elapsed_s": el}
    m = d.get("message", {}) or {}
    return {"content": m.get("content") or "", "thinking": m.get("thinking") or "",
            "done": d.get("done_reason"), "eval_count": d.get("eval_count", 0),
            "prompt_eval_count": d.get("prompt_eval_count", 0), "elapsed_s": el,
            "model_echo": d.get("model"), "budget": budget}


def cleanliness(content: str, thinking: str) -> dict:
    import re
    fences = list(re.finditer(r"```", content))
    if len(fences) >= 2:
        pre = content[:fences[0].start()]
        post = content[fences[-1].end():]
    else:
        pre, post = content, ""
    leak_marks = re.findall(r"(?im)^\s*(primero|vamos a|analicemos|let me|i need to|step 1|razonamiento|pensemos)", content)
    return {"preamble_chars": len(pre.strip()), "trailing_chars": len(post.strip()),
            "thinking_chars": len(thinking), "leak_markers": len(leak_marks),
            "leak": len(leak_marks) > 0 and len(thinking.strip()) == 0}


def main():
    global RUN_ID
    RUN_ID = time.strftime("%Y%m%dT%H%M%S")
    OUT.mkdir(exist_ok=True)
    results = {"run_id": RUN_ID, "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "fixture_version": json.loads((HERE / "tasks.json").read_text())["version"],
               "cells": []}

    print("== warm-up (no se suma al throughput)", flush=True)
    for model in MODELS:
        r = call(model, ARMS["low"][model] if ARMS["low"][model] is not None else "low",
                 f"[warmup {uuid.uuid4().hex[:6]}] Decí OK.")
        print(f"  {model:26s} {r.get('elapsed_s')}s {r.get('content','')[:20]!r} err={r.get('error')}", flush=True)

    for task in TASKS:
        for arm in ("low", "off"):
            for model in MODELS:
                think = ARMS[arm][model]
                if think is None:
                    results["cells"].append({"task": task["id"], "arm": arm, "model": model,
                                             "error": "razonamiento no apagable: think:false ignorado"})
                    print(f"  {task['id']:16s} {arm:3s} {model:26s} NO MEDIDO (no apagable)", flush=True)
                    continue
                r, attempts = call_escalating(model, think, task["prompt"], f"{task['id']}-{arm}")
                if r.get("error"):
                    cell = {"task": task["id"], "arm": arm, "model": model,
                            "error": r["error"], "elapsed_s": r.get("elapsed_s")}
                    print(f"  {task['id']:16s} {arm:3s} {model:26s} ERROR {r['error']}", flush=True)
                else:
                    ev = evaluate(task["id"], r["content"])
                    clean = cleanliness(r["content"], r["thinking"])
                    cell = {"task": task["id"], "arm": arm, "model": model, "think": think,
                            "pass": ev["pass"], "asserts_failed": ev["asserts_failed"],
                            "eval_count": r["eval_count"], "prompt_eval_count": r["prompt_eval_count"],
                            "thinking_chars": len(r["thinking"]), "done": r["done"],
                            "elapsed_s": r["elapsed_s"], "budget": r["budget"],
                            "clean": clean, "attempts": attempts,
                            "content_len": len(r["content"]), "content": r["content"]}
                    d = OUT / f"{model.replace(':','_')}__{arm}__{task['id']}"
                    d.parent.mkdir(parents=True, exist_ok=True)
                    Path(str(d) + ".md").write_text(r["content"])
                    Path(str(d) + ".thinking.txt").write_text(r["thinking"])
                    print(f"  {task['id']:16s} {arm:3s} {model:26s} "
                          f"pass={ev['pass']!s:5s} eval={r['eval_count']:5d} "
                          f"think={len(r['thinking']):6d} t={r['elapsed_s']:6.1f}s "
                          f"pre={clean['preamble_chars']:5d} leak={clean['leak']}", flush=True)
                results["cells"].append(cell)
                RESULTS.write_text(json.dumps(results, indent=1, ensure_ascii=False))
    results["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    RESULTS.write_text(json.dumps(results, indent=1, ensure_ascii=False))
    print("LISTO", RESULTS)


if __name__ == "__main__":
    main()
