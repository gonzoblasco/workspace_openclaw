"""db-connect.py - abre `memory.db` con el índice vectorial adjunto.

POR QUE EXISTE (2026-11-04, ADR-108). El índice vectorial vive en `memory/vectors.db`
desde que se separó el dato crudo (versionado en git) del índice (local y regenerable).
Los scripts que tocan vectores necesitan las dos bases en la misma conexión, y SQLite
lo resuelve con ATTACH.

REGLA (ADR-108): si `vectors.db` no existe, esta función FALLA. No abre la DB sin
índice y no devuelve una conexión a medias. Un instrumento roto tiene que decir que
está roto: el 2026-11-04 un check del pre-commit contó un error de jq como PASS y un
test de concurrencia falló de forma intermitente, las dos veces con verde falso.

Uso:
    from db_connect import connect
    conn = connect()                     # memory.db + idx.* adjunto
    conn = connect(require_vectors=False)  # scripts que no tocan vectores
"""

import os
import sqlite3

DB_PATH = os.environ.get("MEMORY_DB", "memory/memory.db")


def vectors_path(db_path=None):
    """Ruta de vectors.db, hermana de memory.db por defecto."""
    override = os.environ.get("MEMORY_VECTORS_DB")
    if override:
        return override
    base = os.path.dirname(os.path.abspath(db_path or DB_PATH))
    return os.path.join(base, "vectors.db")


def connect(db_path=None, require_vectors=True):
    """Devuelve una conexión con `idx` (vectors.db) adjunta.

    require_vectors=True (default): aborta si vectors.db no existe. Es lo correcto
    para todo script que lee o escribe vectores: sin índice no hay búsqueda, y una
    búsqueda vacía se confunde con "no hay resultados".
    """
    db = db_path or DB_PATH
    vp = vectors_path(db)

    if require_vectors and not os.path.exists(vp):
        raise SystemExit(
            f"ERROR: no existe el indice vectorial en {vp}\n"
            f"La busqueda semantica no puede correr sin el (ADR-108).\n"
            f"Reconstruilo con: python3 scripts/memory-reembed.py --all"
        )

    conn = sqlite3.connect(db)
    if os.path.exists(vp):
        conn.execute("ATTACH DATABASE ? AS idx", (vp,))
    return conn
