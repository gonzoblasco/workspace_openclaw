#!/usr/bin/env python3
"""Re-embed fallback (32-dim SHA-256) vectors with a real embedding model.

The catalog falls back to a SHA-256 hash when Ollama is unreachable. Those
hashes are useless for semantic similarity and also break centroid math when
mixed with real vectors. This script finds them and replaces them with real
embeddings.

Deliberately does NOT fall back: if Ollama fails, the row is skipped and
reported, so a failed run never writes another useless hash.

Usage:
  ./memory-reembed.py [--dry-run] [--limit N] [--all]

By default it re-embeds every vector whose dimension differs from the model's
output, which covers both the 32-dim SHA-256 fallbacks and any vectors left
over from a previous embedding model (for example a 768-dim model after
switching to a 1024-dim one).

Env:
  EMBED_MODEL   default qwen3-embedding:0.6b
  OLLAMA_BASE   default http://127.0.0.1:11434
  MEMORY_DB     default memory/memory.db
"""

import argparse
import json
import os
import sqlite3
import sys
import time
import urllib.request

DB_PATH = os.environ.get("MEMORY_DB", "memory/memory.db")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "qwen3-embedding:0.6b")

# Any vector shorter than this is treated as garbage, never a real embedding.
MIN_REAL_DIM = 128


def embed(text):
    """Return a real embedding or raise. No silent fallback."""
    body = json.dumps({"model": EMBED_MODEL, "prompt": text[:4096]}).encode()
    req = urllib.request.Request(
        f"{OLLAMA_BASE}/api/embeddings",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    vec = data.get("embedding") or (data.get("embeddings") or [None])[0]
    if not vec or len(vec) < MIN_REAL_DIM:
        raise RuntimeError(f"bad embedding from {EMBED_MODEL}: {len(vec) if vec else 0} dims")
    return vec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    if not os.path.exists(DB_PATH):
        print(f"DB not found: {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    # Probe the model once: we need its real dimension to know what to target.
    try:
        target_dim = len(embed("dimension probe"))
    except Exception as exc:
        print(f"Model {EMBED_MODEL} not usable: {exc}", file=sys.stderr)
        print("Nothing written. Fix Ollama/model first.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    def stale(vec_json):
        try:
            return len(json.loads(vec_json)) != target_dim
        except (json.JSONDecodeError, TypeError):
            return False

    targets = []

    for row_id, title, content in c.execute(
        "SELECT id, title, coalesce(content,'') FROM learnings_enriquecido "
        "WHERE learning_vector IS NOT NULL"
    ).fetchall():
        vj = c.execute(
            "SELECT learning_vector FROM learnings_enriquecido WHERE id=?", (row_id,)
        ).fetchone()[0]
        if stale(vj):
            targets.append(("learnings_enriquecido", "learning_vector", row_id, f"{title} {content}".strip()))

    for row_id, chunk_text in c.execute(
        "SELECT id, chunk_text FROM session_vectors "
        "WHERE query_vector IS NOT NULL AND chunk_text IS NOT NULL AND TRIM(chunk_text)!=''"
    ).fetchall():
        vj = c.execute("SELECT query_vector FROM session_vectors WHERE id=?", (row_id,)).fetchone()[0]
        if stale(vj):
            targets.append(("session_vectors", "query_vector", row_id, chunk_text))

    if args.limit:
        targets = targets[: args.limit]

    print(f"Model: {EMBED_MODEL} ({target_dim} dims)")
    print(f"Vectors to re-embed (dim != {target_dim}): {len(targets)}")
    if args.dry_run:
        print("(dry run - nothing written)")
        for t in targets[:5]:
            print(f"  {t[0]} id={t[2]} text={t[3][:60]!r}")
        conn.close()
        return

    ok = 0
    failed = []
    for i, (table, column, row_id, text) in enumerate(targets, 1):
        try:
            vec = embed(text)
        except Exception as exc:
            failed.append((table, row_id, str(exc)[:80]))
            print(f"  [{i}/{len(targets)}] FAIL {table} id={row_id}: {exc}", file=sys.stderr)
            continue
        c.execute(f"UPDATE {table} SET {column}=? WHERE id=?", (json.dumps(vec), row_id))
        ok += 1
        if i % 10 == 0 or i == len(targets):
            conn.commit()
            print(f"  [{i}/{len(targets)}] re-embedded (dim={len(vec)})")
        time.sleep(0.05)

    conn.commit()

    print(f"\nRe-embedded: {ok}")
    if failed:
        print(f"Failed (left as-is, no hash written): {len(failed)}")
        for f in failed[:10]:
            print(f"  {f[0]} id={f[1]}: {f[2]}")

    # Post-run dimension report
    import collections
    for table, column in (("learnings_enriquecido", "learning_vector"), ("session_vectors", "query_vector")):
        dims = collections.Counter()
        for (vj,) in c.execute(f"SELECT {column} FROM {table} WHERE {column} IS NOT NULL"):
            try:
                dims[len(json.loads(vj))] += 1
            except (json.JSONDecodeError, TypeError):
                dims["malformed"] += 1
        print(f"{table}.{column}: {dict(dims)}")

    conn.close()


if __name__ == "__main__":
    main()
