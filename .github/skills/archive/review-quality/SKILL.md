---
name: "review-quality"
metadata:
  category: "Workflow"
  tags:
    - calidad
    - testing
    - seguridad
    - code-review
description: "Workflow de Review & Quality: revisión pre-merge, testing y auditoría. Reemplaza pr-review, po-review, security-audit, agent-review."
user-invocable: false
---

# Workflow: Review & Quality

## Skills que reemplaza
- `pr-review`
- `po-review`
- `security-audit`
- `agent-review`

## Propósito
Revisión de calidad antes de mergear o cerrar un ciclo. Incluye estrategia de testing, code review, auditoría de seguridad y validación pre-deploy opcional.

## Cuándo usarlo
- Revisar un PR antes de mergear (code review + testing + seguridad)
- Auditar seguridad de un cambio (multi-tenant, auth, secrets, RLS)
- Verificar que un cambio cumple con la spec de producto
- Validación pre-deploy opcional post-merge

## Fases

### 1. Estrategia de Testing
Antes de revisar el diff, establecer la estrategia:
- **TDD** — escribir test primero, implementar después
- **Unit testing** — Vitest, mock factories, factory functions. Testear comportamientos, no implementaciones
- **Integration testing** — MSW para mocking de APIs, test de contratos
- **E2E** — Playwright para flujos críticos de usuario
- **Cobertura** — qué testear (lógica de negocio, edge cases) y qué no (config, boilerplate)

### 2. Análisis de diff
Cambios, archivos tocados, impacto.

### 3. Linter cognitivo
Convenciones, naming, estructura, tests. Verificar que el PR incluya tests, que pasen, que cubran edge cases, que haya cobertura para el cambio.

### 4. Auditoría de seguridad
Multi-tenant, auth, secrets, data leaks, RLS. Si el proyecto no es multi-tenant, saltar a auditoría básica (secrets, data leaks) sin el checklist completo de RLS/auth multi-tenant.

### 5. Revisión de producto
¿Cumple con la spec? ¿Satisface la necesidad?

### 6. Validación Pre-Deploy (opcional, post-merge)
Si se va a deployar inmediatamente:
- Build check — `npm run build` sin errores
- Route regression — rutas públicas (200), protegidas (401/403)
- SEO audit — meta tags, OG images, sitemap
- API health — endpoints responden, auth funciona
- Performance — Lighthouse, lazy loading, bundle size
- Security scan — vulnerabilidades, secrets en diff
- Cleanup — console.logs, commented code, archivos temporales

### 7. Reporte
Hallazgos, bloqueantes, sugerencias.

### 8. Gate
Bloquea cierre si hay hallazgos críticos.

## Confidence Tagging

Cuando des una recomendación, análisis, o respuesta basada en datos incompletos, etiquetá tu nivel de confianza:

- 🟢 **Alta** — datos suficientes, contexto claro, patrón conocido
- 🟡 **Media** — algunas asunciones, Gonzo debería verificar inputs clave
- 🔴 **Baja** — unknowns mayores, tratar como direccional solamente

Esto aplica a: recomendaciones técnicas, estimaciones, debugging, decisiones de arquitectura, cualquier cosa donde no tengas certeza absoluta.

**Lección:** la transparencia sobre el nivel de confianza genera más confianza que un falso "estoy seguro".

## Outputs
- Reporte de revisión con hallazgos de testing, seguridad y producto
- Decisión: approve / changes requested / blocked
- (Opcional) Reporte de validación pre-deploy con Go/No-Go

## Helper Scripts

Scripts en `skills/review-quality/scripts/`:

| Script | Uso |
|---|---|
| `review-pr.sh [--pr <number>] [--output <file>]` | Corre build, tsc, lint, tests, y busca `console.log` y TODOs/FIXMEs en `src/`. Genera un reporte Markdown. Usar en la fase 2-4 para verificar calidad automatica del PR. |
| `security-scan.sh [--diff]` | Escanea secrets, hardcoded URLs, eval, y corre `npm audit`. Con `--diff` revisa solo cambios staged. Usar en la fase 4 (Auditoria de seguridad). |

Si se encuentran issues, delegar a [Task Execution](../task-execution) para fixes.

## Related Skills

- [Task Execution](../task-execution): Para implementar fixes post-review
- [Pre-Deploy QA](../pre-deploy-qa): Para validación post-merge pre-deploy
- [Accessibility Studio](../accessibility-studio): Para revisión de accesibilidad
