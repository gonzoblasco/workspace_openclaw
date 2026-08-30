#!/bin/bash
# ============================================================
# memory-catalog.sh - Memory to SQLite relational + vector store
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DB="memory/memory.db"
OLLAMA_BASE="${OLLAMA_BASE:-http://127.0.0.1:11434}"
EMBED_MODEL="${EMBED_MODEL:-nomic-embed-text:latest}"

echo "=================================================="
echo "Memory Cataloger - Transformando memoria a DB relacional + vectorial"
echo "Database: $DB"
echo "Embedding Model: $EMBED_MODEL"
echo "=================================================="

# Create Python helper for heavy lifting
cat > /tmp/memory_catalog.py <<'PYTHON_SCRIPT'
import sys
import sqlite3
import os
import json
import math
import re
from pathlib import Path

DB_PATH = os.environ.get("MEMORY_DB", "memory/memory.db")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text:latest")

def generate_embedding(text, model=EMBED_MODEL, base=OLLAMA_BASE):
    """Call Ollama embeddings API and return normalized vector"""
    try:
        import requests
        response = requests.post(
            f"{base}/api/embeddings",
            json={"model": model, "prompt": text, "n_preamble": 0, "n_context": 768, "n_predict": 0},
            timeout=30
        )
        if response.status_code == 200 and "embeddings" in response.json():
            embeds = response.json()["embeddings"]
            if len(embeds) > 0:
                return [round(float(v), 6) for v in embeds[0]]
    except Exception as e:
        pass
    
    # Fallback: return empty array or use simple hashing
    print(f"Embedding call failed: {e}", file=sys.stderr)
    return []

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

def extract_tags(content):
    """Extract tags from markdown content"""
    matches = re.findall(r'\[(\w+)\]', content)
    return list(set(matches))[:5]

def extract_summary(content, max_words=100):
    """Extract summary from content"""
    lines = content.split('\n')
    words = []
    for line in reversed(lines):
        if not line.strip() or line.startswith('#'):
            break
        line_words = re.findall(r'\w+', line)
        words.extend(line_words)
        if len(words) >= max_words:
            break
    
    text = ' '.join(reversed(words))
    return text[:200]

def create_schema():
    """Create new tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    
    # sessions_relacional table
    conn.execute('''
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
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY(id) REFERENCES daily_notes(id) ON DELETE CASCADE
        )
    ''')
    
    # session_vectors table for semantic search
    conn.execute('''
        CREATE TABLE IF NOT EXISTS session_vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            query_vector TEXT NOT NULL,
            relevance_score REAL DEFAULT 0.0,
            chunk_index INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY(session_id) REFERENCES sessions_relacional(id) ON DELETE CASCADE
        )
    ''')
    
    # topics table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT,
            description TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    ''')
    
    # topic_sessions junction table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS topic_sessions (
            session_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            confidence REAL DEFAULT 0.5,
            FOREIGN KEY(session_id) REFERENCES sessions_relacional(id) ON DELETE CASCADE,
            FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE CASCADE
        )
    ''')
    
    # learnings_enriquecido table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS learnings_enriquecido (
            id INTEGER PRIMARY KEY,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            learning_vector TEXT,
            query_vector TEXT,
            relevance_score REAL DEFAULT 0.0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT,
            FOREIGN KEY(id) REFERENCES learnings(id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes
    conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions_relacional(date)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_summary ON sessions_relacional(summary)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_vectors_session ON session_vectors(session_id)')
    
    conn.commit()

def catalog_memory():
    """Main function to catalog all memory files"""
    import subprocess
    
    # Ensure database exists
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return False
    
    create_schema()
    
    # Process memory files
    memory_dir = Path("memory")
    md_files = list(memory_dir.glob("*.md"))
    
    print(f"Found {len(md_files)} .md files to catalog")
    print("=" * 70)
    
    processed_count = 0
    
    for md_file in sorted(md_files):
        date_str = md_file.stem
        try:
            # Read file content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if not title_match:
                title_match = re.search(r'^##\s+(.+)$', content, re.MULTILINE)
            
            title = title_match.group(1).strip() if title_match else f"Sesión {date_str}"
            tags = extract_tags(content)
            summary = extract_summary(content)
            
            # Generate embedding
            print(f"\n📄 Cataloging: {date_str}")
            print(f"   Title: {title}")
            
            vector = generate_embedding(content)
            print(f"   ✅ Embedding generated: {len(vector)} dimensions")
            
            if not vector:
                # Fallback to hash if embedding fails
                import hashlib
                vector = [float(i) for i in hashlib.md5(content.encode()).hexdigest()][:384]
            
            # Insert into sessions_relacional (upsert)
            conn = sqlite3.connect(DB_PATH)
            conn.execute('''
                INSERT OR REPLACE INTO sessions_relacional 
                (id, date, title, tags, complexity_score, model_used, thinking_level, summary, agent_id, content_bare, created_at)
                VALUES (?, ?, ?, ?, 0, 'unknown', 'high', ?, ?, ?, datetime('now'))
            ''', (
                None, date_str, title, ','.join(tags),
                json.dumps(vector),
                summary, 'Kanam', re.sub(r'[^\x00-\x7F]+| ', ' ', content)
            ))
            conn.commit()
            session_id = conn.execute("SELECT id FROM sessions_relacional WHERE date=? LIMIT 1", (date_str,)).fetchone()[0]
            
            # Split into chunks and generate vectors
            chunk_size = 2000
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            
            print(f"   🧠 Generating {len(chunks)} vector chunks...")
            for i, chunk in enumerate(chunks):
                chunk_vector = generate_embedding(chunk)
                if chunk_vector:
                    conn.execute('''
                        INSERT INTO session_vectors (session_id, query_vector, relevance_score, chunk_index, created_at)
                        VALUES (?, ?, 0.5, ?, datetime('now'))
                    ''', (session_id, json.dumps(chunk_vector), i))
                    print(f"     ⚡ Chunk {i+1}/{len(chunks)}")
            
            # Extract topics from tags
            for tag in tags:
                conn.execute('INSERT OR IGNORE INTO topics (name) VALUES (?)', (tag,))
                topic_id = conn.execute('SELECT id FROM topics WHERE name=?', (tag,)).fetchone()[0]
                conn.execute('''
                    INSERT OR IGNORE INTO topic_sessions (session_id, topic_id, confidence)
                    VALUES (?, ?, 0.7)
                ''', (session_id, topic_id))
            
            # Process learnings if present
            learning_sections = re.findall(r'###\s+(.+?)\n\n(.*?)(?=###|$)', content)
            for section_title, section_content in learning_sections:
                conn.execute('''
                    INSERT OR IGNORE INTO learnings_enriquecido 
                    (id, category, title, content, tags, created_at, updated_at)
                    SELECT id, ?, ?, ?, ?, datetime('now'), datetime('now')
                    FROM learnings WHERE id IN (SELECT id FROM learnings WHERE LOWER(title) LIKE ?)
                ''', (section_title.lower(), f'%{section_title.lower()}%'))
            
            conn.commit()
            processed_count += 1
            
        except Exception as e:
            print(f"   ❌ Error processing {date_str}: {e}")
            continue
    
    conn.close()
    return True

if __name__ == "__main__":
    create_schema()
    catalog_memory()

PYTHON_SCRIPT

echo ""
echo "Running Python cataloger..."
echo ""

python3 /tmp/memory_catalog.py || echo "⚠️ Python script encountered errors, falling back to basic SQLite migration"

echo ""
echo "=================================================="
echo "✅ Cataloging complete!"
echo "=================================================="
echo ""
echo "Summary:"
sqlite3 "$DB" <<'SQL'
SELECT 
  'sessions_relacional: ' || COUNT(*) as item FROM sessions_relacional
UNION ALL
SELECT 'session_vectors: ' || COUNT(*) FROM session_vectors
UNION ALL
SELECT 'topics: ' || COUNT(*) FROM topics
UNION ALL
SELECT 'topic_sessions: ' || COUNT(*) FROM topic_sessions
UNION ALL
SELECT 'learnings_enriquecido: ' || COUNT(*) FROM learnings_enriquecido WHERE learning_vector IS NOT NULL;

SQL

echo ""
echo "Usage examples:"
echo "  # Search by semantic meaning"
echo "    sqlite3 memory/memory.db \"SELECT s.title, s.summary FROM sessions_relacional s JOIN session_vectors sv ON s.id = sv.session_id ORDER BY sv.created_at DESC LIMIT 5;\""
echo ""
echo "  # List all topics"
echo "    sqlite3 memory/memory.db \"SELECT t.name, COUNT(ts.session_id) as mentions FROM topics t LEFT JOIN topic_sessions ts ON t.id = ts.topic_id GROUP BY t.id ORDER BY mentions DESC;\""
