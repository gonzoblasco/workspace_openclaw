# STATUS — Kanam Story

**Actualizado:** 2026-08-13

## Estado: 🟢 Slice 8 COMPLETO (Worldbuilding tipado fino)

- [x] **Slice 6 — Story Bible editable y tipado** (Braindump, Genre tags, Style selector, Synopsis editable; DB v3→v4). Release v0.2.0.
  - [x] `Project.style` migrado de `string` → `ProjectStyle` objeto (mode: featured|custom|match) con migración de datos en DB v3→v4.
  - [x] `genres: string[]` (tags removibles), `braindump: string`, `synopsis: string` (override manual).
  - [x] `StoryBibleSettingsPanel` (nuevo tab "Story Bible" en el panel derecho) — patrón draft-and-commit del CompassPanel.
  - [x] `buildAgentContext` (chat) y `buildContext` (generación) inyectan genres/style/braindump/synopsis.
  - [x] Helpers centralizados en `lib/labels.ts` (`styleText`, `STYLE_PRESETS`).
  - [x] 126 tests, build+TS pasan, lint 0 errores. Commit `6aefc3e` + release `329a4c4` (tag `v0.2.0`).
- [x] **Slice 7 — Fichas de personaje ricas + generación asistida** (Type tipado, Pronouns/Groups/OtherNames/Traits, toggle de contexto, Generate Character + Surprise Me). DB v4→v5.
  - [x] `Character.type` enum + migración `role`→`type` (default `supporting`).
  - [x] Campos nuevos: `pronouns`, `groups[]`, `otherNames[]`, `traits[]`, `inContext`.
  - [x] `buildAgentContext` filtra `inContext === false`.
  - [x] Generación asistida (`buildGenerateCharacterPrompt` + `parseSuggestedCharacterList` + `store.generateCharacter`) + UI Generar/Surprise Me/preview.
  - [x] 137 tests. Commit `f00cb79`. Review (Agente A): validación de `type` en `update_character` + limpieza `mapRoleToType` (commit `a533634`).
- [x] **Slice 8 — Worldbuilding tipado fino** (kinds finos, OtherNames/Traits, toggle de contexto). DB v5→v6.
  - [x] `WorldEntity.category` → `kind` (9 valores: place|organization|lore|key_event|clue|magic_system|item|rule|other).
  - [x] `mapCategoryToKind` + `worldKindLabel` en `lib/labels.ts`.
  - [x] Campos nuevos: `otherNames[]`, `traits[]`, `inContext`.
  - [x] `buildAgentContext` + `buildContext` filtran `inContext` y muestran kind.
  - [x] `bibleExtract` amplía keywords (organización/evento/pista/magia).
  - [x] `WorldPanel` con selector de 9 kinds + tag editors + toggle.
  - [x] 145 tests, build+TS pasan, lint 0 errores. Commit `60434ba`.

## Fase 2 planificada (Slices 9-10) — Hacia el Story Bible de Sudowrite

> **Fuente:** auditoría de 10 capturas de Sudowrite (2026-08-13). ROADMAP ampliado con los slices 6-10 detallados. **División de trabajo:** los agentes A (VS Code) y B (ZCode) implementan y se revisan entre sí; Kanam planifica y documenta. Cada slice actualiza este STATUS al cerrarse.

- [ ] **Slice 9 — Match My Style** (clonar la voz del autor desde una muestra). Release v0.5.0.
- [ ] **Slice 10 — Filtros de outline + vinculación documento↔outline** (POV/tiempo, escenas huérfanas). Release v0.6.0.

Detalle completo en [ROADMAP.md](./ROADMAP.md).

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
- [x] **Slice 6: Story Bible editable** (126 tests, build+TS pasan, CI verde)
  - [x] `braindump`, `genres[]`, `style` → `ProjectStyle` (featured|custom|match), `synopsis` editable
  - [x] Migración DB v3→v4 (style string → objeto) + `StoryBibleSettingsPanel` (tab "Story Bible")
  - [x] Helpers `styleText`/`STYLE_PRESETS` en `lib/labels.ts`; contexto inyecta genres/style/braindump/synopsis
  - [x] Release v0.2.0 (`329a4c4`) + CI (`acc190e`)
- [x] **Review Slice 6 (Agente B) + fixes** (2026-08-13) — 126 tests
  - [x] Migración DB usa la `transaction` del versionchange (antes `db.transaction()` podía tirar `InvalidStateError`)
  - [x] Modo "Match My Style" deshabilitado (no funcional hasta Slice 9)
  - [x] Commit `dc7a8ad`
- [x] **Slice 7: Fichas de personaje ricas + generación asistida** (137 tests, build+TS pasan, lint 0 errores)
  - [x] `Character.type` enum (`protagonist|antagonist|supporting|minor|love_interest|custom`) + migración DB v4→v5 (`role`→`type`, default `supporting`)
  - [x] Campos nuevos: `pronouns`, `groups[]`, `otherNames[]`, `traits[]`, `inContext`
  - [x] `buildAgentContext` filtra `inContext === false` + muestra tipo y campos nuevos
  - [x] Generación asistida: `buildGenerateCharacterPrompt` + `parseSuggestedCharacterList` + `store.generateCharacter`
  - [x] UI: type select, tag editors, toggle inContext, flujo Generar/Surprise Me/preview (Agregar/Regenerar/Descartar)
  - [x] Chat: reusa `add_character` (no se duplica con `generate_character`)
  - [x] Commit `f00cb79`

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

**Slice 8 — Worldbuilding tipado fino** (→ v0.4.0): kinds finos (`place|organization|lore|key_event|clue|magic_system|item|rule|other`) + migración, campos nuevos (`otherNames[]`, `traits[]`), toggle `inContext`. Mismo patrón que Slice 7.

TODOs post-release (no bloquean): Export PDF/DOCX, tema claro, tests de componentes (jsdom), tests de `lib/db.ts` (fake-indexeddb), búsqueda entre escenas.
