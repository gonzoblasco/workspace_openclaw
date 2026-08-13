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

- [ ] Regeneración de biblia desde manuscrito (ya existe en sudolab) + desde cambios del chat.
- [ ] Actualización automática de personajes/mundo cuando el agente los cambia.
- [ ] Overrides manuales por sección preservados.

## Slice 4 — Brújula Narrativa

> Orientación: premisa, promesa, arco, tema. Visible al escribir y discutir.

- [ ] Campos de brújula en el proyecto (premise, promise, theme, protagonist, pov).
- [ ] Panel/insight que muestra la promesa mientras escribís y al debatir.
- [ ] El agente usa la brújula para no desviar la conversación del "qué prometiste contar".

## Slice 5 — Pulido

- [ ] A11y (WCAG 2.1 AA) y validación AT manual.
- [ ] Export (MD / PDF / DOCX).
- [ ] Lint limpio + cobertura de tests de componentes.
- [ ] Release v0.1.0 y registro en PROYECTOS.md.

---

## Notas de trazabilidad

- Slice 1 es el MVP que se prueba con `ultimo-turno` hoy. Si Slice 1 no engancha, no seguimos — aprendemos y ajustamos antes de invertir más.
- Cada slice = commit atómico + release usable. Sin acumular discovery muerto.
