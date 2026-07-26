---
name: "session-lifecycle"
metadata:
  category: "Workflow"
  tags:
    - sesion
    - ciclo
    - productividad
description: "Workflow de Session Lifecycle: ciclo de sesión completo. Reemplaza 4 skills de sesión."
user-invocable: false
---

# Workflow: Session Lifecycle

## Skills que reemplaza
- `session-closure`
- `session-closure-ritual`
- `context-management`
- `agent-dispatcher`

## Propósito
Gestión del ciclo de vida completo de una sesión de trabajo con IA.

## Cuándo usarlo
- Al iniciar una sesión de trabajo con IA (cargar contexto + memoria)
- Al cerrar una sesión (escribir HANDOFF, memory, CHANGELOG)
- Para spawnear sub-agentes según la tarea (fork vs isolated)
- Para convertir pendientes en tareas accionables y hacer commit del workspace

## Fases
1. **Inicio** — cargar contexto, memoria, handoff del proyecto activo
2. **Dispatcher** — spawnear sub-agentes según la tarea:
   - **fork**: cuando el sub-agente necesita el transcript actual (ej: continuar una investigación, analizar una conversación)
   - **isolated**: cuando es trabajo independiente (ej: buscar issues, leer docs, hacer tareas paralelas sin contexto compartido)
3. **Ejecución** — trabajo principal, decisiones, archivos tocados
4. **Cierre** — escanear sesión, escribir HANDOFF, memory, CHANGELOG
   - **Revisar sesiones anteriores del día:** antes de cerrar, leer los archivos `memory/YYYY-MM-DD-*.md` del día para asegurarse de que no hubo sesiones previas que el daily note resumido no capture. No confiar solo en el daily note ni en la memoria.
   - **Self-reflection obligatoria:** si hubo correcciones de Gonzo, cambios estructurales, o aprendizajes significativos, registrar en LEARNINGS.md antes de cerrar. No esperar a que Gonzo pregunte "¿revisamos lecciones?"
   - Si se modificó CONTRIBUTING.md, skills, o AGENTS.md, verificar que el cambio esté completo y no falten adaptaciones en skills relacionadas
5. **Tareas** — convertir pendientes en tareas accionables. Crear cron jobs para follow-ups, o escribir en TODO.md del proyecto. No dejar pendientes en el aire
6. **Commit** — commit + push del workspace (después de HANDOFF y memory, no antes)

## Outputs
- `projects/<slug>/.knowledge/HANDOFF.md`
- `memory/YYYY-MM-DD.md`
- Tareas creadas en el sistema (cron jobs o TODO.md)
- Workspace commiteado y pusheado

## Related Skills

- [Task Execution](../task-execution): Para ejecutar tareas dentro de la sesión
- [Knowledge Management](../knowledge-management): Para registrar aprendizajes de la sesión
