# Hito 5 - IA propone el camino canónico (plan)

**T=16 (high)** | Pipeline: Kanam diseña → A escribe → B revisa → verificación

## Contexto (visión corregida 2026-09-01)

Kanam Studio es un taller de mundos: el grafo es el andamiaje, la biblia el corazón, el relato lineal la salida. El `deriveTimeline` (Slice 6) genera el camino por heurística (label más corto). Este hito agrega el **criterio narrativo**: la IA analiza el grafo + biblia + outline y propone cuál es el relato lineal óptimo - qué ramas incorporar, cuáles descartar, con justificación.

## Objetivo

1. **`/api/canonical`**: la IA recibe el grafo + biblia + outline + timeline actual y propone el camino canónico.
2. **Acciones**: `setCanonicalPath` (reemplaza el camino propuesto) - el autor aprueba y se usa como base del relato final.
3. **UI**: botón "Camino canónico" en el panel Exportar (junto al relato lineal) + vista de la propuesta con justificación.

## Arquitectura

```
src/lib/canonical.ts           - schema de request + tipos de la propuesta
src/app/api/canonical/route.ts - proxy a Ollama (streaming SSE, sin acciones de grafo)
src/components/ExportPanel.tsx  - EXTENDER: sección "Camino canónico" con botón + vista
```

### 1. Request (src/lib/canonical.ts)

```ts
canonicalRequestSchema = z.object({
  story: storySchema,          // grafo + biblia + outline
  timeline: z.array(z.object({  // el timeline actual (deriveTimeline)
    nodeId: z.string(),
    title: z.string(),
    kind: z.enum(['start', 'passage', 'ending']),
    via: z.string().optional(),
  })),
  message: z.string().min(1),
  history: z.array(chatMessageSchema).default([]),
})
```

### 2. Route (src/app/api/canonical/route.ts)

- POST: `{ story, timeline, message, history }`.
- Prompt de sistema:
  - **Rol:** co-directora narrativa. El autor tiene un grafo ramificado y quiere decidir el relato lineal final.
  - **Contexto:** grafo (nodos con contenido, edges con labels/condiciones/efectos), biblia (personajes, lugares, reglas, tramas), outline (actos/beats), timeline actual (camino por heurística).
  - **Tarea:** proponer el camino canónico: orden de sucesos, qué ramas incorporar (y por qué), cuáles descartar (y por qué), con justificación narrativa (tensión, arcos de personaje, ritmo).
  - **Formato:** texto plano + bloque de acciones al final:
    - `setCanonicalPath`: { type, path: [{ nodeId, note? }], rationale: string }
  - **MISMO estilo crítico:** si el grafo tiene problemas (finales inalcanzables, ramas que no aportan), decirlo.
- Streaming SSE idéntico a /api/chat. Timeout 180s (con el fix del AbortController completo).

### 3. ExportPanel - sección "Camino canónico"

- Botón "Proponer camino canónico" → llama a /api/canonical con el timeline actual.
- Vista de la propuesta: camino ordenado (títulos + notas por nodo) + rationale (justificación).
- Botón "Usar como relato lineal" → reemplaza la vista del relato lineal con el camino propuesto (estado local del panel).
- a11y: labels, foco, CSS Modules.

## Criterios de done

- [ ] `/api/canonical` con streaming SSE + setCanonicalPath parseado.
- [ ] ExportPanel: sección camino canónico (botón + vista + usar como relato).
- [ ] Tests: schema, parseo de la propuesta.
- [ ] Tests verdes, lint, typecheck, build OK.
- [ ] Validado contra Ollama real: la IA propone un camino con justificación.
