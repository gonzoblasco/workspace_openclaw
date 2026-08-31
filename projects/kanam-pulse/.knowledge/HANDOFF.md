# HANDOFF - kanam-pulse (v1.0.1 candidates on main, conversacion limpia)

## Session Context
- **Date:** 2026-08-31 02:40
- **Project:** kanam-pulse
- **Repo:** https://github.com/gonzoblasco/kanam-pulse (PUBLIC, MIT)
- **Dev clone:** `~/.openclaw/dev/kanam-pulse`
- **Workspace:** `projects/kanam-pulse/.knowledge/`

## Estado: v1.0.0 RELEASED + 3 hotfixes en main (candidatos a v1.0.1)

Roadmap M0-M5 completo. Tag `v1.0.0` + GitHub Release publicada (31/08).
MAIN tiene 3 commits extra post-tag, NO incluidos en el tag v1.0.0 (candidatos a v1.0.1):

1. `869d011` docs(readme): reflect v1.0.0 release status (badge + roadmap)
2. `05e9412` fix(m3): disable reasoning (think:false) - BUG REAL encontrado en runtime
3. `6141cf4` perf(m3): explainAudit default model -> deepseek-v4-flash (configurable via KANAM_PULSE_AI_MODEL)

## BUG REAL ENCONTRADO Y RESUELTO (importante)

**Sintoma (lo encontro Gonzo probando la app):** boton "Explain this audit" -> "ollama returned an empty response".

**Causa raiz:** modelos de razonamiento (qwen3.5:9b-mlx, deepseek-v4-flash:cloud) emiten un campo `thinking` largo que consume `num_predict` (300), dejando `response` vacio. done_reason: "length".

**Fix:** `think:false` en el payload de /api/generate en `explainAudit` (packages/core/src/audit/summary.js). Test de regresion: assert body.think === false.

**Fix 2:** default model cambiado de qwen3.5:9b-mlx (local, lento) a deepseek-v4-flash:cloud (rapido, ~2s warm). Configurable via env KANAM_PULSE_AI_MODEL.

**VERIFICADO end-to-end:** /api/audit/explain devuelve 450+ chars de explicacion en lenguaje humano (firewall off + memoria alta detectados).

## Como correr en local

```bash
cd ~/.openclaw/dev/kanam-pulse/packages/server && npm start   # 127.0.0.1:4270
cd ~/.openclaw/dev/kanam-pulse/packages/web && npm run dev    # localhost:5173
```
Dashboard: http://localhost:5173 (NO 127.0.0.1:4270 que es API-only, da 404 en /)

## Test & Quality

- 118 tests verdes (core 61, server 21, web 36) + fix no agrega tests nuevos (solo assertion)
- Biome lint exit 0 (4 warnings documentados), build OK, CI gateado

## Pendiente / decisiones Gonzo

- [ ] Crear tag v1.0.1 con los 3 hotfixes de main (release notes con el fix del explain)
- [ ] Community announcement / LinkedIn (a decidir)
- [ ] Por que el boton explain "no funciona" en el navegador de Gonzo a las 02:37 (backend OK verificada; probable HMR/cache del navegador - hard refresh Cmd+Shift+R)
- [ ] Backlog: puerto core a TypeScript, envoltorio nativo
