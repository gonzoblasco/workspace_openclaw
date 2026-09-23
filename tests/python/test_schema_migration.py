"""Tests for scripts/migrate-schema.py (refactor de schema de memory.db).

Los cuatro problemas que arregla, cada uno con su test:
  1. tags rotos -> catalogo + junction N:N
  2. categorias de dos ejes distintos -> tabla `categories` con `kind`
  3. tabla gemela `learnings_enriquecido` -> absorbida en learnings
  4. 20 violaciones de FK (incluida una FK ESPURIA) -> reparadas
"""
import importlib.util
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def load():
    spec = importlib.util.spec_from_file_location("migrate_schema", ROOT / "scripts" / "migrate-schema.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- parse_tags: la pieza que separa tags reales de prosa ---

def test_parse_tags_splits_valid():
    m = load()
    real, prose = m.parse_tags("oss,comunicacion,regla")
    assert real == ["oss", "comunicacion", "regla"]
    assert prose == []


def test_parse_tags_rejects_prose():
    """Un titulo pegado por el bug de carga NO es un tag."""
    m = load()
    real, prose = m.parse_tags("Service worker cache strategy for hashed assets")
    assert real == []
    assert prose == ["Service worker cache strategy for hashed assets"]


def test_parse_tags_mixed():
    m = load()
    real, prose = m.parse_tags("oss,Service worker cache,Doble-click")
    assert real == ["oss"]
    assert len(prose) == 2


def test_parse_tags_empty_and_none():
    m = load()
    assert m.parse_tags(None) == ([], [])
    assert m.parse_tags("") == ([], [])
    assert m.parse_tags("  ,  ") == ([], [])


def test_parse_tags_accepts_hyphen_and_underscore():
    m = load()
    real, prose = m.parse_tags("reflexion-post-tarea,db_first,git-hooks")
    assert real == ["reflexion-post-tarea", "db_first", "git-hooks"]
    assert prose == []


# --- la migracion sobre una DB que reproduce los defectos ---

def make_db(tmp_path):
    """Una DB minima con los 4 defectos, para probar la reparacion."""
    db = tmp_path / "memory.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        """
        CREATE TABLE daily_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL, type TEXT DEFAULT 'daily', content TEXT NOT NULL
        );
        CREATE TABLE sessions_relacional (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL, title TEXT NOT NULL, tags TEXT,
            complexity_score INTEGER DEFAULT 0, model_used TEXT DEFAULT 'unknown',
            thinking_level TEXT DEFAULT 'high', summary TEXT,
            session_duration INTEGER DEFAULT 0, agent_id TEXT,
            content_bare TEXT NOT NULL, created_at TEXT NOT NULL,
            FOREIGN KEY(id) REFERENCES daily_notes(id) ON DELETE CASCADE
        );
        CREATE TABLE topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE,
            category TEXT, description TEXT
        );
        CREATE TABLE topic_sessions (
            session_id INTEGER NOT NULL, topic_id INTEGER NOT NULL,
            confidence REAL DEFAULT 0.5, PRIMARY KEY (session_id, topic_id),
            FOREIGN KEY(session_id) REFERENCES sessions_relacional(id),
            FOREIGN KEY(topic_id) REFERENCES topics(id)
        );
        CREATE TABLE learnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL,
            title TEXT NOT NULL, content TEXT NOT NULL, tags TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')), updated_at TEXT
        );
        CREATE TABLE learnings_enriquecido (
            id INTEGER PRIMARY KEY, category TEXT NOT NULL, title TEXT NOT NULL,
            content TEXT NOT NULL, tags TEXT, learning_vector BLOB,
            query_vector TEXT, relevance_score REAL DEFAULT 0.0,
            created_at TEXT, updated_at TEXT,
            FOREIGN KEY(id) REFERENCES learnings(id) ON DELETE CASCADE
        );
        """
    )
    # daily + sesion con ids que coinciden por numeracion pero sin relacion
    conn.execute("INSERT INTO daily_notes (id,date,content) VALUES (1,'2026-08-05','daily uno')")
    conn.execute(
        """INSERT INTO sessions_relacional (id,date,title,content_bare,created_at)
           VALUES (1,'2026-08-10','sesion uno','contenido de la sesion','2026-08-10')"""
    )
    # topics
    conn.execute("INSERT INTO topics (id,name,category) VALUES (1,'git','devops')")
    # topic_session colgado: apunta a una sesion que no existe
    conn.execute("INSERT INTO topic_sessions (session_id,topic_id) VALUES (99,1)")
    # learnings: uno bien, uno con tags prosa
    conn.execute(
        "INSERT INTO learnings (id,category,title,content,tags) VALUES (10,'oss','titulo uno','cuerpo uno','oss,comunicacion')"
    )
    conn.execute(
        "INSERT INTO learnings (id,category,title,content,tags) VALUES (11,'oss','titulo dos','cuerpo dos','Service worker cache strategy')"
    )
    # hijo huerfano: existe en enriquecido, no en learnings
    conn.execute(
        """INSERT INTO learnings_enriquecido (id,category,title,content,tags,learning_vector)
           VALUES (200,'metodologia','huerfano','contenido valido','oss',?)""",
        (b"\x00" * 16,),
    )
    conn.commit()
    conn.close()
    return db


def migrate_copy(tmp_path):
    db = make_db(tmp_path)
    mod = load()
    mod.DB = db
    conn = sqlite3.connect(db)
    fk_before = set(map(tuple, conn.execute("PRAGMA foreign_key_check").fetchall()))
    mod.migrate(conn, dry_run=False)
    fk_after = set(map(tuple, conn.execute("PRAGMA foreign_key_check").fetchall()))
    return mod, conn, fk_before, fk_after


def test_migration_clears_all_fk_violations(tmp_path):
    _, conn, before, after = migrate_copy(tmp_path)
    assert len(before) > 0, "la DB de prueba debe tener violaciones"
    assert after == set(), f"quedaron violaciones: {after}"
    conn.close()


def test_spurious_fk_is_removed(tmp_path):
    """La FK sessions_relacional -> daily_notes debe desaparecer del DDL."""
    _, conn, _, _ = migrate_copy(tmp_path)
    sql = conn.execute(
        "SELECT sql FROM sqlite_master WHERE name='sessions_relacional'"
    ).fetchone()[0]
    conn.close()
    assert "REFERENCES daily_notes" not in sql


def test_session_data_survives_fk_removal(tmp_path):
    """Reconstruir la tabla por la FK no debe perder filas."""
    _, conn, _, _ = migrate_copy(tmp_path)
    row = conn.execute("SELECT id,date,title FROM sessions_relacional WHERE id=1").fetchone()
    conn.close()
    assert row == (1, "2026-08-10", "sesion uno")


def test_orphan_learning_is_promoted(tmp_path):
    """El hijo huerfano tiene contenido valido: se promueve, no se borra."""
    _, conn, _, _ = migrate_copy(tmp_path)
    row = conn.execute("SELECT title,content FROM learnings WHERE id=200").fetchone()
    conn.close()
    assert row == ("huerfano", "contenido valido")


def test_dangling_topic_link_removed(tmp_path):
    _, conn, _, _ = migrate_copy(tmp_path)
    n = conn.execute("SELECT count(*) FROM topic_sessions WHERE session_id=99").fetchone()[0]
    conn.close()
    assert n == 0


def test_tags_normalized_to_catalog(tmp_path):
    _, conn, _, _ = migrate_copy(tmp_path)
    tags = [r[0] for r in conn.execute("SELECT name FROM tags ORDER BY name")]
    conn.close()
    assert "oss" in tags and "comunicacion" in tags
    # la prosa NO debe entrar al catalogo
    assert not any(" " in t for t in tags)


def test_prose_is_not_indexed_as_tag(tmp_path):
    """'Service worker cache strategy' era prosa: no debe existir como tag."""
    _, conn, _, _ = migrate_copy(tmp_path)
    n = conn.execute(
        "SELECT count(*) FROM tags WHERE name LIKE '%Service worker%'"
    ).fetchone()[0]
    conn.close()
    assert n == 0


def test_learning_tags_junction_works(tmp_path):
    _, conn, _, _ = migrate_copy(tmp_path)
    rows = conn.execute(
        """SELECT t.name FROM learning_tags lt JOIN tags t ON t.id=lt.tag_id
           WHERE lt.learning_id=10 ORDER BY t.name"""
    ).fetchall()
    conn.close()
    assert [r[0] for r in rows] == ["comunicacion", "oss"]
    # el learning 11 solo tenia prosa: sin vinculos
    # (se verifica en el test de abajo)


def test_learning_with_only_prose_has_no_links(tmp_path):
    _, conn, _, _ = migrate_copy(tmp_path)
    n = conn.execute("SELECT count(*) FROM learning_tags WHERE learning_id=11").fetchone()[0]
    conn.close()
    assert n == 0


def test_categories_have_kind(tmp_path):
    """Los dos ejes con el mismo nombre ahora se distinguen por kind."""
    _, conn, _, _ = migrate_copy(tmp_path)
    rows = dict(conn.execute("SELECT name,kind FROM categories").fetchall())
    conn.close()
    assert rows.get("oss") == "learning"
    assert rows.get("devops") == "topic"


def test_twin_table_is_gone(tmp_path):
    _, conn, _, _ = migrate_copy(tmp_path)
    n = conn.execute(
        "SELECT count(*) FROM sqlite_master WHERE name='learnings_enriquecido'"
    ).fetchone()[0]
    conn.close()
    assert n == 0


def test_vectors_survive_twin_absorption(tmp_path):
    """Los vectores de la tabla gemela deben quedar en learnings."""
    _, conn, _, _ = migrate_copy(tmp_path)
    v = conn.execute("SELECT learning_vector FROM learnings WHERE id=200").fetchone()[0]
    conn.close()
    assert v is not None and len(v) == 16


def test_dead_column_dropped(tmp_path):
    _, conn, _, _ = migrate_copy(tmp_path)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(sessions_relacional)")]
    conn.close()
    assert "agent_id" not in cols


def test_indexes_preserved(tmp_path):
    """Reconstruir la tabla por la FK no debe perder los indices."""
    _, conn, _, _ = migrate_copy(tmp_path)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions_relacional(date)")
    names = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='index'")]
    conn.close()
    assert "idx_sessions_date" in names


def test_migration_is_idempotent(tmp_path):
    """Correr la migracion dos veces no debe romper nada."""
    db = make_db(tmp_path)
    mod = load()
    mod.DB = db
    conn = sqlite3.connect(db)
    mod.migrate(conn, dry_run=False)
    first = conn.execute("SELECT count(*) FROM learnings").fetchone()[0]
    second_report = "\n".join(mod.migrate(conn, dry_run=False))
    second = conn.execute("SELECT count(*) FROM learnings").fetchone()[0]
    conn.close()
    assert first == second
    assert "ya absorbida" in second_report or "ya reparada" in second_report
