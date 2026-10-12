#!/usr/bin/env python3
"""
lockutil.py - Lock de archivo portable para escritores concurrentes (B6).

Contexto (2026-10-12): varias sesiones dashboard cierran sesion sobre el MISMO
repo a la vez. `memory-end-session.py` regenera `memory/YYYY-MM-DD.md` y
`session-handoff.py` escribe `.knowledge/HANDOFF.md`. Sin coordinacion, dos
cierre simultaneos pueden intercalar lectura y escritura sobre el mismo archivo
(o sobre el mismo commit). Este modulo serializa esas escrituras.

Por que flock y no mkdir+PID (como scripts/pipeline-queue.sh):
  - `pipeline-queue.sh` es shell y macOS no trae flock(1), asi que usa mkdir
    atomico + PID. En Python, `fcntl.flock` SI existe en macOS/Linux y es mas
    robusto: el lock se libera solo cuando el proceso muere (no quedan locks
    huerfanos que haya que romper por antiguedad).
  - Un lock de archivo asesor (advisory) coordina a todos los que lo usan; es
    exactamente el caso: los unicos escritores de estos archivos son estos
    scripts.

Uso:
    from lockutil import file_lock
    with file_lock("memory/2026-10-12.md"):
        # leer-modificar-escribir del archivo, sin que otro proceso se intercale
        ...

El lock-file se crea en `.openclaw/locks/` (gitignored), derivado del nombre del
recurso, para no ensuciar el arbol versionado ni el propio archivo objetivo.
"""

import fcntl
import hashlib
import os
import time
from contextlib import contextmanager
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
LOCK_DIR = WORKSPACE / ".openclaw" / "locks"

DEFAULT_TIMEOUT = 60.0   # segundos a esperar por el lock antes de rendirse
POLL_INTERVAL = 0.05


def _lock_path_for(resource) -> Path:
    """Deriva el path del lock-file a partir del recurso objetivo.

    Usa el path absoluto del recurso hasheado: asi dos invocaciones que apuntan
    al MISMO archivo (aunque una lo nombre relativo y otra absoluto) comparten
    el mismo lock.
    """
    key = hashlib.sha1(str(Path(resource).resolve()).encode("utf-8")).hexdigest()[:16]
    return LOCK_DIR / f"{key}.lock"


@contextmanager
def file_lock(resource, timeout: float = DEFAULT_TIMEOUT):
    """Adquiere un lock exclusivo para `resource` y lo libera al salir.

    Bloquea hasta `timeout` segundos. Si no lo consigue, lanza TimeoutError.
    El lock se libera automaticamente al cerrar el file descriptor (y tambien
    si el proceso muere), asi que no hay locks huerfanos persistentes.
    """
    lock_path = _lock_path_for(resource)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    fd = open(lock_path, "w")
    deadline = time.monotonic() + timeout
    try:
        while True:
            try:
                fcntl.flock(fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError(
                        f"No se pudo adquirir el lock de '{resource}' en {timeout}s "
                        f"(otro proceso lo retiene)."
                    )
                time.sleep(POLL_INTERVAL)
        # Escribir el pid dentro del lock (diagnostico: quien lo tiene).
        fd.seek(0)
        fd.truncate()
        fd.write(str(os.getpid()))
        fd.flush()
        yield
    finally:
        try:
            fcntl.flock(fd.fileno(), fcntl.LOCK_UN)
        finally:
            fd.close()
