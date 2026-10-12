"""Tests para scripts/lockutil.py (lock de escritura concurrente, B6).

Contexto: varias sesiones dashboard cierran sobre el MISMO repo a la vez;
`memory-end-session.py` y `session-handoff.py` coordinan sus escrituras con
`file_lock`. Lo que se prueba es el CONTRATO que consumen:

  - exclusion mutua real: dos locks sobre el mismo recurso NO se solapan;
  - el lock se libera al salir del `with` (incluido si hubo excepcion);
  - `timeout` acota la espera y lanza TimeoutError si el recurso esta tomado;
  - dos nombres del MISMO archivo (relativo vs absoluto) comparten lock.

El lock se prueba sobre recursos en tmp_path, nunca sobre el workspace real.
"""
import importlib.util
import multiprocessing
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SPEC = importlib.util.spec_from_file_location("lockutil", ROOT / "scripts" / "lockutil.py")
lockutil = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lockutil)


def _hold_lock(resource, hold_seconds, q):
    """Toma el lock y lo mantiene; avisa por la cola cuando lo tiene."""
    try:
        with lockutil.file_lock(resource, timeout=5):
            q.put("locked")
            time.sleep(hold_seconds)
    except Exception as e:  # pragma: no cover
        q.put(f"error: {e}")


def test_lock_provides_mutual_exclusion(tmp_path):
    """Mientras un proceso tiene el lock, otro NO puede tomarlo (timeout corto)."""
    resource = tmp_path / "shared.md"
    resource.write_text("x")
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=_hold_lock, args=(str(resource), 1.0, q))
    p.start()
    assert q.get(timeout=5) == "locked"  # el hijo ya lo tiene
    try:
        with lockutil.file_lock(str(resource), timeout=0.3):
            raise AssertionError("no deberia haber adquirido el lock mientras el hijo lo tiene")
    except TimeoutError:
        pass  # esperado: exclusion mutua
    p.join(timeout=5)
    assert p.exitcode == 0


def test_lock_released_after_exit(tmp_path):
    """Tras salir del `with`, el lock queda libre y se puede re-tomar."""
    resource = tmp_path / "shared.md"
    resource.write_text("x")
    with lockutil.file_lock(str(resource), timeout=1):
        pass
    with lockutil.file_lock(str(resource), timeout=1):
        pass  # no debe colgar ni lanzar


def test_lock_released_on_exception(tmp_path):
    """Una excepcion dentro del bloque tambien libera el lock."""
    resource = tmp_path / "shared.md"
    resource.write_text("x")
    try:
        with lockutil.file_lock(str(resource), timeout=1):
            raise ValueError("boom")
    except ValueError:
        pass
    with lockutil.file_lock(str(resource), timeout=1):
        pass


def test_relative_and_absolute_share_lock(tmp_path, monkeypatch):
    """El MISMO archivo via path relativo y absoluto comparte lock."""
    (tmp_path / "shared.md").write_text("x")
    monkeypatch.chdir(tmp_path)
    q = multiprocessing.Queue()
    abs_path = str(tmp_path / "shared.md")
    p = multiprocessing.Process(target=_hold_lock, args=(abs_path, 1.0, q))
    p.start()
    assert q.get(timeout=5) == "locked"
    try:
        with lockutil.file_lock("shared.md", timeout=0.3):  # relativo
            raise AssertionError("relativo y absoluto deberian compartir lock")
    except TimeoutError:
        pass
    p.join(timeout=5)
