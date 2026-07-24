# Pre-Deploy QA

Validación pre-deploy para producción.

## ¿Para qué sirve?

Para **validar todo antes de deployar a producción**. Corre después del merge, antes del deploy. Verifica build, rutas, SEO, API, performance, seguridad, UI/UX, database y cleanup. Genera un reporte Go/No-Go.

## ¿Cuándo usarlo?

- Antes de cada deploy a producción
- Como gate de calidad en CI/CD
- Después de cambios significativos que afectan rutas, API o SEO

## ¿Cómo se usa?

### Workflow completo

1. **Build** — `npm run build` sin errores ni warnings
2. **Routes** — todas las rutas públicas 200, protegidas 401/403
3. **SEO** — title, description, OG, Twitter, canonical, favicon, JSON-LD
4. **API** — health, auth, CORS, rate limiting
5. **Performance** — Lighthouse ≥ 90, lazy loading, WebP, < 1MB
6. **Security** — npm audit, no secrets, no eval, CSP
7. **UI/UX** — error boundaries, loading states, touch targets
8. **Database** — migrations idempotent, no N+1
9. **Cleanup** — no console.log, no TODOs, no dead imports

### Scripts útiles

```bash
# Correr todas las verificaciones
./scripts/pre-deploy-check.sh --url https://staging.tusitio.com

# Smoke tests rápidos post-deploy
./scripts/smoke-test.sh https://tusitio.com
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/qa-checklist.md` | Checklist detallada por fase con items específicos |
| `references/ci-gate.md` | Template de GitHub Actions + smoke test script |

## Skills relacionadas

- [Review & Quality](../review-quality) — Para revisión pre-merge antes del QA
- [Task Execution](../task-execution) — Para implementar fixes encontrados en QA
