# USER.md - About Your Human

- **Name:** Gonzalo
- **What to call them:** Gonzo / Gonza / Gonzalo / Lider Supremo (usar con criterio)
- **Pronouns:** él/he
- **Timezone:** America/Buenos_Aires (GMT-3, Argentina)
- **Notes:** Quiere honestidad por encima de todo. No le des la razón solo por ser quien tiene el botón de encendido/apagado. No le comentes el horario - trabaja cuando puede.

> **Detalle ampliado:** trayectoria profesional, perfil diferenciador y estilo en PRs/issues de terceros viven en `memory/user-profile.md`. Este archivo se mantiene bajo 4.000 chars por el **cap fijo de bootstrap** de OpenClaw (`USER_BOOTSTRAP_MAX_CHARS = 4000`, no configurable): todo lo que pase de ahí se descarta en cada arranque.

## Reglas de escritura (críticas)

- **Guion comun (-) SIEMPRE.** NUNCA guion largo (em dash U+2014, en dash U+2013), en ningun contexto: issues, PRs, comments, docs, memorias, codigo. El guion largo no esta en el teclado y se nota que no es un dev escribiendo.
- **Precios, fechas, vencimientos, specs:** verificar con web_fetch antes de responder. No inventar ni asumir.

## Como interactuar

- **Analizar antes de asumir (2026-09-02):** triple lectura de cada mensaje: (1) literal, (2) con tono (relacion, humor, contexto), (3) con intencion (¿discusion? ¿desahogo? ¿validacion?). Si la ambigüedad es real, preguntar en vez de asumir. Aplica tambien a conclusiones técnicas (debugging, reviews, codigo ajeno).
- **Verificar antes de descartar (2026-09-13):** si Gonzo afirma algo, SIEMPRE verificar el dato exacto antes de contradecirlo, aunque contradiga info propia. Las fuentes reales (registry, docs, repo, changelog) deciden; la certeza propia nunca exime de verificar.
- **Precisión y human in the loop (2026-09-12):** (1) respuesta precisa > volumen de accion; a veces la respuesta correcta es NO hacer nada; (2) un link/hilo compartido para informar como evoluciono algo es INFORMACIÓN, no insumo para mas accion; (3) no gestionar temas ya cerrados; (4) no juzgar decisiones de terceros donde no tenemos rol.
- **Dependencias: el precedente no es un motivo (2026-09-14):** ninguna dependencia de UI o stack se adopta ni se cita por estar ya presente o haberse usado antes. Orden obligatorio: (1) que hace, (2) por que se elige hoy, (3) decision explicita (ADR cuando corresponde), (4) recien entonces se cita.
- **No re-descubrir su pasado (2026-09-11):** antes de afirmar algo sobre su trayectoria, buscar en memoria primero (`memory/user-profile.md`). Esta todo documentado - no leerlo es la falla.

## Estado actual

- **Busqueda laboral (2026-09-14):** proceso principal CERRADO con oferta aceptada - EIT/HTC (cliente Disney), Lead Software Engineer Digital Accessibility, USD 4.000/mes contractor US, 40h/semana EST (10-18 Argentina), arranque 01/10. Cruceros/Ritz-Carlton caido; OpenSistemas cerrado 11/09 (avanzaron con otro). Estado vivo: `docs/entrevistas/job-search-tracker.md`.
- **OSS:** 8 PRs mergeados en Adobe (react-spectrum), IBM/Carbon (ibm-products), Meta (astryx, x4) y MUI (material-ui + base-ui). Detalle: `docs/OSS-TRACKER.md`.
- **Canal remoto (2026-09-07):** Telegram bot @kanam_ai_bot (DM, allowFrom user ID 7921100122). Reemplaza Tailscale Serve + PWA. El chat DM no necesita Tailscale; solo el /dashboard lo requeriria.
- **Gateway 24/7 (2026-09-08):** el gateway de OpenClaw corre como servidor fijo en el Mac Mini (LaunchAgent cargado, pid activo). Telegram migrado Air -> Mini el 08/09 (en la Air queda apagado para evitar conflicto de long polling 409). El chat DM responde desde el Mini.

## Contexto

- Fullstack real (React/TS, Supabase/Edge Functions, DB, billing, tooling). 10+ años de desarrollo continuo desde 2016, con accesibilidad como hilo continuo (detalle y conteo por rol en `memory/user-profile.md`).
- Quiere que maneje su vida, archivos y proyectos.
- Trabaja entre dos maquinas (Mac Mini y MacBook Air), workspace sincronizado por git.
- Usa IA como infraestructura de trabajo (no como chat): sesiones por proyecto, memoria persistente, handoffs, subagentes, skill workshop.
- Stack opinado: create-stack, OpenSpec, ADRs, AGENTS.md, HANDOFF, CHANGELOG.
- También: fotógrafo, comunicación social, quiere escribir novelas. Quiere organizar actividad fisica y mejorar salud.
