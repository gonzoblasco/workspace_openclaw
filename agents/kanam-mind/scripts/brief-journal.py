#!/usr/bin/env python3
"""brief-journal.py - Journal durable de briefs: que se entrego, con que fuentes y que veredicto.

Por que existe: el Hito 5.2 del ROADMAP pide >=3 entradas reales consultables. Sin journal, mi
produccion no deja traza y no se puede detectar drift (¿cito menos con el tiempo?).

Uso:
  brief-journal.py add --brief reports/x.md --question "..." --verdict PASS \
      --source docs/a.md --source https://x  [--assignee main] [--notes "..."]
  brief-journal.py add --brief reports/x.md --run-audit          # corre kb-audit y guarda el veredicto
  brief-journal.py list [--json] [--limit 20]
  brief-journal.py show <id>
  brief-journal.py stats                                          # por mes y por veredicto

La DB vive en `reports/journal.db` (git-tracked no: es estado local de la sesion; el brief si).
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS briefs (
  id INTEGER PRIMARY KEY,
  created_at TEXT NOT NULL,
  question TEXT NOT NULL,
  brief_path TEXT NOT NULL,
  verdict TEXT NOT NULL,
  auditor TEXT,
  assignee TEXT,
  sources TEXT,
  notes TEXT
);
"""


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def connect(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    c = sqlite3.connect(path)
    c.executescript(SCHEMA)
    return c


def run_audit(brief_path: str) -> tuple[str, str]:
    here = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(here, "kb-audit.py")
    try:
        p = subprocess.run([sys.executable, script, brief_path, "--json"], capture_output=True, text=True, timeout=300)
        data = json.loads(p.stdout)
        return data.get("verdict", "UNKNOWN"), json.dumps(data.get("counts", {}))
    except Exception as e:  # noqa: BLE001
        return "UNKNOWN", f"audit-error: {e}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports", "journal.db"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--brief", required=True)
    a.add_argument("--question", required=True)
    a.add_argument("--verdict")
    a.add_argument("--run-audit", action="store_true")
    a.add_argument("--source", action="append", default=[])
    a.add_argument("--assignee", default="main")
    a.add_argument("--notes", default="")

    l = sub.add_parser("list")
    l.add_argument("--json", action="store_true")
    l.add_argument("--limit", type=int, default=20)

    s = sub.add_parser("show")
    s.add_argument("id", type=int)

    sub.add_parser("stats")
    args = ap.parse_args()

    conn = connect(args.db)
    conn.row_factory = sqlite3.Row

    if args.cmd == "add":
        if not os.path.isfile(args.brief):
            print(json.dumps({"error": "brief inexistente", "path": args.brief}), file=sys.stderr)
            return 2
        verdict = args.verdict
        auditor = None
        if args.brief.endswith(".json"):
            # Acepta la salida de `kb-audit.py --json`: journal sin re-correr el gate.
            try:
                with open(args.brief, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                verdict = data.get("verdict", verdict)
                auditor = f"kb-audit.py {json.dumps(data.get('counts', {}))}" if "verdict" in data else auditor
            except (OSError, ValueError) as e:
                print(json.dumps({"error": f"json de auditoria invalido: {e}"}), file=sys.stderr)
                return 2
        if args.run_audit:
            verdict, counts = run_audit(args.brief)
            auditor = f"kb-audit.py {counts}"
        if not verdict:
            print(json.dumps({"error": "falta --verdict o --run-audit"}), file=sys.stderr)
            return 2
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO briefs(created_at, question, brief_path, verdict, auditor, assignee, sources, notes) VALUES(?,?,?,?,?,?,?,?)",
            (now(), args.question, os.path.abspath(args.brief), verdict, auditor, args.assignee,
             json.dumps(args.source, ensure_ascii=False), args.notes),
        )
        conn.commit()
        print(json.dumps({"ok": True, "id": cur.lastrowid, "verdict": verdict, "sources": len(args.source),
                          "db": os.path.abspath(args.db)}, ensure_ascii=False))
        return 0

    if args.cmd == "list":
        rows = [dict(r) for r in conn.execute(
            "SELECT id, created_at, verdict, question, brief_path FROM briefs ORDER BY id DESC LIMIT ?", (args.limit,))]
        print(json.dumps(rows, ensure_ascii=False, indent=1) if args.json else
              "\n".join(f"#{r['id']} {r['created_at'][:10]} {r['verdict']:8s} {r['question'][:70]}" for r in rows))
        return 0

    if args.cmd == "show":
        r = conn.execute("SELECT * FROM briefs WHERE id=?", (args.id,)).fetchone()
        if not r:
            print(f"no existe #{args.id}", file=sys.stderr)
            return 1
        print(json.dumps(dict(r), ensure_ascii=False, indent=1))
        return 0

    if args.cmd == "stats":
        rows = [dict(r) for r in conn.execute(
            "SELECT substr(created_at,1,7) mes, verdict, COUNT(*) n FROM briefs GROUP BY 1,2 ORDER BY 1 DESC")]
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
