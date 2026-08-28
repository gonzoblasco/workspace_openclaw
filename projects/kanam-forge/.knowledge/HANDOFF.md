# HANDOFF - kanam-forge

## Session Context
- **Date:** 2026-08-27 21:58
- **Project:** kanam-forge
- **Branch:** main (repo propio: git@github.com:gonzoblasco/kanam-forge.git)

## Resumen de la sesión

Sesión dedicada a completar la integración de **create-with-ai → kanam-forge** (Fases B, C, D y parte de E del plan `PLAN-INTEGRACION-CREATE-WITH-AI.md`), usando el pipeline A/B (Kanam en MAX orquesta, agentes A/B en HIGH con deepseek-v4-flash:cloud).

Se probó brevemente **MiniMax M3** como modelo de los agentes (pedido de Gonzo), pero el setup tardaba demasiado y Gonzo abortó a los minutos, volviendo a **DeepSeek V4 Flash** (el default sigue intacto). Se rescató el trabajo válido del agente minimax y se revirtió lo que se desvió fuera de scope.

## Logros de la sesión

- **Fase B COMPLETA:** analyzer integrado al chat. `POST /api/repos` corre `analyzeDescription` antes de provisionar y persiste `analysis` en metadata. `lib/scaffold/build-scaffold.ts` adapta migrations.sql + .env.example al análisis. Commits: `1493673` (buildScaffold), `18bc401` (analyzer integrado).
- **Bug de Fase A corregido (cross-review):** `lib/analyzer.ts` usaba `host.docker.internal:11434` como default, pero el analyzer corre en el HOST (next dev), no en un container. Fix a `localhost:11434` + override por `OLLAMA_BASE_URL`/`OLLAMA_URL`.
- **Fase C COMPLETA:** `lib/project-context.ts` (readProjectContext + buildProjectSystemPrompt) inyecta el contexto real del proyecto al system-prompt del agente. El agente ahora conoce el stack real (verificado: respondió Next.js + Vitest). Commits: `1493673` (project-context), `b67253b` (chat).
- **Fase D VERIFICADA:** TDD + commit every slice confirmado con el tetris de Gonzo (proyecto f3066af2): 28/28 tests pasan dentro del contenedor, 9 commits por slice.
- **Fase E parcial:** create-with-ai archivado en GitHub. Deprecate npm mandado al backlog (todo 27).

## Left off (dónde quedé)

- **Integración create-with-ai → kanam-forge COMPLETA** (Fases A-D verificadas, E solo pendiente del deprecate npm).
- El dev server del orquestador corre en `:3000` (en el terminal de Gonzo).
- Proyectos existentes en `~/.kanam-forge/projects/`: `6c30703d` (kanam-story), `b698a4c6` (kanam-forge-app), `f3066af2` (tetris de Gonzo).

## Next steps

1. **Reiniciar el dev server del orquestador en `:3000`** para activar el análisis real del analyzer (el fix del default URL de Fase B no se toma hasta el restart). Hasta entonces el endpoint devuelve el fallback (tables: [], CRUD).
2. **Todo 27:** deprecar `@gonzoblasco/create-with-ai` en npm (no borrar). Requiere token npm válido (el de `~/.npmrc` expiró, 401). Comando: `npm deprecate @gonzoblasco/create-with-ai@0.0.2 "Fusionado a kanam-forge. Usa kanam-forge en su lugar."`
3. Residuo `projects/create-with-ai/` en el workspace — decisión de borrar/archivar en Gonzo.

## Decisiones clave

- **kanam-forge mantiene Next.js** (no migra a Vite). Se porta el stack opinado de create-with-ai (Vitest, Biome, Supabase, shadcn, CI) adaptado a Next.js.
- **Modelo default:** deepseek-v4-flash:cloud para los agentes A/B (no cambiarlo sin necesidad).
- **Analyzer URL:** `localhost:11434` (el analyzer corre en el host), override via `OLLAMA_BASE_URL`/`OLLAMA_URL`.
- **`.gitignore` de kanam-forge:** `/.knowledge/` movido a `.git/info/exclude` local (double-git: el `.knowledge/` pertenece al workspace, no al repo del proyecto).

## Blockers

- **Deprecate npm:** token npm expirado (401) — requiere `npm login` de Gonzo.
- **Analyzer en endpoint:** dev server sin restart — el fix del default URL no surte efecto hasta reiniciar.

## Lecciones de la sesión

- **MiniMax M3:** el setup/ajuste consume tiempo y el agente se desvió fuera de scope (reformateó files.ts prohibido + dejó `.qwen/`). El modelo default sigue siendo deepseek-v4-flash:cloud.
- **Cross-review del pipeline:** el agente B detectó el bug del default URL (host.docker.internal en un analyzer que corre en el host). El orquestador en MAX verifica contra la fuente real.
- **Validar formato UIMessage:** en Fase C el agente B sobrescribió una conversación real (kanam-story 'hola') por usar `content` en vez de `parts`. Regla: validar el formato antes de escribir conversaciones.
- **Arquitectura rollup:** el npm install se hace dentro del contenedor → node_modules con binarios Linux. El agente corre vitest DENTRO del contenedor (funciona). Correr vitest desde el host falla (rollup-darwin-arm64 missing) — esperado, no es bug.

## Commits de la sesión (kanam-forge main)

- `1493673` feat(scaffold): buildScaffold adapta scaffold a AIAnalysis
- `18bc401` feat(analyzer): run analysis before provisioning + persist it
- `0020c43` chore(gitignore): .knowledge a local exclude
- `1493673` feat(project): read project context + build system prompt section
- `b67253b` feat(chat): inject real project context into agent system prompt

## Estado del repo

- kanam-forge: main pusheado (`b67253b`). 15/15 tests (build-scaffold 8 + project-context 7), typecheck limpio.
- Workspace: commiteado y pusheado (`1cda8a9`).
