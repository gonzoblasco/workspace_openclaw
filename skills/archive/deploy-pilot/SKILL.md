---
name: "deploy-pilot"
description: "Full deploy lifecycle para Next.js en Vercel con planning phase obligatorio"
---

# deploy-pilot

## Descripción
Maneja el ciclo completo de deploy para aplicaciones Next.js: pre-deploy validation, GitHub push, monitoreo de deploy en Vercel, y post-deploy health checks. Cubre preview y production flows, environment variable management, rollbacks, y domain configuration. Enforces un planning phase obligatorio antes de cualquier push.

## Cuándo usarlo
- Para deployar una feature branch a Vercel preview URL para review
- Para mergear y releasear a producción con pre-deploy checks automáticos
- Para hacer rollback de un deploy roto a la última versión conocida buena
- Para sincronizar environment variables faltantes a Vercel antes de un release
- Para verificar CI status en un PR y mergear con squash commit

## Workflow
1. Planning phase: verificar env vars, build status, migraciones
2. Pre-deploy validation: correr tests, linter, type check
3. GitHub push a la branch correspondiente
4. Monitorear deploy en Vercel
5. Post-deploy health checks
6. Si algo falla, guía de rollback

## Tooling relacionado

Este workflow delega la ejecución a [deploy-agent](../deploy-agent/SKILL.md):

| Script | Uso |
|---|---|
| `deploy-agent/scripts/preflight.sh` | Verifica VERCEL_TOKEN, gh auth, proyecto configurado. Usar en Planning phase. |
| `deploy-agent/scripts/validate.sh` | Build + tests + types + lint. Usar en Pre-deploy validation. |
| `deploy-agent/scripts/deploy.sh` | Deploy a preview o production. Usar en paso 3. |
| `deploy-agent/scripts/monitor.sh` | Monitorea build en Vercel hasta READY/ERROR. Usar en paso 4. |
| `deploy-agent/scripts/health.sh` | Health checks post-deploy. Usar en paso 5. |
| `deploy-agent/scripts/rollback.sh` | Rollback al último deploy bueno. Usar si falla. |

## Notas
- El planning phase obligatorio atrapa errores antes de producción
- Requiere VERCEL_TOKEN
- Cubre preview y production flows
