#!/usr/bin/env python3
"""
Analisis comparativo de las 3 catas (3 modelos x 3 harnesses x 3 tareas).

Cruza: suite oculta (verdad de base), juez ciego, y costo. La lectura clave es
el CRUCE modelo x harness: si el ranking de harnesses cambia con el modelo, el
ranking era del modelo y no del harness.
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List

ROOT = pathlib.Path("/tmp/cata-harnesses")
MODELS = [
    ("deepseek-v4.1-flash__cloud", "deepseek-v4.1-flash:cloud"),
    ("gpt-oss_120b-cloud", "gpt-oss:120b-cloud"),
    ("nemotron-3-super_cloud", "nemotron-3-super:cloud"),
    ("minimax-m3.1-flash_cloud", "minimax-m3.1-flash:cloud"),
    ("gemma4_cloud", "gemma4:cloud"),
    ("glm-5.3-flash_cloud", "glm-5.3-flash:cloud"),
]
# Los 4 locales (fase local): 1 TAREA (T1) cada uno, no 3. El slug es el
# nombre del directorio (tr ':/' -> '__'), que es como el driver los nombra.
LOCALES = [
    ("hf.co_ModernoTech_nova-2b_latest", "nova-2b:latest"),
    ("ornith-1.5_9b", "ornith-1.5:9b"),
    ("gemma4_12b-mlx", "gemma4:12b-mlx"),
    ("qwen3.5_9b-mlx", "qwen3.5:9b-mlx"),
]
HARNESSES = ["claude", "opencode", "openhands"]

# Todos los modelos de la matriz, con las tareas que se midieron en cada uno.
# Los cloud: 3 tareas. Los locales: 1 (T1). Es el unico lugar donde se
# declara eso, para que la tabla no sume tareas que nadie corrio.
TODOS = (
    [(s, m, ("T1", "T2", "T3")) for s, m in MODELS]
    + [(s, m, ("T1",)) for s, m in LOCALES]
)


def load(slug: str, name: str) -> Any:
    p = ROOT / slug / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def tokens_of(raw: Dict[str, Any], harness: str) -> tuple[int, int, int, int]:
    """(tokens in, tokens out, turnos, tool calls)"""
    tin = tout = turns = tools = 0
    if harness == "openhands":
        m = ((raw.get("stats") or {}).get("usage_to_metrics") or {}).get("default", {})
        t = m.get("accumulated_token_usage", {}) or {}
        tin = t.get("prompt_tokens", 0) or 0
        tout = t.get("completion_tokens", 0) or 0
        turns = len(m.get("response_latencies", []) or [])
        tools = len(raw.get("actions", []) or [])
    elif harness == "opencode":
        for e in raw.get("events", []) or []:
            if e.get("type") == "step_finish":
                tk = e.get("part", {}).get("tokens", {}) or {}
                tin += tk.get("input", 0) or 0
                tout += tk.get("output", 0) or 0
                turns += 1
        tools = turns
    else:
        j = raw.get("json") or {}
        u = j.get("usage", {}) or {}
        tin = u.get("input_tokens", 0) or 0
        tout = u.get("output_tokens", 0) or 0
        turns = 1
        tools = len(j.get("iterations", []) or [])
    return tin, tout, turns, tools


def main() -> int:
    rows: List[Dict[str, Any]] = []
    for slug, model, tareas in TODOS:
        results = load(slug, "results.json")
        suite = load(slug, "suite.json")
        judge = load(slug, "judge.json")
        if not results:
            print(f"  (sin resultados: {model})")
            continue
        suite_map = {(s["task_id"], s["harness"]): s for s in (suite or [])}
        judge_map = {(j["task_id"], j["harness"]): j for j in (judge or [])}
        for r in results:
            if r.get("task_id") not in tareas:
                continue
            key = (r["task_id"], r["harness"])
            s = suite_map.get(key, {})
            j = judge_map.get(key, {})
            raw = load(slug, f"raw/{r['task_id']}-{r['harness']}.json") or {}
            tin, tout, turns, tools = tokens_of(raw, r["harness"])
            rows.append(
                {
                    "model": model,
                    "harness": r["harness"],
                    "task_id": r["task_id"],
                    "passed": s.get("asserts_passed"),
                    "total": s.get("asserts_total"),
                    "all_pass": s.get("all_pass"),
                    "content": j.get("content"),
                    "cleanliness": j.get("cleanliness"),
                    "seconds": r.get("seconds"),
                    "deliverable": r.get("deliverable_chars"),
                    "tin": tin,
                    "tout": tout,
                    "turns": turns,
                    "tools": tools,
                    "control_ok": r.get("control_ok"),
                }
            )

    print("=" * 96)
    print("SUITE OCULTA (verdad de base): asserts pasados por modelo x harness")
    print("=" * 96)
    print(f"{'MODELO':<28} " + " ".join(f"{h:<12}" for h in HARNESSES) + "  TOTAL")
    for slug, model, _t in TODOS:
        cells = []
        tp = tt = 0
        for h in HARNESSES:
            rs = [r for r in rows if r["model"] == model and r["harness"] == h]
            p = sum(r["passed"] or 0 for r in rs)
            t = sum(r["total"] or 0 for r in rs)
            tp += p
            tt += t
            cells.append(f"{p}/{t}")
        if tt:
            print(f"{model:<28} " + " ".join(f"{c:<12}" for c in cells) + f"  {tp}/{tt}")
        else:
            print(f"{model:<28} (sin datos)")

    print()
    print("=" * 96)
    print("POR TAREA (modelo x harness)")
    print("=" * 96)
    for t in ["T1", "T2", "T3"]:
        print(f"-- {t} --")
        for slug, model, tareas in TODOS:
            if t not in tareas:
                continue
            cells = []
            for h in HARNESSES:
                r = next(
                    (x for x in rows if x["model"] == model and x["harness"] == h and x["task_id"] == t),
                    None,
                )
                cells.append(f"{h}={r['passed']}/{r['total']}" if r else f"{h}=-")
            print(f"   {model:<28} " + "  ".join(cells))

    print()
    print("=" * 96)
    print("COSTO (totales de las tareas del modelo)")
    print("=" * 96)
    print(f"{'MODELO':<28} {'HARNESS':<11} {'seg':>6} {'tok in':>10} {'tok out':>9} {'turnos':>7} {'tools':>6} {'entregable':>11}")
    for slug, model, _t in TODOS:
        for h in HARNESSES:
            rs = [r for r in rows if r["model"] == model and r["harness"] == h]
            if not rs:
                continue
            print(
                f"{model:<28} {h:<11} {sum(r['seconds'] or 0 for r in rs):>6.0f} "
                f"{sum(r['tin'] or 0 for r in rs):>10} {sum(r['tout'] or 0 for r in rs):>9} "
                f"{sum(r['turns'] or 0 for r in rs):>7} {sum(r['tools'] or 0 for r in rs):>6} "
                f"{sum(r['deliverable'] or 0 for r in rs):>10}ch"
            )
        print()

    print("=" * 96)
    print("JUEZ CIEGO (content / cleanliness)")
    print("=" * 96)
    print(f"{'MODELO':<28} " + " ".join(f"{h:<20}" for h in HARNESSES))
    for slug, model, _t in TODOS:
        cells = []
        for h in HARNESSES:
            rs = [r for r in rows if r["model"] == model and r["harness"] == h and r["content"] is not None]
            if rs:
                c = sum(r["content"] for r in rs) / len(rs)
                cl = sum(r["cleanliness"] for r in rs) / len(rs)
                cells.append(f"{c:.2f} / {cl:.2f}")
            else:
                cells.append("-")
        print(f"{model:<28} " + " ".join(f"{c:<20}" for c in cells))

    (ROOT / "comparativo.json").write_text(json.dumps(rows, indent=1, default=str))
    print(f"\n{dataclass_to_json_safe(rows)}")
    return 0


def dataclass_to_json_safe(rows: List[Dict[str, Any]]) -> str:
    return f"detalle en {ROOT / 'comparativo.json'} ({len(rows)} filas)"


if __name__ == "__main__":
    raise SystemExit(main())
