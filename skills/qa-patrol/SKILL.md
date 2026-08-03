---
name: "qa-patrol"
description: "Automated QA testing con browser: smoke tests, auth, payments, data integrity"
---

# qa-patrol

## Descripción
Ejecuta tests automatizados de browser contra aplicaciones web: smoke checks, auth flows, payment flows, static code analysis, y data integrity comparisons. Atrapa cross-platform issues, auth state bugs, y integration failures. Todo corre local sin enviar datos a servidores externos.

## Cuándo usarlo
- Para testear login y logout flows en staging antes de shippear
- Para verificar páginas de Stripe checkout por console errors y redirect failures
- Para verificar persistencia de sesión de Supabase después de un page refresh
- Para escanear source code por hardcoded API keys o secrets expuestos
- Para comparar resultados de DB con lo que el UI muestra realmente

## Workflow
1. Configurar las URLs y credenciales de test
2. Ejecutar qa-patrol con los tests deseados
3. Revisar el reporte de resultados
4. Corregir issues encontrados
5. Re-ejecutar para verificar fixes

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `pre-deploy-qa/scripts/pre-deploy-check.sh` | Smoke tests de endpoints, build, npm audit. Usar como gate previo al deploy. |
| `pre-deploy-qa/scripts/smoke-test.sh <url>` | Smoke tests rapidos de endpoints criticos. Usar en el paso 2. |
| `observability/scripts/health-check.sh` | Verifica salud basica del sistema. Usar en el paso 2. |
| `engineering-governance/scripts/secret-scan.sh` | Escanear hardcoded API keys o secrets. Usar para static code analysis. |
| `review-quality/scripts/security-scan.sh` | Security scan adicional del codigo. Usar para static code analysis. |
| `accessibility-studio/scripts/a11y-audit.sh` | Validar accesibilidad en paginas testeadas. |

## Notas
- Corre 100% local, no envía datos a externos
- Cubre smoke, auth, payments, static analysis, data integrity
- Ideal para pre-release QA
