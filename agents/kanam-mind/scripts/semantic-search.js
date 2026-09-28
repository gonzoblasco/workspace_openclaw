#!/usr/bin/env node
// semantic-search.js
// Busqueda semantica sobre memory/memory.db usando embeddings de Ollama (qwen3-embedding:0.6b).
// Uso: node scripts/semantic-search.js "tu consulta aqui"
// Retorna los fragmentos de sesion mas cercanos semanticamente (RAG lite).

import { execSync } from 'node:child_process';
import { DatabaseSync } from 'node:sqlite';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DB_PATH = path.join(__dirname, '..', 'memory', 'memory.db');
const MODEL = 'qwen3-embedding:0.6b';

// ---------- 1. Embedder de consulta (Ollama) ----------
function embed(text) {
  const safe = text.replace(/"/g, '\\"').replace(/\n/g, ' ');
  const out = execSync(
    `ollama run ${MODEL} "${safe}" 2>/dev/null`,
    { encoding: 'utf-8', timeout: 30000 },
  );
  // Ollama devuelve el vector como JSON en la ultima linea
  const lines = out.trim().split('\n');
  const last = lines[lines.length - 1];
  const parsed = JSON.parse(last);
  if (!Array.isArray(parsed)) {
    throw new Error('Ollama no devolvio un vector JSON valido');
  }
  return parsed;
}

// ---------- 2. Similitud de coseno ----------
function cosine(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return dot / (Math.sqrt(na) * Math.sqrt(nb) || 1);
}

// ---------- 3. Parseo de vector almacenado (string JSON) ----------
function parseStored(raw) {
  try {
    const arr = JSON.parse(raw);
    return Array.isArray(arr) ? arr : null;
  } catch {
    return null;
  }
}

// ---------- 4. Main ----------
function main() {
  const query = process.argv.slice(2).join(' ');
  if (!query) {
    console.error('Uso: node scripts/semantic-search.js "consulta"');
    process.exit(1);
  }

  console.error(`[embed] generando vector para: "${query}"`);
  const qVec = embed(query);

  const db = new DatabaseSync(DB_PATH);
  const rows = db.prepare(
    'SELECT v.id, v.session_id, v.query_vector, v.chunk_text, s.title, s.summary ' +
    'FROM session_vectors v ' +
    'JOIN sessions_relacional s ON s.id = v.session_id',
  ).all();

  const scored = [];
  for (const row of rows) {
    const stored = parseStored(row.query_vector);
    if (!stored) continue;
    const score = cosine(qVec, stored);
    const text = row.chunk_text || row.summary;
    scored.push({ score, sessionId: row.session_id, title: row.title, text });
  }

  scored.sort((a, b) => b.score - a.score);
  const top = scored.slice(0, 5);

  console.log('\n=== RESULTADOS (top 5) ===\n');
  for (const r of top) {
    console.log(`[${(r.score * 100).toFixed(1)}%] sesion ${r.sessionId} - ${r.title}`);
    console.log(`  ${r.text.slice(0, 200)}${r.text.length > 200 ? '...' : ''}\n`);
  }
  db.close();
}

main();
