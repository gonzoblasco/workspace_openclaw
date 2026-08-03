---
name: "pre-deploy-qa"
description: "Pre-deploy QA workflow with added PWA/service worker validation"
metadata:
  category: "Workflow"
  tags:
    - deploy
    - calidad
    - validacion
user-invocable: false
---

# Workflow: Pre-Deploy QA

## Purpose
Systematic validation before deploying to production. Runs after merge, before deploy.

## When to use
- Before deploying to production (post-merge, pre-deploy)
- After significant changes affecting routes, API, SEO, or PWA behavior
- As a quality gate in CI/CD
- To get a Go/No-Go report before release

## Phases

### 1. Build
- `npm run build` with no errors
- No build warnings

### 2. Routes
- Regression of all public routes (200)
- Protected routes (401/403 without auth)
- API endpoints (health, auth, core)
- `sitemap.xml` and `robots.txt` accessible

### 3. SEO
- `<title>` 30-60 chars, unique per page
- `<meta name="description">` present
- og:title, og:description, og:image (≥ 1200×630)
- twitter:card = summary_large_image
- Self-referencing canonical
- favicon.ico returns 200
- JSON-LD structured data if applicable

### 4. PWA / Service Worker
- App has `manifest.json` with valid `start_url`, `display`, `theme_color`
- Icons 192×192 and 512×512 exist and are referenced
- `sw.js` is registered with a relative path and loads without errors
- `index.html` (shell) is **not** served cache-first; use network-first or stale-while-revalidate
- Hashed JS/CSS build assets are cached dynamically or listed in precache
- After deploy, verify no 404 for old hashed assets in DevTools Network tab
- Cache name/version is bumped when the service worker strategy changes

### 5. API
- Health check returns 200
- Auth endpoints work (login, session, logout)
- Errors return consistent JSON `{ error, message }`
- CORS headers correct if cross-origin

### 6. Performance
- Lighthouse ≥ 90 (Performance, Accessibility, Best Practices, SEO)
- Images lazy loaded and served as WebP/AVIF
- Dynamic imports for heavy components
- font-display: swap, no FOIT
- Total page weight < 1MB

### 7. Security
- `npm audit` no critical/high vulnerabilities
- No secrets in diff
- No eval/new Function/document.write
- No stack traces in API errors

### 8. UI/UX
- Error boundaries at root + route level
- not-found.tsx and loading.tsx exist
- Loading, error, and empty states in client fetches
- Buttons have hover, focus-visible, active, disabled, loading states
- No horizontal scroll at 320-1440px

### 9. Database
- Migrations applied and idempotent
- No hardcoded DB credentials in source
- No SQL injection risk
- No N+1 queries

### 10. Cleanup
- No console.log/debugger in staged code
- No unresolved TODOs/FIXMEs
- No dead imports
- No temporary files

## Outputs
- QA report per phase (✅/❌/⚠️)
- Issues with priority (Critical / Major / Minor)
- Go / No-Go decision for deploy

## Helper Scripts

Scripts en `skills/pre-deploy-qa/scripts/`:

| Script | Uso |
|---|---|
| `pre-deploy-check.sh [--url <base-url>] [--output <file>]` | Corre build, endpoints de health/home/sitemap, API auth, npm audit, y busqueda de `console.log` en `src/`. Genera un reporte Markdown con decision Go/No-Go. Usar en fases 1, 2, 3, 5, 7, 10. |
| `smoke-test.sh <url>` | Smoke tests rapidos de endpoints: /health, /, /api/auth/session, /sitemap.xml, /robots.txt, /favicon.ico. Usar justo despues del deploy. |

## Related Skills
- [Review & Quality](../review-quality): Pre-merge review before QA
- [Task Execution](../task-execution): Implement fixes found by QA
- [Performance Optimization](../performance-optimization): Validate performance pre-deploy
