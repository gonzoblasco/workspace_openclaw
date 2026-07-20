---
name: "workflow-review-quality-enrich-v2"
description: "Enriquecer workflow-review-quality con fase de testing (Vitest, TDD, E2E) y validación pre-deploy (build, rutas, SEO, API, performance, seguridad)."
---

# Propuesta: Enriquecer workflow-review-quality (v2)

## Problema

`workflow-review-quality` se enfoca en code review pre-merge. No cubre:
- Estrategia de testing (cómo escribir tests, no solo verificar que existan)
- Validación pre-deploy (build, rutas, SEO, API, performance)

## Inspiración

Del AI Developer Stack (gonzoblasco/ai-developer-stack):
- `testing-patterns` — Vitest, mock factories, TDD
- `javascript-testing-patterns` — unit, integration, E2E, MSW
- `e2e-testing-patterns` — Playwright
- `vibecode-production-qa-validator` — 13 fases de QA

## Propuesta de Cambios

### 1. Nueva Fase: Estrategia de Testing (al inicio)

Agregar antes del análisis de diff:

1. **TDD** — escribir test primero, implementar después
2. **Unit testing** — Vitest, mock factories, factory functions
3. **Integration testing** — MSW, API contracts
4. **E2E** — Playwright, browser testing
5. **Cobertura** — qué testear y qué no

### 2. Nueva Fase: Validación Pre-Deploy (al final, opcional)

Agregar después del gate:

1. **Build check** — `npm run build` sin errores
2. **Route regression** — todas las rutas responden (200)
3. **SEO audit** — meta tags, OG images, sitemap
4. **API health** — endpoints responden, auth funciona
5. **Performance** — Lighthouse scores, lazy loading
6. **Security scan** — vulnerabilidades conocidas
7. **Cleanup** — console.logs, commented code, archivos temporales

### Fases resultantes

1. **Estrategia de Testing** (nueva)
2. **Análisis de diff** (existente)
3. **Linter cognitivo** (existente)
4. **Auditoría de seguridad** (existente)
5. **Revisión de producto** (existente)
6. **Validación pre-deploy** (nueva, opcional)
7. **Reporte** (existente)
8. **Gate** (existente)

## Próximos pasos

1. Aprobar propuesta
2. Actualizar SKILL.md de workflow-review-quality
3. Probar en un proyecto real
