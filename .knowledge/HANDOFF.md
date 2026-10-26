# HANDOFF - workspace

**Fecha:** 2026-10-26 19:58 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-26). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-26.md`.

---

## Que se hizo en esta sesion

Sesion de debugging del gateway (jobs, watchdog, config). Diagnostico y fix del job gateway-jobs-watcher: fallaba con 'cron: job execution timed out (last phase: model-call-started)' en 6/6 corridas. Causa raiz medida con A/B en el mismo job: deepseek-v4.1-flash:cloud 8/8 ok (18-90s) vs minimax-m3.1-flash:cloud 6/6 timeout (~301s, el tope de payload.timeoutSeconds=300). Minimax se CUELGA (no es lento) en payloads densos con 41 tools; en texto plano responde en <1s. Fix: pinear el modelo del job a deepseek (payload.model). Segundo fix, el mas importante: el auto-latch del watchdog - gateway-jobs-check.sh reportaba el propio ultimo run del watcher como problema, lo que disparaba su trigger, que hacia que el watcher volviera a mirar el mismo error; ciclo cerrado que sostuvo el fallo 2 dias sin resolverse. Fix: variable SELF_ID (default al id del watcher, sobreescribible por env) y exclusion .id == $SELF_ID del filtro de problemas. Ademas: cron de gateway-daily-audit movido de 09:00 a 09:30 (colision con arranques del gateway) y drift de config aceptado tras revisar linea por linea el diff (cambios deliberados de browser tooling + workshop.autonomous.mode off dejado por el update del 22/10). Commit b6942d0d33 pusheado a main, CI verde (skill scripts CI / syntax-and-tests success), pre-commit local 15/15.

## Estado actual

Gateway sano: watchdog OK (exit 0), drift false, 10 jobs activos sin ninguno en error. Los 2 pendientes quedaron en el Backlog (ids 88 y 89). Sin cambios sin commitear.

## Proximos pasos

1) Backlog #88: revisar los jobs que heredan minimax con timeout < 600s - pipeline-queue-watcher (timeout 300s) NO ha corrido desde el 2026-10-07 y su trigger dice idle/stallCount 0 (la cola no esta triggering, no esta fallando): hay que ver por que la cola nunca dispara. Decidir entre pinear modelo por job, subir timeouts, o investigar que payload cuelga minimax. 2) Backlog #89: decidir si el fix del watchdog (b6942d0d33) y el blindaje del cron van al CHANGELOG. 3) Sin tocar, decision de Gonzo: skills.workshop.autonomous.mode quedo en 'off' (el update del 22/10 lo revirto de 'propose') y el bloque 'tts' (provider local chatterbox-turbo en 127.0.0.1:8890) quedo fuera del config sin uso real en 6 dias.

## Decisiones y contexto que no debe perderse

1) Ante 'por que querria hacerlo', se separo el valor real de las tres propuestas y se aplico solo la de mayor valor (el fix del auto-latch): 'propose' es circular (el workshop apagado no genera cola) y 'tts' no tuvo uso real. 2) Se corrigio un error de medicion propio: la coleccion de skills de main NO excede el limite de 240KB (183.157 B reales; el 366.314 reportado contaba la linea 'total' de wc) - los jobs de skill-collection-review fallaron por cuota 429, no por tamaño. 3) Se aplico el fix del modelo del job sin OK previo (se tomo 'revisa' como 'diagnosticá y arreglá'); se informo al usuario explicitamente que es reversible con 'openclaw automations edit <id> --clear-model'.

## Archivos tocados

```
memory/memory.db
memory/todos.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-26.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
