# ADR-081: El scope del registro de plugins lo fija el ORDEN de `agents.entries`

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisores:** Gonzo (aprobacion del experimento) / Kanam (diagnostico)
**Origen:** sesion 2026-09-28 - los triggers de automatizacion fallaban con "Plugin runtime changed" desde hacia dias
**Relacionado:** ADR-073 (arquitectura multi-agente), ADR-074 (protocolo multi-agente), ADR-078 (verificar antes de reportar)

---

## Contexto

Los triggers de automatizacion (`pipeline-queue-watcher`, `langchain-starter-health-watch`, `gateway-jobs-watcher`) fallaban intermitentemente con:

```
cron trigger evaluation failed (internal_error): Error: Plugin runtime changed. Continue with the refreshed tool catalog.
```

El registro de plugins persistido quedaba `stale` con un **desacuerdo de scope**:

| | Valor |
|---|---|
| `persisted.workspaceDir` | `…/workspace/agents/kanam-dev` |
| `current.workspaceDir` | `…/workspace` |
| `differences` | `[]` (los 62 manifiestos coincidian) |

El registro vive en `config_machine_state.plugins.installedIndex` (`~/.openclaw/state/openclaw.sqlite`), campo `index.workspaceDir`.

## Diagnostico

El refresh **calculaba bien** el valor correcto pero **no podia escribirlo**: `canRefreshPersistedPolicyState` exige `reason === "policy-changed"` y ademas corta si hay mismatch, mientras el refresh se dispara como `source-changed`. Por eso reescribia el resto del indice y dejaba el scope viejo. `doctor` no detectaba el caso y el CLI no exponia palanca de scope.

**No era residuo pasivo:** borrar la fila no servia (no se regenera sola, pero el proximo comando la reescribe con el mismo valor malo).

**La causa real**, hallada con un experimento A/B/A aprobado por el owner:

| Orden de `agents.entries` | `state` | `workspaceDir` |
|---|---|---|
| `kanam-dev, kanam-mind, kanam-ops, kanam-studio, main` (original) | `stale` | `…/agents/kanam-dev` |
| `main, kanam-dev, kanam-mind, kanam-ops, kanam-studio` | **`fresh`** | **`…/workspace`** |
| revertido al original | `stale` | `…/agents/kanam-dev` |

**El control-plane de plugins resuelve el scope desde el PRIMER entry del roster, no desde `agents.defaults.systemAgent.agentId`.**

Esto se lee como bug: `resolvePluginControlPlaneWorkspace` -> `tryResolveAmbientOwnerAgentId` **si** prefiere `systemAgent.agentId` (`main`, configurado correctamente), pero el indice persistido seguia al primer entry. Ambas rutas coexisten y no coinciden. Reportado como hallazgo; no se parchea codigo de OpenClaw.

## Decision

**1. `main` va PRIMERO en `agents.entries`.** Es el owner del control-plane de plugins y debe encabezar el roster. Verificado: el orden produce `state: fresh` y el scope correcto, y es **estable** (releido 20 s despues sin intervencion, sigue `fresh`).

**2. El orden es significativo, no cosmetico.** Un roster donde un agente especialista precede a `main` fija el scope de plugins a ese especialista y rompe los triggers globales. Al agregar agentes, `main` se mantiene primero.

### Verificacion (2026-09-28)

- `state: fresh`; `persisted.workspaceDir == current.workspaceDir == …/workspace`.
- `langchain-starter-health-watch`: `error` a las 15:04 -> **`ok` a las 16:04**.
- `pipeline-queue-watcher`: `error` a las 15:04 -> `skipped` a las 16:04 (skip propio del job, no del runtime).
- Los `skill-collection-review-*` (scope de agente) siguen `ok`.

## Consecuencias

- **Al sumar un agente nuevo, `main` no se mueve de la primera posicion.** Documentarlo en el procedimiento de alta de agentes.
- **No hace falta reiniciar el gateway:** el orden se lee y el refresh escribe el scope corregido.
- **`gateway-jobs-watcher`** corre cada 2 h; su ultima corrida fue 15:23 (previa al fix). Se verifica en la proxima.
- **`base-ui-stable-check` NO es parte de esto:** falla desde 2026-09-27 con `job execution timed out (last phase: model-call-started)`, una firma distinta y anterior. Causa separada, pendiente propia.
- **El error cambio de firma** durante el dia: `internal_error` -> `plugin_reload_failed`. Ambas son la misma desactualizacion vista en dos superficies.

## Nota de metodo: la lectura de la DB de estado debe incluir el WAL

La DB de estado usa `journal_mode = wal`. **Copiar solo `openclaw.sqlite` lee estado viejo.** En esta sesion eso produjo una "contradiccion" falsa entre el CLI (`fresh`) y la copia de la DB (`stale`): el CLI leia el WAL, la copia no.

Copia correcta:

```bash
cp state/openclaw.sqlite /tmp/r.sqlite
cp state/openclaw.sqlite-wal /tmp/r.sqlite-wal
cp state/openclaw.sqlite-shm /tmp/r.sqlite-shm
```

**Regla:** antes de declarar que dos fuentes se contradicen, verificar que ambas lean la misma version del dato. Un `-wal` no copiado es un falso desacuerdo.
