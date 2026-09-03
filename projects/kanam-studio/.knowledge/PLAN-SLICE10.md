# Slice 10 - Outline y Roadmap de cada historia (plan)

**T=13 (medium)** | Pipeline: A escribe → B cross-review → Kanam aprueba

## Contexto (visión corregida 2026-09-01)

Kanam Studio es un taller de mundos: el grafo es el andamiaje, la biblia el corazón, el relato lineal la salida. El **outline** es la estructura narrativa de la historia (actos, beats, arcos) y el **roadmap** es el plan de desarrollo (qué falta construir). Ambos viven POR historia y se vinculan al grafo.

## Objetivo

1. **Outline** (`story.outline`): estructura narrativa - actos con beats, cada beat vinculado a nodos del grafo (opcional). La IA puede proponer el outline desde el grafo + biblia.
2. **Roadmap** (`story.roadmap`): plan de desarrollo - items con estado (pendiente/en progreso/hecho), generable desde el canon checker (que ya sabe qué falta: nodos huérfanos, finales inalcanzables, personajes sin uso).
3. **UI**: panel "Outline" con ambas vistas + chat de IA para proponer/refinar.

## Arquitectura

```
src/lib/outline.ts            - modelo Zod (outline + roadmap) + helpers
src/lib/outline.test.ts       - tests
src/app/api/outline/route.ts  - proxy a Ollama (proponer outline, streaming SSE)
src/components/OutlinePanel.tsx - panel: outline + roadmap + chat, CSS Modules, a11y
StoryGraphEditor.tsx           - 8vo panel 'outline'
```

### 1. Modelo (src/lib/outline.ts)

```ts
outlineBeatSchema = z.object({
  id: z.string().min(1),
  title: z.string().min(1),
  description: z.string().default(''),
  nodeIds: z.array(z.string()).default([]),   // nodos del grafo vinculados
})
outlineActSchema = z.object({
  id: z.string().min(1),
  title: z.string().min(1),
  beats: z.array(outlineBeatSchema).default([]),
})
outlineSchema = z.object({ acts: z.array(outlineActSchema).default([]) })

roadmapItemSchema = z.object({
  id: z.string().min(1),
  title: z.string().min(1),
  status: z.enum(['pending', 'in-progress', 'done']).default('pending'),
  source: z.enum(['manual', 'canon', 'ai']).default('manual'),
})
roadmapSchema = z.object({ items: z.array(roadmapItemSchema).default([]) })
```

- La story gana `outline` y `roadmap` (defaults vacíos, migración implícita).
- `createOutlineAct`, `createOutlineBeat`, `createRoadmapItem` helpers.

### 2. Roadmap desde canon (lógica pura)

```ts
function roadmapFromCanon(story: Story): RoadmapItem[]
```

- Reusa `checkCanon`: cada issue de severidad error/warning genera un item de roadmap:
  - `no-start` → "Agregar nodo de inicio"
  - `dangling-edge` → "Conectar elección a un nodo existente"
  - `orphan-node` → "Conectar el nodo X a la historia"
  - `unreachable-ending` → "Hacer alcanzable el final X"
  - `missing-world-entity` → "Usar la entidad X en la historia"
- Items con `source: 'canon'`, status `pending`.
- Se regenera al abrir el panel (no se persiste - es derivado del canon).

### 3. Chat de outline (src/app/api/outline/route.ts)

- POST: `{ story, message, history }` (contexto = grafo + biblia + outline actual).
- Prompt: co-estructuradora narrativa, MISMO estilo crítico. Propone actos/beats vinculados a nodos reales.
- Acciones (bloque JSON, mismo patrón):
  - `setOutline`: { type, acts: [{ title, beats: [{ title, description?, nodeIds? }] }] } (reemplaza el outline)
  - `addAct`: { type, title }
  - `addBeat`: { type, actId, title, description?, nodeIds? }
  - `updateBeat`: { type, id, patch: { title?, description?, nodeIds? } }
- Streaming SSE idéntico a /api/chat.

### 4. Panel Outline (src/components/OutlinePanel.tsx)

- **Outline:** actos con beats (colapsable), cada beat muestra los nodos vinculados (click navega al nodo).
- **Roadmap:** items con status (checkbox/select), filtro por source (canon/manual/ai).
- **Chat:** proponer/refinar outline con la IA.
- a11y: labels, foco, CSS Modules.

## Criterios de done

- [ ] Modelo outline + roadmap con Zod + tests.
- [ ] `roadmapFromCanon` con tests (cada issue → item).
- [ ] /api/outline con streaming SSE + acciones.
- [ ] OutlinePanel: outline + roadmap + chat, CSS Modules, a11y.
- [ ] Tests verdes, lint, typecheck, build OK.
- [ ] E2E: abrir panel Outline, ver roadmap generado del canon, chat responde.
