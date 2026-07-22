---
name: "pre-deploy-qa"
description: "Workflow de validación pre-deploy: build, rutas, SEO, API, performance, seguridad y cleanup. Se relaciona con review-quality (pre-merge) y build-scaffold (post-build)."
---

# Workflow: Pre-Deploy QA

## Qué hace
Validación sistemática antes de deployar a producción. Corre después del merge, antes del deploy.

## Fases

### 1. Build
- `npm run build` sin errores
- Verificar que no haya warnings de compilación

### 2. Rutas
- Regression de todas las rutas públicas (200)
- Rutas protegidas (401/403 sin auth)
- API endpoints (health, auth, core)
- sitemap.xml y robots.txt accesibles

### 3. SEO
- `<title>` 30-60 chars, único por página
- `<meta name="description">` presente
- og:title, og:description, og:image (≥ 1200×630)
- twitter:card = summary_large_image
- Canonical self-referencing
- favicon.ico responde 200
- JSON-LD structured data si aplica

### 4. API
- Health check responde 200
- Auth endpoints funcionan (login, session, logout)
- Errores devuelven JSON consistente `{ error, message }`
- CORS headers correctos si cross-origin

### 5. Performance
- Lighthouse ≥ 90 (Performance, A11y, SEO)
- Imágenes con lazy loading y WebP/AVIF
- Dynamic imports para componentes pesados
- font-display: swap, sin FOIT
- Total page weight < 1MB

### 6. Seguridad
- `npm audit` sin critical/high vulnerabilities
- Sin secrets en el diff
- Sin eval/new Function/document.write
- Sin stack traces en errores de API

### 7. UI/UX
- Error boundaries en root + route level
- not-found.tsx y loading.tsx existen
- Estados loading, error y empty en client fetches
- Botones con hover, focus-visible, active, disabled, loading
- Sin horizontal scroll en 320-1440px

### 8. Database
- Migraciones aplicadas y idempotentes
- Sin hardcoded DB credentials en source
- Sin raw SQL injection risk
- Sin N+1 queries

### 9. Cleanup
- Sin console.log/debugger en staged code
- Sin TODOs/FIXMEs sin resolver
- Sin imports muertos
- Sin archivos temporales

## Outputs
- Reporte de QA con cada fase (✅/❌/⚠️)
- Issues encontrados con prioridad (Critical / Major / Minor)
- Decisión: Go / No-Go para deploy
