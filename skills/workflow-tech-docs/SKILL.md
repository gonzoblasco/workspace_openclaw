---
name: "workflow-tech-docs"
description: "Workflow de Technical Documentation: ADRs, README, API docs, CHANGELOG, guías técnicas."
---

# Workflow: Technical Documentation

## Skills que reemplaza
- `adr-framework`
- `adr-sync`

## Qué hace
Creación y gestión de documentación técnica de proyectos: ADRs, README, API docs, CHANGELOG, guías de contribución.

## Fases
1. **Audiencia** — ¿quién lee estos docs? (devs del equipo, contributors externos, usuarios finales, stakeholders)
2. **Estructura** — qué docs necesita el proyecto (README, API docs, guías, ADRs, CHANGELOG, CONTRIBUTING)
3. **ADRs** — crear o sincronizar decisiones arquitecturales con el formato estándar: contexto, decisión, consecuencias, alternativas consideradas
4. **Redacción técnica** — escribir o actualizar docs con ejemplos concretos, no teoría. Código real, no pseudocódigo
5. **Revisión** — coherencia, completitud, ejemplos funcionan, enlaces no rotos, tono consistente
6. **Publicación** — commit + push, integración con el proyecto

## Outputs
- README.md actualizado
- ADRs en `docs/adr/` (creados o sincronizados)
- CHANGELOG.md actualizado
- API docs, guías técnicas
- CONTRIBUTING.md si aplica

## Cuándo usarlo
- Al arrancar un proyecto nuevo (docs iniciales)
- Cuando se cambia una API o feature (actualizar docs)
- Al cerrar un epic o milestone (actualizar CHANGELOG + ADRs)
- Cuando un contributor necesita guías claras
