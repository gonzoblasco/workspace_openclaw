---
name: "memory-wiki-workflow"
description: "Flujo para usar memory-wiki como capa analítica de memoria: entities con claims, dashboards, síntesis y visualización markdown."
---

# Memory Wiki Workflow

Flujo para usar `memory-wiki` como capa analítica y navegable sobre la memoria del workspace, sin reemplazar la fuente de verdad existente.

## Cuándo usar

- Querés ver datos estructurados del workspace (OSS tracker, todos, inbox, daily) como un **wiki navegable** con entities, claims y dashboards.
- Querés que la memoria "se consolide sola": detectar contradicciones, páginas stale, claims sin evidencia.
- Necesitás una capa analítica sobre `memory.db` (SQLite) sin tocar la DB.

## Principios

1. **memory.db sigue siendo la fuente de verdad.** memory-wiki es la capa analítica encima, NO la reemplaza.
2. **memory-core** (memoria activa de OpenClaw) hace `memory_search` sobre markdown. memory-wiki **compila** conocimiento durable aparte.
3. El wiki vive en `~/.openclaw/wiki/main` (vault, NO en el workspace git).

## Setup

### 1. Habilitar (si no está)

Config en `~/.openclaw/openclaw.json`:

```json5
{
  plugins: {
    entries: {
      "memory-wiki": {
        enabled: true,
        config: {
          vaultMode: "isolated",          // o "bridge" para leer memoria activa
          search: { backend: "shared", corpus: "all" },  // conecta con memory_search
          render: { createDashboards: true, createBacklinks: true },
          context: { includeCompiledDigestPrompt: false }
        }
      }
    }
  }
}
```

Luego: `openclaw gateway restart`.

### 2. Verificar

```bash
openclaw wiki status       # modo, salud, páginas
openclaw wiki doctor       # health checks
```

## Flujo: convertir datos estructurados en entities

### a. Ingerir fuente (markdown crudo)

```bash
openclaw wiki ingest <archivo.md> --title "Título"
# → copia a sources/ con provenance (sourcePath, ingestedAt). No modifica el original.
```

### b. Crear entity con claims (la parte valiosa)

Escribir en `~/.openclaw/wiki/main/entities/<id>.md` con frontmatter:

```yaml
---
pageType: entity
entityType: project            # project | person | system | ...
id: entity.<id>
canonicalId: repo.<org>/<repo>
aliases: [<alias>]
privacyTier: local-private
sourceIds: [source.<source-id>]          # <- provenance (obligatorio, evita warning)
updatedAt: "2026-08-23T00:00:00.000Z"   # <- freshness (obligatorio)
claims:
  - id: claim.<id>.<n>
    text: "Descripción del claim."
    status: active
    confidence: 0.9
    updatedAt: "2026-08-23T00:00:00.000Z"
    evidence:
      - kind: source-page
        sourceId: <source-id>
        weight: 1.0
---
```

**Ojo con los warnings de lint:** cada entity page necesita `sourceIds` (provenance) y `updatedAt` (page + cada claim). Sin eso, el lint marca "freshness needs review" y "missing sourceIds". Se corrigen agregando esos campos.

### c. Compilar y validar

```bash
openclaw wiki compile   # regenera índices + agent-digest
openclaw wiki lint      # ideal: 0 issues
```

### d. Dashboards generados (en reports/)

- `relationship-graph.md` - edges entre entities y sources
- `provenance-coverage.md` - cuánta evidencia tiene cada claim
- `claim-health.md` - claims sin evidencia / stale / contested
- `contradictions.md`, `low-confidence.md`, `open-questions.md`, `stale-pages.md`

## Consulta

```bash
openclaw wiki search "query"
openclaw wiki get entity.<id>
```

O en el agente: tools `wiki_search`, `wiki_get`, `wiki_apply`, `wiki_lint`, `wiki_status`. Con `search.backend: shared` y `corpus: all`, `memory_search` y `wiki_search` se conectan.

## Síntesis (wiki_apply)

```bash
openclaw wiki apply synthesis "Título" --body "..." --source-id source.<id>
```

Crea una síntesis con claims para consolidar decisiones. Puebla dashboards.

## Notas

- memory-wiki **no sirve UI web**. Es markdown local navegable (o Obsidian con renderMode obsidian). Para UI web hay que construir renderer aparte.
- La UI web que servía openclaw-os-plugin (ya eliminado) fue la que daba vista browser, no memory-wiki.
- El `index.md` del vault genera una página navegable con links a todas las entities/sources/syntheses/reports.
