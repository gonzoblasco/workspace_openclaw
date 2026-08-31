#!/usr/bin/env node
// semantic-search-json.js
// Version JSON de semantic-search.js para integracion con herramientas.
// Uso: node scripts/semantic-search-json.js "consulta" [topN]
// Retorna JSON: [{score, sessionId, title, text}]

import { execSync } from 'node:child_process';
import { DatabaseSync } from 'node:sqlite';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DB_PATH = path.join(__dirname, '..', 'memory', 'memory.db');
const MODEL = 'nomic-embed-text:latest';

function embed(text) {
  const safe = text.replace(/"/g, '\\"').replace(/\n/g, ' ');
  const out = execSync(
    `ollama run ${MODEL} "${safe}" 2>/dev/null`,
    { encoding: 'utf-8', timeout: 30000 },
  );
  const lines = out.trim().split('\n');
  const last = lines[lines.length - 1];
  const parsed = JSON.parse(last);
  if (!Array.isArray(parsed)) throw new Error('Ollama no devolvio vector JSON');
  return parsed;
}

function cosine(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return dot / (Math.sqrt(na) * Math.sqrt(nb) || 1);
}

function parseStored(raw) {
  try {
    const arr = JSON.parse(raw);
    return Array.isArray(arr) ? arr : null;
  } catch { return null; }
}

function main() {
  const args = process.argv.slice(2);
  const query = args[0];
  const topN = parseInt(args[1], 10) || 5;
  if (!query) {
    console.error('Uso: node scripts/semantic-search-json.js "consulta" [topN]');
    process.exit(1);
  }

  const qVec = embed(query);
  const db = new DatabaseSync(DB_PATH);
  const rows = db.prepare(
    'SELECT v.session_id, v.query_vector, v.chunk_text, s.title ' +
    'FROM session_vectors v JOIN sessions_relacional s ON s.id = v.session_id',
  ).all();

  const scored = [];
  for (const row of rows) {
    const stored = parseStored(row.query_vector);
    if (!stored) continue;
    const score = cosine(qVec, stored);
    scored.push({
      score: Number(score.toFixed(3)),
      sessionId: row.session_id,
      title: row.title,
      text: (row.chunk_text || '').slice(0, 500),
    });
  }

  scored.sort((a, b) => b.score - a.score);
  const top = scored.slice(0, topN);
  console.log(JSON.stringify({ query, results: top }, null, 2));
  db.close();
}

main();
