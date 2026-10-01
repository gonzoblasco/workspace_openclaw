# USER.md - Modelo de Usuario

Guarda preferencias estables y hechos de perfil como directivas que guíen sesiones futuras.

Una directiva por entrada:

```md
<!-- observed: YYYY-MM-DD | status: active -->

- Prefer concise progress updates during implementation work.
```

- Empezar cada directiva con un imperativo: `Always`, `Never` o `Prefer`.
- Registrar la fecha de observación y `active` o `superseded` en la línea de metadatos.
- Guardar acá el estilo de comunicación estable y el contexto del ecosistema. Los hechos y decisiones durables que no son de perfil van en `MEMORY.md`.

## Directivas

<!-- observed: 2026-10-01 | status: active -->

- Prefer español para la prosa interna del workspace e inglés para todo lo que se publica en GitHub.
- Always trazar el plan en `.session_plan.json` y mantenerlo como única fuente de verdad del progreso.
- Never empezar un turno sin leer el plan de sesión actual.
- Always asignar roles en el orden correcto y evitar convocar al equipo para tareas triviales.
- Never saltar los filtros del Auditor y el Critic en un entregable.

## Relacionado

- [Agent workspace](/concepts/agent-workspace)
