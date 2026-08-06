#!/usr/bin/env node
/**
 * session-context — save.mjs
 * Write session data to SQLite and regenerate HANDOFF.md.
 */

import { readFileSync } from 'fs';
import {
  getDb,
  getProjectByPath,
  getLatestSession,
  writeHandoff,
  today,
  now,
  shortId,
  gitSummary,
} from './shared.mjs';

const isInit = process.argv.includes('--init');
const cwd = process.env.PWD || process.cwd();

let input;
try {
  const raw = readFileSync(0, 'utf8').trim();
  if (!raw) throw new Error('empty stdin');
  input = JSON.parse(raw);
} catch (e) {
  console.error(`session-context save: invalid JSON on stdin — ${e.message}`);
  console.log('Expected schema (save):  {"summary":"...","leftOff":"...","nextSteps":["..."],"decisions":[{"what":"...","why":"..."}],"blockers":["..."]}');
  console.log('Expected schema (--init): {"name":"...","path":"...","description":"...","stack":["..."],"goal":"...","constraints":["..."],"repo":"..."}');
  process.exit(1);
}

const db = getDb();

// ── INIT MODE ────────────────────────────────────────────────────────────────
if (isInit) {
  const { name, path: projectPath, description, stack, goal, constraints, repo, display_name } = input;

  if (!name || !projectPath) {
    console.log('session-context init: name and path are required.');
    process.exit(1);
  }

  let contextName = name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');

  // Ensure unique context name
  let suffix = 2;
  while (true) {
    const existing = db.prepare('SELECT id FROM projects WHERE name = ?').get(contextName);
    if (!existing) break;
    contextName = `${contextName.replace(/-\d+$/, '')}-${suffix++}`;
  }

  const stackStr = Array.isArray(stack) ? stack.join(', ') : (stack || '');
  const constraintsStr = JSON.stringify(Array.isArray(constraints) ? constraints : []);

  const insert = db.prepare(`
    INSERT INTO projects (name, display_name, path, description, stack, goal, constraints, repo, created_at, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);
  const createdAt = today();
  const result = insert.run(contextName, display_name || name, projectPath, description || null, stackStr, goal || null, constraintsStr, repo || null, createdAt, createdAt);

  const project = {
    id: result.lastInsertRowid,
    name: contextName,
    display_name: display_name || name,
    path: projectPath,
    description: description || null,
    stack: stackStr,
    goal: goal || null,
    constraints: constraintsStr,
    repo: repo || null,
  };

  writeHandoff(db, project);

  console.log(`✓ Project '${display_name || name}' registered as '${contextName}'.`);
  console.log(`  Use session-context:save to save session state and session-context:resume to reload it.`);
  process.exit(0);
}

// ── SAVE MODE ────────────────────────────────────────────────────────────────
const project = getProjectByPath(db, cwd);
if (!project) {
  console.log("This project isn't registered yet. Run session-context:init first.");
  process.exit(1);
}

const { summary, leftOff, nextSteps, decisions, blockers, goal, session_id, session_key } = input;

const sessionId = session_id || shortId();
const sessionKey = session_key || null;

const lastSession = getLatestSession(db, project.id);
const gitActivity = gitSummary(cwd, lastSession?.date);

const nextStepsStr = Array.isArray(nextSteps) ? nextSteps.join('\n') : (nextSteps || '');
const blockersStr = Array.isArray(blockers) ? blockers.filter(Boolean).join('\n') : (blockers || '');

const insertSession = db.prepare(`
  INSERT INTO sessions (project_id, session_key, session_id, date, summary, left_off, next_steps, blockers, git_activity, created_at)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

const insertDecision = db.prepare(`
  INSERT INTO decisions (session_id, what, why, date)
  VALUES (?, ?, ?, ?)
`);

const dateStr = today();
const result = insertSession.run(
  project.id,
  sessionKey,
  sessionId,
  dateStr,
  summary || 'Session saved',
  leftOff || null,
  nextStepsStr,
  blockersStr,
  gitActivity || null,
  now()
);
const savedSessionId = result.lastInsertRowid;

if (Array.isArray(decisions)) {
  for (const d of decisions) {
    if (!d.what) continue;
    insertDecision.run(savedSessionId, d.what, d.why || '', dateStr);
  }
}

// Update goal if changed
if (goal && goal !== project.goal) {
  db.prepare('UPDATE projects SET goal = ?, last_updated = ? WHERE id = ?')
    .run(goal, dateStr, project.id);
}

// Update last_updated
if (!goal) {
  db.prepare('UPDATE projects SET last_updated = ? WHERE id = ?').run(dateStr, project.id);
}

writeHandoff(db, { ...project, goal: goal || project.goal });

console.log(`✓ Saved. Session: ${sessionId.slice(0, 8)}`);
if (gitActivity) console.log(`  Git: ${gitActivity}`);
console.log(`  HANDOFF.md regenerated.`);
