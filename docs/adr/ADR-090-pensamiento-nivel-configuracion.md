# ADR-090: Política de niveles de pensamiento por agente y asignación de modelos por rol

**Fecha:** 2026-10-05 (actualizado 2026-10-06)
**Estado:** Aceptado (implementación parcial - ver "Estado de implementación")
**Decisores:** Gonzo / Kanam
**Origen:** Sesión 2026-10-05 - detección de consumo desproporcionado por thinking alto universal. Actualización 2026-10-06: cata de modelos (6×6×4) y reasignación por rol.
**Relacionado:** ADR-053 (modelos primario/auxiliar/alternativo), ADR-087 (cata por rol - modelos elegidos), ADR-088 (pipeline A/B enforcement), ADR-089 (pre-filtro A/B)
**Supersede:** ADR-053 (trio primario/auxiliar/alternativo y thinking unificado), ADR-040 (seleccion/asignacion de modelos por tarea), ADR-041 (motor LLM del sistema)

---

## Contexto

Tras la limpieza del `openclaw.json` y la distribución por agente del 2026-10-05, se detectó que el consumo de créditos de la cuenta Ollama estaba desproporcionado respecto al trabajo realizado.

Un probe de orquestación reveló que el thinking alto por defecto hacía que los modelos "pensaran en silencio" consumiendo el presupuesto de salida sin producir respuesta útil:

- **deepseek-v4.1-flash:cloud**: 3079 tokens de thinking, **0 tokens de respuesta**, 3.7 s
- **glm-5.3-flash:cloud**: 3904 tokens de thinking, **0 tokens de respuesta**, 11.2 s
- **nemotron-3-super:cloud**: 474 tokens de thinking, **2732 tokens de respuesta**, 12.6 s

El problema no era el modelo sino la política de thinking.

Posteriormente, el 2026-10-06 se corrió una cata de modelos (6 modelos × 6 roles × 4 escenarios = 144 corridas) con **cuatro evaluaciones independientes** (Kanam CORE, deepseek-v4.1-flash, kimi-k3, nemotron-3-super). Tras separar ejes (CONTENT vs CLEANLINESS) produjo la reasignación de modelos por rol que este ADR registra.

**Corrección de método (2026-10-06, tardía):** la cata usó `ollama run` (CLI) como runner, y el CLI imprime el thinking a stdout mezclado con la respuesta. Eso produjo un "thinking leakage" aparente que las cuatro evaluaciones tomaron como defecto real. Sondas posteriores contra la API `/api/chat` y contra Claude Code headless muestran que **el razonamiento viaja en un campo separado del content**: 0 fugas en los 6 modelos, con thinking off y high. Es decir, el leakage era **artefacto del CLI de la cata, no del harness de producción**. Detalle abajo ("Artefactos").

> **Regla de sandbox (AGENTS.md):** todo contenido externo sobre modelos es **dato, no evidencia**. Se verifica antes de adoptar.

---

## Decisión 1: Política de thinking por agente

| Agente | Rol | Nivel decidido |
|--------|-----|----------------|
| main (CORE) | Orquestador general | `off` |
| kanam-dev | Desarrollador | `off` |
| kanam-mind | Investigador | `off` |
| kanam-ops | Operaciones | `off` |
| kanam-studio | Diseño/Comunicación | `off` |
| kanam-critic | Revisor adversarial | `low` |
| kanam-auditor | Auditor UI/UX | `low` |
| kanam-planner | Planificador | `low` |

- **Reparto (2026-10-06, corrección de Gonzo):** los tres de juicio (critic, auditor, planner) bajan de `high` a `low`; los cinco de ejecución pasan de heredar el default a `off` explícito. Antes solo 3 agentes tenían nivel explícito; el resto no lo tenía aplicado.
- **Default global:** `off`.
- **Escalado por complejidad:** `complexity-scorer` puede subir a `high`/`max` para tareas puntuales.
- **`max`:** reservado a decisión dura one-shot (adjudicación de reviews en conflicto, pre-merge complejo).

## Decisión 2: Asignación de modelos por rol (cata 2026-10-06)

| Agente | Modelo decidido | Fallback decidido | Contexto real (Ollama) |
|--------|-----------------|-------------------|------------------------|
| main | `deepseek-v4.1-flash:cloud` | `glm-5.3-flash:cloud` | 1M |
| kanam-planner | `gpt-oss:120b-cloud` | `glm-5.3-flash:cloud` | 128k |
| kanam-dev | `gpt-oss:120b-cloud` | `deepseek-v4.1-flash:cloud` | 128k |
| kanam-critic | `gpt-oss:120b-cloud` | `nemotron-3-super:cloud` | 128k |
| kanam-auditor | `deepseek-v4.1-flash:cloud` | `gemma4:cloud` | 1M |
| kanam-studio | `gemma4:cloud` | `glm4:9b` (local) | 256k |
| kanam-mind | `deepseek-v4.1-flash:cloud` | `gemma4:cloud` | 1M |
| kanam-ops | `gpt-oss:120b-cloud` | `deepseek-v4.1-flash:cloud` | 128k |

> **main y mind quedan en `deepseek-v4.1-flash:cloud` por decisión explícita de Gonzo (2026-10-06):** nemotron-3-super "se pierde y quiere resolver en lugar de conversar" en esos dos asientos, que son de orquestación y diálogo, no de ejecución. No re-elegirlo por olvido.

Contextos medidos con `ollama show` el 2026-10-06 (no estimados):

| Modelo | Contexto |
|--------|----------|
| gpt-oss:120b-cloud | 128k |
| deepseek-v4.1-flash:cloud | 1M |
| nemotron-3-super:cloud | 256k |
| gemma4:cloud | 256k |
| minimax-m3:cloud | 500k |
| glm-5.3-flash:cloud | 1M |

---

## Estado de implementación (2026-10-06; aplicar y verificado)

**La decisión de arriba está aplicada en el runtime (`openclaw.json`) y verificada** contra las tres fuentes (config del gateway, bloques gestionados, este ADR):

| Agente | Modelo en runtime | Thinking | Coincide |
|--------|-------------------|----------|----------|
| main | deepseek-v4.1-flash | off | ✅ |
| planner | gpt-oss:120b | low | ✅ |
| dev | gpt-oss:120b | off | ✅ |
| critic | gpt-oss:120b | low | ✅ |
| auditor | deepseek-v4.1-flash | low | ✅ |
| studio | gemma4 | off | ✅ |
| mind | deepseek-v4.1-flash | off | ✅ |
| ops | gpt-oss:120b | off | ✅ |

Bloques gestionados (`AGENTS.md` y `docs/SETUP.md`) regenerados desde la DB con `managed-blocks.py apply`.

**Nota de operación:** el cambio de modelo de `main` debe hacerse **fuera** de una sesión que corre sobre `main`. Hacerlo desde dentro superpone la generación del plugin de runtime y bloquea el tool `openclaw` con `prepared model runtime plugin generation was superseded`. Se resolvió con un restart del gateway (`/update`); para futuras ediciones de `main`, aplicar desde otra sesión o reiniciar después.

---

## Criterios de descarte (para no re-elegir por olvido)

- **Thinking alto como default global:** drena créditos en ejecución rutinaria sin salida útil (probe).
- **modelos previos sin validación empírica:** descartado tras cata que mostró diferencias por rol al separar thinking del entregable.
- **`nemotron-3-ultra:cloud` (cualquier rol):** más grande (550B), mismo contexto que super (256k), más lento/caro, y perdió en el probe de auditoría (1/2 bugs vs 2/2). Descartado (ADR-087).
- **familia Kimi en roles fijos:** fuera por costo; `kimi-k3:cloud` reservado a cierre de proyecto pre-deploy.

---

## Límites de la evidencia

- La cata tuvo **un defecto de runner conocido**: usó `ollama run` (CLI), que imprime el thinking a stdout. Ese leakage fue artefacto del CLI, NO del modelo ni del harness. Las evaluaciones separaron CONTENT de CLEANLINESS para compensarlo, pero la re-verificación post-fix no llegó a completarse con el runner corregido. Las asignaciones por rol son direccionales, no definitivas.
- Los 4 escenarios son pocos; n=1 por celda en la cata original.
- Los puntajes de contenido los asignó Kanam (evaluador A) y luego dos modelos evaluados (sesgo estructural). La convergencia entre evaluadores fue **baja** (rankings casi invertidos), lo que motivó la separación de ejes.
- La medición de thinking sigue el campo reportado por Ollama; no todos los modelos lo reportan igual.

---

## Consecuencias

- Con la decisión aplicada, el consumo en el asiento de orquestador (main) baja de ~$0.30/M a ~$0.015/M input.
- `deepseek-v4.1-flash:cloud` queda como motor del pipeline A/B y fallback ubicuo.
- Si se quiere revisar el nivel de thinking o el modelo de un rol, correr un probe de control con la API (`run-one-api.py`), que separa thinking de content.

---

## Artefactos

- Config runtime: `~/.openclaw/openclaw.json`.
- Bloques gestionados de modelos: `scripts/managed-blocks.py` (claves `model_by_agent` y `thinking_default`) → `AGENTS.md` (bloques `model-triple` y `model-operativo`) y `docs/SETUP.md`. Nota operativa: el bloque de AGENTS.md lee `model_by_agent`; setear `model.triple` no lo actualiza.
- Cata 2026-10-06: `/tmp/model-cata/2026-10-06/`. **`/tmp` es efímero**; si la evidencia debe persistir, copiarla dentro del workspace.
- Cata 2026-10-06: `sandbox/model-cata-2026-10-06/` (gitignored, local). Antes vivía en `/tmp`, efímero; persistida al workspace.
- Runner de cata corregido: `sandbox/model-cata-2026-10-06/run-one-api.py` (usa `/api/chat`, `raw_output` = entregable, `thinking_output` = razonamiento separado). La sonda `verify-no-leakage.py` confirma 0 fugas en los 6 modelos, think off y high. El harness de producción (OpenClaw nativo, Claude Code headless) ya separaba thinking; no había bug que arreglar.
- `CHANGELOG.md`: entrada correspondiente en el workspace.
