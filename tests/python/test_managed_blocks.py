"""Tests for scripts/managed-blocks.py (settings -> managed blocks propagation).

The mechanism rewrites ONLY the content between MANAGED markers. The critical
properties: idempotence, that text outside markers is never touched, and that a
missing marker block is reported instead of guessed.
"""
import importlib.util
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = ROOT / "scripts" / "managed-blocks.py"


def load(tmp_path):
    """Carga el modulo y lo apunta a un workspace temporal con su propia DB."""
    spec = importlib.util.spec_from_file_location("managed_blocks", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    ws = tmp_path / "ws"
    (ws / "docs").mkdir(parents=True)
    (ws / "memory").mkdir(parents=True)
    db = ws / "memory" / "memory.db"
    conn = sqlite3.connect(db)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY, value TEXT NOT NULL,
            description TEXT, updated_at TEXT)"""
    )
    conn.commit()
    conn.close()

    mod.WORKSPACE = ws
    mod.DB_PATH = db
    return mod, ws


def write_block(ws, rel, key, inner):
    p = ws / rel
    p.write_text(
        f"antes\n\n{mod_begin(key)}\n{inner}\n{mod_end(key)}\n\ndespues\n",
        encoding="utf-8",
    )
    return p


def mod_begin(key):
    return f"<!-- BEGIN MANAGED:{key} -->"


def mod_end(key):
    return f"<!-- END MANAGED:{key} -->"


def seed(mod):
    conn = mod.db()
    mod.cmd_seed(conn, None)
    conn.close()


def test_seed_inserts_defaults(tmp_path):
    mod, _ = load(tmp_path)
    seed(mod)
    conn = mod.db()
    got = mod.get_settings(conn)
    conn.close()
    assert got["model_primary"] == "deepseek-v4.1-flash:cloud"
    assert got["thinking_default"] == "off"


def test_seed_is_idempotent(tmp_path):
    mod, _ = load(tmp_path)
    seed(mod)
    conn = mod.db()
    mod.cmd_seed(conn, None)  # segunda vez
    n = conn.execute("SELECT count(*) FROM settings").fetchone()[0]
    conn.close()
    assert n == len(mod.DEFAULTS)


def test_apply_rewrites_only_between_markers(tmp_path):
    mod, ws = load(tmp_path)
    seed(mod)
    # El bloque de modelos de AGENTS.md es `model-operativo` (consume
    # model_by_agent + model_primary + pipeline A/B); `model-triple` vive en
    # docs/SETUP.md desde 2026-10-06 (dac9961410).
    p = write_block(ws, "AGENTS.md", "model-operativo", "contenido viejo")
    conn = mod.db()
    mod.run_all(conn, dry_run=False)
    conn.close()
    text = p.read_text(encoding="utf-8")
    assert "contenido viejo" not in text
    assert "deepseek-v4.1-flash:cloud" in text
    # El texto de afuera queda intacto
    assert text.startswith("antes\n\n")
    assert text.endswith("\ndespues\n")


def test_apply_is_idempotent(tmp_path):
    mod, ws = load(tmp_path)
    seed(mod)
    p = write_block(ws, "AGENTS.md", "model-operativo", "viejo")
    conn = mod.db()
    mod.run_all(conn, dry_run=False)
    first = p.read_text(encoding="utf-8")
    mod.run_all(conn, dry_run=False)
    second = p.read_text(encoding="utf-8")
    conn.close()
    assert first == second


def test_dry_run_does_not_write(tmp_path):
    mod, ws = load(tmp_path)
    seed(mod)
    p = write_block(ws, "AGENTS.md", "model-operativo", "viejo")
    before = p.read_text(encoding="utf-8")
    conn = mod.db()
    mod.run_all(conn, dry_run=True)
    conn.close()
    assert p.read_text(encoding="utf-8") == before


def test_missing_markers_are_reported_not_guessed(tmp_path):
    """Sin marcadores, el archivo NO se toca y se reporta el snippet exacto."""
    mod, ws = load(tmp_path)
    seed(mod)
    p = ws / "AGENTS.md"
    original = "# sin marcadores\n\ntexto\n"
    p.write_text(original, encoding="utf-8")
    conn = mod.db()
    out = "\n".join(mod.run_all(conn, dry_run=False))
    conn.close()
    assert p.read_text(encoding="utf-8") == original  # intacto
    assert "faltan los marcadores" in out
    assert mod_begin("model-operativo") in out  # el snippet a pegar


def test_set_updates_value(tmp_path):
    mod, _ = load(tmp_path)
    seed(mod)
    conn = mod.db()
    class A:
        key, value = "thinking_default", "max"
    mod.cmd_set(conn, A())
    assert mod.get_settings(conn)["thinking_default"] == "max"
    conn.close()


def test_change_propagates_to_block(tmp_path):
    """El caso central: cambiar un setting cambia el bloque en el archivo."""
    mod, ws = load(tmp_path)
    seed(mod)
    p = write_block(ws, "AGENTS.md", "model-operativo", "viejo")
    conn = mod.db()
    mod.run_all(conn, dry_run=False)
    class A:
        # El bloque model-operativo de AGENTS.md se arma con {model_by_agent}
        # (2026-10-05, ADR-087), no con {model_primary}: mutar un setting que el
        # bloque ya no usa no lo mueve.
        key, value = "model_by_agent", "modelo-nuevo:cloud"
    mod.cmd_set(conn, A())
    mod.run_all(conn, dry_run=False)
    conn.close()
    assert "modelo-nuevo:cloud" in p.read_text(encoding="utf-8")


def test_missing_file_is_reported(tmp_path):
    mod, _ = load(tmp_path)
    seed(mod)
    conn = mod.db()
    out = "\n".join(mod.run_all(conn, dry_run=False))
    conn.close()
    assert "no existe" in out
