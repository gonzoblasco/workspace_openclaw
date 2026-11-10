#!/usr/bin/env python3
"""
runs_db.py - Registro persistente de corridas del pipeline (v0.3, hito 5.1).

El problema que resuelve: hoy cada corrida del runner escribe un `run.json` en
`/tmp`. Ese archivo existe hasta el proximo reboot y no se puede consultar. Una
corrida de la semana pasada es irrecuperable, y sin ese registro el pipeline es
un comando que se ejecuta, no un sistema que se audita.

Que guarda, por corrida:
  - cuando empezo y cuando termino
  - la plantilla y el repo objetivo
  - cada estacion con su modo, su exit y su salida truncada
  - si el pipeline se completo o se detuvo, y en cual

Que NO guarda: el contenido de los artefactos ni la salida completa. La salida
completa vive en el run.json; aca va truncada para que la base no crezca sin
control (hito 5.3).

SQLite de stdlib, cero dependencias.

Uso:
    runs_db.py record <run.json>        # guarda una corrida del runner
    runs_db.py history [--last N] [--template T]
    runs_db.py show <run_id>
    runs_db.py prune --keep 50
    runs_db.py stats

Exit codes:
  0  ok
  1  no hay registros para lo que se pidio
  2  error de uso o de base (no se pudo abrir o escribir)
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

DEFAULT_DB = Path.home() / ".openclaw" / "workspace" / "agents" / "kanam-dev" / "runs.db"

# Tope de la salida por estacion. Suficiente para ver el error, insuficiente para
# que la base crezca con cada corrida.
OUTPUT_CAP = 2000

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at REAL NOT NULL,
    finished_at REAL,
    template TEXT NOT NULL,
    target_dir TEXT NOT NULL,
    outcome TEXT NOT NULL,
    stopped_at TEXT,
    intake_path TEXT
);
CREATE TABLE IF NOT EXISTS stations (
    run_id INTEGER NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    ord INTEGER NOT NULL,
    station TEXT NOT NULL,
    mode TEXT NOT NULL,
    status TEXT NOT NULL,
    exit_code INTEGER,
    output TEXT,
    PRIMARY KEY (run_id, ord)
);
CREATE INDEX IF NOT EXISTS idx_runs_started ON runs(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_runs_template ON runs(template);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    """Abre o crea la base. Un fallo de apertura es exit 2, nunca silencio."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


# ---------------------------------------------------------------------------
# Escritura.
# ---------------------------------------------------------------------------


def outcome_of(records: list[dict], template: str) -> tuple[str, str | None]:
    """Deriva el resultado de la corrida desde sus estaciones. Pura.

    No confia en un campo `status` del run.json: lo calcula de los exits, que es
    lo que realmente paso.
    """
    for rec in records:
        status = rec.get("status", "")
        if status in ("failed", "infra", "missing"):
            outcome = "infra" if status == "infra" else "detenido"
            return outcome, rec.get("station")
    return "completo", None


def record(db_path: Path, run_path: Path) -> int:
    try:
        run = json.loads(run_path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"[INFRA] no se pudo leer {run_path}: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"[INFRA] JSON invalido en {run_path}: {exc}", file=sys.stderr)
        return 2

    ctx = run.get("context", {})
    records = run.get("records", [])
    if not ctx.get("template"):
        print(f"[INFRA] {run_path.name} no declara contexto de plantilla", file=sys.stderr)
        return 2

    started = float(run.get("started") or time.time())
    outcome, stopped = outcome_of(records, ctx["template"])

    try:
        conn = connect(db_path)
    except sqlite3.Error as exc:
        print(f"[INFRA] no se pudo abrir la base {db_path}: {exc}", file=sys.stderr)
        return 2

    with conn:
        cur = conn.execute(
            "INSERT INTO runs (started_at, finished_at, template, target_dir, outcome, stopped_at, intake_path)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (started, time.time(), ctx["template"], ctx.get("dir", ""),
             outcome, stopped, run.get("intake")),
        )
        run_id = cur.lastrowid
        for i, rec in enumerate(records):
            conn.execute(
                "INSERT INTO stations (run_id, ord, station, mode, status, exit_code, output)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                (run_id, i, rec.get("station", ""), rec.get("mode", ""),
                 rec.get("status", ""), rec.get("exit"),
                 (rec.get("output") or "")[:OUTPUT_CAP]),
            )

    print(f"registrada corrida #{run_id}: {ctx['template']} -> {outcome}"
          + (f" en {stopped}" if stopped else ""))
    return 0


# ---------------------------------------------------------------------------
# Lectura.
# ---------------------------------------------------------------------------


def format_duration(started: float, finished: float | None) -> str:
    if not finished:
        return "-"
    secs = max(0, int(finished - started))
    if secs < 60:
        return f"{secs}s"
    return f"{secs // 60}m{secs % 60:02d}s"


def history(db_path: Path, last: int, template: str | None) -> int:
    try:
        conn = connect(db_path)
    except sqlite3.Error as exc:
        print(f"[INFRA] {exc}", file=sys.stderr)
        return 2

    sql = "SELECT * FROM runs"
    params: list = []
    if template:
        sql += " WHERE template = ?"
        params.append(template)
    sql += " ORDER BY started_at DESC LIMIT ?"
    params.append(last)

    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("[INFO] sin corridas registradas todavia")
        return 1

    print(f"{'id':>4}  {'fecha':<17} {'plantilla':<9} {'resultado':<10} {'dur':>6}  repo")
    for r in rows:
        date = time.strftime("%Y-%m-%d %H:%M", time.localtime(r["started_at"]))
        outcome = r["outcome"] + (f"@{r['stopped_at']}" if r["stopped_at"] else "")
        print(f"{r['id']:>4}  {date:<17} {r['template']:<9} {outcome:<10} "
              f"{format_duration(r['started_at'], r['finished_at']):>6}  {r['target_dir']}")
    return 0


def show(db_path: Path, run_id: int) -> int:
    try:
        conn = connect(db_path)
    except sqlite3.Error as exc:
        print(f"[INFRA] {exc}", file=sys.stderr)
        return 2

    run = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
    if run is None:
        print(f"[INFO] no existe la corrida #{run_id}")
        return 1

    print(f"corrida #{run['id']} | {run['template']} | {run['outcome']}"
          + (f" en {run['stopped_at']}" if run['stopped_at'] else " completo"))
    print(f"repo: {run['target_dir']}")
    print(f"inicio: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(run['started_at']))}"
          f" | duracion: {format_duration(run['started_at'], run['finished_at'])}")
    print()
    for st in conn.execute(
        "SELECT * FROM stations WHERE run_id = ? ORDER BY ord", (run_id,)
    ).fetchall():
        print(f"  {st['ord']}. {st['station']:<10} {st['mode']:<15} {st['status']:<12} "
              f"exit={st['exit_code'] if st['exit_code'] is not None else '-'}")
        if st["output"] and st["status"] in ("failed", "infra", "missing"):
            first = st["output"].strip().splitlines()[0] if st["output"].strip() else ""
            print(f"      {first[:120]}")
    return 0


def stats(db_path: Path) -> int:
    try:
        conn = connect(db_path)
    except sqlite3.Error as exc:
        print(f"[INFRA] {exc}", file=sys.stderr)
        return 2

    total = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    if total == 0:
        print("[INFO] sin corridas registradas todavia")
        return 1

    print(f"corridas: {total}")
    print()
    print("por resultado:")
    for row in conn.execute(
        "SELECT outcome, COUNT(*) n FROM runs GROUP BY outcome ORDER BY n DESC"
    ):
        print(f"  {row['outcome']:<10} {row['n']}")
    print()
    print("por plantilla:")
    for row in conn.execute(
        "SELECT template, COUNT(*) n, "
        "SUM(CASE WHEN outcome='completo' THEN 1 ELSE 0 END) ok "
        "FROM runs GROUP BY template ORDER BY n DESC"
    ):
        print(f"  {row['template']:<10} {row['n']:>3} corridas, {row['ok']:>3} completas")
    print()
    print("estaciones que mas fallan:")
    for row in conn.execute(
        "SELECT station, COUNT(*) n FROM stations "
        "WHERE status IN ('failed','infra','missing') GROUP BY station ORDER BY n DESC LIMIT 5"
    ):
        print(f"  {row['station']:<10} {row['n']}")
    return 0


def prune(db_path: Path, keep: int) -> int:
    try:
        conn = connect(db_path)
    except sqlite3.Error as exc:
        print(f"[INFRA] {exc}", file=sys.stderr)
        return 2

    total = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    if total <= keep:
        print(f"[INFO] {total} corrida(s), nada que purgar (tope {keep})")
        return 0

    with conn:
        conn.execute(
            "DELETE FROM runs WHERE id NOT IN "
            "(SELECT id FROM runs ORDER BY started_at DESC LIMIT ?)", (keep,))
    remaining = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    print(f"purgadas {total - remaining} corrida(s); quedan {remaining} (tope {keep})")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="runs_db.py",
        description="Registro persistente de corridas del pipeline.",
    )
    ap.add_argument("command", choices=("record", "history", "show", "stats", "prune"))
    ap.add_argument("arg", nargs="?", help="run.json para record, run_id para show")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="ruta de la base")
    ap.add_argument("--last", type=int, default=20, help="cuantas corridas mostrar")
    ap.add_argument("--template", help="filtrar history por plantilla")
    ap.add_argument("--keep", type=int, default=50, help="corridas a conservar en prune")
    args = ap.parse_args(argv)

    db = Path(args.db)

    if args.command == "record":
        if not args.arg:
            print("uso: runs_db.py record <run.json>", file=sys.stderr)
            return 2
        return record(db, Path(args.arg))

    if args.command == "history":
        return history(db, args.last, args.template)

    if args.command == "show":
        if not args.arg:
            print("uso: runs_db.py show <run_id>", file=sys.stderr)
            return 2
        return show(db, int(args.arg))

    if args.command == "stats":
        return stats(db)

    return prune(db, args.keep)


if __name__ == "__main__":
    sys.exit(main())
