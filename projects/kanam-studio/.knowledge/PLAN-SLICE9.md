# Slice 9 - Sección Admin local (plan)

**T=10 (low)** | Pipeline: A escribe → Kanam revisa

## Contexto

Gonzo quiere "todo registro creado accesible desde una sección de admin" para tener la app completa en la base de datos. La respuesta local-first: una vista Admin que liste TODAS las historias con stats calculadas (reusa `checkCanon` y `simulateRoutes`), más export masivo a JSON versionable (git como base de datos central). El Portal de OpenClaw expone esto en el Control UI (hito 2, aparte).

## Objetivo

1. **Vista Admin** en la home: tabla de todas las historias con stats por fila.
2. **Stats por historia** (lógica pura, testeable): nodos, edges, variables, personajes de la biblia, cobertura de rutas (simulateRoutes), issues de canon (checkCanon).
3. **Export masivo**: descargar TODAS las historias como un JSON (objeto `{ [storyId]: story }` o array) - versionable para git.

## Arquitectura

```
src/lib/stats.ts              - stats por historia (lógica pura)
src/lib/stats.test.ts         - tests
src/components/AdminPanel.tsx  - vista admin (tabla + export masivo), CSS Modules, a11y
src/app/page.tsx              - botón "Admin" en la home (junto al toggle de tema)
```

### 1. Stats (src/lib/stats.ts)

```ts
interface StoryStats {
  storyId: string
  title: string
  updatedAt: string
  nodeCount: number
  edgeCount: number
  variableCount: number
  characterCount: number      // entidades kind character de la biblia
  worldEntityCount: number    // total de entidades de la biblia
  routeCount: number          // simulateRoutes: coverage.routeCount
  endingCount: number         // simulateRoutes: coverage.endingCount
  deadEndCount: number
  loopCount: number
  canonErrors: number         // checkCanon: summary.errors
  canonWarnings: number
  canonInfos: number
}

function computeStoryStats(story: Story): StoryStats
```

- Reusa `checkCanon` (canon.ts) y `simulateRoutes` (simulate.ts) - ya existen.
- Lógica pura, sin UI.

### 2. AdminPanel (src/components/AdminPanel.tsx)

- Tabla de historias (de `useKanamStudio().stories`): título, actualizada, nodos, edges, personajes, rutas, endings, errores canon.
- Orden: por `updatedAt` desc (más reciente primero).
- Fila clickeable → abre la historia (openStory).
- **Export masivo:** botón "Exportar todo (JSON)" → Blob con `{ exportedAt, stories: [...] }` → download `kanam-studio-export.json`.
- a11y: tabla con `<th scope>`, caption, botones con label, CSS Modules (regla v0.6.0).

### 3. Integración (src/app/page.tsx)

- Botón "Admin" en la home (junto al ThemeToggle) que alterna la vista admin / lista normal.
- La vista admin reemplaza la lista de historias cuando está activa.

## Criterios de done

- [ ] `computeStoryStats` con tests (historia vacía, con grafo, con biblia, con rutas, con issues canon).
- [ ] AdminPanel: tabla con stats + export masivo, CSS Modules, a11y.
- [ ] Botón Admin en la home.
- [ ] Tests verdes, lint, typecheck, build OK.
- [ ] E2E: abrir Admin, ver stats de una historia, exportar todo.
