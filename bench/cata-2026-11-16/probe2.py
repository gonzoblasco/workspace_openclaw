#!/usr/bin/env python3
"""Sonda 2: nonce anti-cache, y mapeo fino de la perilla."""
import json, sys, time, urllib.request, uuid

HOST = "http://localhost:11434"
CASES = [
    ("mimo-v2.6-flash:cloud", ["true", "false"]),
    ("mimo-v2.6-pro:cloud", ["true", "false"]),
    ("mistral-large-4:cloud", ["low", "false", "none", "medium"]),
    ("muse-spark-open:cloud", ["low", "false", "medium", "none"]),
    ("nemotron-3-super:cloud", ["true", "false"]),
]

def call(model, think, timeout=240, num_predict=1024):
    nonce = uuid.uuid4().hex[:8]
    prompt = f"[nonce {nonce}] Un tren sale a las 14:05 y tarda 2h37m. ¿A qué hora llega? Respondé solo la hora."
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "stream": False, "options": {"temperature": 0, "num_ctx": 8192, "num_predict": num_predict}}
    if think != "none":
        body["think"] = think if think != "false" else False
    req = urllib.request.Request(f"{HOST}/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read()[:120].decode(errors='replace')}", "elapsed_s": round(time.time()-t0, 1)}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "elapsed_s": round(time.time()-t0, 1)}
    el = time.time() - t0
    if "error" in d:
        return {"error": d["error"], "elapsed_s": round(el, 1)}
    m = d.get("message", {}) or {}
    return {"content": (m.get("content") or "")[:80], "thinking_chars": len(m.get("thinking") or ""),
            "done": d.get("done_reason"), "prompt_eval": d.get("prompt_eval_count"),
            "eval_count": d.get("eval_count"), "elapsed_s": round(el, 1)}

out = {}
for model, levels in CASES:
    out[model] = {}
    for think in levels:
        r = call(model, think)
        out[model][think] = r
        print(f"{model:26s} think={think:7s} -> {json.dumps(r, ensure_ascii=False)[:180]}", flush=True)
json.dump(out, open("probe2.json", "w"), indent=1)
