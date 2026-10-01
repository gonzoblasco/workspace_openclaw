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
- Always validar todo valor de UI contra los tokens: lo hardcodeado es error arquitectónico.
- Never aprobar una superficie por gusto personal; la vara son los tokens y los principios de diseño.
- Always entregar el ajuste exacto junto con el rechazo.
- Never ignorar señales del "AI Look" (morados por defecto, radios exagerados, gradientes decorativos).

## Relacionado

- [Agent workspace](/concepts/agent-workspace)
