---
name: "session-lifecycle"
description: "Workflow de Session Lifecycle: ciclo de sesión completo. Reemplaza 4 skills de sesión."
---

# Workflow: Session Lifecycle

## Skills que reemplaza
- `session-closure`
- `session-closure-ritual`
- `context-management`
- `agent-dispatcher`

## Qué hace
Gestión del ciclo de vida completo de una sesión de trabajo con IA.

## Fases
1. **Inicio** — cargar contexto, memoria, handoff del proyecto activo
2. **Dispatcher** — spawnear sub-agentes según la tarea:
   - **fork**: cuando el sub-agente necesita el transcript actual (ej: continuar una investigación, analizar una conversación)
   - **isolated**: cuando es trabajo independiente (ej: buscar issues, leer docs, hacer tareas paralelas sin contexto compartido)
3. **Ejecución** — trabajo principal, decisiones, archivos tocados
4. **Cierre** — escanear sesión, escribir HANDOFF, memory, CHANGELOG
5. **Tareas** — convertir pendientes en tareas accionables. Crear cron jobs para follow-ups, o escribir en TODO.md del proyecto. No dejar pendientes en el aire
6. **Commit** — commit + push del workspace (después de HANDOFF y memory, no antes)

## Outputs
- `projects/<slug>/.knowledge/HANDOFF.md`
- `memory/YYYY-MM-DD.md`
- Tareas creadas en el sistema (cron jobs o TODO.md)
- Workspace commiteado y pusheado
