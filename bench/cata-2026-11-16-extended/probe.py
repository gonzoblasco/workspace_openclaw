#!/usr/bin/env python3
"""Sonda de la perilla de razonamiento por candidato (SKILL.md step 3)."""
import json, sys, time, urllib.request

HOST = "http://localhost:11434"
MODELS = {
    "mimo-v2.6-flash:cloud": ["true", "false"],
    "mimo-v2.6-pro:cloud": ["true", "false"],
    "mistral-large-4:cloud": ["low", "true", "false"],
    "muse-spark-open:cloud": ["low", "false"],
    "nemotron-3-super:cloud": ["true", "false"],
}
PROMPT = "Un tren sale a las 14:05 y tarda 2h37m. ¿A qué hora llega? Respondé solo la hora."

def call(model, think, num_predict=1024, timeout=240):
    body = {"model": model, "messages": [{"role": "user", "content": PROMPT}],
            "stream": False, "think": think,
            "options": {"temperature": 0, "num_ctx": 8192, "num_predict": num_predict}}
    req = urllib.request.Request(f"{HOST}/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "elapsed_s": round(time.time()-t0, 1)}
    el = time.time() - t0
    if "error" in d:
        return {"error": d["error"], "elapsed_s": round(el, 1)}
    m = d.get("message", {}) or {}
    return {"model_echo": d.get("model"), "content": (m.get("content") or "")[:200],
            "thinking_chars": len(m.get("thinking") or ""), "done": d.get("done_reason"),
            "eval_count": d.get("eval_count"), "elapsed_s": round(el, 1)}

out = {}
for model, levels in MODELS.items():
    out[model] = {}
    for think in levels:
        r = call(model, think)
        out[model][think] = r
        print(f"{model:26s} think={think:6s} -> {json.dumps(r, ensure_ascii=False)[:220]}", flush=True)
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "probe.json", "w"), indent=1)
