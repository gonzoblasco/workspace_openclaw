#!/usr/bin/env python3
"""
runner.py - Encadena las estaciones del pipeline segun la plantilla (F0/S1-S7).

Hasta aca cada estacion funcionaba sola y el orden lo ponia una persona. Este
runner toma el intake, elige que estaciones corre la plantilla, las ejecuta en
orden y se detiene en la primera que no devuelve 0.

Regla central: **un gate que no puede medir no deja pasar.** Exit 2 corta el
pipeline igual que exit 1, con distinto mensaje. Si una estacion bloqueante no
corre por falta de herramienta, el pipeline no sigue.

Por que no hay motor nuevo: el estado vive en un JSON de corrida en disco, no en
memoria. Si el proceso muere, `--resume` retoma desde la ultima estacion
completada. Eso es lo que necesita un pipeline que corre entre turnos de agente.

Exit codes:
  0  todas las estaciones de la plantilla terminaron en verde
  1  una estacion reporto hallazgos (el pipeline se detuvo)
  2  una estacion no pudo medir, o error de uso/entorno (el pipeline se detuvo)

Uso:
    runner.py --intake /tmp/intake.json
    runner.py --intake /tmp/intake.json --dir /ruta/al/repo
    runner.py --intake /tmp/intake.json --dry-run
    runner.py --resume /tmp/run.json

Cero dependencias. Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_INFRA = 2

# ---------------------------------------------------------------------------
# La matriz de plantillas. Es la unica fuente de verdad de que corre cada una.
# Un valor por estacion: "blocking", "declarative" o None (no aplica).
# ---------------------------------------------------------------------------
# Slice y build no tienen comando propio (los hace el agente). Son bloqueantes
# en toda plantilla donde aplican, y su evidencia se declara en el intake bajo
# `manual_evidence`. Sin evidencia, un bloqueante detiene el pipeline.

TEMPLATE_MATRIX: dict[str, dict[str, str | None]] = {
    "hotfix": {
        "intake": "blocking",
        "discovery": None,
        "slice": "blocking",
        "build": "blocking",
        "verify": "blocking",
        "review": "declarative",
        "handoff": "blocking",
    },
    "task": {
        "intake": "blocking",
        "discovery": None,
        "slice": "blocking",
        "build": "blocking",
        "verify": "blocking",
        "review": "blocking",
        "handoff": "blocking",
    },
    "feature": {
        "intake": "blocking",
        "discovery": "blocking",
        "slice": "blocking",
        "build": "blocking",
        "verify": "blocking",
        "review": "blocking",
        "handoff": "blocking",
    },
    "audit": {
        "intake": "blocking",
        "discovery": "blocking",
        "slice": None,
        "build": None,
        "verify": "blocking",
        "review": "declarative",
        "handoff": "blocking",
    },
    "docs": {
        "intake": "blocking",
        "discovery": None,
        "slice": "blocking",
        "build": "blocking",
        "verify": "blocking",
        "review": "declarative",
        "handoff": "blocking",
    },
}

STATION_ORDER = ("intake", "discovery", "slice", "build", "verify", "review", "handoff")


# ---------------------------------------------------------------------------
# Planificacion (funcion pura). El resto del runner solo ejecuta este plan.
# ---------------------------------------------------------------------------


def build_plan(template: str) -> list[dict]:
    """Devuelve la lista ordenada de estaciones a correr con su modo.

    No aplica (None) se omite y queda registrado: no es lo mismo que salteado.
    """
    matrix = TEMPLATE_MATRIX.get(template)
    if matrix is None:
        raise ValueError(f"plantilla desconocida: {template}")
    plan: list[dict] = []
    for station in STATION_ORDER:
        mode = matrix[station]
        if mode is None:
            plan.append({"station": station, "mode": "not-applicable"})
        else:
            plan.append({"station": station, "mode": mode})
    return plan


def blocking_stations(template: str) -> list[str]:
    return [s for s in STATION_ORDER if TEMPLATE_MATRIX[template].get(s) == "blocking"]


# ---------------------------------------------------------------------------
# Comandos por estacion.
# ---------------------------------------------------------------------------


def station_command(station: str, ctx: dict) -> list[str] | None:
    """Comando real de la estacion, o None si es manual.

    `docs` usa docs-sync (verify de documentacion); el resto de plantillas usa el
    verify de stack a traves del despachador.
    """
    if station == "verify":
        if ctx["template"] == "docs":
            return [sys.executable, str(HERE / "docs_sync.py"), ctx["dir"], "--check"]
        return [sys.executable, str(HERE / "kanam-dev"), "audit", ctx["dir"]]
    if station == "handoff":
        if not ctx.get("handoff"):
            return None
        return [sys.executable, str(HERE / "handoff_gate.py"), ctx["handoff"]]
    return None


def run_station(station: str, mode: str, ctx: dict) -> dict:
    """Ejecuta una estacion y devuelve su registro. No decide: registra."""
    record: dict = {"station": station, "mode": mode, "started": time.time()}

    if mode == "not-applicable":
        record.update(status="not-applicable", exit=None, output="")
        return record

    # S1 ya esta satisfecha por el propio intake.json: pedirle evidencia aparte
    # seria pedir dos veces lo mismo y detener el pipeline en la primera estacion.
    if station == "intake":
        record.update(status="ok", exit=0, command=None,
                      output=f"intake {ctx['template']} completo ({ctx.get('intake_status', 'complete')})")
        return record

    cmd = station_command(station, ctx)

    if cmd is None:
        # Estacion manual: se exige evidencia declarada en el intake. Una
        # estacion manual sin evidencia NUNCA es "ok": si es bloqueante detiene
        # el pipeline, y si es declarativa deja constancia y sigue.
        declared = ctx.get("manual_evidence", {}).get(station)
        if declared:
            record.update(status="declared", exit=0, output=str(declared), command=None)
        elif mode == "blocking":
            record.update(
                status="missing",
                exit=EXIT_FINDINGS,
                output=f"{station} es bloqueante en {ctx['template']} y no trae evidencia",
                command=None,
            )
        else:
            record.update(
                status="declared-without-evidence",
                exit=0,
                output=f"{station} sin evidencia declarada: queda registrado para el handoff",
                command=None,
            )
        return record

    proc = subprocess.run(cmd, capture_output=True, text=True)
    record.update(
        command=" ".join(cmd),
        exit=proc.returncode,
        output=(proc.stdout or "") + (proc.stderr or ""),
        status="ok" if proc.returncode == 0 else "failed" if proc.returncode == 1 else "infra",
    )
    return record


# ---------------------------------------------------------------------------
# Persistencia de la corrida.
# ---------------------------------------------------------------------------


def runs_db_default_db() -> Path:
    """Ruta de la base por defecto, sin importar el modulo de la base."""
    return Path.home() / ".openclaw" / "workspace" / "agents" / "kanam-dev" / "runs.db"


def save_run(path: Path, run: dict) -> None:
    """Escribe el run.json y lo registra en runs.db.

    El registro en la base es best-effort a proposito: si la base falla, la
    corrida ya ocurrio y su resultado no cambia. Se avisa por stderr y se sigue.
    Un fallo de telemetria no puede tumbar un pipeline que ya hizo el trabajo.
    """
    path.write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
    if run.get("registered"):
        return
    # La base se puede redirigir por entorno para que los tests no escriban en la
    # base real del workspace. Verificado: sin esto, test_runner registraba sus
    # corridas temporales en runs.db y contaminaba el historial del usuario.
    raw_db = os.environ.get("KANAM_DEV_RUNS_DB", "").strip()
    db = Path(raw_db) if raw_db else runs_db_default_db()
    try:
        sys.path.insert(0, str(HERE))
        import runs_db  # noqa: PLC0415
        # Primera vez: insertar y guardar el id. Despues: actualizar la MISMA fila.
        # Sin esto, una corrida que muere a mitad quedaba como `completo` porque el
        # registro se hacia con el estado parcial y nunca se corregia.
        run_id = run.get("run_id")
        new_id = runs_db.record(db, path, run_id=run_id)
        if new_id and new_id > 0:
            run["run_id"] = new_id
    except Exception as exc:  # noqa: BLE001
        print(f"[AVISO] no se pudo registrar la corrida en runs.db: {exc}", file=sys.stderr)


def resume_point(run: dict) -> tuple[int, str | None]:
    """Indice desde donde retomar y la razon de la detencion previa, si hubo."""
    for i, rec in enumerate(run["records"]):
        if rec["status"] in ("failed", "infra", "missing"):
            return i, f"{rec['station']} {rec['status']}: {rec.get('output', '')[:200]}"
    return len(run["records"]), None


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="runner.py",
        description="Ejecuta las estaciones del pipeline segun la plantilla del intake.",
    )
    parser.add_argument("--intake", help="intake.json generado por S1")
    parser.add_argument("--resume", help="run.json de una corrida anterior")
    parser.add_argument("--dir", default=".", help="repo objetivo para verify")
    parser.add_argument("--handoff", help="handoff.json a validar en S7")
    parser.add_argument("--dry-run", action="store_true", help="solo imprime el plan")
    parser.add_argument("--out", help="donde escribir run.json")
    args = parser.parse_args(argv)

    if not args.intake and not args.resume:
        parser.print_usage(sys.stderr)
        print("error: hace falta --intake o --resume", file=sys.stderr)
        return EXIT_INFRA

    if args.resume:
        run_path = Path(args.resume)
        try:
            run = json.loads(run_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[INFRA] no se pudo leer {run_path}: {exc}", file=sys.stderr)
            return EXIT_INFRA
        ctx = run["context"]
        start, why = resume_point(run)
        if why:
            # Se retoma desde la estacion que fallo, no desde el principio.
            run["records"] = run["records"][:start]
        plan = build_plan(ctx["template"])
        print(f"resume: {ctx['template']} desde {plan[start]['station'] if start < len(plan) else 'fin'}")
    else:
        intake_path = Path(args.intake)
        try:
            intake = json.loads(intake_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[INFRA] no se pudo leer {intake_path}: {exc}", file=sys.stderr)
            return EXIT_INFRA

        if intake.get("status") != "complete":
            missing = intake.get("missing", [])
            print(f"[BLOQUEA] intake incompleto: faltan {', '.join(missing) or 'campos'}", file=sys.stderr)
            return EXIT_FINDINGS

        ctx = {
            "template": intake["template"],
            "dir": str(Path(args.dir).resolve()),
            "handoff": args.handoff,
            "manual_evidence": intake.get("manual_evidence", {}),
        }
        plan = build_plan(ctx["template"])
        start = 0
        run_path = Path(args.out) if args.out else Path("/tmp") / f"pipeline-{int(ctx['template'] and time.time())}.json"
        run = {
            "context": ctx,
            "records": [],
            "started": time.time(),
            "intake": str(intake_path),
        }

    if args.dry_run:
        print(f"plantilla: {ctx['template']}")
        for i, step in enumerate(plan):
            mark = "->" if i >= start else "  "
            print(f"{mark} {step['station']:10} {step['mode']}")
        return EXIT_OK

    for i, step in enumerate(plan):
        if i < start:
            continue
        rec = run_station(step["station"], step["mode"], ctx)
        run["records"].append(rec)
        save_run(run_path, run)

        label = rec["status"]
        print(f"[{label.upper()}] {step['station']} ({step['mode']})")
        if rec["status"] in ("failed", "infra", "missing"):
            print(f"      {rec.get('output', '')[:400]}")
            print(f"\npipeline detenido en {step['station']}. run: {run_path}")
            return EXIT_INFRA if rec["status"] == "infra" else EXIT_FINDINGS

    print(f"\npipeline completo ({ctx['template']}). run: {run_path}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
