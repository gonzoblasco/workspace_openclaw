# Slice 3 - IA co-autora de ramas (plan de implementación)

**T=15 (high)** | Pipeline: Kanam diseña → A escribe → B revisa → verificación

> **Estado: COMPLETO 2026-08-31 23:35.** Verificación: 34 tests verdes (incluye 5 tests de edge cases de review B), lint + typecheck + build OK, endpoint validado contra Ollama real (reply + 2 acciones). Fixes de review B aplicados (idempotencia, validación de existencia). Tag v0.3.0 + GitHub Release publicados.

## Objetivo

Chat con manos: el autor conversa con la IA sobre la historia y la IA puede **proponer acciones** (crear nodos, conectar edges, editar contenido) que el autor aprueba y se aplican al grafo. Proxy a Ollama, contexto = story completa + ruta actual.

## Arquitectura

```
AICoAuthor (panel chat) ──POST──> /api/chat (route handler)
                                      │
                                      ├─ construye prompt (story + ruta + historial)
                                      ├─ llama a Ollama /api/chat (streaming off, JSON mode)
                                      └─ parsea respuesta con Zod → { reply, actions }
AICoAuthor ──aplica acciones──> store (addNode / addStoryEdge / updateNode)
```

## Archivos nuevos

### 1. `src/lib/ai.ts` - tipos + schema Zod de la respuesta IA

```ts
// Acciones que la IA puede proponer (manos sobre el grafo)
aiActionSchema = z.discriminatedUnion('type', [
  createNode: { type, kind: 'passage'|'ending', title, content?, position? }
  createEdge: { type, source, target, label? }
  updateNode: { type, id, patch: { title?, content? } }
  updateEdge: { type, id, patch: { label? } }
])
aiResponseSchema = z.object({
  reply: z.string(),          // texto para el autor
  actions: z.array(aiActionSchema).default([]),
})
```

### 2. `src/app/api/chat/route.ts` - proxy a Ollama

- POST: `{ story: Story, currentNodeId: string | null, path: string[], message: string, history: { role, content }[] }`
- Construye el prompt del sistema: rol de co-autor, formato JSON estricto, contexto serializado (nodos con id/title/content, edges con source/target/label, variables con nombre/tipo/valor inicial, ruta actual).
- Llama a `OLLAMA_BASE_URL/api/chat` (default `http://localhost:11434`) con `OLLAMA_MODEL` (default `qwen3.5:9b-mlx`), `format: 'json'`, `stream: false`.
- Timeout 60s. Si Ollama no responde → 503 con mensaje claro ("¿Está Ollama corriendo?").
- Parseo con `aiResponseSchema`. Si falla → 502 con el texto crudo para debug.
- **Nunca** exponer la story completa al cliente en el error (solo mensaje).

### 3. `src/components/AICoAuthor.tsx` - panel de chat

- Props: `{ story, currentNodeId, path }`
- Estado local: mensajes `{ role: 'user'|'assistant', content, actions? }[]`, input, loading, error.
- Envía POST a `/api/chat` con historial (últimos 10 mensajes).
- Renderiza: historial (aria-live="polite" para respuestas), acciones propuestas como cards con botón "Aplicar" (una por acción) + "Aplicar todas", input con label visible, botón enviar (disabled mientras loading).
- Al aplicar: llama al store (`addNode`, `addStoryEdge`, `updateNode`, `updateEdge`), marca la acción como aplicada, feedback visual.
- a11y: focus management (input enfocado al abrir), botones con aria-label descriptivo, estados de loading con aria-busy.

### 4. `src/lib/ai.test.ts` - tests

- Parseo de respuesta válida (reply + acciones de los 4 tipos).
- Rechazo de acción inválida (type desconocido, patch con campos inválidos).
- Rechazo de respuesta sin reply.
- Acciones con campos opcionales ausentes (content vacío, label vacío).

## Archivos modificados

### 5. `src/components/StoryGraphEditor.tsx`

- Botón "IA" en la toolbar (modo edit) que abre/cierra el panel `AICoAuthor` (panel derecho, como VariablesPanel).
- Pasa `currentNodeId` (nodo seleccionado) y `path` (camino recorrido en modo play - si no hay, ruta vacía).
- El panel IA convive con node/variables: tercer panel `'ai'` en `activePanel`.

### 6. `src/lib/env.ts`

- `OLLAMA_BASE_URL: z.string().url().default('http://localhost:11434')`
- `OLLAMA_MODEL: z.string().min(1).default('qwen3.5:9b-mlx')`

### 7. `.env.example`

- Documentar `OLLAMA_BASE_URL` y `OLLAMA_MODEL`.

## Prompt del sistema (clave)

```
Sos Kanam, co-autora de ficción interactiva. El autor escribe una historia ramificada
como grafo: nodos = pasajes, edges = elecciones, variables = estado del mundo.

CONTEXTO (JSON):
{ story, currentNodeId, path, history }

Tu tarea: responder al autor con texto útil Y proponer acciones concretas sobre el
grafo cuando aporten valor (nueva rama, conexión, edición de contenido).

REGLAS:
- Respondé SIEMPRE en el idioma del autor (español por defecto).
- Las acciones deben referenciar IDs EXISTENTES del grafo (source/target/id).
- Para nodos nuevos, el id debe ser "nuevo-<slug>" (el server lo reemplaza por UUID).
- No inventes variables que no existen. Si necesitás una, proponela en el texto.
- JSON estricto: { "reply": string, "actions": [...] }.
- Si el autor pide algo fuera de alcance (export, jugar), respondé en texto sin acciones.
```

## Criterios de done

- [ ] Chat funcional: enviar mensaje → respuesta de Ollama → render en panel.
- [ ] Acciones propuestas se aplican al grafo (nodo nuevo aparece, edge conecta, contenido cambia).
- [ ] IDs nuevos (`nuevo-*`) se reemplazan por UUID reales al aplicar.
- [ ] Error de Ollama caído → mensaje claro, no crash.
- [ ] Tests del schema (parseo válido + rechazos) verdes.
- [ ] Lint + typecheck + build OK.
- [ ] Validado en browser real: chat + aplicar acción de crear nodo + persistir.
