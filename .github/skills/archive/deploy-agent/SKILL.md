---
name: "deploy-agent"
metadata:
  category: "Agent"
  tags:
    - deploy
    - release
    - vercel
    - ci-cd
    - agente-autonomo
description: "Deploy Agent: maneja el ciclo completo de deploy para Next.js en Vercel. Planning, pre-deploy validation, push, monitoreo, health checks, y rollback."
user-invocable: true
---

# Deploy Agent

Agente autónomo de deploy. Hereda el workflow de [deploy-pilot](../deploy-pilot/SKILL.md). Maneja el ciclo completo: planning, validación, push, monitoreo, health checks, y rollback.

## Filosofía

Planning phase obligatorio antes de cualquier push. Pre-deploy validation atrapa errores antes de producción. Rollback automático si los health checks fallan.

## Invocación

Desde el chat:

> Kanam, deployá [branch] a preview
> Kanam, releaseá a producción
> Kanam, hacé rollback del último deploy
> Kanam, verificá el estado del deploy

Desde el Orchestrator:
- Cuando la solicitud es deploy, release, producción, CI/CD

## Flujo del agente

### Fase 0: Pre-flight Check
Antes de cualquier deploy, verificar:

1. **VERCEL_TOKEN** configurado en el entorno
2. **GitHub CLI** autenticado (`gh auth status`)
3. **Proyecto** configurado en Vercel (`vercel link` o `vercel.json`)
4. **Branch** actual y estado del working tree

Si falta algo, reportar y no continuar.

### Fase 1: Planning
Para CADA deploy:

1. **Verificar env vars** — comparar `.env.local` con Vercel project env vars. Si faltan, listarlas
2. **Verificar build status** — `npm run build` localmente (debe pasar)
3. **Verificar migraciones** — si hay cambios en schema, verificar que las migraciones estén listas
4. **Verificar CI** — si es un PR, verificar que los checks de CI pasen
5. **Generar plan** — resumen de lo que se va a deployar

### Fase 2: Pre-deploy Validation
Ejecutar:

1. `npm run build` — build completo
2. `npx vitest run` — tests
3. `npx tsc --noEmit` — type check
4. `npx biome check` — lint
5. Si algo falla: NO deployar. Handoff al Debug Agent o escalar

### Fase 3: Deploy
**Para preview (branch):**
```bash
vercel --token $VERCEL_TOKEN
```

**Para producción (main):**
```bash
vercel --prod --token $VERCEL_TOKEN
```

### Fase 4: Monitor
1. Obtener URL del deploy (preview o production)
2. Monitorear el build en Vercel:
   - `vercel inspect <deploy-id> --token $VERCEL_TOKEN`
   - Esperar hasta que el estado sea "READY" o "ERROR"
3. Si el build falla: reportar error, NO hacer health checks

### Fase 5: Health Check
Una vez que el deploy está READY:

1. **HTTP 200** — `curl -o /dev/null -s -w "%{http_code}" <url>` debe ser 200
2. **Rutas críticas** — verificar que las rutas principales respondan
3. **API health** — si hay API, verificar que responda
4. **Performance** — Lighthouse o métrica simple de tiempo de carga

### Fase 6: Rollback (si health checks fallan)
Si los health checks fallan:

1. Identificar el último deploy conocido bueno
2. Ejecutar rollback:
   ```bash
   vercel rollback --token $VERCEL_TOKEN
   ```
3. Verificar que el rollback fue exitoso
4. Reportar: qué falló, qué se hizo, qué sigue

### Fase 7: Report
Generar reporte estructurado:

```json
{
  "status": "success" | "failed" | "rolled_back",
  "environment": "preview" | "production",
  "branch": "feat/xxx",
  "url": "https://...",
  "deployId": "dpl_xxx",
  "buildTime": "2m 30s",
  "healthChecks": {
    "http200": true,
    "routes": {"pass": 5, "fail": 0},
    "api": true,
    "performance": "good"
  },
  "rollback": {
    "needed": false,
    "previousDeploy": "dpl_yyy",
    "success": null
  }
}
```

## Scripts

| Script | Función |
|---|---|
| `scripts/preflight.sh` | Verifica VERCEL_TOKEN, gh auth, proyecto configurado |
| `scripts/validate.sh` | Build + tests + types + lint |
| `scripts/deploy.sh` | Deploy a preview o production |
| `scripts/monitor.sh` | Monitorea build en Vercel hasta READY/ERROR |
| `scripts/health.sh` | Health checks post-deploy |
| `scripts/rollback.sh` | Rollback al último deploy bueno |

## Integración con otros agentes

### Con Execution Agent
- Después del deploy exitoso, handoff al Execution Agent para post-deploy tasks
- Si el deploy falla, handoff al Debug Agent para root cause

### Con Code Review Agent
- Antes de deployar a producción, verificar que el PR pasó code review
- Si no pasó, NO deployar

### Con Governance Agent
- El Governance Agent audita la frecuencia y éxito de deploys
- Detecta patrones: mismos errores recurrentes, deploys fallidos frecuentes

## Structured Escalation

```
BLOQUEO: Deploy Agent — no puede completar el deploy
CAUSA: [VERCEL_TOKEN no configurado, build falla, health checks no pasan]
INTENTOS: [qué se intentó, qué validaciones se corrieron]
NECESITO: [decisión de Gonzo: proceder igual, rollback, debuggear]
ALTERNATIVA: [rollback automático si health checks fallan, o skip health checks si Gonzo lo autoriza]
```

## Principios

- Planning phase obligatorio antes de cualquier push
- Pre-deploy validation atrapa errores antes de producción
- Rollback automático si health checks fallan
- No deployar si el PR no pasó code review
- Monitorear post-deploy, no abandonar
- Cada deploy debe ser reversible
