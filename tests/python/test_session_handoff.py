"""Tests para scripts/session-handoff.py (A+C: historial + indice de sesiones).

Contexto (2026-10-13): el HANDOFF es last-writer-wins por diseno (es "estado
actual"). Dos cierres sobre el MISMO proyecto perdian el primero. Se agregan:

  - A. backup del HANDOFF previo en `.knowledge/handoff-history/` antes de pisarlo;
  - C. indice append-only `.knowledge/SESSIONS.md` con una linea por cierre.

Lo que se prueba es el CONTRATO observable en disco, siempre sobre un tmp_path
(nunca el workspace real):

  - primer cierre: crea HANDOFF y SESSIONS.md, sin historial;
  - segundo cierre: HANDOFF = el nuevo, historial = el anterior, indice con 2 filas;
  - el indice es append puro: las filas previas nunca se pierden;
  - un HANDOFF ausente no genera backup (no hay nada que preservar).
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
# session-handoff.py hace `from lockutil import file_lock`; lockutil vive en
# scripts/, asi que hay que poner ese directorio en sys.path antes de cargarlo.
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "session_handoff", SCRIPTS / "session-handoff.py"
)
session_handoff = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(session_handoff)


def _close(handoff_dir, summary, ts):
    """Ejecuta el cierre en `handoff_dir` con un timestamp fijo (determinista)."""
    target = Path(handoff_dir) / "HANDOFF.md"
    with session_handoff.file_lock(target):
        existed = target.exists()
        backup = session_handoff.backup_previous(target, ts) if existed else None
        index = session_handoff.append_session_index(target, "workspace", ts, summary)
        tmp = target.with_suffix(".md.tmp")
        tmp.write_text(session_handoff.build_handoff(_Args(summary)), encoding="utf-8")
        import os

        os.replace(tmp, target)
    return backup, index


class _Args:
    """Minimo de args que build_handoff consume."""

    def __init__(self, summary):
        self.date = "2026-10-13"
        self.branch = "main"
        self.repo = "https://github.com/gonzoblasco/workspace_openclaw"
        self.summary = summary
        self.status = ""
        self.next_steps = ""
        self.decisions = ""
        self.files = ""
        self.project = "workspace"

    def __getattr__(self, name):  # pragma: no cover - solo por robustez
        return ""


def test_first_close_creates_handoff_and_index_without_history(tmp_path):
    k = tmp_path / ".knowledge"
    k.mkdir()
    backup, _ = _close(k, "Primera sesion", "2026-10-13 10:00")

    assert backup is None, "sin HANDOFF previo no debe haber backup"
    assert (k / "HANDOFF.md").exists()
    assert (k / "SESSIONS.md").exists()
    assert not (k / "handoff-history").exists()


def test_second_close_preserves_first_in_history_and_index(tmp_path):
    k = tmp_path / ".knowledge"
    k.mkdir()
    _close(k, "Primera sesion", "2026-10-13 10:00")
    backup, _ = _close(k, "Segunda sesion", "2026-10-13 11:00")

    # A: el HANDOFF anterior quedo archivado, no perdido.
    assert backup is not None and backup.exists()
    assert "Primera sesion" in backup.read_text(encoding="utf-8")
    # HANDOFF actual = el nuevo (last-writer-wins se mantiene).
    assert "Segunda sesion" in (k / "HANDOFF.md").read_text(encoding="utf-8")
    # C: el indice acumula las dos sesiones, sin pisar la primera.
    index = (k / "SESSIONS.md").read_text(encoding="utf-8")
    assert "Primera sesion" in index
    assert "Segunda sesion" in index
    assert index.count("- **") == 2


def test_index_is_append_only(tmp_path):
    k = tmp_path / ".knowledge"
    k.mkdir()
    for i in range(5):
        _close(k, f"Sesion {i}", f"2026-10-13 1{i}:00")
    index = (k / "SESSIONS.md").read_text(encoding="utf-8")
    # Ninguna fila previa se pierde: append puro.
    for i in range(5):
        assert f"Sesion {i}" in index
    assert index.count("- **") == 5
