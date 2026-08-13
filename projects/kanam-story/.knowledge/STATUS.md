# STATUS — Kanam Story

**Actualizado:** 2026-08-13

## Estado: 🟢 Slice 1 COMPLETO y probado con `ultimo-turno`

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
- [x] Build + tests + TS pasan (65 tests)
- [x] **Streaming Ollama (prep Slice 1):** `ollamaChatStream` (SSE) + parser `lib/ollamaStream.ts` testeado (6 tests) + ruta `/api/ollama` con `stream: true` vía ReadableStream
- [x] **Silenciado warning lockfile:** `turbopack.root` en `next.config.ts`
- [x] **Slice 1: Chat con Manos** (92 tests, build+TS pasan)
  - [x] `ChatPanel` (conversaciones + streaming + aceptar/descartar)
  - [x] `lib/agentReply.ts` — parseo de respuesta estructurada del agente
  - [x] `lib/agentPrompts.ts` — contexto completo + prompt JSON
  - [x] `lib/actions.ts` — aplicar/revertir ContentActions (puro)
  - [x] `applyContentActions` en store — persiste + devuelve undo
  - [x] **Undo conectado a la UI** + detalle por acción
- [x] **Prueba con `ultimo-turno`** (2026-08-13) — validado end-to-end
  - [x] Chat conversacional + streaming + rewrite_scene con sceneId real
  - [x] Aceptar aplica a IndexedDB; Deshacer revierte
  - [x] Bugs arreglados: IDs de escena en contexto, persistencia sin conversación activa, turbopack.root

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
| Repo | ✅ `gonzoblasco/kanam-story` (público) — creado 2026-08-12, remote `origin`, `.knowledge/` excluido (doble-git) |

## Notas de Slice 0

- **Lint:** 8 errores pre-existentes heredados de sudolab (ProjectTree, SettingsModal, NewProjectModal), documentados en el README de origen. Se arreglan en Slice 5 (lint limpio), fuera de Slice 0.
- **Bootstrap:** se reusa lo funcional (storage, editor, biblia) y Kanam Story diverge hacia chat-first; el editor pasa a ser "delgado".

## Próximo paso

Slice 1: Chat con Manos — panel de chat persistido + buildContext del agente + streaming Ollama + herramientas (rewrite_scene, add_beat, etc.) + modelo aceptar/deshacer + tests. Probar con `ultimo-turno`.
