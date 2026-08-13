# HANDOFF — Kanam Story · Slice 4 (Brújula Narrativa)

**Fecha:** 2026-08-13
**Autor:** Agente B (review de Slice 3 + fixes + Slice 4)
**Estado:** 🟢 Slices 0-4 COMPLETOS. Próximo: Slice 5 (Pulido).
**Propósito de este HANDOFF:** que el **Agente A** (o quien siga) tome el proyecto desde el estado actual y continúe con el Slice 5.

---

## Estado actual (resumen para retomar)

- **Slice 0 (fundación):** base `sudolab` copiada y renombrada a Kanam Story; stores de chat + beats; DB_VERSION 3.
- **Slice 1 (Chat con Manos):** hecho por Agente A, revisado y corregido por Agente B.
- **Slice 2 (Outline & Beats):** hecho por Agente B, revisado y corregido por Agente A.
- **Slice 3 (Biblia Viva):** hecho por Agente A, **revisado y corregido por Agente B** (ver "Review de Slice 3" abajo).
- **Slice 4 (Brújula Narrativa):** hecho por Agente B (ver abajo). **117 tests, build+TS pasan.**
- **Repo:** `gonzoblasco/kanam-story` (público), remote `origin`. `.knowledge/` solo en el workspace (doble-git).

---

## Review de Slice 3 (Agente B) — fixes aplicados

1. **Gap (punto 2 del HANDOFF):** `rewrite_scene`/`append_scene` cambiaban el manuscrito pero NO marcaban `summary`/`themes`/`rules` stale. **Fix:** ahora `applyContentActions` marca esas secciones stale en ambos casos.
2. **Undo no revertía `staleAt` (punto 3):** al deshacer un `update_character`/`update_world`/`rewrite_scene`/`append_scene`, la sección quedaba stale. **Fix:** nuevo `clearBibleStale(keys)` en el store; el undo lo llama para limpiar `staleAt` de las secciones que la acción marcó.
3. **Lint:** el `useEffect` de reset de preview en `OutlineView` (agregado en el review de Slice 2) disparaba `set-state-in-effect` → disable de bloque.
- Puntos 1 y 4 del HANDOFF (regenerate preserva override + prompt claro): ✅ OK, sin cambios.

## Qué se construyó en Slice 4 (Brújula Narrativa)

- **Campos en `Project`:** `premise`, `promise`, `theme`, `protagonist` (opcionales; `pov` ya existía).
- **`components/BrújulaPanel.tsx`** (tab "Brújula" en el panel derecho): edita premise/promise/theme/protagonist (select de personajes)/pov, commit en blur.
- **Editor:** strip de promesa (`editor-compass`) visible al escribir.
- **`buildAgentContext`:** incluye la brújula (premisa/promesa/tema/protagonista) para que el agente la respete al debatir.
- **Tests:** +2 de brújula en `buildAgentContext` → 117 totales.

### Archivos tocados (Slice 4)
- `types/index.ts`, `lib/agentPrompts.ts` (+test), `components/BrújulaPanel.tsx` (nuevo), `components/RightPanel.tsx`, `components/Editor.tsx`, `app/globals.css`.

---

## Qué se construyó (Slice 3 — Biblia Viva)

- **Regeneración por sección:** `regenerateBibleSection(key)` + `buildBibleSectionPrompt` regeneran solo una sección (no todo), preservando overrides manuales.
- **Stale tracking:** campo `staleAt` por sección en `StoryBibleSection`; badge "desactualizada" en el panel cuando el manuscrito cambió.
- **Auto-marcado de stale:** cuando el agente cambia personajes/mundo vía chat (`update_character`/`add_character`/`update_world`), `applyContentActions` marca las secciones correspondientes como stale.
- **UI:** botón de regenerar por sección en cada sección del panel Biblia.

### Archivos tocados
- `lib/prompts.ts` — `buildBibleSectionPrompt` (nuevo).
- `lib/store.tsx` — `regenerateBibleSection`, `markBibleStale`, auto-marcado en `applyContentActions`.
- `components/StoryBiblePanel.tsx` — botón por sección + badge stale.
- `types/index.ts` — `staleAt` en `StoryBibleSection`.
- `lib/prompts.test.ts` — +3 tests de `buildBibleSectionPrompt`.

---

## Puntos que quiero que el Agente B revise con lupa

1. **`regenerateBibleSection` en `lib/store.tsx`** — ¿el prompt por sección es correcto? ¿Preserva el override manual (solo actualiza `auto`)? ¿El `staleAt: undefined` se limpia bien?
2. **`markBibleStale`** — ¿debería marcar también `summary`/`themes`/`rules` cuando cambia el manuscrito (no solo personajes/mundo)? Actualmente solo se marca al cambiar personajes/mundo vía chat.
3. **`applyContentActions`** — el auto-marcado de stale: ¿hay casos donde el undo no revierte el `staleAt`? (El undo revierte el contenido pero no el stale.)
4. **`buildBibleSectionPrompt`** — ¿el prompt es claro para que el modelo devuelva solo el contenido de la sección?

---

## Estado de verificación

- ✅ **117 tests** pasan (8 archivos).
- ✅ **Build** + TypeScript OK.
- ✅ Commits en `main`: `47c8ccf` (review Slice 3), `278af16` (Slice 4).

---

## Próximo paso (Slice 5 — Pulido)

> Release v0.1.0 usable.

- A11y (WCAG 2.1 AA) y validación AT manual.
- Export (MD / PDF / DOCX).
- Lint limpio + cobertura de tests de componentes.
- Release v0.1.0 y registro en PROYECTOS.md.

---

## Notas operativas

- **Errores `EMFILE: too many open files`** del watcher: son del sandbox (límite de archivos), no de la app. No bloquean, pero impiden el hot-reload — hay que reiniciar el server para aplicar cambios de código.
- **Para levantar:** `PORT=3100 npm run dev` (evita conflicto con otros servers en :3000).
- **Modelos probados:** `deepseek-v4-flash`, `glm-5.2`, `kimi-k2.7` (Ollama en la nube). El modelo default auto-detectado fue `qwen3.5:cloud`.
