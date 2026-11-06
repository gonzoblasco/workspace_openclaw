#!/usr/bin/env python3
"""kb-search.py - Consulta local (sin modelo) sobre la DB de conocimiento y la memoria curada.

Por que existe: la busqueda semantica del workspace (`scripts/memory-search.py`) devuelve
fragmentos por similitud pero se traga la leccion del pipeline (2026-10-06): hay que poder
**verificar** cada cita contra el disco. Este script busca por FTS5 en `memory/knowledge.db` y
verifica cada cita (`path#Lx-Ly`) contra el archivo real antes de mostrarla. Sin Ollama, sin red,
respuesta en milisegundos.

Uso:
  kb-search.py "verificacion de subagentes"
  kb-search.py --db memory/knowledge.db "brief" -n 5 --json
  kb-search.py --sources            # lista el corpus ingestado
  kb-search.py --stale              # citas cuya fuente cambio desde la ingesta (sha256)

Salida: resultados con su cita, su fuente y el estado de la cita (ok|missing|no-line-span).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys

CITE_RE = re.compile(r"^(?P<path>.+)#L(?P<a>\d+)(?:-L(?P<b>\d+))?$")


def cite_status(quote: str) -> str:
    m = CITE_RE.match(quote)
    if not m:
        return "no-line-span"
    p = m.group("path")
    if not os.path.isfile(p):
        return "missing"
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as fh:
            total = sum(1 for _ in fh)
    except OSError:
        return "missing"
    b = int(m.group("b") or m.group("a"))
    return "ok" if 1 <= int(m.group("a")) <= b <= total else "out-of-range"


def open_db(path: str) -> sqlite3.Connection | None:
    if not os.path.isfile(path):
        return None
    return sqlite3.connect(path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="?")
    ap.add_argument("--db", default="memory/knowledge.db")
    ap.add_argument("-n", "--limit", type=int, default=5)
    ap.add_argument("--sources", action="store_true")
    ap.add_argument("--stale", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    conn = open_db(args.db)
    if conn is None:
        print(json.dumps({"error": "db inexistente", "db": os.path.abspath(args.db)}), file=sys.stderr)
        return 2
    conn.row_factory = sqlite3.Row

    if args.sources:
        rows = [dict(r) for r in conn.execute(
            "SELECT s.id, s.source, s.title, s.kind, s.ingested_at, COUNT(sec.id) n "
            "FROM sources s LEFT JOIN sections sec ON sec.source_id=s.id GROUP BY s.id ORDER BY s.ingested_at DESC")]
        print(json.dumps(rows, ensure_ascii=False, indent=1) if args.json else
              "\n".join(f"[{r['id']}] {r['kind']:10s} {r['n']:3d} sec  {r['source']}" for r in rows))
        return 0

    if args.stale:
        out = []
        for r in conn.execute("SELECT source, sha256, title FROM sources"):
            src = r["source"]
            if not os.path.isfile(src):
                out.append({"source": src, "state": "missing"})
                continue
            with open(src, "rb") as fh:
                h = hashlib.sha256(fh.read().decode("utf-8", errors="replace").encode()).hexdigest()
            out.append({"source": src, "state": "ok" if h == r["sha256"] else "changed"})
        print(json.dumps(out, ensure_ascii=False, indent=1) if args.json else
              "\n".join(f"{r['state']:8s} {r['source']}" for r in out))
        return 0

    if not args.query:
        ap.print_help()
        return 2

    try:
        rows = list(conn.execute(
            """SELECT sec.id, sec.heading, sec.body, sec.quote, sec.label, src.source, src.title,
                      bm25(sections_fts) AS score
               FROM sections_fts
               JOIN sections sec ON sec.id = sections_fts.rowid
               JOIN sources src ON src.id = sec.source_id
               WHERE sections_fts MATCH ?
               ORDER BY score LIMIT ?""",
            (args.query, args.limit)))
    except sqlite3.OperationalError as e:
        print(json.dumps({"error": f"query FTS invalida: {e}", "query": args.query}), file=sys.stderr)
        return 2

    results = []
    for r in rows:
        st = cite_status(r["quote"])
        results.append({
            "title": r["title"], "heading": r["heading"], "label": r["label"],
            "quote": r["quote"], "state": st, "score": round(r["score"], 4),
            "excerpt": (r["body"] or "")[:400],
        })

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        print(f"KB SEARCH · {len(results)} resultados · {args.query}")
        for r in results:
            mark = {"ok": "✓", "missing": "✗", "out-of-range": "✗", "no-line-span": "?"}[r["state"]]
            print(f"\n  {mark} [{r['label'] or '-'}] {r['title']} · {r['heading'] or '(sin titulo)'}")
            print(f"     cita: {r['quote']}  ({r['state']})")
            print(f"     {(r['excerpt'] or '').strip()[:280]}")
    missing = sum(1 for r in results if r["state"] in ("missing", "out-of-range"))
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
