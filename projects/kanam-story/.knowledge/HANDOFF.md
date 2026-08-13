# HANDOFF — Kanam Story · Fase 2 (Slices 7-10)

**Fecha:** 2026-08-13
**Autor:** Agente B (Slice 7)
**Estado:** 🟢 Slice 7 COMPLETO. Próximo: **Slice 8** (Worldbuilding tipado fino).
**Propósito:** documentar el estado actual y dejar listo el Slice 8.

---

## Estado actual

- **Slices 0-7 completos:** fundación, chat con manos, outline & beats, biblia viva, brújula, pulido (v0.1.0), story bible editable (v0.2.0), fichas de personaje ricas + generación (Slice 7).
- **137 tests**, build + TS pasan, lint 0 errores, **CI verde** (GitHub Actions).
- **Repo:** `gonzoblasco/kanam-story` (público), remote `origin`. `.knowledge/` solo en el workspace (doble-git).
- **Releases:** v0.1.0 (`133bc7d`), v0.2.0 (`329a4c4`, tag `v0.2.0`). Slice 7 → v0.3.0 pendiente.

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

## Slice 8 — Worldbuilding tipado fino (→ v0.4.0) — SIGUIENTE

- [ ] Kinds finos (`place|organization|lore|key_event|clue|magic_system|item|rule|other`) + migración.
- [ ] Campos nuevos (`otherNames[]`, `traits[]`) + toggle `inContext`.
- [ ] Tests. Release v0.4.0.

## Slice 9 — Match My Style (→ v0.5.0)

- [ ] `buildStyleProfilePrompt` + parseo a `StyleProfile`; `style.mode: 'match'` + `style.profile`.
- [ ] Inyección del perfil en todos los prompts de generación.
- [ ] UI: 3er modo "Match My Style" (habilitar la opción hoy deshabilitada).
- [ ] Tests. Release v0.5.0.

## Slice 10 — Filtros de outline + vinculación (→ v0.6.0)

- [ ] Filtros por POV y tiempo verbal (`tense: 'past'|'present'|'future'`).
- [ ] Detección de escenas sin beats + sugerir vincular (link/connect).
- [ ] Tests. Release v0.6.0.

---

## Notas para los agentes

- **No romper el modelo de aceptación del chat** (propuesta → diff → aceptar/deshacer).
- **Migraciones de DB** siempre con bump de `DB_VERSION` y mapeo de datos existentes (patrón Slice 6: v3→v4).
- **`.knowledge/` no se commitea al repo del proyecto** (doble-git); los cambios de docs van al workspace.
- **Idioma:** UI y prompts en español; commits/PRs en inglés.
- **Al cerrar cada slice:** actualizar STATUS.md, ROADMAP.md y este HANDOFF.

## TODOs pendientes (post-release, no bloquean)

- Export PDF / DOCX (hoy solo MD/TXT).
- Tema claro (toggle).
- Tests de componentes (jsdom + Testing Library).
- Tests de `lib/db.ts` (fake-indexeddb).
- Búsqueda entre escenas.

## Notas operativas

- **Errores `EMFILE: too many open files`** del watcher: del sandbox (límite de archivos), no de la app. No bloquean, pero impiden hot-reload — reiniciar el server para aplicar cambios.
- **Para levantar:** `PORT=3100 npm run dev`.
- **Modelo default:** `deepseek-v4-flash` (si está disponible).
