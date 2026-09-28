#!/bin/bash
# Simple memory cataloging script - SQLite relational + vector store

DB="memory/memory.db"

echo "=== Memory Cataloger (Simple) ==="
python3 <<'PYTHON'
import sqlite3
import os
import re
import sys
from pathlib import Path
import json
from datetime import datetime

DB_PATH = os.environ.get("MEMORY_DB", "memory/memory.db")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")

def get_embedding(text):
    try:
        import urllib.request
        body = json.dumps({
            "model": "qwen3-embedding:0.6b",
            "prompt": text[:768] if len(text) > 768 else text,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{OLLAMA_BASE}/api/embeddings",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            if resp.status == 200:
                data = json.loads(resp.read())
                vec = data.get("embedding") or (data.get("embeddings") or [None])[0]
                if vec:
                    return vec
    except Exception as e:
        print(f"Ollama fallback: {e}", file=sys.stderr)

    import hashlib
    h = hashlib.sha256(text.encode('utf-8', errors='ignore')).digest()
    return [float(i) for i in h]

def main():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        sys.exit(1)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    
    # Create sessions_relacional table
    c.execute("""CREATE TABLE IF NOT EXISTS sessions_relacional (
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
    )""")
    
    # Create session_vectors table
    c.execute("""CREATE TABLE IF NOT EXISTS session_vectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        query_vector TEXT NOT NULL,
        relevance_score REAL DEFAULT 0.0,
        chunk_index INTEGER DEFAULT 0,
        created_at TEXT
    )""")
    
    # Create topics table
    c.execute("""CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category TEXT,
        description TEXT,
        created_at TEXT
    )""")
    
    # Create topic_sessions junction table
    c.execute("""CREATE TABLE IF NOT EXISTS topic_sessions (
        session_id INTEGER NOT NULL,
        topic_id INTEGER NOT NULL,
        confidence REAL DEFAULT 0.5,
        FOREIGN KEY(session_id) REFERENCES sessions_relacional(id),
        FOREIGN KEY(topic_id) REFERENCES topics(id)
    )""")
    
    conn.commit()
    
    # Process all .md files in memory/
    memory_dir = Path("memory")
    md_files = list(memory_dir.glob("*.md"))
    
    print(f"Found {len(md_files)} markdown files to catalog...")
    print("=" * 60)
    
    for i, md_file in enumerate(sorted(md_files), 1):
        if not md_file.stem.startswith("2026"):
            continue
        
        date_str = md_file.stem
        with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract metadata
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else date_str
        
        # Extract tags: match known domain keywords + bracketed tags
        KNOWN_TAGS = [
            'soporteml', 'kanam', 'a11y', 'accessibility', 'pipeline', 'agent',
            'git', 'github', 'oss', 'linkedin', 'entrevista', 'supabase',
            'react', 'typescript', 'fastify', 'vitest', 'ollama', 'glm',
            'deepseek', 'qwen', 'kimi', 'memory', 'catalog', 'semantic',
            'docker', 'tailscale', 'meli', 'mercadolibre', 'adr', 'openspec',
            'biome', 'billing', 'mp', 'mercadopago', 'cron', 'skill', 'workspace',
        ]
        content_lower = content.lower()
        tags = list(set(re.findall(r'\[(\w+)\]', content)))
        for kw in KNOWN_TAGS:
            if kw in content_lower and kw not in tags:
                tags.append(kw)
        tags = tags[:5]
        
        # Generate embedding
        print(f"\n{i}/{len(md_files)} Cataloging: {date_str}")
        vector = get_embedding(content)
        print(f"  Generated {len(vector)}-dim embedding")
        
        # Insert into sessions_relacional
        c.execute("""INSERT OR REPLACE INTO sessions_relacional 
                     (id, date, title, tags, model_used, thinking_level, summary, content_bare, created_at)
                     VALUES (?, ?, ?, ?, 'unknown', 'high', ?, ?, ?)""",
                  (None, date_str, title, ','.join(tags),
                   re.sub(r'[\x00-\x1f\x7f-\x9f]', '', content)[:200], content,
                   datetime.now().isoformat()))
        conn.commit()
        
        session_id = c.execute("SELECT id FROM sessions_relacional WHERE date=?", (date_str,)).fetchone()[0]
        
        # Generate chunk vectors (limit to 3 chunks)
        chunks = [content[j:j+1500] for j in range(0, len(content), 1500)]
        for chunk_idx, chunk in enumerate(chunks[:3]):
            chunk_vector = get_embedding(chunk)
            c.execute("""INSERT INTO session_vectors 
                         (session_id, query_vector, relevance_score, chunk_index, chunk_text, created_at)
                         VALUES (?, ?, 0.5, ?, ?, ?)""",
                      (session_id, json.dumps(chunk_vector), chunk_idx, chunk, datetime.now().isoformat()))
        
        # Extract topics from tags
        for tag in tags:
            c.execute('INSERT OR IGNORE INTO topics (name) VALUES (?)', (tag,))
            topic_id = c.execute('SELECT id FROM topics WHERE name=?', (tag,)).fetchone()[0]
            if topic_id:
                c.execute("""INSERT OR IGNORE INTO topic_sessions 
                              (session_id, topic_id, confidence)
                              VALUES (?, ?, 0.7)""", (session_id, topic_id))
    
    conn.commit()
    
    # Print summary
    print("\n" + "=" * 60)
    print("Cataloging complete!")
    print("- sessions_relacional: " + str(c.execute('SELECT COUNT(*) FROM sessions_relacional').fetchone()[0]))
    print("- session_vectors: " + str(c.execute('SELECT COUNT(*) FROM session_vectors').fetchone()[0]))
    print("- topics: " + str(c.execute('SELECT COUNT(*) FROM topics').fetchone()[0]))

if __name__ == "__main__":
    main()
PYTHON

echo ""
echo "Usage examples:"
echo "  # Semantic search"
echo "  sqlite3 memory/memory.db \"SELECT s.title, substr(s.summary,1,200) FROM sessions_relacional s JOIN session_vectors sv ON s.id = sv.session_id ORDER BY sv.created_at DESC LIMIT 3;\""
echo "  # List topics with frequency"
echo "  sqlite3 memory/memory.db \"SELECT t.name as topic, COUNT(*) as freq FROM topics t LEFT JOIN topic_sessions ts ON t.id = ts.topic_id GROUP BY t.id ORDER BY freq DESC;\""
