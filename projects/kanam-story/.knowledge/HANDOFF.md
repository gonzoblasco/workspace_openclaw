# HANDOFF — Kanam Story · Slice 1 (Chat con Manos)

**Fecha:** 2026-08-13
**Autor:** Agente A (implementación del Slice 1)
**Estado:** 🟢 Slice 1 COMPLETO y probado con `ultimo-turno`
**Propósito de este HANDOFF:** que el **Agente B** revise el trabajo del Agente A (Slice 1) con intención crítica.

---

## Qué se construyó (Slice 1 — el corazón del producto)

El objetivo del Slice 1 era el **Chat con Manos**: un agente con quien conversás sobre la obra, que conoce el manuscrito + biblia + outline, y que **aplica** cambios al contenido cuando los aceptás. Nada se aplica sin tu OK.

### Archivos nuevos
| Archivo | Rol |
|---|---|
| `lib/agentReply.ts` | Parsea la respuesta JSON estructurada del agente (`reply` + `actions`) y valida acciones. |
| `lib/agentPrompts.ts` | `buildAgentContext` (contexto completo: proyecto, personajes, mundo, manuscrito, beats, biblia) + `buildAgentPrompt` (instruye JSON estructurado). |
| `lib/actions.ts` | Aplicar/revertir `ContentAction`s de forma pura sobre un `StoryState` inmutable. |
| `components/ChatPanel.tsx` | Panel de chat: conversaciones, streaming, aceptar/descartar, deshacer. |
| Tests | `agentReply.test.ts`, `agentPrompts.test.ts`, `actions.test.ts` (27 tests nuevos). |

### Archivos modificados
- `lib/store.tsx` — `applyContentActions` (persiste + devuelve undo), `createMessage`/`selectConversation`/etc.
- `components/RightPanel.tsx` — pestaña "Co-writer" como tab principal.
- `app/globals.css` — estilos del chat.
- `lib/ollama.ts` + `app/api/ollama/route.ts` + `lib/ollamaStream.ts` — streaming SSE (de la sesión previa).
- `next.config.ts` — `turbopack.root` (ver nota abajo).

---

## Cómo funciona el flujo (validado end-to-end)

```
usuario escribe → buildAgentContext (manuscrito+biblia+outline) → buildAgentPrompt (JSON)
→ ollamaChatStream (SSE) → parseAgentReply → muestra reply + propone actions
→ usuario Acepta → applyContentActions (persiste a IndexedDB) → botón Deshacer (revierte)
```

**Validado con `ultimo-turno` (2026-08-13):**
- El agente conoció el contexto (sinopsis, género, tono, manuscrito de la escena "El bolso").
- Propuso `rewrite_scene` con el `sceneId` real.
- **Aceptar** aplicó el cambio a IndexedDB (el cierre cambió: latido antes de la sangre).
- **Deshacer** revirtió al contenido original.

---

## Bugs que la prueba destapó y arreglé

1. **`buildAgentContext` no incluía los IDs de escenas** → el agente no podía devolver `sceneId` reales, así que `rewrite_scene` nunca aplicaba (mostraba "Cambios aplicados" pero no cambiaba nada). **Fix:** agregué `(id: <id>)` al contexto del manuscrito.
2. **Tras reload, la conversación no quedaba seleccionada** → los mensajes no se persistían. **Fix:** `send()` ahora crea/selecciona la conversación si no hay una activa.
3. **`turbopack.root` mal configurado** → Next.js infería el root del workspace (por el `package-lock.json` raíz) y las rutas API daban 404. **Fix:** `turbopack.root: __dirname` (esto también silencia el warning de lockfile).

---

## Puntos que quiero que el Agente B revise con lupa

1. **`applyContentActions` en `lib/store.tsx`** — captura valores previos y devuelve undo. ¿El undo es correcto para todos los tipos de acción? ¿Hay casos donde el `before`/`after` no se capture bien (ej. `update_bible` con sección inexistente)?
2. **`lib/actions.ts`** — el módulo puro de aplicar/revertir. ¿Cubre todos los `ContentAction`? ¿El `append_scene` genera un `id` con `crypto.randomUUID()` correctamente?
3. **`parseAgentReply` en `lib/agentReply.ts`** — ¿el parseo del JSON (primer `{` al último `}`) es robusto? ¿Qué pasa si el modelo devuelve JSON anidado o prosa con llaves?
4. **`ChatPanel.tsx`** — el manejo de `busy`, abort, y el historial (últimos 10 mensajes). ¿Hay race conditions si el usuario cambia de conversación mientras el agente responde?
5. **`buildAgentPrompt`** — ¿el prompt es lo suficientemente claro para que el modelo devuelva JSON válido de forma consistente? ¿Debería incluir ejemplos de acciones?

---

## Estado de verificación

- ✅ **92 tests** pasan (7 archivos).
- ✅ **Build** + TypeScript OK.
- ✅ **Prueba end-to-end** con `ultimo-turno` (chat, streaming, rewrite, aceptar, deshacer).
- ✅ Commits en `main`: `fd7ff84` (Slice 1), `9e6a6c2` (undo+detalle), `86a54e6` (fixes de la prueba).

---

## Próximo paso (Slice 2 — Outline & Beats)

> La estructura: mapa de beats por capítulo/escena, a mano o sugerido por IA.

- Vista de outline (mapa de beats) por capítulo y escena.
- Edición manual de beats (reordenar, editar, marcar status).
- **"Sugerir outline"**: el agente propone beats desde biblia/brújula/lo escrito (tool `suggest_beats`).
- Conectar beats con la escritura (qué beat estoy escribiendo ahora).
- Discutir un beat con el chat y refinarlo.

---

## Notas operativas

- **Errores `EMFILE: too many open files`** del watcher: son del sandbox (límite de archivos), no de la app. No bloquean, pero impiden el hot-reload — hay que reiniciar el server para aplicar cambios de código.
- **Para levantar:** `PORT=3100 npm run dev` (evita conflicto con otros servers en :3000).
- **Modelos probados:** `deepseek-v4-flash`, `glm-5.2`, `kimi-k2.7` (Ollama en la nube). El modelo default auto-detectado fue `qwen3.5:cloud`.

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

- **Slice 0 (HECHO):** base `sudolab` copiada y renombrada a Kanam Story; stores de chat (`conversations`, `messages`, `contentActions` vía `Message.actions`) + store `beats` con CRUD; DB_VERSION 2→3; cascade delete; build+tests+TS pasan (59 tests). Commit `feat: scaffold Kanam Story foundation from sudolab` en repo local (sin remote).
- **Slice 1 (siguiente):** Chat con Manos (MVP con `ultimo-turno` como banco de pruebas) — panel de chat persistido, buildContext del agente, streaming Ollama, herramientas (rewrite_scene, add_beat, update_character, append_scene...), modelo aceptar/deshacer, tests de prompts + parseo.
- Luego: Outline & Beats → Biblia Viva → Brújula → Pulido.

## Notas operativas

- **Bootstrap, no destino:** sudolab es la base funcional (editor + biblia + mundo); Kanam Story diverge hacia chat-first, el editor pasa a ser "delgado".
- **Lint:** 8 errores pre-existentes heredados de sudolab (ProjectTree, SettingsModal, NewProjectModal) → se arreglan en Slice 5.
- **Streaming:** hoy `/api/ollama` usa `stream:false`. Para Slice 1 hay que cambiar la ruta + `ollamaChat` (exponer AsyncIterable o SSE).

## Criterio de éxito del proyecto

Abrís la app y en 10 segundos sabés qué capítulo sigue, qué prometiste contar y qué necesita cada personaje — y podés *debatirlo* con el agente, que lo aplica.
