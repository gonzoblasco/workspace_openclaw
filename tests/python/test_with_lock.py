"""Tests para scripts/with-lock.py (wrapper de shell sobre lockutil).

Contexto (2026-10-19): `session-end.sh` y `session-commit.sh` son bash y macOS
no trae `flock(1)`. `with-lock.py` envuelve un comando con un flock tomado via
`lockutil`, y devuelve EX_TEMPFAIL (75) cuando el recurso esta tomado.

Contrato:
  - corre el comando y propaga su exit code;
  - por defecto ESPERA a que el lock se libere (cola, no error);
  - con --timeout corto es fail-fast: sale 75 y NO corre el comando;
  - libera el lock al salir, incluso si el comando falla.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
WITH_LOCK = ROOT / "scripts" / "with-lock.py"

# El script calcula LOCK_DIR desde su propia ubicacion (WORKSPACE/scripts/..),
# asi que los locks caen en el `.openclaw/locks` del repo, no en tmp_path. Para
# no ensuciar el workspace, cada test usa un recurso con nombre unico.
EX_TEMPFAIL = 75


def _run(resource, command, timeout=10, lock_timeout=None):
    prefix = [sys.executable, str(WITH_LOCK)]
    if lock_timeout is not None:
        prefix += ["--timeout", str(lock_timeout)]
    return subprocess.run(
        [*prefix, resource, "--", *command],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def test_runs_command_and_propagates_exit_code():
    r = _run("test-with-lock-basic", ["sh", "-c", "exit 0"])
    assert r.returncode == 0
    r = _run("test-with-lock-basic", ["sh", "-c", "exit 3"])
    assert r.returncode == 3


def test_returns_75_and_skips_command_when_lock_is_held(tmp_path):
    holder = tmp_path / "holder.py"
    holder.write_text(
        "import sys, time\n"
        f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
        "from lockutil import file_lock\n"
        "with file_lock('test-with-lock-held'):\n"
        "    print('locked', flush=True)\n"
        "    time.sleep(3)\n"
    )
    p = subprocess.Popen(
        [sys.executable, str(holder)], stdout=subprocess.PIPE, text=True
    )
    try:
        assert p.stdout.readline().strip() == "locked"
        marker = tmp_path / "ran.txt"
        r = _run(
            "test-with-lock-held",
            ["sh", "-c", f"echo ran > {marker}"],
            lock_timeout=0.3,  # fail-fast: el holder duerme 3s
        )
        assert r.returncode == EX_TEMPFAIL, r.stderr
        assert not marker.exists(), "el comando no debio ejecutarse con el lock tomado"
    finally:
        p.kill()
        p.wait(timeout=5)


def test_waits_for_lock_by_default(tmp_path):
    """Sin --timeout hace cola: espera y despues corre el comando."""
    holder = tmp_path / "holder.py"
    holder.write_text(
        "import sys, time\n"
        f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
        "from lockutil import file_lock\n"
        "with file_lock('test-with-lock-waits'):\n"
        "    print('locked', flush=True)\n"
        "    time.sleep(1.5)\n"
    )
    p = subprocess.Popen(
        [sys.executable, str(holder)], stdout=subprocess.PIPE, text=True
    )
    try:
        assert p.stdout.readline().strip() == "locked"
        start = time.monotonic()
        r = _run("test-with-lock-waits", ["sh", "-c", "exit 0"])
        elapsed = time.monotonic() - start
        assert r.returncode == 0, r.stderr
        assert elapsed >= 0.5, f"deberia haber esperado al holder (espero {elapsed:.1f}s)"
    finally:
        p.kill()
        p.wait(timeout=5)


def test_releases_lock_when_command_fails():
    """Un comando que falla no debe dejar el lock tomado."""
    r = _run("test-with-lock-release", ["sh", "-c", "exit 1"])
    assert r.returncode == 1
    r = _run("test-with-lock-release", ["sh", "-c", "exit 0"])
    assert r.returncode == 0


def test_rejects_missing_separator():
    r = subprocess.run(
        [sys.executable, str(WITH_LOCK), "solo-un-arg"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2
