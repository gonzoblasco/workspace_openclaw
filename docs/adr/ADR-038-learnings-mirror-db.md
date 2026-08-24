# ADR-038: Learnings con mirror en DB (categorías + consulta veloz)

**Status:** Accepted
**Fecha:** 2026-08-23
**Origen:** workspace
**Scope:** Workspace - sistema de memoria (learnings)
**Deciders:** Gonzo / Kanam

## Contexto

Las lecciones aprendidas vivían en `docs/LEARNINGS.md` como un archivo monolítico de 681 líneas con 40+ lecciones mezcladas por tema (a11y, OSS, pipeline de agentes, infraestructura, proyectos, metodología). Al arrancar una tarea, consultar la lección relevante implicaba escanear todo el archivo.

Gonzo propuso dos mejoras: (1) separar las lecciones en archivos por categoría para consulta más rápida según el tipo de tarea, y (2) crear un mirror en la base de datos para que la consulta al arrancar una tarea sea veloz.

El workspace ya tiene un patrón establecido de "DB como fuente de verdad + markdown espejo regenerable" para datos estructurados: `todos`, `inbox` y `contributions` (OSS tracker) viven en `memory/memory.db` y se regeneran como markdown con `./scripts/memory-db.sh`.

**Anti-patrón a evitar:** un archivo monolítico que crece sin estructura, donde la consulta por tema es lenta y el conocimiento se pierde entre líneas.

## Decision

Separar las lecciones por categoría en `docs/learnings/` y crear un mirror en la DB (`memory/memory.db`, tabla `learnings`) como **fuente de verdad**.

### Estructura

```
docs/learnings/
├── README.md           (índice generado con conteo por categoría)
├── a11y.md             (accesibilidad: ARIA, axe, screen readers)
├── oss.md              (colaboración OSS: PRs, reviews, triage, bots)
├── pipeline-agentes.md (Qwen Code, cross-review, delegación, loops de IA)
├── infraestructura.md  (OpenClaw, Ollama, SQLite, sync, Tailwind, Docker, git)
├── proyectos.md        (SoporteML, Kanam Forge, skills, estructura)
└── metodologia.md      (proceso, documentación, patrones, ADHD, bootcamp)
```

`docs/LEARNINGS.md` queda como portada-índice con links a cada categoría.

### Tabla `learnings`

```sql
CREATE TABLE learnings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT NOT NULL,        -- a11y | oss | pipeline-agentes | infraestructura | proyectos | metodologia
  title TEXT NOT NULL,
  content TEXT NOT NULL,         -- la lección completa
  tags TEXT,                     -- tags para búsqueda
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT
);
```

### Flujo

- **Fuente de verdad:** la DB (`memory/memory.db`, tabla `learnings`).
- **Markdown espejo:** `docs/learnings/*.md` se regeneran con `./scripts/memory-db.sh export-learnings`. Nunca se editan a mano.
- **Consulta rápida al arrancar tarea:** `./scripts/memory-db.sh learnings <categoria>`.
- **Agregar lección:** `./scripts/memory-db.sh add-learning <cat> "<titulo>" "<contenido>" [tags]`.
- **Migración inicial:** `scripts/migrate-learnings.py` (idempotente, re-ejecutable).

## Por qué el mirror es correcto para learnings (y no para todo)

El mirror en DB es la decisión correcta **para learnings** porque:

1. **Consistencia con el patrón existente:** todos, inbox y contributions ya funcionan así. Agregar learnings al mismo patrón es consistencia, no una decisión nueva.
2. **Resuelve el caso de uso real:** consulta veloz por categoría al arrancar una tarea - exactamente el "query" que SQLite resuelve bien y que un markdown monolítico no.
3. **Las lecciones son híbridas:** tienen estructura (categoría, tags) + narrativa (contexto, reflexión). El mirror captura ambos: la estructura en la DB para consultar, la narrativa en markdown para leer.

**Límite del patrón (documentado en la lección del 14/08):** los documentos narrativos puros (MEMORY.md, AGENTS.md, SOUL.md) se leen como narrativa, se curan a mano, se versionan - migrarlos a DB es un error. El mirror es para **datos estructurados con narrativa**, no para narrativa pura.

## Consecuencias

1. **Consulta veloz:** al arrancar una tarea de a11y, `./scripts/memory-db.sh learnings a11y` devuelve las lecciones relevantes al instante, sin escanear 681 líneas.
2. **Crecimiento escalable:** las lecciones siguen acumulándose; la DB escala mejor que un archivo monolítico.
3. **Tags para búsqueda futura:** la columna `tags` habilita búsqueda semántica.
4. **Riesgo de desincronización:** dos fuentes (DB + markdown) pueden desincronizarse si se edita el markdown a mano. Mitigación: la DB es la fuente de verdad, los markdown son espejos regenerables, nunca se editan a mano (mismo patrón que todos/inbox/contributions).

## Implementación

```bash
# Regenerar los markdown por categoría desde la DB
./scripts/memory-db.sh export-learnings

# Consulta rápida por categoría
./scripts/memory-db.sh learnings a11y

# Agregar una lección
./scripts/memory-db.sh add-learning a11y "Titulo" "Contenido" "tags"

# Migración inicial (idempotente)
python3 scripts/migrate-learnings.py
```

## Referencias

- Lección del 14/08: "no todo lo que es archivo plano conviene migrarlo a DB; separar datos estructurados de documentos narrativos" (`docs/learnings/infraestructura.md`)
- Patrón existente: `todos`, `inbox`, `contributions` en `memory/memory.db`
- Script: `scripts/memory-db.sh`
