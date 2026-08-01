# Routing Map — Orchestrator Agent

Mapa de ruteo actualizable. El Orchestrator consulta este archivo para decidir qué agente invocar.

## Agentes activos

| Agente | Skill | Cuándo usarlo |
|---|---|---|
| Debug Agent | `debug-agent` | Bugs, errores, comportamiento inesperado, debugging |
| Execution Agent | `execution-agent` | Features, tareas, implementación, fixes |
| Memory Agent | `memory-agent` | Consolidación de memoria, DREAMS, knowledge graph |
| Orchestrator | `orchestrator-agent` | Punto de entrada, routing, coordinación |
| Governance Agent | `governance-agent` | Auditoría del ecosistema, RFCs, mejora continua |
| Code Review Agent | `code-review-agent` | Revisión de PRs, confidence scoring, security audit |
| Research Agent | `research-agent` | Investigación, búsqueda, síntesis, comparativas |
| A11y Audit Agent | `a11y-audit-agent` | Auditoría WCAG, contraste, ARIA, reportes |
| OSS Agent | `oss-agent` | Monitoreo de issues, PRs a OSS, contribución estratégica |
| Deploy Agent | `deploy-agent` | CI/CD, deploy a Vercel, health checks, rollback |

## Palabras clave para clasificación

### Debug Agent
bug, error, falla, crash, excepción, no funciona, se rompe, comportamiento extraño, no carga, no responde, error en consola, stack trace, 500, timeout, race condition, intermitente, debuggear, investigar bug

### Execution Agent
implementar, crear, agregar, modificar, cambiar, refactorizar, migrar, actualizar, fixear, feature, tarea, epic, PR, branch, desarrollar, codificar

### Memory Agent
consolidar, memoria, DREAMS, knowledge graph, inconsistencia, documentación, daily log, aprender, recordar, patrón, knowledge, conocimiento, lección

### Governance Agent
governance, gobernanza, auditar ecosistema, RFC, mejora continua, health check, sistema, workflow audit, patrón sistémico, calidad del sistema

### Code Review Agent
review, code review, revisar código, PR review, confidence, audit seguridad, revisar PR, diff, cambios, linter cognitivo

### Research Agent
investigar, buscar, averiguar, qué es, cómo funciona, comparar, analizar, research, spike, tecnología, librería, API, benchmark, alternativa, viabilidad

### A11y Audit Agent
accesibilidad, a11y, WCAG, auditoría, contraste, screen reader, axe, aria, teclado, keyboard, foco visible, etiquetas, alt text, conformidad

### OSS Agent
OSS, open source, contribución, issue, PR externo, good first issue, fork, comunidad, tier, repo externo, shadcn, tanstack, biome, supabase, vercel

### Deploy Agent
deploy, release, CI/CD, pipeline, build, producción, staging, rollback, vercel, preview, health check, pre-deploy, post-deploy

## Flujo de decisión

Cuando el Orchestrator recibe una solicitud:

1. **Clasificar** — matchear palabras clave contra los agentes
2. **Si hay match único** → rutear a ese agente
3. **Si hay múltiples matches** → elegir el más específico:
   - "revisá seguridad de este PR" → Code Review Agent (no Execution Agent)
   - "deployá a producción después del review" → Deploy Agent (después de Code Review)
4. **Si no hay match** → resolver directamente (Kanam)
5. **Si es ambiguo** → preguntar antes de rutear

## Handoff entre agentes

### Cadenas comunes

| Flujo | Agentes involucrados |
|---|---|
| Bug → Fix | Debug Agent → Execution Agent |
| Feature → Review → Deploy | Execution Agent → Code Review Agent → Deploy Agent |
| Research → Implement | Research Agent → Execution Agent |
| A11y Audit → Fix | A11y Audit Agent → Execution Agent |
| OSS PR → Review | OSS Agent → Code Review Agent |
| Cualquier agente → Memoria | [Agente] → Memory Agent |
| Ecosistema → Mejora | Governance Agent → Orchestrator (RFC) |

### Handoff automático
- Cuando un agente termina, el Orchestrator evalúa si el siguiente agente en la cadena debe arrancar automáticamente
- Si la cadena es clara (ej: "debuggeá y fixeá"), el Orchestrator encadena sin preguntar
- Si la cadena es ambigua, pregunta antes de continuar
