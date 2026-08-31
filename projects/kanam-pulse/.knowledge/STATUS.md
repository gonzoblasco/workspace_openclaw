# STATUS - Project Status

> **Ultima actualizacion:** 2026-08-31 00:05

## Current Phase

In Development (pre-alpha). M1 y M2 DONE - M3 es el siguiente hito.

## What's Working

- [x] M0 scaffold: public repo `gonzoblasco/kanam-pulse`, README + LICENSE + SPEC-v1
- [x] Motor heredado importado a `packages/core` (30/08): 13 modulos, 46/46 tests verdes
- [x] Monorepo npm workspaces (core + server + web)
- [x] Dev clone + symlink `.knowledge` (ver HANDOFF para la convención)
- [x] **M1 (30/08)**: server Fastify con health + SSE. Dashboard read-only (Vite + React + TS). 57 tests verdes. Commit `d4f3ea9`
- [x] **M2 (31/08)**: consent-driven fixes. Server: scan/dry-run/apply (apply exige confirmed). Web UI accesible (FixesPanel + ConfirmDialog con focus trap + aria). Build web arreglado (estaba roto desde M1). 63 tests verdes (46 core + 17 server). Commit `9556bf1`

## What's Blocked

- [ ] Nothing at the moment

## Next Up (M3 - Ollama audit summary)

1. Detectar Ollama; si está presente, ofrecer "Explain this audit" en la UI
2. Prompt de solo-resumen (sin rutas de datos de usuario), modelo opcional (GLM Flash / Gemma)
3. Si Ollama ausente: feature oculta, nunca rompe

## Deuda técnica

- **web sin test runner**: falta vitest + React Testing Library para probar ConfirmDialog y los flujos de consentimiento (deuda anotada en M2, resolver en M3 o M4)
- Puerto del core a TypeScript (incremental, sin cambio de comportamiento)

## Decisions Log (quick reference)

- Name: Kanam Pulse (2026-08-29)
- Public repo: yes (2026-08-29)
- No Electron v1: yes (2026-08-29)
- M2 scope (2026-08-30): consent-driven fixes usando `core/src/fix/` existente (cleaner.js + processes.js). Server expone, web consiente
- Pipeline M2 (2026-08-30): T=13 (A+B con cross-review, thinking high, Kanam aprueba)
- Web build fix (2026-08-31): faltaban index.html/main.tsx, react nunca instalado (lockfile vacio), tsconfig apuntaba al base equivocado
