#!/usr/bin/env python3
"""
memory-search.py - Semantic search over the memory database
Uses Ollama embeddings + cosine similarity to find relevant sessions.

Usage:
  ./memory-search.py "query text" [top_n]
  ./memory-search.py --topics          # list all topics
  ./memory-search.py --recent [n]      # list recent sessions
"""

import sqlite3
import os
import sys
import json
import math
import hashlib
from datetime import datetime

# Los vectores pueden estar en BLOB float32 (nuevo) o JSON (legacy). El decoder
# compartido acepta ambos, asi el script sigue funcionando durante y despues de
# la migracion (scripts/migrate-vectors.py).
import importlib.util as _ilu

_spec = _ilu.spec_from_file_location(
    "vector_util", os.path.join(os.path.dirname(os.path.abspath(__file__)), "vector-util.py")
)
_vu = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_vu)
decode_vector = _vu.decode

# El corte de texto es COMPARTIDO con rechunk-vectors.py: si divergieran, el
# texto mostrado no seria el que se vectorizo.
_spec2 = _ilu.spec_from_file_location(
    "chunk_util", os.path.join(os.path.dirname(os.path.abspath(__file__)), "chunk-util.py")
)
_cu = _ilu.module_from_spec(_spec2)
_spec2.loader.exec_module(_cu)
split_large = _cu.split_large
strip_harness_header = _cu.strip_harness_header

# El indice vectorial vive en vectors.db (ADR-108). Esta apertura adjunta `idx` y
# aborta si falta: sin indice no hay busqueda, y una lista vacia se confunde con
# "no hay resultados".
_spec3 = _ilu.spec_from_file_location(
    "db_connect", os.path.join(os.path.dirname(os.path.abspath(__file__)), "db-connect.py")
)
_dbc = _ilu.module_from_spec(_spec3)
_spec3.loader.exec_module(_dbc)
connect_db = _dbc.connect

DB_PATH = os.environ.get("MEMORY_DB", "memory/memory.db")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "qwen3-embedding:0.6b")


def get_embedding(text):
    """Get embedding vector from text via Ollama (fallback to hash)

    Uses urllib (stdlib): the system python has no requests installed, which
    silently forced every call into the SHA-256 fallback.
    """
    try:
        import urllib.request

        body = json.dumps({
            "model": EMBED_MODEL,
            "prompt": text[:768],
            "n_preamble": 0,
            "n_context": 768,
            "n_predict": 0,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{OLLAMA_BASE}/api/embeddings",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            if resp.status == 200:
                data = json.loads(resp.read())
                # Ollama returns 'embedding' (singular) for /api/embeddings
                if "embedding" in data:
                    return data["embedding"]
                if "embeddings" in data and data["embeddings"]:
                    return data["embeddings"][0]
    except Exception as e:
        print(f"⚠️ Ollama unavailable ({e}), using hash fallback", file=sys.stderr)

    h = hashlib.sha256(text.encode("utf-8", errors="ignore")).digest()
    return [float(i) for i in h]


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    dot = sum(a * b for a, b in zip(vec1, vec2))
    n1 = math.sqrt(sum(x * x for x in vec1))
    n2 = math.sqrt(sum(x * x for x in vec2))
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)


def search(query, top_n=5):
    """Search sessions and sections by semantic similarity to query.

    Busca en DOS niveles, porque un chunk de ficha (un tema entero) y un chunk
    de seccion (una parte concreta) responden preguntas distintas:

      - session_vectors: "¿que sesiones hablan de X?"
      - section_vectors: "¿en que parte exacta se dijo X?"

    Devuelve los mejores de cada uno, marcados. Antes solo miraba fichas.
    """
    conn = connect_db()
    c = conn.cursor()

    qv = get_embedding(query)

    # --- Nivel ficha ---
    scored = []
    for session_id, blob, chunk_idx, txt in c.execute(
        "SELECT session_id, query_vector, chunk_index, chunk_text FROM idx.session_vectors"
    ):
        vec = decode_vector(blob)
        if vec is None:
            continue
        scored.append((cosine_similarity(qv, vec), session_id, chunk_idx, txt))
    scored.sort(key=lambda x: x[0], reverse=True)

    seen = set()
    results = []
    for score, session_id, chunk_idx, txt in scored:
        if session_id in seen:
            continue
        seen.add(session_id)
        results.append((score, session_id, chunk_idx, txt))
        if len(results) >= top_n:
            break

    print(f"\n🔍 Results for: \"{query}\"")
    print("=" * 60)
    if not results:
        print("  No results found.")
    for score, session_id, chunk_idx, txt in results:
        row = c.execute(
            "SELECT date, title, summary FROM sessions_relacional WHERE id=?", (session_id,)
        ).fetchone()
        if not row:
            continue
        date, title, summary = row
        print(f"\n  [{score * 100:.1f}%] {date} - {title}")
        if summary:
            print(f"      {summary[:150]}...")
        # El texto del chunk AHORA se lee de su columna, no se reconstruye con
        # una ventana fija: desde el re-chunking los cortes son semanticos y
        # `chunk_idx * 1500` devolvia texto de otro lado.
        if txt:
            print(f"      📄 {txt[:200].replace(chr(10), ' ')}...")

    # --- Nivel seccion ---
    # El texto NO se lee de una columna: `section_vectors` solo guarda el vector
    # y apunta a la seccion. El texto se reconstruye desde los offsets, que es
    # lo que evita duplicar 2.9 MB en una DB versionada.
    secs = []
    for sec_id, blob, ci in c.execute(
        "SELECT section_id, query_vector, chunk_index FROM idx.section_vectors"
    ):
        vec = decode_vector(blob)
        if vec is None:
            continue
        secs.append((cosine_similarity(qv, vec), sec_id, ci))
    secs.sort(key=lambda x: x[0], reverse=True)

    if secs:
        print(f"\n📑 Fragmentos")
        print("=" * 60)
        for score, sec_id, ci in secs[:top_n]:
            meta = c.execute(
                """SELECT doc_type, doc_id, level, time_start FROM sections WHERE id=?""",
                (sec_id,),
            ).fetchone()
            donde = ""
            if meta:
                dt, did, lvl, ts = meta
                tabla = "daily_notes" if dt == "daily" else "sessions_relacional"
                d = c.execute(f"SELECT date FROM {tabla} WHERE id=?", (did,)).fetchone()
                donde = f"{dt}:{d[0] if d else did}" + (f" {ts}" if ts else "")
            print(f"\n  [{score * 100:.1f}%] {donde}")
            txt = rebuild_section_text(c, sec_id, ci)
            if txt:
                print(f"      {txt[:180].replace(chr(10), ' ')}...")

    conn.commit()
    search_learnings(query, top_n=3)
    conn.close()


def body_of_section(conn, doc_type, doc_id, char_start, char_end):
    """Reconstruye el cuerpo de una seccion desde los offsets de su padre."""
    tabla = "daily_notes" if doc_type == "daily" else "sessions_relacional"
    col = "content" if doc_type == "daily" else "content_bare"
    row = conn.execute(f"SELECT {col} FROM {tabla} WHERE id=?", (doc_id,)).fetchone()
    return (row[0][char_start:char_end] or "") if row else ""






def rebuild_section_text(conn, section_id, chunk_index):
    """Reconstruye el texto de un chunk de seccion desde los offsets del padre.

    Mismo algoritmo que rechunk-vectors.py, para que el texto mostrado sea
    exactamente el que se vectorizo.
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
    piezas = split_large(body)
    if chunk_index >= len(piezas):
        return ""
    return f"## {strip_harness_header(title)}\n\n{piezas[chunk_index]}"


def search_learnings(query, top_n=3):
    """Search learnings by semantic similarity to query"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    qv = get_embedding(query)

    rows = c.execute(
        "SELECT id, category, title, content, learning_vector FROM learnings WHERE learning_vector IS NOT NULL"
    ).fetchall()

    scored = []
    for lid, category, title, content, vec_json in rows:
        vec = decode_vector(vec_json)
        if vec is None:
            continue
        score = cosine_similarity(qv, vec)
        scored.append((score, lid, category, title, content))

    scored.sort(key=lambda x: x[0], reverse=True)
    scored = scored[:top_n]

    if not scored:
        return

    print(f"\n📚 Top learnings")
    print("=" * 60)
    for score, lid, category, title, content in scored:
        pct = score * 100
        print(f"\n  [{pct:.1f}%] [{category}] {title}")
        if content:
            print(f"      {content[:150]}...")

    conn.close()


def list_topics():
    """List all topics with session counts"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    print("\n🏷️  Topics")
    print("=" * 60)
    rows = c.execute(
        """SELECT t.name, t.description, COUNT(ts.session_id) as sessions
           FROM topics t
           LEFT JOIN topic_sessions ts ON t.id = ts.topic_id
           GROUP BY t.id ORDER BY sessions DESC"""
    ).fetchall()
    for name, desc, count in rows:
        print(f"  • {name} ({count} sesiones) - {desc or ''}")
    conn.close()


def list_recent(n=10):
    """List recent sessions"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    print(f"\n📜 Recent {n} sessions")
    print("=" * 60)
    rows = c.execute(
        "SELECT date, title, substr(summary,1,80) FROM sessions_relacional ORDER BY created_at DESC LIMIT ?",
        (n,),
    ).fetchall()
    for date, title, summary in rows:
        print(f"  • {date} - {title}")
        if summary:
            print(f"      {summary}...")
    conn.close()


def main():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        sys.exit(1)

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--topics":
        list_topics()
    elif arg == "--recent":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        list_recent(n)
    elif arg in ("-h", "--help"):
        print(__doc__)
    else:
        query = " ".join(sys.argv[1:])
        top_n = 5
        # Allow "query --top 10" style
        if "--top" in sys.argv:
            idx = sys.argv.index("--top")
            top_n = int(sys.argv[idx + 1])
            query = " ".join(sys.argv[1:idx])
        search(query, top_n)


if __name__ == "__main__":
    main()
