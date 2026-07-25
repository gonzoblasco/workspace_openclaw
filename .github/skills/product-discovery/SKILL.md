---
name: "product-discovery"
metadata:
  category: "Product"
  tags:
    - producto
    - discovery
    - definicion
description: "Workflow de Product Discovery: idea a definición de producto. Fase 0 dividida en Brainstorming (0.1), Arquitectura (0.2) y Diseño (0.3) con modelos especializados. Reemplaza 4 skills de producto."
user-invocable: false
---

# Workflow: Product Discovery

## Skills que reemplaza
- `product-orchestrator`
- `profile-positioning`
- `openspec-creator`
- `product-reset`

## Propósito
Guía desde la idea inicial hasta la definición del producto lista para construir.

## Fases

### Cuándo usarlo
- Explorar una idea de producto desde cero
- Evaluar viabilidad técnica y de mercado antes de construir
- Definir MVP, features, métricas y posicionamiento
- Documentar una especificación formal (OpenSpec) antes de arrancar desarrollo
- Hacer retrospectiva post-lanzamiento

### 0.1 — Brainstorming & Producto
**Rol:** Product Manager / Socio Fundador
**Modelo sugerido:** GLM 5.2 (visión holística, razonamiento de propósito general)
**Output:** `BRIEF.md`, `DEFINITION.md`

Abrir opciones, cuestionar la idea, encontrar la propuesta de valor:
- Técnicas de brainstorming (SCAMPER, inversión, primeros principios)
- Mapa de soluciones existentes
- Definición del problema en una frase
- Personas, métricas de éxito, features core
- Stack tecnológico asumido y restricciones conocidas

> **Validation Gate 0.1 → 0.2:** Antes de pasar a 0.2, verificar que BRIEF.md y DEFINITION.md estén completos:
> - [ ] Problema definido en una frase
> - [ ] Público objetivo identificado
> - [ ] Features core listadas
> - [ ] Métricas de éxito definidas
> - [ ] Stack asumido y restricciones técnicas documentadas
> - [ ] Preguntas abiertas para el arquitecto (si las hay)
>
> Si falta algo, volver a 0.1 antes de continuar.

### 0.2 — Arquitectura & Plan de Ataque
**Rol:** Arquitecto / Tech Lead
**Modelo sugerido:** Kimi K2.7 (rigor técnico, planificación agéntica)
**Output:** `OpenSpec`, `ADRs`, `ROADMAP.md`

Tomar la definición de producto de 0.1 y bajarla a tierra técnica:
- Stack tecnológico definitivo y justificación
- Patrones arquitectónicos (Hexagonal, DDD, etc.)
- Esquemas de base de datos
- Diagrama C4 (contexto, contenedores, componentes)
- ADRs iniciales de decisiones técnicas
- Desglose de epics y tasks en ROADMAP.md
- Identificación de riesgos técnicos y mitigaciones

> **Validation Gate 0.2 → 0.3:** Antes de pasar a 0.3, verificar que ARCHITECTURE.md, DATA_MODEL.md, ADRs y ROADMAP.md estén completos:
> - [ ] Stack definitivo documentado
> - [ ] Esquemas de DB completos
> - [ ] ADRs de decisiones técnicas clave
> - [ ] ROADMAP con sprints y tareas desglosadas
> - [ ] Riesgos técnicos identificados
>
> Si falta algo, volver a 0.2 antes de continuar.

### 0.3 — Diseño UI/UX
**Rol:** Diseñador / Product Designer
**Modelo sugerido:** Claude Sonnet (visión estética, consistencia visual)
**Output:** `DESIGN.md`

Definir la identidad visual y la experiencia de usuario antes de codear:
- Paleta de colores y justificación
- Tipografía y jerarquía visual
- Tono y personalidad de la interfaz
- Wireframes de pantallas clave (onboarding, feed, detalle de salida, perfil)
- Flujo de navegación
- Componentes visuales clave
- Estados (loading, vacío, error)

> **Validation Gate 0.3 → Build:** Antes de pasar a Build & Scaffold, verificar que DESIGN.md esté completo:
> - [ ] Paleta de colores definida
> - [ ] Tipografía definida
> - [ ] Wireframes de pantallas clave
> - [ ] Flujo de navegación documentado
> - [ ] Tono y personalidad definidos
>
> Si falta algo, volver a 0.3 antes de continuar.

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
- `projects/<slug>/.knowledge/BRIEF.md` (Fase 0.1)
- `projects/<slug>/.knowledge/EVALUATION.md`
- `projects/<slug>/.knowledge/DEFINITION.md` (Fase 0.1)
- `projects/<slug>/.knowledge/ARCHITECTURE.md` (Fase 0.2)
- `projects/<slug>/.knowledge/DATA_MODEL.md` (Fase 0.2)
- `projects/<slug>/.knowledge/ROADMAP.md` (Fase 0.2)
- `projects/<slug>/.knowledge/DESIGN.md` (Fase 0.3)
- `projects/<slug>/.knowledge/STATUS.md`
- `projects/<slug>/.knowledge/TRACKER.md`
- ADRs en `docs/adr/` (Fase 0.2)

## Related Skills

- [Build & Scaffold](../build-scaffold): Para construir el proyecto post-discovery
- [Technical Documentation](../tech-docs): Para documentar decisiones de producto
