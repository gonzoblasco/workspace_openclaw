#!/usr/bin/env python3
"""Program plans for the Crew Planner.

Un *programa* es un objetivo multi-sesion: 3+ pasos secuenciales, 2+ roles,
mas de una sesion, o una fecha/bloqueo externo. Vive en
`.knowledge/programs/<slug>.json` y es la fuente de verdad del avance.

El Planner no ejecuta el trabajo: define pasos, duenos, criterios de salida,
dependencias y evidencia. El CORE ejecuta los contratos y vuelve al Planner
en los gates y en el cierre.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROLE_ROOT = Path(__file__).resolve().parents[1]
PROGRAMS_DIR = Path(
    os.environ.get("PROGRAM_PLAN_DIR", ROLE_ROOT / ".knowledge" / "programs")
)

ROLE_AGENT = {
    "core": "main",
    "planner": "kanam-planner",
    "dev": "kanam-dev",
    "ops": "kanam-ops",
    "mind": "kanam-mind",
    "studio": "kanam-studio",
    "auditor": "kanam-auditor",
    "critic": "kanam-critic",
}

VALID_ROLES = set(ROLE_AGENT)
VALID_STATUS = {"pending", "in-progress", "review", "blocked", "completed", "waived"}
TERMINAL_STATUS = {"completed", "waived"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "programa"


def fail(message: str, code: int = 1) -> None:
    print(f"❌ {message}", file=sys.stderr)
    raise SystemExit(code)


def program_path(slug: str) -> Path:
    # Los slugs pueden llevar puntos (v0.3) pero nunca '..' ni barras.
    if not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", slug or "") or ".." in (slug or ""):
        fail(f"Slug invalido: '{slug}'. Usá minúsculas, números, guiones y puntos.")
    return PROGRAMS_DIR / f"{slug}.json"


def normalize_program(program: dict[str, Any]) -> dict[str, Any]:
    """Completa campos faltantes de programas escritos por versiones previas.

    El primer programa real (abya-yala-05) se escribio a mano con `write_path`
    singular y sin timestamps. El script no debe romperse por eso: normaliza en
    memoria y migra el archivo en el proximo update.
    """
    program.setdefault("slug", slugify(program.get("title", "programa")))
    program.setdefault("title", program["slug"])
    program.setdefault("objective", "")
    program.setdefault("status", "active")
    program.setdefault("owner", "gonzalo")
    program.setdefault("created_at", now())
    program.setdefault("updated_at", program["created_at"])
    program.setdefault("gates", [])
    program.setdefault("steps", [])
    program.setdefault("metadata", {})
    for index, step in enumerate(program["steps"], start=1):
        step.setdefault("id", index)
        step.setdefault("task", "")
        step.setdefault("role", "dev")
        step.setdefault("owner", ROLE_AGENT.get(step["role"], "kanam-dev"))
        step.setdefault("status", "pending")
        step.setdefault("exit_criteria", "")
        step.setdefault("depends_on", [])
        step.setdefault("gate", None)
        if "write_paths" not in step:
            legacy = step.get("write_path")
            if isinstance(legacy, str) and legacy:
                step["write_paths"] = [legacy]
            elif isinstance(legacy, list):
                step["write_paths"] = legacy
            else:
                step["write_paths"] = []
        step.setdefault("evidence", [])
        step.setdefault("blocker", None)
        step.setdefault("waiver_reason", None)
        step.setdefault("attempts", 0)
        step.setdefault("created_at", program["created_at"])
        step.setdefault("updated_at", program["updated_at"])
        step.setdefault("started_at", None)
        step.setdefault("completed_at", None)
        step.setdefault("session_ref", None)
    return program


def load_program(slug: str) -> dict[str, Any]:
    path = program_path(slug)
    if not path.exists():
        fail(f"No existe el programa '{slug}' en {PROGRAMS_DIR}")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"No pude leer {path}: {exc}")
    return normalize_program(data)


def save_program(program: dict[str, Any]) -> None:
    PROGRAMS_DIR.mkdir(parents=True, exist_ok=True)
    program["updated_at"] = now()
    path = program_path(program["slug"])
    tmp = path.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(program, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def all_programs() -> list[dict[str, Any]]:
    if not PROGRAMS_DIR.exists():
        return []
    programs = []
    for path in sorted(PROGRAMS_DIR.glob("*.json")):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                programs.append(normalize_program(json.load(fh)))
        except (OSError, json.JSONDecodeError):
            continue
    return programs


def find_step(program: dict[str, Any], step_id: int) -> dict[str, Any]:
    for step in program.get("steps", []):
        if int(step.get("id", 0)) == int(step_id):
            return step
    fail(f"El paso {step_id} no existe en '{program['slug']}'")


def step_deps_done(program: dict[str, Any], step: dict[str, Any]) -> bool:
    by_id = {int(s["id"]): s for s in program.get("steps", [])}
    for dep in step.get("depends_on", []) or []:
        dep_step = by_id.get(int(dep))
        if dep_step is None:
            return False
        if dep_step.get("status") not in TERMINAL_STATUS:
            return False
    return True


def next_step(program: dict[str, Any]) -> dict[str, Any] | None:
    for step in program.get("steps", []):
        if step.get("status") in TERMINAL_STATUS:
            continue
        if step.get("status") == "blocked":
            continue
        if step_deps_done(program, step):
            return step
    return None


def progress(program: dict[str, Any]) -> tuple[int, int]:
    steps = program.get("steps", [])
    done = sum(1 for s in steps if s.get("status") in TERMINAL_STATUS)
    return done, len(steps)


def parse_ids(raw: str | None) -> list[int]:
    if not raw:
        return []
    ids: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            fail(f"Dependencia invalida: '{part}' (usá numeros separados por coma)")
    return ids


def cmd_init(args: argparse.Namespace) -> None:
    slug = args.slug or slugify(args.title)
    path = program_path(slug)
    if path.exists() and not args.force:
        fail(f"El programa '{slug}' ya existe. Usá --force para reemplazarlo.")
    program = {
        "slug": slug,
        "title": args.title,
        "objective": args.objective,
        "status": "active",
        "owner": args.owner,
        "created_at": now(),
        "updated_at": now(),
        "gates": [g.strip() for g in (args.gates or "").split(",") if g.strip()],
        "steps": [],
        "metadata": {},
    }
    save_program(program)
    print(f"✅ Programa creado: {slug} -> {path}")


def cmd_add_step(args: argparse.Namespace) -> None:
    program = load_program(args.slug)
    if args.status not in VALID_STATUS:
        fail(f"Estado invalido: {args.status}")
    if args.role not in VALID_ROLES:
        fail(f"Rol invalido: {args.role}. Validos: {', '.join(sorted(VALID_ROLES))}")
    if not args.exit.strip():
        fail("El criterio de salida es obligatorio.")
    step_id = max([int(s.get("id", 0)) for s in program.get("steps", [])] or [0]) + 1
    step = {
        "id": step_id,
        "task": args.task,
        "role": args.role,
        "owner": args.owner or ROLE_AGENT[args.role],
        "status": args.status,
        "exit_criteria": args.exit.strip(),
        "depends_on": parse_ids(args.depends),
        "gate": args.gate or None,
        "write_paths": [p.strip() for p in (args.write_path or "").split(",") if p.strip()],
        "evidence": [],
        "blocker": None,
        "waiver_reason": None,
        "attempts": 0,
        "created_at": now(),
        "updated_at": now(),
        "started_at": None,
        "completed_at": None,
        "session_ref": None,
    }
    program.setdefault("steps", []).append(step)
    save_program(program)
    print(f"✅ Paso {step_id} agregado a {args.slug}: {args.task}")


def cmd_update(args: argparse.Namespace) -> None:
    program = load_program(args.slug)
    step = find_step(program, args.step)
    if args.status not in VALID_STATUS:
        fail(f"Estado invalido: {args.status}")
    if args.status == "completed" and not args.evidence and not args.force:
        fail("Un paso 'completed' requiere --evidence (o --force explicito).")
    if args.status == "blocked" and not (args.blocker or "").strip():
        fail("Un paso 'blocked' requiere --blocker.")
    if args.status == "waived" and not (args.waiver_reason or "").strip() and not args.force:
        fail("Un paso 'waived' requiere --waiver-reason (o --force).")

    previous = step.get("status")
    step["status"] = args.status
    step["updated_at"] = now()
    if args.blocker is not None:
        step["blocker"] = args.blocker or None
    if args.waiver_reason is not None:
        step["waiver_reason"] = args.waiver_reason or None
    if args.session_ref is not None:
        step["session_ref"] = args.session_ref or None
    if args.evidence:
        step.setdefault("evidence", []).extend(args.evidence)
    if args.status == "blocked":
        step["blocker"] = args.blocker
    if args.status == "in-progress":
        if not step.get("started_at"):
            step["started_at"] = now()
        if previous in {"pending", "blocked"}:
            step["attempts"] = int(step.get("attempts") or 0) + 1
        step["blocker"] = None
    if args.status in TERMINAL_STATUS:
        step["completed_at"] = now()
        step["blocker"] = None
    save_program(program)
    print(f"✅ Paso {args.step} de {args.slug} -> {args.status}")


def cmd_show(args: argparse.Namespace) -> None:
    """Muestra todos los pasos, no solo el proximo.

    El review semanal necesita los titulos exactos para no inventar pasos.
    """
    programs = [load_program(args.slug)] if args.slug else [
        p for p in all_programs() if p.get("status") == "active"
    ]
    if not programs:
        print("Sin programas.")
        return
    for index, program in enumerate(programs):
        if index:
            print()
        done, total = progress(program)
        print(f"🗺️ {program['title']} [{program.get('status')}] — {done}/{total}")
        for step in program.get("steps", []):
            gate = f" gate={step['gate']}" if step.get("gate") else ""
            print(
                f"  #{step['id']} [{step['status']}] {step['task']} — {step['owner']}{gate}"
            )
            if step.get("blocker"):
                print(f"      blocker: {step['blocker']}")


def cmd_next(args: argparse.Namespace) -> None:
    program = load_program(args.slug)
    step = next_step(program)
    if not step:
        print("Sin próximo paso accionable (todos completados, waived o bloqueados).")
        return
    print(
        f"#{step['id']} {step['task']} | {step['status']} | "
        f"{step['owner']} ({step['role']}) | salida: {step['exit_criteria']}"
    )


def _format_program_brief(program: dict[str, Any]) -> list[str]:
    done, total = progress(program)
    pct = round((done / total) * 100) if total else 0
    lines = [f"🗺️ {program['title']} [{program['status']}] — {done}/{total} ({pct}%)"]
    step = next_step(program)
    if step:
        lines.append(
            f"   Próximo: #{step['id']} {step['task']} → {step['owner']} ({step['status']})"
        )
    else:
        lines.append("   Próximo: sin paso accionable")
    blocked = [s for s in program.get("steps", []) if s.get("status") == "blocked"]
    for s in blocked:
        lines.append(f"   🚫 #{s['id']} bloqueado: {s.get('blocker')}")
    return lines


def cmd_brief(args: argparse.Namespace) -> None:
    programs = [load_program(args.slug)] if args.slug else all_programs()
    if not args.all:
        programs = [p for p in programs if p.get("status") == "active"]
    if not programs:
        if not args.quiet:
            print("Sin programas activos.")
        return
    for idx, program in enumerate(programs):
        if idx:
            print()
        print("\n".join(_format_program_brief(program)))


def _step_counts(program: dict[str, Any]) -> dict[str, int]:
    counts = {status: 0 for status in VALID_STATUS}
    for step in program.get("steps", []):
        status = step.get("status", "pending")
        counts[status] = counts.get(status, 0) + 1
    return counts


def cmd_status(args: argparse.Namespace) -> None:
    programs = [load_program(args.slug)] if args.slug else all_programs()
    stale_cutoff = datetime.now(timezone.utc) - timedelta(days=args.stale_days)
    payload = []
    for program in programs:
        done, total = progress(program)
        stale = []
        for step in program.get("steps", []):
            if step.get("status") not in {"in-progress", "review"}:
                continue
            try:
                updated = datetime.fromisoformat(step.get("updated_at", ""))
            except ValueError:
                continue
            if updated < stale_cutoff:
                stale.append(step["id"])
        payload.append(
            {
                "slug": program["slug"],
                "title": program["title"],
                "status": program.get("status"),
                "progress": {"done": done, "total": total},
                "next_step": (next_step(program) or {}).get("id"),
                "blocked": [
                    {"id": s["id"], "blocker": s.get("blocker")}
                    for s in program.get("steps", [])
                    if s.get("status") == "blocked"
                ],
                "stale_steps": stale,
                "counts": _step_counts(program),
                "steps": [
                    {
                        "id": s["id"],
                        "task": s["task"],
                        "status": s["status"],
                        "owner": s["owner"],
                        "gate": s.get("gate"),
                        "blocker": s.get("blocker"),
                    }
                    for s in program.get("steps", [])
                ],
            }
        )
    if args.json:
        print(json.dumps({"generated_at": now(), "programs": payload}, indent=2, ensure_ascii=False))
        return
    if not payload:
        print("Sin programas.")
        return
    for item in payload:
        print(
            f"{item['slug']}: {item['status']} — "
            f"{item['progress']['done']}/{item['progress']['total']} — "
            f"next: {item['next_step'] or '-'}"
        )
        if item["blocked"]:
            print(f"   bloqueos: {item['blocked']}")
        if item["stale_steps"]:
            print(f"   estancados: {item['stale_steps']}")


def _detect_cycles(program: dict[str, Any]) -> list[str]:
    steps = {int(s["id"]): s for s in program.get("steps", [])}
    visiting: set[int] = set()
    visited: set[int] = set()
    errors: list[str] = []

    def visit(node: int, stack: list[int]) -> None:
        if node in visited:
            return
        if node in visiting:
            cycle = " -> ".join(str(x) for x in stack + [node])
            errors.append(f"Ciclo de dependencias: {cycle}")
            return
        visiting.add(node)
        for dep in steps[node].get("depends_on", []) or []:
            dep = int(dep)
            if dep in steps:
                visit(dep, stack + [node])
        visiting.remove(node)
        visited.add(node)

    for node in steps:
        visit(node, [])
    return errors


def lint_program(program: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    steps = program.get("steps", [])
    if not steps:
        errors.append("El programa no tiene pasos.")
    ids = [int(s.get("id", 0)) for s in steps]
    if len(ids) != len(set(ids)):
        errors.append("Hay ids de paso duplicados.")
    by_id = {int(s.get("id", 0)): s for s in steps}
    for step in steps:
        sid = step.get("id")
        if not step.get("task"):
            errors.append(f"Paso {sid}: falta 'task'.")
        if step.get("role") not in VALID_ROLES:
            errors.append(f"Paso {sid}: rol invalido '{step.get('role')}'.")
        if not step.get("owner"):
            errors.append(f"Paso {sid}: falta 'owner'.")
        if step.get("status") not in VALID_STATUS:
            errors.append(f"Paso {sid}: estado invalido '{step.get('status')}'.")
        if not (step.get("exit_criteria") or "").strip():
            errors.append(f"Paso {sid}: falta 'exit_criteria'.")
        for dep in step.get("depends_on", []) or []:
            if int(dep) not in by_id:
                errors.append(f"Paso {sid}: depende del paso inexistente {dep}.")
            if int(dep) == int(sid):
                errors.append(f"Paso {sid}: se depende a si mismo.")
        if step.get("status") == "completed" and not step.get("evidence"):
            errors.append(f"Paso {sid}: completado sin evidencia.")
        if step.get("status") == "blocked" and not step.get("blocker"):
            errors.append(f"Paso {sid}: bloqueado sin 'blocker'.")
        if step.get("status") == "waived" and not step.get("waiver_reason"):
            warnings.append(f"Paso {sid}: waived sin waiver_reason.")
        if step.get("status") == "review" and not step.get("gate"):
            warnings.append(f"Paso {sid}: review sin gate explicito.")
    errors.extend(_detect_cycles(program))
    gates = set(program.get("gates", []) or [])
    for gate in gates:
        if gate not in {"auditor", "critic"}:
            warnings.append(f"Gate desconocido: {gate}")
            continue
        has_gate_step = any(
            s.get("gate") == gate or s.get("role") == gate for s in steps
        )
        if not has_gate_step:
            warnings.append(f"El programa declara gate '{gate}' pero no tiene paso de {gate}.")
    return errors, warnings


def cmd_lint(args: argparse.Namespace) -> None:
    programs = [load_program(args.slug)] if args.slug else all_programs()
    results = []
    total_errors = 0
    for program in programs:
        errors, warnings = lint_program(program)
        total_errors += len(errors)
        results.append(
            {
                "slug": program["slug"],
                "ok": not errors,
                "errors": errors,
                "warnings": warnings,
            }
        )
    if args.json:
        print(json.dumps({"ok": total_errors == 0, "results": results}, indent=2, ensure_ascii=False))
    else:
        for item in results:
            mark = "✅" if item["ok"] else "❌"
            print(f"{mark} {item['slug']}")
            for err in item["errors"]:
                print(f"   error: {err}")
            for warn in item["warnings"]:
                print(f"   warning: {warn}")
        if not results:
            print("Sin programas para validar.")
    if total_errors:
        raise SystemExit(1)


def cmd_set_gate(args: argparse.Namespace) -> None:
    program = load_program(args.slug)
    step = find_step(program, args.step)
    step["gate"] = None if args.gate == "none" else args.gate
    step["updated_at"] = now()
    save_program(program)
    print(f"✅ Paso {args.step} de {args.slug}: gate -> {args.gate}")


def cmd_set_gates(args: argparse.Namespace) -> None:
    program = load_program(args.slug)
    program["gates"] = [g.strip() for g in args.gates.split(",") if g.strip()]
    save_program(program)
    print(f"✅ Programa {args.slug}: gates -> {', '.join(program['gates']) or 'ninguno'}")


def cmd_close(args: argparse.Namespace) -> None:
    program = load_program(args.slug)
    errors, _warnings = lint_program(program)
    if errors and not args.force:
        fail(
            "No puedo cerrar: el plan tiene errores de lint: "
            + "; ".join(errors)
            + ". Usá --force para cerrar igual."
        )
    pending = [
        s for s in program.get("steps", []) if s.get("status") not in TERMINAL_STATUS
    ]
    if pending and not args.force:
        fail(
            "No puedo cerrar: quedan pasos no terminales "
            + ", ".join(f"#{s['id']}({s['status']})" for s in pending)
            + ". Usá --force para cerrar igual."
        )
    program["status"] = "completed"
    program["closed_at"] = now()
    if pending:
        program.setdefault("metadata", {})["forced_close"] = True
        program["metadata"]["forced_close_steps"] = [s["id"] for s in pending]
    if errors:
        program.setdefault("metadata", {})["forced_close_lint"] = errors
    save_program(program)
    print(f"✅ Programa cerrado: {args.slug}")


def cmd_list(args: argparse.Namespace) -> None:
    programs = all_programs()
    if not programs:
        print("Sin programas.")
        return
    for program in programs:
        done, total = progress(program)
        print(
            f"{program['slug']:28} {program.get('status', '?'):10} "
            f"{done}/{total}  {program.get('title', '')}"
        )


def cmd_board(args: argparse.Namespace) -> None:
    programs = [p for p in all_programs() if p.get("status") == "active"]
    if not programs:
        print("Sin programas activos.")
        return
    print("| Programa | Estado | Progreso | Próximo | Dueño | Bloqueo |")
    print("|---|---|---|---|---|---|")
    for program in programs:
        done, total = progress(program)
        step = next_step(program)
        next_txt = f"#{step['id']} {step['task']}" if step else "—"
        owner = step["owner"] if step else "—"
        blocked = [s for s in program.get("steps", []) if s.get("status") == "blocked"]
        blocker = blocked[0].get("blocker") if blocked else "—"
        print(
            f"| {program['title']} | {program.get('status')} | {done}/{total} | "
            f"{next_txt} | {owner} | {blocker} |"
        )


def cmd_report(args: argparse.Namespace) -> None:
    programs = all_programs()
    counts = {status: 0 for status in VALID_STATUS}
    blocked = []
    stale_cutoff = datetime.now(timezone.utc) - timedelta(days=args.stale_days)
    for program in programs:
        for step in program.get("steps", []):
            status = step.get("status", "pending")
            counts[status] = counts.get(status, 0) + 1
            if status == "blocked":
                blocked.append(
                    {
                        "program": program["slug"],
                        "step": step["id"],
                        "blocker": step.get("blocker"),
                    }
                )
            if status in {"in-progress", "review"}:
                try:
                    updated = datetime.fromisoformat(step.get("updated_at", ""))
                except ValueError:
                    continue
                if updated < stale_cutoff:
                    blocked.append(
                        {
                            "program": program["slug"],
                            "step": step["id"],
                            "blocker": f"estancado desde {step.get('updated_at')}",
                        }
                    )
    payload = {
        "generated_at": now(),
        "programs": len(programs),
        "active": sum(1 for p in programs if p.get("status") == "active"),
        "steps": counts,
        "alerts": blocked,
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    print(f"Programas: {payload['programs']} ({payload['active']} activos)")
    print("Pasos: " + ", ".join(f"{k}={v}" for k, v in counts.items() if v))
    if blocked:
        print("Alertas:")
        for item in blocked:
            print(f"  - {item['program']} #{item['step']}: {item['blocker']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="program_plan.py",
        description="Planes de programa del Crew Planner.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="Crear un programa.")
    p.add_argument("slug", nargs="?", help="Slug; si se omite, se deriva del titulo.")
    p.add_argument("--title", required=True)
    p.add_argument("--objective", required=True)
    p.add_argument("--owner", default="gonzalo")
    p.add_argument("--gates", default="", help="Gates separados por coma: auditor,critic")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add-step", help="Agregar un paso.")
    p.add_argument("slug")
    p.add_argument("task")
    p.add_argument("--role", required=True, choices=sorted(VALID_ROLES))
    p.add_argument("--owner", default="")
    p.add_argument("--exit", required=True, dest="exit")
    p.add_argument("--depends", default="")
    p.add_argument("--gate", default="", choices=["", "auditor", "critic"])
    p.add_argument("--write-path", default="")
    p.add_argument("--status", default="pending", choices=sorted(VALID_STATUS))
    p.set_defaults(func=cmd_add_step)

    p = sub.add_parser("update", help="Actualizar un paso.")
    p.add_argument("slug")
    p.add_argument("step", type=int)
    p.add_argument("status", choices=sorted(VALID_STATUS))
    p.add_argument("--blocker", default=None)
    p.add_argument("--evidence", action="append", default=[])
    p.add_argument("--session-ref", default=None)
    p.add_argument("--waiver-reason", default=None)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("show", help="Mostrar todos los pasos de un programa (o de los activos).")
    p.add_argument("slug", nargs="?")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("next", help="Mostrar el proximo paso accionable.")
    p.add_argument("slug")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("brief", help="Brief compacto para el CORE/Telegram.")
    p.add_argument("slug", nargs="?")
    p.add_argument("--all", action="store_true", help="Incluir programas no activos.")
    p.add_argument("--quiet", action="store_true")
    p.set_defaults(func=cmd_brief)

    p = sub.add_parser("status", help="Estado JSON o resumido.")
    p.add_argument("slug", nargs="?")
    p.add_argument("--json", action="store_true")
    p.add_argument("--stale-days", type=int, default=7)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("lint", help="Validar el plan.")
    p.add_argument("slug", nargs="?")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_lint)

    p = sub.add_parser("set-gate", help="Cambiar el gate de un paso.")
    p.add_argument("slug")
    p.add_argument("step", type=int)
    p.add_argument("gate", choices=["auditor", "critic", "none"])
    p.set_defaults(func=cmd_set_gate)

    p = sub.add_parser("set-gates", help="Cambiar los gates del programa.")
    p.add_argument("slug")
    p.add_argument("gates", help="Lista separada por coma: auditor,critic")
    p.set_defaults(func=cmd_set_gates)

    p = sub.add_parser("close", help="Cerrar un programa.")
    p.add_argument("slug")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_close)

    p = sub.add_parser("list", help="Listar programas.")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("board", help="Tablero Markdown de programas activos.")
    p.set_defaults(func=cmd_board)

    p = sub.add_parser("report", help="Metricas y alertas.")
    p.add_argument("--json", action="store_true")
    p.add_argument("--stale-days", type=int, default=7)
    p.set_defaults(func=cmd_report)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
