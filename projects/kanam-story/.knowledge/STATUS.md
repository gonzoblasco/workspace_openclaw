# STATUS — Kanam Story

**Actualizado:** 2026-08-13

## Estado: 🟢 v0.1.0 RELEASED (Slices 0-5 completos)

- [x] Interview-me convergido (intención confirmada)
- [x] BRIEF
- [x] DATA_MODEL
- [x] ROADMAP (slices 0-5)
- [x] **Slice 0: Fundación sobre sudolab** (bootstrap temporal hacia chat-first)
  - [x] Copiado `sudolab` como base (editor + biblia + mundo + tests)
  - [x] Renombrado a Kanam Story (UI, prompts, DB_NAME `kanam-story`)
  - [x] Stores de chat: `conversations`, `messages`, `contentActions` (vía `Message.actions` inline)
  - [x] Modelo `Beat` + CRUD básico (store `beats` separado con chapterId/sceneId)
  - [x] DB_VERSION 2 → 3, cascade delete extendido
- [x] Build + tests + TS pasan (65 tests)
- [x] **Streaming Ollama (prep Slice 1):** `ollamaChatStream` (SSE) + parser `lib/ollamaStream.ts` testeado (6 tests) + ruta `/api/ollama` con `stream: true` vía ReadableStream
- [x] **Silenciado warning lockfile:** `turbopack.root` en `next.config.ts`
- [x] **Slice 1: Chat con Manos** (92 tests, build+TS pasan)
  - [x] `ChatPanel` (conversaciones + streaming + aceptar/descartar)
  - [x] `lib/agentReply.ts` — parseo de respuesta estructurada del agente
  - [x] `lib/agentPrompts.ts` — contexto completo + prompt JSON
  - [x] `lib/actions.ts` — aplicar/revertir ContentActions (puro)
  - [x] `applyContentActions` en store — persiste + devuelve undo
  - [x] **Undo conectado a la UI** + detalle por acción
- [x] **Prueba con `ultimo-turno`** (2026-08-13) — validado end-to-end
  - [x] Chat conversacional + streaming + rewrite_scene con sceneId real
  - [x] Aceptar aplica a IndexedDB; Deshacer revierte
  - [x] Bugs arreglados: IDs de escena en contexto, persistencia sin conversación activa, turbopack.root
- [x] **Review Slice 1 (Agente B) + fixes** (2026-08-13)
  - [x] HIGH: preservar conversación activa al aplicar acciones (loadProjectData/selectProject)
  - [x] MED: stale-state en applyContentActions (leer prev de DB) + parseAgentReply robusto
  - [x] LOW: validación isValidAction (beat/character shape, update_bible keys), prompt update_bible, append_scene projectId
  - [x] 100 tests, build+TS pasan
- [x] **Slice 2: Outline & Beats** (112 tests, build+TS pasan)
  - [x] Vista en área principal (toggle Editor/Outline + botón por capítulo en el tree)
  - [x] Edición manual inline (title/kind/status/desc/notes), reorder ↑/↓, add/delete
  - [x] "Sugerir outline": flujo dedicado (buildSuggestBeatsPrompt + parseBeatList + store.suggestBeats) con preview Agregar/Descartar
  - [x] Beats de la escena actual en el editor (strip)
  - [x] `lib/outline.ts` (moveBeatInList) + tests
- [x] **Review Slice 2 (Agente A) + fixes** (2026-08-13)
  - [x] Fix crítico: `add_beat` del chat creaba beats sin `chapterId` (rompía chat→outline)
  - [x] Limpieza de código muerto (`loadBeatsByChapter`/`loadBeatsByScene`)
  - [x] Beats huérfanos al borrar capítulo/escena (cascade en db.ts)
  - [x] Dedupe de beats sugeridos + reset del preview al cambiar capítulo
  - [x] Error visible en `suggestBeats` (antes silencioso)
- [x] **Slice 3: Biblia Viva** (115 tests, build+TS pasan)
  - [x] Regeneración por sección (`regenerateBibleSection` + `buildBibleSectionPrompt`)
  - [x] Stale tracking (`staleAt` por sección, badge "desactualizada")
  - [x] Auto-marcado de stale cuando el agente cambia personajes/mundo vía chat
  - [x] Overrides manuales preservados
- [x] **Review Slice 3 (Agente B) + fixes** (2026-08-13)
  - [x] `rewrite_scene`/`append_scene` marcan summary/themes/rules stale
  - [x] Undo limpia `staleAt` (nuevo `clearBibleStale`)
- [x] **Slice 4: Brújula Narrativa** (117 tests, build+TS pasan)
  - [x] Campos opcionales en `Project` (premise/promise/theme/protagonist)
  - [x] Tab "Brújula" en el panel derecho (editable)
  - [x] Strip de promesa en el editor
  - [x] `buildAgentContext` incluye la brújula
- [x] **Review Slice 4 (Agente A) + fixes** (2026-08-13)
  - [x] `protagonist` huérfano al borrar personaje (se limpia)
  - [x] Etiquetas POV centralizadas en `lib/labels.ts`
  - [x] Renombrado `BrújulaPanel` → `CompassPanel` (ASCII)
  - [x] Selects de brújula commitean en `onChange`
- [x] **Slice 5: Pulido** (121 tests, build+TS pasan)
  - [x] Export MD/TXT (`lib/export.ts` + `ExportMenu`)
  - [x] Lint limpio (0 errores)
  - [x] Release v0.1.0 + registro en PROYECTOS.md
- [x] **Review Slice 5 (Agente B) + fixes** (2026-08-13) — 123 tests
  - [x] `stripHtml` preserva párrafos (antes aplanaba el manuscrito)
  - [x] Export TXT real (`markdownToPlainText`); slug sin perder acentos
  - [x] Commit `7bc30d3`

## Decisiones clave

| Decisión | Opción |
|---|---|
| Base de código | `sudolab` (Next.js 16, TipTap 3, IndexedDB, Ollama) — **bootstrap, no destino** |
| El corazón | Chat con agente que **aplica** cambios (ContentAction) |
| Modelo de aceptación | Propuesta → diff/resumen → aceptar/deshacer |
| Estructura | Outline & Beats por capítulo/escena, manual o sugerido por IA |
| Idioma | Español (UI y prompts) |
| Slice fino primero | Sí, para no repetir el patrón de abandono |
| Beats | Store `beats` separado (con chapterId/sceneId), en vez de embederlos en Chapter/Scene |
| Repo | ✅ `gonzoblasco/kanam-story` (público) — remote `origin`, `.knowledge/` excluido (doble-git) |
| Vista outline | Área principal (toggle Editor/Outline), no panel derecho |
| Modelo default | `deepseek-v4-flash` (si está disponible) |
| POV labels | Centralizadas en `lib/labels.ts` |

## Próximo paso

- Export PDF/DOCX (TODO).
- Tema claro (toggle).
- Tests de componentes (jsdom + Testing Library).
- Tests de `lib/db.ts` (fake-indexeddb).
- Búsqueda entre escenas.
