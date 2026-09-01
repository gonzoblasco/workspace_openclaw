# Slice 6 - Export + derivación del relato lineal final (plan)

**T=12 (low)** | Pipeline: A escribe → Kanam revisa

## Contexto (visión corregida 2026-09-01)

Kanam Studio es un taller de mundos: el grafo es el andamiaje, la biblia el corazón. El paso final del flujo es **derivar el relato lineal**: el orden exacto de los sucesos (camino canónico + ramas) para escribir la prosa final. Este slice implementa eso + el export (JSON versionable para sync entre máquinas, Twine HTML, Ink).

## Objetivo

1. **Derivación del relato lineal** (`src/lib/timeline.ts`): dado el grafo, generar el orden canónico de los sucesos.
2. **Export JSON** (versionable, para sync entre máquinas vía git - respuesta a la pregunta de arquitectura de Gonzo).
3. **Export Twine HTML** (formato estándar de ficción interactiva).
4. **Export Ink** (formato de Inkle).
5. **UI**: panel "Exportar" con las opciones + vista previa del relato lineal.

## Arquitectura

```
src/lib/timeline.ts          - derivación del relato lineal (lógica pura)
src/lib/timeline.test.ts     - tests
src/lib/export.ts            - serializadores: JSON, Twine HTML, Ink
src/lib/export.test.ts       - tests
src/components/ExportPanel.tsx - panel: opciones de export + vista previa del relato
StoryGraphEditor.tsx           - 6to panel 'export'
```

### 1. Derivación del relato lineal (src/lib/timeline.ts)

Lógica pura, sin UI:

```ts
interface TimelineBeat {
  nodeId: string
  title: string
  content: string
  kind: 'start' | 'passage' | 'ending'
  /** Cómo se llegó a este nodo (label del edge). */
  via?: string
  /** Ramas alternativas disponibles en este punto (edges salientes no tomados). */
  branches?: { label: string; targetTitle: string }[]
}

function deriveTimeline(story: Story): TimelineBeat[]
```

- **Camino principal:** BFS/DFS desde el start siguiendo el primer edge saliente (o el de label más corto como heurística estable). Los nodos ending cierran el camino.
- **Ramas:** en cada nodo, los edges salientes NO tomados se listan como `branches` (para que el autor sepa qué alternativas existen y decida si las incorpora).
- **Determinismo:** mismo grafo → mismo timeline (orden estable por id de edge).
- Si no hay start: timeline vacío (el canon checker ya reporta no-start).

### 2. Export JSON (src/lib/export.ts)

```ts
function exportJson(story: Story): string
```

- `JSON.stringify(story, null, 2)` - el documento completo (grafo + biblia + variables).
- **Este es el formato versionable para sync entre máquinas** (respuesta a la pregunta de Gonzo: JSON en repo > .db binario).
- El panel ofrece "Descargar .json" (Blob + download) y "Copiar al portapapeles".

### 3. Export Twine HTML (src/lib/export.ts)

```ts
function exportTwineHtml(story: Story): string
```

- Formato Twine 2 (HTML con `<tw-passagedata>`): cada nodo = un pasaje, cada edge = un link `[[label -> targetTitle]]`.
- El start se marca con `pid` especial (Twine usa el pasaje "Start").
- Escapar HTML correctamente.

### 4. Export Ink (src/lib/export.ts)

```ts
function exportInk(story: Story): string
```

- Formato Ink: cada nodo = un knot, cada edge = una choice.
- Variables (flags/counters) → `VAR` de Ink.
- Condiciones/efectos → `{...}` de Ink (mapeo básico: eq/neq → `==`/`!=`, set → `~ var = value`, increment/decrement → `~ var += n`).

### 5. Panel Exportar (src/components/ExportPanel.tsx)

- Vista previa del **relato lineal** (timeline beats con ramas).
- Botones: "Descargar JSON", "Descargar Twine", "Descargar Ink", "Copiar JSON".
- a11y: labels, foco, CSS Modules (regla v0.6.0).

## Criterios de done

- [ ] `deriveTimeline`: camino principal + ramas, determinista, tests.
- [ ] `exportJson` / `exportTwineHtml` / `exportInk` con tests (escapado, estructura).
- [ ] ExportPanel: vista previa del relato + descargas, CSS Modules, a11y.
- [ ] Tests verdes, lint, typecheck, build OK.
- [ ] E2E: abrir panel Exportar, ver el relato lineal, descargar JSON.
