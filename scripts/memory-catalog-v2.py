#!/usr/bin/env python3
"""
memory-catalog-v2.py - Memory to SQLite with semantic topic extraction
Improvements over v1:
- Idempotent (upsert by date, no duplicates on re-run)
- Semantic topic inference using cosine similarity to topic centroids
- Absorbe la tabla gemela: los vectores de learnings viven en `learnings`
  (la tabla `learnings_enriquecido` se elimino en ADR-058: duplicaba el 94% del texto).
- Handles embedding generation with Ollama fallback to hash
"""

import sqlite3
import os
import re
import sys
import json
import hashlib
import math
from pathlib import Path

# Vectores en BLOB float32 (nuevo) o JSON (legacy): decoder/encoder compartidos.
# Asi el catalogo sigue leyendo vectores viejos y escribe siempre el formato nuevo.
import importlib.util as _ilu

_spec = _ilu.spec_from_file_location(
    "vector_util", os.path.join(os.path.dirname(os.path.abspath(__file__)), "vector-util.py")
)
_vu = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_vu)
decode_vector = _vu.decode
encode_vector = _vu.encode
from datetime import datetime

DB_PATH = os.environ.get("MEMORY_DB", "memory/memory.db")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "qwen3-embedding:0.6b")

CHUNK_SIZE = 1500
MAX_CHUNKS_PER_SESSION = 3
TAG_THRESHOLD = 0.7


def get_embedding(text, use_ollama=True):
    """Get embedding vector from text via Ollama (fallback to hash)

    Uses urllib (stdlib) instead of requests: the system python has no
    requests installed, which silently forced every call into the SHA-256
    fallback and produced useless 32-dim vectors.
    """
    try:
        if not use_ollama:
            h = hashlib.sha256(text.encode("utf-8", errors="ignore")).digest()
            return [float(i) for i in h]

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
        print(f"⚠️ Ollama fallback: {e}", file=sys.stderr)

    print(
        "⚠️ Usando hash SHA-256 (32 dims) como vector: NO sirve para busqueda "
        f"semantica real. Revisar Ollama en {OLLAMA_BASE} con {EMBED_MODEL}. "
        "Reparar los vectores luego con scripts/memory-reembed.py",
        file=sys.stderr,
    )
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


def compute_topic_centroids():
    """Compute average embedding (centroid) for each topic from existing sessions"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    rows = c.execute(
        """
        SELECT sv.session_id, sv.query_vector, t.name
        FROM session_vectors sv
        JOIN topic_sessions ts ON sv.session_id = ts.session_id
        JOIN topics t ON ts.topic_id = t.id
        WHERE sv.chunk_index = 0
    """
    ).fetchall()

    centroids = {}
    counts = {}
    for session_id, vec_json, topic_name in rows:
        vec = decode_vector(vec_json)
        if vec is None:
            continue
        # Robustness: some sessions were catalogued with a different embedding
        # model (32-dim vs the current 1024-dim qwen3). Only mix vectors of the
        # same dimensionality per topic, otherwise centroid math breaks.
        if not vec or not isinstance(vec[0], (int, float)):
            continue
        if topic_name not in centroids:
            centroids[topic_name] = [0.0] * len(vec)
            counts[topic_name] = 0
        elif len(vec) != len(centroids[topic_name]):
            # Different dims for the same topic - keep the most common one.
            # Simple, safe: skip this vector (centroid stays from first dim).
            continue
        for i, v in enumerate(vec):
            centroids[topic_name][i] += v
        counts[topic_name] += 1

    conn.close()

    # Only keep centroids for topics with >= 2 sessions (reliable signal)
    reliable = {t for t, cnt in counts.items() if cnt >= 2}
    centroids = {t: v for t, v in centroids.items() if t in reliable}

    for topic, vec in centroids.items():
        c = counts.get(topic, 0)
        if c > 0:
            centroids[topic] = [v / c for v in vec]
        else:
            centroids[topic] = [0.0] * len(vec)

    return centroids


def extract_topics_from_content(content, centroids=None):
    """Extract topics using semantic similarity to topic centroids"""
    if centroids is None:
        centroids = compute_topic_centroids()

    content_embedding = get_embedding(content)

    potential_topics = {
        "git": "Git workflow",
        "soporteml": "SoporteML CRM project",
        "accessibility": "a11y / accessibility features",
        "linkedin": "LinkedIn branding/marketing",
        "assessment": "Interview/assessment preparation",
        "kanam-skills": "Skills repository management",
        "agentic": "Agentic AI workflows",
        "infrastructure": "Infrastructure setup/ops",
    }

    found_topics = {}

    for keyword, description in potential_topics.items():
        if keyword in centroids:
            topic_vec = centroids[keyword]
            similarity = cosine_similarity(content_embedding, topic_vec)
            if similarity > 0.75:
                found_topics[keyword] = description
        else:
            # Fallback to keyword density if centroid not available
            pattern = re.compile(r"\b" + keyword + r"\b", re.IGNORECASE)
            sections = re.split(r"\n---\n|\n## ", content, flags=re.MULTILINE)
            total_mentions = sum(len(pattern.findall(s)) for s in sections)
            if total_mentions >= 2:
                found_topics[keyword] = description

    return list(found_topics.items())


def extract_learnings(content):
    """Extract learning sections from content. More selective: only treat
    ### headers as learnings if they look like real learning entries (not generic sections)."""
    learnings = []
    section_pattern = re.compile(r"^###\s+(.+?)\s*$")

    # Learning-like keywords that indicate a real learning entry
    learning_kws = ["learn", "lesson", "leccion", "aprend", "insight", "tip", "clave",
                    "key", "takeaway", "conclusion"]

    lines = content.split("\n")
    current_learning = {}

    for line in lines:
        line = line.strip()
        match = section_pattern.match(line)
        if match:
            if current_learning and "content" in current_learning:
                learnings.append(current_learning)
            # Only start a learning if title looks like a real learning
            title = match.group(1)
            title_low = title.lower()
            is_learning = any(kw in title_low for kw in learning_kws)
            current_learning = {"title": title, "is_learning": is_learning}
        elif current_learning and line:
            current_learning.setdefault("content", "")
            current_learning["content"] += " " + line

    if current_learning and "content" in current_learning:
        learnings.append(current_learning)

    # Filter: only return sections that look like real learnings
    return [l for l in learnings if l.get("is_learning")] or learnings[:0]


def compute_category_centroids(min_examples=5):
    """Compute average embedding (centroid) for each learning category.
    Only returns centroids for categories with >= min_examples (reliable signal)."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    rows = c.execute(
        "SELECT category, learning_vector FROM learnings WHERE learning_vector IS NOT NULL"
    ).fetchall()
    conn.close()

    centroids = {}
    counts = {}
    skipped = {}
    for category, vec_json in rows:
        vec = decode_vector(vec_json)
        if vec is None:
            continue
        # Robustness: some learnings were catalogued with a different embedding
        # model (32-dim SHA-256 fallback vs the current 1024-dim qwen3). Mixing
        # dimensions in one centroid raises IndexError. Same guard as
        # compute_topic_centroids: only mix same-dimensional vectors per
        # category; skip the rest.
        if not vec or not isinstance(vec[0], (int, float)):
            continue
        if category not in centroids:
            centroids[category] = [0.0] * len(vec)
            counts[category] = 0
            skipped[category] = 0
        elif len(vec) != len(centroids[category]):
            skipped[category] = skipped.get(category, 0) + 1
            continue
        for i, v in enumerate(vec):
            centroids[category][i] += v
        counts[category] += 1

    # Only keep categories with enough examples
    reliable = {cat for cat, cnt in counts.items() if cnt >= min_examples}
    centroids = {cat: v for cat, v in centroids.items() if cat in reliable}

    if skipped:
        total = sum(skipped.values())
        det = ", ".join(f"{cat}:{n}" for cat, n in sorted(skipped.items()) if n)
        print(f"ℹ️  Centroides: {total} vector(es) de dimension distinta omitidos ({det})", file=sys.stderr)

    for cat, vec in centroids.items():
        cnt = counts.get(cat, 0)
        if cnt > 0:
            centroids[cat] = [v / cnt for v in vec]
        else:
            centroids[cat] = [0.0] * len(vec)

    return centroids


def categorize_learning(learning_text, category_centroids=None):
    """Assign a learning to the category whose centroid is most similar.
    Falls back to keyword matching if no reliable centroid exists."""
    if category_centroids is None:
        category_centroids = compute_category_centroids()

    # Keyword fallback (also catches obvious keywords)
    title_low = learning_text.lower()
    if any(kw in title_low for kw in ["accessib", "accesib", " a11y", "wcag", "screen reader"]):
        return "a11y"
    if any(kw in title_low for kw in ["infraestruct", "server setup", "deploy to", "devops", "docker", "kubernetes"]):
        return "infraestructura"
    if any(kw in title_low for kw in ["open source", "contribution", "astryx", "radix", " github", "pull request", "pr "]):
        return "oss"
    if any(kw in title_low for kw in ["agent", "subagent", "orchestr", "pipeline a/b"]):
        return "pipeline-agentes"

    # Workspace / memory / script workflow notes are methodology (Kanam work)
    if any(kw in title_low for kw in ["memory", "script", "workspace", "learnings",
                                       "memoria", "catalog", "busqueda", "archiv",
                                       "daily", "handoff", "session", "skey"]):
        return "metodologia"

    # Embedding-based: pick closest category centroid
    embedding = get_embedding(learning_text)
    best_cat = None
    best_sim = -1
    for cat, centroid in category_centroids.items():
        sim = cosine_similarity(embedding, centroid)
        if sim > best_sim:
            best_sim = sim
            best_cat = cat

    if best_cat is not None and best_sim > 0.35:  # Tunable threshold
        return best_cat

    return "metodologia"  # Default


def create_schema():
    """Create database schema if not exists"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions_relacional (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            tags TEXT,
            complexity_score INTEGER DEFAULT 0,
            model_used TEXT DEFAULT 'unknown',
            thinking_level TEXT DEFAULT 'high',
            summary TEXT,
            session_duration INTEGER DEFAULT 0,
            agent_id TEXT,
            content_bare TEXT NOT NULL,
            created_at TEXT
        )
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS session_vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            query_vector BLOB NOT NULL,
            relevance_score REAL DEFAULT 0.0,
            chunk_index INTEGER DEFAULT 0,
            chunk_text TEXT,
            created_at TEXT,
            FOREIGN KEY(session_id) REFERENCES sessions_relacional(id)
        )
    """
    )

    # Migration: older databases created session_vectors without chunk_text
    # (the column arrived later via memory-catalog-simple.sh). Without it,
    # semantic search returns matches with empty text.
    sv_cols = {r[1] for r in c.execute("PRAGMA table_info(session_vectors)")}
    if "chunk_text" not in sv_cols:
        c.execute("ALTER TABLE session_vectors ADD COLUMN chunk_text TEXT")

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT,
            description TEXT,
            created_at TEXT
        )
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS topic_sessions (
            session_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            confidence REAL DEFAULT 0.5,
            PRIMARY KEY (session_id, topic_id),
            FOREIGN KEY(session_id) REFERENCES sessions_relacional(id),
            FOREIGN KEY(topic_id) REFERENCES topics(id)
        )
    """
    )

    conn.commit()
    return conn


def catalog_session(conn, content, date_str, detected_topics):
    """Upsert a single session into sessions_relacional"""
    c = conn.cursor()

    # Better summary: representative section (more informative than raw head)
    summary = extract_representative_section(content, max_chars=300)

    existing = c.execute(
        "SELECT id FROM sessions_relacional WHERE date=?", (date_str,)
    ).fetchone()

    if existing:
        session_id = existing[0]
        c.execute(
            """UPDATE sessions_relacional SET
               title=?, tags=?, summary=?, content_bare=?, created_at=?
               WHERE id=?""",
            (
                date_str,
                "",
                summary,
                content,
                datetime.now().isoformat(),
                session_id,
            ),
        )
        c.execute("DELETE FROM session_vectors WHERE session_id=?", (session_id,))
    else:
        c.execute(
            """INSERT INTO sessions_relacional
               (id, date, title, tags, model_used, thinking_level, summary, content_bare, created_at)
               VALUES (?, ?, ?, ?, 'unknown', 'high', ?, ?, ?)""",
            (
                None,
                date_str,
                date_str,
                "",
                summary,
                content,
                datetime.now().isoformat(),
            ),
        )
        session_id = c.execute(
            "SELECT id FROM sessions_relacional WHERE date=?", (date_str,)
        ).fetchone()[0]

    return session_id

    conn.commit()


def extract_representative_section(content, max_chars=2000):
    """Extract the most informative section from a daily note.
    Prefers sections under ## headers over raw leading content.
    Returns the best section text for embedding."""
    lines = content.split("\n")
    sections = []  # (title, text)
    current_title = ""
    current_text = []

    for line in lines:
        if line.startswith("## ") and current_title:
            sections.append((current_title, " ".join(current_text)))
            current_title = line.strip().lstrip("#").strip()
            current_text = []
        elif line.startswith("## "):
            current_title = line.strip().lstrip("#").strip()
        elif current_title and line.strip():
            current_text.append(line.strip())

    if current_title and current_text:
        sections.append((current_title, " ".join(current_text)))

    if not sections:
        return content[:max_chars]

    # Prefer sections whose title suggests substance: achievement, insight, decision, result
    preferred_keywords = ["achievement", "insight", "decision", "result", "summary", "logro",
                          "decision", "conclusion", "aprendizaje", "learn", "hicimos", "avance"]
    best_idx = 0
    best_score = -1
    for i, (title, text) in enumerate(sections):
        score = 0
        title_low = title.lower()
        for kw in preferred_keywords:
            if kw in title_low:
                score += 3
        # Longer substantive sections score higher
        if 100 <= len(text) <= max_chars:
            score += 1
        if score > best_score:
            best_score = score
            best_idx = i

    title, text = sections[best_idx]
    combined = f"{title}: {text}"
    return combined[:max_chars]


def catalog_memory():
    """Main cataloging function"""
    print("Memory Catalog v2 - Starting...")
    print("=" * 60)

    conn = create_schema()
    c = conn.cursor()

    memory_dir = Path("memory")
    if not memory_dir.exists():
        print("Error: memory/ directory not found")
        return

    md_files = sorted(memory_dir.glob("*.md"))
    daily_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}(-\d{4})?$")
    md_files = [f for f in md_files if daily_pattern.match(f.stem)]

    print(f"Found {len(md_files)} daily files to catalog...")

    for i, md_file in enumerate(md_files, 1):
        date_str = md_file.stem

        with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        print(f"\n{i}/{len(md_files)} Cataloging: {date_str[:10]}")

        # Extract topics (first pass with existing centroids)
        detected_topics = extract_topics_from_content(content)

        # Insert/update session
        session_id = catalog_session(conn, content, date_str, detected_topics)

        # Generate chunk vectors - chunk 0 is the representative section (most informative)
        representative = extract_representative_section(content)
        chunks = [representative]
        # Add raw content chunks for coarse coverage (skip the representative section to avoid dup)
        raw_chunks = [
            content[j : j + CHUNK_SIZE] for j in range(0, len(content), CHUNK_SIZE)
        ]  # include first chunk for continuity
        for cchunk in raw_chunks[:MAX_CHUNKS_PER_SESSION - 1]:
            chunks.append(cchunk)

        for chunk_idx, chunk in enumerate(chunks):
            chunk_embedding = get_embedding(chunk)
            relevance = TAG_THRESHOLD if (detected_topics and chunk_idx == 0) else 0.0
            c.execute(
                """INSERT INTO session_vectors
                   (session_id, query_vector, relevance_score, chunk_index, chunk_text, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    session_id,
                    encode_vector(chunk_embedding),
                    relevance,
                    chunk_idx,
                    chunk,
                    datetime.now().isoformat(),
                ),
            )

        # Process topics
        for keyword, description in detected_topics:
            c.execute(
                "INSERT OR IGNORE INTO topics (name, category, description) VALUES (?, ?, ?)",
                (keyword, description, description[:100]),
            )
            topic_id = c.execute(
                "SELECT id FROM topics WHERE name=?", (keyword,)
            ).fetchone()
            if topic_id:
                c.execute(
                    """INSERT OR IGNORE INTO topic_sessions
                       (session_id, topic_id, confidence)
                       VALUES (?, ?, ?)""",
                    (session_id, topic_id[0], TAG_THRESHOLD),
                )

        # Extract learnings from markdown (only real learning entries + categorize)
        for learning in extract_learnings(content):
            if not learning.get("content"):
                continue
            title = learning.get("title", "")
            content_text = learning.get("content", "")[:500]

            # Skip if a learning with this title already exists
            exists = c.execute(
                "SELECT id FROM learnings WHERE title=? LIMIT 1", (title,)
            ).fetchone()
            if exists:
                continue

            # Categorize using embeddings (with keyword fallback)
            category = categorize_learning(title + " " + content_text)

            learning_embedding = get_embedding(content_text)
            c.execute(
                """INSERT INTO learnings
                   (category, title, content, tags, learning_vector, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))""",
                (category, title, content_text, "", encode_vector(learning_embedding)),
            )

    # Rellenar el vector de los learnings que todavia no lo tengan.
    # Antes esto copiaba TODA la tabla a una gemela; ahora el vector vive en
    # la misma fila, asi que solo se completan los que faltan (ADR-058).
    existing = c.execute(
        "SELECT id, title, content FROM learnings WHERE learning_vector IS NULL"
    ).fetchall()
    for lid, ltitle, lcontent in existing:
        if not lcontent:
            continue
        learning_embedding = get_embedding(lcontent[:500])
        c.execute(
            "UPDATE learnings SET learning_vector=?, updated_at=datetime('now') WHERE id=?",
            (encode_vector(learning_embedding), lid),
        )

    conn.commit()

    # Summary
    print(f"\n{'=' * 60}")
    print("✅ Cataloging complete!\n")
    print("Database Summary:")
    print(f"   - sessions_relacional: {c.execute('SELECT COUNT(*) FROM sessions_relacional').fetchone()[0]}")
    print(f"   - session_vectors: {c.execute('SELECT COUNT(*) FROM session_vectors').fetchone()[0]}")
    print(f"   - topics: {c.execute('SELECT COUNT(*) FROM topics').fetchone()[0]}")
    print(
        f"   - topic_sessions mappings: {c.execute('SELECT COUNT(*) FROM topic_sessions').fetchone()[0]}"
    )
    print(
        f"   - learnings (with vectors): {c.execute('SELECT COUNT(*) FROM learnings WHERE learning_vector IS NOT NULL').fetchone()[0]}"
    )

    conn.close()


if __name__ == "__main__":
    catalog_memory()
