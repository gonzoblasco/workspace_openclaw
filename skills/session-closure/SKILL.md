---
name: "session-closure"
description: "Cerrar sesión guardando todo: escanea conversación, escribe HANDOFF/memory/CHANGELOG, commitea cambios en curso y workspace, y muestra resumen."
---

# session-closure

Ritual automatizado de cierre de sesión. Cuando el usuario dice "cerremos sesión", "cerramos", "guardemos esto", o similar, esta skill se ejecuta para capturar todo el valor de la conversación antes de que se pierda.

## Cuándo usarla

- El usuario dice "cerremos sesión", "cerramos", "guardemos esto", "hagamos el cierre"
- El usuario dice "tomá nota de esto y cerramos"
- Al finalizar una sesión de trabajo significativa

## Flujo

### Fase 0: Detectar cambios en curso

1. Identificar el proyecto activo de la conversación (el que más se tocó).
2. Si hay un proyecto activo con código:
   - Correr `git status` en `projects/<slug>/code/`
   - Si hay cambios sin commit (modified, untracked):
     - `git add -A`
     - `git commit -m "wip: <descripción corta de lo que se estaba haciendo>"`
     - Si hay branches sin upstream, preguntar al usuario si quiere pushear
3. Si hay cambios en docs del proyecto (`projects/<slug>/docs/`):
   - No commitear automáticamente (van con el cierre de sesión)

### Fase 1: Escanear la sesión

Revisar la conversación actual para identificar:

- **Proyectos tocados** — ¿qué proyectos se mencionaron o modificaron?
- **Decisiones tomadas** — ¿qué se decidió? (arquitectura, prioridades, cambios)
- **Archivos creados/modificados** — specs, código, docs, configs
- **Lecciones aprendidas** — ¿qué descubrimos que valga la pena recordar?
- **Pendientes** — ¿qué quedó sin terminar? ¿próximos pasos?
- **Skills creadas/actualizadas** — ¿se tocó alguna skill?

### Fase 1.5: Convertir Pendientes en Tareas (NUEVO)

**Objetivo:** Transformar la lista de "Pendientes" de texto plano a tareas accionables en el sistema.

1. **Extraer candidatos a tarea:**
   - Por cada pendiente identificado, crear un objeto estructurado:
     ```json
     {
       "title": "<título corto y accionable>",
       "context": "<proyecto o área relevante>",
       "priority": "<High|Medium|Low>"
     }
     ```
   - Ejemplo: "PENDIENTE #1: Configurar DEEPSEEK_API_KEY..." → `{ "title": "Configurar API Keys", "context": "SoporteML v2", "priority": "High" }`

2. **Spawn sub-agente para creación de tareas:**
   - Usar `sessions_spawn` con `taskName="create_tasks_from_closure"`
   - Prompt: "Crear las siguientes tareas en el sistema taskflow: <lista de candidatos JSON>"
   - Esperar completitud con `sessions_yield`

3. **Capturar IDs generadas:**
   - El sub-agente debe devolver los IDs de tareas creadas (ej: `TASK-902`, `TASK-903`)
   - Estos IDs se usarán en el resumen final (Fase 4) en lugar del texto plano

### Fase 2: Escribir archivos

Para cada proyecto tocado:

1. **`projects/<slug>/docs/HANDOFF.md`** — estado actual del proyecto, qué se hizo, qué falta, próximos pasos. Si el proyecto es un fork externo (create-next-stack, ui, router, query, etc.), NO escribir HANDOFF.md (lección aprendida: los HANDOFF de forks externos no van al workspace).
2. **`projects/<slug>/docs/LEARNINGS.md`** — lecciones específicas del proyecto (si las hay).

Archivos globales:

3. **`memory/YYYY-MM-DD.md`** — resumen de la sesión: qué pasó, qué se decidió, archivos tocados, skills creadas/actualizadas. Siempre escribir (incluso si es breve).
4. **`MEMORY.md`** — solo si hay lecciones transversales que merezcan entrada permanente (no escribir placeholders vacíos).
5. **`CHANGELOG.md`** — solo si se crearon o modificaron features significativas (no por cambios menores).

Reglas:
- No escribir placeholders vacíos. Si no hay nada que agregar a un archivo, no tocarlo.
- MEMORY.md y CHANGELOG.md se leen antes de escribir para no duplicar ni pisar contenido.

### Fase 3: Commit + push del workspace

1. `cd /Users/gonzoblasco/.openclaw/workspace`
2. `git add -A`
3. `git commit -m "sesión: <YYYY-MM-DD> - <resumen corto de 1 línea>"`
4. `git push`

### Fase 4: Mostrar resumen

Mostrar al usuario:

```
📋 Cierre de sesión — <fecha>

Proyectos tocados:
- <proyecto>: <qué se hizo>

Decisiones registradas:
- <decisión 1>
- <decisión 2>

Archivos actualizados:
- <archivo 1>
- <archivo 2>

Skills creadas/actualizadas:
- <skill 1>

Tareas creadas:
- TASK-<id> (<título>) — <prioridad>
- TASK-<id> (<título>) — <prioridad>

✅ Todo guardado, commiteado y tareas generadas.
```

## Notas

- Si la sesión fue breve o sin contenido relevante, preguntar antes de ejecutar el ritual completo.
- Si hay cambios sin commit en el proyecto activo, commitearlos como "wip" antes de todo lo demás para no perder trabajo en curso.
- Los forks externos (create-next-stack de akd-io, ui de shadcn, router/query de TanStack, etc.) NO reciben HANDOFF.md en el workspace. Sus docs de sesión van en `projects/<slug>/docs/` pero no se commitean al workspace (son referencias locales).
- Si el usuario cancela el cierre, no hacer nada.
