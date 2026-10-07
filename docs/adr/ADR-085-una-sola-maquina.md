# ADR-085: Una sola máquina - el workspace deja de sincronizarse entre equipos

**Fecha:** 2026-09-29
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** observación de Gonzo en la sesión del 2026-09-29: el workspace se seguía describiendo como compartido entre Mac Mini y MacBook Air, cuando la segunda dejó de usarse
**Relacionado:** ADR-073 (arquitectura multi-agente), ADR-074 (protocolo de despacho multi-agente), ADR-050 (memoria en SQLite), ADR-054 (kanam-os), ADR-056 (guardas del pre-commit)

---

## Contexto

El workspace nació como un repo **compartido entre dos máquinas** (Mac Mini + MacBook Air), sincronizado por git. Esa premisa atraviesa una cantidad de documentación: `README.md`, `AGENTS.md`, `USER.md`, `MEMORY.md`, `docs/SETUP.md`, `docs/gateway-operations.md`, `docs/learnings/`, `.knowledge/BRIEF.md`, y varios ADRs que justifican decisiones **por** la sincronización.

Con la migración a **arquitectura multi-agente** (ADR-073, 2026-09-26) y el despacho multi-agente (ADR-074), el modo de trabajo cambió: el sistema orquesta agentes dentro de **una sola máquina**. La MacBook Air dejó de tener un rol en ese flujo.

La deriva concreta: la documentación siguió afirmando "compartido entre dos máquinas, sincronizado por git" mucho después de que eso dejara de ser cierto. Se detectó el 2026-09-29 leyendo el `README.md` recién escrito.

**Nota honesta sobre el registro:** la decisión de Gonzo sobre la Air no había quedado escrita en ningún lado (se buscó en los dailies del 27/28/29 y en la memoria: no está). Este ADR es el registro que faltaba. La causa es la de siempre: una decisión que solo se dice en una conversación no viaja a la documentación, y el sistema sigue describiendo un mundo que ya no existe.

---

## Decisión

**El workspace vive en una sola máquina: la Mac Mini. No hay sincronización entre equipos.**

1. **La Mac Mini es la única máquina del workspace.** Corre el gateway 24/7 y hospeda el repo, la memoria y los proyectos.
2. **`git` sigue, pero por versionado y respaldo, no por sincronización.** `pull --rebase` antes del push se conserva como higiene de historial; ya no protege de "pisar cambios de la otra máquina".
3. **`memory.db` sigue versionada en git, con otro fundamento.** El motivo original era que la memoria viajara entre equipos (ADR-050/054). Con una sola máquina ese motivo desaparece; la DB se queda como **respaldo versionado de la fuente de verdad**. El umbral de higiene de git (bloat) sigue vigente; los conflictos de merge entre equipos, no.
4. **La regla "merge, nunca reset" se conserva, sin su porqué original.** Nació para no descartar commits de la otra máquina. Sigue siendo buena práctica al resolver conflictos de historial, así que se queda; lo que se retira es la justificación "de la otra máquina".
5. **Se retira la documentación cuyo único sujeto era el cambio de máquina.** El protocolo de cambio de máquina (archivo retirado: `machine-switch-protocol`, hoy en Trash) y el roadmap "3.2 La segunda máquina como activo" perdieron su sujeto: se eliminan / retiran, no se mantienen "por las dudas".

### Lo que NO cambia

- La Mac Mini sigue siendo el servidor 24/7 con Telegram y el gateway.
- `git` y GitHub siguen siendo el respaldo; los proyectos siguen viviendo en `~/projects` (ADR-075).
- No se borra historia: los registros fechados (dailies, learnings, ADRs) se conservan; se les añade una nota de que el escenario cambió, en vez de reescribirlos.

---

## Consecuencias

### Positivas
- **La documentación vuelve a describir la realidad.** Una afirmación falsa en `README.md`/`AGENTS.md` se propaga a cada sesión que la lee; corregirla en la raíz es la corrección de mayor rendimiento.
- **Se retira el ruido.** Un protocolo y un item de roadmap cuyo único sujeto ya no existe son deuda de lectura, no cobertura.

### Negativas
- **Sin segunda máquina no hay redundancia de hardware.** Si la Mini muere, el acceso al workspace depende del respaldo de GitHub. Aceptado: era el trade-off implícito de centralizar en la Mini.
- **La MacBook Air queda como máquina sin rol declarado.** Si vuelve a tener uno, este ADR se revisa (no se parchea).

---

## Alternativas consideradas

1. **Dejar la documentación como estaba "por si se reconecta la Air".** Rechazado: es exactamente el razonamiento que produce deriva. Un doc que describe un escenario inexistente miente en cada lectura.
2. **Mantener `machine-switch-protocol.md` marcado como inactivo.** Rechazado: sus fragmentos vivos (datos locales irrecoverables, gitlinks, `pull --rebase`) ya viven en `AGENTS.md` y `docs/AGENTS-DETALLE.md`; el resto era sólo el cambio de máquina. Conservarlo agregaba un archivo para no decir nada.
3. **Sacar `memory.db` de git al perder su motivo de sincronización.** Rechazado: el versionado sigue aportando respaldo, y su costo (bloat) ya está aceptado en ADR-054.

---

## Implementación

| Superficie | Cambio |
|---|---|
| `README.md`, `AGENTS.md`, `USER.md`, `MEMORY.md`, `docs/SETUP.md` | "dos máquinas / sincronizado" -> una máquina (Mac Mini) |
| `docs/gateway-operations.md`, `.knowledge/BRIEF.md` | idem |
| `docs/ROADMAP.md` | item 3.2 retirado |
| el viejo mapa de próximos pasos (retirado 2026-10-06; su contenido vivo pasó a `docs/ROADMAP.md`) | el código de `system-health-check` está en GitHub, no "en la Air" |
| `docs/learnings/` | notas fechadas; el texto histórico se conserva |
| `docs/adr/ADR-050`, `ADR-054` | nota: el argumento de sync era del escenario de dos máquinas |
| `docs/machine-switch-protocol` (retirado) | eliminado (perdió su sujeto) |
| `.gitignore` | comentario de la excepción de `memory.db` ya no cita sincronización |

## Referencias

- ADR-073 / ADR-074: la arquitectura multi-agente, el origen del cambio de modo de trabajo
- ADR-050 / ADR-054: por qué `memory.db` vive en git (motivo original: sincronización)
- `memory/2026-09-29.md`: la sesión que detectó la deriva
