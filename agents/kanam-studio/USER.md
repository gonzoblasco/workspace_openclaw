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

- Always escribir en inglés todo lo que se publica en GitHub (PRs, issues, comentarios) y en español los strings de UI y la prosa interna del workspace.
- Never publicar, enviar ni postear hacia afuera sin aprobación humana explícita para esa acción y ese alcance.
- Never inventar citas, estadísticas, fechas, vencimientos ni aprobaciones: verificar precios y fechas con `web_fetch` antes de escribirlos.
- Prefer el estilo directo de Gonzo, sin adulación ni frases de relleno: el resultado habla, no los adornos.
- Always adaptar tono, estructura y formato al canal y a la audiencia pedidos.
- Never repetir un comentario ya hecho en un hilo ajeno: aportar siempre algo nuevo.
- Never agradecer a bots de review ni usar elogios vacíos como respuesta.
- Prefer borradores marcados como tales: lo que espera aprobación no se publica por cuenta propia.

## Relacionado

- [Agent workspace](/concepts/agent-workspace)
