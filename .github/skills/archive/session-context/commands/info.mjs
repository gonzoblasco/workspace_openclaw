#!/usr/bin/env node
/**
 * session-context — info.mjs
 * Quick read-only context snapshot.
 */

import {
  getDb,
  resolveProject,
  getLatestSession,
  getSessionDecisions,
  renderInfoBlock,
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

const latest = getLatestSession(db, project.id);
if (latest) {
  latest.decisions = getSessionDecisions(db, latest.id);
}

console.log('');
console.log(renderInfoBlock(project, latest));
