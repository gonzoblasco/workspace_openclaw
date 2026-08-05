# BRIEF — Learning JavaScript Data Structures and Algorithms

**Source:** Learning JavaScript Data Structures and Algorithms, Third Edition — Loiane Avancini (Packt Publishing)
**Project start:** 2026-08-05
**Node version:** LTS (v22.x)
**Stack:** JavaScript (ES2026+), Node.js runtime, VSCode

## Objective

Read the book chapter by chapter, implementing all data structures and algorithms in modern JavaScript (ES2026+), generating ADRs for technical decisions, and documenting learnings.

## Methodology

- Each chapter gets its own folder under `src/chapter-NN/`
- Code is written in ES modules (`import`/`export`), not CommonJS
- `var` is replaced with `const`/`let` throughout
- Constructor functions + prototype are replaced with ES6 `class` syntax
- Deprecated/removed packages are replaced with modern equivalents
- Each significant deviation from the book is documented in an ADR
- Learnings are accumulated in `docs/LEARNINGS.md`

## Deviations from the book

1. `var` → `const`/`let` (modern JS best practice)
2. Constructor functions → ES6 `class` syntax
3. `http-server` global install → `npx http-server` or Node `--watch`
4. Debugger for Chrome extension → VSCode built-in debugger (no extension needed)
5. URLs updated (Atom.io → archived, Electron → electronjs.org)
6. ES modules over inline `<script>` tags for Node examples
7. `console.log` with template literals instead of string concatenation
