---
name: "workflow-review-quality-enrich"
description: "Enriquecer workflow-review-quality con fase de validación pre-deploy: build, rutas, SEO, API, performance, seguridad."
---

# Propuesta: Enriquecer workflow-review-quality

## Problema

`workflow-review-quality` se enfoca en code review pre-merge (seguridad, convenciones, tests). No cubre validación pre-deploy: build, rutas, SEO, API, performance.

## Inspiración

Del AI Developer Stack (gonzoblasco/ai-developer-stack):
- `vibecode-production-qa-validator` — 13 fases de QA para Next.js fullstack

## Propuesta de Cambios

### Nueva Fase: Validación Pre-Deploy (opcional, post-merge)

Agregar como fase opcional al final del workflow:

1. **Build check** — `npm run build` sin errores
2. **Route regression** — todas las rutas responden (200)
3. **SEO audit** — meta tags, OG images, sitemap
4. **API health** — endpoints responden, auth funciona
5. **Performance** — Lighthouse scores, lazy loading
6. **Security scan** — vulnerabilidades conocidas
7. **Cleanup** — console.logs, commented code, archivos temporales

### Outputs adicionales

- Reporte de QA pre-deploy
- Go/No-Go para producción

## Próximos pasos

1. Aprobar propuesta
2. Actualizar SKILL.md de workflow-review-quality
3. Probar en un proyecto real
