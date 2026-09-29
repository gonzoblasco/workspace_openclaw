# ADR-081: El scope del registro de plugins lo fija el ORDEN de `agents.entries`

**Fecha:** 2026-09-28 (corregido 2026-09-29)
**Estado:** **Parcialmente refutado** - ver la correccion al final
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

---

## CORRECCION 2026-09-29: la causa del fallo NO era el orden (y el orden no es una palanca durable)

Diez horas despues, el sistema desmintio la conclusion principal de este ADR. Tres hechos medidos:

**1. El orden se revirtio solo, y el registro volvio a `stale`.** El gateway reescribio `openclaw.json` a las **23:29-23:30** del 2026-09-28 (eventos `config.write` en `logs/config-audit.jsonl`, **sin actor de agente**), y dejo `agents.entries` en orden **alfabetico** (`kanam-dev, kanam-mind, kanam-ops, kanam-studio, main`). O sea: **la posicion de `main` no persiste entre escrituras del gateway**, asi que "mantener `main` primero" no es una decision que el sistema respete.

**2. Con el orden roto, los jobs NO fallan.** Estado actual medido: `state: stale`, `persisted.workspaceDir = …/agents/kanam-dev`, orden alfabetico... y **0 errores en 31 corridas** de los tres jobs vigilados desde ayer 23:30 (36 `ok`, 74 `skipped`, 0 `error`).

**3. Por lo tanto, la inferencia causal de este ADR es falsa.** El A/B/A original **si** probo que el orden controla `index.workspaceDir` (eso sigue en pie y es reproducible). Lo que **no** se sostiene es el paso siguiente: que ese desvio sea la causa del fallo de los triggers. Hay dos estados independientes que yo trate como uno:

| Hecho | Estado |
|---|---|
| El scope persistido del registro | `stale` (cosmetico en la practica) |
| El fallo de los triggers | resuelto |

**La causa real, revisada:** el desalineamiento de la **generacion del runtime de plugins** dentro de la sesion que evalua el trigger (el guard `Plugin runtime changed` compara la generacion que tenia la sesion contra la actual). Eso se resetea con un **reinicio del gateway** -y hubo tres: 20:01, 23:14 y 23:30- y/o con un **refresh que reescriba el indice**. Mi refresh de las 16:04 coincidio con la recuperacion, pero el reinicio de las 20:01 es igualmente suficiente para explicarla. **No aislé cual de los dos fue:** el experimento que faltaba era dejar el orden roto, reiniciar, y ver si los jobs fallaban.

### Que queda firme y que no

- **Firme:** el orden de `agents.entries` determina el `workspaceDir` persistido del registro. Reproducible.
- **Firme:** el gateway reescribe el config en orden alfabetico, sin actor de agente, y el scope resultante queda `stale`.
- **Refutado:** que ese `stale` cause el fallo de los triggers. **El registro puede estar `stale` con los jobs sanos.**
- **Refutado:** que "`main` primero" sea el fix. **No persiste**, y ademas no era lo que arreglaba el sintoma.

### Regla que reemplaza a la decision original

**No perseguir el flag `stale` del registro, y no tocar el orden de `agents.entries` para arreglarlo.** El flag no predice el fallo de los jobs. Si los triggers fallan con `Plugin runtime changed`, la palanca es **reiniciar el gateway** (que regenera el runtime) o **refrescar el registro**, y la verificacion es la **corrida del job**, nunca el `state`.

**Y la leccion de metodo, que es la de fondo:** probe una correlacion (orden -> `state`) y salte a una causa (orden -> fallo de los jobs) **sin probar el mecanismo**. El A/B/A confirmaba una cosa y yo reporte dos. Faltaba el paso que la propia hipotesis exigia: revertir el orden **y** ver el sintoma. Una correlacion reproducible no es una cadena causal verificada.

**Nota historica (no borrar):** el diagnostico original sigue util como registro del sintoma y de la superficie del flag. Lo refutado es la causa y el fix, no el sintoma.
