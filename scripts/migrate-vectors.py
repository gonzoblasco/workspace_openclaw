#!/usr/bin/env python3
"""
migrate-vectors.py - Convierte los embeddings de memory.db de JSON a BLOB.

Contexto (medido 2026-09-22): el 77% de los 12 MB de memory.db eran vectores
guardados como texto JSON. 1024 floats ocupaban ~22 KB en JSON y 4096 bytes en
BLOB float32. Con ~168 vectores nuevos por mes, el JSON crecia ~3.6 MB/mes.

Lo que hace:
  1. Convierte session_vectors.query_vector y learnings.learning_vector
     de TEXT(JSON) a BLOB(float32). Idempotente: salta los que ya son BLOB.
  2. Reemplaza idx_learnings_vector (copia completa de los vectores en texto,
     3.2 MB) por un indice parcial sobre id (KB). El original solo servia para
     responder "que filas tienen vector", y para eso no hace falta el valor.
  3. Opcional (--drop-dead-columns): elimina columnas que SIEMPRE estan NULL.
     OJO: eso NO ahorra espacio medible (un NULL cuesta ~1 byte por fila). Es
     higiene de schema: una columna que nadie escribe es una trampa para el
     proximo que asuma que esta poblada.
  4. VACUUM para devolver las paginas liberadas al sistema de archivos.

Uso:
    migrate-vectors.py --dry-run     muestra que haria, sin escribir
    migrate-vectors.py               aplica
    migrate-vectors.py --drop-dead-columns    ademas quita las columnas muertas

Antes de escribir: hace un backup junto al original (memory.db.pre-vector-blob).
"""
import argparse
import shutil
import sqlite3
import sys
import time
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
DB = WS / "memory" / "memory.db"

# (tabla, columna) con vectores que hay que convertir. Desde ADR-058 el vector
# de learnings vive en `learnings`, no en la tabla gemela eliminada.
VECTOR_COLS = [
    ("session_vectors", "query_vector"),
    ("learnings", "learning_vector"),
]

# El indice pesado y su reemplazo liviano.
HEAVY_INDEX = "idx_learnings_vector"
LIGHT_INDEX_SQL = (
    "CREATE INDEX IF NOT EXISTS idx_learnings_vec_present "
    "ON learnings(id) WHERE learning_vector IS NOT NULL"
)

# Columnas siempre NULL (verificado antes de escribir esto).
DEAD_COLS = [
    ("sessions_relacional", "agent_id"),
]


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def load_vector_util():
    import importlib.util

    spec = importlib.util.spec_from_file_location("vector_util", WS / "scripts" / "vector-util.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def survey(conn, vu):
    """Foto del estado actual: cuantos JSON, cuantos BLOB, cuanto pesan."""
    out = {}
    for table, col in VECTOR_COLS:
        rows = conn.execute(f"SELECT id, {col} FROM {table} WHERE {col} IS NOT NULL").fetchall()
        as_json = sum(1 for _id, v in rows if vu.is_json(v))
        total = sum(len(v) if isinstance(v, str) else len(bytes(v)) for _id, v in rows)
        out[(table, col)] = {"filas": len(rows), "json": as_json, "bytes": total}
    return out


def migrate(conn, vu, dry_run, drop_dead):
    report = []

    # --- 1. Vectores JSON -> BLOB ---
    for table, col in VECTOR_COLS:
        rows = conn.execute(f"SELECT id, {col} FROM {table} WHERE {col} IS NOT NULL").fetchall()
        converted = skipped = failed = 0
        before = after = 0
        updates = []
        for row_id, value in rows:
            if not vu.is_json(value):
                skipped += 1
                continue
            before += len(value)
            vec = vu.decode(value)
            if vec is None:
                failed += 1
                continue
            blob = vu.encode(vec)
            # Invariante: el BLOB debe decodificar al MISMO vector. Si no, no se escribe.
            if vu.decode(blob) != vec:
                failed += 1
                continue
            updates.append((blob, row_id))
            after += len(blob)
            converted += 1

        if not dry_run:
            conn.executemany(f"UPDATE {table} SET {col}=? WHERE id=?", updates)
            conn.commit()

        report.append(
            f"  {table}.{col}: {converted} convertidos, {skipped} ya eran BLOB, "
            f"{failed} fallidos  ({human(before)} -> {human(after)}, ahorro "
            f"{100 * (1 - after / before) if before else 0:.0f}%)"
        )

    # --- 2. Indice pesado -> liviano ---
    exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='index' AND name=?", (HEAVY_INDEX,)
    ).fetchone()
    if exists:
        size = 0
        try:
            size = conn.execute(
                "SELECT sum(pgsize) FROM dbstat WHERE name=?", (HEAVY_INDEX,)
            ).fetchone()[0] or 0
        except sqlite3.Error:
            pass
        if not dry_run:
            conn.execute(f"DROP INDEX {HEAVY_INDEX}")
            conn.execute(LIGHT_INDEX_SQL)
            conn.commit()
        report.append(
            f"  indice {HEAVY_INDEX} ({human(size)}) -> idx_learnings_vec_present (KB): "
            "la pregunta es 'que filas tienen vector', no el valor"
        )
    else:
        report.append(f"  indice {HEAVY_INDEX}: ya no existe (nada que hacer)")

    # --- 3. Columnas muertas (opcional) ---
    if drop_dead:
        for table, col in DEAD_COLS:
            info = conn.execute(f"PRAGMA table_info({table})").fetchall()
            if col not in [r[1] for r in info]:
                report.append(f"  {table}.{col}: ya no existe")
                continue
            n = conn.execute(f"SELECT count({col}) FROM {table}").fetchone()[0]
            if n:
                report.append(f"  {table}.{col}: SE SALTA, tiene {n} valores (no es muerta)")
                continue
            if not dry_run:
                conn.execute(f"ALTER TABLE {table} DROP COLUMN {col}")
                conn.commit()
            report.append(
                f"  {table}.{col}: eliminada (siempre NULL; ahorro ~0 bytes, es higiene)"
            )

    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="muestra que haria, no escribe")
    ap.add_argument("--drop-dead-columns", action="store_true", help="elimina columnas siempre NULL")
    ap.add_argument("--db", default=None, help="path alternativo a la DB (para probar sobre una copia)")
    args = ap.parse_args()

    global DB
    if args.db:
        DB = Path(args.db).resolve()

    if not DB.exists():
        sys.exit(f"No existe {DB}")

    vu = load_vector_util()

    if not args.dry_run:
        backup = DB.with_suffix(".db.pre-vector-blob")
        shutil.copy2(DB, backup)
        print(f"backup: {backup} ({human(backup.stat().st_size)})")

    size_before = DB.stat().st_size
    conn = sqlite3.connect(DB)
    try:
        # Invariante correcto: la migracion no debe AGREGAR violaciones. Las que
        # ya existen son otro problema (foreign_keys=0, ver ADR) y se reportan
        # aparte; fallar por ellas haria el chequeo inutil (falla siempre).
        fk_before = set(map(tuple, conn.execute("PRAGMA foreign_key_check").fetchall()))

        print("Antes:")
        for line in migrate(conn, vu, args.dry_run, args.drop_dead_columns):
            print(line)

        if not args.dry_run:
            print("VACUUM (devuelve las paginas liberadas)...")
            t = time.time()
            try:
                conn.execute("VACUUM")
                conn.commit()
                print(f"  listo en {time.time() - t:.1f}s")
            except sqlite3.OperationalError as exc:
                # Tipico: otra conexion (la app) tiene la DB abierta.
                print(f"  SALTADO: {exc}")
                print("  (los datos ya se convirtieron; VACUUM solo recupera espacio en disco)")
                print("  Para recuperarlo: cerrar la app y correr 'sqlite3 memory/memory.db VACUUM'")
                globals()["VACUUM_SKIPPED"] = True

        # Verificacion post: invariantes de integridad.
        print("\nVerificacion:")
        bad = 0
        for table, col in VECTOR_COLS:
            rows = conn.execute(f"SELECT id, {col} FROM {table} WHERE {col} IS NOT NULL").fetchall()
            still_json = sum(1 for _id, v in rows if vu.is_json(v))
            dims = set()
            for _id, v in rows:
                d = vu.dims(v)
                if d:
                    dims.add(d)
            if args.dry_run:
                # En dry-run nada se escribe: reportar "quedan JSON" seria confuso.
                print(f"  {table}.{col}: {len(rows)} filas, dims={sorted(dims)} (dry-run: se convertiran)")
            else:
                flag = "OK" if still_json == 0 else f"!! quedan {still_json} JSON"
                if still_json:
                    bad += 1
                print(f"  {table}.{col}: {len(rows)} filas, dims={sorted(dims)}, {flag}")

        # Integridad referencial: DELTA, no absoluto.
        fk_after = set(map(tuple, conn.execute("PRAGMA foreign_key_check").fetchall()))
        nuevas = fk_after - fk_before
        resueltas = fk_before - fk_after
        if nuevas:
            print(f"  foreign keys: !! {len(nuevas)} violaciones NUEVAS (las causo la migracion)")
            for v in list(nuevas)[:5]:
                print(f"     {v}")
            bad += 1
        else:
            extra = f", {len(resueltas)} resueltas" if resueltas else ""
            print(f"  foreign keys: OK, sin violaciones nuevas ({len(fk_before)} preexistentes{extra})")
            if fk_before:
                from collections import Counter

                print(f"     preexistentes por tabla: {dict(Counter(v[0] for v in fk_before))}")
                print("     (causa: PRAGMA foreign_keys=0 -> los ON DELETE CASCADE no disparan)")
    finally:
        conn.close()

    size_after = DB.stat().st_size
    print(
        f"\nTamano: {human(size_before)} -> {human(size_after)} "
        f"(-{100 * (1 - size_after / size_before):.0f}%)"
    )
    if args.dry_run:
        print("(dry-run: nada se escribio)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
