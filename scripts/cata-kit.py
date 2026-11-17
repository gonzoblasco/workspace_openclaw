#!/usr/bin/env python3
"""Kit de catas de modelos: init / check / run / analyze.

Replica la metodologia de `skills/model-comparison-cata` (nacida de la cata
2026-11-16). Cada cata vive en su propio directorio con:

  cata.json        modelos, valor de la perilla por tanda, limites
  tasks.json       enunciados verbatim + kind (code|analysis) + result_anchor
  evaluate.py      asserts ocultos + --selftest (dos direcciones)
  reference/       soluciones correctas (PASS)
  defective/       versiones con defecto (FAIL)
  work/            salidas crudas por celda
  results.json     resultado por celda

Uso:
  python3 scripts/cata-kit.py init bench/cata-2026-11-17 [--force]
  python3 scripts/cata-kit.py check bench/cata-2026-11-17
  python3 scripts/cata-kit.py run bench/cata-2026-11-17 [--dry] [--models a,b] [--arms low,off]
  python3 scripts/cata-kit.py analyze bench/cata-2026-11-17
"""
from __future__ import annotations
import argparse, importlib.util, json, re, shutil, subprocess, sys, time, urllib.request, urllib.error, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "skills" / "model-comparison-cata" / "templates"


# ------------------------------------------------------------------- helpers
def load_json(p: Path):
    return json.loads(p.read_text())


def fixture(d: str) -> Path:
    p = Path(d).expanduser().resolve()
    if not (p / "cata.json").exists():
        raise SystemExit(f"no es un directorio de cata (falta cata.json): {p}")
    return p


def load_evaluator(root: Path):
    spec = importlib.util.spec_from_file_location("cata_eval", str(root / "evaluate.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------- init
def cmd_init(args):
    dest = Path(args.dir).expanduser().resolve()
    if dest.exists() and any(dest.iterdir()) and not args.force:
        raise SystemExit(f"{dest} no esta vacio (usar --force para pisar plantillas)")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "reference").mkdir(exist_ok=True)
    (dest / "defective").mkdir(exist_ok=True)
    shutil.copyfile(TEMPLATES / "cata.json", dest / "cata.json")
    shutil.copyfile(TEMPLATES / "tasks.example.json", dest / "tasks.json")
    shutil.copyfile(TEMPLATES / "evaluate.example.py", dest / "evaluate.py")
    for sub in ("reference", "defective"):
        for f in (TEMPLATES / sub).iterdir():
            shutil.copyfile(f, dest / sub / f.name)
    for tpl in ("REPORT.template.md", "blind-eval-brief.md"):
        shutil.copyfile(TEMPLATES / tpl, dest / tpl)
    print(f"cata creada en {dest}")
    print("siguiente: editá cata.json (modelos y perilla) y tasks.json (enunciados),")
    print("           reemplazá los asserts de evaluate.py, y corré `check`.")


# --------------------------------------------------------------------- check
def cmd_check(args):
    root = fixture(args.dir)
    r = subprocess.run([sys.executable, str(root / "evaluate.py"), "--selftest"],
                       capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    if r.returncode != 0:
        raise SystemExit("SELFTEST FALLA: la suite no vale hasta que referencia=PASS y defectuosa=FAIL")


# ----------------------------------------------------------------------- run
def call(root: Path, cfg: dict, model: str, think, prompt: str, budget: int):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "stream": False, "think": think,
            "options": {"temperature": 0, "num_ctx": cfg.get("num_ctx", 32768),
                        "num_predict": budget}}
    url = cfg.get("route", "http://localhost:11434") + cfg.get("endpoint", "/api/chat")
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=cfg.get("timeout_s", 300)) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read()[:160].decode(errors='replace')}",
                "elapsed_s": round(time.time() - t0, 1)}
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


def call_escalating(root, cfg, model, think, prompt, cell_key, run_id):
    """Auto-escalado de num_predict cuando el content vuelve vacio con thinking."""
    attempts = []
    budgets = cfg.get("budgets", [4096, 8192, 16384, 24576])
    r = {}
    for i, budget in enumerate(budgets):
        # nonce compartido por celda: identico entre candidatos, distinto entre
        # intentos y tandas. Sin el, el daemon devuelve la respuesta cacheada y
        # la perilla parece no viajar (verified 2026-11-16).
        p = f"[cata-nonce {run_id}-{cell_key}-a{i}]\n{prompt}"
        r = call(root, cfg, model, think, p, budget)
        attempts.append({k: r.get(k) for k in
                         ("done", "eval_count", "thinking", "elapsed_s", "error", "budget")})
        if r.get("error"):
            return r, attempts
        if (r["content"].strip() or not r["thinking"].strip()
                or r["eval_count"] < budget):
            return r, attempts
        print(f"      (vacio con thinking, escalando de {budget})", flush=True)
    return r, attempts


def cmd_run(args):
    root = fixture(args.dir)
    cfg = load_json(root / "cata.json")
    tasks = load_json(root / "tasks.json")["tasks"]
    ev = load_evaluator(root)

    models = cfg["models"]
    if args.models:
        want = [m.strip() for m in args.models.split(",") if m.strip()]
        models = {k: v for k, v in models.items() if k in want}
        if not models:
            raise SystemExit("ningun modelo de --models esta en cata.json")
    arms = [a.strip() for a in (args.arms.split(",") if args.arms else cfg.get("arms", ["low"]))]

    cells = [(t, a, m) for t in tasks for a in arms for m in models]
    if args.dry:
        for t, a, m in cells:
            print(f"{t['id']:20s} {a:4s} {m:28s} think={models[m].get(a)!r}")
        print(f"{len(cells)} celdas")
        return

    run_id = time.strftime("%Y%m%dT%H%M%S")
    out = root / "work"
    out.mkdir(exist_ok=True)
    results = {"run_id": run_id, "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "fixture_version": load_json(root / "tasks.json").get("version"),
               "arms": arms, "cells": []}
    results_path = root / "results.json"

    print("== warm-up (no se suma al throughput)", flush=True)
    for m, per_arm in models.items():
        vals = [v for v in per_arm.values() if v is not None]
        r = call(root, cfg, m, vals[0] if vals else False,
                 f"[warmup {uuid.uuid4().hex[:6]}] Decí OK.", 64)
        print(f"  {m:28s} {r.get('elapsed_s')}s err={r.get('error')}", flush=True)

    for task, arm, model in cells:
        think = models[model].get(arm)
        if think is None:
            results["cells"].append({"task": task["id"], "arm": arm, "model": model,
                                     "error": "no medido: el modelo no permite apagar el razonamiento"})
            print(f"  {task['id']:20s} {arm:4s} {model:28s} NO MEDIDO", flush=True)
            continue
        r, attempts = call_escalating(root, cfg, model, think, task["prompt"],
                                      f"{task['id']}-{arm}", run_id)
        if r.get("error"):
            cell = {"task": task["id"], "arm": arm, "model": model, "think": think,
                    "error": r["error"], "elapsed_s": r.get("elapsed_s")}
            print(f"  {task['id']:20s} {arm:4s} {model:28s} ERROR {r['error'][:70]}", flush=True)
        else:
            res = ev.evaluate(task["id"], r["content"])
            cell = {"task": task["id"], "arm": arm, "model": model, "think": think,
                    "pass": res["pass"], "asserts_failed": res["asserts_failed"],
                    "eval_count": r["eval_count"], "prompt_eval_count": r["prompt_eval_count"],
                    "thinking_chars": len(r["thinking"]), "done": r["done"],
                    "elapsed_s": r["elapsed_s"], "budget": r["budget"],
                    "attempts": attempts, "content": r["content"]}
            base = out / f"{model.replace(':', '_')}__{arm}__{task['id']}"
            Path(str(base) + ".md").write_text(r["content"])
            Path(str(base) + ".thinking.txt").write_text(r["thinking"])
            print(f"  {task['id']:20s} {arm:4s} {model:28s} "
                  f"pass={res['pass']!s:5s} eval={r['eval_count']:5d} "
                  f"think={len(r['thinking']):6d} t={r['elapsed_s']:6.1f}s", flush=True)
        results["cells"].append(cell)
        results_path.write_text(json.dumps(results, indent=1, ensure_ascii=False))
    results["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    results_path.write_text(json.dumps(results, indent=1, ensure_ascii=False))
    print("LISTO", results_path)


# ------------------------------------------------------------------- analyze
CODE_LINE = re.compile(
    r"^\s*(import |from |def |class |return |if |elif |else\b|for |while |try\b|"
    r"except\b|with |raise |async def |@|#|\)|\]|\}|\"\"\"|'''|[A-Za-z_][\w\.\[\], ]*=)")


def cleanliness(content: str, task: dict) -> dict:
    if task.get("kind") == "analysis":
        anchor = task.get("result_anchor")
        if anchor:
            i = content.find(anchor)
            pre = content[:i] if i > 0 else (content if i < 0 else "")
        else:
            pre = content
        return {"prose_chars": len(pre.strip()), "has_fence": "```" in content}
    if "```" in content:
        outside = re.sub(r"```.*?```", "", content, flags=re.S)
        prose = len(" ".join(l.strip() for l in outside.splitlines() if l.strip()))
        return {"prose_chars": prose, "has_fence": True}
    noncode = [l for l in content.splitlines()
               if l.strip() and not CODE_LINE.match(l) and not l.strip().startswith(('"""', "'''"))]
    return {"prose_chars": len("\n".join(noncode)), "has_fence": False}


def cmd_analyze(args):
    root = fixture(args.dir)
    d = load_json(root / "results.json")
    tasks = {t["id"]: t for t in load_json(root / "tasks.json")["tasks"]}
    models = list(load_json(root / "cata.json")["models"].keys())

    rows = []
    for c in d["cells"]:
        if "error" in c:
            rows.append(c)
            continue
        cl = cleanliness(c.get("content", ""), tasks.get(c["task"], {}))
        c["clean"] = cl
        c["mode"] = ("razona en el output" if (c["arm"] == "off" and c["thinking_chars"] == 0
                                               and cl["prose_chars"] > 80)
                     else "entrega directa" if cl["prose_chars"] <= 80
                     else "prosa fuera del entregable")
        rows.append(c)

    print(f"| tanda | modelo | pass | eval prom. | thinking prom. | t prom. (s) | prosa prom. | modo |")
    print("|---|---|---|---|---|---|---|---|")
    for arm in d.get("arms", ["low", "off"]):
        for m in models:
            cs = [r for r in rows if r["arm"] == arm and r["model"] == m]
            if not cs:
                continue
            if "error" in cs[0]:
                print(f"| {arm} | {m} | NO MEDIDO | — | — | — | — | {cs[0]['error'][:40]} |")
                continue
            p = sum(1 for r in cs if r["pass"])
            n = len(cs)
            ev = sum(r["eval_count"] for r in cs) / n
            th = sum(r["thinking_chars"] for r in cs) / n
            tt = sum(r["elapsed_s"] for r in cs) / n
            pr = sum(r["clean"]["prose_chars"] for r in cs) / n
            modes = ", ".join(sorted({r["mode"] for r in cs}))
            print(f"| {arm} | {m} | {p}/{n} | {ev:.0f} | {th:.0f} | {tt:.1f} | {pr:.0f} | {modes} |")

    print("\nCeldas con CONTENT < 1.0:")
    for r in rows:
        if "error" not in r and not r["pass"]:
            print(f"- {r['task']} / {r['arm']} / {r['model']}: {r['asserts_failed']}")

    json.dump({"cells": rows}, open(root / "results_analyzed.json", "w"),
              indent=1, ensure_ascii=False)
    print(f"\n-> {root / 'results_analyzed.json'}")


def main():
    ap = argparse.ArgumentParser(description="Kit de catas de modelos")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init", help="crear un directorio de cata desde las plantillas")
    p.add_argument("dir")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)
    p = sub.add_parser("check", help="validar la suite en las dos direcciones")
    p.add_argument("dir")
    p.set_defaults(func=cmd_check)
    p = sub.add_parser("run", help="correr la cata")
    p.add_argument("dir")
    p.add_argument("--dry", action="store_true")
    p.add_argument("--models")
    p.add_argument("--arms")
    p.set_defaults(func=cmd_run)
    p = sub.add_parser("analyze", help="agregar resultados y clasificar modo de salida")
    p.add_argument("dir")
    p.set_defaults(func=cmd_analyze)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
