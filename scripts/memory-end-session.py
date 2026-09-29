#!/usr/bin/env python3
"""
memory-end-session.py - Write session end to DB as source of truth,
then regenerate the .md daily as an exportable view (not required).

Inverts the flow: the database (daily_notes + sessions_relacional) is the
source of truth; the markdown files become regenerable views.

Usage:
  ./memory-end-session.py --project "<name>" --summary "<text>" [--date YYYY-MM-DD]

Behavior:
  1. Reconciles the .md into the DB if the .md has content the DB lacks (guard, 2026-09-14)
  2. Appends the session-end block to daily_notes in the DB (source of truth)
  3. Regenerates memory/YYYY-MM-DD.md from the DB (view)
  4. Keeps everything DB-first

Guard (2026-09-14): the export DB -> .md is LOSSY when the .md was edited directly or
written by a concurrent session, because the DB is not always the more complete source.
Before writing, md-only sections are merged into the DB and the .md is backed up to /tmp.
"""

import argparse
import shutil
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
    conn.execute("PRAGMA foreign_keys = ON")
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
    # Match the marker on a WHOLE LINE, never as a substring: "## Session End - workspace"
    # is a substring of "## Session End - workspace-general", so a plain `in` check
    # silently blocked saves for the shorter slug (found 2026-09-15).
    if row and any(ln.strip() == marker for ln in row["content"].split("\n")):
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


def _strip_title(text, date):
    """Drop leading level-1 title lines so md/db bodies compare cleanly.

    Handles repeated titles. Two writers share the same daily file: the built-in
    memory flush (OpenClaw) and this script. A second writer's "# Daily YYYY-MM-DD"
    can end up as the first line if the .md was replaced, so drop every leading
    "# " line, not just one (found 2026-09-29).
    """
    lines = text.lstrip("\n").split("\n")
    while lines and lines[0].startswith("# "):
        lines.pop(0)
    return "\n".join(lines)


def _normalize_section_body(body):
    """Remove artifact level-1 headings buried inside a section body.

    A daily is "## section" blocks under a single title. When the built-in memory
    flush appends to the same file, its leading "# Daily YYYY-MM-DD" lands inside
    the previous section's body (see memory/2026-09-29.md). Any "# " line there is
    an artifact, so drop it and keep the section content.
    """
    return "\n".join(ln for ln in body.split("\n") if not ln.startswith("# "))


def _dedupe_sections(sections):
    """Keep the first occurrence of each "## " heading, plus one preamble.

    Idempotency guard: the built-in memory flush and this script can both write
    the same daily file, so the .md can carry the same section twice. Only the
    first instance of a heading survives; later duplicates are dropped.
    """
    seen = set()
    out = []
    for head, body in sections:
        body = _normalize_section_body(body)
        key = head if head is not None else "__preamble__"
        if key in seen:
            continue
        seen.add(key)
        out.append((head, body))
    return out


def _join_sections(sections):
    """Serialize (heading, body) pairs back to markdown, dropping empties."""
    blocks = [b.strip("\n") for _, b in sections if b and b.strip()]
    return "\n\n".join(blocks) + "\n" if blocks else ""


def _split_sections(text):
    """Split markdown into ordered (heading, block) pairs; preamble gets heading None."""
    sections = []
    cur_head = None
    cur_lines = []
    for ln in text.split("\n"):
        if ln.startswith("## "):
            if cur_lines or cur_head is not None:
                sections.append((cur_head, "\n".join(cur_lines)))
            cur_head = ln.strip()
            cur_lines = [ln]
        else:
            cur_lines.append(ln)
    if cur_lines:
        sections.append((cur_head, "\n".join(cur_lines)))
    return sections


def reconcile_md_into_db(conn, date):
    """Seed the DB from the .md when the .md holds sections the DB lacks.

    Returns a report string when it acted, or None when the DB already covers the .md.
    """
    md_path = WORKSPACE / "memory" / f"{date}.md"
    if not md_path.exists():
        return None

    md_body = _strip_title(md_path.read_text(encoding="utf-8"), date).strip("\n")
    if not md_body.strip():
        return None

    row = get_or_create_daily(conn, date)

    if row is None:
        # No DB row for the date: writing the session-end block alone would clobber
        # the whole .md on export. Seed the row from the .md first (deduped).
        md_clean = _join_sections(_dedupe_sections(_split_sections(md_body)))
        md_heads = [h for h, _ in _dedupe_sections(_split_sections(md_body)) if h]
        backup = _backup_md(md_path, date)
        cur = conn.execute(
            "INSERT INTO daily_notes (date, type, content, created_at) VALUES (?, 'daily', ?, datetime('now'))",
            (date, md_clean),
        )
        conn.commit()
        note = f"la DB no tenia fila para {date} - creada desde el .md (id={cur.lastrowid}, {len(md_heads)} secciones)"
        return note + (f" | backup: {backup}" if backup else "")

    db_body = (row["content"] or "").strip("\n")
    md_secs = _dedupe_sections(_split_sections(md_body))
    db_secs = _dedupe_sections(_split_sections(db_body))
    md_heads = {h for h, _ in md_secs if h}
    db_heads = {h for h, _ in db_secs if h}

    md_only = [(h, b) for h, b in md_secs if h and h not in db_heads]
    if not md_only and _join_sections(md_secs).strip() == _join_sections(db_secs).strip():
        return None  # DB already covers the .md, de-duplicated: the export is lossless

    db_only = [b for h, b in db_secs if h and h not in md_heads and b.strip()]
    # Rebuild from de-duplicated sections; never re-ingest the raw .md body, which
    # may carry the same section twice (found 2026-09-29).
    merged_parts = [b for _, b in md_secs if b and b.strip()] + db_only
    merged = "\n\n".join(p.strip("\n") for p in merged_parts) + "\n" if merged_parts else ""

    backup = _backup_md(md_path, date)
    conn.execute("UPDATE daily_notes SET content=? WHERE id=?", (merged, row["id"]))
    conn.commit()

    parts = ["secciones solo en el .md: " + ", ".join(h for h, _ in md_only)]
    if db_only:
        parts.append(f"{len(db_only)} seccion(es) de la DB preservadas")
    note = f"DB reconciliada desde el .md (id={row['id']}) deduplicada - " + "; ".join(parts)
    return note + (f" | backup: {backup}" if backup else "")


def _backup_md(md_path, date):
    """Copy the .md to /tmp before it is regenerated. Returns the backup path or None."""
    backup = Path("/tmp") / f"daily-{date}.backup.md"
    try:
        shutil.copy2(md_path, backup)
        return str(backup)
    except OSError:
        return None


def export_daily_to_md(conn, date):
    """Regenerate memory/YYYY-MM-DD.md from the DB (view).

    Always emits exactly one top-level title. The DB body is normalized first so a
    stale "# Daily YYYY-MM-DD" left inside it by a concurrent writer cannot produce
    a second heading on export (found 2026-09-29: grep -c returned 5).
    """
    row = get_or_create_daily(conn, date)
    if not row:
        return None
    md_path = WORKSPACE / "memory" / f"{date}.md"
    body = _strip_title(row["content"] or "", date).strip("\n")
    content = f"# Daily {date}\n\n{body}\n" if body else f"# Daily {date}\n"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(content, encoding="utf-8")
    return md_path


def dedupe_daily_db(conn, date):
    """De-duplicate the daily row in the DB in place. Returns report or None."""
    row = get_or_create_daily(conn, date)
    if not row:
        return None
    body = _strip_title(row["content"] or "", date).strip("\n")
    secs = _dedupe_sections(_split_sections(body))
    clean = _join_sections(secs)
    before_heads = len([h for h, _ in _split_sections(body) if h])
    after_heads = len([h for h, _ in secs if h])
    if clean.strip() != body.strip():
        conn.execute("UPDATE daily_notes SET content=? WHERE id=?", (clean, row["id"]))
        conn.commit()
        return f"DB dedupe (id={row['id']}): {before_heads} -> {after_heads} secciones"
    return None


def run_catalog():
    """Run the catalog script to rebuild embeddings/topics from DB-first dailies."""
    catalog_script = WORKSPACE / "scripts" / "memory-catalog-v2.py"
    if catalog_script.exists():
        import subprocess
        subprocess.run([sys.executable, str(catalog_script)], check=False)


def main():
    parser = argparse.ArgumentParser(description="Write session end to DB as source of truth")
    parser.add_argument("--project")
    parser.add_argument("--summary")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--branch", default="unknown")
    parser.add_argument("--tscore", default="", help="Complexity T-score line if any")
    parser.add_argument("--skip-catalog", action="store_true", help="Skip running the catalog")
    parser.add_argument("--skip-export", action="store_true", help="Skip regenerating the .md view")
    parser.add_argument(
        "--no-reconcile",
        action="store_true",
        help="Skip the .md -> DB guard and export the DB as-is (may drop md-only sections)",
    )
    parser.add_argument(
        "--dedupe-only",
        action="store_true",
        help="Only reconcile + de-duplicate the daily and regenerate the .md; no session block appended",
    )
    args = parser.parse_args()

    if not os.path.exists(DB_PATH):
        print(f"Error: DB not found at {DB_PATH}")
        sys.exit(1)

    if not args.dedupe_only and (not args.project or not args.summary):
        parser.error("--project and --summary are required unless --dedupe-only is set")

    block = build_session_block(args.project, args.summary, args.branch, args.tscore)

    conn = db_connection()
    try:
        if not args.no_reconcile:
            report = reconcile_md_into_db(conn, args.date)
            if report:
                print(f"   [guard] {report}")
            dreport = dedupe_daily_db(conn, args.date)
            if dreport:
                print(f"   [dedupe] {dreport}")
        if not args.dedupe_only:
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
