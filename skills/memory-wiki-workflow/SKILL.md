---
name: "memory-wiki-workflow"
description: "Capa analítica de memoria con memory-wiki: entities con claims (la ingesta sola no alcanza), dashboards y síntesis."
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

No siempre hace falta reiniciar. Verificado 2026-09-24: `openclaw plugins enable memory-wiki` devolvio `restartRequired: false` y el `config patch` aviso "will apply without restarting the gateway"; `wiki status` respondio de inmediato. Si algo no responde, ahi si: `openclaw gateway restart`.

**Grants que pide el plugin (saberlo ANTES de activar):** `allowConversationAccess` y `allowPromptInjection`. Es bundled y de la casa, pero no es pasivo: escribe un vault y toca la conversacion. Se activa por la via oficial (`plugins enable`, con el `reviewToken` del `inspect`), nunca editando el JSON a mano.

### 2. Verificar

```bash
openclaw wiki status       # modo, salud, páginas
openclaw wiki doctor       # health checks
openclaw wiki lint         # ideal: 0 issues
```

## Flujo: convertir datos estructurados en entities

**La trampa central: ingerir NO alcanza.** Los reports analiticos (claim-health, provenance-coverage, contradictions) **no leen el texto crudo** de `sources/`: leen la capa de **claims**. Si solo corres el paso (a), el vault queda con fuentes y los reports siguen diciendo "No structured claims yet" o "No issues", y **parece que el plugin no funciona** cuando en realidad falta un paso. El flujo completo:

```
ingest (evidencia)  ->  entities con claims (conocimiento)  ->  compile/lint (analisis)
```

Verificado 2026-09-24: tras ingestar 3 fuentes los reports siguieron vacios; con 1 entity de 4 claims, `provenance-coverage` paso a reportar "Evidence entries: 4 / Claims missing evidence: 0".

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

**Que los reports digan "no issues" NO prueba que funcionen.** Un detector esta probado recien cuando se le sembro el defecto que debe cazar. Para verificarlos: crear una entity con claims deliberadamente malos (uno sin `evidence`, uno con `confidence: 0.2`, uno con `status: contested`, y `updatedAt` viejo), correr `compile` + `lint`, y confirmar que `claim-health`, `low-confidence` y `stale-pages` reportan exactamente esos defectos. Borrada la sonda, los reports se limpian solos en el siguiente `compile`.

### d. Dashboards generados (en reports/)

Se pueblan desde la capa de **claims** (paso b), no desde las fuentes: vacios con fuentes y sin entities es el estado normal, no un fallo.

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

- **El vault no tiene backup por versionado:** vive en `~/.openclaw/wiki/main`, fuera del workspace git. El conocimiento compilado ahi **no viaja entre maquinas**; solo el material de origen (que si es workspace) es recuperable.
- **Politica de ingesta:** `memory/` y `docs/entrevistas/` contienen datos personales y de busqueda laboral: NO se ingestan sin decision explicita de Gonzo. El plugin viene con `bridge` y `unsafe-local` **apagados** por defecto, y esos son justamente los canales por los que podria chupar archivos privados: dejarlos asi.
- memory-wiki **no sirve UI web**. Es markdown local navegable (o Obsidian con renderMode obsidian). Para UI web hay que construir renderer aparte.
- La UI web que servía openclaw-os-plugin (ya eliminado) fue la que daba vista browser, no memory-wiki.
- El `index.md` del vault genera una página navegable con links a todas las entities/sources/syntheses/reports.
