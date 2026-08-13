# HANDOFF — Kanam Story · Slice 3 (Biblia Viva)

**Fecha:** 2026-08-13
**Autor:** Agente A (review de Slice 2 + fixes + Slice 3)
**Estado:** 🟢 Slices 0-3 COMPLETOS. Próximo: Slice 4 (Brújula Narrativa).
**Propósito de este HANDOFF:** que el **Agente B** (o quien siga) tome el proyecto desde el estado actual y continúe con el Slice 4.

---

## Estado actual (resumen para retomar)

- **Slice 0 (fundación):** base `sudolab` copiada y renombrada a Kanam Story; stores de chat + beats; DB_VERSION 3.
- **Slice 1 (Chat con Manos):** hecho por Agente A, revisado y corregido por Agente B.
- **Slice 2 (Outline & Beats):** hecho por Agente B, **revisado y corregido por Agente A** (ver "Review de Slice 2" abajo).
- **Slice 3 (Biblia Viva):** hecho por Agente A (ver abajo). **115 tests, build+TS pasan.**
- **Repo:** `gonzoblasco/kanam-story` (público), remote `origin`. `.knowledge/` solo en el workspace (doble-git).

---

## Review de Slice 2 (Agente A) — fixes aplicados

El Slice 2 de Agente B estaba bien estructurado, pero el review destapó baches que corregí:

1. **🔴 CRÍTICO — `add_beat` del chat creaba beats sin `chapterId`.** El `ContentAction.add_beat` pone `chapterId` a nivel de acción, pero `applyContentActions` hacía `createBeat(action.beat)` sin propagarlo. Resultado: beats aceptados vía chat quedaban sin `chapterId` y no aparecían en el outline. **Fix:** `createBeat({ ...action.beat, projectId, chapterId: action.chapterId ?? action.beat.chapterId })`.
2. **Código muerto:** `loadBeatsByChapter`/`loadBeatsByScene` (0 usos) → eliminadas del store.
3. **Beats huérfanos al borrar capítulo/escena:** `chaptersDB.delete` y `scenesDB.delete` no limpiaban beats → agregué cascade delete en `lib/db.ts`.
4. **Dedupe de beats sugeridos + reset del preview:** `acceptSuggested` ahora evita duplicados por título; el preview se resetea al cambiar de capítulo.
5. **Error silencioso en `suggestBeats`:** ahora muestra el mensaje de error real.

---

## Qué se construyó en Slice 3 (Biblia Viva)

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

- ✅ **115 tests** pasan (8 archivos).
- ✅ **Build** + TypeScript OK.
- ✅ Commits en `main`: `444a7db` (Slice 2), `19404c5` (Slice 3 + fixes review).

---

## Próximo paso (Slice 4 — Brújula Narrativa)

> Orientación: premisa, promesa, arco, tema. Visible al escribir y discutir.

- Campos de brújula en el proyecto (premise, promise, theme, protagonist, pov).
- Panel/insight que muestra la promesa mientras escribís y al debatir.
- El agente usa la brújula para no desviar la conversación del "qué prometiste contar".

---

## Notas operativas

- **Errores `EMFILE: too many open files`** del watcher: son del sandbox (límite de archivos), no de la app. No bloquean, pero impiden el hot-reload — hay que reiniciar el server para aplicar cambios de código.
- **Para levantar:** `PORT=3100 npm run dev` (evita conflicto con otros servers en :3000).
- **Modelos probados:** `deepseek-v4-flash`, `glm-5.2`, `kimi-k2.7` (Ollama en la nube). El modelo default auto-detectado fue `qwen3.5:cloud`.
