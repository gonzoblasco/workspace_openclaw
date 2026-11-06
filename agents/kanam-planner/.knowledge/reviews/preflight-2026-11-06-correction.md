# Corrección al review del Planner — Preflight Etapa 2

**Fecha:** 2026-11-06
**Origen:** review del Planner sobre `.knowledge/ROADMAP.md` de `projects/preflight`.
**Estado:** corrección verificada contra el código **y contra el commit del fix**. El Planner no escribe fuera de su workspace; este archivo es para que el CORE aplique la corrección en el roadmap del proyecto.

---

## Confirmado: un error del Planner

- **`--no-sandbox` fue un error del Planner.** `src/lib/scan.ts:69` lanza Chromium con
  `args: ['--disable-dev-shm-usage']`; **no** pasa `--no-sandbox`.
  El riesgo real es el inverso: Chromium puede negarse a arrancar como root dentro de un
  contenedor sin `--no-sandbox`. Eso se prueba en el contenedor, no se asume.
  (El review citó `scan.ts:33`, que es un comentario; el argumento real está en la línea 69.
  La sustancia del hallazgo es correcta, la línea no.)

## El estado del código cambió después del review

El review se escribió **antes** del commit `289cb19` (`feat(mcp): enforce quota and cap
concurrency before any public exposure`, 2026-11-06 16:21:36). En ese momento:

- `mcp.ts` **no** llamaba `checkQuota`; el gap de quota era real.
- `scan.ts` **no** tenía cap de concurrencia; el gap era real.

El commit `289cb19` cerró ambos:

- **Quota:** `src/lib/mcp.ts:25` importa `checkQuota`/`recordUsage`; `:100` define
  `chargeQuota`; `scan_url` lo llama en `:135` y `get_fix_prompt` en `:247`.
  `src/lib/ratelimit.ts:19-20` define `BURST_MAX=3`/min y `DAILY_MAX=8`/día.
  En HTTP con bearer token, `mcp-cli.ts` pasa `quotaKey` (hash del token). El test del
  11º scan **ahora sí** es válido; antes era trabajo faltante, como dijo el review.
- **Concurrencia:** `src/lib/scan.ts:38` define `MAX_CONCURRENT` (default 4);
  `acquireSlot`/`releaseSlot` en `:43/:52`; `scanPage` adquiere/libera en `:100/:104`.
  Diez callers hacen cola; no lanzan diez Chromium. El cap es **por proceso**.

**Lectura correcta:** el review no tuvo falsos positivos; describió el estado pre-fix. La
verificación posterior encontró el estado post-fix. La lección es citar **commit + archivo:línea**,
porque una afirmación de estado es válida solo para el snapshot que se leyó.

## Huecos que siguen reales

| Hueco | Estado | Consecuencia |
|---|---|---|
| HTTP sin `PREFLIGHT_MCP_TOKEN` | Real | `mcp-cli.ts` permite no tener token en local/dev; si se expone así, no hay auth ni quota. Debe fallar cerrado en producción. |
| Cap global entre réplicas | Real si se escala | 4 por proceso × N réplicas. Hace falta un límite compartido o un solo writer. |
| Guard de CI para `readOnlyHint` | Real | Las cinco tools usan `READ_ONLY`, pero ningún test falla si una tool futura lo olvida. |
| Determinismo en contenedor | Real | El stable-wait está probado en la Mac, no en el destino. |
| Chromium como root / sandbox | Real | Hace falta un smoke test en el contenedor; decidir `--no-sandbox` vs usuario no-root. |

## Orden corregido

1. **Verificar quota y concurrencia en la topología HTTP real.** El commit `289cb19` ya
   incluye una prueba con `PREFLIGHT_DAILY_MAX=2` y otra con `PREFLIGHT_MAX_CONCURRENT=2`;
   correrlas contra el server HTTP, no solo en unit test. Revisar `/health`
   (`activeScans`/`maxConcurrent`).
2. **Cerrar HTTP sin token:** si `PREFLIGHT_MCP_TOKEN` no está seteado en producción, el
   server no debe arrancar (fail closed).
3. **Cap global** si hay más de una réplica.
4. **Smoke test de contenedor:** Chromium como root/no-root, decisión de `--no-sandbox`,
   determinismo.
5. **Guard de CI** para `READ_ONLY` en cada tool registrada.
6. **Recién entonces** Funnel/Fly.

## Lección de proceso

El error de `--no-sandbox` no fue un problema de brief: fue una afirmación de estado sin
leer el código. La regla queda escrita en `program-orchestration`: **cada afirmación sobre
el estado actual cita `archivo:línea` y el commit/snapshot que se leyó; si no se pudo
verificar, se marca como supuesto y se agrega un paso de verificación.** El plan no se
dispatcha sobre supuestos.

## Decisión sobre el modelo (feedback de Preflight, 2026-11-06)

**No se cambia `gpt-oss:120b-cloud`.** El Planner razonó bien la secuencia, el gate y el
criterio de aborto; lo mejor del plan salió de ahí. Falló al afirmar detalles del código
que no abrió (`--no-sandbox`, el 429 pre-fix).

**El fix va en el brief/contrato, no en el modelo.** La opción elegida es la primera del
backlog de Preflight: exigir que cada afirmación sobre el código cite `archivo:línea` o se
marque como supuesta. Un modelo más caro con el mismo brief cometería el mismo error, solo
más rápido.

Implementación: `program-orchestration` y `planner-delegation` ya exigen esa regla; el
brief del CORE debe pasarla explícitamente y no aceptar un plan que afirme estado sin
fuente.
