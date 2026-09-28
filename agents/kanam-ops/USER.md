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

- Always respaldar `~/.openclaw/openclaw.json` antes de cualquier cambio de configuración o scheduler.
- Never editar el JSON de config a mano: usar `openclaw config set` o `openclaw config patch --stdin`.
- Always inspeccionar el estado actual (`config get`, `status`, `plugins list --json`) antes de cambiar un valor.
- Never escribir secretos en el JSON, en el chat ni en el historial del shell: guardarlos con la tool de secrets y cablearlos por ref.
- Always verificar el efecto real (status, channels status, el comando corriendo) antes de declarar un cambio exitoso.
- Never tocar `.env`, `*.db`, credenciales ni uploads sin respaldo previo: son datos locales irrecuperables.
- Prefer español para la prosa interna del workspace y inglés para todo lo que se publica en GitHub.
- Never usar guion largo (em dash/en dash): guion comun (-) siempre; escanear con `scripts/check_em_dash.py` antes de publicar.
- Always diffear contra el `.bak-*` más nuevo y nombrar cada campo cambiado antes de aceptar un baseline de drift.
- Never revertir ni tocar la configuración de otra máquina asumiendo que aplica: cada máquina tiene su propio `openclaw.json`.

## Relacionado

- [Agent workspace](/concepts/agent-workspace)
