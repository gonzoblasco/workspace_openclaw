---
name: "workflow-tech-docs-enrich"
description: "Enriquecer workflow-tech-docs con fase de diseño arquitectónico, referencia de patrones y checklist de seguridad."
---

# Propuesta: Enriquecer workflow-tech-docs

## Problema

`workflow-tech-docs` cubre ADRs, README, API docs y CHANGELOG, pero arranca directo en "audiencia" sin una fase de diseño arquitectónico previa. No tiene soporte para diagramas, trade-offs ni patrones.

## Inspiración

Del AI Developer Stack (gonzoblasco/ai-developer-stack):
- `senior-architect` — diagramas C4/Mermaid, análisis de dependencias, trade-offs
- `architecture-patterns` — guía de Hexagonal, Clean Architecture, DDD
- `security-audit` — threat modeling, RLS, guards

## Propuesta de Cambios

### 1. Nueva Fase: Diseño Arquitectónico (pre-ADRs)

Agregar entre "Audiencia" y "Estructura":

1. **Diagramas** — generar diagramas C4/Mermaid de la arquitectura propuesta
2. **Trade-offs** — evaluar opciones (stack, patrones, base de datos)
3. **Dependencias** — analizar dependencias y salud del proyecto
4. **Riesgos** — identificar riesgos técnicos tempranos

### 2. Referencia de Patrones (integrada en ADRs)

Agregar como guía dentro de la fase de ADRs:

- **Hexagonal Architecture** — puertos y adaptadores
- **Clean Architecture** — capas y dependencias inward
- **Domain-Driven Design** — bounded contexts, entidades, value objects

### 3. Checklist de Seguridad (pre-ADRs)

Checklist rápido antes de documentar ADRs:

- Threat modeling básico
- RLS para multi-tenancy
- Guards de autenticación
- Rate limiting

## Próximos pasos

1. Aprobar propuesta
2. Actualizar SKILL.md de workflow-tech-docs
3. Probar en un proyecto real
