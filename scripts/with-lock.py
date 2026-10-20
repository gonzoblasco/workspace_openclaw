#!/usr/bin/env python3
"""
with-lock.py - Corre un comando sosteniendo un flock sobre un recurso.

Existe porque `session-end.sh` y `session-commit.sh` son bash y macOS no trae
`flock(1)`. En Python, `fcntl.flock` si existe en macOS y Linux, y `lockutil.py`
ya resuelve el timeout, el diagnostico por PID y la liberacion al morir el
proceso.

Por defecto ESPERA a que el recurso se libere (hasta 60s): en un cierre de
sesion, hacer cola es lo correcto. Con --timeout corto se convierte en
fail-fast, que es lo que quiere un script que prefiere abortar antes que
demorar.

Uso:
    ./scripts/with-lock.py [--timeout SEGUNDOS] RECURSO -- COMANDO [ARGS...]

Exit code: el del comando. Si no consigue el lock, 75 (EX_TEMPFAIL).
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lockutil import DEFAULT_TIMEOUT, file_lock  # noqa: E402

EX_TEMPFAIL = 75

USAGE = "Uso: with-lock.py [--timeout SEGUNDOS] RECURSO -- COMANDO [ARGS...]"


def main() -> int:
    args = sys.argv[1:]
    timeout = DEFAULT_TIMEOUT

    while args and args[0].startswith("--timeout"):
        if args[0] == "--timeout":
            if len(args) < 2:
                print(USAGE, file=sys.stderr)
                return 2
            timeout = float(args[1])
            args = args[2:]
        else:  # --timeout=5
            timeout = float(args[0].split("=", 1)[1])
            args = args[1:]

    if len(args) < 3 or args[1] != "--":
        print(USAGE, file=sys.stderr)
        return 2

    resource, command = args[0], args[2:]
    try:
        with file_lock(resource, timeout=timeout):
            return subprocess.call(command)
    except TimeoutError as exc:
        print(f"with-lock: {exc}", file=sys.stderr)
        return EX_TEMPFAIL


if __name__ == "__main__":
    sys.exit(main())
