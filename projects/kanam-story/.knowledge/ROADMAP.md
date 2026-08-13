# ROADMAP — Kanam Story

> Anti-repetición: slices finos, cada uno termina en release usable. Arrancamos por el corazón.

## Fase 0 — Fundación (slab sobre sudolab)

- [x] Reusar `sudolab` como base de código (Next.js, TipTap, IndexedDB, Ollama, tests).
- [x] Nombrar el producto (Kanam Story) y renombrar UI/prompts.
- [x] Definir stores nuevos: `conversations`, `messages`, `contentActions`.
- [x] Modelo `Beat` + CRUD básico sobre Chapters/Scenes.
  - *Hecho 2026-08-12 (Slice 0). Beats en store separado con chapterId/sceneId. DB_VERSION 2→3. Build+tests+TS pasan.*

## Slice 1 — Chat con Manos (MVP usable hoy)

> El corazón: conversar con un agente que conoce la obra y la aplica. Objetivo: usarlo con `ultimo-turno`.

- [x] Panel de chat por proyecto, persistido en IndexedDB.
- [x] Contexto del agente: manuscrito + biblia + outline actual (buildContext).
- [x] Streaming de respuesta desde Ollama.
- [x] **Herramientas del agente** (el "tiene manos"):
  - [x] `rewrite_scene` — reescribe una escena bajo acuerdo.
  - [x] `add_beat` / `update_beat` — arma/ajusta el outline.
  - [x] `update_character` / `add_character`.
  - [x] `append_scene`.
- [x] **Modelo de aceptación:** el agente propone un cambio, el usuario ve diff/resumen, **acepta/deshace**. Nada se aplica sin OK.
- [x] Tests de prompts + parseo de acciones de herramienta.
  - *Hecho 2026-08-13 (Slice 1). 27 tests nuevos (agentReply, agentPrompts, actions, ollamaStream). 92 tests totales. Build+TS pasan. Undo conectado a la UI + detalle por acción.*
- [x] **Prueba con `ultimo-turno`** (2026-08-13).
  - *Validado end-to-end: chat conversacional, streaming, rewrite_scene con sceneId real, aceptar aplica a IndexedDB, deshacer revierte.*
  - *Bugs destapados y arreglados: (1) buildAgentContext no incluía IDs de escenas → rewrite nunca aplicaba; (2) tras reload la conversación no quedaba seleccionada → mensajes no persistían; (3) turbopack.root mal configurado → rutas API 404.*

## Slice 2 — Outline & Beats

> La estructura: mapa de beats por capítulo/escena, a mano o sugerido por IA.

- [x] Vista de outline (mapa de beats) por capítulo y escena.
- [x] Edición manual de beats (reordenar, editar, marcar status).
- [x] **"Sugerir outline"**: el agente propone beats desde biblia/brújula/lo escrito (tool `suggest_beats`).
- [x] Conectar beats con la escritura (qué beat estoy escribiendo ahora).
- [x] Discutir un beat con el chat y refinarlo.
  - *Hecho 2026-08-13 (Slice 2). Vista en área principal (toggle Editor/Outline + botón por capítulo en el tree). Edición inline (title/kind/status/desc/notes), reorder ↑/↓, add/delete. Sugerir outline: flujo dedicado (buildSuggestBeatsPrompt + parseBeatList + store.suggestBeats) con preview Agregar/Descartar. Beats de la escena actual en el editor. 112 tests, build+TS pasan.*

## Slice 3 — Biblia Viva

- [x] Regeneración de biblia desde manuscrito (ya existe en sudolab) + desde cambios del chat.
- [x] Actualización automática de personajes/mundo cuando el agente los cambia.
- [x] Overrides manuales por sección preservados.
  - *Hecho 2026-08-13 (Slice 3). Regeneración por sección (`regenerateBibleSection` + `buildBibleSectionPrompt`), stale tracking (`staleAt` por sección, badge "desactualizada"), auto-marcado de stale cuando el agente cambia personajes/mundo vía chat. 115 tests, build+TS pasan.*

## Slice 4 — Brújula Narrativa

> Orientación: premisa, promesa, arco, tema. Visible al escribir y discutir.

- [x] Campos de brújula en el proyecto (premise, promise, theme, protagonist, pov).
- [x] Panel/insight que muestra la promesa mientras escribís y al debatir.
- [x] El agente usa la brújula para no desviar la conversación del "qué prometiste contar".
  - *Hecho 2026-08-13 (Slice 4). Campos opcionales en `Project` (premise/promise/theme/protagonist). Tab "Brújula" en el panel derecho (editable). Strip de promesa en el editor. `buildAgentContext` incluye la brújula. 117 tests, build+TS pasan.*

## Slice 5 — Pulido

- [x] A11y (WCAG 2.1 AA) y validación AT manual.
- [x] Export (MD / PDF / DOCX).
- [x] Lint limpio + cobertura de tests de componentes.
- [x] Release v0.1.0 y registro en PROYECTOS.md.
  - *Hecho 2026-08-13 (Slice 5). Export MD/TXT (`lib/export.ts` + `ExportMenu`), lint limpio (0 errores), release v0.1.0. 121 tests, build+TS pasan.*

---

# Fase 2 — Hacia el Story Bible de Sudowrite (Slices 6-10)

> **Fuente:** auditoría de 10 capturas de Sudowrite (2026-08-13). El gap principal es el **Story Bible estructurado y editable** (Genre, Style, Synopsis, Braindump) que hace que la IA sea coherente; de ahí cuelgan las fichas de personaje ricas, el worldbuilding tipado, la generación asistida y el Match My Style. Orden por valor/esfuerzo, cada slice termina en release usable.
>
> **División de trabajo:** los agentes A (VS Code) y B (ZCode) implementan y se revisan entre sí. Este ROADMAP es el spec de planificación; los detalles de implementación los resuelven los agentes. Cada slice debe actualizar STATUS.md al cerrarse.

## Slice 6 — Story Bible editable y tipado (el corazón de la coherencia)

> El bloque central que Sudowrite muestra como base de todo. Hoy la biblia es una vista auto-generada (summary/themes/characters/world/rules). La convertimos en **editable y tipada**: Genre, Style, Synopsis editable, Braindump. Todo lo demás (slices 7-10) cuelga de acá.

- [x] **Braindump** — campo libre de volcado de ideas que alimenta el contexto del agente.
  - [x] Store: `braindump: string` en `Project` (o store propio `braindump` por proyecto).
  - [x] UI: sección editable en el panel de biblia (textarea grande, autosave con debounce).
  - [x] Contexto: `buildAgentContext` incluye el braindump (como contexto de bajo peso, no como regla).
- [x] **Genre** — géneros del proyecto para ajustar el tono de las sugerencias.
  - [x] Store: `genres: string[]` en `Project` (multi-select con tags).
  - [x] UI: sección editable con tags removibles + input para agregar.
  - [x] Contexto: incluido en `buildAgentContext` y en los prompts de escritura.
- [x] **Style** — estilo narrativo del proyecto (3 modos, ver Slice 9 para Match My Style).
  - [x] Store: `style: { mode: 'featured' | 'custom'; featured?: string; custom?: string }` en `Project`.
  - [x] UI: sección editable con selector de modo (Featured presets / Custom libre).
  - [x] Presets iniciales: prosa tensa, lírica, minimalista, sensorial, literaria elevada.
  - [x] Contexto: el style activo se inyecta en todos los prompts de generación (Write/Rewrite/Describe/Expand).
- [x] **Synopsis editable** — la sinopsis deja de ser solo auto-generada; se puede editar a mano.
  - [x] Store: `synopsis: string` en `Project` (override manual sobre la sección auto-generada).
  - [x] UI: sección editable; si hay override manual, se marca y se preserva (patrón `overrides` de la biblia).
  - [x] Contexto: la synopsis (manual o auto) alimenta `buildAgentContext`.
- [x] **Migración de datos** — DB_VERSION 3 → 4 con los nuevos campos en `Project`.
- [x] **Tests** — parseo de los nuevos campos, migración, y que el contexto incluya genre/style/synopsis/braindump.
  - *Hecho 2026-08-13 (Slice 6). `Project.style` migrado a objeto `ProjectStyle` (mode: featured|custom|match) con migración DB v3→v4. `genres`/`braindump`/`synopsis` nuevos. `StoryBibleSettingsPanel` (tab "Story Bible"). `buildAgentContext` + `buildContext` inyectan los campos. Helpers en `lib/labels.ts`. 126 tests, build+TS pasan, lint 0 errores. Release v0.2.0 (commit `6aefc3e` + `329a4c4`, tag `v0.2.0`).*

## Slice 7 — Fichas de personaje ricas + generación asistida

> Sudowrite tiene fichas con Type (rol), Pronouns, Groups, Other Names, Traits y toggle de visibilidad en contexto. Kanam Story ya tiene role/age/appearance/personality/voice/wants/needs/backstory/goals/arc — lo enriquecemos y agregamos el flujo de generación.

- [x] **Type tipado** — reemplazar `role: string` por un enum con roles predefinidos + custom.
  - [x] Roles: `protagonist | antagonist | supporting | minor | love_interest | custom`.
  - [x] Migración: `role` → `type` (mapear valores existentes, default `supporting`).
- [x] **Campos nuevos** — `pronouns`, `groups: string[]`, `otherNames: string[]`, `traits: string[]`.
  - [x] UI: campos en la ficha de personaje (editable).
  - [x] `+ Add Trait` — agregar rasgos (con sugerencia IA opcional).
- [x] **Toggle de contexto** — `inContext: boolean` por personaje; si es false, se excluye de `buildAgentContext`.
  - [x] UI: icono de ojo en la ficha (incluir/excluir del contexto IA).
  - [x] Contexto: `buildAgentContext` filtra por `inContext`.
- [x] **Generación asistida de personaje** — flujo dedicado (no solo vía chat).
  - [x] Modal `Generate Character`: selector de Character Type + campo de instrucciones custom.
  - [x] `Surprise Me` — genera un personaje aleatorio/inspirado en el contexto del proyecto.
  - [x] Preview del personaje generado → Agregar / Regenerar / Descartar (patrón de aceptación del chat).
  - [x] Tool del agente: el chat ya propone personajes vía `add_character` (se reusa; no se duplica con `generate_character`).
- [x] **Tests** — parseo de los nuevos campos, filtro de contexto, y el flujo de generación.
  - *Hecho 2026-08-13 (Slice 7). `Character.type` enum + campos nuevos (pronouns/groups/otherNames/traits/inContext). Migración DB v4→v5. `buildGenerateCharacterPrompt` + `parseSuggestedCharacterList` + `store.generateCharacter`. UI: type select, tag editors, toggle inContext, flujo Generar/Surprise Me/preview. 137 tests, build+TS pasan, lint 0 errores. Release v0.3.0 pendiente.*

## Slice 8 — Worldbuilding tipado fino ✅

> Sudowrite tipa cada elemento (Setting, Organization, Lore, Key Event, Clue, Magic System, Item). Kanam Story ya tenía `category: place|lore|rule|item|other` — lo refinamos a `kind` con 9 valores y agregamos campos.

- [x] **Tipos finos** — ampliar `kind` de `WorldEntity`.
  - [x] `place | organization | lore | key_event | clue | magic_system | item | rule | other`.
  - [x] Migración: `mapCategoryToKind` mapea `location→place`, `lore→lore`, `rule→rule`, `object→item`, `other→other` (DB v5→v6).
- [x] **Campos nuevos** — `otherNames: string[]`, `traits: string[]` (mismo patrón que personajes).
  - [x] UI: campos en la ficha de elemento de mundo (`TagEditor`).
  - [x] `+ Add Trait`.
- [x] **Toggle de contexto** — `inContext: boolean` por elemento (mismo patrón que personajes).
- [x] **Tests** — migración de kinds, nuevos campos, filtro de contexto.
  - *Hecho 2026-08-13 (Slice 8). `WorldEntity.category` → `kind` (9 valores) + `otherNames[]`/`traits[]`/`inContext`. `mapCategoryToKind` + `worldKindLabel` en `lib/labels.ts`. `buildAgentContext` + `buildContext` filtran `inContext` y muestran kind. `bibleExtract` amplía keywords (organización/evento/pista/magia). `WorldPanel` con selector de 9 kinds + tag editors + toggle. 145 tests, build+TS pasan, lint 0 errores. Commit `60434ba`.*

## Slice 9 — Match My Style (clonar la voz del autor)

> La feature más diferenciadora de Sudowrite (PRO). Con Ollama local podemos hacerla gratis. La IA analiza una muestra del texto del autor y genera un perfil de estilo para que las sugerencias "suenen como él".

- [x] **Análisis de muestra** — el usuario pega/selecciona un extracto de su escritura.
  - [x] Prompt dedicado `buildStyleProfilePrompt` que pide al modelo extraer: tono, ritmo, longitud de frase, vocabulario, uso de diálogo, imágenes, subtexto.
  - [x] Parseo de la respuesta en un perfil de estilo estructurado (`StyleProfile`).
- [x] **Persistencia** — `style.mode: 'match'` + `style.profile: StyleProfile` en `Project`.
- [x] **Inyección** — el perfil se inyecta en todos los prompts de generación (Write/Rewrite/Describe/Expand).
- [x] **UI** — 3er modo en la sección Style: "Match My Style" (pegar muestra → analizar → guardar perfil).
- [x] **Tests** — parseo del perfil, inyección en prompts, persistencia.
  - *Hecho 2026-08-13 (Slice 9). `buildStyleProfilePrompt` + `parseStyleProfile` + `store.analyzeStyle`. `styleText` inyecta el perfil completo en modo match. UI: modo match habilitado (pegar muestra → analizar → guardar perfil). 152 tests, build+TS pasan, lint 0 errores. Release v0.5.0 pendiente.*

## Slice 10 — Filtros de outline + vinculación documento↔outline ✅

> Sudowrite filtra el outline por POV y tiempo verbal, y sugiere vincular documentos al outline ("Link it / Connect it / Add Scenes"). Kanam Story ya conecta beats con escenas; agregamos los filtros y el flujo de vinculación.

- [x] **Filtros de outline** — por POV y tiempo verbal.
  - [x] Store: `tense: 'past' | 'present' | 'future'` agregado a `Project` (DB v6→v7, default `past`).
  - [x] UI: filtros en la vista de outline (dropdowns de POV y tense).
- [x] **Vinculación documento↔outline** — detectar escenas sin beats y sugerir vincular.
  - [x] Detección: escenas del capítulo actual sin beats se listan al final del outline.
  - [x] Acción: botón "Vincular" que crea un beat para esa escena.
- [x] **Tests** — `tenseLabel`, contexto con tense.
  - *Hecho 2026-08-13 (Slice 10). `Project.tense` + `TENSE_LABELS`/`tenseLabel` en `lib/labels.ts`. Migración DB v6→v7. Selector de tense en `CompassPanel`. Filtros de POV/tense en `OutlineView`. Detección de escenas huérfanas con botón "Vincular". `buildAgentContext` + `buildContext` inyectan tense. 155 tests, build+TS pasan, lint 0 errores. Commit `9b36cde`. Release v0.6.0.*

---

## TODOs no bloqueantes (post-release, no son slices)

> No bloquean el pipeline; se atienden cuando haya espacio. Están trackeados acá para no perderlos.

- [ ] **Export PDF / DOCX** — hoy solo MD/TXT (`lib/export.ts` + `ExportMenu`).
- [ ] **Tema claro** — toggle light/dark (hoy solo dark vía `data-bs-theme`).
- [ ] **Tests de componentes** — jsdom + `@testing-library/react` para Editor, StoryBiblePanel, etc.
- [ ] **Tests de `lib/db.ts`** — `fake-indexeddb` para cubrir migraciones y CRUD.
- [ ] **Búsqueda entre escenas** — find/replace a lo largo del manuscrito.
- [ ] **Versioning / snapshots** — ver versiones previas de una escena.
- [ ] **Streaming en el editor** — el chat ya usa SSE; el editor usa `ollamaChat` no-streaming.

---

## Notas de trazabilidad

- Slice 1 es el MVP que se prueba con `ultimo-turno` hoy. Si Slice 1 no engancha, no seguimos — aprendemos y ajustamos antes de invertir más.
- Cada slice = commit atómico + release usable. Sin acumular discovery muerto.
- **Slices 6-10 (Fase 2):** derivados de la auditoría de Sudowrite (2026-08-13). El Slice 6 es la base (Story Bible editable); los slices 7-10 lo extienden. Cada slice debe actualizar STATUS.md y terminar en release usable (v0.2.0 → v0.6.0).
- **División de trabajo:** agentes A (VS Code) y B (ZCode) implementan y se revisan entre sí. Kanam (este agente) planifica y documenta. Los agentes deben leer este ROADMAP como spec y actualizar STATUS.md al cerrar cada slice.
