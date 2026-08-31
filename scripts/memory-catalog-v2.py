#!/usr/bin/env python3
"""
memory-catalog-v2.py - Memory to SQLite with semantic topic extraction
Improvements over v1:
- Better tag/topic extraction from actual content (not just markdown syntax)
- Completes learnings_enriquecido table
- Includes cosine similarity for semantic search
- More robust chunking
"""

import sqlite3
import os
import re
import sys
import json
import hashlib
import math
from pathlib import Path
from datetime import datetime

DB_PATH = os.environ.get("MEMORY_DB", "memory/memory.db")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text:latest")

# Configuration
CHUNK_SIZE = 1500
MAX_CHUNKS_PER_SESSION = 3
TAG_THRESHOLD = 0.7  # Minimum confidence for topic assignment


def get_embedding(text, use_ollama=True):
    """Get embedding vector from text"""
    try:
        if not use_ollama:
            # Fallback to SHA256 hash
            h = hashlib.sha256(text.encode("utf-8", errors="ignore")).digest()
            return [float(i) for i in h]

        import requests
        response = requests.post(
            f"{OLLAMA_BASE}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": text[:768], "n_preamble": 0, "n_context": 768, "n_predict": 0},
            timeout=25,
        )

        if response.status_code == 200 and "embeddings" in response.json():
            return response.json()["embeddings"][0]
    except Exception as e:
        print(f"⚠️ Embedding fallback (Ollama unavailable): {e}", file=sys.stderr)

    # Default fallback
    h = hashlib.sha256(text.encode("utf-8", errors="ignore")).digest()
    return [float(i) for i in h]


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(x * x for x in vec1))
    norm2 = math.sqrt(sum(x * x for x in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def extract_topics_from_content(content):
    """Extract meaningful topics from content using semantic analysis"""
    # Define potential topic keywords found in daily content
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

    # Extract topics based on keyword density
    found_topics = {}

    for keyword, description in potential_topics.items():
        pattern = re.compile(r"\b" + keyword + r"\b", re.IGNORECASE)

        # Search in all content sections (between --- dividers or major headers)
        sections = re.split(r"\n---\n|\n## ", content, flags=re.MULTILINE)
        total_mentions = 0

        for section in sections:
            matches = pattern.findall(section)
            total_mentions += len(matches)

        # Count meaningful mentions (at least 2 occurrences)
        if total_mentions >= 2:
            found_topics[keyword] = description

    return list(found_topics.items())


def extract_learnings(content):
    """Extract learning sections from content"""
    learnings = []

    # Pattern to find "### Topic Title" followed by content until next ### or end
    section_pattern = re.compile(r"^###\s+(.+?)\s*$")

    lines = content.split("\n")
    current_learning = {}

    for line in lines:
        line = line.strip()

        # Check if this is a learning title (###)
        match = section_pattern.match(line)
        if match:
            # Save previous learning if exists
            if current_learning and "content" in current_learning:
                learnings.append(current_learning)

            # Start new learning section
            current_learning = {"title": match.group(1)}
        elif current_learning and line:
            # Continue accumulating content for current learning
            if "content" not in current_learning:
                current_learning["content"] = ""
            current_learning["content"] += " " + line

    # Don't forget last learning
    if current_learning and "content" in current_learning:
        learnings.append(current_learning)

    return learnings


def create_schema():
    """Create database schema with all tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. sessions_relacional
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
            created_at TEXT,
            FOREIGN KEY(id) REFERENCES daily_notes(id) ON DELETE CASCADE
        )
        """
    )

    # 2. session_vectors
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS session_vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            query_vector TEXT NOT NULL,
            relevance_score REAL DEFAULT 0.0,
            chunk_index INTEGER DEFAULT 0,
            created_at TEXT,
            FOREIGN KEY(session_id) REFERENCES sessions_relacional(id) ON DELETE CASCADE
        )
        """
    )

    # 3. topics
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

    # 4. topic_sessions
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS topic_sessions (
            session_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            confidence REAL DEFAULT 0.5,
            FOREIGN KEY(session_id) REFERENCES sessions_relacional(id),
            FOREIGN KEY(topic_id) REFERENCES topics(id)
        )
        """
    )

    # 5. learnings_enriquecido
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS learnings_enriquecido (
            id INTEGER PRIMARY KEY,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            learning_vector TEXT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(id) REFERENCES learnings(id)
        )
        """
    )

    conn.commit()
    return conn


def catalog_memory():
    """Main cataloging function"""
    print("Memory Catalog v2 - Starting...")
    print("=" * 60)

    # Ensure database exists and schema is created
    conn = create_schema()
    c = conn.cursor()

    # Get all markdown files from memory directory
    memory_dir = Path("memory")
    if not memory_dir.exists():
        print("Error: memory/ directory not found")
        return

    md_files = sorted(memory_dir.glob("*.md"))
    # Only catalog daily files: YYYY-MM-DD or YYYY-MM-DD-HHMM pattern
    daily_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}(-\d{4})?$")
    md_files = [f for f in md_files if daily_pattern.match(f.stem)]
    processed_count = 0

    for i, md_file in enumerate(md_files, 1):
        with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Extract metadata
        date_str = md_file.stem

        # Extract topics using semantic analysis
        detected_topics = extract_topics_from_content(content)

        # Generate embeddings for main content
        print(f"\n{i}/{len(md_files)} Cataloging: {date_str[:10]}")

        # Insert into sessions_relacional (upsert by date - no duplicates)
        existing = c.execute(
            "SELECT id FROM sessions_relacional WHERE date=?", (date_str,)
        ).fetchone()
        if existing:
            session_id = existing[0]
            c.execute(
                """UPDATE sessions_relacional SET
                   title=?, tags=?, summary=?, content_bare=?, created_at=?
                   WHERE id=?""",
                (date_str, "", content[:200], content, datetime.now().isoformat(), session_id),
            )
            # Remove old vectors for this session (will re-insert fresh)
            c.execute("DELETE FROM session_vectors WHERE session_id=?", (session_id,))
        else:
            c.execute(
                """INSERT INTO sessions_relacional
                   (id, date, title, tags, model_used, thinking_level, summary, content_bare, created_at)
                   VALUES (?, ?, ?, ?, 'unknown', 'high', ?, ?, ?)""",
                (None, date_str, date_str, "", content[:200], content, datetime.now().isoformat()),
            )
            session_id = c.execute(
                "SELECT id FROM sessions_relacional WHERE date=?", (date_str,)
            ).fetchone()[0]
        conn.commit()

        # Generate vectors for chunked content
        chunks = [content[j : j + CHUNK_SIZE] for j in range(0, len(content), CHUNK_SIZE)][
            :MAX_CHUNKS_PER_SESSION
        ]

        for chunk_idx, chunk in enumerate(chunks):
            chunk_embedding = get_embedding(chunk)

            # Insert vector with relevance score
            relevance = TAG_THRESHOLD if (detected_topics and chunk_idx == 0) else 0.0
            c.execute(
                """INSERT INTO session_vectors
                   (session_id, query_vector, relevance_score, chunk_index, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (session_id, json.dumps(chunk_embedding), relevance, chunk_idx, datetime.now().isoformat()),
            )

        # Process detected topics and link to sessions
        for keyword, description in detected_topics:
            try:
                c.execute(
                    "INSERT OR IGNORE INTO topics (name, category, description) VALUES (?, ?, ?)",
                    (keyword, description, description[:100]),
                )
            except sqlite3.IntegrityError:
                pass

            # Link to session
            topic_id = c.execute("SELECT id FROM topics WHERE name=?", (keyword,)).fetchone()
            if topic_id:
                c.execute(
                    """INSERT OR IGNORE INTO topic_sessions
                       (session_id, topic_id, confidence)
                       VALUES (?, ?, ?)""",
                    (session_id, topic_id[0], TAG_THRESHOLD),
                )

        # Extract and process learnings from markdown (best-effort)
        learnings = extract_learnings(content)
        for learning in learnings:
            if not learning.get("content"):
                continue

            title = learning.get("title", "")
            content_text = learning.get("content", "")[:500]

            # Try to categorize learning
            if any(kw in title.lower() for kw in ["access", "a11y"]):
                category = "a11y"
            elif any(kw in title.lower() for kw in ["infrastructure", "setup"]):
                category = "infraestructura"
            elif any(kw in title.lower() for kw in ["method", "process", "pipeline"]):
                category = "metodologia"
            else:
                continue  # Skip if we can't categorize

            # Generate learning embedding
            learning_embedding = get_embedding(content_text)

            # Insert directly (new row, no fragile LIKE matching)
            c.execute(
                """INSERT INTO learnings_enriquecido
                   (category, title, content, tags, learning_vector, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))""",
                (category, title, content_text, "", json.dumps(learning_embedding)),
            )

    # Populate learnings_enriquecido from the existing learnings table (source of truth)
    # This is the main path: curated learnings get embeddings.
    existing = c.execute("SELECT id, category, title, content, tags FROM learnings").fetchall()
    for row in existing:
        lid, lcat, ltitle, lcontent, ltags = row
        if not lcontent:
            continue
        learning_embedding = get_embedding(lcontent[:500])
        c.execute(
            """INSERT OR REPLACE INTO learnings_enriquecido
               (id, category, title, content, tags, learning_vector, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))""",
            (lid, lcat, ltitle, lcontent, ltags or "", json.dumps(learning_embedding)),
        )

    conn.commit()
    processed_count += 1

    # Print summary
    print(f"\n{'=' * 60}")
    print("✅ Cataloging complete!")
    print("\nDatabase Summary:")
    c.execute("SELECT COUNT(*) FROM sessions_relacional")
    print(f"  - sessions_relacional: {c.fetchone()[0]}")

    c.execute("SELECT COUNT(*) FROM session_vectors")
    print(f"  - session_vectors: {c.fetchone()[0]}")

    c.execute("SELECT COUNT(DISTINCT name) FROM topics")
    print(f"  - topics: {c.fetchone()[0]}")

    c.execute("SELECT COUNT(*) FROM topic_sessions")
    print(f"  - topic_sessions mappings: {c.fetchone()[0]}")

    c.execute("SELECT COUNT(*) FROM learnings_enriquecido WHERE learning_vector IS NOT NULL")
    print(f"  - learnings_enriquecido (with vectors): {c.fetchone()[0]}")

    # Show example semantic search capability
    print("\n🔍 Semantic Search Ready:")
    c.execute(
        "SELECT t.name, t.description FROM topics t JOIN topic_sessions ts ON t.id = ts.topic_id GROUP BY t.id"
    )
    results = c.fetchall()
    if results:
        for name, desc in results[:5]:
            print(f"  • {name}: {(desc or '')[:80]}...")


if __name__ == "__main__":
    catalog_memory()
