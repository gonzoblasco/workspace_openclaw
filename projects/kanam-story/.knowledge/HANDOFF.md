# HANDOFF — Kanam Story · v0.1.0 (Release)

**Fecha:** 2026-08-13
**Autor:** Agente A (review de Slice 4 + fixes + Slice 5)
**Estado:** 🟢 v0.1.0 RELEASED (Slices 0-5 completos)
**Propósito de este HANDOFF:** documentar el estado final del release y los TODOs pendientes.

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
