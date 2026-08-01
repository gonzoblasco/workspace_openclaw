# Routing Map — Orchestrator Agent

Mapa de ruteo actualizable. El Orchestrator consulta este archivo para decidir qué agente invocar.

## Agentes activos

| Agente | Skill | Cuándo usarlo |
|---|---|---|
| Debug Agent | `debug-agent` | Bugs, errores, comportamiento inesperado, debugging |
| Execution Agent | `execution-agent` | Features, tareas, implementación, fixes |
| Memory Agent | `memory-agent` | Consolidación de memoria, DREAMS, knowledge graph |
| Orchestrator | `orchestrator-agent` | Punto de entrada, routing, coordinación |

## Agentes planificados

| Agente | Skill | Cuándo usarlo |
|---|---|---|
| Governance Agent | `engineering-governance` | PR review, calidad de código, governance |
| Code Review Agent | `review-quality` | Revisión de PRs, confidence scoring |
| Research Agent | `research-spike` | Investigación, búsqueda, síntesis |
| A11y Audit Agent | `accessibility-studio` + `sovereign-accessibility-auditor` | Auditoría WCAG, reportes |
| OSS Agent | `oss-contribution` | Monitoreo de issues, PRs a OSS |
| Deploy Agent | `deploy-pilot` | CI/CD, deploy, rollback |

## Palabras clave para clasificación

### Debug Agent
bug, error, falla, crash, excepción, no funciona, se rompe, comportamiento extraño, no carga, no responde, error en consola, stack trace, 500, timeout, race condition, intermitente

### Execution Agent
implementar, crear, agregar, modificar, cambiar, refactorizar, migrar, actualizar, fixear, feature, tarea, epic, PR, branch

### Memory Agent
consolidar, memoria, DREAMS, knowledge graph, inconsistencia, documentación, daily log, aprender, recordar, patrón

### Governance Agent (planificado)
revisar PR, governance, calidad, estándar, ADR, arquitectura, desviación

### Code Review Agent (planificado)
review, code review, revisar código, PR review, confidence

### Research Agent (planificado)
investigar, buscar, averiguar, qué es, cómo funciona, comparar, analizar, research

### A11y Audit Agent (planificado)
accesibilidad, a11y, WCAG, auditoría, contraste, screen reader, axe

### OSS Agent (planificado)
OSS, open source, contribución, issue, PR externo, good first issue

### Deploy Agent (planificado)
deploy, release, CI/CD, pipeline, build, producción, staging, rollback
