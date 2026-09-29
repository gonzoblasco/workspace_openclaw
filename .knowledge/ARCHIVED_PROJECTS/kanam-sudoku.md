# Archived Project: kanam-sudoku

## Summary
This was a test project created on 2026-09-26, a Sudoku web app built with Vite, pure JavaScript, and no runtime dependencies (only dev dependencies for build). The repository was public at https://github.com/gonzoblasco/kanam-sudoku. Initial commit `784c9bd` created the scaffold, and further work was done in units U1‑U8.

## Commits
- `784c9bd` - chore: initial scaffold with project memory
- `e93a911` - docs(knowledge): record U4 delivery in STATUS
- `317dc23` - docs(knowledge): record U5+U6 delivery in STATUS
- `ecbe733` - feat(ui): per-cell notes and reversible history
- `2cba4eb` - feat(ui): timer, stats and versioned persistence
- `6b704e6` - feat(ui): wire notes, undo/redo, timer, stats and difficulty selection
- `065aa16` - feat(ui): hint logic wired to the explanation engine
- `a3b82f1` - feat(ui): show hints with evidence highlighted and aria-live text
- `dd03ce8` - feat(pwa): local icon generator and web app manifest
- `a2a4132` - feat(pwa): offline service worker with a safe cache strategy
- `00586a1` - chore(deploy): prepare GitHub Pages workflow (not enabled)
- `1d025a7` - docs(knowledge): record U7+U8 delivery in STATUS

## Test Results
- **U1 (engine)** - 116 tests passed.
- **U5+U6** - 219 tests passed (all green).
- **U7+U8** - 253 tests passed (all green).
- Overall `npm test` after U8: **253 tests passed**, 0 failures.

## Build
- `npm run build` succeeded, producing `dist/` with `index.html`, `manifest.webmanifest`, `sw.js`, assets and icons.

## Accessibility
- `aria-label` generation for cells includes notes, conflict state, and selection.
- Accessibility audit performed with Playwright + axe-core, no critical issues after fixing a fallback navigation bug.

## Hints
- Hint functionality wired to the engine, works for difficulty levels `facil`, `medio`, `dificil`.
- UI shows full hint text and highlights cells/evidence; hints are announced via `aria-live`.

## Status
The project was a test and has been removed from the `projects` directory. All relevant information has been archived here for future reference.