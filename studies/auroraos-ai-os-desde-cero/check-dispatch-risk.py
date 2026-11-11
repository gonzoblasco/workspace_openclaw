#!/usr/bin/env python3
"""
check-dispatch-risk.py - Un paso que no declara su riesgo no esta listo para delegar.

POR QUE EXISTE (2026-11-11). En studies/auroraos-ai-os-desde-cero/ el agente
aviso ANTES de escribir que VirtualBox no correria el OS x86 sobre un Mac ARM.
El humano ignoró el aviso, y el costo aparecio recien en el primer boot: hubo
que cambiar de emulador. El agente no fallo - tenia el dato y lo dijo - pero el
aviso se perdio porque no era un campo del contrato, era una frase suelta en
una conversacion.

En este workspace pasa lo mismo con otra forma: los programas del Planner
tienen id, task, role, owner, exit_criteria, depends_on, gate, write_paths y
evidence, pero NO tienen un campo de riesgo. Medido el 2026-11-11: 5 de 6
programas en agents/kanam-planner/.knowledge/programs/ no mencionan la palabra
riesgo ni una vez, y `dispatch_contract.py` no la incluye en el contrato de
despacho. El riesgo existe, pero vive en la sesion que delego, no en el
artefacto que el siguiente ejecutor lee.

Que revisa, por cada paso NO completado (status != completed):
  1. DECLARACION - el paso tiene `risks` con al menos una entrada no vacia.
     Un `"risks": []` explicito es valido y significa "evaluado, ninguno".
     Ausente es distinto de vacio: ausente es no evaluado.
  2. VERIFICABLE - cada riesgo tiene `assumption` (que se esta asumiendo) y
     `falsified_by` (que observacion demostraria que el supuesto es falso).
     Un riesgo sin forma de falsarse es una preocupacion, no un riesgo.
  3. AVISO AL EJECUTOR - `dispatch_contract.py` incluye los riesgos en el
     prompt que se le entrega al agente. Si el campo existe pero no viaja, el
     ejecutor sigue sin saberlo.

Codigos de salida (verification-gates: cero casos no es verde):
  0  APLICA   - todos los pasos no completados declaran y propagan su riesgo
  1  VIOLACION- hay pasos sin declarar, o declarados sin forma de falsarse
  2  NO-CORRIDO- no hay programas en la ruta dada: el check no probo nada
  3  ERROR    - un programa no parsea

Uso:
    check-dispatch-risk.py [root]

`root` es inyectable para que los tests construyan programs falsos en un
directorio temporal y no siembren el defecto en el workspace real.
"""

import json
import sys
from pathlib import Path

# El gate vive en studies/<slug>/ pero audita el workspace: la raiz del repo
# es dos niveles arriba, no la raiz de la clase (si no, corre contra studies/
# y reporta "no hay programas", un falso NO-CORRIDO).
ROOT = Path(__file__).resolve().parent.parent.parent
PROGRAMS_DIR = Path("agents/kanam-planner/.knowledge/programs")
DISPATCH = Path("agents/kanam-planner/scripts/dispatch_contract.py")

# Estados que se consideran cumplidos y no se auditan.
DONE = {"completed", "cancelled"}


def load_programs(root: Path):
    """(lista de (path, data), lista de (path, error))."""
    d = root / PROGRAMS_DIR
    ok, bad = [], []
    if not d.is_dir():
        return ok, bad
    for p in sorted(d.glob("*.json")):
        try:
            ok.append((p, json.loads(p.read_text(encoding="utf-8"))))
        except Exception as e:  # JSON roto es un hallazgo, no un skip
            bad.append((p, f"{type(e).__name__}: {e}"))
    return ok, bad


def open_steps(program):
    return [s for s in program.get("steps", []) if s.get("status") not in DONE]


def check_step(step):
    """Lista de defectos del paso (vacia = declara riesgo de forma utilizable)."""
    problems = []
    sid = step.get("id")
    if "risks" not in step:
        return [f"paso {sid}: no declara `risks` (ausente != vacio)"]
    risks = step["risks"]
    if not isinstance(risks, list):
        return [f"paso {sid}: `risks` no es una lista"]
    for i, r in enumerate(risks):
        if not isinstance(r, dict):
            problems.append(f"paso {sid} riesgo {i}: no es un objeto")
            continue
        for field in ("assumption", "falsified_by"):
            v = r.get(field)
            if not isinstance(v, str) or not v.strip():
                problems.append(f"paso {sid} riesgo {i}: falta `{field}`")
    return problems


def main(argv):
    root = Path(argv[1]).resolve() if len(argv) > 1 else ROOT
    progs, broken = load_programs(root)
    if not progs and not broken:
        print(f"NO-CORRIDO: no hay programas en {root / PROGRAMS_DIR}")
        return 2
    for p, err in broken:
        print(f"ERROR: {p.name}: no parsea ({err})")
    if broken:
        return 3

    violations = []
    audited = 0
    for path, prog in progs:
        for step in open_steps(prog):
            audited += 1
            for msg in check_step(step):
                violations.append(f"{path.name}: {msg}")

    dispatch_missing = False
    disp = root / DISPATCH
    if disp.exists():
        text = disp.read_text(encoding="utf-8")
        if "risk" not in text.lower() and "riesgo" not in text.lower():
            dispatch_missing = True

    if violations:
        print(f"VIOLACION: {len(violations)} defecto(s) en {audited} paso(s) no completados")
        for v in violations:
            print(f"  - {v}")
        if dispatch_missing:
            print(f"  - {DISPATCH}: el contrato de despacho no incluye riesgos")
        return 1

    if dispatch_missing:
        print(f"VIOLACION: el contrato de despacho no incluye riesgos ({DISPATCH})")
        return 1

    print(f"APLICA: {audited} paso(s) no completados declaran y propagan su riesgo")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
