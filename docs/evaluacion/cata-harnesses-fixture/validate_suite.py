#!/usr/bin/env python3
"""
Valida la suite OCULTA en las DOS direcciones.

Regla (harness-model-comparison): una suite que solo se probo en verde no se
probo. Contra una referencia correcta escrita a mano tiene que dar PASS, y
contra una version deliberadamente defectuosa tiene que dar FAIL.

Granularidad: una TAREA pasa si pasan TODOS sus asserts. La referencia tiene
que dar 3/3 tareas PASS y la version defectuosa 0/3.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from suite import eval_assert  # noqa: E402

TASKS = json.loads((HERE / "tasks.json").read_text())


def run_suite(body: str, task: Dict[str, Any]) -> Dict[str, Any]:
    results = [eval_assert(a, body) for a in task["asserts"]]
    passed = sum(1 for r in results if r["ok"])
    return {
        "task_id": task["id"],
        "passed": passed,
        "total": len(results),
        "all_pass": passed == len(results) and len(results) > 0,
        "failed": [
            {"detail": r["detail"], "assert": r["assert"]} for r in results if not r["ok"]
        ],
    }


def evaluate(dirname: str) -> List[Dict[str, Any]]:
    out = []
    for task in TASKS:
        p = HERE / dirname / f"{task['id']}.md"
        if not p.exists():
            out.append({"task_id": task["id"], "all_pass": False, "error": "falta el archivo"})
            continue
        r = run_suite(p.read_text(), task)
        r["file"] = str(p)
        out.append(r)
    return out


def main() -> int:
    ref = evaluate("reference")
    bad = evaluate("broken")
    print("=== REFERENCIA (debe dar 3/3 PASS) ===")
    for r in ref:
        print(f"  {r['task_id']}: {r['passed']}/{r['total']} {'PASS' if r['all_pass'] else 'FAIL'}")
        for f in r.get("failed", []):
            print(f"      fallo: {f['detail']}  <- {f['assert']}")
    print("\n=== DEFECTUOSA (debe dar 0/3 PASS) ===")
    for r in bad:
        print(f"  {r['task_id']}: {r['passed']}/{r['total']} {'PASS' if r['all_pass'] else 'FAIL'}")
        for f in r.get("failed", []):
            print(f"      fallo: {f['detail']}  <- {f['assert']}")

    ref_tasks = sum(1 for r in ref if r["all_pass"])
    bad_tasks = sum(1 for r in bad if r["all_pass"])
    n = len(TASKS)
    ok = ref_tasks == n and bad_tasks == 0
    print(f"\nreferencia: {ref_tasks}/{n} tareas PASS")
    print(f"defectuosa: {bad_tasks}/{n} tareas PASS")
    print("VALIDACION:", "OK - la suite discrimina en las dos direcciones" if ok else "FALLA")
    (HERE / "suite-validation.json").write_text(
        json.dumps({"reference": ref, "broken": bad, "ok": ok}, indent=1, default=str)
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
