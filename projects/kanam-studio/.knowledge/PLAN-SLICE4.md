# Slice 4 - Canon checker automático (plan de implementación)

**T=16 (high)** | Pipeline: Kanam diseña → A escribe → B revisa → verificación

## Objetivo

Verificar la consistencia del grafo de narrativa y reportar problemas al autor. El canon checker es lógica pura (sin UI, sin storage) - la base para el Slice 5 (world-building con IA) y el Slice 7 (simulación de rutas).

## Checks a implementar

1. **Sin nodo start** (error): el grafo debe tener exactamente 1 nodo `start`.
2. **Múltiples nodos start** (error): más de 1 nodo `start`.
3. **Edges a nodos inexistentes** (error): `edge.target` o `edge.source` no existe en `story.nodes`.
4. **Nodos huérfanos** (warning): nodo sin edges entrantes que no es `start` (inalcanzable desde el inicio).
5. **Nodos sin salida** (warning): nodo que no es `ending` y no tiene edges salientes (callejón sin salida).
6. **Variables usadas pero no definidas** (error): variableId en condiciones/efectos que no existe en `story.variables`.
7. **Variables definidas pero nunca usadas** (info): variable que no aparece en ninguna condición/efecto.
8. **Finales inalcanzables** (warning): nodo `ending` sin camino desde el `start` (BFS).

## Arquitectura

```
src/lib/canon.ts          - lógica pura: checkCanon(story) → CanonReport
src/lib/canon.test.ts     - tests de cada check
src/components/CanonPanel.tsx - panel UI: lista de issues con severidad
StoryGraphEditor.tsx      - botón "Canon" + panel (4to panel)
```

### Tipos

```ts
type CanonSeverity = 'error' | 'warning' | 'info'
interface CanonIssue {
  severity: CanonSeverity
  code: string          // 'no-start' | 'multiple-start' | 'dangling-edge' | ...
  message: string       // legible, en español
  nodeId?: string       // nodo relacionado (para navegar al seleccionarlo)
  edgeId?: string
  variableId?: string
}
interface CanonReport {
  issues: CanonIssue[]
  summary: { errors: number; warnings: number; infos: number }
}
```

### checkCanon(story): CanonReport

- Orden de checks: primero los de estructura (start, edges), después los de variables, después los de alcanzabilidad (BFS desde start).
- BFS: si no hay start, los checks de alcanzabilidad se saltan (ya hay error de no-start).
- Los issues se ordenan por severidad (error > warning > info) y por código.

## UI (CanonPanel)

- Panel derecho (como NodeInspector/VariablesPanel/AICoAuthor), 4to panel `'canon'`.
- Header: "Canon" + badge con conteo (ej. "2 errores · 1 warning").
- Lista de issues: ícono/color por severidad (rojo error, ámbar warning, azul info), mensaje legible.
- Click en un issue con nodeId → selecciona el nodo en el grafo (setSelectedNodeId).
- a11y: lista con role="list", items con role="listitem", aria-label en el badge, foco manejado.
- Se recalcula al abrir el panel (useMemo sobre story).

## Criterios de done

- [ ] checkCanon cubre los 8 checks con tests (1 test por check + casos borde).
- [ ] Panel Canon muestra issues con severidad y conteo.
- [ ] Click en issue navega al nodo en el grafo.
- [ ] Tests verdes, lint, typecheck, build OK.
- [ ] Validado en browser real (o curl + tests si browser bloqueado).
