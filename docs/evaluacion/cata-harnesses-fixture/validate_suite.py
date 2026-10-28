#!/usr/bin/env python3
"""
Valida la suite OCULTA en las DOS direcciones.

Regla (harness-model-comparison): una suite que solo se probo en verde no se
probo. Contra una referencia correcta escrita a mano tiene que dar PASS, y
contra una version deliberadamente defectuosa tiene que dar FAIL.

Granularidad: una TAREA pasa si pasan TODOS sus asserts. La referencia tiene
que dar 3/3 tareas PASS y la version defectuosa 0/3.

TERCERA DIRECCION (2026-10-28): el entregable VACIO tiene que dar 0. Sin esto,
los asserts "not_contains" PASSAN por omision y una celda que no entrego nada
se llevaba 6/12 en T3 solo por callar. Medido: nemotron+openhands/T3 daba
6/12 sin informe, y minimax+openhands/T3 daba 6/12.

CUARTA DIRECCION (2026-10-28): el texto del CHAT no es el entregable. Cada
prompt dice "el informe es el unico entregable: escribilo en
`.context/informe.md`", asi que un modelo que responde en el chat sin escribir
ese archivo no entrego nada y tiene que valer 0.

Esta direccion existe porque el fallback a `output` en suite.py puntuaba el
chat cuando no habia archivo. Medido en la fase local: nova-2b daba 8/10
(claude) y 4/10 (opencode) con el fallback y 0/10 y 0/10 sin el, porque en los
dos casos escribio el informe en el chat y no en el archivo. El 0 de "no
escribio el entregable" se camuflaba de nota.

Ademas valida que suite.py NO tenga el fallback: si alguien lo reintroduce,
esta direccion falla.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from suite import eval_assert, eval_task  # noqa: E402

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

    # Tercera direccion: sin entregable, 0 puntos. Callar no es acertar.
    print("\n=== VACIO (debe dar 0/0 en las 3 tareas) ===")
    vacio_ok = True
    vacio = []
    for task in TASKS:
        ev = eval_task(task["id"], "")
        ok = ev.get("passed") == 0
        vacio_ok = vacio_ok and ok
        vacio.append({"task_id": task["id"], "passed": ev.get("passed"), "ok": ok})
        print(f"  {task['id']}: {ev.get('passed')}/{ev.get('total')} {'OK' if ok else 'FALLA'}")

    # Cuarta direccion: el texto del chat NO es el entregable.
    #
    # OJO: lo que se valida NO es que un cuerpo con los hechos correctos valga
    # 0 (si el archivo tuviera esos hechos, valeria 10/10: el juicio es sobre
    # el contenido, no sobre el canal). Lo que se valida es que suite.py
    # elija el ARCHIVO y no el chat: una celda que no escribio el archivo no
    # tiene cuerpo, y por lo tanto 0.
    #
    # Por eso la prueba es sobre la SELECCION del cuerpo, replicando la
    # linea exacta de suite.py con una fila que tiene chat y no archivo.
    print("\n=== CHAT SIN ARCHIVO (la celda no tiene cuerpo -> 0) ===")
    chat_ok = True
    chat = []
    for task in TASKS:
        # Una fila tipica: el agente respondio en el chat y no escribio
        # `.context/informe.md`.
        fila = {
            "task_id": task["id"],
            "deliverable": "",     # no hay archivo
            "output": "Aqui esta mi informe: muted sobre panel-2, ratio 4.10, "
                      "umbral 4.5, --muted es --k-text-secondary en dark.css.",
            "deliverable_chars": 0,
            "output_chars": 120,
        }
        # La MISMA seleccion que hace suite.py en main().
        body = fila.get("deliverable") or ""
        ev = eval_task(task["id"], body)
        ok = ev.get("passed") == 0
        chat_ok = chat_ok and ok
        chat.append({"task_id": task["id"], "passed": ev.get("passed"), "ok": ok})
        print(f"  {task['id']}: cuerpo de la celda={len(body)}ch -> {ev.get('passed')}/{ev.get('total')} {'OK' if ok else 'FALLA'}")

    # Y el fallback a `output` no puede volver: el cuerpo que se califica es
    # el del ARCHIVO, no el del chat.
    src = (HERE / "suite.py").read_text()
    fallback_presente = 'or r.get("output")' in src or "or r.get('output')" in src
    print(f"\n  fallback a `output` en suite.py: {'PRESENTE (FALLA)' if fallback_presente else 'ausente (OK)'}")
    fallback_ok = not fallback_presente

    ref_tasks = sum(1 for r in ref if r["all_pass"])
    bad_tasks = sum(1 for r in bad if r["all_pass"])
    n = len(TASKS)
    ok = ref_tasks == n and bad_tasks == 0 and vacio_ok and chat_ok and fallback_ok
    print(f"\nreferencia: {ref_tasks}/{n} tareas PASS")
    print(f"defectuosa: {bad_tasks}/{n} tareas PASS")
    print(f"vacio: {'todas dan 0' if vacio_ok else 'FALLA'}")
    print(f"chat sin archivo: {'todas dan 0' if chat_ok else 'FALLA'}")
    print(f"fallback a output: {'ausente' if fallback_ok else 'PRESENTE'}")
    print(
        "VALIDACION:",
        "OK - la suite discrimina en las cuatro direcciones" if ok else "FALLA",
    )
    (HERE / "suite-validation.json").write_text(
        json.dumps(
            {
                "reference": ref,
                "broken": bad,
                "vacio": vacio,
                "chat_sin_archivo": chat,
                "fallback_output_ausente": fallback_ok,
                "ok": ok,
            },
            indent=1,
            default=str,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
