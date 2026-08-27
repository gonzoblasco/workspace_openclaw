---
name: compaction-domain-aware
metadata:
  category: "Context"
  tags:
    - compactacion
    - contexto
    - domain
    - memoria
description: "Compactacion de contexto con conciencia de dominio: usa tiers de prioridad (Tier 0-4) para decidir que preservar al compactar una sesion. Preserva ADRs, arquitectura, API contracts y seguridad (Tier 0) y descarta ruido (Tier 4). Portado del concepto DomainAwareCompaction (ClawHub)."
user-invocable: false
---

# Compaction Domain-Aware

Compactar el contexto de una sesion **preservando lo que importa para el dominio actual**, en vez de compactar a ciegas. Portado del concepto del plugin DomainAwareCompaction (ClawHub), adaptado a nuestro stack.

## Cuando usar

- Antes de compactar una sesion (cerca del limite de contexto, ~60%+).
- Al armar el working buffer / snapshot de compactacion.
- Cuando la sesion mezcla trabajo de software con ruido operativo.

## Los Tiers de Prioridad

Cada dominio define 5 niveles de que preservar al compactar:

| Tier | Importancia | Que hacer al compactar |
|---|---|---|
| **Tier 0** | Critico | Preservar completo, no comprimir |
| **Tier 1** | Alto | Preservar casi entero, compresion minima |
| **Tier 2** | Medio-alto | Comprimir moderado, mantener nucleo |
| **Tier 3** | Medio | Comprimir fuerte, mantener resumen |
| **Tier 4** | Bajo | Descartar o comprimir fuerte |

## Dominios relevantes (nuestro stack)

### Dominio: Software Engineering (default)
**Tier 0 (preservar completo):**
- Decisiones de arquitectura y ADRs
- API contracts e interfaces publicas
- Security policies y control de acceso
- Invariantes del sistema
- Criterios de aceptacion de las unidades en curso

**Tier 1 (casi completo):**
- Specs tecnicas, parametros clave, schemas de datos
- Decisiones de diseno de la unidad actual

**Tier 2 (moderado):**
- Detalles de implementacion soporte, configs
- Ejemplos de uso (mantener 1-2)

**Tier 3 (comprimir):**
- Background, discusiones de alternativas, contexto extendido

**Tier 4 (descartar):**
- Chit-chat, confirmaciones obvias, ruido operativo
- Contenido repetido, notas temporales, detalles triviales

### Dominio: Accesibilidad (a11y)
**Tier 0:** hallazgos de a11y sin resolver, decisiones de ARIA, criterios WCAG aplicados, ADRs de a11y.
**Tier 4:** discusiones de estetica, cambios de color cosméticos sin impacto funcional.

### Dominio: OSS / Contribucion
**Tier 0:** estado de PRs abiertos, decisiones de colaboracion, lecciones de feedback, que repo/issue es cual.
**Tier 4:** historial de navegacion, reads de docs sin conclusion.

### Dominio: Supabase / backend
**Tier 0:** schema de DB, RLS policies, decisiones de auth, migraciones pendientes.
**Tier 4:** detalles de logs, configuracion temporal.

## Proceso

1. **Identificar el dominio** de la sesion (software, a11y, oss, supabase, o general).
2. **Antes de compactar**, revisar que el working buffer / snapshot capture los items Tier 0 del dominio (ADRs, API contracts, arquitectura, invariantes, criterios de aceptacion).
3. **Al armar el resumen** de compactacion, asegurar que los Tier 0 esten textualmente preservados (no solo resumidos).
4. **Descartar** Tier 4 (chit-chat, ruido) - no llenar el contexto con basura.
5. **Dejar nota** en el daily de que se compacto con X tiers preservados.

## Relacion con el sistema existente

- Complementa el **working buffer** de session-lifecycle: el buffer captura lo crudo, esta skill decide que es Tier 0 (lo que el buffer debe asegurar).
- Complementa el plugin **compaction-context** (que reinyecta las ultimas N mensajes): esta skill garantiza que los items Tier 0 esten en el buffer/note, no solo los ultimos mensajes.
- Complementa **DREAMS.md**: al consolidar, los Tier 0 promovidos a MEMORY.md/LEARNINGS.md.

## Nota

La skill es una guia para Kanam, no un plugin automatico. Kanam aplica los tiers al decidir que conservar al compactar / armar el buffer.

## Related

- [Session Lifecycle](../session-lifecycle): manejo del contexto y compactacion.
- [Context Engineering](../context-engineering): curar el contexto del agente.
- [Knowledge Management](../knowledge-management): DREAMS y consolidacion de memoria.
