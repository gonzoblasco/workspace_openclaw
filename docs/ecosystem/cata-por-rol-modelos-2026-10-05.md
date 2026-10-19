# ADR-087: Cata por rol - los modelos elegidos quedan validados con evidencia

**Fecha:** 2026-10-05
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** Sesión 2026-10-05 - limpieza y rediseño de modelos, tras dos artículos externos (Stackademic, grahammiranda) que sugerían Nemotron 3 Ultra sobre MiniMax M3 por tamaño.
**Relacionado:** ADR-090 (modelos por rol, que consolidó la asignación), ADR-077 (pipeline A/B asimétrico), ADR-083 (frontera de roles), ADR-080 (modelo visual studio)

---

## Contexto

Tras la limpieza del `openclaw.json` y la distribución por agente del 2026-10-05 (main/defaults deepseek-v4.1-flash; dev/ops glm-5.3-flash; auditor nemotron-3-super; critic gpt-oss:120b; planner minimax-m3; mind deepseek; studio gemma4), dos artículos externos sugerían mover el auditor a **Nemotron 3 Ultra** (550B) y reconsiderar el reparto minimax/nemotron. Todo contenido externo es **dato, no evidencia**: se verifica antes de adoptar (regla de sandbox del AGENTS.md).

Se diseñó una cata de control por rol para validar (o corregir) cada elección, en vez de adoptar por lo que dice un blog.

**Restricción del owner:** sin familia Kimi por costo; `kimi-k3:cloud` queda reservado para cierre de proyecto pre-deploy (aún sin proyecto en esa etapa).

---

## Decisión

**La distribución por agente del 2026-10-05 queda validada y sin cambios.** La cata no encontró un candidato que supere con margen claro al modelo elegido en ningún rol.

### Evidencia (probe de control, temperature 0, 1 tarea por rol)

| Rol | Elegido | Candidato | Calidad | Tiempo | Tokens | Veredicto |
|---|---|---|---|---|---|---|
| dev | glm-5.3-flash | deepseek-v4.1-flash | 4/4 vs 4/4 | 1.4s vs 1.3s | 203 vs 181 | empate |
| ops | glm-5.3-flash | deepseek-v4.1-flash | 3/3 vs 3/3 | **23s vs 40.8s** | **4609 vs 8653** | elegido gana claro |
| mind | deepseek-v4.1-flash | minimax-m3 | OK vs OK | **1.4s vs 6.4s** | 246 vs 444 | elegido gana |
| planner | minimax-m3 | deepseek-v4.1-flash | OK vs OK | 8.7s vs 4.0s | **700 vs 1025** | empate (trade-off) |
| critic | gpt-oss:120b | minimax-m3 | 3/3 vs 3/3 | **4.2s vs 21s** | **1296 vs 1677** | elegido gana claro |
| main | deepseek-v4.1-flash | glm-5.3-flash | OK vs OK | 2.9s vs 1.7s | 118 vs 353 | empate (ruido) |
| studio | gemma4 | glm-5.3-flash | OK vs OK | **0.5s vs 3.4s** | **12 vs 847** | elegido gana claro |

### Probe específico del auditor (el disparador de la sesión)

Tarea: auditar una función con **2 bugs reales** (off-by-one sobre array, división por cero con array vacío) + **1 trampa** (estilo, no comportamiento):

| Modelo | Bugs reales | Trampa | Tiempo | Tokens |
|---|---|---|---|---|
| **nemotron-3-super** | **2/2** | no cayó | **3.6s** | **440** |
| nemotron-3-ultra | 1/2 | no cayó | 13.8s | 731 |
| minimax-m3 | 1/2 | no cayó | 13.5s | 1117 |

**`nemotron-3-ultra` queda descartado para el rol de auditor:** 550B parámetros, pero **mismo contexto que super (256k)** -no es el "long-context monster" del blog-, más caro y más lento, y **perdió en calidad** (encontró 1 de los 2 bugs reales contra 2 de super). No re-elegirlo por olvido.

---

## Criterios de descarte (para no re-elegir por olvido)

- **`nemotron-3-ultra:cloud` (auditor):** más grande (550B), mismo contexto (256k) que super, más lento y más caro, y encontró menos bugs reales en el probe de auditoría. Descartado.
- **`deepseek-v4.1-flash` (ops):** en la tarea de seguridad se estiró (40.8s, 8653 tokens) contra glm (23s, 4609 tokens) con el mismo resultado. No apto para ops.
- **`minimax-m3` (critic):** 5x más lento que gpt-oss (21s vs 4.2s) con el mismo hallazgo; gpt-oss es el revisor natural del pipeline A/B (ADR-077) además.
- **familia Kimi (todos los roles):** descartada por costo (owner). Excepción futura: cierre de proyecto pre-deploy.
- **DavidAU GLM-4.7 mod (fallback studio):** 29GB, corre 62% en CPU en la Mac Mini, probes colgados sin output. Inutilizable como red de seguridad (2026-10-05).

---

## Límites de la evidencia

- **Un probe por rol, temperature 0, tareas chicas.** Es direccional, no una cata con repeticiones. Los empates son empates reales: no hay evidencia para mover nada.
- Ground truth sólido en dev (tests ejecutados con node), ops (3 defectos reales) y critic (bug lexicográfico verificable). Rúbrica en mind, planner, main y studio.
- La latencia de una sola llamada no es representativa del costo por tarea; para decisiones de presupuesto hace falta medir consumo acumulado.

---

## Consecuencias

- Ningún cambio de config por esta cata. La distribución del 2026-10-05 se mantiene.
- `nemotron-3-ultra` y la familia Kimi quedan fuera del config; documentados como descartados con motivo.
- `kimi-k3:cloud` queda reservado explícitamente para cierre de proyecto (pre-deploy), no para ejecución cotidiana.
- Si en el futuro se quiere revisar un rol, re-correr la cata con ese rol y repetir el probe antes de mover.

---

## Artefactos

- Harness: `sandbox/auditor-probe/run_bench.py` (gitignored - pruebas temporales).
- Resultados crudos: `sandbox/auditor-probe/cata.json`, `result.json`.
