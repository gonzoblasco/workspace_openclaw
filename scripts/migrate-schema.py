#!/usr/bin/env python3
"""
migrate-schema.py - Refactor del schema de memory.db (2026-09-22).

Alcance (decidido por Gonzo): normalizar la taxonomia, quitar la tabla gemela,
limpiar columnas muertas y arreglar la integridad referencial.

Los 4 problemas, cada uno con su reparacion:

  1. tags: 0 de 121 cumplian el contrato "JSON array". 48 eran titulos pegados.
     -> tabla `tags` + junction `learning_tags` (N:N). Vocabulario controlado.

  2. categorias: `learnings.category` (7 valores, conjunto cerrado) y
     `topics.category` (prosa libre) son DOS EJES distintos con el mismo nombre.
     -> tabla `categories` con columna `kind` que los distingue.

  3. learnings_enriquecido: tabla gemela con el 94% del texto duplicado.
     -> se absorbe en `learnings` (agrega learning_vector) y se elimina.

  4. 20 violaciones de FK, que resultaron ser TRES cosas distintas:
     a) learnings_enriquecido.id -> learnings.id (9): FK real, faltan los padres.
        -> promover los 9 hijos a `learnings`.
     b) topic_sessions.session_id -> sessions_relacional (7): FK real, apuntan a
        la sesion 73 que nunca se catalogo. -> quitar los vinculos colgados.
     c) sessions_relacional.id -> daily_notes.id (4): **FK ESPURIA**. Verificado:
        de 47 vinculos que resuelven, 0 comparten fecha. Los escritores pasan
        id=None (AUTOINCREMENT) y las dos secuencias coinciden por numeracion.
        -> QUITAR la FK. No hay nada que arreglar en los datos.

Uso:
    migrate-schema.py --dry-run
    migrate-schema.py [--db <path>]
"""
import argparse
import re
import shutil
import sqlite3
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
DB = WS / "memory" / "memory.db"

VALID_TAG = re.compile(r"^[a-z0-9][a-z0-9._-]*$")

CATEGORY_KINDS = ("learning", "topic")


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024:
            return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} TB"


# --------------------------------------------------------------------------
# 1. tags: parsear lo que hay y separar tags reales de prosa
# --------------------------------------------------------------------------

def parse_tags(raw):
    """Separa una cadena de tags en (reales, prosa).

    Un tag real es un token: minuscula inicial, sin espacios, solo [a-z0-9._-].
    Lo que no cumple eso es prosa (un titulo pegado por un bug de carga).
    """
    if not raw:
        return [], []
    real, prose = [], []
    for part in raw.split(","):
        tok = part.strip()
        if not tok:
            continue
        if VALID_TAG.match(tok):
            real.append(tok)
        else:
            prose.append(tok)
    return real, prose


# --------------------------------------------------------------------------
# 2. La migracion
# --------------------------------------------------------------------------

def migrate(conn, dry_run):
    out = []
    c = conn.cursor()

    # --- 3c. Rebuild de sessions_relacional SIN la FK espuria ---------------
    # SQLite no permite ALTER ... DROP CONSTRAINT: hay que reconstruir la tabla.
    fk_sql = c.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='sessions_relacional'"
    ).fetchone()[0]
    if "REFERENCES daily_notes" in fk_sql:
        new_sql = """CREATE TABLE sessions_relacional_new (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL,
  title TEXT NOT NULL,
  tags TEXT,
  complexity_score INTEGER DEFAULT 0,
  model_used TEXT DEFAULT 'unknown',
  thinking_level TEXT DEFAULT 'high',
  summary TEXT,
  session_duration INTEGER DEFAULT 0,
  agent_id TEXT,
  content_bare TEXT NOT NULL,
  created_at TEXT NOT NULL
)"""
        cols = "id,date,title,tags,complexity_score,model_used,thinking_level,summary,session_duration,agent_id,content_bare,created_at"
        if not dry_run:
            c.execute(new_sql)
            c.execute(f"INSERT INTO sessions_relacional_new ({cols}) SELECT {cols} FROM sessions_relacional")
            c.execute("DROP TABLE sessions_relacional")
            c.execute("ALTER TABLE sessions_relacional_new RENAME TO sessions_relacional")
            c.execute("CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions_relacional(date)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_sessions_summary ON sessions_relacional(summary)")
            conn.commit()
        out.append(
            "  sessions_relacional: FK espuria -> daily_notes ELIMINADA (tabla reconstruida). "
            "Verificado: 0 de 47 vinculos compartian fecha. El CASCADE habria borrado "
            "sesiones sin relacion."
        )
    else:
        out.append("  sessions_relacional: sin FK espuria (ya reparada)")

    # --- 3b. topic_sessions: quitar los vinculos colgados ------------------
    dangling = c.execute(
        """SELECT ts.rowid FROM topic_sessions ts
           LEFT JOIN sessions_relacional s ON s.id = ts.session_id
           WHERE s.id IS NULL"""
    ).fetchall()
    if dangling:
        if not dry_run:
            c.execute(
                """DELETE FROM topic_sessions WHERE rowid IN (
                       SELECT ts.rowid FROM topic_sessions ts
                       LEFT JOIN sessions_relacional s ON s.id = ts.session_id
                       WHERE s.id IS NULL)"""
            )
            conn.commit()
        out.append(
            f"  topic_sessions: {len(dangling)} vinculos colgados eliminados "
            "(apuntaban a sesiones nunca catalogadas)"
        )
    else:
        out.append("  topic_sessions: sin vinculos colgados")

    # --- 3a. Promover los hijos huerfanos de learnings_enriquecido ---------
    # Guard de idempotencia: en la segunda corrida la tabla gemela ya no existe
    # (el paso 3 la absorbe), asi que consultarla a ciegas rompe la re-ejecucion.
    twin_present = c.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='learnings_enriquecido'"
    ).fetchone()
    if twin_present:
        orphans = c.execute(
            """SELECT le.id, le.category, le.title, le.content, le.tags
               FROM learnings_enriquecido le
               LEFT JOIN learnings l ON l.id = le.id
               WHERE l.id IS NULL ORDER BY le.id"""
        ).fetchall()
    else:
        orphans = []
    if orphans:
        promoted = 0
        for oid, cat, title, content, tags in orphans:
            if not dry_run:
                c.execute(
                    """INSERT OR IGNORE INTO learnings (id, category, title, content, tags)
                       VALUES (?,?,?,?,?)""",
                    (oid, cat, title, content, tags or ""),
                )
            promoted += 1
        if not dry_run:
            conn.commit()
        out.append(
            f"  learnings: {promoted} hijos huerfanos promovidos (contenido valido, ids libres)"
        )
    else:
        out.append("  learnings: sin hijos huerfanos" if twin_present else "  learnings: tabla gemela ya absorbida (nada que promover)")

    # --- 1. Normalizar tags: catalogo + junction ---------------------------
    raw_rows = c.execute(
        "SELECT id, tags FROM learnings WHERE tags IS NOT NULL AND TRIM(tags) != ''"
    ).fetchall()
    real_tags, prose_count = {}, 0
    per_learning = {}
    for lid, raw in raw_rows:
        real, prose = parse_tags(raw)
        per_learning[lid] = real
        prose_count += len(prose)
        for t in real:
            real_tags[t] = real_tags.get(t, 0) + 1

    if not dry_run:
        c.execute(
            """CREATE TABLE IF NOT EXISTS tags (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL UNIQUE,
                   created_at TEXT NOT NULL DEFAULT (datetime('now'))
               )"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS learning_tags (
                   learning_id INTEGER NOT NULL,
                   tag_id INTEGER NOT NULL,
                   PRIMARY KEY (learning_id, tag_id),
                   FOREIGN KEY(learning_id) REFERENCES learnings(id) ON DELETE CASCADE,
                   FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE
               )"""
        )
        for name in real_tags:
            c.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (name,))
        for lid, tags in per_learning.items():
            for t in tags:
                c.execute(
                    """INSERT OR IGNORE INTO learning_tags (learning_id, tag_id)
                       SELECT ?, id FROM tags WHERE name = ?""",
                    (lid, t),
                )
        conn.commit()

    out.append(
        f"  tags: {len(real_tags)} tags reales normalizados a tabla + junction. "
        f"{prose_count} valores de prosa descartados (eran titulos pegados, "
        "redundantes con learnings.title)"
    )

    # --- 2. Categorias como catalogo, distinguiendo los DOS ejes -----------
    learn_cats = [r[0] for r in c.execute("SELECT DISTINCT category FROM learnings ORDER BY category")]
    topic_cats = [
        r[0] for r in c.execute("SELECT DISTINCT category FROM topics WHERE category IS NOT NULL ORDER BY category")
    ]
    if not dry_run:
        c.execute(
            """CREATE TABLE IF NOT EXISTS categories (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   kind TEXT NOT NULL DEFAULT 'learning',
                   description TEXT,
                   UNIQUE (name, kind)
               )"""
        )
        for name in learn_cats:
            c.execute("INSERT OR IGNORE INTO categories (name, kind) VALUES (?, 'learning')", (name,))
        for name in topic_cats:
            c.execute("INSERT OR IGNORE INTO categories (name, kind) VALUES (?, 'topic')", (name,))
        conn.commit()

    out.append(
        f"  categories: {len(learn_cats)} de learnings + {len(topic_cats)} de topics, "
        "distinguidas por `kind` (antes eran dos ejes distintos con el mismo nombre)"
    )

    # --- 3. Absorber la tabla gemela en learnings --------------------------
    twin_exists = c.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='learnings_enriquecido'"
    ).fetchone()
    if twin_exists:
        before = len(c.execute("SELECT 1 FROM learnings_enriquecido").fetchall())
        if not dry_run:
            cols = [r[1] for r in c.execute("PRAGMA table_info(learnings)")]
            if "learning_vector" not in cols:
                c.execute("ALTER TABLE learnings ADD COLUMN learning_vector BLOB")
            c.execute(
                """UPDATE learnings SET learning_vector = (
                       SELECT le.learning_vector FROM learnings_enriquecido le
                       WHERE le.id = learnings.id)"""
            )
            c.execute("DROP TABLE learnings_enriquecido")
            conn.commit()
        out.append(
            f"  learnings_enriquecido: absorbida en learnings ({before} vectores movidos) "
            "y eliminada. Se va el 94% de texto duplicado."
        )
    else:
        out.append("  learnings_enriquecido: ya absorbida")

    # --- 3d. Columnas muertas ---------------------------------------------
    for table, col in (("learnings_enriquecido", "query_vector"), ("sessions_relacional", "agent_id")):
        info = [r[1] for r in c.execute(f"PRAGMA table_info({table})")]
        if col not in info:
            out.append(f"  {table}.{col}: ya no existe")
            continue
        n = c.execute(f"SELECT count({col}) FROM {table}").fetchone()[0]
        if n:
            out.append(f"  {table}.{col}: SE SALTA, tiene {n} valores")
            continue
        if not dry_run:
            c.execute(f"ALTER TABLE {table} DROP COLUMN {col}")
            conn.commit()
        out.append(f"  {table}.{col}: eliminada (siempre NULL; higiene, no espacio)")

    return out


def verify(conn, fk_before):
    print("\nVerificacion:")
    bad = 0
    c = conn.cursor()

    fk_after = set(map(tuple, c.execute("PRAGMA foreign_key_check").fetchall()))
    nuevas = fk_after - fk_before
    if nuevas:
        print(f"  FKs: !! {len(nuevas)} violaciones NUEVAS")
        for v in list(nuevas)[:5]:
            print(f"     {v}")
        bad += 1
    else:
        print(f"  FKs: OK, sin violaciones nuevas ({len(fk_before)} antes, {len(fk_after)} ahora)")

    # Integridad de la nueva taxonomia
    n_tags = c.execute("SELECT count(*) FROM tags").fetchone()[0]
    n_links = c.execute("SELECT count(*) FROM learning_tags").fetchone()[0]
    n_sin_tag = c.execute(
        """SELECT count(*) FROM learnings l
           LEFT JOIN learning_tags lt ON lt.learning_id = l.id WHERE lt.tag_id IS NULL"""
    ).fetchone()[0]
    print(f"  tags: {n_tags} tags, {n_links} vinculos, {n_sin_tag} learnings sin tag")
    dangling = c.execute(
        """SELECT count(*) FROM learning_tags lt
           LEFT JOIN learnings l ON l.id = lt.learning_id
           LEFT JOIN tags t ON t.id = lt.tag_id
           WHERE l.id IS NULL OR t.id IS NULL"""
    ).fetchone()[0]
    print(f"  learning_tags huerfanos: {dangling} {'OK' if dangling == 0 else '!!'}")
    if dangling:
        bad += 1

    n_cats = c.execute("SELECT count(*) FROM categories").fetchone()[0]
    print(f"  categories: {n_cats} ({dict(c.execute('SELECT kind, count(*) FROM categories GROUP BY kind').fetchall())})")

    # Vectores: no se deben haber perdido
    n_vec = c.execute("SELECT count(*) FROM learnings WHERE learning_vector IS NOT NULL").fetchone()[0]
    print(f"  vectores de learnings preservados: {n_vec}")

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
        backup = DB.with_suffix(".db.pre-schema")
        shutil.copy2(DB, backup)
        print(f"backup: {backup} ({human(backup.stat().st_size)})")

    size_before = DB.stat().st_size
    conn = sqlite3.connect(DB)
    try:
        fk_before = set(map(tuple, conn.execute("PRAGMA foreign_key_check").fetchall()))
        print("Migracion:" + (" (DRY-RUN)" if args.dry_run else ""))
        for line in migrate(conn, args.dry_run):
            print(line)

        if not args.dry_run:
            print("VACUUM...")
            try:
                conn.execute("VACUUM")
                conn.commit()
            except sqlite3.OperationalError as exc:
                print(f"  SALTADO: {exc}")

        bad = verify(conn, fk_before) if not args.dry_run else 0
    finally:
        conn.close()

    size_after = DB.stat().st_size
    print(f"\nTamano: {human(size_before)} -> {human(size_after)}")
    if args.dry_run:
        print("(dry-run: nada se escribio)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
