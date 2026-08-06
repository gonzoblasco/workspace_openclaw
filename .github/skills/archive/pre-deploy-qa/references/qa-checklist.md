# QA Checklist — Pre-Deploy QA Reference

Checklist detallada para cada fase de validación pre-deploy.

## Build

- [ ] `npm run build` exits with 0
- [ ] No compilation warnings
- [ ] Source maps disabled in production
- [ ] Bundle analysis shows expected sizes

## Routes

- [ ] All public routes return 200
- [ ] Protected routes return 401/403 without auth
- [ ] API health endpoint responds
- [ ] Auth endpoints work (login, session, logout)
- [ ] sitemap.xml accessible
- [ ] robots.txt accessible
- [ ] 404 page renders for unknown routes

## SEO

- [ ] `<title>` 30-60 chars, unique per page
- [ ] `<meta name="description">` present
- [ ] og:title, og:description, og:image (≥ 1200×630)
- [ ] twitter:card = summary_large_image
- [ ] Canonical self-referencing
- [ ] favicon.ico responds 200
- [ ] JSON-LD structured data (if applicable)

## API

- [ ] Health check responds 200
- [ ] Auth endpoints work
- [ ] Errors return consistent JSON: `{ error, message }`
- [ ] CORS headers correct if cross-origin
- [ ] Rate limiting active
- [ ] Request validation active

## Performance

- [ ] Lighthouse ≥ 90 (Performance, A11y, SEO)
- [ ] Images: lazy loading + WebP/AVIF
- [ ] Dynamic imports for heavy components
- [ ] font-display: swap, no FOIT
- [ ] Total page weight < 1MB
- [ ] No render-blocking resources

## Security

- [ ] `npm audit` no critical/high vulnerabilities
- [ ] No secrets in diff
- [ ] No eval/new Function/document.write
- [ ] No stack traces in API errors
- [ ] CSP headers set
- [ ] XSS protection active

## UI/UX

- [ ] Error boundaries at root + route level
- [ ] not-found.tsx and loading.tsx exist
- [ ] Loading, error, empty states in client fetches
- [ ] Buttons: hover, focus-visible, active, disabled, loading
- [ ] No horizontal scroll at 320-1440px
- [ ] Touch targets ≥ 44×44px

## Database

- [ ] Migrations applied and idempotent
- [ ] No hardcoded DB credentials in source
- [ ] No raw SQL injection risk
- [ ] No N+1 queries

## Cleanup

- [ ] No console.log/debugger in staged code
- [ ] No unresolved TODOs/FIXMEs
- [ ] No dead imports
- [ ] No temporary files

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Review & Quality](../../review-quality) — Revisión pre-merge
