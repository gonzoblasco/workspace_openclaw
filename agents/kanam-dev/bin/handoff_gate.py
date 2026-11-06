#!/usr/bin/env python3
"""
handoff_gate.py - Estacion S7: no se cierra un trabajo sin contrato completo.

El problema que resuelve: un handoff que dice "todo verde" sin la salida del
comando, o que omite una estacion salteada. Lo que no esta escrito no existe, y
un campo vacio no es un campo.

Contrato (PIPELINE-CONTRACTS.md seccion 2, S7):
    summary            una frase de que se hizo
    status             uno de: completo | parcial | bloqueado
    artifact           ruta exacta del artefacto
    verified[]         cada item: {command, exit, output}
    inferred[]         lo que NO se verifico y por que
    openDecisions[]    decisiones que esperan a un humano
    skipped[]          estaciones salteadas por plantilla, con motivo

Reglas que hacen que el gate sirva:
  1. `verified` exige el exit code Y la salida. "Corri los tests" no es evidencia.
  2. Un item de `verified` con exit != 0 es una contradiccion: si fallo, no
     verifica. Se rechaza.
  3. `skipped` exige motivo. Una estacion salteada sin motivo es un olvido
     disfrazado.
  4. `status: completo` con `openDecisions` no vacio es contradictorio: si hay
     una decision abierta, no esta completo.

Exit codes:
  0  handoff valido
  1  handoff invalido (lista cada campo que falta o se contradice)
  2  no se pudo leer el archivo

Cero dependencias. Solo stdlib.

Uso:
    handoff_gate.py handoff.json
    handoff_gate.py handoff.json --json
    handoff_gate.py --template            # imprime un esqueleto
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ("summary", "status", "artifact", "verified", "inferred", "openDecisions", "skipped")
STATUSES = ("completo", "parcial", "bloqueado")

# Estaciones conocidas: un `skipped` que nombra otra cosa es ruido, no registro.
STATIONS = ("intake", "discovery", "slice", "build", "verify", "review", "handoff")

# El esqueleto tiene valores que el gate acepta: un template que el propio gate
# rechaza es una trampa. Los campos que exigen contenido real llevan un
# placeholder explicito, no un string vacio.
SKELETON = {
    "summary": "QUE SE HIZO (una frase)",
    "status": "parcial",
    "artifact": "ruta/exacta/del/artefacto",
    "verified": [
        {"command": "npm test", "exit": 0, "output": "168 pass / 0 fail"}
    ],
    "inferred": [
        "lo que no se midio y por que"
    ],
    "openDecisions": [],
    "skipped": [
        {"station": "review", "reason": "hotfix de una linea con criterio explicito en el pedido"}
    ],
}


def validate(data: object) -> list[str]:
    """Devuelve la lista de problemas. Vacia significa valido. Pura."""
    problems: list[str] = []

    if not isinstance(data, dict):
        return ["el handoff no es un objeto JSON"]

    for field in REQUIRED:
        if field not in data:
            problems.append(f"falta el campo obligatorio '{field}'")

    summary = data.get("summary")
    if isinstance(summary, str) and not summary.strip():
        problems.append("'summary' esta vacio")
    elif summary is not None and not isinstance(summary, str):
        problems.append("'summary' no es texto")

    status = data.get("status")
    if status is not None and status not in STATUSES:
        problems.append(f"'status' invalido: {status!r} (esperado uno de {', '.join(STATUSES)})")

    artifact = data.get("artifact")
    if isinstance(artifact, str) and not artifact.strip():
        problems.append("'artifact' esta vacio: sin ruta no hay artefacto")
    elif artifact is not None and not isinstance(artifact, str):
        problems.append("'artifact' no es texto")

    problems.extend(_check_verified(data.get("verified")))
    problems.extend(_check_inferred(data.get("inferred")))
    problems.extend(_check_open(data.get("openDecisions")))
    problems.extend(_check_skipped(data.get("skipped")))

    if status == "completo" and isinstance(data.get("openDecisions"), list) and data["openDecisions"]:
        problems.append("'status: completo' con decisiones abiertas: si hay una decision pendiente, no esta completo")

    return problems


def _check_verified(items: object) -> list[str]:
    if items is None:
        return []
    if not isinstance(items, list):
        return ["'verified' no es una lista"]
    problems: list[str] = []
    if not items:
        problems.append("'verified' esta vacio: un handoff sin ninguna verificacion no es un handoff")
        return problems
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            problems.append(f"verified[{i}] no es un objeto")
            continue
        for key in ("command", "exit", "output"):
            if key not in item:
                if key == "output":
                    problems.append(
                        f"verified[{i}] sin 'output': afirmar no es verificar, "
                        "falta la salida del comando"
                    )
                else:
                    problems.append(f"verified[{i}] sin '{key}'")
        if "command" in item and not str(item["command"]).strip():
            problems.append(f"verified[{i}] tiene el comando vacio")
        if "output" in item and not str(item["output"]).strip():
            problems.append(f"verified[{i}] no trae la salida del comando: afirmar no es verificar")
        if "exit" in item:
            if not isinstance(item["exit"], int):
                problems.append(f"verified[{i}].exit no es entero")
            elif item["exit"] != 0:
                problems.append(
                    f"verified[{i}] declara un comando con exit {item['exit']}: "
                    "una verificacion que fallo no verifica"
                )
    return problems


def _check_inferred(items: object) -> list[str]:
    if items is None:
        return []
    if not isinstance(items, list):
        return ["'inferred' no es una lista"]
    return [f"inferred[{i}] esta vacio" for i, x in enumerate(items) if not str(x).strip()]


def _check_open(items: object) -> list[str]:
    if items is None:
        return []
    if not isinstance(items, list):
        return ["'openDecisions' no es una lista"]
    return [f"openDecisions[{i}] esta vacio" for i, x in enumerate(items) if not str(x).strip()]


def _check_skipped(items: object) -> list[str]:
    if items is None:
        return []
    if not isinstance(items, list):
        return ["'skipped' no es una lista"]
    problems: list[str] = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            problems.append(f"skipped[{i}] no es un objeto")
            continue
        station = item.get("station")
        reason = item.get("reason")
        if not station:
            problems.append(f"skipped[{i}] sin 'station'")
        elif station not in STATIONS:
            problems.append(f"skipped[{i}] nombra una estacion desconocida: {station!r}")
        if not reason or not str(reason).strip():
            problems.append(
                f"skipped[{i}] ({station}) sin motivo: una estacion salteada sin motivo es un olvido"
            )
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="handoff_gate.py",
        description="Valida un handoff contra el contrato S7.",
    )
    parser.add_argument("file", nargs="?", help="handoff en JSON")
    parser.add_argument("--json", action="store_true", help="salida JSON")
    parser.add_argument("--template", action="store_true", help="imprime un esqueleto valido")
    args = parser.parse_args(argv)

    if args.template:
        print(json.dumps(SKELETON, ensure_ascii=False, indent=2))
        return 0

    if not args.file:
        print("uso: handoff_gate.py <handoff.json> | --template", file=sys.stderr)
        return 2

    path = Path(args.file)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"[INFRA] no se pudo leer {path}: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"[INFRA] JSON invalido en {path}: {exc}", file=sys.stderr)
        return 2

    problems = validate(data)

    if args.json:
        print(json.dumps({"valid": not problems, "problems": problems}, ensure_ascii=False, indent=2))
    else:
        if problems:
            print(f"[INVALIDO] {len(problems)} problema(s) en {path.name}:")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"[VALIDO] {path.name}: contrato S7 completo")

    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
