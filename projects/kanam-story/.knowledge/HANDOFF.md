# HANDOFF — Kanam Story · Fase 2 completa (Slices 0-10)

**Fecha:** 2026-08-13
**Autor:** Agente A (Slice 10)
**Estado:** 🟢 FASE 2 COMPLETA. Slices 0-10 done. v0.6.0 RELEASED.
**Propósito:** documentar el cierre del Slice 10 y de la Fase 2 para revisión del Agente B.

---

## Estado actual

- **Slices 0-10 completos:** fundación, chat con manos, outline & beats, biblia viva, brújula, pulido (v0.1.0), story bible editable (v0.2.0), fichas de personaje ricas + generación (v0.3.0), worldbuilding tipado fino (v0.4.0), Match My Style (v0.5.0), outline filters + orphan linking (v0.6.0).
- **155 tests**, build + TS pasan, lint 0 errores, **CI verde** (GitHub Actions).
- **Repo:** `gonzoblasco/kanam-story` (público), remote `origin`. `.knowledge/` solo en el workspace (doble-git).
- **Releases:** v0.1.0 → v0.6.0 (todos taggeados en GitHub).

## Qué se construyó en Slice 10 (Agente A)

- **`Project.tense`** (`past|present|future`) + `TENSE_LABELS`/`tenseLabel` en `lib/labels.ts`. Migración DB v6→v7 (default `past`).
- **Selector de tense** en `CompassPanel` (junto al POV).
- **Filtros de outline** en `OutlineView`: dropdowns de POV y tense. Cuando el POV/tense del proyecto no coincide con el filtro, el contenido del capítulo se oculta con un hint.
- **Detección de escenas huérfanas**: escenas del capítulo actual sin beats se listan al final del outline con un botón "Vincular" que crea un beat para esa escena.
- **`buildAgentContext` + `buildContext`** inyectan el tense.
- Commit `9b36cde`. **155 tests**, build+TS pasan, lint 0 errores. Release v0.6.0.

## Qué se construyó en Slice 9 (Agente B)

- **`buildStyleProfilePrompt`** — extrae un perfil de estilo (tono, ritmo, frases, vocabulario, diálogo, imágenes, subtexto) de una muestra del autor.
- **`parseStyleProfile`** — parsea la respuesta a `StyleProfile` (escaneo progresivo de llaves).
- **`store.analyzeStyle(sample)`** — llama a Ollama y devuelve el perfil.
- **`styleText`** — en modo `match` inyecta el perfil completo en todos los prompts de generación.
- **UI (`StoryBibleSettingsPanel`)** — modo "Match My Style" habilitado: pegar muestra → analizar → guardar perfil.
- Commit `011347d`. **152 tests**, build+TS pasan, lint 0 errores.

## Review de Slice 8 (Agente B) — fixes aplicados

1. **🟡 `inferCategory`** quedó con nombre engañoso (ahora devuelve `kind`) → renombrado a `inferKind` (+ constante `KIND_KEYWORDS`).
2. **🟡 Keyword duplicado `'invasión'`** en `key_event` → eliminado.
- Commit `ec75acd`.

## Qué se construyó en Slice 8 (Agente A)

- **`WorldEntity.category` → `kind`** con 9 valores: `place | organization | lore | key_event | clue | magic_system | item | rule | other`.
- **Migración DB v5→v6** con `mapCategoryToKind` (mapea `location→place`, `object→item`, `regla→rule`, etc., default `other`).
- **Campos nuevos:** `otherNames[]`, `traits[]`, `inContext` (toggle de contexto).
- **`buildAgentContext` + `buildContext`** filtran `inContext === false` y muestran el kind + campos nuevos.
- **`bibleExtract`** amplía keywords de inferencia (organización, evento, pista, magia) y parsea los nuevos tags.
- **UI (`WorldPanel`):** selector de kind (9 opciones), tag editors, toggle inContext, badge de ojo excluido.
- **`buildBibleExtractPrompt`** actualizado al schema de 9 kinds.
- Commit `60434ba`. **145 tests**, build+TS pasan, lint 0 errores.

## Review de Slice 7 (Agente A) — fixes aplicados

1. **🟠 `update_character` del chat podía escribir un `type` inválido.** `isValidAction` validaba el `type` en `add_character` pero no en `update_character` (el `changes` era un objeto libre). **Fix:** si el modelo propone un cambio de `type`, se valida contra el enum; si es inválido, se descarta la acción. 3 tests nuevos.
2. **🟡 `mapRoleToType` tenía condiciones redundantes** (`r === 'protagonist'` era inalcanzable, ya lo cubría `r.includes('protagon')`). **Fix:** limpieza sin cambio de comportamiento.
3. **💡 Prompt `add_character` del chat** ahora lista los campos completos de la ficha rica (`age`, `appearance`, `groups`, `otherNames`) para paridad con `buildGenerateCharacterPrompt`.
- Commit `a533634`. **140 tests**.

## Qué se construyó en Slice 7 (Agente B)

- **`Character.type` enum** (`protagonist|antagonist|supporting|minor|love_interest|custom`) + migración DB v4→v5 (`role`→`type`, default `supporting`).
- **Campos nuevos:** `pronouns`, `groups[]`, `otherNames[]`, `traits[]`, `inContext`.
- **`buildAgentContext`** filtra `inContext === false` + muestra tipo y campos nuevos.
- **Generación asistida:** `buildGenerateCharacterPrompt` + `parseSuggestedCharacterList` + `store.generateCharacter`.
- **UI (`CharactersPanel`):** type select, tag editors, toggle inContext, flujo Generar/Surprise Me/preview (Agregar/Regenerar/Descartar).
- **Chat:** reusa `add_character` (no se duplica con `generate_character`).
- Commit `f00cb79`. **137 tests**, build+TS pasan, lint 0 errores.

## Review de Slice 6 (Agente B) — fixes aplicados

1. **🟠 Migración DB v3→v4** usaba `db.transaction()` dentro de `upgrade` (puede lanzar `InvalidStateError` en `onupgradeneeded`). **Fix:** ahora usa la `transaction` del versionchange (commit `dc7a8ad`).
2. **🟡 Modo "Match My Style"** era seleccionable pero no funcional (llega en Slice 9) → opción deshabilitada.

## Qué se construyó en Slice 6 (Agente A)

- **Story Bible editable y tipado:** `braindump`, `genres[]`, `style` → objeto `ProjectStyle` (`featured|custom|match`), `synopsis` editable.
- **Migración DB v3→v4** (style string → objeto) + helpers en `lib/labels.ts` (`styleText`, `STYLE_PRESETS`).
- **`StoryBibleSettingsPanel`** (tab "Story Bible"), patrón draft-and-commit.
- **Contexto:** `buildAgentContext` + `buildContext` inyectan genres/style/braindump/synopsis.
- Commits: `6aefc3e` (Slice 6), `acc190e` (CI), `329a4c4` (release v0.2.0).

---

# Fase 2 — Hacia el Story Bible de Sudowrite (Slices 7-10)

> **Fuente:** auditoría de 10 capturas de Sudowrite (2026-08-13). El gap principal era el Story Bible estructurado y editable (resuelto en Slice 6); de ahí cuelgan las fichas de personaje ricas, el worldbuilding tipado, la generación asistida y el Match My Style.
>
> **División de trabajo:** los agentes A (VS Code) y B (ZCode) implementan y se revisan entre sí. Kanam planifica y documenta; este ROADMAP es el spec. Cada slice: implementar → testear → build+TS → lint → **actualizar STATUS.md** → commit atómico → release usable.

## Slice 7 — Fichas de personaje ricas + generación asistida (→ v0.3.0) ✅

- [x] **Type tipado** — `role` → enum `type` (`protagonist|antagonist|supporting|minor|love_interest|custom`). Migración DB v4→v5.
- [x] **Campos nuevos** — `pronouns`, `groups[]`, `otherNames[]`, `traits[]` + UI (tag editors).
- [x] **Toggle de contexto** — `inContext`; `buildAgentContext` filtra.
- [x] **Generación asistida** — `buildGenerateCharacterPrompt` + `parseSuggestedCharacterList` + `store.generateCharacter`; UI Generar/Surprise Me/preview. Chat reusa `add_character`.
- [x] **Tests** — 137 totales. Commit `f00cb79`.

## Slice 8 — Worldbuilding tipado fino (→ v0.4.0) ✅

- [x] Kinds finos (`place|organization|lore|key_event|clue|magic_system|item|rule|other`) + migración DB v5→v6 (`mapCategoryToKind`).
- [x] Campos nuevos (`otherNames[]`, `traits[]`) + toggle `inContext`.
- [x] `buildAgentContext` + `buildContext` filtran `inContext` y muestran kind; `bibleExtract` amplía keywords.
- [x] Tests — 145 totales. Commit `60434ba`.

## Slice 9 — Match My Style (→ v0.5.0) ✅

- [x] `buildStyleProfilePrompt` + `parseStyleProfile`; `style.mode: 'match'` + `style.profile`.
- [x] Inyección del perfil en todos los prompts de generación (`styleText`).
- [x] UI: 3er modo "Match My Style" habilitado (pegar muestra → analizar → guardar).
- [x] Tests — 152 totales. Commit `011347d`.

## Slice 10 — Filtros de outline + vinculación (→ v0.6.0) ✅

- [x] Filtros por POV y tiempo verbal (`tense: 'past'|'present'|'future'`).
- [x] Detección de escenas sin beats + sugerir vincular (link/connect).
- [x] Tests — 155 totales. Commit `9b36cde` + release v0.6.0.

---

## Notas para los agentes

- **No romper el modelo de aceptación del chat** (propuesta → diff → aceptar/deshacer).
- **Migraciones de DB** siempre con bump de `DB_VERSION` y mapeo de datos existentes (patrón Slice 6: v3→v4).
- **`.knowledge/` no se commitea al repo del proyecto** (doble-git); los cambios de docs van al workspace.
- **Idioma:** UI y prompts en español; commits/PRs en inglés.
- **Al cerrar cada slice:** actualizar STATUS.md, ROADMAP.md y este HANDOFF.

## TODOs pendientes (backlog, no bloquean)

> Sincronizado con el ROADMAP (sección "TODOs no bloqueantes"). Se atienden cuando haya espacio.

- Export PDF / DOCX (hoy solo MD/TXT).
- Tema claro (toggle light/dark).
- Tests de componentes (jsdom + Testing Library).
- Tests de `lib/db.ts` (fake-indexeddb).
- Búsqueda entre escenas (find/replace).
- Versioning / snapshots (ver versiones previas de una escena).
- Streaming en el editor (el chat ya usa SSE; el editor usa `ollamaChat` no-streaming).

## Notas operativas

- **Errores `EMFILE: too many open files`** del watcher: del sandbox (límite de archivos), no de la app. No bloquean, pero impiden hot-reload — reiniciar el server para aplicar cambios.
- **Para levantar:** `PORT=3100 npm run dev`.
- **Modelo default:** `deepseek-v4-flash` (si está disponible).
