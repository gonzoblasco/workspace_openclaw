"""Tests para scripts/memory-end-session.py (idempotencia del cierre, B7/B9).

Contexto (2026-10-12): el append del cierre deduplicaba por el TITULO
("## Session End - <proyecto>"). Consecuencia: dos sesiones DISTINTAS del mismo
proyecto el mismo dia -> la segunda se descartaba en silencio. Y no se podia
simplemente permitir dos titulos iguales: _dedupe_sections (que conserva solo la
primera seccion de cada heading) las colapsaria al exportar -> perdida.

Lo que se prueba (el CONTRATO):

  B7 - idempotencia: un reintento del MISMO save (mismo fingerprint) no duplica.
  B9 - sesiones distintas: una sesion distinta del mismo proyecto/dia se ACEPTA,
       con un heading unico ("... (2)", "... (3)") que el export no colapsa.

Los tests corren contra una DB temporal (tmp_path), nunca sobre memory/memory.db.
"""
import importlib.util
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("mes", ROOT / "scripts" / "memory-end-session.py")
mes = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mes)


def _fresh_db(tmp_path, monkeypatch):
    db = tmp_path / "t.db"
    c = sqlite3.connect(db)
    c.execute(
        "CREATE TABLE daily_notes (id INTEGER PRIMARY KEY, date TEXT, type TEXT, "
        "content TEXT, created_at TEXT)"
    )
    c.commit()
    c.close()
    monkeypatch.setattr(mes, "DB_PATH", str(db))
    return mes.db_connection()


def _fp(project, summary):
    return mes.session_fingerprint(project, summary, "main", "")


def _headings(content):
    return [h for h, _ in mes._dedupe_sections(mes._split_sections(content)) if h]


def test_same_summary_is_deduplicated(tmp_path, monkeypatch):
    """B7: repetir el mismo save (mismo fingerprint) no duplica el bloque."""
    c = _fresh_db(tmp_path, monkeypatch)
    _, ins1, _ = mes.append_to_daily_db(c, "2026-01-01", "workspace", "A", "main", "", _fp("workspace", "A"))
    _, ins2, reason2 = mes.append_to_daily_db(c, "2026-01-01", "workspace", "A", "main", "", _fp("workspace", "A"))
    assert ins1 is True
    assert ins2 is False and reason2 == "duplicate"
    content = c.execute("SELECT content FROM daily_notes WHERE date='2026-01-01'").fetchone()[0]
    assert content.count("## Session End - workspace") >= 1
    assert content.count("**Summary:** A") == 1  # no se duplico
    c.close()


def test_distinct_sessions_same_day_are_both_kept(tmp_path, monkeypatch):
    """B9: dos sesiones DISTINTAS del mismo proyecto/dia -> ambas sobreviven."""
    c = _fresh_db(tmp_path, monkeypatch)
    mes.append_to_daily_db(c, "2026-01-01", "workspace", "A", "main", "", _fp("workspace", "A"))
    mes.append_to_daily_db(c, "2026-01-01", "workspace", "B", "main", "", _fp("workspace", "B"))
    content = c.execute("SELECT content FROM daily_notes WHERE date='2026-01-01'").fetchone()[0]
    heads = _headings(content)  # tras dedupe (lo que se exporta)
    assert "## Session End - workspace" in heads
    assert "## Session End - workspace (2)" in heads
    assert content.count("**Summary:** A") == 1
    assert content.count("**Summary:** B") == 1
    c.close()


def test_three_distinct_sessions_unique_headings(tmp_path, monkeypatch):
    """B9: headings unicos incrementales (base, (2), (3)) y ninguno colapsado."""
    c = _fresh_db(tmp_path, monkeypatch)
    for s in ("A", "B", "C"):
        mes.append_to_daily_db(c, "2026-01-01", "workspace", s, "main", "", _fp("workspace", s))
    content = c.execute("SELECT content FROM daily_notes WHERE date='2026-01-01'").fetchone()[0]
    heads = _headings(content)
    assert heads == ["## Session End - workspace", "## Session End - workspace (2)", "## Session End - workspace (3)"]
    assert len(heads) == len(set(heads))  # sin colisiones de heading
    c.close()


def test_export_preserves_all_sessions(tmp_path, monkeypatch):
    """El round-trip DB -> .md no pierde ninguna sesion (el bug original)."""
    c = _fresh_db(tmp_path, monkeypatch)
    for s in ("A", "B"):
        mes.append_to_daily_db(c, "2026-01-01", "workspace", s, "main", "", _fp("workspace", s))
    content = c.execute("SELECT content FROM daily_notes WHERE date='2026-01-01'").fetchone()[0]
    exported = mes._join_sections(mes._dedupe_sections(mes._split_sections(content)))
    assert "**Summary:** A" in exported
    assert "**Summary:** B" in exported
    c.close()


def test_fingerprint_is_stable_and_distinct():
    """B7: mismo input -> mismo fingerprint; input distinto -> distinto."""
    assert mes.session_fingerprint("p", "s", "main", "") == mes.session_fingerprint("p", "s", "main", "")
    assert mes.session_fingerprint("p", "s", "main", "") != mes.session_fingerprint("p", "s2", "main", "")
