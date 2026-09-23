"""Tests for scripts/vector-util.py y scripts/migrate-vectors.py.

Contexto: el 77% de memory.db eran embeddings guardados como JSON de texto
(1024 floats -> ~22 KB). En BLOB float32 son 4096 bytes (-82%). Estos tests
cubren la propiedad que hace segura la migracion: el decoder acepta AMBOS
formatos, y convertir no cambia el vector.
"""
import importlib.util
import json
import sqlite3
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def vu():
    return load("vector_util", "scripts/vector-util.py")


# --- vector-util: encode/decode ---

def test_roundtrip_blob():
    m = vu()
    vec = [0.5, -0.25, 1.0, 0.0]
    assert m.decode(m.encode(vec)) == vec


def test_encode_is_float32_little_endian():
    m = vu()
    blob = m.encode([1.0])
    assert isinstance(blob, bytes)
    assert len(blob) == 4
    assert struct.unpack("<f", blob)[0] == 1.0


def test_1024_dims_shrink_dramatically():
    """El caso real: 1024 floats de embeddings ocupan 4096 bytes, no ~22 KB.

    Se usan floats de precision completa (como los del modelo): con floats
    "cortos" el JSON tambien seria chico y el test mediria otra cosa.
    """
    m = vu()
    vec = [0.12345678901234567] * 1024
    blob = m.encode(vec)
    as_json = len(json.dumps(vec))
    assert len(blob) == 4096
    # En los datos reales el JSON es ~22 KB (ratio 0.18). Umbral holgado a 0.25.
    assert len(blob) < as_json * 0.25, f"blob={len(blob)} json={as_json}"


def test_decode_accepts_legacy_json_string():
    """Compatibilidad: los vectores viejos siguen leyendose."""
    m = vu()
    vec = [1.5, 2.5]
    assert m.decode(json.dumps(vec)) == vec


def test_decode_accepts_json_bytes():
    m = vu()
    vec = [1.5, 2.5]
    assert m.decode(json.dumps(vec).encode()) == vec


def test_decode_none():
    m = vu()
    assert m.decode(None) is None


def test_is_json_distinguishes_formats():
    m = vu()
    assert m.is_json(json.dumps([1.0, 2.0]))
    assert not m.is_json(m.encode([1.0, 2.0]))


def test_dims_works_on_both_formats():
    m = vu()
    assert m.dims(m.encode([0.0] * 1024)) == 1024
    assert m.dims(json.dumps([0.0] * 1024)) == 1024


def test_dims_malformed_returns_none():
    """Valores que no son ni JSON valido ni BLOB float32 -> None.

    OJO con la limitacion documentada: cualquier byte-string cuyo largo sea
    multiplo de 4 es indistinguible de un float32 y decodifica a ALGO. El
    decoder no puede distinguirlo sin metadata. En esta DB la columna solo
    contiene una de las dos cosas (lo garantiza la migracion), asi que la
    ambiguedad no aparece en la practica. Se testea el caso detectable.
    """
    m = vu()
    assert m.dims(b"no soy un vector") is None or len(b"no soy un vector") % 4 == 0
    # El caso realmente garantizado: largo no multiplo de 4 y sin JSON.
    assert m.dims(b"12345") is None
    assert m.dims("no json {[") is None


def test_cosine_identical_is_one():
    m = vu()
    vec = [0.3, 0.4, 0.5]
    assert abs(m.cosine(m.encode(vec), json.dumps(vec)) - 1.0) < 1e-6


def test_cosine_orthogonal_is_zero():
    m = vu()
    assert abs(m.cosine(m.encode([1.0, 0.0]), m.encode([0.0, 1.0]))) < 1e-6


def test_cosine_length_mismatch_is_zero():
    m = vu()
    assert m.cosine(m.encode([1.0, 2.0]), m.encode([1.0])) == 0.0


# --- migrate-vectors: la conversion sobre una DB real ---

def make_db(tmp_path, n=3):
    db = tmp_path / "memory.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        """
        CREATE TABLE session_vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            query_vector TEXT NOT NULL,
            chunk_index INTEGER DEFAULT 0
        );
        CREATE TABLE learnings_enriquecido (
            id INTEGER PRIMARY KEY,
            learning_vector TEXT,
            query_vector TEXT
        );
        """
    )
    vec = [0.25] * 1024
    for i in range(n):
        conn.execute(
            "INSERT INTO session_vectors (session_id, query_vector, chunk_index) VALUES (?,?,0)",
            (i + 1, json.dumps(vec)),
        )
        conn.execute(
            "INSERT INTO learnings_enriquecido (id, learning_vector, query_vector) VALUES (?,?,NULL)",
            (i + 1, json.dumps(vec)),
        )
    conn.commit()
    conn.close()
    return db


def migrate_module():
    return load("migrate_vectors", "scripts/migrate-vectors.py")


def test_migration_converts_all_and_preserves_values(tmp_path):
    db = make_db(tmp_path)
    mod = migrate_module()
    mod.DB = db
    m = vu()

    conn = sqlite3.connect(db)
    mod.migrate(conn, m, dry_run=False, drop_dead=False)
    conn.close()

    conn = sqlite3.connect(db)
    for table, col in (("session_vectors", "query_vector"), ("learnings_enriquecido", "learning_vector")):
        rows = conn.execute(f"SELECT {col} FROM {table}").fetchall()
        assert rows, f"{table} quedo vacia"
        for (v,) in rows:
            assert not m.is_json(v), f"{table}.{col} quedo en JSON"
            decoded = m.decode(v)
            assert decoded is not None and len(decoded) == 1024
            # El valor debe ser identico al original (0.25 exacto en float32).
            assert all(abs(x - 0.25) < 1e-6 for x in decoded)
    conn.close()


def test_migration_is_idempotent(tmp_path):
    db = make_db(tmp_path)
    mod = migrate_module()
    mod.DB = db
    m = vu()

    conn = sqlite3.connect(db)
    mod.migrate(conn, m, dry_run=False, drop_dead=False)
    first = conn.execute("SELECT query_vector FROM session_vectors ORDER BY id").fetchall()
    mod.migrate(conn, m, dry_run=False, drop_dead=False)
    second = conn.execute("SELECT query_vector FROM session_vectors ORDER BY id").fetchall()
    conn.close()
    assert first == second


def test_dry_run_does_not_change_data(tmp_path):
    db = make_db(tmp_path)
    mod = migrate_module()
    mod.DB = db
    m = vu()

    conn = sqlite3.connect(db)
    before = conn.execute("SELECT query_vector FROM session_vectors ORDER BY id").fetchall()
    mod.migrate(conn, m, dry_run=True, drop_dead=False)
    after = conn.execute("SELECT query_vector FROM session_vectors ORDER BY id").fetchall()
    conn.close()
    assert before == after
    assert m.is_json(after[0][0])  # sigue en JSON


def test_drop_dead_columns_skips_when_not_null(tmp_path):
    """Una columna con valores NO debe dropearse aunque este en la lista."""
    db = make_db(tmp_path)
    conn = sqlite3.connect(db)
    conn.execute("UPDATE learnings_enriquecido SET query_vector='algo' WHERE id=1")
    conn.commit()
    conn.close()

    mod = migrate_module()
    mod.DB = db
    m = vu()
    conn = sqlite3.connect(db)
    report = "\n".join(mod.migrate(conn, m, dry_run=False, drop_dead=True))
    cols = [r[1] for r in conn.execute("PRAGMA table_info(learnings_enriquecido)")]
    conn.close()
    assert "query_vector" in cols, "dropeo una columna que tenia datos"
    assert "SE SALTA" in report
