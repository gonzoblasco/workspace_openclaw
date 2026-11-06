# Despacho de infraestructura: el CORE llama a OPS

**Fecha:** 2026-11-06
**Regla en `AGENTS.md`:** seccion "Infraestructura: el CORE llama a OPS".
**Base:** ADR-074 (OPS es duenio del sustrato), ADR-083 (el CORE orquesta, no implementa).

Este archivo existe porque la regla completa no entra en el cap de bootstrap
del `AGENTS.md` (20000 caracteres) y lo que se pasa se trunca en silencio. El
`AGENTS.md` lleva el principio; aca va el detalle operativo.

---

## 1. Que es de OPS

Todo cambio sobre el sustrato del gateway:

| Area | Incluye |
|---|---|
| Config | `openclaw.json` en cualquier forma, `config set`, `config patch --stdin` |
| Canales | alta, cambio, credenciales de Telegram y otros |
| Plugins | habilitar, deshabilitar, instalar, actualizar |
| Automatizaciones | crear, editar, mover de agente, triggers, schedules |
| Drift | baseline, aceptar, explicar diferencias |
| Backups | crear, verificar, restaurar |
| Secretos | migracion a SecretRef, rotacion |
| Diagnostico | por que el gateway no responde, por que un job falla |

## 2. Que NO es de OPS

- Codigo de aplicacion: es de `kanam-dev`.
- Contenido, marca, redaccion: es de `kanam-studio`.
- Investigacion y decision de producto: es de `kanam-mind`.
- Gobernar un programa, escribir ADRs: es del CORE.
- Revision de codigo: es de `kanam-critic` / `kanam-auditor`.

## 3. OPS ya esta en el flujo

No hace falta despertarlo a mano para lo rutinario. Tres jobs corren con
`agentId: kanam-ops`:

| Job | Schedule | Que hace |
|---|---|---|
| `gateway-daily-audit` | cron `30 9 * * *` | audit completo a `~/.openclaw/gateway-audit.log` |
| `gateway-jobs-watcher` | cada 2h con trigger | alerta si un job falla o el check no puede correr |
| `openclaw-backup-scheduled` | cada 24h | backup git de la config a `~/Backups/openclaw-git` |

Ademas, `hooks.allowedAgentIds` incluye `kanam-ops`, asi que OPS puede recibir
trabajo por hook, no solo por spawn.

## 4. Como se le pide algo

`sessions_spawn(agentId: "kanam-ops")` con:

1. **Que hay que hacer**, en imperativo.
2. **Riesgo esperado**: que puede salir mal y que NO se debe tocar.
3. **Limite de aprobacion**: si el trabajo incluye un restart, un borrado o un
   cambio de produccion, se dice explicitamente que NO esta aprobado.

## 5. Que devuelve siempre (contrato de handoff)

- Que cambio, con el comando exacto.
- Nombre del backup.
- Valor antes y despues.
- Evidencia de verificacion (salida real del comando, no la promesa).
- Si requiere restart.

**Un "quedo bien" de OPS es un reporte, no una prueba.** El estandar del CORE
sigue siendo correr el efecto real antes de reportar a Gonzo.

## 6. El limite que no se delega

Aprobar un restart, un borrado o un cambio de produccion es de Gonzo, aunque
OPS tenga la capacidad tecnica para hacerlo. Delegar la tarea no delega la
aprobacion.

---

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
