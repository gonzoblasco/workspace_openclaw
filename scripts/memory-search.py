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
import requests
from datetime import datetime

DB_PATH = os.environ.get("MEMORY_DB", "memory/memory.db")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text:latest")


def get_embedding(text):
    """Get embedding vector from text via Ollama (fallback to hash)"""
    try:
        response = requests.post(
            f"{OLLAMA_BASE}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": text[:768], "n_preamble": 0, "n_context": 768, "n_predict": 0},
            timeout=25,
        )
        if response.status_code == 200:
            data = response.json()
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
    """Search sessions by semantic similarity to query"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    qv = get_embedding(query)

    rows = c.execute(
        "SELECT session_id, query_vector, chunk_index FROM session_vectors"
    ).fetchall()

    # Score each vector against query
    scored = []
    for session_id, vec_json, chunk_idx in rows:
        try:
            vec = json.loads(vec_json)
        except (json.JSONDecodeError, TypeError):
            continue
        score = cosine_similarity(qv, vec)
        scored.append((score, session_id, chunk_idx))

    # Sort by score desc, dedupe by session (keep best chunk)
    scored.sort(key=lambda x: x[0], reverse=True)
    seen = set()
    results = []
    for score, session_id, chunk_idx in scored:
        if session_id in seen:
            continue
        seen.add(session_id)
        results.append((score, session_id, chunk_idx))
        if len(results) >= top_n:
            break

    # Fetch session details
    print(f"\n🔍 Results for: \"{query}\"")
    print("=" * 60)
    if not results:
        print("  No results found.")
        return

    for score, session_id, chunk_idx in results:
        row = c.execute(
            "SELECT date, title, summary FROM sessions_relacional WHERE id=?", (session_id,)
        ).fetchone()
        if not row:
            continue
        date, title, summary = row
        pct = score * 100
        print(f"\n  [{pct:.1f}%] {date} - {title}")
        if summary:
            print(f"      {summary[:150]}...")
        # Show matching chunk content
        vec_row = c.execute(
            "SELECT query_vector FROM session_vectors WHERE session_id=? AND chunk_index=?",
            (session_id, chunk_idx),
        ).fetchone()
        if vec_row:
            # Find the content chunk from the session
            content = c.execute(
                "SELECT content_bare FROM sessions_relacional WHERE id=?", (session_id,)
            ).fetchone()
            if content and content[0]:
                chunk_size = 1500
                start = chunk_idx * chunk_size
                chunk_text = content[0][start : start + chunk_size]
                print(f"      📄 {chunk_text[:200]}...")

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
