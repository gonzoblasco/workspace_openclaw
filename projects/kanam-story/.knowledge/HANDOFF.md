# HANDOFF — Kanam Story

**Fecha:** 2026-08-12
**Sesión:** Definición de producto (interview-me convergido + spec)
**Estado:** 🟢 Spec lista, Slice 0 pendiente

---

## Qué es

Co-writer de ficción local-first (BYOK → Ollama), en español, sin login, sin SaaS, valor del día 1. La **conversación** es el producto: un agente que conoce tu manuscrito + biblia + brújula, con quien debatís ideas/finales y que **aplica** los acuerdos al contenido.

## Por qué este proyecto (contexto)

Gonzo intentó clonar Sudowrite **3 veces** (`umbrawriter` v1, `sudolab`, `umbrawriter-v2`) y todas murieron en interfaz, no en tecnología. `sudolab` (archivado, `0.2.0-beta`) YA es funcional: editor TipTap + biblia + personajes + mundo + 38 tests. El `kanam-story` NO es un 4to clon de cero — es **reusar `sudolab`** y agregarle el chat con manos + outline/beats.

## El producto (5 pilares)

1. **Chat con Manos (corazón)** — agente que conoce la obra, conversás, y al acordar APLICA cambios (rewrite_scene, add_beat, update_character, append_scene...). Modelo aceptar/deshacer.
2. **Outline & Beats** — mapa de beats por capítulo/escena, a mano o sugerido por IA.
3. **Biblia Viva** — personajes (wants/needs/voice), mundo, reglas; se auto-actualiza.
4. **Brújula Narrativa** — premisa, promesa al lector, arco, tema.
5. **Editor Delgado** — escribe a mano, no es el protagonista.

## Decisiones tomadas

| Decisión | Valor |
|---|---|
| Nombre | **Kanam Story** (confirmado) |
| Base de código | `sudolab` (Next.js 16, TipTap 3, IndexedDB via idb, Ollama via rutas API) |
| Idioma | Español (UI y prompts) |
| Estrategia | Slices finos, cada uno = release usable. Anti-repetición. |
| MVP (Slice 1) | Chat con Manos, probado con `ultimo-turno` |
| Modelo de aceptación | El agente propone → diff/resumen → aceptar/deshacer |

## Archivos de referencia

- `projects/kanam-story/.knowledge/BRIEF.md`
- `projects/kanam-story/.knowledge/DATA_MODEL.md` (incluye Conversation/Message/ContentAction)
- `projects/kanam-story/.knowledge/ROADMAP.md` (slices 0-5)
- `projects/kanam-story/.knowledge/STATUS.md`
- `projects/sudolab/` — base de código reutilizable
- `projects/PROYECTOS.md` — indexado como activo

## Dónde dejamos / próximo paso

- **Slice 0 (siguiente):** copiar `sudolab` como base → crear stores de chat (`conversations`, `messages`, `contentActions`) → definir modelo `Beat` + CRUD.
- **Slice 1:** Chat con Manos (MVP con `ultimo-turno` como banco de pruebas).
- Luego: Outline & Beats → Biblia Viva → Brújula → Pulido.

## Criterio de éxito del proyecto

Abrís la app y en 10 segundos sabés qué capítulo sigue, qué prometiste contar y qué necesita cada personaje — y podés *debatirlo* con el agente, que lo aplica.
