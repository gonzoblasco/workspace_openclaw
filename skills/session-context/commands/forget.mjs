#!/usr/bin/env node
/**
 * session-context - forget.mjs
 * Remove a project, its sessions, decisions, and HANDOFF.md.
 */

import { rmSync } from 'fs';
import { resolve } from 'path';
import {
  getDb,
  resolveProject,
  handoffPath,
} from './shared.mjs';

const arg = process.argv[2];
const cwd = process.env.PWD || process.cwd();

const db = getDb();
const project = resolveProject(db, arg, cwd);
if (!project) {
  const hint = arg ? `No project matching "${arg}".` : 'This directory is not registered.';
  console.log(`${hint}`);
  process.exit(1);
}

const { name, path: projectPath, id } = project;

// Remove project (CASCADE removes sessions and decisions)
db.prepare('DELETE FROM projects WHERE id = ?').run(id);

// Remove HANDOFF.md
try {
  rmSync(handoffPath(projectPath), { force: true });
} catch (e) {
  console.log(`session-context: could not remove HANDOFF.md - ${e.message}`);
}

console.log(`✓ Context for '${name}' removed.`);
