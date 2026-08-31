#!/usr/bin/env python3
"""
memory-end-session.py - Write session end to DB as source of truth,
then regenerate the .md daily as an exportable view (not required).

Inverts the flow: the database (daily_notes + sessions_relacional) is the
source of truth; the markdown files become regenerable views.

Usage:
  ./memory-end-session.py --project "<name>" --summary "<text>" [--date YYYY-MM-DD]

Behavior:
  1. Appends the session-end block to daily_notes in the DB (source of truth)
  2. Regenerates memory/YYYY-MM-DD.md from the DB (view)
  3. Keeps everything DB-first
"""

import argparse
import sqlite3
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = os.environ.get("MEMORY_DB", "memory/memory.db")
WORKSPACE = Path(__file__).resolve().parent.parent


def sql_escape(s):
    """Escape single quotes for safe SQL string interpolation."""
    return s.replace("'", "''")


def db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_or_create_daily(conn, date):
    """Return id of the daily row for a date; create if missing."""
    row = conn.execute(
        "SELECT id, content FROM daily_notes WHERE date=? AND type='daily' ORDER BY id DESC LIMIT 1",
        (date,),
    ).fetchone()
    return row


def build_session_block(project, summary, branch, tscores):
    """Build the markdown session-end block to append."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    block = f"""
## Session End - {project}
**End:** {now}
**Summary:** {summary}
**Branch:** {branch}
"""
    if tscores:
        block += f"{tscores}\n"
    return block


def append_to_daily_db(conn, date, block, project):
    """Append session block to daily_notes content in DB (source of truth), idempotent.
    Avoids duplicating if the same project already has a Session End for this date."""
    marker = f"## Session End - {project}"
    row = get_or_create_daily(conn, date)
    if row and marker in row["content"]:
        # Already recorded for this project/date - skip to avoid duplicate
        return row["id"], False

    if row:
        new_content = row["content"] + block
        conn.execute(
            "UPDATE daily_notes SET content=? WHERE id=?",
            (new_content, row["id"]),
        )
        daily_id = row["id"]
    else:
        cur = conn.execute(
            "INSERT INTO daily_notes (date, type, content, created_at) VALUES (?, 'daily', ?, datetime('now'))",
            (date, block),
        )
        daily_id = cur.lastrowid
    conn.commit()
    return daily_id, True


def export_daily_to_md(conn, date):
    """Regenerate memory/YYYY-MM-DD.md from the DB (view)."""
    row = get_or_create_daily(conn, date)
    if not row:
        return None
    md_path = WORKSPACE / "memory" / f"{date}.md"
    # Ensure the content starts with a title header for readability
    content = row["content"]
    if not content.strip().startswith("# "):
        title = f"# Daily {date}\n\n"
        content = title + content
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(content, encoding="utf-8")
    return md_path


def run_catalog():
    """Run the catalog script to rebuild embeddings/topics from DB-first dailies."""
    catalog_script = WORKSPACE / "scripts" / "memory-catalog-v2.py"
    if catalog_script.exists():
        import subprocess
        subprocess.run([sys.executable, str(catalog_script)], check=False)


def main():
    parser = argparse.ArgumentParser(description="Write session end to DB as source of truth")
    parser.add_argument("--project", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--branch", default="unknown")
    parser.add_argument("--tscore", default="", help="Complexity T-score line if any")
    parser.add_argument("--skip-catalog", action="store_true", help="Skip running the catalog")
    parser.add_argument("--skip-export", action="store_true", help="Skip regenerating the .md view")
    args = parser.parse_args()

    if not os.path.exists(DB_PATH):
        print(f"Error: DB not found at {DB_PATH}")
        sys.exit(1)

    block = build_session_block(args.project, args.summary, args.branch, args.tscore)

    conn = db_connection()
    try:
        daily_id, inserted = append_to_daily_db(conn, args.date, block, args.project)
        if inserted:
            print(f"✅ Daily actualizado en DB (id={daily_id}) para {args.date}")
            print(f"   Proyecto: {args.project}")
        else:
            print(f"ℹ️  Ya existe un Session End para '{args.project}' en {args.date} - sin duplicar")
    finally:
        conn.close()

    # Regenerate the .md as a view (optional but keeps humans able to read)
    if not args.skip_export:
        conn = db_connection()
        try:
            md_path = export_daily_to_md(conn, args.date)
            if md_path:
                print(f"   View .md regenerado: {md_path.relative_to(WORKSPACE)}")
        finally:
            conn.close()

    # Rebuild embeddings/topics from the DB-first daily (source of truth)
    if not args.skip_catalog:
        run_catalog()

    print("✅ Sesión guardada (DB-first)")


if __name__ == "__main__":
    main()
