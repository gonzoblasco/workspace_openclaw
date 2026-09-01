# Slice 7 - Simulación de rutas (plan de implementación)

**T=15 (high)** | Pipeline: Kanam diseña → A escribe → B revisa → verificación

## Contexto (visión corregida 2026-09-01)

Kanam Studio es un taller de mundos: el grafo es el andamiaje, la biblia el corazón, el relato lineal la salida. La **simulación de rutas** es la herramienta de exploración definitiva: recorre todas las rutas posibles del grafo (con condiciones y efectos) para que el autor entienda las posibilidades narrativas antes de decidir el camino canónico.

## Objetivo

1. **Simulador de rutas** (`src/lib/simulate.ts`): dado el grafo, explorar todas las rutas desde el start hasta los endings, evaluando condiciones y aplicando efectos (reusa el engine del Slice 2).
2. **Cobertura**: qué nodos/edges se alcanzan, qué endings son alcanzables, cuántas rutas distintas existen.
3. **Detección de problemas**: rutas que se cortan (dead-ends), bucles infinitos (ciclos sin progreso de estado).
4. **UI**: panel "Simular" con resumen de cobertura + lista de rutas.

## Arquitectura

```
src/lib/simulate.ts          - simulador (lógica pura, reusa engine.ts)
src/lib/simulate.test.ts     - tests
src/components/SimulatePanel.tsx - panel: cobertura + rutas, CSS Modules, a11y
StoryGraphEditor.tsx           - 7mo panel 'simulate'
```

### 1. Simulador (src/lib/simulate.ts)

Reusa `getInitialState`, `getAvailableChoices`, `takeEdge` de engine.ts.

```ts
interface SimulatedRoute {
  /** Nodos recorridos (ids, en orden). */
  path: string[]
  /** Labels de los edges tomados (para mostrar la ruta legible). */
  via: string[]
  /** Estado final del mundo al terminar la ruta. */
  finalState: GameState
  /** Cómo terminó: 'ending' | 'dead-end' | 'loop' | 'max-depth' */
  endKind: 'ending' | 'dead-end' | 'loop' | 'max-depth'
  /** Nodo donde terminó. */
  endNodeId: string
}

interface SimulationResult {
  routes: SimulatedRoute[]
  coverage: {
    reachableNodes: string[]      // ids de nodos alcanzados
    reachableEndings: string[]    // ids de endings alcanzables
    unreachableNodes: string[]    // nodos nunca visitados
    routeCount: number
    endingCount: number           // rutas que llegan a un ending
    deadEndCount: number
    loopCount: number
  }
}

function simulateRoutes(story: Story, options?: { maxDepth?: number; maxRoutes?: number }): SimulationResult
```

**Algoritmo:**
- DFS desde el start con estado del mundo (GameState).
- En cada nodo: `getAvailableChoices` (condiciones evaluadas con el estado actual).
- Por cada choice: aplicar efectos (`takeEdge`), recursión.
- **Ciclos:** si el nodo ya está en el camino actual Y el estado no cambió respecto a la visita anterior → loop (cortar). Si el estado cambió (ej. un contador que baja), seguir (progreso).
- **Límites:** `maxDepth` (default 50) y `maxRoutes` (default 200) para grafos grandes - el resultado incluye `truncated: true` si se cortó por límite.
- **Determinismo:** orden estable de exploración (edges ordenados por id).

### 2. Panel Simular (src/components/SimulatePanel.tsx)

- Resumen: "X rutas · Y llegan a un final · Z se cortan · W bucles".
- Cobertura: nodos alcanzables vs no alcanzables (con click para navegar al nodo).
- Lista de rutas (colapsable): camino legible (títulos + labels), estado final, cómo terminó.
- a11y: labels, foco, CSS Modules (regla v0.6.0).

## Criterios de done

- [ ] `simulateRoutes`: DFS con estado, ciclos detectados (estado sin progreso), límites, determinista.
- [ ] Cobertura: reachable/unreachable nodes, endings alcanzables, conteos.
- [ ] Tests: ruta simple, ramas con condiciones, efectos que cambian el estado, loop, dead-end, límites.
- [ ] SimulatePanel: resumen + cobertura + rutas, CSS Modules, a11y.
- [ ] Tests verdes, lint, typecheck, build OK.
- [ ] E2E: abrir panel Simular, ver resumen y rutas.
