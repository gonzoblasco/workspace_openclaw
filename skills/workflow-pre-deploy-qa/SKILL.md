---
name: "workflow-pre-deploy-qa"
description: "Workflow de validación pre-deploy: build, rutas, SEO, API, performance, seguridad y cleanup. Basado en vibecode-production-qa-validator."
---

# Propuesta: workflow-pre-deploy-qa

## Problema

OpenClaw tiene `workflow-review-quality` para code review pre-merge, pero no un workflow de QA pre-deploy que valide build, rutas, SEO, API auth, performance, seguridad y cleanup antes de ir a producción.

## Inspiración

Del AI Developer Stack (gonzoblasco/ai-developer-stack):
- `vibecode-production-qa-validator` — 13 fases de QA para Next.js fullstack

## Propuesta de Workflow

### Fases

1. **Build** — `npm run build` sin errores
2. **Rutas** — regression de todas las rutas (públicas, protegidas, API)
3. **SEO** — meta tags, OG images, favicon, sitemap, robots.txt
4. **API** — health check, auth headers, rate limiting
5. **Performance** — Lighthouse, lazy loading, bundle size
6. **Seguridad** — vulnerability scan, RLS, tokens
7. **UI/UX** — error boundaries, loading states, responsive
8. **Database** — migrations, RLS policies, indexes
9. **Cleanup** — console.logs, commented code, temp files

### Outputs

- Reporte de QA con cada fase (✅/❌)
- Issues encontrados con prioridad
- Go/No-Go para deploy

### Skills que reemplazaría

Ninguna — es nuevo. Se relaciona con `workflow-review-quality` (pre-merge) y `workflow-build-scaffold` (post-build).

## Próximos pasos

1. Aprobar propuesta
2. Escribir SKILL.md
3. Probar en un proyecto real
