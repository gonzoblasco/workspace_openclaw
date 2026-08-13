# STATUS — Kanam Story

**Actualizado:** 2026-08-12

## Estado: 🟢 En definición (Slice 0 completado, Slice 1 siguiente)

- [x] Interview-me convergido (intención confirmada)
- [x] BRIEF
- [x] DATA_MODEL
- [x] ROADMAP (slices 0-5)
- [x] **Slice 0: Fundación sobre sudolab** (bootstrap temporal hacia chat-first)
  - [x] Copiado `sudolab` como base (editor + biblia + mundo + tests)
  - [x] Renombrado a Kanam Story (UI, prompts, DB_NAME `kanam-story`)
  - [x] Stores de chat: `conversations`, `messages`, `contentActions` (vía `Message.actions` inline)
  - [x] Modelo `Beat` + CRUD básico (store `beats` separado con chapterId/sceneId)
  - [x] DB_VERSION 2 → 3, cascade delete extendido
  - [x] Build + tests + TS pasan (59 tests)
- [ ] Slice 1: Chat con Manos (MVP con `ultimo-turno`)

## Decisiones clave

| Decisión | Opción |
|---|---|
| Base de código | `sudolab` (Next.js 16, TipTap 3, IndexedDB, Ollama) — **bootstrap, no destino** |
| El corazón | Chat con agente que **aplica** cambios (ContentAction) |
| Modelo de aceptación | Propuesta → diff/resumen → aceptar/deshacer |
| Estructura | Outline & Beats por capítulo/escena, manual o sugerido por IA |
| Idioma | Español (UI y prompts) |
| Slice fino primero | Sí, para no repetir el patrón de abandono |
| Beats | Store `beats` separado (con chapterId/sceneId), en vez de embederlos en Chapter/Scene |
| Repo | Local sin remote por ahora (doble-git: `.knowledge/` en workspace, código en repo propio) |

## Notas de Slice 0

- **Lint:** 8 errores pre-existentes heredados de sudolab (ProjectTree, SettingsModal, NewProjectModal), documentados en el README de origen. Se arreglan en Slice 5 (lint limpio), fuera de Slice 0.
- **Bootstrap:** se reusa lo funcional (storage, editor, biblia) y Kanam Story diverge hacia chat-first; el editor pasa a ser "delgado".

## Próximo paso

Slice 1: Chat con Manos — panel de chat persistido + buildContext del agente + streaming Ollama + herramientas (rewrite_scene, add_beat, etc.) + modelo aceptar/deshacer + tests. Probar con `ultimo-turno`.
