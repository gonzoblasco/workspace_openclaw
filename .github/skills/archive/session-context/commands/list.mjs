#!/usr/bin/env node
/**
 * session-context — list.mjs
 * Portfolio view of all registered projects.
 */

import { getDb, listProjects, getLatestSession, renderListTable } from './shared.mjs';

const cwd = process.env.PWD || process.cwd();
const db = getDb();
const projects = listProjects(db);

if (projects.length === 0) {
  console.log('No projects registered. Run session-context:init to get started.');
  process.exit(1);
}

const entries = projects.map(p => {
  const latest = getLatestSession(db, p.id);
  return {
    name: p.name,
    display_name: p.display_name,
    path: p.path,
    last_date: latest?.date || p.last_updated || p.created_at,
    summary: latest?.summary || '',
    session_id: latest?.session_id || '',
  };
});

console.log('');
console.log(renderListTable(entries, cwd));
console.log('');
console.log('Resume which? (number or name)');
