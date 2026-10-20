"""Extended tests for the updated `session-handoff.py` behaviour.

These tests verify the new requirements:
* backup file name is derived from the **Fecha** line inside the previous
  HANDOFF, not from the supplied timestamp `ts`.
* when a name collision occurs an incremental suffix (``-2``, ``-3`` ...) is
  added.
* a retention policy keeps only the last N backups (configurable via the
  ``HANDOFF_HISTORY_KEEP`` environment variable) and discards older files in a
  recoverable way.
* if the ``**Fecha:**`` line is missing the fallback is the file's modification
  time ``mtime``.

All tests are written for Python 3.9; they avoid modern type-union syntax and
use only the standard library.

Ningun test dispara el ``/usr/bin/trash`` real: todos fijan
``HANDOFF_HISTORY_TRASH_BIN=""`` para forzar el fallback local (o apuntan la
variable a un binario falso cuando quieren probar el camino del binario).
"""

import importlib.util
import os
import stat
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "session_handoff", SCRIPTS / "session-handoff.py"
)
session_handoff = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(session_handoff)


@pytest.fixture(autouse=True)
def _no_real_trash(monkeypatch):
    """Nunca tocar el ~/.Trash real: fallback local por defecto en cada test."""
    monkeypatch.setenv("HANDOFF_HISTORY_TRASH_BIN", "")


def _create_handoff(target: Path, fecha_line: Optional[str]) -> None:
    """Create a HANDOFF file at *target*.

    If *fecha_line* is ``None`` the line is omitted, forcing the fallback to
    ``mtime``. Otherwise the line must be a complete ``**Fecha:**`` entry.
    """
    content_parts = ["# HANDOFF - test", ""]
    if fecha_line is not None:
        content_parts.append(fecha_line)
    else:
        # some other content without a date line
        content_parts.append("Some content without a date line.")
    content = "\n".join(content_parts)
    target.write_text(content, encoding="utf-8")


def _remaining(hist: Path):
    return sorted(p.name for p in hist.iterdir() if p.is_file())


def test_backup_uses_fecha_line_not_ts(tmp_path):
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    _create_handoff(target, "**Fecha:** 2026-01-02 03:45 GMT-3")
    original = target.read_text(encoding="utf-8")

    backup = session_handoff.backup_previous(target, "2026-10-20 15:00")

    assert backup is not None and backup.exists()
    assert backup.name == "2026-01-02-0345-HANDOFF.md"
    # El backup es una copia fiel del HANDOFF anterior.
    assert backup.read_text(encoding="utf-8") == original


def test_backup_collision_suffix(tmp_path):
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    _create_handoff(target, "**Fecha:** 2026-02-03 04:56 GMT-3")

    first = session_handoff.backup_previous(target, "2026-10-20 15:01")
    assert first.name == "2026-02-03-0456-HANDOFF.md"

    second = session_handoff.backup_previous(target, "2026-10-20 15:02")
    assert second.name == "2026-02-03-0456-2-HANDOFF.md"

    # Un tercero no pisa a ninguno de los dos anteriores.
    third = session_handoff.backup_previous(target, "2026-10-20 15:03")
    assert third.name == "2026-02-03-0456-3-HANDOFF.md"
    assert len({first.name, second.name, third.name}) == 3


def test_fecha_line_embedded_in_prose_is_ignored(tmp_path):
    """Una fecha con formato **Fecha:** dentro de una linea de prosa no cuenta."""
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    target.write_text(
        "# HANDOFF - test\n\n"
        "Ver el ejemplo **Fecha:** 2020-01-01 00:00 en la documentacion.\n",
        encoding="utf-8",
    )
    mtime_ts = 1609459200  # 2021-01-01 00:00 UTC
    os.utime(target, (mtime_ts, mtime_ts))

    backup = session_handoff.backup_previous(target, "2026-10-20 15:04")

    expected = datetime.fromtimestamp(mtime_ts).strftime("%Y-%m-%d-%H%M")
    assert backup is not None
    assert backup.name == f"{expected}-HANDOFF.md"


def test_retention_keeps_latest_n(tmp_path, monkeypatch):
    """La retencion deja los N mas nuevos y saca el resto del directorio.

    No se asserta la ruta exacta del destino (el binario del sistema no es
    inspeccionable de forma portable): se verifica el resultado observable, que
    el archivo ya no este en ``handoff-history/`` y que siga existiendo en el
    fallback local recuperable (``.trash/``), es decir que no se borro.
    """
    monkeypatch.setenv("HANDOFF_HISTORY_KEEP", "2")
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    hist = target.parent / "handoff-history"
    hist.mkdir()
    for d in ["2026-01-01-0100", "2026-01-02-0200", "2026-01-03-0300"]:
        (hist / f"{d}-HANDOFF.md").write_text("old", encoding="utf-8")

    _create_handoff(target, "**Fecha:** 2026-01-04 04:00 GMT-3")
    backup = session_handoff.backup_previous(target, "2026-10-20 15:03")

    assert backup is not None and backup.exists()
    assert _remaining(hist) == [
        "2026-01-03-0300-HANDOFF.md",
        "2026-01-04-0400-HANDOFF.md",
    ]
    # Recuperables: siguen existiendo, movidos al fallback local.
    trash_dir = hist / ".trash"
    trashed = sorted(p.name for p in trash_dir.iterdir())
    assert trashed == ["2026-01-01-0100-HANDOFF.md", "2026-01-02-0200-HANDOFF.md"]


def test_retention_counts_collision_suffixes_by_base_date(tmp_path, monkeypatch):
    """El orden por fecha del nombre funciona con sufijos de colision."""
    monkeypatch.setenv("HANDOFF_HISTORY_KEEP", "3")
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    hist = target.parent / "handoff-history"
    hist.mkdir()
    for name in [
        "2026-01-01-0100-HANDOFF.md",
        "2026-01-03-0300-HANDOFF.md",
        "2026-01-03-0300-2-HANDOFF.md",
    ]:
        (hist / name).write_text("old", encoding="utf-8")

    _create_handoff(target, "**Fecha:** 2026-01-05 05:00 GMT-3")
    session_handoff.backup_previous(target, "2026-10-20 15:05")

    # Sobreviven el backup nuevo y, de la misma fecha, el sufijo mas alto
    # (el mas reciente); el sufijo no rompe la extraccion de la fecha base.
    assert set(_remaining(hist)) == {
        "2026-01-03-0300-2-HANDOFF.md",
        "2026-01-03-0300-HANDOFF.md",
        "2026-01-05-0500-HANDOFF.md",
    }


def test_retention_never_prunes_the_new_backup(tmp_path, monkeypatch):
    """Un HANDOFF viejo copiado ahora no se poda a si mismo."""
    monkeypatch.setenv("HANDOFF_HISTORY_KEEP", "1")
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    hist = target.parent / "handoff-history"
    hist.mkdir()
    for d in ["2026-01-01-0100", "2026-01-02-0200"]:
        (hist / f"{d}-HANDOFF.md").write_text("old", encoding="utf-8")

    # El HANDOFF que se copia tiene fecha MAS VIEJA que lo ya archivado.
    _create_handoff(target, "**Fecha:** 2025-12-31 23:00 GMT-3")
    backup = session_handoff.backup_previous(target, "2026-10-20 15:06")

    assert backup is not None and backup.exists()
    assert backup.name == "2025-12-31-2300-HANDOFF.md"
    assert backup.name in _remaining(hist)
    assert len(_remaining(hist)) == 1


@pytest.mark.parametrize("keep", ["no-es-un-entero", "", "3.5"])
def test_invalid_keep_falls_back_to_default(tmp_path, monkeypatch, keep):
    monkeypatch.setenv("HANDOFF_HISTORY_KEEP", keep)
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    hist = target.parent / "handoff-history"
    hist.mkdir()
    for i in range(12):
        (hist / f"2026-01-{i + 1:02d}-0100-HANDOFF.md").write_text("old", encoding="utf-8")

    _create_handoff(target, "**Fecha:** 2026-02-01 01:00 GMT-3")
    session_handoff.backup_previous(target, "2026-10-20 15:07")

    # Default = 10: el backup nuevo + los 9 mas recientes.
    assert len(_remaining(hist)) == 10


def test_keep_zero_keeps_only_the_new_backup(tmp_path, monkeypatch):
    monkeypatch.setenv("HANDOFF_HISTORY_KEEP", "0")
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    hist = target.parent / "handoff-history"
    hist.mkdir()
    for d in ["2026-01-01-0100", "2026-01-02-0200"]:
        (hist / f"{d}-HANDOFF.md").write_text("old", encoding="utf-8")

    _create_handoff(target, "**Fecha:** 2026-01-03 03:00 GMT-3")
    backup = session_handoff.backup_previous(target, "2026-10-20 15:08")

    assert backup is not None and backup.exists()
    assert _remaining(hist) == ["2026-01-03-0300-HANDOFF.md"]


def test_trash_binary_is_preferred_when_configured(tmp_path, monkeypatch):
    """Con un binario de papelera disponible, se usa ese camino primero."""
    fake = tmp_path / "fake-trash"
    log = tmp_path / "trash.log"
    # El doble del binario MUEVE el archivo a una papelera propia (no borra).
    graveyard = tmp_path / "graveyard"
    graveyard.mkdir()
    fake.write_text(
        "#!/bin/sh\n"
        f'for f in "$@"; do printf "%s\\n" "$f" >> "{log}"; mv "$f" "{graveyard}/"; done\n',
        encoding="utf-8",
    )
    fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("HANDOFF_HISTORY_TRASH_BIN", str(fake))
    monkeypatch.setenv("HANDOFF_HISTORY_KEEP", "1")

    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    hist = target.parent / "handoff-history"
    hist.mkdir()
    (hist / "2026-01-01-0100-HANDOFF.md").write_text("old", encoding="utf-8")

    _create_handoff(target, "**Fecha:** 2026-01-02 02:00 GMT-3")
    session_handoff.backup_previous(target, "2026-10-20 15:09")

    assert log.exists() and "2026-01-01-0100-HANDOFF.md" in log.read_text()
    assert _remaining(hist) == ["2026-01-02-0200-HANDOFF.md"]
    assert not (hist / ".trash").exists()


def test_fallback_to_mtime_when_no_fecha(tmp_path):
    mtime_ts = 1609459200  # epoch 1609459200 = 2021-01-01 00:00 UTC
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    _create_handoff(target, None)  # no fecha line
    os.utime(target, (mtime_ts, mtime_ts))

    backup = session_handoff.backup_previous(target, "2026-10-20 15:10")

    assert backup is not None and backup.exists()
    dt = datetime.fromtimestamp(mtime_ts)
    assert backup.name == dt.strftime("%Y-%m-%d-%H%M") + "-HANDOFF.md"


def test_unparseable_fecha_falls_back_to_mtime(tmp_path):
    """Un ``**Fecha:**`` con fecha imposible (mes 13) tambien cae a mtime."""
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    _create_handoff(target, "**Fecha:** 2026-13-45 99:99 GMT-3")
    mtime_ts = 1609459200
    os.utime(target, (mtime_ts, mtime_ts))

    backup = session_handoff.backup_previous(target, "2026-10-20 15:11")

    expected = datetime.fromtimestamp(mtime_ts).strftime("%Y-%m-%d-%H%M")
    assert backup is not None
    assert backup.name == f"{expected}-HANDOFF.md"
