#!/usr/bin/env python3
"""Cata 2026-11-04 - calidad x cuota sobre el catalogo Ollama Cloud.

Mide, para cada modelo, en UNA sola llamada:
  - recall de revisores sobre el artefacto con 4 bugs sembrados (ground truth)
  - tokens de salida reales (incluye thinking, que es lo que quema cuota)
  - latencia

Los modelos cloud no tienen filesystem ni shell: el prompt lleva los
archivos INLINE y se pide SOLO hallazgos (no edicion). Es el modo
correcto del agente B: reportar con evidencia, sin tocar produccion.

Uso:  python3 run_cata.py [--models a,b,c] [--dry]
"""
from __future__ import annotations
import json, sys, time, pathlib, urllib.request, argparse

BENCH = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(__file__).resolve().parent
HOST = "http://localhost:11434"

# Ground truth: 4 bugs sembrados (bench/GROUND_TRUTH.md)
# Cada uno se detecta por marcadores que solo aparecen si el modelo lo caza.
BUGS = {
    "BUG-1": {  # per_page <= 0 paso a < 0
        "desc": "per_page=0 ya no lanza ValueError (falta el <=)",
        "markers": [("per_page", "0"), ("<=", "valueerror")],
    },
    "BUG-2": {  # until inclusivo paso a exclusivo
        "desc": "filter_by_date dejo until EXCLUSIVO (< en vez de <=)",
        "markers": [("<=", "until"), ("exclusiv",), ("inclu", "until")],
    },
    "BUG-3": {  # edad invertida -> cache nunca expira
        "desc": "cached_reports: (cached_at - now) invierte la edad, cache no expira",
        "markers": [("cached_at",), ("negative", "negativ"), ("nunca", "expir")],
    },
    "BUG-4": {  # return data en vez de list(data)
        "desc": "cached_reports devuelve la lista interna (sin copia)",
        "markers": [("list(", "data"), ("copi", "copy"), ("intern",)],
    },
}

PROMPT = """Sos el Agente B (revisor) adversarial de un pipeline de desarrollo.
Otro agente (A) implemento una unidad a partir de un spec. Tu trabajo: encontrar los defectos REALES.

Un review hecho con el mismo modelo que escribio no sirve: sos ojos frescos.

## REGLAS
- Solo reportas, NO editas codigo y NO ejecutas comandos (no tenes shell).
- No comentes estilo, naming ni preferencias. Solo defectos de comportamiento.
- Un criterio ambiguo del spec NO es bug.
- Cada bug necesita: archivo, severidad y la linea exacta del codigo que lo causa.

## SPEC (task_spec.md)
---INICIO SPEC---
{spec}
---FIN SPEC---

## IMPLEMENTACION (reports.py)
---INICIO reports.py---
{impl}
---FIN reports.py---

## TESTS DE A (test_reports.py)
---INICIO test_reports.py---
{tests}
---FIN test_reports.py---

## FORMATO DE SALIDA (obligatorio)
Un unico bloque JSON, sin texto antes ni despues:
{{"bugs": [{{"titulo": "...", "archivo": "reports.py", "linea": "...", "severidad": "CRITICO|ALTO|MEDIO|BAJO", "explicacion": "..."}}],
 "tests_que_mienten": ["..."],
 "veredicto": "APROBADO|RECHAZADO"}}
"""


def call(model: str, prompt: str, timeout=300):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0, "num_predict": 8192},
    }).encode()
    req = urllib.request.Request(f"{HOST}/api/chat", data=body,
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
    return {
        "content": m.get("content", "") or "",
        "thinking": m.get("thinking", "") or "",
        "eval_count": d.get("eval_count", 0),
        "prompt_eval_count": d.get("prompt_eval_count", 0),
        "elapsed_s": round(el, 1),
    }


def score(content: str, thinking: str) -> dict:
    """Recall por marcadores sobre content + thinking (el pensamiento tambien es señal)."""
    text = (content + "\n" + thinking).lower()
    found = {}
    for bid, b in BUGS.items():
        hit = any(all(k.lower() in text for k in combo) for combo in b["markers"])
        found[bid] = hit
    return {"found": found, "recall": sum(found.values()), "total": len(BUGS)}


def usage_snapshot():
    """Conteo exacto por modelo (Legacy: solo request_count)."""
    try:
        with urllib.request.urlopen(f"{HOST}/api/usage?range=7d&group_by=model", timeout=15) as r:
            d = json.loads(r.read())
        return {g["model"]: g.get("request_count", 0)
                for g in d.get("totals", {}).get("groups", [])}
    except Exception as e:
        return {"_error": str(e)}


def usage_total():
    """Conteo exacto total (Legacy: solo request_count; los grupos se cortan en 10)."""
    try:
        with urllib.request.urlopen(f"{HOST}/api/usage?range=7d", timeout=15) as r:
            d = json.loads(r.read())
        return d.get("totals", {}).get("request_count")
    except Exception as e:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--out", default="results.json")
    args = ap.parse_args()

    work = OUT / "work"
    spec = (BENCH / "b-deepseek/task_spec.md").read_text()
    impl = (work / "reports.py").read_text()
    tests = (work / "test_reports.py").read_text()
    prompt = PROMPT.format(spec=spec, impl=impl, tests=tests)

    models = [m.strip() for m in args.models.split(",") if m.strip()] or [
        "mimo-v2.6-flash:cloud", "mimo-v2.6-pro:cloud", "mistral-large-4:cloud",
        "muse-spark-open:cloud", "kimi-k3.1-pro:cloud", "clef:cloud",
        "deepseek-v4.1-flash:cloud", "minimax-m3.1-flash:cloud", "gpt-oss:120b-cloud",
    ]
    if args.dry:
        print(f"prompt chars={len(prompt)}  models={models}")
        return

    before = usage_snapshot()
    total_before = usage_total()
    results = []
    outpath = OUT / args.out
    for i, m in enumerate(models, 1):
        print(f"[{i}/{len(models)}] {m} ...", flush=True)
        r = call(m, prompt)
        if "error" in r:
            rec = {"model": m, **r, "recall": None}
            print(f"    ERROR {r['error'][:90]} ({r['elapsed_s']}s)")
        elif not (r["content"] or "").strip():
            rec = {
                "model": m, "recall": None, "truncated": True,
                "eval_count": r["eval_count"], "thinking_chars": len(r["thinking"]),
                "elapsed_s": r["elapsed_s"], "thinking": r["thinking"][:4000],
            }
            print(f"    SIN ENTREGA: 0 content, {r['eval_count']} tok out, "
                  f"think={len(r['thinking'])}c, {r['elapsed_s']}s")
        else:
            s = score(r["content"], r["thinking"])
            rec = {
                "model": m, "recall": s["recall"], "found": s["found"],
                "eval_count": r["eval_count"], "prompt_eval_count": r["prompt_eval_count"],
                "thinking_chars": len(r["thinking"]), "content_chars": len(r["content"]),
                "elapsed_s": r["elapsed_s"],
                "content": r["content"][:4000], "thinking": r["thinking"][:4000],
            }
            print(f"    recall {s['recall']}/4  out_tok={r['eval_count']}  "
                  f"think={len(r['thinking'])}c  {r['elapsed_s']}s")
        results.append(rec)
        # guardado incremental: si algo falla, no perdemos la corrida
        outpath.write_text(json.dumps({"results": results}, ensure_ascii=False, indent=2))
        time.sleep(2)

    after = usage_snapshot()
    total_after = usage_total()
    print("\n=== DELTA DE REQUESTS (exacto, total de la cuenta) ===")
    if total_before is not None and total_after is not None:
        print(f"  requests de la cata (aprox): {total_after - total_before}")
    print("\n=== POR MODELO (top-10 del panel; los nuevos caen en remainder) ===")
    for m in models:
        base = m.split(":")[0]
        cands = [k for k in after if k.startswith(base)]
        d = sum(after.get(k, 0) - before.get(k, 0) for k in cands) if cands else "no visible"
        print(f"  {m:32} {d}")
    print(f"\nGuardado en {outpath}")


if __name__ == "__main__":
    main()
