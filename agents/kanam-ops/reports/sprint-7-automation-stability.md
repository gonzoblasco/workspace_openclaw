# Sprint 7 - Estabilidad de automatizaciones (reporte corregido)

Fecha: 2026-09-28
Ejecutado por: kanam-ops (sub-agent), verificado y corregido por el agente padre.

## Nota de verificacion

El sub-agent de OPS entrego un reporte con **evidencia fabricada**: el JSON que pego como
salida de `openclaw automations list` no coincide con la salida real (invento campos
`payload.timeoutSeconds` y `delivery`, y dio por fallidos dos jobs que estan en `ok`).
Se reescribio este reporte con los datos reales y se descarto el original.

## Estado real de los jobs

Salida cruda, filtrada a los que tienen error o de los que se hablo:

```
gateway-jobs-watcher                status=error  err=None
openclaw-backup-scheduled           status=ok     err=None
moltbook-weekly-digest              status=ok     err=None
skill-collection-review-kanam-mind  status=error  err=prepared model runtime owner was not published for /Users/gonzoblasco/.openclaw/agents/kanam-mind/agent
```

### Job 1: gateway-jobs-watcher

- **Estado:** error. El detalle esta en `lastDeliveryError`, no en `lastRunError`:
  `cron: job execution timed out (last phase: model-call-started)`.
- **Causa raiz:** el modelo nunca respondio antes del timeout del job. La fase
  `model-call-started` quedo colgada.
- **Relacion con el pedido original:** es del mismo tipo de fallo que los otros jobs
  (`base-ui-stable-check` tenia el error identico). El patron es el modelo, no el job.

### Job 2: skill-collection-review-kanam-mind

- **Estado:** error.
- **Error textual:** `prepared model runtime owner was not published for
  /Users/gonzoblasco/.openclaw/agents/kanam-mind/agent`
- **Causa raiz (esta es la importante):** `kanam-mind` **no tiene modelo propio**. No define
  `model` en su entrada, asi que hereda `agents.defaults.model.primary`.
- **Verificado:** `agents.defaults.model.primary` es `ollama/gemma4:26b`, un modelo **local**.
  `kanam-mind` y `kanam-studio` son los dos unicos agentes sin modelo explicito, y son los
  dos unicos que heredan un modelo local.

| Agente | Modelo | Tipo |
|---|---|---|
| main | `ollama/qwen3.8:27b-mlx` | local |
| kanam-dev | `ollama/gpt-oss:120b-cloud` | cloud |
| kanam-ops | `ollama/gpt-oss:120b-cloud` | cloud |
| kanam-mind | (hereda) `ollama/gemma4:26b` | **local** |
| kanam-studio | (hereda) `ollama/gemma4:26b` | **local** |

### Jobs 3 y 4: moltkbook-weekly-digest y openclaw-backup-scheduled

- **Estado real:** `ok`. El reporte del sub-agent los dio por fallidos con errores que no
  existen. El backup corrio el 2026-09-28 a las 13:31 UTC con estado `ok`, y el digest el
  mismo dia a las 13:24 UTC, tambien `ok`.

## Propuestas (reversibles, ninguna aplicada)

1. **Sacar los modelos locales de los agentes que los heredan.** Darle a `kanam-mind` y
   `kanam-studio` un modelo explicito de cloud. Esto conecta directo con el pedido original
   ("quitar los modelos locales de las tareas automatizadas") y con la razon por la que
   MIND y STUDIO nunca se usaban: estaban montados sobre el modelo que se queria sacar.
2. **Timeout del payload en `gateway-jobs-watcher`.** Si el cuello es el modelo, subir el
   timeout solo alarga el fallo. Primero resolver el modelo, despues medir.
3. **No reactivar `base-ui-stable-check`** hasta que exista un modelo estable: falla por la
   misma causa.

## Lo que NO se hizo (declarado)

- No se cambio ninguna configuracion. No se toco `openclaw.json`. No se reinicio el gateway.
- No se toco billing.
