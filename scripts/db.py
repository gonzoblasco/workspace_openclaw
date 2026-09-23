#!/usr/bin/env python3
"""
db.py - Conexion unica a memory.db, con las foreign keys ACTIVAS.

Por que existe este modulo: `PRAGMA foreign_keys` es **por conexion** en SQLite,
y viene DESACTIVADA por defecto. Eso significa que declarar una FK en el schema
no alcanza: hay que activarla en cada conexion que escribe, o el motor la ignora.

Estado medido el 2026-09-23: la DB tenia **6 FK declaradas y 0 activas**. Los
`ON DELETE CASCADE` nunca dispararon, y por eso aparecieron 20 filas huerfanas
que hubo que limpiar a mano en ADR-058.

Centralizar la conexion evita el olvido: si un script nuevo importa `connect()`,
ya nace con la integridad activa.

Uso:
    from db import connect
    conn = connect(DB_PATH)              # lectura/escritura, FK activas
    conn = connect(DB_PATH, readonly=True)

Para scripts de shell que invocan la CLI de sqlite3:
    sqlite3 -cmd "PRAGMA foreign_keys=ON" "$DB" "..."   (misma idea)
"""
import sqlite3


def connect(path, readonly=False):
    """Abre memory.db con las foreign keys activas.

    En modo readonly no se activa el pragma: no se escribe, asi que no puede
    crear huerfanos, y activarlo obligaria a tomar un lock de escritura.
    """
    if readonly:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    else:
        conn = sqlite3.connect(str(path))
        conn.execute("PRAGMA foreign_keys = ON")
    return conn


def check(path):
    """Devuelve las violaciones de FK. Lista vacia = integridad OK.

    Se usa para verificar despues de escribir: un script puede activar el pragma
    y aun asi dejar huerfanos si el orden de las operaciones es incorrecto.
    """
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        return list(conn.execute("PRAGMA foreign_key_check"))
    finally:
        conn.close()


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "memory/memory.db"
    v = check(target)
    if v:
        print(f"{len(v)} violaciones de foreign key en {target}:")
        for row in v[:20]:
            print(f"  {row}")
        sys.exit(1)
    print(f"OK: integridad referencial correcta en {target}")
