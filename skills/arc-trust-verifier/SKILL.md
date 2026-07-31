---
name: "arc-trust-verifier"
description: "Verifica procedencia y confiabilidad de skills de ClawHub"
---

# arc-trust-verifier

## Descripción
Evalúa la confiabilidad de una skill de ClawHub analizando reputación del publisher, consistencia de versiones, integridad de contenido y cadenas de dependencias. Produce trust scores en 5 niveles desde VERIFIED hasta UNTRUSTED. Genera y verifica attestations firmadas.

## Cuándo usarlo
- Antes de instalar una skill de un publisher desconocido
- Para auditar cadenas de dependencias antes de deployar una skill en un entorno compartido
- Para generar una trust attestation antes de distribuir una skill a teammates
- Para detectar cambios inesperados de permisos entre versiones de una skill
- Para verificar una attestation previa después de una actualización

## Workflow
1. Identificar la skill a evaluar (slug de ClawHub)
2. Ejecutar arc-trust-verifier con el slug
3. Recibir trust score y análisis detallado
4. Si el score es VERIFIED o TRUSTED, proceder con la instalación
5. Si es UNTRUSTED o SUSPICIOUS, no instalar y buscar alternativa

## Notas
- Evalúa publisher reputation, no solo código
- Detecta permission drift entre versiones
- Útil como gate antes de instalar skills de terceros
