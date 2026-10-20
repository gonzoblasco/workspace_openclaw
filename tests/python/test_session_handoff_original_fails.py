"""Tests que prueban que la implementacion VIEJA no cumple el contrato nuevo.

Estos tests cargan el `session-handoff.py` original (commit ``00777910b0``) y
verifican que su comportamiento observable es el que motivó el fix:

* el nombre del backup sale del ``ts`` del cierre, no de la linea ``**Fecha:**``;
* no hay sufijo incremental: dos backups con el mismo minuto se pisan;
* no hay politica de retencion.

Pasan mientras el codigo viejo este realmente roto: si alguien "arregla" el
loader o apunta a la version nueva, fallan. La version vieja se extrae con
``git show <commit>:scripts/session-handoff.py``; si el objeto no existe, el
test se saltea (no se inventa evidencia).
"""

import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Optional

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

OLD_COMMIT = "00777910b0"


@pytest.fixture(scope="module")
def old_module(tmp_path_factory):
    """Carga la version vieja del script desde git en un archivo temporal."""
    res = subprocess.run(
        ["git", "show", f"{OLD_COMMIT}:scripts/session-handoff.py"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if res.returncode != 0 or not res.stdout.strip():
        pytest.skip(f"no se pudo extraer {OLD_COMMIT}:scripts/session-handoff.py")
    tmp = tmp_path_factory.mktemp("old_handoff") / "session-handoff.py"
    tmp.write_text(res.stdout, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("session_handoff_old", tmp)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _create_handoff(target: Path, fecha_line: Optional[str]) -> None:
    content_parts = ["# HANDOFF - test", ""]
    if fecha_line is not None:
        content_parts.append(fecha_line)
    else:
        content_parts.append("Some content without a date line.")
    target.write_text("\n".join(content_parts), encoding="utf-8")


def test_old_backup_name_comes_from_ts(old_module, tmp_path):
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    _create_handoff(target, "**Fecha:** 2026-01-02 03:45 GMT-3")

    backup = old_module.backup_previous(target, "2026-10-20 15:00")

    # El bug: ignora la fecha interna del HANDOFF y usa el ts del cierre nuevo.
    assert backup is not None
    assert backup.name == "2026-10-20-1500-HANDOFF.md"
    assert backup.name != "2026-01-02-0345-HANDOFF.md"


def test_old_backup_overwrites_on_same_minute(old_module, tmp_path, monkeypatch):
    monkeypatch.setenv("HANDOFF_HISTORY_KEEP", "1")
    handoff_dir = tmp_path / ".knowledge"
    handoff_dir.mkdir()
    target = handoff_dir / "HANDOFF.md"
    hist = target.parent / "handoff-history"
    hist.mkdir()
    (hist / "2026-01-01-0100-HANDOFF.md").write_text("old", encoding="utf-8")
    _create_handoff(target, "**Fecha:** 2026-01-02 02:00 GMT-3")

    first = old_module.backup_previous(target, "2026-01-02 02:00")
    second = old_module.backup_previous(target, "2026-01-02 02:00")

    # Sin sufijo: el segundo pisa al primero.
    assert first.name == second.name == "2026-01-02-0200-HANDOFF.md"
    # Sin retencion: el backup viejo sigue estando.
    assert (hist / "2026-01-01-0100-HANDOFF.md").exists()
    assert len([p for p in hist.iterdir() if p.is_file()]) == 2
