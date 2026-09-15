# Fase 0 - Cola durable de ejecucion del pipeline (spec)

**Fecha:** 2026-09-15
**Autor:** Kanam (MAX, diseno) - implementa Agente A (HIGH), revisa Agente B (HIGH)
**T-score:** 14 (high) - `complexity-scorer.sh`, 2026-09-15
**Origen:** `docs/architecture/kanam-os-layers-evaluacion.md`, decision de Gonzo: "iniciemos fase 0"

---

## Correccion del diagnostico original

La evaluacion del 2026-09-15 nombro el gap como "SIGKILL de Qwen Code a ~3 min". **Eso esta desactualizado.** Gonzo lo cuestiono y tenia razon: el harness del pipeline ya migro a Claude Code (verificado: binario 2.1.260 funcionando, `HARNESS_OK` el 2026-09-15).

**El gap real, corregido:** la ejecucion del pipeline **no tiene continuidad**. Cuando una unidad se interrumpe (muerte del proceso, restart del gateway, eviction de contexto, corte de red), no hay reanudacion automatica. `pipeline-track.sh` guarda el *estado* del plan, pero nada avanza la cola ni reencola lo interrumpido sin intervencion manual.

**Lo que resuelve esta fase:** que una unidad interrumpida se reencuele y continue sola, con reintentos acotados.

---

## Estado actual (verificado)

`scripts/pipeline-track.sh` ya aporta:

| Campo | Uso actual |
|---|---|
| `state` | `queued` / `running` / `review` / `done` |
| `owner` | A / B (paridad) |
| `startTime` / `endTime` | epoch seconds |
| `iterations` | re-arranques de la misma unidad |
| `regressions` | bugs introducidos por el agente B |
| `complexity` | T-score |

**Lo que falta:** seleccion de la proxima unidad, deteccion de huerfanas, reintentos con cap, y un estado terminal de fallo que no bloquee el resto.

---

## Diseno: `scripts/pipeline-queue.sh`

Capa **aditiva** sobre `pipeline-track.sh`. No lo modifica: escribe los mismos campos mas tres nuevos (`attempts`, `pid`, `lastError`) en el mismo `pipeline-state.json`.

### Estados

Los cuatro existentes, mas uno:

| Estado | Significado |
|---|---|
| `queued` | lista para ejecutar |
| `running` | en ejecucion (con `pid` vivo esperado) |
| `review` | esperando revision de B |
| `done` | completada |
| **`failed`** | agotó reintentos. Terminal. **No bloquea** el resto de la cola |

### Comandos

```
pipeline-queue.sh enqueue <fase> [--score T] U1 U2 ...   # plan + attempts=0
pipeline-queue.sh next                                    # imprime la proxima unidad, o vacio
pipeline-queue.sh claim <unit> <pid>                      # running + pid + attempts++ + startTime
pipeline-queue.sh release <unit> [reason]                 # reintento o failed segun attempts
pipeline-queue.sh done <unit>                             # delega en pipeline-track done
pipeline-queue.sh review <unit>                           # delega en pipeline-track review
pipeline-queue.sh orphans                                 # running con pid muerto
pipeline-queue.sh tick                                    # reencola huerfanas + imprime proxima
pipeline-queue.sh report                                  # telemetria por unidad
pipeline-queue.sh status                                  # estado extendido
```

### Reglas

1. **Reintentos:** `PIPELINE_MAX_ATTEMPTS` (default 3). Al superarlo, `failed` y mensaje claro.
2. **Huerfana:** unidad `running` cuyo `pid` no responde a `kill -0` se reencola como `queued`.
3. **Sin pid registrado** (compatibilidad con planes viejos): no se considera huerfana - se respeta el estado.
4. **Determinismo:** `next` devuelve siempre la primera `queued` en orden de declaracion.
5. **`failed` no bloquea:** `next` salta las `failed` y sigue con las `queued`.
6. **Idempotencia:** `claim` sobre una unidad ya `running` con pid vivo no la duplica.

### Integracion con automations de OpenClaw

La cola es la pieza de estado; el disparador es un job de automations. El diseno deja `tick` como el punto de entrada unico para que un job `every` o un `stream` (on-exit) lo invoque. **Esta fase entrega el script y sus tests; el job se cablea en la fase siguiente, con prueba visible.**

---

## Criterios de aceptacion

1. `bash -n scripts/pipeline-queue.sh` limpio.
2. `tests/bash/pipeline-queue.bats` con cobertura de: enqueue, next, claim, release con reintento, release hasta `failed`, deteccion de huerfana, salto de `failed` en `next`, report.
3. Suite completa verde: `npm test` (test-skills + bats + pytest).
4. **No rompe** `pipeline-track.sh`: correr su flujo completo (`init` -> `start` -> `review` -> `done` -> `status`) sobre el mismo archivo y verificar que sigue funcionando.
5. `python3 scripts/check_em_dash.py scripts/pipeline-queue.sh tests/bash/pipeline-queue.bats` → OK.
6. Estado de un plan viejo (sin `attempts`/`pid`) se lee sin error.

---

## Restricciones

- **No modificar** `scripts/pipeline-track.sh`. Solo consumirlo.
- **No tocar** `pipeline-state.json` real durante los tests: usar `PIPELINE_STATE_FILE` apuntando a un tmp.
- Bash POSIX-compatible con `set -uo pipefail`, mismo estilo que `pipeline-track.sh`.
- `jq` disponible (ya es dependencia de `pipeline-track.sh`).
- Guion comun siempre. Nunca em dash.
