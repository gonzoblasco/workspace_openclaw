# STATUS — Kanam Story

**Actualizado:** 2026-08-14

## Estado: 🟢 FASE 3 COMPLETA (U1-U8). v0.7.0 RELEASED.

Todas las fases y slices (0-10) están detallados abajo y en [ROADMAP.md](./ROADMAP.md).

## Fase 3 — Editor refinado + Sincronización Biblia↔tabs (COMPLETA)

> Plan completo en [PLAN-FASE-3.md](./PLAN-FASE-3.md). Pipeline en cadena: A desarrolla unidades impares, B pares; cada uno revisa la unidad del otro antes de seguir.

- [x] **U1 (A) — Barra de formato básica** — B/I/S + undo/redo en `Editor.tsx`. Commit `b5e9484`. 155 tests, build+TS pasan, lint 0 errores. *(Nota: se creía que el subrayado requería `@tiptap/extension-underline`; verificado que StarterKit 3.27.1 ya lo incluye.)*
- [x] **U2 (B) — Listas + headings + enlaces** — completar la barra (viñetas/numeradas, H1/H2/H3, enlaces). Subrayado habilitado. Commit `4c10c8f`. 155 tests, build+TS pasan, lint 0 errores.
- [x] **U3 (A) — Selección contextual IA** — indicador flotante sobre la selección conectado a las herramientas IA. Contador de palabras + Rewrite/Describe, reusa `runAI`. Se oculta al deseleccionar o click fuera. Commits `4dbe1ba` + `7bbf398`. 155 tests, build+TS pasan, lint 0 errores. **Revisado por B (U4): correcto, sin bugs.**
- [x] **U4 (B) — Contador de palabras seleccionadas + polish** — contador preciso (multilínea) + polish de estilos (`.format-bar` flex-wrap, contador del indicador). Copiar/pegar/editar verificado: no rompe autosave. Commit `58369fb`. 155 tests, build+TS pasan, lint 0 errores. **Revisado por A (U5): correcto, sin bugs.**
- [x] **U5 (A) — Auto-import de personajes** desde la Biblia — `syncCharactersFromBible` en el store: dedupe por nombre (case-insensitive), solo toca personajes con `source === 'biblia'` (no pisa manual), rellena solo campos vacíos. Se llama tras regenerar la Biblia en `StoryBiblePanel`. Commit `82de211`. 155 tests, build+TS pasan, lint 0 errores. **Revisado por B (U6): bug de orden corregido** (sync corría antes de regenerar; ahora después + lee biblia fresca de DB).
- [x] **U6 (B) — Auto-import de mundo** desde la Biblia — `syncWorldFromBible` en el store (mismo patrón que U5): dedupe por nombre, marca `source: 'biblia'`, solo toca entidades `source === 'biblia'`, rellena `description` vacía. Se llama tras regenerar junto a la de personajes. Commit `49501c9`. 155 tests, build+TS pasan, lint 0 errores. **Revisado por A (U7): correcto, sin bugs.**
- [x] **U7 (A) — Sincronización bidireccional + no pisar manual** — `revertBibleImport(kind, id)` en el store: quita la marca `source: 'biblia'` → `'manual'` (no-destructivo, conserva ediciones; el próximo sync ya no toca la entidad). Botón "Revertir import" en las fichas de personaje y mundo (solo visible si `source === 'biblia'`). Commit `7b2a38f`. 155 tests, build+TS pasan, lint 0 errores. **Revisado por B (U8): correcto, sin bugs.**
- [x] **U8 (B) — Tests + integración** — lógica pura de dedupe/merge extraída a `lib/bibleSync.ts` (`buildCharacterSyncPlan`/`buildWorldSyncPlan`, sin DB). Syncs refactorizados para usarlas. 8 tests nuevos. **163 tests**, build+TS pasan, lint 0 errores. Commit `b2a7740`.
- [x] **Release v0.7.0** + docs — bump a v0.7.0, CHANGELOG con features de la Fase 3, tag `v0.7.0` + GitHub Release. Commit `1baa434`. **Fase 3 completa.**

## Backlog (B1-B7) — pipeline de revisión cruzada A/B

> Plan en [ROADMAP.md](./ROADMAP.md). Cada item = commit atómico + push + actualizar ROADMAP/STATUS. A desarrolla impares, B pares; se revisan mutuamente.

- [x] **B1 — Tests de `lib/db.ts`** (fake-indexeddb). Commits `b5d0c17`, `88ac174`, `13b0914`, `6a9220c`. 202 tests. Aprobado tras 2 rondas de revisión cruzada.
- [x] **B2 — Tests de componentes** (jsdom + testing-library). Commits `9546e82`, `f3fd795`, `13b0914`, `6a9220c`. 202 tests. Aprobado tras 2 rondas.
- [x] **B3 — Export PDF / DOCX** — `docx` + `pdfmake` client-side. Commits `b064c36`, `a9eb65c`, `461b1bc`, `1afb734` (CI Node 22). 204 tests. Aprobado tras revisión multi-ronda.
- [x] **B4 — Búsqueda entre escenas** — `lib/search.ts` (lógica pura) + `SearchPanel.tsx` (modal global). Busca en contenido/título/summary, agrupa por capítulo con snippet + conteo, click navega a la escena, find/replace con confirmación. Commit `d8f37ad`. 21 tests nuevos. **225 tests**, build+TS pasan, lint 0 errores. **Asignado: Agente A. Pendiente revisión del Agente B.**

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
- [x] **Review Slice 7 (Agente A) + fixes** (2026-08-13)
  - [x] `update_character` del chat validaba `type` (antes podía escribir uno inválido)
  - [x] Limpieza de `mapRoleToType`; prompt `add_character` con campos completos
  - [x] Commit `a533634`
- [x] **Slice 8: Worldbuilding tipado fino** (145 tests, build+TS pasan, lint 0 errores)
  - [x] `WorldEntity.category` → `kind` (9 valores) + migración DB v5→v6 (`mapCategoryToKind`)
  - [x] Campos nuevos: `otherNames[]`, `traits[]`, `inContext`
  - [x] `buildAgentContext` + `buildContext` filtran `inContext`; `bibleExtract` amplía keywords
  - [x] UI (`WorldPanel`): selector de kind, tag editors, toggle inContext
  - [x] Commit `60434ba`
- [x] **Review Slice 8 (Agente B) + fixes** (2026-08-13)
  - [x] Renombrado `inferCategory` → `inferKind`; keyword duplicado eliminado
  - [x] Commit `ec75acd`
- [x] **Slice 9: Match My Style** (152 tests, build+TS pasan, lint 0 errores)
  - [x] `buildStyleProfilePrompt` + `parseStyleProfile` + `store.analyzeStyle`
  - [x] `styleText` inyecta el perfil completo en modo match
  - [x] UI: modo match habilitado (pegar muestra → analizar → guardar perfil)
  - [x] Commit `011347d` + release v0.5.0
- [x] **Slice 10: Filtros de outline + vinculación documento↔outline** (155 tests, build+TS pasan, lint 0 errores)
  - [x] `Project.tense` (`past|present|future`) + migración DB v6→v7 + `TENSE_LABELS`/`tenseLabel` en `lib/labels.ts`
  - [x] Selector de tense en `CompassPanel`
  - [x] Filtros de POV/tense en `OutlineView`
  - [x] Detección de escenas huérfanas (sin beats) + botón "Vincular"
  - [x] `buildAgentContext` + `buildContext` inyectan tense
  - [x] Commit `9b36cde` + release v0.6.0

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

**Fase 2 completa (Slices 0-10, v0.6.0).** El pipeline de producto está cerrado: chat con manos, outline & beats, biblia viva, brújula, export, story bible editable, fichas ricas, worldbuilding tipado, match my style, filtros + vinculación. Todos los releases v0.1.0 → v0.6.0 creados en GitHub.

**Fase 3 planificada (2026-08-13):** dos features prioritarias de Gonzo — (1) área de texto refinada (barra de formato + selección contextual IA), (2) sincronización automática Biblia ↔ tabs Personajes/Mundo. **Plan detallado con pipeline de revisión cruzada A/B en [PLAN-FASE-3.md](./PLAN-FASE-3.md).** Release v0.7.0.

**Backlog (no bloquea, se atiende cuando haya espacio):** ver [ROADMAP.md](./ROADMAP.md) sección "TODOs no bloqueantes". Resto: búsqueda entre escenas (B4), versioning/snapshots (B6), streaming en el editor (B7). **Hecho:** export PDF/DOCX (B3), tema claro (B5, commit `82f2a2e`), tests de componentes (jsdom, B2), tests de `lib/db.ts` (fake-indexeddb, B1).
