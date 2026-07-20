---
name: "workflow-product-discovery-enrich"
description: "Enriquecer workflow-product-discovery con fase de ideación (brainstorming) y modo detallado (8 archivos de planning)."
---

# Propuesta: Enriquecer workflow-product-discovery

## Problema

`workflow-product-discovery` arranca directo en "Intake" sin una fase de ideación pura. Además, el modo estándar produce 5 archivos de `.knowledge/` pero no hay un modo detallado para proyectos complejos.

## Inspiración

Del AI Developer Stack (gonzoblasco/ai-developer-stack):
- `brainstorming` — técnicas de ideación estructurada (SCAMPER, Primeros Principios, Inversión)
- `not-a-vibe-coder` — 8 archivos de planning (PRD, Architecture, Design, Data Model, Routes, Components, Tracker, Guidelines)

## Propuesta de Cambios

### 1. Fase opcional de Ideación (antes de Intake)

Agregar como paso opcional al inicio:
- Técnicas de brainstorming (SCAMPER, inversión, primeros principios)
- Mapa de soluciones existentes
- Definición del problema en una frase

### 2. Modo Detallado (flag --detailed)

Cuando se activa, en lugar de 5 archivos de `.knowledge/`:
- BRIEF.md
- EVALUATION.md
- DEFINITION.md (expandido con PRD, user personas, features)
- ARCHITECTURE.md (nuevo — decisiones técnicas tempranas)
- DESIGN.md (nuevo — guía de estilo y UI)
- DATA_MODEL.md (nuevo — esquemas de datos)
- ROADMAP.md
- STATUS.md
- TRACKER.md (nuevo — seguimiento de progreso)

### 3. Modo Estándar (default)

Sin cambios — los 5 archivos actuales funcionan bien para proyectos chicos/medios.

## Próximos pasos

1. Aprobar propuesta
2. Actualizar SKILL.md de workflow-product-discovery
3. Probar modo detallado en un proyecto
