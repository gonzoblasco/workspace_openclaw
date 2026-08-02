#!/usr/bin/env node
/**
 * session-context — regenerate.mjs
 * Regenerate HANDOFF.md for a project without creating a new session.
 */

import { getDb, resolveProject, writeHandoff } from './shared.mjs';

const arg = process.argv[2];
const cwd = process.env.PWD || process.cwd();

const db = getDb();
const project = resolveProject(db, arg, cwd);
if (!project) {
  const hint = arg ? `No project matching "${arg}".` : 'This directory is not registered.';
  console.log(`${hint} Run session-context:init to register it.`);
  process.exit(1);
}

writeHandoff(db, project);
console.log(`✓ Regenerated HANDOFF.md for '${project.display_name ?? project.name}'.`);
