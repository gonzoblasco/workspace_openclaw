#!/usr/bin/env python3
"""
migrate-content.py - Descompone el markdown de memory.db en campos consultables.

Todo el contenido de la DB es markdown en un campo de texto. Esta migracion lo
estructura en tres piezas (decidido por Gonzo), cada una con fiabilidad medida:

  1. Metadatos del documento -> columnas en `daily_notes`:
       doc_kind     'harness' | 'daily'   (100% confiable: prefijo "# Session:")
       session_key  de los dumps         (100% parseable: 65/65)
       session_id   idem                 (100% parseable: 65/65)
       source       webchat | reset       (100% parseable: 65/65)

     Ademas corrige `type`: hoy 6 dumps del harness estan marcados type='daily'.
     El `type` se recalcula desde el contenido, que es la fuente de verdad.

  2. `sections` -> los headings ## y ### como filas propias.
     Medido: 1255 secciones en 106 docs. El rango horario del titulo se separa
     a columnas, asi "Session End - workspace" agrupa aunque cada instancia
     tenga horas distintas.

  3. `checklist_items` -> los "- [ ]" / "- [x]" embebidos.
     Medido: 67 abiertos y 35 hechos que HOY NO APARECEN EN NINGUN LISTADO,
     porque nunca llegaron a la tabla `todos`.

QUE NO HACE, a proposito:
  Extraer entidades (repos, PRs) del texto libre. Medido: de 5143 matches de
  `owner/name`, la mayoria son rutas de archivo (`dist/stacks`, `memory/archive`)
  y fechas (`28/08`). Regex sobre prosa fabrica datos falsos.

Uso:
    migrate-content.py --dry-run
    migrate-content.py [--db <path>]
"""
import argparse
import importlib.util
import shutil
import sqlite3
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
DB = WS / "memory" / "memory.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sections (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_type    TEXT NOT NULL,          -- 'daily' | 'session' (la TABLA, no el tipo de doc)
    doc_id      INTEGER NOT NULL,
    ordinal     INTEGER NOT NULL,       -- orden dentro del documento
    level       INTEGER NOT NULL,       -- 1 (preambulo) | 2 (##) | 3 (###)
    title       TEXT NOT NULL,
    char_start  INTEGER NOT NULL,       -- offset hacia el content del padre
    char_end    INTEGER NOT NULL,
    time_start  TEXT,                   -- "08:00" si el titulo lo tenia
    time_end    TEXT,
    UNIQUE (doc_type, doc_id, ordinal)
);
-- El body NO se copia: se reconstruye con content[char_start:char_end].
-- Copiarlo duplicaba 1948 KB (95% del texto ya presente en el padre), el
-- mismo defecto que la tabla gemela de ADR-058. Con offsets: ~78 KB.
CREATE INDEX IF NOT EXISTS idx_sections_doc   ON sections(doc_type, doc_id);
CREATE INDEX IF NOT EXISTS idx_sections_title ON sections(title);
CREATE INDEX IF NOT EXISTS idx_sections_time  ON sections(time_start);

CREATE TABLE IF NOT EXISTS checklist_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_type    TEXT NOT NULL,
    doc_id      INTEGER NOT NULL,
    ordinal     INTEGER NOT NULL,
    section     TEXT,                   -- heading al que pertenecia
    text        TEXT NOT NULL,
    done        INTEGER NOT NULL DEFAULT 0,
    UNIQUE (doc_type, doc_id, ordinal)
);
CREATE INDEX IF NOT EXISTS idx_checklist_doc  ON checklist_items(doc_type, doc_id);
CREATE INDEX IF NOT EXISTS idx_checklist_done ON checklist_items(done);
"""

DOC_COLUMNS = ("doc_kind", "session_key", "session_id", "source")


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024:
            return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} TB"


def load_parser():
    spec = importlib.util.spec_from_file_location("content_parse", WS / "scripts" / "content-parse.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ensure_columns(conn, dry_run):
    """Agrega las columnas de metadatos si faltan. Idempotente."""
    have = {r[1] for r in conn.execute("PRAGMA table_info(daily_notes)")}
    added = []
    for col in DOC_COLUMNS:
        if col in have:
            continue
        if not dry_run:
            conn.execute(f"ALTER TABLE daily_notes ADD COLUMN {col} TEXT")
        added.append(col)
    if added and not dry_run:
        conn.commit()
    return added


def migrate(conn, cp, dry_run):
    out = []

    added = ensure_columns(conn, dry_run)
    if added:
        out.append(f"  daily_notes: columnas agregadas -> {', '.join(added)}")
    else:
        out.append("  daily_notes: columnas de metadatos ya presentes")

    # --- 1. Metadatos + correccion de `type` ------------------------------
    rows = conn.execute("select id, type, content from daily_notes").fetchall()
    fixed_type = {k: 0 for k in ("harness", "daily")}
    updates = []
    for rid, old_type, content in rows:
        kind = cp.doc_kind(content)
        hf = cp.harness_fields(content)
        # `type` refleja el contenido, no lo que se anoto al cargar.
        new_type = "session" if kind == "harness" else "daily"
        if new_type != old_type:
            fixed_type[kind] += 1
        updates.append((kind, hf["session_key"], hf["session_id"], hf["source"], new_type, rid))

    if not dry_run:
        conn.executemany(
            """UPDATE daily_notes SET doc_kind=?, session_key=?, session_id=?, source=?, type=?
               WHERE id=?""",
            updates,
        )
        conn.commit()

    n_harness = sum(1 for r in rows if cp.doc_kind(r[2]) == "harness")
    out.append(
        f"  metadatos: {n_harness} dumps del harness anotados (session_key/session_id/source); "
        f"type corregido en {sum(fixed_type.values())} filas que decian el tipo equivocado"
    )

    # --- 2. Secciones ------------------------------------------------------
    docs = [("daily", i, t) for i, t in conn.execute("select id, content from daily_notes")]
    docs += [("session", i, t) for i, t in conn.execute("select id, content_bare from sessions_relacional")]

    sec_rows = []
    for dtype, did, text in docs:
        for n, s in enumerate(cp.split_sections(text)):
            sec_rows.append(
                (
                    dtype,
                    did,
                    n,
                    s["level"],
                    s["title"],
                    s["char_start"],
                    s["char_end"],
                    s["time_start"],
                    s["time_end"],
                )
            )

    if not dry_run:
        conn.execute("DELETE FROM sections")
        conn.executemany(
            """INSERT OR REPLACE INTO sections
               (doc_type, doc_id, ordinal, level, title, char_start, char_end, time_start, time_end)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            sec_rows,
        )
        conn.commit()

    con_hora = sum(1 for r in sec_rows if r[7])
    titulos = len({r[4] for r in sec_rows})
    out.append(
        f"  sections: {len(sec_rows)} secciones de {len(docs)} docs "
        f"({titulos} titulos distintos, {con_hora} con rango horario parseado). "
        "El body no se copia: se reconstruye con content[char_start:char_end]"
    )

    # --- 3. Checklist ------------------------------------------------------
    item_rows = []
    for dtype, did, text in docs:
        for n, it in enumerate(cp.extract_checklist(text)):
            item_rows.append((dtype, did, n, it["section"], it["text"], it["done"]))

    if not dry_run:
        conn.execute("DELETE FROM checklist_items")
        conn.executemany(
            """INSERT OR REPLACE INTO checklist_items
               (doc_type, doc_id, ordinal, section, text, done)
               VALUES (?,?,?,?,?,?)""",
            item_rows,
        )
        conn.commit()

    abiertos = sum(1 for r in item_rows if not r[5])
    out.append(
        f"  checklist_items: {len(item_rows)} items rescatados "
        f"({abiertos} abiertos, {len(item_rows) - abiertos} hechos) que antes solo existian dentro del texto"
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

    # Cada seccion debe apuntar a un documento existente.
    huerfanas = c.execute(
        """SELECT count(*) FROM sections s
           WHERE (s.doc_type='daily'   AND NOT EXISTS (SELECT 1 FROM daily_notes d WHERE d.id=s.doc_id))
              OR (s.doc_type='session' AND NOT EXISTS (SELECT 1 FROM sessions_relacional r WHERE r.id=s.doc_id))"""
    ).fetchone()[0]
    print(f"  secciones huerfanas: {huerfanas} {'OK' if huerfanas == 0 else '!!'}")
    if huerfanas:
        bad += 1

    n_sin_kind = c.execute("SELECT count(*) FROM daily_notes WHERE doc_kind IS NULL").fetchone()[0]
    print(f"  docs sin doc_kind: {n_sin_kind} {'OK' if n_sin_kind == 0 else '!!'}")
    if n_sin_kind:
        bad += 1

    # Los offsets deben reconstruir un body no vacio en TODAS las secciones.
    vacias = 0
    for dtype, did, cs, ce in c.execute("SELECT doc_type, doc_id, char_start, char_end FROM sections"):
        table = "daily_notes" if dtype == "daily" else "sessions_relacional"
        col = "content" if dtype == "daily" else "content_bare"
        row = c.execute(f"SELECT {col} FROM {table} WHERE id=?", (did,)).fetchone()
        if not row or not row[0][cs:ce].strip():
            vacias += 1
    print(f"  secciones con offset invalido: {vacias} {'OK' if vacias == 0 else '!!'}")
    if vacias:
        bad += 1

    fuera = c.execute(
        """SELECT count(*) FROM sections s
           WHERE s.char_start > s.char_end OR s.char_start < 0"""
    ).fetchone()[0]
    print(f"  offsets invertidos o negativos: {fuera} {'OK' if fuera == 0 else '!!'}")
    if fuera:
        bad += 1

    # El `type` debe coincidir con el doc_kind recalculado.
    m = c.execute(
        """SELECT count(*) FROM daily_notes
           WHERE (doc_kind='harness' AND type!='session')
              OR (doc_kind='daily'   AND type!='daily')"""
    ).fetchone()[0]
    print(f"  type coherente con el contenido: {m} incoherencias {'OK' if m == 0 else '!!'}")
    if m:
        bad += 1

    for t in ("sections", "checklist_items"):
        print(f"  {t}: {c.execute(f'SELECT count(*) FROM {t}').fetchone()[0]} filas")

    # El contenido original NO se toco: la migracion es aditiva.
    n = c.execute("SELECT count(*) FROM daily_notes WHERE content IS NULL OR TRIM(content)=''").fetchone()[0]
    print(f"  docs con content vacio: {n} {'OK' if n == 0 else '!!'}")
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

    cp = load_parser()

    if not args.dry_run:
        backup = DB.with_suffix(".db.pre-content")
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
        for line in migrate(conn, cp, args.dry_run):
            print(line)

        if not args.dry_run:
            print("VACUUM...")
            try:
                conn.execute("VACUUM")
                conn.commit()
            except sqlite3.OperationalError as exc:
                print(f"  SALTADO: {exc}")

        bad = verify(conn) if not args.dry_run else 0
    finally:
        conn.close()

    print(f"\nTamano: {human(size_before)} -> {human(DB.stat().st_size)}")
    if args.dry_run:
        print("(dry-run: nada se escribio)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
