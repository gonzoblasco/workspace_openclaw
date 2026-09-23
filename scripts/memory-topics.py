#!/usr/bin/env python3
"""
memory-topics.py - Discover topics via K-means clustering on embeddings.
Finds emergent themes in memory that aren't in the fixed topic list.

Usage:
  ./memory-topics.py [k]                 # cluster into k groups (default auto)
  ./memory-topics.py --list              # list existing topics
  ./memory-topics.py --refresh           # re-cluster and update topics table
"""

import sqlite3
import os
import sys
import json
import math
import random

# Vectores en BLOB float32 (nuevo) o JSON (legacy): el decoder compartido acepta ambos.
import importlib.util as _ilu

_spec = _ilu.spec_from_file_location(
    "vector_util", os.path.join(os.path.dirname(os.path.abspath(__file__)), "vector-util.py")
)
_vu = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_vu)
decode_vector = _vu.decode
import re
from collections import Counter
from pathlib import Path

DB_PATH = os.environ.get("MEMORY_DB", "memory/memory.db")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "qwen3-embedding:0.6b")


def get_embedding(text):
    """Get embedding via Ollama

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
                if "embedding" in data:
                    return data["embedding"]
                if "embeddings" in data and data["embeddings"]:
                    return data["embeddings"][0]
    except Exception as e:
        print(f"⚠️ Ollama fallback: {e}", file=sys.stderr)
    import hashlib
    h = hashlib.sha256(text.encode("utf-8", errors="ignore")).digest()
    return [float(i) for i in h]


def cosine_similarity(vec1, vec2):
    """Cosine similarity between two vectors"""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    dot = sum(a * b for a, b in zip(vec1, vec2))
    n1 = math.sqrt(sum(x * x for x in vec1))
    n2 = math.sqrt(sum(x * x for x in vec2))
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)


def load_chunks():
    """Load session chunks with their content snippets for labeling"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute(
        """SELECT sv.session_id, sv.query_vector, sv.chunk_index, s.date, s.content_bare
           FROM session_vectors sv
           JOIN sessions_relacional s ON s.id = sv.session_id
           WHERE sv.chunk_index = 0""".replace("sv.chunk_index = 0", "1=1")
    ).fetchall()
    conn.close()

    chunks = []
    for session_id, vec_json, chunk_idx, date, content in rows:
        vec = decode_vector(vec_json)
        if vec is None:
            continue
        chunks.append({
            "session_id": session_id,
            "vector": vec,
            "chunk_index": chunk_idx,
            "date": date,
            "content": (content or "")[chunk_idx * 1500 : (chunk_idx + 1) * 1500],
        })
    return chunks


def kmeans(clusters_data, k, max_iter=50):
    """Simple K-means clustering"""
    points = [c["vector"] for c in clusters_data]
    if not points:
        return []

    dim = len(points[0])
    # Initialize centroids with k-means++ (random distinct)
    centroids = []
    centroids.append(points[random.randrange(len(points))])
    while len(centroids) < k:
        # Pick point farthest from existing centroids
        best_dist = -1
        best_point = None
        for p in points:
            min_dist = min(cosine_similarity(p, c) for c in centroids)
            # Use negative distance (farthest = most dissimilar)
            if best_dist < -min_dist:  # track max dissimilarity
                pass  # keep
            d = -min_dist  # negative similarity = farther
            if d > best_dist:
                best_dist = d
                best_point = p
        if best_point is None:
            break
        centroids.append(best_point)
    centroids = centroids[:k]
    if len(centroids) < k:
        # Pad with random points
        while len(centroids) < k:
            centroids.append(points[random.randrange(len(points))])

    assignments = [0] * len(points)

    for _ in range(max_iter):
        # Assign
        changed = False
        for i, p in enumerate(points):
            best_k = 0
            best_sim = -1
            for cidx, c in enumerate(centroids):
                sim = cosine_similarity(p, c)
                if sim > best_sim:
                    best_sim = sim
                    best_k = cidx
            if assignments[i] != best_k:
                assignments[i] = best_k
                changed = True

        # Update centroids
        for cidx in range(k):
            cluster_points = [p for i, p in enumerate(points) if assignments[i] == cidx]
            if cluster_points:
                new_centroid = [sum(p[d] for p in cluster_points) / len(cluster_points) for d in range(dim)]
                centroids[cidx] = new_centroid

        if not changed:
            break

    # Return clusters
    cluster_map = {}
    for i, a in enumerate(assignments):
        cluster_map.setdefault(a, []).append(clusters_data[i])
    return [cluster_map.get(i, []) for i in range(k)]


def pick_k(clusters_data, max_k=8):
    """Auto-pick k using elbow heuristic on average within-cluster similarity"""
    from_chunks = len(clusters_data)
    if from_chunks <= 2:
        return max(1, from_chunks)
    # Simple heuristic: k = sqrt(n/2), capped
    k = min(max_k, max(2, int(math.sqrt(from_chunks / 2))))
    return k


def summarize_cluster(cluster):
    """Generate a readable name for a cluster based on frequent keywords"""
    all_text = " ".join(c["content"] for c in cluster)
    words = re.findall(r"[a-zA-Záéíóúñü]+", all_text.lower())
    # Stopwords (includes proper nouns and workflow terms that are too generic)
    stopwords = {
        "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
        "is", "are", "was", "were", "be", "been", "it", "this", "that", "as", "at",
        "la", "el", "los", "las", "un", "una", "de", "en", "que", "y", "con",
        "no", "se", "al", "por", "del", "para", "una", "unos", "unas",
        "session", "sessionkey", "agent", "dashboard", "status", "source",
        "gateway", "date", "time", "model", "main", "user", "assistant", "id",
        "2026", "aug", "august", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
        "ver", "mas", "como", "que", "cuando", "hacer", "ser", "haber", "uno", "todo",
        # Proper nouns / workflow terms too generic for a topic name
        "gonzo", "kanam", "commit", "handoff", "config", "memory", "archive",
        "archiving", "dailies", "daily", "files", "scripts", "check", "done",
        "openclaw", "workspace", "high", "pipeline", "review", "deepseek", "flash",
        "tenant", "system", "change", "changes", "next", "step", "need", "needs",
        "would", "could", "should", "will", "want", "make", "made", "used", "use",
    }
    filtered = [w for w in words if w not in stopwords and len(w) > 3]
    counts = Counter(filtered)

    # Get top meaningful words (exclude those with tiny counts)
    meaningful = [w for w, c in counts.most_common(30) if c >= 2][:6]
    if not meaningful:
        return None  # Skip cluster - only generic words
    return ", ".join(meaningful)


def assign_new_topics(cluster_map):
    """Insert discovered topics into DB and link to sessions"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for cluster_name, cluster in cluster_map.items():
        if not cluster_name or cluster_name == "untitled-cluster":
            continue
        # Insert topic if new
        display_name = cluster_name.split(", ")[0][:30]  # first keyword as name
        c.execute(
            "INSERT OR IGNORE INTO topics (name, description, created_at) VALUES (?, ?, datetime('now'))",
            (display_name, f"Auto-discovered: {cluster_name}"),
        )
        topic_id = c.execute("SELECT id FROM topics WHERE name=?", (display_name,)).fetchone()[0]

        # Link to sessions with moderate confidence
        for chunk in cluster:
            c.execute(
                """INSERT OR IGNORE INTO topic_sessions (session_id, topic_id, confidence)
                   VALUES (?, ?, 0.5)""",
                (chunk["session_id"], topic_id),
            )

    conn.commit()
    conn.close()


def recalc_fixed_topics():
    """Reassign fixed topics by real keyword matching (more discriminative than embeddings).
    Fixed topics are those NOT marked 'Auto-discovered'."""
    topic_keywords = {
        "soporteml": ["soporteml", "mercado", "meli", "ml ", "vendedor"],
        "accessibility": ["accessib", "a11y", "accesib"],
        "git": ["git", "commit", "push", "rebase", "merge", "branch"],
        "linkedin": ["linkedin", "post", "branding"],
        "agentic": ["agentic", "pipeline", "agente", "subagente", "orquestad"],
        "kanam-skills": ["kanam-skills", "skill", "skills"],
        "assessment": ["assessment", "interview", "entrevista", "samarth", "hiring"],
    }

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sessions = c.execute(
        "SELECT id, date, content_bare FROM sessions_relacional"
    ).fetchall()

    print("\nRecalculando topics fijos por keywords...")
    for topic, kws in topic_keywords.items():
        tid = c.execute("SELECT id FROM topics WHERE name=?", (topic,)).fetchone()
        if not tid:
            continue
        tid = tid[0]
        c.execute("DELETE FROM topic_sessions WHERE topic_id=?", (tid,))
        count = 0
        for sid, date, content in sessions:
            content_lower = (content or "").lower()
            if any(kw in content_lower for kw in kws):
                c.execute(
                    "INSERT OR IGNORE INTO topic_sessions (session_id, topic_id, confidence) VALUES (?,?,?)",
                    (sid, tid, 0.9),
                )
                count += 1
        print(f"  {topic}: {count} sesiones")

    conn.commit()
    conn.close()


def main():
    chunks = load_chunks()
    if not chunks:
        print("No chunks found in DB. Run memory-catalog-v2.py first.")
        sys.exit(1)

    if "--list" in sys.argv:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(
            """SELECT t.name, t.description, COUNT(ts.session_id)
               FROM topics t LEFT JOIN topic_sessions ts ON t.id = ts.topic_id
               GROUP BY t.id ORDER BY COUNT(ts.session_id) DESC"""
        ).fetchall()
        print("\n🏷️  Topics")
        print("=" * 60)
        for name, desc, count in rows:
            print(f"  • {name} ({count} sesiones) - {desc or ''}")
        conn.close()
        return

    # Recalc fixed topics by keyword
    recalc_fixed_topics()

    # Determine k
    k_opt = None
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        k_opt = int(sys.argv[1])
    else:
        k_opt = pick_k(chunks)

    print(f"Running K-means clustering with k={k_opt} on {len(chunks)} chunks...")

    random.seed(42)  # deterministic
    cluster_map = kmeans(chunks, k_opt)

    # Label clusters
    named = {}
    for i, cluster in enumerate(cluster_map):
        if not cluster:
            continue
        label = summarize_cluster(cluster)
        if label is None:
            print("\n  Cluster {i + 1}: (genérico, omitido)")
            continue
        named[label] = cluster
        dates = sorted(set(c["date"][:10] for c in cluster))
        print(f"\n  Cluster {i + 1}: {label}")
        print(f"    {len(cluster)} chunks | fechas: {', '.join(dates[:5])}")

    if "--refresh" in sys.argv:
        print("\n⚙️  Assigning discovered topics to DB...")
        assign_new_topics(named)
        print("   Done.")

    # Show existing fixed topics for contrast
    print("\n" + "=" * 60)
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        """SELECT t.name, COUNT(ts.session_id) FROM topics t
           LEFT JOIN topic_sessions ts ON t.id = ts.topic_id
           GROUP BY t.id HAVING COUNT(ts.session_id) > 0 ORDER BY 2 DESC"""
    ).fetchall()
    print("Existing topics with sessions:")
    for name, count in rows:
        print(f"  • {name} ({count})")
    conn.close()


if __name__ == "__main__":
    main()
