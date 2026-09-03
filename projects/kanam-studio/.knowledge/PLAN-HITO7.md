# Hito 7 - Prosa final (plan)

**T=13 (medium)** | Pipeline: A escribe → B cross-review → Kanam aprueba

## Contexto (visión corregida 2026-09-01)

Kanam Studio es un taller de mundos: el grafo es el andamiaje, la biblia el corazón, el camino canónico la decisión, y **la prosa final la salida**. Este hito cierra el círculo: la IA escribe el relato lineal completo en prosa narrativa, con voz consistente, desde el camino canónico + biblia + outline.

## Objetivo

1. **`/api/prose`**: la IA escribe el relato en prosa narrativa desde el camino canónico (o el timeline si no hay propuesta canónica).
2. **Voz narrativa**: consistente (persona, tiempo, tono) - configurable por el autor (opcional, default tercera persona pasado).
3. **Exportable**: el resultado se descarga como Markdown.
4. **UI**: sección "Prosa final" en el panel Exportar.

## Arquitectura

```
src/lib/prose.ts                - schema de request + tipos
src/app/api/prose/route.ts      - proxy a Ollama (streaming SSE, sin acciones)
src/components/ExportPanel.tsx  - EXTENDER: sección "Prosa final"
```

### 1. Request (src/lib/prose.ts)

```ts
proseRequestSchema = z.object({
  story: storySchema,           // grafo + biblia + outline
  path: z.array(z.object({      // camino canónico (o timeline derivado)
    nodeId: z.string(),
    title: z.string(),
    content: z.string().optional(),
    via: z.string().optional(),
    note: z.string().optional(),
  })).min(1),
  voice: z.object({             // voz narrativa (defaults)
    person: z.enum(['first', 'third']).default('third'),
    tense: z.enum(['past', 'present']).default('past'),
    tone: z.string().default('neutral'),  // descripción libre del tono
  }).default({}),
  message: z.string().min(1),
  history: z.array(chatMessageSchema).default([]),
})
```

### 2. Route (src/app/api/prose/route.ts)

- POST: `{ story, path, voice, message, history }`.
- Prompt de sistema:
  - **Rol:** escritora. El autor tiene el camino canónico (orden de sucesos) + la biblia (personajes, lugares, reglas) + el outline (actos/beats) y quiere la versión final en prosa.
  - **Tarea:** escribir el relato completo siguiendo el camino, en prosa narrativa fluida (no lista de nodos). Integrar los contenidos de los nodos, las notas del camino, la voz de los personajes de la biblia, la coherencia del mundo.
  - **Voz:** persona/tiempo/tono del request.
  - **Reglas:** no inventar sucesos fuera del camino; no contradecir la biblia; prosa continua (párrafos, no bullets); el idioma del autor (español por defecto).
  - **MISMO estilo crítico:** si el camino tiene problemas (huecos, saltos bruscos), señalarlo en el texto final o en un preámbulo breve.
- Streaming SSE idéntico a /api/chat (delta/done/error). Sin acciones (solo texto). Timeout 180s con AbortController completo.

### 3. ExportPanel - sección "Prosa final"

- Selector de voz: persona (1ra/3ra), tiempo (pasado/presente), tono (input libre).
- Botón "Escribir prosa final" → llama a /api/prose con el camino canónico (o timeline si no hay propuesta).
- Vista del texto con streaming (markdown renderizado).
- Botón "Descargar .md" → Blob con el texto.
- a11y: labels, foco, CSS Modules.

## Criterios de done

- [ ] `/api/prose` con streaming SSE + voz configurable.
- [ ] ExportPanel: sección prosa final (voz + escribir + vista + descargar .md).
- [ ] Tests: schema, parseo.
- [ ] Tests verdes, lint, typecheck, build OK.
- [ ] Validado contra Ollama real: la IA escribe prosa narrativa coherente con el camino y la biblia.
