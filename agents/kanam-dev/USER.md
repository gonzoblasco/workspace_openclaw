# USER.md - Modelo de Usuario

Guarda preferencias estables y hechos de perfil como directivas que guíen sesiones futuras.

Una directiva por entrada:

```md
<!-- observed: YYYY-MM-DD | status: active -->

- Prefer concise progress updates during implementation work.
```

- Empezar cada directiva con un imperativo: `Always`, `Never` o `Prefer`.
- Registrar la fecha de observación y `active` o `superseded` en la línea de metadatos.
- Cuando una preferencia cambia, marcar la anterior como `superseded` y reescribir la directiva activa en su lugar. Nunca dejar dos directivas activas contradictorias.
- Guardar acá el estilo de comunicación estable, relaciones y contexto de proyecto activo. Los hechos y decisiones durables que no son de perfil van en `MEMORY.md`.
- Guardar este archivo en la raíz del workspace como `USER.md`. Se carga en cada sesión con un presupuesto separado de 4.000 caracteres.

## Directivas

<!-- observed: 2026-09-26 | status: active -->

- Prefer español para la prosa interna del workspace y inglés para todo lo que se publica en GitHub (commits, PRs, issues, comentarios).
- Prefer código y su documentación entregados juntos: un cambio sin su ADR/README cuando corresponde está incompleto.
- Always correr la verificación real (tests, build, lint, el comando) antes de afirmar que algo funciona.
- Never adoptar ni citar una dependencia o tecnología por precedente: primero qué hace, después por qué se elige hoy, después la decisión explícita.
- Prefer slices verticales: un cambio verificable a la vez en vez de una feature entera en una pasada.
- Never tocar `.env`, `*.db`, tokens ni uploads sin respaldo previo: son datos locales irrecuperables.
- Always pedir aprobación humana explícita antes de publicar, borrar, desplegar o salir del flujo del equipo.

## Relacionado

- [Agent workspace](/concepts/agent-workspace)
