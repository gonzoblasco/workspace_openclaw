/**
 * session-context — shared utilities
 * No external dependencies. Node.js stdlib + node:sqlite only.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { resolve, basename, dirname } from 'path';
import { homedir } from 'os';
import { spawnSync } from 'child_process';
import { randomBytes } from 'crypto';
import { DatabaseSync } from 'node:sqlite';

// ─── Paths ────────────────────────────────────────────────────────────────────

export const DATA_DIR = resolve(homedir(), '.openclaw', 'workspace', '.data');
export const DB_FILE = resolve(DATA_DIR, 'session-context.db');

export function getDb() {
  mkdirSync(DATA_DIR, { recursive: true });
  const db = new DatabaseSync(DB_FILE);
  db.exec(`
    CREATE TABLE IF NOT EXISTS projects (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      display_name TEXT,
      path TEXT NOT NULL UNIQUE,
      description TEXT,
      stack TEXT,
      goal TEXT,
      constraints TEXT,
      repo TEXT,
      created_at TEXT NOT NULL,
      last_updated TEXT
    );

    CREATE TABLE IF NOT EXISTS sessions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
      session_key TEXT,
      session_id TEXT,
      date TEXT NOT NULL,
      summary TEXT,
      left_off TEXT,
      next_steps TEXT,
      blockers TEXT,
      git_activity TEXT,
      created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS decisions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
      what TEXT NOT NULL,
      why TEXT,
      date TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_sessions_project_date ON sessions(project_id, date);
    CREATE INDEX IF NOT EXISTS idx_decisions_session ON decisions(session_id);
  `);
  return db;
}

// ─── JSON / file I/O helpers ──────────────────────────────────────────────────

export function readJson(filePath) {
  try {
    if (!existsSync(filePath)) return null;
    return JSON.parse(readFileSync(filePath, 'utf8'));
  } catch {
    return null;
  }
}

export function writeJson(filePath, data) {
  const dir = dirname(filePath);
  mkdirSync(dir, { recursive: true });
  writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

// ─── Date helpers ─────────────────────────────────────────────────────────────

export function today() {
  return new Date().toISOString().slice(0, 10);
}

export function now() {
  return new Date().toISOString();
}

export function daysAgoLabel(dateStr) {
  if (!dateStr) return 'unknown';
  const diff = Math.floor((Date.now() - new Date(dateStr)) / 86_400_000);
  if (diff === 0) return 'Today';
  if (diff === 1) return '1 day ago';
  return `${diff} days ago`;
}

export function stalenessIcon(dateStr) {
  if (!dateStr) return '○';
  const diff = Math.floor((Date.now() - new Date(dateStr)) / 86_400_000);
  if (diff < 1) return '●';
  if (diff <= 5) return '◐';
  return '○';
}

// ─── ID generation ────────────────────────────────────────────────────────────

export function shortId() {
  return randomBytes(4).toString('hex');
}

// ─── Git helpers ──────────────────────────────────────────────────────────────

function runGit(args, cwd) {
  try {
    const result = spawnSync('git', ['-C', cwd, ...args], {
      timeout: 3000,
      stdio: 'pipe',
      encoding: 'utf8',
    });
    if (result.status !== 0) return null;
    return result.stdout.trim();
  } catch {
    return null;
  }
}

export function gitLogSince(projectPath, sinceDate) {
  if (!sinceDate) return null;
  return runGit(['log', '--oneline', `--since=${sinceDate}`], projectPath);
}

export function gitSummary(projectPath, sinceDate) {
  const log = gitLogSince(projectPath, sinceDate);
  if (!log) return null;
  const commits = log.split('\n').filter(Boolean).length;
  if (commits === 0) return null;

  const countStr = runGit(['rev-list', '--count', 'HEAD', `--since=${sinceDate}`], projectPath);
  const revCount = countStr ? parseInt(countStr, 10) : commits;
  const diff = runGit(['diff', '--shortstat', `HEAD~${Math.min(revCount, 50)}..HEAD`], projectPath);

  if (diff) {
    const filesMatch = diff.match(/(\d+) file/);
    const files = filesMatch ? parseInt(filesMatch[1]) : '?';
    return `${commits} commit${commits !== 1 ? 's' : ''}, ${files} file${files !== 1 ? 's' : ''} changed`;
  }
  return `${commits} commit${commits !== 1 ? 's' : ''}`;
}

// ─── Markdown extraction helpers ──────────────────────────────────────────────

export function extractSection(md, heading) {
  const re = new RegExp(`## ${heading}\\n([\\s\\S]*?)(?=\\n## |$)`);
  const m = md.match(re);
  return m ? m[1].trim() : null;
}

export function parseBullets(text) {
  if (!text) return [];
  return text.split('\n')
    .filter(l => /^[-*\d]\s/.test(l.trim()))
    .map(l => l.replace(/^[-*\d]+\.?\s+/, '').trim())
    .filter(Boolean);
}

export function handoffPath(projectPath) {
  return resolve(projectPath, '.knowledge', 'HANDOFF.md');
}

// ─── DB helpers ───────────────────────────────────────────────────────────────

export function getProjectByPath(db, projectPath) {
  const stmt = db.prepare('SELECT * FROM projects WHERE path = ?');
  return stmt.get(projectPath) || null;
}

export function getProjectByName(db, name) {
  const stmt = db.prepare('SELECT * FROM projects WHERE name = ? COLLATE NOCASE');
  return stmt.get(name) || null;
}

export function getProjectById(db, id) {
  const stmt = db.prepare('SELECT * FROM projects WHERE id = ?');
  return stmt.get(id) || null;
}

export function listProjects(db) {
  const stmt = db.prepare('SELECT * FROM projects ORDER BY name');
  return stmt.all();
}

export function getLatestSession(db, projectId) {
  const stmt = db.prepare('SELECT * FROM sessions WHERE project_id = ? ORDER BY date DESC, id DESC LIMIT 1');
  return stmt.get(projectId) || null;
}

export function getAllSessions(db, projectId) {
  const stmt = db.prepare('SELECT * FROM sessions WHERE project_id = ? ORDER BY date DESC, id DESC');
  return stmt.all(projectId);
}

export function getSessionDecisions(db, sessionId) {
  const stmt = db.prepare('SELECT * FROM decisions WHERE session_id = ?');
  return stmt.all(sessionId);
}

export function resolveProject(db, arg, cwd) {
  const projects = listProjects(db);

  if (!arg) {
    return projects.find(p => p.path === cwd) || null;
  }

  const asNumber = parseInt(arg, 10);
  if (!isNaN(asNumber) && String(asNumber) === arg) {
    return projects[asNumber - 1] || null;
  }

  const lower = arg.toLowerCase();
  return projects.find(p => p.name.toLowerCase() === lower) ||
         projects.find(p => p.name.toLowerCase().startsWith(lower)) ||
         projects.find(p => p.name.toLowerCase().includes(lower)) ||
         null;
}

export function writeHandoff(db, project) {
  const sessions = getAllSessions(db, project.id);
  const latest = sessions[0] || null;
  if (latest) {
    latest.decisions = getSessionDecisions(db, latest.id);
    latest.session_count = sessions.length;
  }
  const md = renderHandoffMd(project, latest, sessions);
  const p = handoffPath(project.path);
  mkdirSync(dirname(p), { recursive: true });
  writeFileSync(p, md, 'utf8');
}

// ─── Rendering ────────────────────────────────────────────────────────────────

export function renderHandoffMd(project, latestSession, allSessions) {
  const lines = [
    `<!-- Generated by session-context — edit via commands only -->`,
    `# Project: ${project.display_name ?? project.name}`,
    `> Path: ${project.path}`,
  ];
  if (project.repo) lines.push(`> Repo: ${project.repo}`);
  const sessionCount = allSessions?.length || 0;
  lines.push(`> Last Session: ${latestSession?.date || 'never'} | Sessions: ${sessionCount}`);
  lines.push('');
  lines.push(`## What This Is`);
  lines.push(project.description || '_Not set._');
  lines.push('');
  lines.push(`## Tech Stack`);
  lines.push(project.stack || '_Not set._');
  lines.push('');
  lines.push(`## Current Goal`);
  lines.push(project.goal || '_Not set._');
  lines.push('');
  lines.push(`## Where I Left Off`);
  lines.push(latestSession?.left_off || '_Not yet recorded._');
  lines.push('');
  lines.push(`## Next Steps`);
  if (latestSession?.next_steps) {
    const steps = latestSession.next_steps.split('\n').filter(Boolean);
    steps.forEach((s, i) => lines.push(`${i + 1}. ${s}`));
  } else {
    lines.push('_Not yet recorded._');
  }
  lines.push('');
  lines.push(`## Blockers`);
  if (latestSession?.blockers) {
    const blockers = latestSession.blockers.split('\n').filter(Boolean);
    blockers.forEach(b => lines.push(`- ${b}`));
  } else {
    lines.push('- None');
  }
  lines.push('');

  lines.push(`## Decisions Made`);
  lines.push(`| Decision | Why | Date |`);
  lines.push(`|----------|-----|------|`);
  const decisions = (latestSession?.decisions || []);
  if (decisions.length) {
    decisions.forEach(d => lines.push(`| ${d.what} | ${d.why || ''} | ${d.date || ''} |`));
  } else {
    lines.push(`| _(none yet)_ | | |`);
  }
  lines.push('');

  if (allSessions && allSessions.length > 1) {
    lines.push(`## Session History`);
    const reversed = [...allSessions].reverse();
    reversed.forEach(s => {
      lines.push(`### ${s.date} — ${s.summary || 'Session'}`);
      if (s.git_activity) lines.push(`_${s.git_activity}_`);
      if (s.left_off) lines.push(`**Left off:** ${s.left_off}`);
    });
    lines.push('');
  }

  return lines.join('\n');
}

export function renderBriefingBox(project, session) {
  const W = 57;
  const pad = (str, w) => {
    const s = String(str || '');
    return s.length > w ? s.slice(0, w - 1) + '…' : s.padEnd(w);
  };
  const row = (label, value) => `│  ${label} → ${pad(value, W - label.length - 7)}│`;

  const when = daysAgoLabel(session?.date);
  const sessions = session?.session_count || 0;

  const lines = [
    `┌${'─'.repeat(W)}┐`,
    `│  RESUMING: ${pad(project.display_name ?? project.name, W - 12)}│`,
    `│  Last session: ${pad(`${when}  |  Sessions: ${sessions}`, W - 16)}│`,
    `├${'─'.repeat(W)}┤`,
    row('WHAT IT IS', project.description || '—'),
    row('STACK     ', project.stack || '—'),
    row('PATH      ', project.path),
    row('GOAL      ', project.goal || '—'),
    `├${'─'.repeat(W)}┤`,
    `│  WHERE I LEFT OFF${' '.repeat(W - 18)}│`,
  ];
  const leftOffLines = (session?.left_off || '—').split('\n').filter(Boolean);
  leftOffLines.forEach(l => lines.push(`│    • ${pad(l, W - 7)}│`));
  lines.push(`├${'─'.repeat(W)}┤`);
  lines.push(`│  NEXT STEPS${' '.repeat(W - 12)}│`);
  const steps = session?.next_steps?.split('\n').filter(Boolean) || [];
  if (steps.length) {
    steps.forEach((s, i) => lines.push(`│    ${i + 1}. ${pad(s, W - 8)}│`));
  } else {
    lines.push(`│    —${' '.repeat(W - 5)}│`);
  }
  const blockers = session?.blockers?.split('\n').filter(Boolean) || [];
  const blockersStr = blockers.length ? blockers.join(', ') : 'None';
  lines.push(`│  BLOCKERS → ${pad(blockersStr, W - 13)}│`);
  if (session?.git_activity) {
    lines.push(`│  GIT      → ${pad(session.git_activity, W - 13)}│`);
  }
  lines.push(`└${'─'.repeat(W)}┘`);
  return lines.join('\n');
}

export function renderInfoBlock(project, session) {
  const latest = session || {};
  const sep = '─'.repeat(44);
  const lines = [
    `session-context: ${project.display_name ?? project.name}`,
    sep,
    `PATH     ${project.path}`,
  ];
  if (project.repo) lines.push(`REPO     ${project.repo}`);
  if (latest.session_id) lines.push(`SESSION  ${latest.session_id.slice(0, 8)}`);
  lines.push(`GOAL     ${project.goal || '—'}`);
  lines.push(sep);
  lines.push(`WHERE I LEFT OFF`);
  (latest.left_off || '—').split('\n').filter(Boolean).forEach(l => lines.push(`  • ${l}`));
  lines.push(`NEXT STEPS`);
  (latest.next_steps || '').split('\n').filter(Boolean).forEach((s, i) => lines.push(`  ${i + 1}. ${s}`));
  if (!latest.next_steps) lines.push(`  —`);
  lines.push(`BLOCKERS`);
  if (latest.blockers) {
    latest.blockers.split('\n').filter(Boolean).forEach(b => lines.push(`  • ${b}`));
  } else {
    lines.push(`  • None`);
  }
  return lines.join('\n');
}

export function renderListTable(entries, cwd) {
  const rows = entries.map((e, i) => {
    const isHere = e.path === cwd;
    const when = daysAgoLabel(e.last_date);
    const icon = stalenessIcon(e.last_date);
    const statusLabel = icon === '●' ? '● Active' : icon === '◐' ? '◐ Warm' : '○ Stale';
    const sessId = e.session_id ? e.session_id.slice(0, 8) : '—';
    const summary = (e.summary || '—').slice(0, 34);
    const displayName = ((e.display_name ?? e.name) + (isHere ? ' <-' : '')).slice(0, 18);
    return {
      num: String(i + 1),
      name: displayName,
      status: statusLabel,
      when: when.slice(0, 10),
      sessId,
      summary,
    };
  });

  const cols = {
    num: Math.max(1, ...rows.map(r => r.num.length)),
    name: Math.max(7, ...rows.map(r => r.name.length)),
    status: Math.max(6, ...rows.map(r => r.status.length)),
    when: Math.max(9, ...rows.map(r => r.when.length)),
    sessId: Math.max(7, ...rows.map(r => r.sessId.length)),
    summary: Math.max(12, ...rows.map(r => r.summary.length)),
  };

  const hr = `+${'-'.repeat(cols.num + 2)}+${'-'.repeat(cols.name + 2)}+${'-'.repeat(cols.status + 2)}+${'-'.repeat(cols.when + 2)}+${'-'.repeat(cols.sessId + 2)}+${'-'.repeat(cols.summary + 2)}+`;
  const cell = (val, width) => ` ${val.padEnd(width)} `;
  const headerRow = `|${cell('#', cols.num)}|${cell('Project', cols.name)}|${cell('Status', cols.status)}|${cell('Last Seen', cols.when)}|${cell('Session', cols.sessId)}|${cell('Last Summary', cols.summary)}|`;

  const dataRows = rows.map(r =>
    `|${cell(r.num, cols.num)}|${cell(r.name, cols.name)}|${cell(r.status, cols.status)}|${cell(r.when, cols.when)}|${cell(r.sessId, cols.sessId)}|${cell(r.summary, cols.summary)}|`
  );

  return [hr, headerRow, hr, ...dataRows, hr].join('\n');
}
