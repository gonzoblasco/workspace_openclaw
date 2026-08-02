---
name: "background-execution"
description: "Patrones para ejecutar tareas en background: exec + process, parallel worktrees, auto-notify, isolated workspaces"
metadata:
  category: "Workflow"
  tags:
    - background
    - procesos
    - paralelismo
    - exec
    - process
user-invocable: false
---

# Workflow: Background Execution

## Propósito
Ejecutar tareas largas, batch, o paralelas en background usando `exec` + `process`, con monitoreo, notificación al completar, y aislamiento de workspace. Complementa a `task-execution` para tareas que no requieren interacción constante.

## Cuándo usarlo
- Tareas largas (>30s) que no necesitan supervisión constante
- Batch processing (múltiples archivos, reviews, fixes)
- Tareas paralelas independientes (un proceso por issue, por PR, por módulo)
- Cualquier proceso interactivo que requiera PTY (coding agents, TUIs, REPLs)
- Cuando necesitás lanzar algo y que avise cuando termine sin esperar heartbeat

## Principios

1. **Nunca esperar pasivamente.** Si una tarea va a tardar, lanzarla en background y seguir con otra cosa.
2. **Siempre aislar.** Cada tarea en su propio directorio temporal o git worktree. Nunca tocar el repo principal sin approval explícito.
3. **Siempre notificar.** Toda tarea background debe terminar con un wake event. No dejar que el usuario pregunte "¿ya terminó?".
4. **PTY para interactivos, no para batch.** Procesos interactivos (coding agents, prompts) → `pty:true`. Scripts batch → `pty:false` (default).

## Patrones

### Patrón 1: Lanzar y Monitorear

El patrón base para cualquier tarea background:

```yaml
# 1. Lanzar
exec(command: "...", pty: true, background: true, workdir: "/tmp/task-xyz")

# 2. Monitorear (cuando quieras ver estado)
process(action: poll, sessionId: "<id>")

# 3. Ver logs
process(action: log, sessionId: "<id>", offset: 0, limit: 50)

# 4. Enviar input (si el proceso pregunta algo)
process(action: submit, sessionId: "<id>", text: "y")

# 5. Matar (si se cuelga)
process(action: kill, sessionId: "<id>")
```

**Regla:** después de lanzar, no hacer poll loop. Seguir con otra cosa y dejar que el completion wake avise.

### Patrón 2: Aislar en Temp Dir

Para tareas que necesitan un workspace limpio:

```yaml
# 1. Crear temp dir
exec(command: "mktemp -d")
# → devuelve /tmp/tmp.XXXXX

# 2. Clonar / preparar en ese dir
exec(command: "git clone <url> /tmp/tmp.XXXXX/repo", workdir: "/tmp/tmp.XXXXX")

# 3. Trabajar ahí
exec(command: "npm run build", workdir: "/tmp/tmp.XXXXX/repo", background: true)

# 4. Al terminar, limpiar
exec(command: "trash /tmp/tmp.XXXXX")
```

**Regla:** siempre limpiar al terminar. Usar `trash` (no `rm -rf`) por si algo sale mal.

### Patrón 3: Git Worktree para Tareas Paralelas

Para trabajar en múltiples issues/PRs en paralelo sin contaminar el repo:

```yaml
# 1. Crear worktree por tarea
exec(command: "git worktree add -b fix/issue-78 /tmp/issue-78 main")
exec(command: "git worktree add -b fix/issue-79 /tmp/issue-79 main")

# 2. Lanzar proceso en cada worktree
exec(command: "<comando>", workdir: "/tmp/issue-78", background: true, pty: true)
exec(command: "<comando>", workdir: "/tmp/issue-79", background: true, pty: true)

# 3. Monitorear todos
process(action: list)

# 4. Al terminar, mergear y limpiar
exec(command: "cd /repo/main && git merge fix/issue-78")
exec(command: "git worktree remove /tmp/issue-78")
```

**Regla:** un worktree por tarea. Nombrar branches descriptivamente. Mergear solo después de verificar que cada tarea está completa.

### Patrón 4: Auto-Notify al Completar

Para que una tarea background avise inmediatamente cuando termina:

```yaml
# Incluir al final del comando o script:
cron(action: wake, text: "✅ Tarea X completada: [resumen]", mode: "now")
```

**Regla:** toda tarea background DEBE terminar con un wake event. No confiar en heartbeats ni en que el usuario va a preguntar.

**Formato del texto:** incluir qué tarea, resultado (éxito/fallo), y qué sigue. Ej: "✅ Batch review completado: 3 PRs revisados, 1 con cambios solicitados. Revisar PR #78."

### Patrón 5: Parallel Batch con Sessions Spawn

Para tareas que requieren contexto conversacional (reviews, análisis):

```yaml
# Lanzar sub-agentes en paralelo
sessions_spawn(task: "Revisar PR #78 en <repo>", context: "isolated")
sessions_spawn(task: "Revisar PR #79 en <repo>", context: "isolated")

# Esperar resultados
sessions_yield()
```

**Regla:** `sessions_spawn` para tareas que necesitan razonamiento. `exec` + `process` para tareas que son puro comando (build, test, batch script).

### Patrón 6: submit vs write — Input a Procesos

Cuando un proceso background espera input:

| Acción | Qué hace | Cuándo usarlo |
|---|---|---|
| `process(action: submit, text: "y")` | Escribe texto + Enter | Respuestas a prompts ("¿Continuar? [y/N]") |
| `process(action: write, data: "texto")` | Escribe texto crudo (sin Enter) | Streaming, input parcial |
| `process(action: send-keys, keys: ["ctrl+c"])` | Envía combinación de teclas | Interrumpir, salir de modo insert |

## Reglas de PTY

| Tipo de proceso | pty | Razón |
|---|---|---|
| Coding agent (Codex, Claude Code) | `true` | Son TUIs interactivos, sin PTY se cuelgan |
| Script batch (build, test, lint) | `false` | No necesita terminal, ahorra recursos |
| REPL (node, python, psql) | `true` | Espera input interactivo |
| git command | `false` | Batch, no interactivo |
| npm/pnpm command | `false` | Batch, salida estructurada |

## Integración con task-execution

Cuando una tarea de `task-execution` tiene pasos que son largos o paralelizables:

1. **Planificar** normalmente en `task-execution`
2. **Los pasos batch/paralelos** se ejecutan con estos patrones
3. **Monitorear** con `process` o esperar wake events
4. **Continuar** cuando todos los pasos background completaron

## Outputs
- Procesos lanzados y monitoreados
- Resultados consolidados al completar
- Wake events de notificación
- Temp dirs / worktrees limpiados

## Related Skills

- [Task Execution](../task-execution): Para el workflow completo de tareas
- [Session Lifecycle](../session-lifecycle): Para handoffs y cierre de sesión
- [Debug Investigation](../debug-investigation): Para debugging de procesos que fallan
