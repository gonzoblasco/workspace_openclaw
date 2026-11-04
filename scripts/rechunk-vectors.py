#!/usr/bin/env python3
"""
rechunk-vectors.py - Re-cortar los vectores por unidades semanticas (2026-09-23).

ESTADO (2026-11-04): herramienta de REPARACION MANUAL, no parte del ciclo
automatico. Se conserva porque rehace los chunks cuando cambia la estrategia de
corte, y porque `chunk-util.py` -que comparte con `memory-search.py`- es la
fuente unica del corte: si los dos divergieran, la busqueda mostraria texto que
no es el que se vectorizo. Desde ADR-108 escribe en `memory/vectors.db` (idx).

PROBLEMA MEDIDO

Los 136 vectores de `session_vectors` se cortaron con una ventana CIEGA de 1500
caracteres sobre el texto crudo:

    raw_chunks = [content[j : j + CHUNK_SIZE] for j in range(0, len(content), CHUNK_SIZE)]

Consecuencias, medidas sobre la DB real:

  - **29% de los chunks cortan a mitad de frase.** Ejemplo real: un chunk empieza
    con `'should be archived to...'` (perdio el sujeto de la oracion anterior) y
    termina con `'it does'` (corta el verbo). El embedding de ese fragmento
    representa mal su contenido.
  - **El chunk 0 es el volcado del harness** en 20 de 136 casos (15%): empieza con
    `# Session: 2026-08-29... - **Session Key**: agent:main:main`. Se vectoriza
    metadata de la sesion, no su contenido.
  - **Solo 48 sesiones tienen vectores**, cuando hay 51 fichas y 408 unidades de
    tema: el texto vectorizado es una fraccion del material (3 chunks maximo por
    sesion, sobre un texto que puede tener 11000 caracteres).

QUE HACE

Recorta usando las **unidades de nivel 2** que ya existen en `session_entries`
(ADR-060): son las fronteras semanticas reales (cada `##` es un tema), y ya
tienen offsets calculados. No hay que adivinar donde cortar.

  - Cada unidad de TEMA entra como un chunk propio, con su titulo adelante: el
    titulo da contexto que el fragmento crudo perdia.
  - Las unidades de BOILERPLATE se saltan: `Session End`, `Cierre`,
    `Self-reflection`, `Conversation Summary` no son contenido de trabajo.
    (113 unidades, el 15% que contaminaba.)
  - Las unidades MAS GRANDES que el limite se parten en fronteras de parrafo
    (doble salto de linea), nunca a mitad de palabra. Se conserva algo de solape
    para que una idea partida siga encontrandose desde cualquiera de los dos
    lados.

QUE NO HACE

  - No re-vectoriza por hash si Ollama falla: un fallo deja la fila afuera y se
    reporta. Un vector basura contamina las busquedas para siempre.
  - No toca `sessions_relacional` ni `session_entries`: solo reescribe
    `session_vectors`.

Uso:
    rechunk-vectors.py --dry-run          # mide y muestra, sin escribir
    rechunk-vectors.py                    # reescribe session_vectors
    rechunk-vectors.py --limit 10         # solo N fichas (para probar)
"""
import argparse
import importlib.util as _ilu_db
import json
import os
import re
import shutil
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
DB = Path(os.environ.get("MEMORY_DB", WS / "memory" / "memory.db"))
OLLAMA = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "qwen3-embedding:0.6b")

# El indice vectorial vive en vectors.db (ADR-108): esta apertura adjunta `idx`
# y reescribe las tablas de vectores ahi, no en memory.db.
_spec_db = _ilu_db.spec_from_file_location(
    "db_connect", os.path.join(str(Path(__file__).resolve().parent), "db-connect.py")
)
_dbc = _ilu_db.module_from_spec(_spec_db)
_spec_db.loader.exec_module(_dbc)
connect_db = _dbc.connect

# El corte de texto vive en chunk-util.py: memory-search.py usa el MISMO modulo,
# asi el texto que muestra el buscador es exactamente el que se vectorizo.
# Los tamanos tambien salen de ahi: una sola fuente para los dos scripts.
_util = None


def util():
    """El modulo compartido de corte (se carga una sola vez)."""
    global _util
    if _util is None:
        _util = _load("chunk_util", "chunk-util.py")
    return _util


SCHEMA = """
CREATE TABLE IF NOT EXISTS idx.section_vectors (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id   INTEGER NOT NULL,     -- FK a sections
    chunk_index  INTEGER NOT NULL,     -- una seccion grande puede dar varios
    query_vector BLOB NOT NULL,        -- float32, 1024 dims
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (section_id, chunk_index),
    FOREIGN KEY(section_id) REFERENCES sections(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx.idx_svec_section ON idx.section_vectors(section_id);
"""
# NOTA: a proposito NO hay columna `chunk_text`.
#
# Medido: el 75% del texto de los chunks era identico al cuerpo de su seccion,
# que ya vive en el padre y se reconstruye con los offsets de `sections`. Eran
# +2.9 MB de duplicacion en una DB que esta TRACKEADA EN GIT, o sea que crecia
# la historia del repo con cada commit. Mismo principio que ADR-059/060:
# offsets, no copias.
#
# Para mostrar los 5 resultados de una busqueda no hace falta almacenar 2352
# textos: se reconstruyen al vuelo desde el offset de la seccion.


def _load(nombre, archivo):
    import importlib.util

    spec = importlib.util.spec_from_file_location(nombre, WS / "scripts" / archivo)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_vector_util():
    return _load("vector_util", "vector-util.py")


def embed(text, vu):
    """Embedding real. Lanza si Ollama no responde: nunca escribe un hash."""
    body = json.dumps({"model": EMBED_MODEL, "prompt": text[:8000]}).encode()
    req = urllib.request.Request(
        f"{OLLAMA}/api/embeddings", data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        vec = json.loads(r.read()).get("embedding")
    if not vec or len(vec) < 128:
        raise RuntimeError(f"embedding invalido (dim={len(vec) if vec else 0})")
    return vec






def build_chunks(conn, session_id):
    """Los chunks de una ficha, desde sus unidades semanticas.

    Si la ficha no tiene unidades de tema (18 de 51: son volcados del harness
    cuyo unico heading es 'Conversation Summary'), se cae al contenido crudo
    sin la cabecera de metadata. Descartarlas perderia texto real: medido, 17
    de esas 18 tienen contenido propio y ninguna esta duplicada.
    """
    row = conn.execute(
        "SELECT content_bare FROM sessions_relacional WHERE id=?", (session_id,)
    ).fetchone()
    if not row:
        return []
    content = row[0] or ""

    entries = conn.execute(
        """SELECT title, char_start, char_end FROM session_entries
           WHERE session_id=? AND kind='tema' ORDER BY ordinal""",
        (session_id,),
    ).fetchall()

    if not entries:
        # Sin unidades de tema: partir el texto sin la cabecera del harness.
        limpio = util().strip_harness_header(content)
        return [c for c in util().split_large(limpio) if len(c) >= util().MIN_CHARS]

    chunks = []
    for title, cs, ce in entries:
        body = (content[cs:ce] or "").strip()
        if not body:
            continue
        # El titulo adelante: da el contexto que el fragmento crudo perdia
        # (un chunk que empezaba en "should be archived" ahora dice de que).
        cabecera = f"## {title}\n\n"
        for piece in util().split_large(body):
            full = cabecera + piece
            if len(full) >= util().MIN_CHARS:
                chunks.append(full)
    return chunks


def body_of_section(conn, doc_type, doc_id, char_start, char_end):
    """Reconstruye el cuerpo de una seccion desde los offsets de su padre."""
    tabla = "daily_notes" if doc_type == "daily" else "sessions_relacional"
    col = "content" if doc_type == "daily" else "content_bare"
    row = conn.execute(f"SELECT {col} FROM {tabla} WHERE id=?", (doc_id,)).fetchone()
    return (row[0][char_start:char_end] or "") if row else ""


def build_section_chunks(conn, section_id, title, doc_type, doc_id, cs, ce):
    """Los chunks de una seccion, con su titulo adelante.

    El titulo es la clave: una seccion como "Pendientes" sin su encabezado no
    dice nada. Con el, el vector representa el contenido Y su proposito.
    """
    body = body_of_section(conn, doc_type, doc_id, cs, ce).strip()
    if not body:
        return []
    cabecera = f"## {util().strip_harness_header(title)}\n\n"
    return [
        cabecera + p
        for p in util().split_large(body)
        if len(cabecera + p) >= util().MIN_CHARS
    ]


def run_sections(conn, dry_run, limit=None):
    """Vectoriza las secciones de TODOS los documentos (daily + session).

    Son las 1987 secciones de ADR-059. Medido: 1631 entran directo en un chunk y
    204 son grandes y se parten. 152 son ruido (<100 chars) y se saltan.

    Es una tabla aparte de `session_vectors`, no una columna mas, porque el FK
    apunta a otra tabla (`sections`). Mantener un FK real por tabla es lo que
    ADR-060 acaba de establecer; un `source_id` polimorfico lo perderia.
    """
    vu = load_vector_util()
    cu = load_chunk_util()
    filas = conn.execute(
        """SELECT s.id, s.title, s.doc_type, s.doc_id, s.char_start, s.char_end
           FROM sections s ORDER BY s.doc_type, s.doc_id, s.ordinal"""
    ).fetchall()
    if limit:
        filas = filas[:limit]

    antes = conn.execute("SELECT count(*) FROM idx.section_vectors").fetchone()[0]
    print(f"  secciones: {len(filas)}")
    print(f"  vectores de seccion antes: {antes}")

    nuevos, descartados, vacias = [], 0, 0
    t0 = time.time()
    for i, (sid, title, dt, did, cs, ce) in enumerate(filas, 1):
        chunks = build_section_chunks(conn, sid, title, dt, did, cs, ce)
        if not chunks:
            vacias += 1
            continue
        if dry_run:
            continue
        for idx, ch in enumerate(chunks):
            try:
                vec = embed(ch, vu)
            except Exception as exc:
                descartados += 1
                print(f"    seccion {sid} chunk {idx}: se omite ({exc})")
                continue
            nuevos.append((sid, idx, vu.encode(vec)))
        if i % 250 == 0:
            print(f"    {i}/{len(filas)} secciones, {len(nuevos)} chunks, {time.time()-t0:.0f}s")

    print(f"  chunks de seccion generados: {len(nuevos)}")
    if vacias:
        print(f"  secciones sin cuerpo (saltadas): {vacias}")
    if descartados:
        print(f"  descartados por fallo de embedding: {descartados}")

    if dry_run:
        print("  (dry-run: no se escribio)")
        return len(nuevos)

    conn.execute("DELETE FROM idx.section_vectors")
    conn.executemany(
        """INSERT INTO idx.section_vectors (section_id, chunk_index, query_vector)
           VALUES (?,?,?)""",
        nuevos,
    )
    conn.commit()
    print(f"  vectores de seccion escritos: {conn.execute('SELECT count(*) FROM idx.section_vectors').fetchone()[0]}")
    print(f"  tiempo: {time.time()-t0:.0f}s")
    return len(nuevos)


def rebuild_section_text(conn, section_id, chunk_index):
    """Reconstruye el texto de un chunk de seccion desde los offsets del padre.

    El texto NO se guarda en `section_vectors` (era 2.9 MB de duplicacion en una
    DB versionada). Se recalcula con el mismo algoritmo que lo genero, asi que
    el resultado es identico al que se vectorizo.
    """
    meta = conn.execute(
        """SELECT title, doc_type, doc_id, char_start, char_end FROM sections WHERE id=?""",
        (section_id,),
    ).fetchone()
    if not meta:
        return ""
    title, dt, did, cs, ce = meta
    body = body_of_section(conn, dt, did, cs, ce).strip()
    if not body:
        return ""
    from_title = util().strip_harness_header(title)
    piezas = util().split_large(body)
    if chunk_index >= len(piezas):
        return ""
    return f"## {from_title}\n\n{piezas[chunk_index]}"


def body_of_section(conn, doc_type, doc_id, char_start, char_end):
    """Reconstruye el cuerpo de una seccion desde los offsets de su padre."""
    tabla = "daily_notes" if doc_type == "daily" else "sessions_relacional"
    col = "content" if doc_type == "daily" else "content_bare"
    row = conn.execute(f"SELECT {col} FROM {tabla} WHERE id=?", (doc_id,)).fetchone()
    return (row[0][char_start:char_end] or "") if row else ""


def rebuild_section_text(conn, section_id, chunk_index):
    """Reconstruye el texto de un chunk de seccion desde los offsets del padre.

    Usa el mismo corte que al vectorizar, asi el texto mostrado es identico al
    que se vectorizo. El texto NO se guarda: era 2.9 MB de duplicacion en una DB
    versionada.
    """
    meta = conn.execute(
        """SELECT title, doc_type, doc_id, char_start, char_end FROM sections WHERE id=?""",
        (section_id,),
    ).fetchone()
    if not meta:
        return ""
    title, dt, did, cs, ce = meta
    body = body_of_section(conn, dt, did, cs, ce).strip()
    if not body:
        return ""
    piezas = util().split_large(body)
    if chunk_index >= len(piezas):
        return ""
    return f"## {util().strip_harness_header(title)}\n\n{piezas[chunk_index]}"


def run(conn, dry_run, limit=None):
    vu = load_vector_util()
    # TODAS las fichas, no solo las que tienen unidades de tema: 18 de 51 no
    # tienen (son volcados) y quedarian sin vectores. Medido: 17 de esas 18
    # tienen contenido propio y ninguna esta duplicada.
    sesiones = [
        r[0]
        for r in conn.execute("SELECT id FROM sessions_relacional ORDER BY id")
    ]
    if limit:
        sesiones = sesiones[:limit]

    antes = conn.execute("SELECT count(*) FROM idx.session_vectors").fetchone()[0]
    print(f"  sesiones con unidades de tema: {len(sesiones)}")
    print(f"  vectores antes: {antes}")

    total, descartados = 0, 0
    nuevos = []
    t0 = time.time()
    for i, sid in enumerate(sesiones, 1):
        chunks = build_chunks(conn, sid)
        if dry_run:
            total += len(chunks)
            if i <= 3:
                print(f"\n  --- ficha {sid}: {len(chunks)} chunks ---")
                for c in chunks[:2]:
                    print(f"    [{len(c)} chars] {c[:88]!r}")
            continue
        for idx, ch in enumerate(chunks):
            try:
                vec = embed(ch, vu)
            except Exception as exc:
                descartados += 1
                print(f"    ficha {sid} chunk {idx}: se omite ({exc})")
                continue
            nuevos.append((sid, vu.encode(vec), idx, ch))
        total += len(chunks)
        if i % 10 == 0:
            print(f"    {i}/{len(sesiones)} fichas, {total} chunks, {time.time()-t0:.0f}s")

    print(f"\n  chunks generados: {total}")
    if descartados:
        print(f"  descartados por fallo de embedding: {descartados}")

    if dry_run:
        print("  (dry-run: no se escribio)")
        return total

    conn.execute("DELETE FROM session_vectors")
    conn.executemany(
        """INSERT INTO idx.session_vectors
           (session_id, query_vector, relevance_score, chunk_index, chunk_text, created_at)
           VALUES (?,?,0.0,?,?,datetime('now'))""",
        nuevos,
    )
    conn.commit()
    print(f"  vectores escritos: {conn.execute('SELECT count(*) FROM idx.session_vectors').fetchone()[0]}")
    print(f"  tiempo: {time.time()-t0:.0f}s")
    return total


def verify(conn):
    print("\nVerificacion:")
    bad = 0
    fk = list(conn.execute("PRAGMA foreign_key_check"))
    print(f"  foreign keys: {len(fk)} violaciones {'OK' if not fk else '!!'}")
    bad += 1 if fk else 0

    # Ningun chunk debe EMPEZAR con el volcado del harness. Ojo: '%Session Key%'
    # en cualquier parte NO sirve como criterio - este workspace discute
    # internals de OpenClaw donde "session key" es un tema legitimo (medido: los
    # 10 chunks que el filtro amplio marcaba eran contenido real).
    n = conn.execute(
        """SELECT count(*) FROM idx.session_vectors
           WHERE chunk_text LIKE '# Session:%'
              OR chunk_text LIKE '%- **Session Key**:%'"""
    ).fetchone()[0]
    print(f"  chunks que empiezan con volcado del harness: {n} {'OK' if n == 0 else '!!'}")
    bad += 1 if n else 0

    # Los chunks de fichas CON unidades semanticas deben empezar con su titulo
    # ("## ..."). Los de fichas SIN estructura son texto crudo: ahi un inicio en
    # minuscula es esperable, no un defecto. Medido: de 147 marcados por el
    # filtro amplio, TODOS venian de las 18 fichas sin estructura.
    con_ent = {
        r[0]
        for r in conn.execute("SELECT DISTINCT session_id FROM session_entries WHERE kind='tema'")
    }
    mal_sem = 0
    for sid, t in conn.execute("SELECT session_id, chunk_text FROM idx.session_vectors"):
        if sid in con_ent and t and not t.startswith("## "):
            mal_sem += 1
    print(
        f"  chunks semanticos sin titulo al frente: {mal_sem} {'OK' if mal_sem == 0 else '!!'}"
    )
    bad += 1 if mal_sem else 0

    dims = set()
    vu = load_vector_util()
    for (v,) in conn.execute("SELECT query_vector FROM idx.session_vectors"):
        try:
            dims.add(len(vu.decode(v)))
        except Exception:
            bad += 1
    print(f"  dimensiones (fichas): {dims} {'OK' if dims and max(dims) >= 128 else '!!'}")

    # Las mismas garantias para las secciones.
    n_sec = conn.execute("SELECT count(*) FROM idx.section_vectors").fetchone()[0]
    if n_sec:
        sin_titulo = conn.execute(
            """SELECT count(*) FROM idx.section_vectors WHERE chunk_text NOT LIKE '## %'"""
        ).fetchone()[0]
        print(f"  secciones vectorizadas: {n_sec}")
        print(f"  chunks de seccion sin titulo al frente: {sin_titulo} {'OK' if sin_titulo == 0 else '!!'}")
        bad += 1 if sin_titulo else 0
        huerfanos = conn.execute(
            """SELECT count(*) FROM idx.section_vectors v LEFT JOIN sections s ON s.id=v.section_id
               WHERE s.id IS NULL"""
        ).fetchone()[0]
        print(f"  section_vectors huerfanos: {huerfanos} {'OK' if huerfanos == 0 else '!!'}")
        bad += 1 if huerfanos else 0
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--db", default=None)
    ap.add_argument(
        "--sections", action="store_true", help="vectoriza tambien las 1987 secciones"
    )
    ap.add_argument("--only-sections", action="store_true", help="solo las secciones")
    args = ap.parse_args()

    global DB
    if args.db:
        DB = Path(args.db).resolve()
    if not DB.exists():
        sys.exit(f"No existe {DB}")

    if not args.dry_run:
        backup = DB.with_suffix(".db.pre-rechunk")
        shutil.copy2(DB, backup)
        print(f"backup: {backup}")

    conn = connect_db(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    bad = 0
    try:
        if args.sections or args.only_sections:
            conn.executescript(SCHEMA)
            conn.commit()
        if not args.only_sections:
            print(f"Re-cortando vectores de FICHA por unidades semanticas{'(dry-run)' if args.dry_run else ''}...")
            run(conn, args.dry_run, args.limit)
        if args.sections or args.only_sections:
            print(f"\nVectorizando SECCIONES{'(dry-run)' if args.dry_run else ''}...")
            run_sections(conn, args.dry_run, args.limit)
        if not args.dry_run:
            bad = verify(conn)
    finally:
        conn.close()
    return 1 if not args.dry_run and bad else 0


if __name__ == "__main__":
    sys.exit(main())
