---
name: "workflow-product-discovery"
description: "Workflow de Product Discovery: idea a definición de producto. Incluye ideación opcional y modo detallado. Reemplaza 4 skills de producto."
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

### 0. Ideación (opcional)
Si la idea es vaga o necesita exploración:
- Técnicas de brainstorming (SCAMPER, inversión, primeros principios)
- Mapa de soluciones existentes
- Definición del problema en una frase

### 1. Intake
Capturar idea, contexto, problema a resolver.

### 2. Evaluación
Mercado, competidores, viabilidad técnica (¿podemos construirlo con el stack actual? ¿Cuánto tiempo estimado? ¿Qué riesgos técnicos hay?), fit estratégico.

### 3. Definición
MVP, personas, features, métricas, posicionamiento.

### 4. Especificación
OpenSpec de features (delta si el proyecto ya existe, as-built si es nuevo), ADRs.

### 5. Go/No-Go
Decisión de construir o iterar.

### 6. Retrospectiva (post-lanzamiento)
¿Qué salió bien? ¿Qué no? ¿Qué aprendimos? Actualizar STATUS.md.

## Modo Detallado (--detailed)
Para proyectos complejos, en lugar de 5 archivos genera 9:
- BRIEF.md
- EVALUATION.md
- DEFINITION.md (expandido con PRD, user personas, features)
- ARCHITECTURE.md (decisiones técnicas tempranas)
- DESIGN.md (guía de estilo y UI)
- DATA_MODEL.md (esquemas de datos)
- ROADMAP.md
- STATUS.md
- TRACKER.md (seguimiento de progreso)

## Outputs
- `projects/<slug>/.knowledge/BRIEF.md`
- `projects/<slug>/.knowledge/EVALUATION.md`
- `projects/<slug>/.knowledge/DEFINITION.md`
- `projects/<slug>/.knowledge/ROADMAP.md`
- `projects/<slug>/.knowledge/STATUS.md`
- ADRs en `docs/adr/`
- (Modo detallado: + ARCHITECTURE.md, DESIGN.md, DATA_MODEL.md, TRACKER.md)
