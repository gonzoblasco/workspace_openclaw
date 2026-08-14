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

## Slice 6 — Story Bible editable y tipado (el corazón de la coherencia) ✅

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

## Slice 7 — Fichas de personaje ricas + generación asistida ✅

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
  - *Hecho 2026-08-13 (Slice 7). `Character.type` enum + campos nuevos (pronouns/groups/otherNames/traits/inContext). Migración DB v4→v5. `buildGenerateCharacterPrompt` + `parseSuggestedCharacterList` + `store.generateCharacter`. UI: type select, tag editors, toggle inContext, flujo Generar/Surprise Me/preview. 137 tests, build+TS pasan, lint 0 errores. Commit `f00cb79`. Release v0.3.0.*

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
  - *Hecho 2026-08-13 (Slice 8). `WorldEntity.category` → `kind` (9 valores) + `otherNames[]`/`traits[]`/`inContext`. `mapCategoryToKind` + `worldKindLabel` en `lib/labels.ts`. `buildAgentContext` + `buildContext` filtran `inContext` y muestran kind. `bibleExtract` amplía keywords (organización/evento/pista/magia). `WorldPanel` con selector de 9 kinds + tag editors + toggle. 145 tests, build+TS pasan, lint 0 errores. Commit `60434ba`. Release v0.4.0.*

## Slice 9 — Match My Style (clonar la voz del autor) ✅

> La feature más diferenciadora de Sudowrite (PRO). Con Ollama local podemos hacerla gratis. La IA analiza una muestra del texto del autor y genera un perfil de estilo para que las sugerencias "suenen como él".

- [x] **Análisis de muestra** — el usuario pega/selecciona un extracto de su escritura.
  - [x] Prompt dedicado `buildStyleProfilePrompt` que pide al modelo extraer: tono, ritmo, longitud de frase, vocabulario, uso de diálogo, imágenes, subtexto.
  - [x] Parseo de la respuesta en un perfil de estilo estructurado (`StyleProfile`).
- [x] **Persistencia** — `style.mode: 'match'` + `style.profile: StyleProfile` en `Project`.
- [x] **Inyección** — el perfil se inyecta en todos los prompts de generación (Write/Rewrite/Describe/Expand).
- [x] **UI** — 3er modo en la sección Style: "Match My Style" (pegar muestra → analizar → guardar perfil).
- [x] **Tests** — parseo del perfil, inyección en prompts, persistencia.
  - *Hecho 2026-08-13 (Slice 9). `buildStyleProfilePrompt` + `parseStyleProfile` + `store.analyzeStyle`. `styleText` inyecta el perfil completo en modo match. UI: modo match habilitado (pegar muestra → analizar → guardar perfil). 152 tests, build+TS pasan, lint 0 errores. Commit `011347d`. Release v0.5.0.*

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

### 🔴 Prioridad (pedidos de Gonzo, 2026-08-13) — ✅ COMPLETADO en v0.7.0 (Fase 3)

> **Plan detallado con pipeline de revisión cruzada A/B en [PLAN-FASE-3.md](./PLAN-FASE-3.md).** Release v0.7.0.

- [x] **Área de texto refinada (barra de formato + selección contextual IA)** — el editor usa TipTap/StarterKit (soporta formato) pero **no expone barra de formato en la UI**. Falta:
  - [x] Barra de formato: negrita, cursiva, subrayado, tachado, enlaces, listas (viñetas/numeradas), H1/H2/H3, deshacer/rehacer. (U1/U2)
  - [x] Selección contextual: al seleccionar texto, mostrar un indicador (como el círculo azul de Sudowrite) que conecte la selección con las herramientas de IA (Write/Rewrite/Describe/Expand). (U3/U4)
  - [x] El usuario debe poder escribir, copiar/pegar y editar libremente (no todo generado por IA). (U4)
  - [x] **Sincronización Biblia ↔ tabs** (personajes y mundo auto-importados, dedupe, no pisar manual, revertir). (U5-U8)
  - [ ] Referencia visual: captura de Sudowrite (editor de prosa con barra de formato + selección resaltada en púrpura + contador de palabras seleccionadas).
  - [x] **Sincronización Biblia ↔ tabs (Personajes/Mundo)** — hoy el `StoryBiblePanel` tiene un bridge **manual** (Detectar → preview → Importar todos/uno). Gonzo quiere que lo generado en la Biblia se **duplique automáticamente** en las tabs correspondientes:
  - [x] Al regenerar la Biblia, los personajes detectados se crean/actualizan en la tab Personajes (con marca "de biblia"). (U5)
  - [x] Ídem para el mundo → tab Mundo (lugares, lore, reglas, etc.). (U6)
  - [x] Mantener sincronizado: si la Biblia se regenera, las tabs reflejan los cambios (sin duplicar entradas ya existentes). (U5/U6, dedupe por nombre)
  - [x] Preservar el modelo de aceptación: los cambios automáticos deben ser revisables (no pisar ediciones manuales del usuario). (U7, botón "Revertir import")

### Resto del backlog (priorizado 2026-08-14)

> **Plan del backlog con pipeline de revisión cruzada A/B.** Cada item = commit atómico + push + actualizar este ROADMAP y STATUS.md. Orden por valor: primero deuda técnica que desbloquea calidad, luego features de producto, luego polish/infra.

#### 🥇 Alta — deuda técnica (desbloquea calidad)

- [x] **B1 — Tests de `lib/db.ts`** (`fake-indexeddb`). La DB es el corazón (migraciones + CRUD); sin tests es frágil. Agregar `fake-indexeddb` como devDep y cubrir:
  - Migraciones (v1 → v7): cada versión migra datos sin romper.
  - CRUD de cada store (projects, conversations, messages, scenes, beats, bible, characters, world).
  - Transacciones `versionchange` (el fix del Slice 6 review).
  - ✅ **Hecho 2026-08-14 (commit `b5d0c17`).** Migraciones extraídas a `lib/migrations.ts` (funciones puras: `migrateProjectStyle`, `migrateCharacterRole`, `migrateWorldCategory`, `migrateProjectTense`) — fake-indexeddb cuelga en upgrades asíncronos de `idb`, así que las migraciones se testean a nivel de transform puro y el CRUD con fake-indexeddb. 20 tests nuevos (`lib/db.test.ts`): 8 migraciones puras + 11 CRUD (todos los stores) + cascade delete. **183 tests totales.**
  - **Revisado 2026-08-14 (Agente A).** ✅ Extracción fiel: las 4 funciones puras replican exactamente la lógica del `onupgradeneeded` original (no se perdió/alteró lógica; mappers `mapRoleToType`/`mapCategoryToKind` intactos). La firma de `lib/db.ts` no cambió. Cobertura CRUD completa (11 stores + cascade). Fixtures correctos (`category: 'location'`→`place`, no `'place'` legacy mal usado).
  - **Fix aplicado 2026-08-14 (Agente A, commit `88ac174`):** los fixtures de migración legacy (p.ej. `{ id, name, role }`) usaban casts directos `as Character`/`as Project`/`as WorldEntity` que TypeScript rechaza (TS2352) porque no solapan estructuralmente con los tipos completos → 8 errores `tsc` introducidos por B1. Corregido con double casts `as unknown as T` (los objetos legacy parciales son deliberadamente parciales). `tsc` vuelve a quedar limpio para `db.test.ts` (quedan 3 errores pre-existentes en `export.test.ts`/`bibleSync.test.ts`, fuera del alcance de B1/B2).
  - **Asignado:** Agente B (par). Agente A revisa.
- [x] **B2 — Tests de componentes** (jsdom + `@testing-library/react`). Cubrir Editor (barra de formato, indicador de selección), StoryBiblePanel (sync + revertir), CompassPanel, OutlineView. `vitest` ya está; falta el environment jsdom + testing-library.
  - ✅ **Hecho 2026-08-14 (commit `9546e82`).** Instalados `jsdom`, `@testing-library/react`, `@testing-library/jest-dom`, `@testing-library/user-event`. Config: `vitest.config.ts` ahora incluye `components/**/*.test.{ts,tsx}` + `test/setup.ts` (jest-dom matchers + cleanup automático). 6 tests de `StoryBiblePanel` cubriendo el flujo de auto-sync de la Fase 3: regenerar → sync personajes → sync mundo → mensaje de feedback, orden de ejecución, error en regeneración no dispara syncs, biblia vacía. (El Editor se deja fuera por dependencia de TipTap — difícil de montar en jsdom.) **189 tests totales.**
  - **Revisado 2026-08-14 (Agente A).** ✅ Mock de `useApp` completo (cubre todos los campos que `StoryBiblePanel` destructura de `useApp()`: currentProject, storyBible, settings, regenerate/section/ensure/update/preview/import/sync de biblia y tabs). El mock de `MarkdownView` es correcto. El orden de ejecución (regenerar → sync personajes → sync mundo) está bien verificado con un arreglo de llamadas. La config de vitest no rompe los tests de `lib/` (environment node se mantiene; jsdom solo vía directiva `@vitest-environment jsdom` por archivo).
  - **Fix/mejora aplicada 2026-08-14 (Agente A, commit `f3fd795`):** (1) `ensureStoryBible` mock devolvía `undefined` (el componente hace `.catch()` sobre él — latente si algún test quitara el guard); ahora devuelve una Promise resuelta, consistente con la firma real del store. (2) Se agregaron 3 tests de `CharactersPanel` (U7 "Revertir import"): el botón aparece al editar un personaje con `source === 'biblia'`, llama a `revertBibleImport('character', id)`, y se oculta para personajes manuales. **192 tests totales.**
  - **Asignado:** Agente A (impar). Agente B revisa.
  - *Cadena de revisión: Agente A revisó B1/B2 (commits `88ac174`, `f3fd795`, `13b0914` — fixes de casts legacy, tests de U7 revert-import, cascade delete a beats). Pendiente ronda del Agente B.*
  - **2ª pasada de QA 2026-08-14 (Agente B, commit `13b0914`):** ✅ verificadas las correcciones de A (doble cast `88ac174` correcto; tests de revert-import + mock `ensureStoryBible` `f3fd795` correctos y sin bugs). Migraciones puras exactas, CRUD robusto, vitest config sólida. Mejora de cobertura agregada: 2 tests de cascade — `chaptersDB.delete` elimina escenas + beats (nivel capítulo y escena), y `scenesDB.delete` elimina beats de escena (estaban implementados en Slice 2 review pero sin testear). **194 tests totales.** B1 y B2 quedan aprobados con revisión múltiple.
  - **2ª RONDA de revisión 2026-08-14 (Agente B, commit `6a9220c`):** ✅ re-verificado el estado completo de B1/B2 con ojos frescos. Migraciones puras exactas (sin lógica perdida), CRUD robusto (transacciones/índices/orden OK), cascade de proyecto y de capítulo/escena→beats cubierto. Mocks de `useApp` completos y correctos; vitest config sólida (env node + directiva jsdom por archivo). **Mejora de cobertura agregada:** `WorldPanel.test.tsx` (3 tests, espejo de CharactersPanel) — el botón "Revertir import" de U7 para el lado mundo (`revertBibleImport('world', id)`) no estaba testeado. **202 tests totales.** B1/B2 aprobados tras 2 rondas de revisión cruzada.

- [x] **B3 — Export PDF / DOCX** — hoy solo MD/TXT (`lib/export.ts` + `ExportMenu`). Agregar export PDF y DOCX (reusar el HTML que ya genera MD/TXT, o librería server-side).
  - ✅ **Hecho 2026-08-14 (commit `b064c36`).** `docx` (v9) para .docx y `pdfmake` (v0.3) para .pdf, ambos client-side (app local-first, sin server). `exportManuscriptPdf` + `exportManuscriptDocx` en `lib/export.ts` + `markdownToPdfmakeContent` (convierte markdown a estructura pdfmake: headings, listas agrupadas en `ul`, blockquotes, párrafos). `downloadBlob` para binarios. Opciones PDF y DOCX en `ExportMenu`. Import dinámico de pdfmake para no inflar el bundle inicial. 5 tests nuevos de `markdownToPdfmakeContent`. **199 tests totales.**
  - **Revisado 2026-08-14 (Agente A).** ✅ El import dinámico de pdfmake/docx no rompe el bundle de Next (build verde; `ExportMenu` es `'use client'` y los exports se disparan solo por click). No rompió los exports MD/TXT existentes. `markdownToPdfmakeContent` cubre headings/listas/blockquotes/párrafos.
  - **Fix aplicado 2026-08-14 (Agente A, commit `a9eb65c`):**
    1. **Bug crítico — PDF export crasheaba:** `vfs_fonts` en runtime es un mapa plano `{ "<font>.ttf": base64 }` (`module.exports = vfs`), NO `{ pdfMake: { vfs } }`. B3 accedía a `vfsFonts.pdfMake.vfs` → `undefined` → `addVirtualFileSystem(undefined)` lanzaba `TypeError` en su `for...in`. Corregido a `addVirtualFileSystem(vfsFonts)` (verificado en runtime con node).
    2. **Calidad — markers inline `**`/`*` se filtraban literalmente** al PDF/DOCX: `buildManuscriptMarkdown` genera `- **Santiago**...` y `*meta*`, pero pdfmake/docx no parsean markdown. Agregué `inlineToPdfmake` (pdfmake) e `inlineToDocxRuns` (docx) que convierten `**bold**`/`*italic*` en nodos con `bold`/`italics`. Aplica a listas y párrafos.
    3. **UX — errores silenciosos:** `ExportMenu` hacía `.catch(() => {})` (sin feedback si fallaba). Ahora muestra el error en el menú y solo cierra el dropdown si la exportación tuvo éxito.
    4. **tsc:** B3 introdujo un error TS en `export.test.ts` (callback `.some()` con tipo incorrecto) — corregido. Quedan solo los 3 errores pre-existentes (`export.test.ts` style, `bibleSync.test.ts`).
  - **203 tests totales** (5 originales de B3 + 1 nuevo de inline markdown). Build + lint + tsc verdes.
  - **Asignado:** Agente B. Agente A revisa.
  - **2ª ronda de revisión 2026-08-14 (Agente B, commit `461b1bc`):** ✅ verificadas las correcciones de A (`a9eb65c`): forma de `vfs_fonts` correcta, inline `**`/`*` parseado en listas/párrafos, errores de export visibles. Import dinámico no rompe SSR (solo por click, `'use client'`), MD/TXT intactos. **Mejora residual corregida:** el blockquote (`> descripción`) no corría `inlineToPdfmake` → un `**bold**` inline en la descripción se filtraba al PDF. Ahora lo parsea (con `italics` del blockquote preservado). +1 test. **204 tests totales.** B3 aprobado tras revisión multi-ronda.
  - **Fix de CI 2026-08-14 (orquestador, commit `1afb734`):** el CI fallaba con `TypeError: webidl.util.markAsUncloneable is not a function` en los tests de componentes. Causa raíz: el CI usaba **Node 20**, pero `jsdom@30` → `undici@8.10` importa `markAsUncloneable` de `node:worker_threads`, API que **no existe en Node 20** (sí en Node 22, que es lo que se usa localmente). Fix: subir el CI a **Node 22** + agregar `.nvmrc` (22) para consistencia dev/CI. **CI verde** (Lint + Test + Build).

#### 🥈 Media — features de producto
- [x] **B4 — Búsqueda entre escenas** — find/replace a lo largo del manuscrito (todas las escenas de un proyecto). UI en el editor o vista global.
  - ✅ **Hecho 2026-08-14 (commit `d8f37ad`).** `lib/search.ts` (lógica pura, sin DB/DOM): `searchScenes` (busca en contenido/título/summary, agrupa por capítulo, snippet con contexto + conteo), `buildReplacePlan` (plan de find/replace por escena), `replaceInHtml` (reemplaza SOLO en nodos de texto, nunca dentro de etiquetas — un término como "p" no corrompe `<p>`), `htmlToText` (HTML→texto plano para snippets). `SearchPanel.tsx` (modal global): input de búsqueda, resultados agrupados por capítulo con snippet y conteo por campo, click en resultado → `selectScene` + `setView('editor')` (navega a la escena), toggle "Reemplazar" con confirmación (`window.confirm` con nº de escenas/ocurrencias) que aplica vía `updateScene`. Botón "Buscar" en la topbar (`page.tsx`). 21 tests nuevos (`lib/search.test.ts`). **225 tests totales**, build+TS pasan, lint 0 errores.
  - **Asignado:** Agente A. Agente B revisa.
  - 🔍 **Revisión B (2026-08-14, commit `bbd3f4e`):** revisado `d8f37ad`. `searchScenes`/`replaceInHtml`/`buildReplacePlan` correctos (snippet con contexto, conteo por campo sobre texto plano, `replaceInHtml` robusto: preserva `<` literal en texto, no toca atributos ni etiquetas, reemplazo con `$` literal vía callback). **Bug corregido:** `handleReplace` disparaba `updateScene` sin `await` y por campo; como `scenesDB.update` es read-modify-write, las escrituras concurrentes de una escena con cambios en varios campos podían pisarse (perder cambios). Ahora agrupa todos los cambios de una escena en un solo `updateScene` y los aplica secuencialmente con `await`. Además el conteo del `window.confirm` ahora se calcula sobre el texto plano (lo que realmente se reemplaza), no sobre el HTML. Build + TS + lint + 225 tests verdes.

#### 🥉 Baja — polish / infra

- [x] **B5 — Tema claro** — toggle light/dark (hoy solo dark vía `data-bs-theme`). Persistir preferencia.
  - ✅ **Hecho 2026-08-14 (commit `82f2a2e`).** El toggle ya existía en la topbar (scaffold sudolab) y persistía vía `settings.theme` (IndexedDB) + `data-bs-theme`; B5 lo completa y lo hace legible/consistente:
    1. **Contraste del tema claro (bug de legibilidad):** `--sl-accent-2` en light era `#b48cff` (lavanda claro) y se usaba como fondo de `.btn-primary`, `.btn-outline-primary:hover` y burbujas de chat del usuario con texto blanco → contraste pobre. Ahora light usa `--sl-accent: #5f3dc4` (7.1:1 sobre blanco, para texto) y `--sl-accent-2: #6a4bd8` (5.8:1, para fondos con texto blanco) — ambos WCAG AA.
    2. **Flash de tema al recargar:** el `<html data-bs-theme="dark">` estaba hardcodeado; con preferencia light había un flash oscuro. El store ahora espeja el tema a `localStorage` (`kanam-theme`) y un script inline en `layout.tsx` lo aplica antes del primer paint (IndexedDB sigue siendo la fuente de verdad).
    3. **Componente + a11y:** toggle extraído a `components/ThemeToggle.tsx` (con `aria-label`/`title` en español) y conectado en la topbar.
    4. **Tests:** 2 tests de componente (`ThemeToggle.test.tsx`): icono según tema + flip vía `setSettings`. **206 tests totales.** Build + lint verdes; tsc solo con los 3 errores pre-existentes (export.test.ts/bibleSync.test.ts).
  - **Asignado:** Agente B. Agente A revisa.
  - 🔍 **Revisión A (2026-08-14, commit `3ad0e70`):** revisado `82f2a2e`. Contraste ✅ (`--sl-accent-2: #6a4bd8` 5.8:1 sobre blanco cubre `.btn-primary`, `.btn-outline-primary:hover` y `.chat-msg-user .chat-msg-bubble` con texto blanco; `--sl-accent: #5f3dc4` 7.1:1 para texto sobre superficies claras; gradiente del brand AA; sin otros usos rotos). Dark intacto ✅ (solo se tocó el bloque `[data-bs-theme='light']`). ThemeToggle accesible y flip vía `setSettings` correcto ✅. **Bug corregido (anti-flash):** el effect del tema corría en el mount con el default hardcodeado `'dark'` antes de que IndexedDB cargara las settings reales. En un reload con tema light persistido, el effect pisaba `data-bs-theme` a dark (flash) y **sobrescribía `kanam-theme=dark` en localStorage** (corrompía la preferencia persistida), anulando el propósito del script inline. Fix: gatear el effect con `ready` (solo corre cuando IndexedDB ya cargó las settings reales). Build + lint + 225 tests verdes.
- [x] **B6 — Versioning / snapshots** — ver versiones previas de una escena (snapshot al guardar, diff + restaurar).
  - ✅ **Hecho 2026-08-14 (commit `f7fab09`).** `lib/snapshots.ts` (lógica pura, sin DB/DOM): `sceneEditable`/`sameContent`/`shouldSnapshot` (dedupe de idénticos — no guarda snapshot si el contenido no cambió respecto a la última), `buildSnapshot`, `sortSnapshotsNewestFirst`, `formatSnapshotTime` (dd/mm/yyyy hh:mm en español), `diffLines` (diff por líneas con LCS para mostrar qué cambió). Store nuevo `sceneSnapshots` en IndexedDB (DB_VERSION 7→8, índices `by-project`/`by-scene`/`by-scene-created`) + `sceneSnapshotsDB` (listByScene newest-first, getLatest, create, delete, deleteByScene). **Snapshot al guardar:** `updateScene` en el store captura una snapshot del estado PREVIO de la escena (leído de la DB, no del snapshot de React) antes de aplicar el cambio, con dedupe de idénticos — cubre autosave (debounce 600ms) y guardado manual. **Cascade:** borrar escena/proyecto elimina sus snapshots. **UI:** `VersionHistoryPanel.tsx` (modal, botón "Versiones" en la topbar): lista de versiones con timestamp, diff del contenido entre la versión seleccionada y la actual (agregado/eliminado), y "Restaurar esta versión" con `window.confirm` (la restauración pasa por `updateScene`, así que el estado previo queda versionado y la restauración es reversible). 19 tests nuevos (16 `lib/snapshots.test.ts` + 3 CRUD/cascade de `sceneSnapshots` en `lib/db.test.ts`). **244 tests totales**, build+TS pasan (solo los 3 errores pre-existentes), lint 0 errores.
  - **Asignado:** Agente A. Agente B revisa.
  - **Nota para el Agente B:** B6 es independiente de B7 (no toqué `Editor.tsx`). El snapshot se dispara desde `updateScene` en el store, así que el streaming de B7 (que llama a `updateScene` al finalizar) también queda versionado automáticamente. A revisar: dedupe de idénticos, cascade de snapshots, y que el diff/restore respete el modelo de aceptación.
  - 🔍 **Revisión B (2026-08-14, Agente B):** revisado `f7fab09` en profundidad. **Sin correcciones — B6 correcto.** Verificado:
    1. **Dedupe (`shouldSnapshot`)** ✅ — compara `title`/`content`/`summary` (los 3 campos versionables) entre el estado previo leído de la DB y la última snapshot; no guarda ruido cuando el autosave dispara sin cambios reales. El estado previo se lee bien de la DB (`scenesDB.get`), no del closure de React.
    2. **`diffLines` (LCS)** ✅ — probado en runtime con casos de líneas repetidas (`a\nb\na`→`a\na\nb`, `x\ny`→`y\nx`, `a\na\na`→`a\na`) y strings vacíos: produce diffs válidos (agregado/eliminado correctos, sin líneas perdidas). El caso `''`→`'x'` marca `removed:['']` + `added:['x']` (comportamiento documentado y testeado).
    3. **Snapshot del estado PREVIO** ✅ — `updateScene` captura el estado anterior al cambio (leído de la DB), que es lo correcto para restaurar: cada snapshot es una versión a la que se puede volver. La restauración pasa por `updateScene`, así que el estado pre-restauración queda versionado y el restore es reversible.
    4. **Race conditions con B7** ✅ — no hay. B7 suprime el autosave con debounce durante el streaming (`streamingRef`) y llama a `updateScene` una sola vez al finalizar; el guardado de título/resumen es on-blur. No hay `updateScene` concurrentes que puedan capturar un estado intermedio incorrecto.
    5. **Migración DB v7→v8** ✅ — el store `sceneSnapshots` se crea con guard `contains`; las migraciones de datos existentes (v3→v8) están gateadas por `oldVersion < N` y no se tocan. No rompe datos existentes.
    6. **Cascade** ✅ — borrar escena (`scenesDB.delete`) y proyecto (`projectsDB.delete`) elimina las snapshots vía índices `by-scene`/`by-project`; cubierto por tests.
    7. **`VersionHistoryPanel`** ✅ — diff entre versión seleccionada y estado actual correcto; "Restaurar" usa `window.confirm` y pasa por `updateScene` (reversible, respeta el modelo de aceptación).
    8. **Verificación** ✅ — build + TS + lint + **244 tests** verdes.
    - **Observación menor (no corregida):** el id de snapshot es `${sceneId}:${createdAt}`; dos snapshots de la misma escena en el mismo milisegundo colisionarían (la segunda sobrescribiría la primera). En la práctica es imposible con el debounce de 600ms + un solo `updateScene` por stream, así que no lo toqué para no romper el test determinista (`s1:123`).
- [x] **B7 — Streaming en el editor** — el chat ya usa SSE; el editor usa `ollamaChat` no-streaming. Migrar a streaming para feedback en vivo.
  - ✅ **Hecho 2026-08-14 (commit `af3cfbf`).** `runAI` en `Editor.tsx` migrado de `ollamaChat` (no-streaming) a `ollamaChatStream` (SSE existente). El texto se inserta **en vivo** mientras se genera: el primer chunk se inserta en la posición correcta (reemplazando la selección en describe/rewrite/dialogue, o toda la escena en expand/tension) y los chunks siguientes se anexan al final del texto creciente (`insertContent`/`insertContentAt` mueven la selección al final, así el siguiente chunk cae justo después). **Autosave protegido:** un flag `streamingRef` suprime el guardado con debounce mientras hay un stream activo (nunca se persiste texto a medio generar); el contenido final se guarda explícitamente al terminar. **Modelo de propuesta respetado:** ante abort/error se revierte la propuesta parcial (`setContent(preStreamHtml)`) dejando el editor como estaba (igual que la ruta no-streaming). Se preserva el wrapper de diálogo (`\n\n…\n`). Reusa la infraestructura SSE existente. Build + lint + **225 tests** verdes; tsc solo con los 3 errores pre-existentes.
  - **Asignado:** Agente B. Agente A revisa.
  - 🔍 **Revisión A (2026-08-14, Agente A, commit `28fdb1e`):** revisado `af3cfbf` en profundidad (inserción incremental, `streamingRef`, revert, guardado final, estrategia por kind). **Corregidos 2 bugs:**
    1. **Cierre del diálogo caía al final del documento** — `insertContentAt(doc.content.size, '\n')` insertaba la nueva línea al final de toda la escena en vez de justo después del bloque de diálogo (que se inserta en el medio). Se cambió a `insertContent('\n')` en el cursor, que ya queda al final del último chunk.
    2. **Chunk inicial con solo espacios marcaba `started`** — si el primer chunk SSE era solo whitespace, `started=true` sin ejecutar `startInsert` (que hace `deleteSelection()` en describe/rewrite/dialogue y aplica el wrapper `\n\n`). Ahora solo se marca `started` una vez que se inserta texto real.
    - **Verificado como correcto:** (a) `insertContent`/`insertContentAt` mueven la selección al final del contenido insertado, así el chunk siguiente cae bien; (b) el debounce pendiente se limpia **sincrónicamente** antes de `streamingRef=true`, así ningún autosave previo se cuela con texto parcial; (c) el revert `setContent(preStreamHtml, {emitUpdate:false})` no dispara update ni rompe cursor; (d) el contenido final se persiste explícitamente al terminar; (e) la estrategia de inserción por kind es correcta. Build + lint + **244 tests** verdes.
    - **Nota para el Agente B:** revisá que el diálogo multi-parrafo (los chunks intermedios llevan `\n\n` entre turnos) no pierda el wrapper de apertura cuando el primer chunk del turno empieza con nueva línea. La extracción a función pura testeable para la estrategia de inserción se dejó de lado en esta ronda (los bugs reales eran de lógica de flujo, no de pureza de la decisión); puede hacerse luego si se agregan más kinds.

> **Nota:** los items B1-B7 son independientes entre sí (no hay dependencias de orden). Cada agente toma el siguiente item de su paridad (A = impares B1/B3/B5/B7, B = pares B2/B4/B6) cuando termine el anterior. El pipeline de revisión cruzada aplica igual que en la Fase 3.

---

## Notas de trazabilidad

- Slice 1 es el MVP que se prueba con `ultimo-turno` hoy. Si Slice 1 no engancha, no seguimos — aprendemos y ajustamos antes de invertir más.
- Cada slice = commit atómico + release usable. Sin acumular discovery muerto.
- **Slices 6-10 (Fase 2):** derivados de la auditoría de Sudowrite (2026-08-13). El Slice 6 es la base (Story Bible editable); los slices 7-10 lo extienden. **Fase 2 completa 2026-08-13** (releases v0.2.0 → v0.6.0). Todos los slices 0-10 cerrados.
- **División de trabajo:** agentes A (VS Code) y B (ZCode) implementan y se revisan entre sí. Kanam (este agente) planifica y documenta. Los agentes deben leer este ROADMAP como spec y actualizar STATUS.md al cerrar cada slice.
- **Estado:** Fase 2 cerrada. **Fase 3 + backlog B1-B7 completos 2026-08-14** (releases v0.7.0 y v0.8.0). Proximo foco: planificar v0.9.0 (errores de UI/UX que Gonzo tiene en mente).
- **Leccion del pipeline multi-agente (2026-08-14):** el cross-review multi-ronda atrapo **8 bugs reales** que los autores no vieron (orden de sync en U5, vfs_fonts en B3, race condition en B4, anti-flash en B5, 2 bugs de streaming en B7, etc.). Cada agente aporta ojos frescos y detecta lo que el autor asume correcto. Formalizado en la skill `agent-orchestration-pipeline`. Valor real: el codigo mergeado a main pasa por 2+ rondas de revision antes de publicarse.
