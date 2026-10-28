#!/usr/bin/env python3
"""
Suite oculta: el veredicto REAL de la cata.

Cada tarea tiene una lista de asserts. Un assert es un hecho verificable que
debe estar en el entregable del agente. Los asserts NO van en el prompt.

Dos reglas de la disciplina (harness-model-comparison):
  - La suite se valida en las DOS direcciones antes de medir: contra una
    referencia correcta (100% PASS) y contra una version deliberadamente
    defectuosa (100% FAIL). Una suite que solo se probo en verde no se probo.
  - Un aserto no puede depender de un detalle que el prompt NO fija.

Cada assert es de tipo:
  contains:   el entregable debe contener la cadena (case-insensitive)
  regex:      el entregable debe matchear el patron
  not_contains: el entregable NO debe contener la cadena (para castigar
               afirmaciones falsas: p.ej. decir que un ADR esta roto cuando no)
  number_lt / number_gt: el entregable debe contener un numero que cumpla la
               relacion (para ratios, conteos, exit codes)
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

MODEL = os.environ.get("CATA_MODEL", "deepseek-v4.1-flash:cloud")
_SLUG = MODEL.replace(":", "__").replace("/", "__")
OUT = Path(os.environ.get("CATA_OUT", f"/tmp/cata-harnesses/{_SLUG}"))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).lower()


def eval_assert(a: Dict[str, Any], body: str) -> Dict[str, Any]:
    n = normalize(body)
    kind = a["kind"]
    ok = False
    detail = ""
    if kind == "contains":
        needle = a["value"].lower()
        ok = needle in n
        detail = f"contains {a['value']!r}"
    elif kind == "not_contains":
        needle = a["value"].lower()
        ok = needle not in n
        detail = f"not_contains {a['value']!r}"
    elif kind == "regex":
        ok = re.search(a["value"], body, flags=re.I | re.M) is not None
        detail = f"regex {a['value']!r}"
    elif kind == "number_lt":
        nums = [float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", body)]
        target = float(a["value"])
        hits = [x for x in nums if x < target]
        ok = bool(hits)
        detail = f"number < {target} (encontrados: {hits[:6]})"
    elif kind == "number_gt":
        nums = [float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", body)]
        target = float(a["value"])
        hits = [x for x in nums if x > target]
        ok = bool(hits)
        detail = f"number > {target} (encontrados: {hits[:6]})"
    else:
        ok = False
        detail = f"tipo de assert desconocido: {kind}"
    return {"assert": a, "ok": ok, "detail": detail}


def eval_task(task_id: str, body: str) -> Dict[str, Any]:
    tasks = json.loads((OUT / "tasks.json").read_text())
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return {"error": f"tarea desconocida: {task_id}"}
    # Sin entregable no hay nada que puntuar.
    #
    # POR QUE: los asserts "not_contains" PASSAN por omision (no affirmar
    # "hay un ADR roto" es cierto de un informe vacio). Una celda que no
    # entrego nada se llevaba 6/12 en T3 solo por callar. Medido:
    # nemotron+openhands/T3 (sin informe) daba 6/12 y minimax+openhands/T3
    # daba 6/12. Callar no es acertar: un entregable vacio vale 0.
    if not (body or "").strip():
        results = [
            {"assert": a, "ok": False, "detail": "sin entregable"}
            for a in task.get("asserts", [])
        ]
        return {
            "task_id": task_id,
            "passed": 0,
            "total": len(results),
            "all_pass": False,
            "results": results,
        }
    results = [eval_assert(a, body) for a in task.get("asserts", [])]
    passed = sum(1 for r in results if r["ok"])
    return {
        "task_id": task_id,
        "passed": passed,
        "total": len(results),
        "all_pass": passed == len(results) and len(results) > 0,
        "results": results,
    }


def main() -> int:
    results = json.loads((OUT / "results.json").read_text())
    table: List[Dict[str, Any]] = []
    for r in results:
        # SOLO el archivo. El prompt de cada tarea dice explicitamente "el
        # informe es el unico entregable: escribilo en `.context/informe.md`",
        # asi que un modelo que responde en el chat SIN escribir ese archivo
        # NO entrego nada: tiene que valer 0.
        #
        # POR QUE se saco el fallback a `output` (el texto del chat): con el,
        # una celda que no escribio el archivo se puntuaba igual. Medido en
        # la fase local: nova-2b daba 8/10 (claude) y 4/10 (opencode) con el
        # fallback y 0/10 y 0/10 sin el, porque en los dos casos el modelo
        # escribio el informe en el chat y no en el archivo. El 0 de "no
        # escribio el entregable" se estaba camuflando de nota.
        #
        # El unico caso donde el chat cuenta es el INPUT de la tarea, y ese
        # ya se repara aparte (deliverable_fuente=corpus_input).
        body = r.get("deliverable") or ""
        ev = eval_task(r["task_id"], body)
        table.append(
            {
                "task_id": r["task_id"],
                "harness": r["harness"],
                "control_ok": r.get("control_ok"),
                "model_used": r.get("model_used"),
                "seconds": r.get("seconds"),
                "asserts_passed": ev.get("passed"),
                "asserts_total": ev.get("total"),
                "all_pass": ev.get("all_pass"),
                "failed": [
                    {"detail": x["detail"], "assert": x["assert"]}
                    for x in ev.get("results", [])
                    if not x["ok"]
                ],
            }
        )
    (OUT / "suite.json").write_text(json.dumps(table, indent=1, default=str))
    # Resumen legible.
    print(f"{'TAREA':<14} {'HARNESS':<11} {'PASES':<8} {'CTRL':<6} {'s':<6}")
    for t in table:
        print(
            f"{t['task_id']:<14} {t['harness']:<11} "
            f"{str(t['asserts_passed'])+'/'+str(t['asserts_total']):<8} "
            f"{str(t['control_ok']):<6} {t['seconds']:<6}"
        )
    print(f"\ndetalle en {OUT / 'suite.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
