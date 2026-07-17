---
name: "adr-sync"
description: "Mantener ADRs actualizados cuando cambian decisiones de producto o tecnología."
author: "OpenClaw Skill Workshop"
---

# adr-sync

## Overview

Los Architecture Decision Records (ADRs) son la memoria institucional de las decisiones de producto y tecnología. Pero se desactualizan rápido: un MVP recortado, un cambio de stack, una decisión de negocio que pivota, y los ADRs quedan documentando un pasado que ya no refleja la realidad.

Esta skill detecta ADRs desactualizados, los actualiza con el estado correcto, y crea nuevos ADRs para decisiones que aún no están documentadas.

## Cuándo ejecutarla

- Después de cualquier cambio significativo en el código (refactors, cambios de stack, nuevas dependencias)
- Después de cambios en la documentación de producto (BRIEF, DEFINITION, ROADMAP)
- Al cerrar un epic o milestone
- Antes de un handoff o session closure
- Periódicamente como parte de una healthcheck del proyecto

## Flujo

### 1. Listar todos los ADRs existentes

Buscar archivos en `docs/` que coincidan con patrones de ADR:
- `docs/adr/*.md`
- `docs/decisions/*.md`
- `docs/*.adr.md`
- Cualquier archivo con frontmatter que incluya `status: ACEPTADO|RECHAZADO|REEMPLAZADO|OBSOLETO|VIGENTE`

Para cada ADR encontrado, extraer:
- Título y número
- Estado actual
- Fecha de la última actualización
- Decisión documentada (resumen)
- Contexto y motivación

### 2. Verificar vigencia de cada ADR

Para cada ADR, determinar si la decisión sigue vigente:

**Fuentes de verdad a consultar:**
- `docs/BRIEF.md` — requisitos y alcance actual del producto
- `docs/DEFINITION.md` — definición funcional vigente
- `docs/ROADMAP.md` — hoja de ruta y prioridades
- `docs/STATUS.md` — estado actual del proyecto
- `code/` — el código fuente (dependencias reales, configuración, stack)
- `package.json`, `composer.json`, `Cargo.toml`, etc. — dependencias declaradas
- Archivos de configuración de infraestructura (Dockerfile, docker-compose, CI configs)

**Indicadores de desactualización:**
- La tecnología mencionada ya no aparece en `package.json` o configs
- El requisito que motivó la decisión ya no existe en BRIEF/DEFINITION
- Hay un ADR posterior que reemplaza explícitamente a este
- El código muestra un approach diferente al documentado
- El ROADMAP indica un cambio de dirección incompatible

### 3. Actualizar ADRs desactualizados

Si una decisión ya no es vigente, actualizar el ADR con:

```yaml
---
status: OBSOLETO|REEMPLAZADO
updated: YYYY-MM-DD
superseded_by: ADR-NNN  # si aplica
---
```

**Campos a modificar:**
- **Estado**: cambiar a `OBSOLETO` (la decisión ya no aplica) o `REEMPLAZADO` (hay un nuevo ADR que la reemplaza)
- **Fecha de actualización**: la fecha actual
- **Contexto del cambio**: párrafo explicando por qué cambió la decisión
- **Nueva decisión**: si el ADR se reemplaza, enlazar al nuevo ADR

**Formato de la actualización:**

```markdown
## Actualización (YYYY-MM-DD)

**Estado anterior:** ACEPTADO
**Estado nuevo:** OBSOLETO

**Contexto del cambio:**
[Explicación de por qué la decisión original ya no aplica]

**Implicaciones:**
- [Impacto en el código]
- [Impacto en la documentación]
- [Acciones necesarias]
```

### 4. Crear nuevos ADRs para decisiones no documentadas

Si se detecta una decisión significativa que no tiene ADR asociado:

1. Identificar el contexto: qué se decidió, cuándo, por quién, por qué
2. Buscar en el código, commits, o discusiones la motivación
3. Crear un nuevo archivo `docs/adr/NNN-decision-slug.md` con:

```markdown
---
number: NNN
title: "[título descriptivo]"
status: VIGENTE
date: YYYY-MM-DD
deciders: [nombre de quien decidió]
---

# ADR-NNN: [título]

## Contexto

[Descripción del problema o situación que motivó la decisión]

## Decisión

[Qué se decidió hacer]

## Consecuencias

- [Consecuencia positiva 1]
- [Consecuencia positiva 2]
- [Consecuencia negativa / trade-off 1]
- [Consecuencia negativa / trade-off 2]

## Estado

VIGENTE
```

### 5. Reportar resultados

Al finalizar, producir un resumen con:

```
## Resumen de sincronización de ADRs

### ADRs actualizados
- ADR-001: Cambio de estado ACEPTADO → OBSOLETO (decisión de stack ya no aplica)
- ADR-003: Cambio de estado ACEPTADO → REEMPLAZADO por ADR-005

### ADRs nuevos creados
- ADR-005: Migración de SQLite a PostgreSQL

### ADRs sin cambios
- ADR-002: Autenticación con Supabase (VIGENTE)
- ADR-004: Despliegue en Vercel (VIGENTE)
```

## Ejemplo real: create-with-ai

En el proyecto **create-with-ai** se crearon 3 ADRs durante la fase de planificación:

| ADR | Decisión original | Estado después del MVP recortado |
|-----|-------------------|----------------------------------|
| ADR-001 | Usar SQLite para almacenamiento local | **OBSOLETO** — el MVP eliminó el almacenamiento local |
| ADR-002 | Integración con OpenAI para generación de contenido | **VIGENTE** — sigue siendo el core del producto |
| ADR-003 | Despliegue multi-región con Docker Swarm | **OBSOLETO** — el MVP usa Vercel + serverless |

La skill detectó que ADR-001 y ADR-003 ya no se correspondían con el código ni con BRIEF.md, los marcó como OBSOLETOS, y agregó contexto del cambio explicando que el alcance del MVP se redujo.

## Output

La skill produce:
1. Lista de ADRs actualizados (con estado anterior y nuevo)
2. Lista de ADRs nuevos creados
3. Lista de ADRs que siguen vigentes (sin cambios)
4. Un archivo `docs/adr/CHANGELOG.md` o entrada en `CHANGELOG.md` del proyecto documentando la sincronización

## Integración con otras skills

- **session-closure**: ejecutar adr-sync antes de cerrar una sesión para dejar los ADRs al día
- **project-healthcheck**: incluir adr-sync como paso de verificación de salud del proyecto
- **sdd-brownfield**: después de generar specs as-built, ejecutar adr-sync para reflejar decisiones reales
