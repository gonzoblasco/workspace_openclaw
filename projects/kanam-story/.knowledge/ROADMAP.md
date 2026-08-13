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

- [ ] Panel de chat por proyecto, persistido en IndexedDB.
- [ ] Contexto del agente: manuscrito + biblia + outline actual (buildContext).
- [ ] Streaming de respuesta desde Ollama.
- [ ] **Herramientas del agente** (el "tiene manos"):
  - [ ] `rewrite_scene` — reescribe una escena bajo acuerdo.
  - [ ] `add_beat` / `update_beat` — arma/ajusta el outline.
  - [ ] `update_character` / `add_character`.
  - [ ] `append_scene`.
- [ ] **Modelo de aceptación:** el agente propone un cambio, el usuario ve diff/resumen, **acepta/deshace**. Nada se aplica sin OK.
- [ ] Tests de prompts + parseo de acciones de herramienta.

## Slice 2 — Outline & Beats

> La estructura: mapa de beats por capítulo/escena, a mano o sugerido por IA.

- [ ] Vista de outline (mapa de beats) por capítulo y escena.
- [ ] Edición manual de beats (reordenar, editar, marcar status).
- [ ] **"Sugerir outline"**: el agente propone beats desde biblia/brújula/lo escrito (tool `suggest_beats`).
- [ ] Conectar beats con la escritura (qué beat estoy escribiendo ahora).
- [ ] Discutir un beat con el chat y refinarlo.

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
