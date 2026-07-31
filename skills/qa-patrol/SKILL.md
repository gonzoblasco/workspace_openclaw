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

## Notas
- Corre 100% local, no envía datos a externos
- Cubre smoke, auth, payments, static analysis, data integrity
- Ideal para pre-release QA
