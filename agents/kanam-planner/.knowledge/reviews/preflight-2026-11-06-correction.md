# Corrección al review del Planner — Preflight Etapa 2

**Fecha:** 2026-11-06
**Origen:** review del Planner sobre `.knowledge/ROADMAP.md` de `projects/preflight`.
**Estado:** corrección verificada contra el código. El Planner no escribe fuera de su workspace; este archivo es para que el CORE aplique la corrección en el roadmap del proyecto.

---

## Confirmado: un error del Planner

- **`--no-sandbox` fue un error del Planner.** `src/lib/scan.ts:33` lanza Chromium con
  `args: ['--disable-dev-shm-usage']`; **no** pasa `--no-sandbox`.
  El riesgo real es el inverso: Chromium puede negarse a arrancar como root dentro de un
  contenedor sin `--no-sandbox`. Eso se prueba en el contenedor, no se asume.

## Falsos positivos del review

- **“`mcp.ts` nunca llama `checkQuota`” — falso.**
  - `src/lib/mcp.ts:22` importa `checkQuota` y `recordUsage`.
  - `src/lib/mcp.ts:100` define `chargeQuota`.
  - `scan_url` lo llama en `src/lib/mcp.ts:135`; `get_fix_prompt` en `src/lib/mcp.ts:247`.
  - `src/lib/ratelimit.ts` define `BURST_MAX=3` por minuto y `DAILY_MAX=8` por día.
  - En HTTP con bearer token, `mcp-cli.ts` pasa `quotaKey` (hash del token), así que el
    test del 11º scan **sí** es válido: el 4º request en un minuto o el 9º del día devuelve 429.
- **“No hay cap de concurrencia” — falso.**
  - `src/lib/scan.ts:38` define `MAX_CONCURRENT` (default 4).
  - `acquireSlot`/`releaseSlot` en líneas 43/52.
  - `scanPage` adquiere y libera en líneas 100/104.
  - Diez callers hacen cola; no lanzan diez Chromium.
  - **Matiz real:** el cap es **por proceso**. Con N réplicas, el global es
    `MAX_CONCURRENT × N`. Eso sí falta si se escala horizontalmente.

## Huecos reales (corregidos)

| Hueco | Estado | Consecuencia |
|---|---|---|
| HTTP sin `PREFLIGHT_MCP_TOKEN` | Real | `mcp-cli.ts` permite no tener token en local/dev; si se expone así, no hay auth ni quota. Debe fallar cerrado en producción. |
| Cap global entre réplicas | Real si se escala | 4 por proceso × N réplicas. Hace falta un límite compartido o un solo writer. |
| Guard de CI para `readOnlyHint` | Real | Las cinco tools usan `READ_ONLY`, pero ningún test falla si una tool futura lo olvida. |
| Determinismo en contenedor | Real | El stable-wait está probado en la Mac, no en el destino. |
| Chromium como root / sandbox | Real | Hace falta un smoke test en el contenedor; decidir `--no-sandbox` vs usuario no-root. |

## Orden corregido

1. **Verificar quota y concurrencia en la topología HTTP real:** token seteado, 4 requests
   en un minuto → 429; `/health` con `activeScans` y `maxConcurrent`.
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
el estado actual cita `archivo:línea` o se marca como supuesto; si no se pudo verificar,
se agrega un paso de verificación y no se dispatcha el plan.**
