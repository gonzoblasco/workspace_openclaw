# Slice 5 - World-building con IA (plan de implementación)

**T=16 (high)** | Pipeline: Kanam diseña → A escribe → B revisa → verificación

## Contexto (visión corregida 2026-09-01)

Kanam Studio es un **taller de construcción de mundos y planificación narrativa**, no un juego de aventura. El grafo es el andamiaje interno; la **biblia del mundo** (personajes, lugares, reglas, tramas) es el corazón. Este slice construye esa biblia con IA asistida y consistencia cruzada con el grafo.

## Objetivo

1. **Modelo de datos de la biblia** (`world`): entidades tipadas (character, location, rule, plotline) con nombre, descripción, tags y relaciones.
2. **Persistencia**: la biblia viaja con la story (documento denormalizado, mismo patrón que el grafo).
3. **Chat de world-building**: el autor conversa con la IA para definir el mundo; la IA propone entidades/ediciones y detecta inconsistencias. Reusa el streaming SSE.
4. **Consistencia cruzada**: el canon checker valida que las entidades mencionadas en el grafo existan en la biblia (y viceversa).
5. **UI**: panel "Mundo" con la biblia (lista por tipo, CRUD) + chat dedicado.

## Arquitectura

```
src/lib/world.ts              - modelo Zod de la biblia + helpers
src/lib/world.test.ts         - tests del modelo
src/lib/canon.ts              - EXTENDER: checks de consistencia cruzada
src/app/api/world/route.ts    - proxy a Ollama (chat world-building, streaming SSE)
src/components/WorldPanel.tsx  - panel: biblia (CRUD) + chat
StoryGraphEditor.tsx           - 5to panel 'world'
```

### 1. Modelo (src/lib/world.ts)

```ts
worldEntityKindSchema = z.enum(['character', 'location', 'rule', 'plotline'])
worldEntitySchema = z.object({
  id: z.string().min(1),
  kind: worldEntityKindSchema,
  name: z.string().min(1),
  description: z.string().default(''),
  tags: z.array(z.string()).default([]),
  relations: z.array(z.object({
    targetId: z.string().min(1),
    label: z.string().default(''),
  })).default([]),
})
worldSchema = z.object({
  entities: z.array(worldEntitySchema).default([]),
})
// La story se extiende: storySchema + world (opcional, default vacío)
```

- `createWorldEntity(kind, name)` helper.
- La story gana `world: worldSchema` (default `{ entities: [] }`). Migración: `storySchema` con `.default()` para no romper historias existentes.

### 2. Canon checker - consistencia cruzada (src/lib/canon.ts)

Nuevos checks:
- **`missing-world-entity`** (warning): una entidad mencionada en el grafo (nodo/edge cuyo texto contiene el nombre de una entidad de la biblia... NO - mejor: el autor referencia entidades por nombre en el contenido de nodos; el check busca nombres de entidades de la biblia en el contenido de nodos y edges, y reporta si una entidad de la biblia NO se menciona en ningún nodo = entidad sin uso en la historia).
- **`unused-world-entity`** (info): entidad de la biblia que no aparece en ningún nodo/edge.
- **`world-entity-conflict`** (warning): dos entidades con el mismo nombre (duplicadas).

Simple y accionable: el canon checker ya tiene la infraestructura (issues con severidad, orden, summary).

### 3. Chat de world-building (src/app/api/world/route.ts)

- POST: `{ story, message, history }` (contexto = biblia completa + grafo resumido).
- Prompt: co-constructora de mundos, MISMO estilo crítico que el chat de IA (no servicial, señala problemas con justificación).
- Acciones propuestas (bloque JSON al final, mismo patrón <<<ACCIONES/>>>FIN):
  - `createEntity`: { type, kind, name, description?, tags? }
  - `updateEntity`: { type, id, patch: { name?, description?, tags? } }
  - `deleteEntity`: { type, id }
- Streaming SSE idéntico al chat de IA (delta/done/error).
- Reusa `extractActionsBlock`/`stripActionsBlock` de ai.ts (exportar los schemas de acciones world desde world.ts).

### 4. Panel Mundo (src/components/WorldPanel.tsx)

- Lista de entidades agrupadas por tipo (Personajes, Lugares, Reglas, Tramas).
- CRUD: crear (form con kind+name), editar (descripción, tags), borrar.
- Chat integrado (reusa el patrón de AICoAuthor pero con /api/world).
- a11y: labels visibles, aria-live, foco.
- CSS Modules (regla v0.6.0).

### 5. Integración

- `StoryGraphEditor`: 5to panel `'world'` con botón "Mundo".
- `store.ts`: `updateWorld` (updater sobre story.world) + acciones del chat aplican al store con validación.

## Criterios de done

- [ ] Modelo world con Zod + tests (crear entidad, validar kinds, story con world default).
- [ ] Canon checker: 3 checks nuevos (unused-world-entity, world-entity-conflict, + mención en grafo) con tests.
- [ ] /api/world con streaming SSE + acciones (createEntity/updateEntity/deleteEntity) parseadas.
- [ ] WorldPanel: CRUD + chat, CSS Modules, a11y.
- [ ] Tests verdes, lint, typecheck, build OK.
- [ ] E2E: crear entidad desde el panel, verla en la lista, chat responde.
- [ ] Validado contra Ollama real (deepseek-v4-flash:cloud).
