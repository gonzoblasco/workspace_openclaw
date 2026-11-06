#!/usr/bin/env python3
"""kb-ingest.py - Ingesta de material de estudio citado en la DB de conocimiento del workspace.

Por que existe: las skills de estudio (technical-book-processor, study-tracker, knowledge-
management) exigen "procesar capitulo por capitulo, con su cita", pero no habia forma de
verificar la cita ni de consultar el material despues. Esto convierte un archivo en secciones
citables (`file#Lx-Ly` o `URL + fecha`) dentro de `memory/knowledge.db`, con FTS5, para que el
recorrido de un libro o de un corpus sea retomable.

Diseno:
  - Cada seccion es una unidad con su cita, su hash y su origen. Re-ingerir es idempotente
    (UNIQUE por source + section idx: se reemplaza, no se duplica).
  - `--tag [obs|inf|unk]` solo aplica a texto libre; por defecto las secciones quedan sin etiqueta
    y es `kb-audit.py` el que exige que cada afirmacion del brief tenga etiqueta.
  - Nunca borra: `--replace` reemplaza las secciones de ESA fuente.
  - Sin secretos ni PII: si el archivo trae `.env` o claves, se usa `--redact` para descartarlas.

Uso:
  kb-ingest.py --db memory/knowledge.db --source docs/libro/cap01.md --title "Cap 1: X" --kind book
  kb-ingest.py --db memory/knowledge.db --source https://example.com/doc --fetch --title "Doc"
  kb-ingest.py --db memory/knowledge.db --source docs/libro/cap01.md --split h2 --tag obs
  kb-ingest.py --db memory/knowledge.db --source docs/libro/cap01.md --replace

Salida: JSON con las secciones insertadas y sus citas.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import urllib.request
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
  id INTEGER PRIMARY KEY,
  source TEXT NOT NULL,
  title TEXT,
  kind TEXT NOT NULL DEFAULT 'doc',
  origin TEXT NOT NULL DEFAULT 'file',
  sha256 TEXT,
  ingested_at TEXT NOT NULL,
  UNIQUE(source)
);
CREATE TABLE IF NOT EXISTS sections (
  id INTEGER PRIMARY KEY,
  source_id INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  idx INTEGER NOT NULL,
  heading TEXT,
  body TEXT NOT NULL,
  quote TEXT NOT NULL,
  label TEXT,
  chars INTEGER NOT NULL,
  UNIQUE(source_id, idx)
);
CREATE INDEX IF NOT EXISTS sections_source ON sections(source_id, idx);
CREATE TABLE IF NOT EXISTS notes (
  id INTEGER PRIMARY KEY,
  section_id INTEGER REFERENCES sections(id) ON DELETE SET NULL,
  learning TEXT NOT NULL,
  applies_to TEXT,
  created_at TEXT NOT NULL
);
CREATE VIRTUAL TABLE IF NOT EXISTS sections_fts USING fts5(
  heading, body, content='sections', content_rowid='id', tokenize='unicode61'
);
CREATE TRIGGER IF NOT EXISTS sections_ai AFTER INSERT ON sections BEGIN
  INSERT INTO sections_fts(rowid, heading, body) VALUES (new.id, new.heading, new.body);
END;
CREATE TRIGGER IF NOT EXISTS sections_ad AFTER DELETE ON sections BEGIN
  INSERT INTO sections_fts(sections_fts, rowid, heading, body) VALUES('delete', old.id, old.heading, old.body);
END;
"""

REDACT_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password|passwd|bearer)\s*[:=]\s*\S+"),
    re.compile(r"\b(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})\b"),
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
]


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def redact(text: str) -> str:
    out = text
    for pat in REDACT_PATTERNS:
        out = pat.sub("[redacted]", out)
    return out


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "kanam-mind-kb/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    charset = resp.headers.get_content_charset() or "utf-8"
    text = raw.decode(charset, errors="replace")
    # Markdown si es texto plano; si es HTML, se conserva como texto y se delega el extract
    # fino a web_fetch (esto es la copia durable, no el parser).
    return text


def split_sections(text: str, level: str):
    """Devuelve [(heading, body, start_line, end_line)] con lineas 1-based."""
    lines = text.splitlines()
    marker = {"h1": r"^#\s+", "h2": r"^##\s+", "h3": r"^###\s+", "none": None}[level]
    if not marker:
        return [(None, text.strip(), 1, len(lines) or 1)]
    pat = re.compile(marker)
    sections = []
    cur_head, cur_start = None, 1
    buf: list[str] = []
    for i, line in enumerate(lines, start=1):
        if pat.match(line):
            if buf or cur_head is not None:
                body = "\n".join(buf).strip()
                if body or cur_head:
                    sections.append((cur_head, body, cur_start, i - 1))
            cur_head, cur_start, buf = line.lstrip("# ").strip(), i, []
        else:
            buf.append(line)
    if buf or cur_head is not None:
        sections.append((cur_head, "\n".join(buf).strip(), cur_start, len(lines) or 1))
    return [s for s in sections if s[1] or s[0]]


def quote_for(source: str, start: int, end: int, origin: str) -> str:
    if origin == "url":
        return f"{source} (consultado {now()[:10]})"
    return f"{source}#L{start}-L{end}"


def init_db(path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    return conn


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True)
    ap.add_argument("--source", required=True, help="path o URL")
    ap.add_argument("--title")
    ap.add_argument("--kind", default="doc", choices=["doc", "book", "chapter", "paper", "transcript", "note"])
    ap.add_argument("--split", default="h2", choices=["h1", "h2", "h3", "none"])
    ap.add_argument("--fetch", action="store_true", help="source es una URL que se descarga")
    ap.add_argument("--replace", action="store_true", help="reemplaza las secciones de esta fuente")
    ap.add_argument("--tag", choices=["obs", "inf", "unk"], help="etiqueta por defecto de las secciones")
    ap.add_argument("--redact", action="store_true", default=True)
    args = ap.parse_args()

    origin = "url" if args.fetch or args.source.startswith(("http://", "https://")) else "file"
    if origin == "url":
        text = fetch(args.source)
    else:
        with open(args.source, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()

    if args.redact:
        text = redact(text)

    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    sections = split_sections(text, args.split)
    if not sections:
        print(json.dumps({"error": "sin secciones", "source": args.source}), file=sys.stderr)
        return 2

    conn = init_db(args.db)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO sources(source, title, kind, origin, sha256, ingested_at)
           VALUES(?,?,?,?,?,?)
           ON CONFLICT(source) DO UPDATE SET title=excluded.title, kind=excluded.kind,
             sha256=excluded.sha256, ingested_at=excluded.ingested_at
           RETURNING id""",
        (args.source, args.title or os.path.basename(args.source), args.kind, origin, sha, now()),
    )
    sid = cur.fetchone()[0]
    if args.replace:
        cur.execute("DELETE FROM sections WHERE source_id=?", (sid,))
        cur.execute("UPDATE sources SET sha256=?, ingested_at=? WHERE id=?", (sha, now(), sid))

    rows = []
    for idx, (head, body, start, end) in enumerate(sections):
        quote = quote_for(args.source, start, end, origin)
        cur.execute(
            """INSERT INTO sections(source_id, idx, heading, body, quote, label, chars)
               VALUES(?,?,?,?,?,?,?)
               ON CONFLICT(source_id, idx) DO UPDATE SET heading=excluded.heading,
                 body=excluded.body, quote=excluded.quote, label=excluded.label, chars=excluded.chars""",
            (sid, idx, head, body, quote, args.tag, len(body)),
        )
        rows.append({"idx": idx, "heading": head, "quote": quote, "chars": len(body)})
    conn.commit()
    conn.close()

    print(json.dumps({
        "ok": True, "db": os.path.abspath(args.db), "source": args.source,
        "sha256": sha[:12], "sections": len(rows), "quote_sample": rows[0]["quote"],
        "total_chars": sum(r["chars"] for r in rows),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
