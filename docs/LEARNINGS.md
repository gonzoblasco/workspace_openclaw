# LEARNINGS.md - Lecciones aprendidas del workspace

Lessons learned during development. Distilled from session notes; for cross-project patterns, see `skills/`.

> **Estructura:** las lecciones están separadas por categoría en `docs/learnings/`. La fuente de verdad es la DB (`memory/memory.db`, tabla `learnings`). Los archivos por categoría se regeneran con `./scripts/memory-db.sh export-learnings`.

## Cómo consultar

Según el tipo de tarea, abrir el archivo de la categoría correspondiente. Consulta rápida desde la DB:

```bash
./scripts/memory-db.sh learnings <categoria>
```

## Categorías

| Categoría | Archivo | Enfoque |
|-----------|---------|---------|
| **a11y** | [docs/learnings/a11y.md](docs/learnings/a11y.md) | Accesibilidad: ARIA, axe, screen readers, fixes de a11y |
| **oss** | [docs/learnings/oss.md](docs/learnings/oss.md) | Colaboración OSS: PRs, reviews, triage, bots, maintainers |
| **pipeline-agentes** | [docs/learnings/pipeline-agentes.md](docs/learnings/pipeline-agentes.md) | Qwen Code, cross-review, delegación, loops de IA |
| **infraestructura** | [docs/learnings/infraestructura.md](docs/learnings/infraestructura.md) | OpenClaw, Ollama, SQLite, sync, Tailwind, Docker, git |
| **proyectos** | [docs/learnings/proyectos.md](docs/learnings/proyectos.md) | SoporteML, Kanam Forge, skills, estructura de proyectos |
| **metodologia** | [docs/learnings/metodologia.md](docs/learnings/metodologia.md) | Proceso, documentación, patrones, ADHD, bootcamp |

## Índice completo

Ver [docs/learnings/README.md](docs/learnings/README.md) para el índice generado con el conteo por categoría.

---

*Este archivo es la portada. El contenido detallado vive en `docs/learnings/` y la fuente de verdad en la DB.*
