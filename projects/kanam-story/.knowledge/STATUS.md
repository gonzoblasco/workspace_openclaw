# STATUS — Kanam Story

**Actualizado:** 2026-08-17

## Estado: 🟢 v0.17.0 + Fase A completa + OpenSpec inicializado (379 tests)

> **OpenSpec inicializado 2026-08-17:** 6 specs de casos de uso core (34 requirements) + project.md + config.yaml. Los specs documentan la intención; falta auditar el comportamiento real contra ellos (ver checklist en cada spec).

## OpenSpec (2026-08-17)

- [x] **Inicializado** con schema `spec-driven` (commit `1801c98`).
- [x] **`project.md`** - visión, stack, dominio, estrategia de 3 públicos.
- [x] **`config.yaml`** - contexto del proyecto + reglas para el CLI.
- [x] **6 specs de casos de uso core** (34 requirements): co-writer (9), editor (6), outline-beats (6), proyecto-persistencia (5), biblia-viva (4), brújula-narrativa (4).
- [x] **Auditoría del co-writer realizada** (2026-08-17): 4 hallazgos - ver `openspec/audits/co-writer-2026-08-17.md`.
- [x] **Fixes de la auditoría del co-writer aplicados** (commit `f618a38`): IDs de personajes/mundo, filtro inContext consistente, brújula en editor, continuidad en editor. 382 tests.
- [x] **Auditorías de los 5 specs restantes** (2026-08-17): editor, outline, biblia, brújula, persistencia - ver `openspec/audits/`.
- [x] **Fixes menores aplicados** (commit `9df57e3`): contador del editor reusa `countWords`, brújula commitea en onChange.
- [x] **Specs + auditorías de Personajes, Mundo y Brainstorm** (2026-08-17): todos cumplidos, sin hallazgos.
- [ ] **Filtros de outline por POV/tense** - pendiente de rediseño (removidos en `4349401`, el modelo era defectuoso).

## Decisión: NO open source + roadmap a la nube (2026-08-17)

- **Kanam Story NO será open source.** Se trabaja en local hasta el salto a la nube.
- **Roadmap a la nube planificado** (referencia futura en `ROADMAP-NUBE.md`): DB → Supabase, middleware, login, después Vercel. No se ejecuta hasta que Gonzo lo indique.

## Fase A - Cerrar el producto local (2026-08-17)

- [x] **Release v0.17.0** — bump + CHANGELOG + tag + GitHub Release. Cierra el bloque post-v0.16.1 (roles, PWA, mobile, a11y, export). Commit `cb80bdc`.
- [x] **Smoke tests de acciones nuevas** — `scripts/smoke-actions.ts` valida `delete_character`, `delete_world`, `update_project` con Ollama real. **3/3 OK.**
- [x] **WelcomeScreen onboarding** — pantalla de bienvenida cuando no hay proyectos (explica co-writer, outline, biblia, brújula + botón crear primer proyecto). `components/WelcomeScreen.tsx` + 2 tests. Commit `e45448d`.
- [x] **README BYOK** — status v0.17.0, sección BYOK (Ollama + cualquier endpoint OpenAI-compatible), 379 tests, TODO corregido. Commit `fb7381d`.
- [x] **Feature flag del co-writer (diseñado, revertido)** — `NEXT_PUBLIC_ENABLE_COWRITER` en `lib/features.ts` (commit `2f5130e`), **revertido** por `8eb6275` por decisión de Gonzo: el co-writer sigue en open source hasta que exista el backend SaaS con usuarios.

## Estrategia de monetización (definida con Gonzo)

**3 públicos que conviven:**
1. **Open source (gratis, local-first)** — producto completo, BYOK → Ollama. Embajador de marca + portfolio.
2. **SaaS BYOK (5 USD/mes)** — mismo producto + sync en la nube + multi-dispositivo + registro. El usuario trae su LLM (OpenAI-compatible).
3. **SaaS premium (con LLM incluido)** — DeepSeek V4 Flash server-side. Más caro.

**Bonus de pago:** el co-writer (el corazón) es exclusivo de pago. El open source conserva el producto de escritura completo pero sin el chat con manos. **Se activa cuando exista el backend + auth + billing.**

## Bloque de features 2026-08-17 (completado)

- [x] **a11y:** `--sl-danger` en tema claro 2.78:1 → 5.22:1 (`58a6706`); `ConfirmDialog`+`PromptDialog` reemplazan 12 `window.prompt/confirm` nativos (`f53a7e1`); fix lint `useId()` (`e26c3d6`).
- [x] **Mobile responsive (≤768px):** sidebar como drawer overlay con backdrop + topbar compacto (`164a406`); padding reducido + co-writer full-width (`140616f`); modales full-width + ai-bar apilado + chapter reader (`ea915cf`).
- [x] **PWA:** Serwist (`@serwist/turbopack`) — SW compilado en build, manifest, página offline, SerwistProvider (`f3e41a7`); iconos reales con PIL (`6a01623`).
- [x] **Export polish:** metadata narrativa (POV + estilo) en portada + word count (`3c1c012`).
- [x] **Co-writer U5+:** `delete_character`, `delete_world`, `update_project` (`f5ee579`); roles especializados Plot Doctor + Consistency Checker (`f68aff9`); smoke test de roles con Ollama (`912db24`).
- [x] **Validación AT manual verificada** por Gonzo con VoiceOver (live region chat + radio group onboarding).

**Quality:** 377 tests (subió de 366), build + tsc + ESLint verdes.

## Detalle previo: Feature block post-v0.9.0 — Outline global + persistencia (v0.10.0 → v0.16.0)

- [x] **U1 — Vista global del outline** — refactor de `OutlineView` con modo Capítulo/Global. Commit `efaadb2`.
- [x] **Fixes de runtime post-U1** — hydration warning, orden de escenas, no repetir setup. Commits `3e43c9a`, `4127bf1`, `6f24eed`.
- [x] **Layout más ancho** — `65369f0`.
- [x] **Menús de acciones en el árbol** — `ActionMenu.tsx` accesible. Commit `e02c1ad`.
- [x] **U2 — Generación automática de estructura global** — `lib/outlineGeneration.ts` + preview. Commit `4ca27bf`.
- [x] **Árbol de manuscrito colapsable** — `a70a290`.
- [x] **Persistencia del estado de sesión** — `8b5b675`.
- [x] **Code review + reestructuración** — `4349401`.
- [x] **U3 — Chat-assisted global outline generation** — `replace_outline`.
- [x] **Release v0.16.0** — publicado 2026-08-16 (`b119220`). Sidebar de co-writer desde la escritura. Tags v0.10.0 → v0.16.0.

## Fase 4 — Rediseño de navegación accesible (COMPLETA, v0.9.0)

> Plan completo en [PLAN-FASE-4.md](./PLAN-FASE-4.md). Pipeline en cadena: A desarrolla unidades impares, B pares; cada uno revisa la unidad del otro (incluida su a11y) antes de seguir.

- [x] **U1 (A) — Refactor de layout: secciones apiladas en el main** — grid 3→2 columnas, `RightPanel` eliminado como contenedor de tabs, las 7 secciones (Co-writer, Brainstorm, Personajes, Mundo, Biblia, Ajustes, Brújula) apiladas verticalmente en el main con scroll. Store `view` extendido a `'editor' | 'outline' | 'story'` + `activeStorySection`. Sidebar navega Escritura/Outline/Historia con `aria-current`. a11y integrada: skip link, `<nav aria-label="Secciones">`, `<main id="contenido-principal">`, cada sección como `<section aria-labelledby>` con h2 bajo h1 (jerarquía sin saltos), foco visible global. Commit `3437359`. **244 tests**, build+TS pasan (solo errores pre-existentes en `bibleSync.test.ts`/`export.test.ts`), lint 0 errores. **Revisada por Agente B (U2): sin correcciones.**
- [x] **U2 (B) — Scrollspy + acordeón de secciones apiladas** — `IntersectionObserver` sobre el `<main>` resalta la sección activa en el sidebar al hacer scroll, actualizando `aria-current="true"`. Cada sección es un acordeón accesible: toggle nativo `<button>` dentro del h2 con `aria-expanded` y `aria-controls="body-{key}"`; al colapsar, el h2 permanece presente para no romper la jerarquía. Click en una sección del sidebar desplaza suavemente el main hacia ella sin pelear con el scrollspy. Commit `771dabb`. **244 tests**, build+TS pasan, lint 0 errores. **Revisada por Agente A (U3): sin correcciones** (scrollspy actualiza `aria-current`, sin jitter; acordeón operable por teclado, h2 visible al colapsar).
- [x] **U3 (A) — Renombrar "Story Bible"→"Ajustes" + consistencia visual + h1 OutlineView** — título interno "Story Bible" eliminado (la sección "Ajustes" ahora muestra un único título coherente). Sistema de headers consistentes (`.stack-panel-header`/`.stack-panel-hint`) aplicado a las 7 cards; eliminados los `<strong>` que duplicaban el h2 del acordeón. `OutlineView` ganó `<h1>Outline</h1>` y capítulos/escenas pasaron a `<h2>`/`<h3>` (jerarquía h1→h2→h3 sin saltos). Commit `f3dde30`. **244 tests**, build+TS pasan, lint 0 errores. **Revisada por Agente B (U4): 1 corrección** — Brainstorm era la única de las 7 cards que seguía usando `sidebar-section-title` para su conteo interno "Notas (n)", rompiendo el sistema unificado; se pasó a `.stack-panel-header`/`.stack-panel-count`. Commit `c490cfc`. El resto (renombrado sin "Story Bible" en la UI, headers/hints en las 6 cards restantes, h1→h2→h3, acordeón `aria-expanded`/`aria-controls`, `aria-current`, foco, contraste) **aprobado sin correcciones**.
- [x] **U4 (B) — Generar escena desde outline + función pura testeable** — botón "Generar escena" por beat en `OutlineView` → crea la escena (y el capítulo automáticamente si el beat no tiene ninguno, estructuras opcionales), la selecciona, relinkea el beat dentro de ella y abre el editor con el foco. Lógica de creación extraída a `lib/sceneFromBeat.ts` (`planGenerateScene`, pura, sin DB/DOM) + 6 tests. a11y: `aria-label` descriptivo por botón, live region **global persistente** (`role="status"` en `app/page.tsx`, vía store `announce`/`announcement`) que anuncia éxito/error incluso tras cambiar a la vista editor, y `requestEditorFocus` (nonce en store) mueve el caret al editor. Commits `acb04d5` + fix a11y `3a5adcb`. **250 tests**, build+TS pasan, lint 0 errores. Verificado en browser: botón con label descriptivo, escena "Nuevo beat" creada, foco en el editor (`.tiptap-editor` focused), anuncio "Escena "Nuevo beat" generada." presente en la live region. **Revisada por Agente A (U5): 1 corrección de UX** — al hacer click repetido sobre un beat que ya tiene escena, ahora se **reutiliza** esa escena (se abre) en lugar de crear una duplicada; `planGenerateScene` devuelve `existingSceneId` y el handler hace `selectScene` sin crear. Commit `896b4af`. Flujo, función pura, a11y (live region global + foco) verificados en browser.
- [x] **U5 (A) — Onboarding por plantillas al crear proyecto** — al crear un proyecto se ofrecen 4 puntos de partida opcionales (nunca obligatorio): **outline en blanco** (capítulo + primer beat), **biblia de la historia** (en blanco, secciones listas), **plantilla de género** (estructura sugerida de capítulos + beats: thriller/romance/sci-fi) y **proyecto vacío**. Datos puros en `lib/projectTemplates.ts` (`GENRE_TEMPLATES`), aplicación vía `createProjectWithStructure` en el store. a11y: `components/StarterPicker.tsx` como **radio group accesible** (`role="radiogroup"`/`radio` + `aria-checked`, roving tabindex, flechas + Enter/Espacio, `aria-labelledby`, instrucciones descriptivas, foco visible, contraste AA). Sub-radiogroup de géneros al elegir plantilla. Fix a11y extra: al cerrar el modal se restaura el foco al botón "Nuevo proyecto" (evita `aria-hidden` focus trap, WCAG 2.4.3). Commits `a5eeb55` + `fadea7a`. **262 tests** (250 + 9 U5 + 3 U4-reuse), build+TS pasan, lint 0 errores. Verificado en browser: 4 opciones como radio group, sub-radiogroup de géneros, creación de Thriller arma 5 capítulos + beat incitante en el outline, teclado (flechas) mueve la selección, foco vuelve al trigger al cerrar. **Revisado por Agente B (U6): sin correcciones.**
- [x] **U6 (B) — Creación en línea contextual con botones "＋"** — botones contextuales en cada vista: Brainstorm ("Nueva nota"), Personajes ("Agregar personaje"), Mundo ("Agregar entrada"), Outline ("Beat" por capítulo/escena + "Vincular" escenas huérfanas). Todos con `aria-label` descriptivo, iconos `aria-hidden`, y anuncio de creación vía live region global (`announce`). Commit `e689a87`. **262 tests**, build+TS pasan, lint 0 errores. Verificado en browser: botones visibles en cada sección, labels descriptivos en árbol de accesibilidad, foco visible, anuncios funcionando. **a11y integrada:** WCAG 2.1 AA — labels descriptivos, foco visible, contraste AA, feedback anunciado. **Revisada por Agente A (U7): sin correcciones.**
- [x] **U7 (A) — Chat con input sticky + inserción contextual del co-writer** — el input del chat queda **anclado (sticky) al fondo** de la sección Co-writer con scroll interno de mensajes (card de altura fija `min(58vh, 520px)`), para escribir sin hacer scroll hasta el final de las secciones apiladas. **Inserción contextual:** al aceptar una propuesta, se navega a la sección donde el cambio aplica (personaje → Personajes, beat → Outline, mundo → Mundo, biblia → Biblia, escena → Editor) reusando el flujo propuesta→diff→aceptar/descartar del chat. Nueva función pura `lib/actionTargets.ts` (`getActionsTarget`) + 10 tests. **a11y:** input con `aria-label` descriptivo + label visible oculto, región `role="log"` (`aria-live="polite"`) que anuncia las respuestas nuevas del co-writer (se reinicia tras 6s), foco devuelto al input tras enviar, inserción contextual/aceptar/descartar/deshacer anunciados vía live region global, jerarquía h1→h2→h3 y acordeón de U2 intactos. Commit `8f21f91`. **272 tests**, build+TS pasan, lint 0 errores. Verificado en browser: input sticky con `position: sticky; bottom: 0` + card de altura fija, scroll interno de mensajes con el input anclado al fondo, `aria-label` en el árbol de accesibilidad, live region presente. **Revisada por Agente B (U8): aprobada con 2 correcciones a11y** (foco tras enviar roto por el textarea `disabled`; pérdida de foco a `<body>` al aceptar/descartar/deshacer) — aplicadas en U8, commit `8ec5511`.
- [x] **U8 (B) — Cierre de la Fase 4: tests del layout + auditoría a11y + verificación** — fix test flaky de DB verificado estable (5/5; el `7c2432c` ya eliminó el flaky del sort). **10 tests nuevos** del layout: `StorySections.test.tsx` (acordeón `aria-expanded`/`aria-controls` + body `hidden`, scrollspy `IntersectionObserver`→sección activa, foco de sección) y `ChatPanel.test.tsx` (input `aria-label`, live region `role="log"`, foco tras enviar, inserción contextual, descartar devuelve foco). **Auditoría a11y final:** teclado, foco visible, landmarks, contraste AA, anuncio AT — se corrigieron 2 hallazgos de foco de U7: (1) foco tras enviar se difiere con `setTimeout(0)` porque el textarea `disabled` no tomaba foco; (2) nuevo `requestSectionFocus` (nonce en store, patrón `requestEditorFocus`) que `StorySections` observa para enfocar el heading de la sección destino al aceptar, y foco al input al descartar/deshacer (WCAG 2.4.3). **Fix tsc en tests:** 4 errores de tipo pre-existentes corregidos (`StarterPicker.test.tsx`, `bibleSync.test.ts` x2, `export.test.ts`) → `tsc --noEmit` limpio. Commit `8ec5511`. **282 tests**, build+TS pasan, lint 0 errores. Fase 4 completa y lista para release v0.9.0.

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
- [x] **Release v0.8.0** + docs — bump a v0.8.0, CHANGELOG con features del backlog B1-B7, tag `v0.8.0` + GitHub Release. Commit `f96075c`. **Backlog completo.**

## Backlog (B1-B7) — pipeline de revisión cruzada A/B

> Plan en [ROADMAP.md](./ROADMAP.md). Cada item = commit atómico + push + actualizar ROADMAP/STATUS. A desarrolla impares, B pares; se revisan mutuamente.

- [x] **B1 — Tests de `lib/db.ts`** (fake-indexeddb). Commits `b5d0c17`, `88ac174`, `13b0914`, `6a9220c`. 202 tests. Aprobado tras 2 rondas de revisión cruzada.
- [x] **B2 — Tests de componentes** (jsdom + testing-library). Commits `9546e82`, `f3fd795`, `13b0914`, `6a9220c`. 202 tests. Aprobado tras 2 rondas.
- [x] **B3 — Export PDF / DOCX** — `docx` + `pdfmake` client-side. Commits `b064c36`, `a9eb65c`, `461b1bc`, `1afb734` (CI Node 22). 204 tests. Aprobado tras revisión multi-ronda.
- [x] **B4 — Búsqueda entre escenas** — `lib/search.ts` (lógica pura) + `SearchPanel.tsx` (modal global). Busca en contenido/título/summary, agrupa por capítulo con snippet + conteo, click navega a la escena, find/replace con confirmación. Commit `d8f37ad`. 21 tests nuevos. **225 tests**, build+TS pasan, lint 0 errores. **Revisado por B: fix de race condition en `handleReplace`** (updateScene sin await + read-modify-write concurrente perdía cambios; ahora agrupa por escena + await secuencial). Commit `bbd3f4e`.
- [x] **B6 — Versioning / snapshots** — `lib/snapshots.ts` (lógica pura: dedupe de idénticos, diff por líneas, formato de timestamp) + store `sceneSnapshots` (DB v7→v8) + snapshot al guardar en `updateScene` (estado previo, dedupe) + `VersionHistoryPanel.tsx` (historial con timestamp, diff, restaurar con confirmación). Commit `f7fab09`. 19 tests nuevos. **244 tests**, build+TS pasan (solo 3 errores pre-existentes), lint 0 errores. **Revisado por B: correcto, sin correcciones** (dedupe, LCS con líneas repetidas, snapshot del estado previo, sin race con B7, migración v8, cascade, panel). Observación menor no bloqueante: id de snapshot `${sceneId}:${createdAt}` podría colisionar en el mismo ms (imposible en práctica).
- [x] **B7 — Streaming en el editor** — `runAI` migrado a `ollamaChatStream` (SSE existente). Texto insertado en vivo mientras se genera; `streamingRef` suprime el autosave durante el stream (sin guardados parciales); ante abort/error se revierte la propuesta parcial. Commit `af3cfbf`. **225 tests**, build+TS pasan, lint 0 errores. **Revisado por A: 2 bugs corregidos** (cierre de diálogo caía al final del doc en vez de tras el bloque; primer chunk con solo whitespace no reemplazaba la selección). Commit `28fdb1e`.

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

**Bloque de features 2026-08-17 COMPLETO** (a11y, mobile, PWA, export, co-writer U5+, roles especializados). 377 tests. Validación AT manual verificada por Gonzo.

**Considerar:** bump de versión del bloque (los features post-v0.16.1 no tienen release).

**Futuro (largo plazo):** multi-usuario/sync, mocks de tests frágiles, iconos PWA más pulidos, UI de selector de rol más rica (chips/tabs).
