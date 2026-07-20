---
name: "workflow-product-discovery"
description: "Workflow de Product Discovery: idea a definición de producto. Reemplaza 4 skills de producto."
---

# Workflow: Product Discovery

## Skills que reemplaza
- `product-orchestrator`
- `profile-positioning`
- `openspec-creator`
- `product-reset`

## Qué hace
Guía desde la idea inicial hasta la definición del producto lista para construir.

## Fases
1. **Intake** — capturar idea, contexto, problema a resolver
2. **Evaluación** — mercado, competidores, viabilidad técnica (¿podemos construirlo con el stack actual? ¿Cuánto tiempo estimado? ¿Qué riesgos técnicos hay?), fit estratégico
3. **Definición** — MVP, personas, features, métricas, posicionamiento
4. **Especificación** — OpenSpec de features (delta si el proyecto ya existe, as-built si es nuevo), ADRs
5. **Go/No-Go** — decisión de construir o iterar
6. **Retrospectiva** (post-lanzamiento) — ¿qué salió bien? ¿Qué no? ¿Qué aprendimos? Actualizar STATUS.md

## Outputs
- `projects/<slug>/.knowledge/BRIEF.md`
- `projects/<slug>/.knowledge/EVALUATION.md`
- `projects/<slug>/.knowledge/DEFINITION.md`
- `projects/<slug>/.knowledge/ROADMAP.md`
- `projects/<slug>/.knowledge/STATUS.md`
- ADRs en `docs/adr/`
