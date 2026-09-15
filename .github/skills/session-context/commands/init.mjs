#!/usr/bin/env node
/**
 * session-context - init.mjs
 * Auto-detect project info and output JSON for confirmation.
 */

import { readFileSync, existsSync } from 'fs';
import { resolve, basename } from 'path';
import {
  readJson,
  extractSection,
} from './shared.mjs';

const cwd = process.env.PWD || process.cwd();

const output = {
  path: cwd,
  name: null,
  display_name: null,
  description: null,
  stack: [],
  goal: null,
  constraints: [],
  repo: null,
};

function readFileLocal(filename) {
  const p = resolve(cwd, filename);
  if (!existsSync(p)) return null;
  try { return readFileSync(p, 'utf8'); } catch { return null; }
}

// ── package.json ─────────────────────────────────────────────────────────────
const pkg = readFileLocal('package.json');
if (pkg) {
  try {
    const parsed = JSON.parse(pkg);
    if (parsed.name && !output.name) output.name = parsed.name;
    if (parsed.description && !output.description) output.description = parsed.description;

    const deps = Object.keys({ ...(parsed.dependencies || {}), ...(parsed.devDependencies || {}) });
    const stackMap = {
      next: 'Next.js', react: 'React', vue: 'Vue', svelte: 'Svelte', astro: 'Astro',
      express: 'Express', fastify: 'Fastify', hono: 'Hono', nestjs: 'NestJS',
      typescript: 'TypeScript', prisma: 'Prisma', drizzle: 'Drizzle',
      '@neondatabase/serverless': 'Neon', '@upstash/redis': 'Upstash Redis',
      '@clerk/nextjs': 'Clerk', stripe: 'Stripe', tailwindcss: 'Tailwind CSS',
    };
    for (const [dep, label] of Object.entries(stackMap)) {
      if (deps.includes(dep) && !output.stack.includes(label)) {
        output.stack.push(label);
      }
    }
    if (deps.includes('typescript') || existsSync(resolve(cwd, 'tsconfig.json'))) {
      if (!output.stack.includes('TypeScript')) output.stack.push('TypeScript');
    }
  } catch { /* malformed package.json */ }
}

// ── go.mod ────────────────────────────────────────────────────────────────────
const goMod = readFileLocal('go.mod');
if (goMod) {
  if (!output.stack.includes('Go')) output.stack.push('Go');
  const modName = goMod.match(/^module\s+(\S+)/m)?.[1];
  if (modName && !output.name) output.name = modName.split('/').pop();
}

// ── Cargo.toml ────────────────────────────────────────────────────────────────
const cargo = readFileLocal('Cargo.toml');
if (cargo) {
  if (!output.stack.includes('Rust')) output.stack.push('Rust');
  const crateName = cargo.match(/^name\s*=\s*"(.+?)"/m)?.[1];
  if (crateName && !output.name) output.name = crateName;
}

// ── pyproject.toml ────────────────────────────────────────────────────────────
const pyproject = readFileLocal('pyproject.toml');
if (pyproject) {
  if (!output.stack.includes('Python')) output.stack.push('Python');
  const pyName = pyproject.match(/^name\s*=\s*"(.+?)"/m)?.[1];
  if (pyName && !output.name) output.name = pyName;
}

// ── .git/config (repo URL) ────────────────────────────────────────────────────
const gitConfig = readFileLocal('.git/config');
if (gitConfig) {
  const repoMatch = gitConfig.match(/url\s*=\s*(.+)/);
  if (repoMatch) output.repo = repoMatch[1].trim();
}

// ── README.md / CLAUDE.md / DEFINITION.md / BRIEF.md ──────────────────────────
function readKnowledge(name) {
  return readFileLocal(resolve(cwd, '.knowledge', name)) ||
         readFileLocal(name);
}

const claudeMd = readKnowledge('CLAUDE.md');
if (claudeMd) {
  const goal = extractSection(claudeMd, 'Current Goal');
  if (goal && !output.goal) output.goal = goal.split('\n')[0].trim();

  const doNot = extractSection(claudeMd, 'Do Not Do');
  if (doNot) {
    const bullets = doNot.split('\n')
      .filter(l => /^[-*]\s+/.test(l))
      .map(l => l.replace(/^[-*]\s+/, '').trim());
    output.constraints = bullets;
  }

  const stack = extractSection(claudeMd, 'Tech Stack');
  if (stack && output.stack.length === 0) {
    output.stack = stack.split(/[,\n]/).map(s => s.replace(/^[-*]\s+/, '').trim()).filter(Boolean);
  }

  const whatItIs = extractSection(claudeMd, 'What This Is') || extractSection(claudeMd, 'About');
  if (whatItIs && !output.description) output.description = whatItIs.split('\n')[0].trim();
}

const briefMd = readKnowledge('BRIEF.md');
if (briefMd && !output.description) {
  const firstPara = briefMd.split('\n').find(l => l.trim() && !l.trim().startsWith('#'));
  if (firstPara) output.description = firstPara.trim().slice(0, 120);
}

const definitionMd = readKnowledge('DEFINITION.md');
if (definitionMd) {
  const goal = extractSection(definitionMd, 'Goal') || extractSection(definitionMd, 'Objectives');
  if (goal && !output.goal) output.goal = goal.split('\n')[0].trim();
  const scope = extractSection(definitionMd, 'Scope') || extractSection(definitionMd, 'What This Is');
  if (scope && !output.description) output.description = scope.split('\n')[0].trim();
}

// ── README.md fallback ────────────────────────────────────────────────────────
const readme = readFileLocal('README.md');
if (readme && !output.description) {
  const lines = readme.split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith('#') && !trimmed.startsWith('!') && !trimmed.startsWith('>') && !trimmed.startsWith('[') && trimmed !== '---' && trimmed !== '___') {
      output.description = trimmed.slice(0, 120);
      break;
    }
  }
}

// ── Name fallback ─────────────────────────────────────────────────────────────
if (!output.name) {
  output.name = basename(cwd).toLowerCase().replace(/\s+/g, '-');
}
if (!output.display_name) {
  output.display_name = output.name.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

console.log(JSON.stringify(output, null, 2));
