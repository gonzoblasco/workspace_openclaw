---
name: "task-execution"
metadata:
  category: "Workflow"
  tags:
    - tareas
    - implementacion
    - pr
description: "Workflow de ejecución de tareas: definir objetivo, planificar, implementar, verificar con feedback loop, PR y cerrar epic. Goal-oriented architecture."
user-invocable: false
---

# Workflow: Task Execution

## Propósito
Ejecución día a día de tareas: desde que se define una tarea hasta que se cierra el epic con PR, merge y CHANGELOG. Se relaciona con `build-scaffold` (post-scaffold) y `review-quality` (pre-merge).

## Cuándo usarlo
- Implementar una tarea o feature definida en un epic activo
- Planificar y desglosar trabajo en subtareas verificables
- Crear branch, implementar, testear y abrir PR
- Cerrar un epic con CHANGELOG, tags y lecciones aprendidas

## Principio: Goal-Oriented Architecture

Esta skill sigue los principios de **ADR-007 — Patrones de Agente Autónomo**:
- **Objetivos claros + restricciones explícitas**, no instrucciones paso a paso
- **Feedback loops rápidos** (acción → resultado → acción, sin demora humana)
- **Herramientas flexibles con límites explícitos**, no restricciones implícitas
- **Persistencia sin fatiga**: explorar más alternativas antes de escalar
- **Logging completo** para depuración y auditoría

## Fases

### 0. Goal Definition (NUEVA)
Antes de cualquier planificación, definir:
- **Objetivo:** ¿Qué queremos lograr? Una frase, concreta, medible.
- **Restricciones:** ¿Qué NO podemos hacer? (no tocar X, no modificar Y, no gastar más de Z)
- **Criterio de éxito:** ¿Cómo sabemos que está hecho?

No pasar a planificación hasta que objetivo y restricciones estén claros. Si el objetivo es difuso, pedir clarificación.

### 1. Intake
Leer contexto del epic activo, criterios de aceptación, archivos de `.knowledge/` relevantes. No empezar a escribir código sin entender las restricciones.

### 2. Planificación
Desglosar tarea en subtareas de 2-5 minutos, cada una con verificación clara ("¿cómo sé que está hecho?"). Máximo 10 subtareas por plan. Si son más, dividir en múltiples planes.

### 3. Branch
```bash
git checkout main && git pull origin main
git checkout -b task/E[N]-T[NN]-[descripcion-corta]
```

### 4. Implementación
Código + tests + tipos. Commits atómicos: un cambio por commit, no acumular todo al final.

### 5. Auto-Validation Loop (NUEVA — reemplaza Verificación)
Después de cada subtarea completada, ejecutar feedback loop rápido:
1. **Build** — `npm run build` (debe pasar)
2. **Tests** — `npx vitest run` (debe pasar)
3. **Auto-evaluación** — ¿Cumple el objetivo de la subtarea? ¿Violé alguna restricción?
4. **Si falla** → corregir y repetir el loop. No avanzar a la siguiente subtarea con fallos.
5. **Si pasa** → avanzar.

Este loop se ejecuta a velocidad máquina. No esperar validación humana para cada paso.

### 6. PR
PR estructurado con:
- Título: `feat|fix|refactor(scope): descripción`
- Body: qué hace, cambios principales, cómo testear, checklist
- Review automático antes de mergear

### 7. Merge
Merge a main preservando historial (`--no-ff`). No eliminar la branch (referencia histórica).

### 8. Cierre de Epic (cuando todas las tasks están completas)
- CHANGELOG: mover `[Unreleased]` a nueva versión semver
- Tags: `git tag -a E[N]-complete`
- Lecciones aprendidas documentadas
- STATUS.md actualizado

## Outputs
- Plan de tarea en `{task-slug}.md`
- Branch con commits atómicos
- PR con descripción estructurada
- Epic cerrado con CHANGELOG y tags

## Verify Implementation, Not Intent

Cuando cambies cómo funciona algo:

1. Identificá los **componentes arquitectónicos**, no solo el texto
2. Cambiá el **mecanismo real**, no solo la descripción
3. Verificá **observando comportamiento**, no solo leyendo la config

**Trampa común:** decís "✅ Listo, actualicé la config" pero solo cambiaste el texto del prompt, no el sessionTarget ni el kind del cron. El sistema sigue haciendo lo mismo, solo que con palabras distintas.

**La regla:** cambios de texto ≠ cambios de comportamiento. Verificá siempre.

## Related Skills

- [Build & Scaffold](../build-scaffold): Para scaffolding inicial del proyecto
- [Review & Quality](../review-quality): Para revisar antes de mergear
- [Pre-Deploy QA](../pre-deploy-qa): Para validar post-merge pre-deploy
