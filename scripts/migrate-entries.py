#!/usr/bin/env python3
"""
migrate-entries.py - Desaplanar la jerarquia de las fichas (2026-09-23).

PROBLEMA: una "ficha" (`sessions_relacional`) NO es una sesion. Es un DIA, con
varias sesiones adentro, cada una con sus subsecciones. Todo eso vive aplanado
en un solo campo de texto (`content_bare`). Medido:

    Nivel 0 - fichas (sessions_relacional):     51
    Nivel 1 - unidades de nivel 2:             521   <- hoy invisibles
    Nivel 2 - todas las secciones:             843
    Aparte  - checklist items:                 102

Las 521 unidades de nivel 2 se titulan asi:
    408  tema real          ("Fusion de skills de estudio", "Cap 1 - The Architecture")
    113  boilerplate        ("Session End - workspace" 63, "Cierre" 12,
                             "Self-reflection" 4, "Conversation Summary" 34)

QUE HACE ESTA MIGRACION:

  1. Crea `session_entries`: una fila por unidad de nivel 2, con titulo, offsets
     y una clasificacion (`kind`). Es el nivel que faltaba entre la ficha y las
     secciones.

  2. Agrega `sessions_relacional.project` y `.daily_id`, capturados donde el
     dato existe (ver docs/architecture/fichas-registro-columnas.md).

QUE NO HACE, a proposito:

  - NO interpreta: no decide "esto es un resultado" ni "esto es una decision".
    Solo separa las unidades y las clasifica por su titulo (tema vs boilerplate),
    que es determinista.
  - NO inventa el proyecto de las fichas viejas: 28 de 51 no lo tienen en el
    texto. Quedan en NULL. Adivinar sobre prosa fabrica datos (ADR-059).

La interpretacion semantica va en una etapa aparte, con revision humana.

Uso:
    migrate-entries.py --dry-run
    migrate-entries.py [--db <path>]
"""
import argparse
import re
import shutil
import sqlite3
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
DB = WS / "memory" / "memory.db"

# Titulos de nivel 2 que son estructura del proceso, no temas de trabajo.
BOILERPLATE = re.compile(
    r"^(Session End|Cierre de sesi|Self-reflection|Conversation Summary|Notas de proceso)",
    re.I,
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS session_entries (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL,      -- FK a sessions_relacional (la ficha = el dia)
    ordinal     INTEGER NOT NULL,      -- orden dentro de la ficha
    level       INTEGER NOT NULL,      -- 2 | 3 (normalmente 2)
    kind        TEXT NOT NULL,         -- 'tema' | 'boilerplate' (determinista)
    title       TEXT NOT NULL,
    char_start  INTEGER NOT NULL,      -- offsets hacia content_bare del padre
    char_end    INTEGER NOT NULL,
    time_start  TEXT,
    time_end    TEXT,
    -- Campos INTERPRETADOS (los llena interpret-entries.py, con revision):
    topic       TEXT,
    summary     TEXT,
    activity    TEXT,                  -- eje interpretado: trabajo | estudio | reflexion
                                       -- (distinto de `kind`, que es determinista)
    UNIQUE (session_id, ordinal),
    FOREIGN KEY(session_id) REFERENCES sessions_relacional(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_entries_session ON session_entries(session_id);
CREATE INDEX IF NOT EXISTS idx_entries_kind    ON session_entries(kind);
CREATE INDEX IF NOT EXISTS idx_entries_title   ON session_entries(title);
"""

LEVEL2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
TIME_RANGE = re.compile(r"\(\s*(\d{1,2}:\d{2})\s*[-\u2013]\s*(\d{1,2}:\d{2})\s*\)\s*$")


def load_parser():
    """El parser de contenido (una sola fuente para limpiar titulos).

    `clean_title` vive en content-parse.py: esta script extraia el titulo con
    su propia logica y por eso un comentario `<!-- project: ... -->` llego
    crudo a la UI ('Engram - adopcion completa <!-- project: ... -->').
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "content_parse", WS / "scripts" / "content-parse.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024:
            return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} TB"


def split_level2(text):
    """Parte el texto en las unidades de nivel 2, con offsets.

    Devuelve dicts con level, kind, title, char_start, char_end, time_start,
    time_end. Los offsets apuntan al `content_bare` del padre: el texto NO se
    copia (copiarlo duplicaba el 95%, ver ADR-059 y ADR-060).
    """
    if not text:
        return []

    lines = text.split("\n")
    offsets, p = [], 0
    for line in lines:
        offsets.append(p)
        p += len(line) + 1
    total = len(text)

    marks = []
    for i, line in enumerate(lines):
        m = LEVEL2.match(line)
        if m:
            marks.append((i, m.group(1).strip()))

    entries = []
    for idx, (i, raw) in enumerate(marks):
        start = min(offsets[i] + len(lines[i]) + 1, total)
        end = offsets[marks[idx + 1][0]] if idx + 1 < len(marks) else total
        if start > end:
            start = end
        ts, te = (None, None)
        tr = TIME_RANGE.search(raw)
        if tr:
            ts, te = tr.group(1), tr.group(2)
        title = load_parser().clean_title(raw)
        entries.append(
            {
                "level": 2,
                "kind": "boilerplate" if BOILERPLATE.match(title) else "tema",
                "title": title,
                "char_start": start,
                "char_end": end,
                "time_start": ts,
                "time_end": te,
            }
        )
    return entries


def ensure_columns(conn, dry_run):
    have = {r[1] for r in conn.execute("PRAGMA table_info(sessions_relacional)")}
    added = []
    for col in ("project", "daily_id"):
        if col in have:
            continue
        if not dry_run:
            conn.execute(f"ALTER TABLE sessions_relacional ADD COLUMN {col} TEXT")
        added.append(col)
    if added and not dry_run:
        conn.commit()
    return added


def backfill_daily_id(conn, dry_run):
    """Linca cada ficha a su documento diario, SOLO cuando la fecha lo confirma.

    Medido: 23 de 51 fichas tienen correspondencia (20 por fecha exacta, 3 por
    contenido identico). Las otras 28 quedan en NULL.

    Diferencia con la FK espuria que se elimino en ADR-058: esa AFIRMABA que el
    id coincidia (y era falso: 0 de 47 compartian fecha). Esta columna DECLARA a
    que diario pertenece, y puede ser NULL sin mentir.
    """
    fichas = conn.execute("select id, date, content_bare from sessions_relacional").fetchall()
    linked = 0
    updates = []
    for fid, date, cb in fichas:
        # 1. por contenido identico (la evidencia mas fuerte)
        hit = conn.execute(
            "select id from daily_notes where content=? limit 1", (cb,)
        ).fetchone()
        if not hit and date:
            # 2. por fecha normalizada (la ficha puede tener "2026-08-24-2214")
            hit = conn.execute(
                "select id from daily_notes where date=? and type='daily' limit 1",
                (date[:10],),
            ).fetchone()
        updates.append((str(hit[0]) if hit else None, fid))
        if hit:
            linked += 1
    if not dry_run:
        conn.executemany("UPDATE sessions_relacional SET daily_id=? WHERE id=?", updates)
        conn.commit()
    return linked, len(fichas)


def migrate(conn, dry_run):
    out = []

    added = ensure_columns(conn, dry_run)
    out.append(
        f"  sessions_relacional: columnas {'agregadas -> ' + ', '.join(added) if added else 'project/daily_id ya presentes'}"
    )

    rows = conn.execute("select id, content_bare from sessions_relacional").fetchall()
    entries = []
    for fid, cb in rows:
        for n, e in enumerate(split_level2(cb)):
            entries.append(
                (fid, n, e["level"], e["kind"], e["title"], e["char_start"], e["char_end"], e["time_start"], e["time_end"])
            )

    if not dry_run:
        conn.execute("DELETE FROM session_entries")
        conn.executemany(
            """INSERT OR REPLACE INTO session_entries
               (session_id, ordinal, level, kind, title, char_start, char_end, time_start, time_end)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            entries,
        )
        conn.commit()

    temas = sum(1 for e in entries if e[3] == "tema")
    boiler = len(entries) - temas
    out.append(
        f"  session_entries: {len(entries)} unidades de nivel 2 "
        f"({temas} temas, {boiler} boilerplate) que estaban aplanadas en el texto"
    )

    linked, total = backfill_daily_id(conn, dry_run)
    out.append(
        f"  daily_id: {linked}/{total} fichas linkeadas a su documento diario "
        f"({total - linked} quedan NULL: no hay correspondencia verificable)"
    )

    return out


def verify(conn):
    print("\nVerificacion:")
    bad = 0
    c = conn.cursor()

    fk = list(c.execute("PRAGMA foreign_key_check"))
    print(f"  foreign keys: {len(fk)} violaciones {'OK' if not fk else '!!'}")
    if fk:
        bad += 1

    huerfanas = c.execute(
        """SELECT count(*) FROM session_entries e
           LEFT JOIN sessions_relacional s ON s.id = e.session_id
           WHERE s.id IS NULL"""
    ).fetchone()[0]
    print(f"  entries huerfanas: {huerfanas} {'OK' if huerfanas == 0 else '!!'}")
    if huerfanas:
        bad += 1

    # Los offsets deben reconstruir texto.
    vacias = 0
    for sid, cs, ce in c.execute("SELECT session_id, char_start, char_end FROM session_entries"):
        row = c.execute("SELECT content_bare FROM sessions_relacional WHERE id=?", (sid,)).fetchone()
        if not row or not row[0][cs:ce].strip():
            vacias += 1
    print(f"  entries con offset invalido: {vacias} {'OK' if vacias == 0 else '!!'}")
    if vacias:
        bad += 1

    # El daily_id debe apuntar a un documento real.
    malos = c.execute(
        """SELECT count(*) FROM sessions_relacional s
           WHERE s.daily_id IS NOT NULL
             AND NOT EXISTS (SELECT 1 FROM daily_notes d WHERE d.id = CAST(s.daily_id AS INTEGER))"""
    ).fetchone()[0]
    print(f"  daily_id que no resuelven: {malos} {'OK' if malos == 0 else '!!'}")
    if malos:
        bad += 1

    for t in ("session_entries",):
        n = c.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {n} filas")

    # El contenido original no se toca (migracion aditiva).
    n = c.execute("SELECT count(*) FROM sessions_relacional WHERE content_bare IS NULL OR TRIM(content_bare)=''").fetchone()[0]
    print(f"  fichas con contenido vacio: {n} {'OK' if n == 0 else '!!'}")
    if n:
        bad += 1
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--db", default=None)
    args = ap.parse_args()

    global DB
    if args.db:
        DB = Path(args.db).resolve()
    if not DB.exists():
        sys.exit(f"No existe {DB}")

    if not args.dry_run:
        backup = DB.with_suffix(".db.pre-entries")
        shutil.copy2(DB, backup)
        print(f"backup: {backup} ({human(backup.stat().st_size)})")

    size_before = DB.stat().st_size
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        if not args.dry_run:
            conn.executescript(SCHEMA)
            conn.commit()
        print("Migracion:" + (" (DRY-RUN)" if args.dry_run else ""))
        for line in migrate(conn, args.dry_run):
            print(line)
        if not args.dry_run:
            bad = verify(conn)
        else:
            bad = 0
    finally:
        conn.close()

    print(f"\nTamano: {human(size_before)} -> {human(DB.stat().st_size)}")
    if args.dry_run:
        print("(dry-run: nada se escribio)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
