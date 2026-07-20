---
name: "workflow-review-quality"
description: "Workflow de Review & Quality: revisión pre-merge, testing y auditoría. Reemplaza pr-review, po-review, security-audit, agent-review."
---

# Workflow: Review & Quality

## Skills que reemplaza
- `pr-review`
- `po-review`
- `security-audit`
- `agent-review`

## Qué hace
Revisión de calidad antes de mergear o cerrar un ciclo. Incluye estrategia de testing, code review, auditoría de seguridad y validación pre-deploy opcional.

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

## Outputs
- Reporte de revisión con hallazgos de testing, seguridad y producto
- Decisión: approve / changes requested / blocked
- (Opcional) Reporte de validación pre-deploy con Go/No-Go
