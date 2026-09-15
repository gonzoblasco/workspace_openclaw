#!/usr/bin/env node
/**
 * session-context - resume.mjs
 * Full project briefing.
 */

import { existsSync } from 'fs';
import {
  getDb,
  resolveProject,
  getLatestSession,
  getAllSessions,
  getSessionDecisions,
  renderBriefingBox,
} from './shared.mjs';

const arg = process.argv[2];
const cwd = process.env.PWD || process.cwd();

const db = getDb();
const project = resolveProject(db, arg, cwd);
if (!project) {
  const hint = arg ? `No project matching "${arg}".` : 'This directory is not registered.';
  console.log(`${hint} Run session-context:init to register it.`);
  process.exit(1);
}

const sessions = getAllSessions(db, project.id);
const latest = sessions[0] || null;
if (latest) {
  latest.decisions = getSessionDecisions(db, latest.id);
  latest.session_count = sessions.length;
}

if (project.path !== cwd && existsSync(project.path)) {
  console.log(`→ cd ${project.path}`);
}

console.log('');
console.log(renderBriefingBox(project, latest));
