# HANDOFF — Kanam Story · v0.2.0 (Release)

**Fecha:** 2026-08-13
**Autor:** Agente A (Slice 6)
**Estado:** 🟢 v0.2.0 RELEASED (Slice 6 completo)
**Propósito de este HANDOFF:** documentar el estado del Slice 6 (Story Bible editable) y los TODOs pendientes.

---

## Estado actual (resumen)

- **Slice 6 completo:** Story Bible editable y tipado (Braindump, Genre tags, Style selector, Synopsis editable).
- **126 tests**, build + TS pasan, lint 0 errores.
- **Repo:** `gonzoblasco/kanam-story` (público), remote `origin`. `.knowledge/` solo en el workspace (doble-git).
- **Release:** v0.2.0 (commit `6aefc3e` + release `329a4c4`, tag `v0.2.0`).

---

## Qué se construyó en Slice 6 (Story Bible editable)

- **`Project.style` migrado** de `string` → `ProjectStyle` objeto (`{ mode: 'featured'|'custom'|'match', featured?, custom?, profile? }`). Migración de datos en DB v3→v4 (string → `{ mode:'custom', custom: <string> }`).
- **`genres: string[]`** — tags removibles en el proyecto.
- **`braindump: string`** — volcado libre de ideas (contexto de bajo peso).
- **`synopsis: string`** — override manual sobre la descripción.
- **`StoryBibleSettingsPanel`** (nuevo) — tab "Story Bible" en el panel derecho, patrón draft-and-commit del CompassPanel.
- **`buildAgentContext`** (chat) y **`buildContext`** (generación) inyectan genres/style/braindump/synopsis.
- **Helpers centralizados** en `lib/labels.ts`: `styleText` + `STYLE_PRESETS` (prosa tensa, lírica, minimalista, sensorial, literaria elevada).

### Archivos tocados (Slice 6)
- `types/index.ts` — `ProjectStyle`, `StyleProfile`, campos nuevos en `Project`.
- `lib/db.ts` — `DB_VERSION` 3→4 + migración de `style`.
- `lib/labels.ts` — `styleText`, `STYLE_PRESETS`.
- `lib/agentPrompts.ts`, `lib/prompts.ts` — inyección de los campos nuevos.
- `components/StoryBibleSettingsPanel.tsx` (nuevo), `components/RightPanel.tsx` (tab), `components/NewProjectModal.tsx` (style objeto).
- `lib/agentPrompts.test.ts`, `lib/prompts.test.ts` — tests nuevos.

## Decisiones de compatibilidad (Slice 6)

1. **`genre` (string) se mantiene** y se agrega `genres: string[]` como complemento — no rompe el modal ni los tests existentes.
2. **`style` se reemplaza** por el objeto `ProjectStyle` (target del data model) con migración del string existente.
3. **`synopsis` es nuevo** como override manual; `buildAgentContext`/`buildContext` usan `synopsis || description`.

## TODOs pendientes (post-release)

- Export PDF / DOCX (hoy solo MD/TXT).
- Tema claro (toggle).
- Tests de componentes (jsdom + Testing Library).
- Tests de `lib/db.ts` (fake-indexeddb).
- Búsqueda entre escenas.
- **Slice 7** (fichas de personaje ricas + generación asistida) — Release v0.3.0.

---

# Handoff a Agentes A y B — Fase 2 (Slices 7-10)

**Fecha:** 2026-08-13
**Autor:** Kanam (planificación y documentación)
**Estado:** v0.2.0 RELEASED. Fase 2 planificada en [ROADMAP.md](./ROADMAP.md), Slice 6 completo, pendientes 7-10.

## División de trabajo

- **Agente A (VS Code)** y **Agente B (ZCode)** implementan y se revisan entre sí (patrón de los slices 1-5).
- **Kanam** planifica y documenta. Este ROADMAP es el spec; los detalles de implementación los resuelven los agentes.
- Cada slice debe: implementar → testear → build+TS → lint → **actualizar STATUS.md** → commit atómico → release usable.

## Punto de partida (estado actual del código)

- **126 tests**, build + TS pasan, lint 0 errores 0 warnings, CI verde en GitHub Actions.
- **Data model:** `Project` (premise/promise/theme/protagonist/pov + **braindump/genres/style/synopsis**), `Chapter`, `Scene`, `Beat`, `Character` (role/age/appearance/personality/voice/wants/needs/backstory/goals/arc), `WorldEntity` (kind: place|lore|rule|object|other), `StoryBible` (auto-generada con overrides), `Conversation`/`Message`/`ContentAction`.
- **DB_VERSION:** 4 (Slice 7 la sube a 5).
- **Contexto del agente:** `buildAgentContext` en `lib/agentPrompts.ts`.
- **Prompts de generación:** `lib/prompts.ts` (Write/Rewrite/Describe/Expand/Dialogue/Tension).
- **Biblia:** `lib/bibleExtract.ts` + `lib/bibleParse.ts` (auto-generada, stale tracking).
- **Estilo:** `lib/labels.ts` (`styleText`, `STYLE_PRESETS`).

## Orden recomendado (dependencias)

1. **Slice 7** (fichas de personaje + generación) — extiende el Story Bible.
2. **Slice 8** (worldbuilding tipado) — mismo patrón que Slice 7.
3. **Slice 9** (Match My Style) — depende del Style del Slice 6.
4. **Slice 10** (filtros + vinculación) — independiente, puede ir en paralelo.

## Notas para los agentes

- **No romper el modelo de aceptación del chat** (propuesta → diff → aceptar/deshacer). Las nuevas features deben respetarlo.
- **Migraciones de DB** siempre con bump de `DB_VERSION` y mapeo de datos existentes (patrón de Slice 6: v3→v4).
- **El `.knowledge/` no se commitea al repo del proyecto** (doble-git). Los cambios de docs van al workspace.
- **Idioma:** UI y prompts en español; commits/PRs en inglés (regla de GitHub).
- **Al cerrar cada slice:** actualizar STATUS.md (marcar items), ROADMAP.md (checklist), y este HANDOFF si hay decisiones nuevas.

---

## Estado actual (resumen)

- **Slices 0-5 completos:** fundación, chat con manos, outline & beats, biblia viva, brújula narrativa, pulido (export + lint).
- **121 tests**, build + TS pasan, lint limpio (0 errores).
- **Repo:** `gonzoblasco/kanam-story` (público), remote `origin`. `.knowledge/` solo en el workspace (doble-git).
- **Release:** v0.1.0 (commit `133bc7d`).

---

## Review de Slice 4 (Agente A) — fixes aplicados

1. **🔴 `protagonist` huérfano al borrar personaje.** `deleteCharacter` no limpiaba `project.protagonist` → el agente veía un UUID crudo en su contexto. **Fix:** si el personaje borrado era el protagonista, se limpia la referencia.
2. **Etiquetas POV duplicadas en 3 lugares** (`BrújulaPanel`, `agentPrompts`, `NewProjectModal`). **Fix:** centralizadas en `lib/labels.ts`.
3. **Archivo con acento (`BrújulaPanel.tsx`)** — riesgo de build/CI. **Fix:** renombrado a `CompassPanel.tsx` (ASCII), tab `'compass'`.
4. **Selects de brújula commiteaban en blur** (inconsistente con el resto). **Fix:** ahora commitean en `onChange`.

---

## Qué se construyó en Slice 5 (Pulido)

- **Export MD/TXT:** `lib/export.ts` (`buildManuscriptMarkdown` + `downloadTextFile`) + `components/ExportMenu.tsx` (menú en la topbar). 4 tests.
- **Lint limpio:** corregidos todos los errores pre-existentes (unused imports, `any` en rutas API, comillas sin escapar, set-state-in-effect).
- **Release v0.1.0:** CHANGELOG + README actualizados, registro en PROYECTOS.md.

### Archivos tocados (Slice 5)
- `lib/export.ts` + `lib/export.test.ts` (nuevos).
- `components/ExportMenu.tsx` (nuevo).
- `app/page.tsx`, `app/globals.css` (menú export).
- `app/api/ollama/route.ts`, `app/api/ollama/models/route.ts` (tipos `any` → interfaces).
- `components/Editor.tsx`, `MarkdownView.tsx`, `NewProjectModal.tsx`, `ProjectTree.tsx`, `SettingsModal.tsx` (lint).
- `CHANGELOG.md`, `README.md` (release).

## Review de Slice 5 (Agente B) — fixes aplicados (post-release)

1. **`stripHtml` aplanaba los párrafos** — el manuscrito exportado perdía los saltos de párrafo (muro de texto). **Fix:** preserva límites de bloque (`</p>`, `</h1>`, `<br>`, listas).
2. **Export TXT en realidad era Markdown** — ahora `markdownToPlainText` despoja los marcadores para un `.txt` de verdad.
3. **Slug del filename perdía acentos** — ahora `normalize('NFD')` quita acentos antes del slug.
- Commit: `7bc30d3`. **123 tests**, build + TS pasan, lint 0 errores.

---

## TODOs pendientes (post-release)

- Export PDF / DOCX (hoy solo MD/TXT).
- Tema claro (toggle).
- Tests de componentes (jsdom + Testing Library).
- Tests de `lib/db.ts` (fake-indexeddb).
- Búsqueda entre escenas.

---

## Notas operativas

- **Errores `EMFILE: too many open files`** del watcher: son del sandbox (límite de archivos), no de la app. No bloquean, pero impiden el hot-reload — hay que reiniciar el server para aplicar cambios de código.
- **Para levantar:** `PORT=3100 npm run dev` (evita conflicto con otros servers en :3000).
- **Modelo default:** `deepseek-v4-flash` (si está disponible).

---

# Handoff a Agentes A y B — Fase 2 (Slices 6-10)

**Fecha:** 2026-08-13
**Autor:** Kanam (planificación y documentación)
**Estado:** v0.1.0 RELEASED. Fase 2 planificada en [ROADMAP.md](./ROADMAP.md), pendiente de implementar.

## División de trabajo

- **Agente A (VS Code)** y **Agente B (ZCode)** implementan y se revisan entre sí (patrón de los slices 1-5).
- **Kanam** planifica y documenta. Este ROADMAP es el spec; los detalles de implementación los resuelven los agentes.
- Cada slice debe: implementar → testear → build+TS → lint → **actualizar STATUS.md** → commit atómico → release usable.

## Punto de partida (estado actual del código)

- **123 tests**, build + TS pasan, lint 0 errores 0 warnings, CI verde en GitHub Actions.
- **Data model:** `Project` (premise/promise/theme/protagonist/pov), `Chapter`, `Scene`, `Beat`, `Character` (role/age/appearance/personality/voice/wants/needs/backstory/goals/arc), `WorldEntity` (kind: place|lore|rule|object|other), `StoryBible` (auto-generada con overrides), `Conversation`/`Message`/`ContentAction`.
- **DB_VERSION:** 3 (Slice 6 la sube a 4).
- **Contexto del agente:** `buildAgentContext` en `lib/agentPrompts.ts`.
- **Prompts de generación:** `lib/prompts.ts` (Write/Rewrite/Describe/Expand/Dialogue/Tension).
- **Biblia:** `lib/bibleExtract.ts` + `lib/bibleParse.ts` (auto-generada, stale tracking).

## Orden recomendado (dependencias)

1. **Slice 6** (Story Bible editable) — base; los slices 7-10 cuelgan de acá.
2. **Slice 7** (fichas de personaje + generación) — extiende el Story Bible.
3. **Slice 8** (worldbuilding tipado) — mismo patrón que Slice 7.
4. **Slice 9** (Match My Style) — depende del Style del Slice 6.
5. **Slice 10** (filtros + vinculación) — independiente, puede ir en paralelo.

## Notas para los agentes

- **No romper el modelo de aceptación del chat** (propuesta → diff → aceptar/deshacer). Las nuevas features deben respetarlo.
- **Migraciones de DB** siempre con bump de `DB_VERSION` y mapeo de datos existentes (patrón de Slice 0: v2→v3).
- **El `.knowledge/` no se commitea al repo del proyecto** (doble-git). Los cambios de docs van al workspace.
- **Idioma:** UI y prompts en español; commits/PRs en inglés (regla de GitHub).
- **Al cerrar cada slice:** actualizar STATUS.md (marcar items), ROADMAP.md (checklist), y este HANDOFF si hay decisiones nuevas.
