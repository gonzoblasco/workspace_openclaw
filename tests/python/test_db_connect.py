"""Tests for scripts/db-connect.py - la apertura con el indice adjunto (ADR-108).

Por que importa (2026-11-04): el indice vectorial se separo a `memory/vectors.db`,
local y no versionado. El dato crudo queda en `memory.db`. Los scripts que tocan
vectores abren con ATTACH.

La regla que estos tests fijan es la del ADR: **sin indice, la busqueda FALLA**. No
abre la DB sin `idx`, no devuelve una conexion a medias y no deja una busqueda vacia
que se confunda con "no hay resultados". El 2026-11-04 dos chequeos del repo
reportaron verde midiendo nada; este test existe para que no vuelva a pasar con la
memoria.
"""
import importlib.util
import os
import sqlite3
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dbc():
    return load("db_connect", "scripts/db-connect.py")


def _make_db(tmpdir, with_vectors=True):
    """Crea un memory.db minimo y, opcionalmente, su vectors.db hermano."""
    db = os.path.join(tmpdir, "memory.db")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE sections (id INTEGER PRIMARY KEY, title TEXT)")
    c.execute("INSERT INTO sections (title) VALUES ('una seccion')")
    c.commit()
    c.close()

    if with_vectors:
        v = os.path.join(tmpdir, "vectors.db")
        c = sqlite3.connect(v)
        c.execute("CREATE TABLE section_vectors (id INTEGER PRIMARY KEY, section_id INTEGER, query_vector BLOB)")
        c.execute("INSERT INTO section_vectors (section_id, query_vector) VALUES (1, x'00')")
        c.commit()
        c.close()
    return db


def test_vectors_path_es_hermano_de_memory_db():
    m = dbc()
    assert m.vectors_path("/tmp/x/memory.db") == "/tmp/x/vectors.db"


def test_vectors_path_respeta_override():
    m = dbc()
    os.environ["MEMORY_VECTORS_DB"] = "/tmp/otro.db"
    try:
        assert m.vectors_path("/tmp/x/memory.db") == "/tmp/otro.db"
    finally:
        del os.environ["MEMORY_VECTORS_DB"]


def test_sin_indice_falla_en_vez_de_abrir():
    """La regla del ADR: sin vectors.db no hay conexion, hay error."""
    with tempfile.TemporaryDirectory() as tmp:
        db = _make_db(tmp, with_vectors=False)
        os.environ.pop("MEMORY_VECTORS_DB", None)
        m = dbc()
        try:
            m.connect(db)
        except SystemExit as exc:
            assert "indice vectorial" in str(exc)
            assert "memory-reembed" in str(exc)
            return
        raise AssertionError("connect() abrio sin indice: deberia fallar (ADR-108)")


def test_con_indice_adjunta_el_esquema_idx():
    with tempfile.TemporaryDirectory() as tmp:
        db = _make_db(tmp)
        os.environ.pop("MEMORY_VECTORS_DB", None)
        m = dbc()
        conn = m.connect(db)
        try:
            esquemas = [r[1] for r in conn.execute("PRAGMA database_list")]
            assert "idx" in esquemas, f"idx no adjunto: {esquemas}"
            n = conn.execute("SELECT count(*) FROM idx.section_vectors").fetchone()[0]
            assert n == 1
        finally:
            conn.close()


def test_require_vectors_false_abre_sin_indice():
    """Los scripts que no tocan vectores pueden abrir sin el."""
    with tempfile.TemporaryDirectory() as tmp:
        db = _make_db(tmp, with_vectors=False)
        os.environ.pop("MEMORY_VECTORS_DB", None)
        m = dbc()
        conn = m.connect(db, require_vectors=False)
        try:
            assert conn.execute("SELECT count(*) FROM sections").fetchone()[0] == 1
            esquemas = [r[1] for r in conn.execute("PRAGMA database_list")]
            assert "idx" not in esquemas
        finally:
            conn.close()


def test_indice_vacio_no_se_confunde_con_indice_ausente():
    """Un vectors.db existente pero sin filas es un indice valido y vacio."""
    with tempfile.TemporaryDirectory() as tmp:
        db = _make_db(tmp)
        v = os.path.join(tmp, "vectors.db")
        c = sqlite3.connect(v)
        c.execute("DELETE FROM section_vectors")
        c.commit()
        c.close()
        os.environ.pop("MEMORY_VECTORS_DB", None)
        m = dbc()
        conn = m.connect(db)
        try:
            assert conn.execute("SELECT count(*) FROM idx.section_vectors").fetchone()[0] == 0
        finally:
            conn.close()
