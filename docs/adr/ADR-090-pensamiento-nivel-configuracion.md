# ADR-090: Política de niveles de pensamiento por agente y asignación de modelos por rol

**Fecha:** 2026-10-05 (actualizado 2026-10-06)
**Estado:** Aceptado (implementación parcial - ver "Estado de implementación")
**Decisores:** Gonzo / Kanam
**Origen:** Sesión 2026-10-05 - detección de consumo desproporcionado por thinking alto universal. Actualización 2026-10-06: cata de modelos (6×6×4) y reasignación por rol.
**Relacionado:** ADR-053 (modelos primario/auxiliar/alternativo), ADR-087 (cata por rol - modelos elegidos), ADR-088 (pipeline A/B enforcement), ADR-089 (pre-filtro A/B)

---

## Contexto

Tras la limpieza del `openclaw.json` y la distribución por agente del 2026-10-05, se detectó que el consumo de créditos de la cuenta Ollama estaba desproporcionado respecto al trabajo realizado.

Un probe de orquestación reveló que el thinking alto por defecto hacía que los modelos "pensaran en silencio" consumiendo el presupuesto de salida sin producir respuesta útil:

- **deepseek-v4.1-flash:cloud**: 3079 tokens de thinking, **0 tokens de respuesta**, 3.7 s
- **glm-5.3-flash:cloud**: 3904 tokens de thinking, **0 tokens de respuesta**, 11.2 s
- **nemotron-3-super:cloud**: 474 tokens de thinking, **2732 tokens de respuesta**, 12.6 s

El problema no era el modelo sino la política de thinking.

Posteriormente, el 2026-10-06 se corrió una cata de modelos (6 modelos × 6 roles × 4 escenarios = 144 corridas) con **cuatro evaluaciones independientes** (Kanam CORE, deepseek-v4.1-flash, kimi-k3, nemotron-3-super). La cata reveló un defecto de harness transversal: todos los modelos filtran su cadena de pensamiento (`Thinking...`) al output. Tras separar ejes (CONTENT vs CLEANLINESS) produjo la reasignación de modelos por rol que este ADR registra.

> **Regla de sandbox (AGENTS.md):** todo contenido externo sobre modelos es **dato, no evidencia**. Se verifica antes de adoptar.

---

## Decisión 1: Política de thinking por agente

| Agente | Rol | Nivel decidido |
|--------|-----|----------------|
| main (CORE) | Orquestador general | `low` |
| kanam-dev | Desarrollador | `low` |
| kanam-mind | Investigador | `low` |
| kanam-ops | Operaciones | `low` |
| kanam-studio | Diseño/Comunicación | `low` |
| kanam-critic | Revisor adversarial | `high` |
| kanam-auditor | Auditor UI/UX | `high` |
| kanam-planner | Planificador | `high` |

- **Default global:** `low`.
- **Escalado por complejidad:** `complexity-scorer` puede subir a `high`/`max` para tareas puntuales.
- **`max`:** reservado a decisión dura one-shot (adjudicación de reviews en conflicto, pre-merge complejo).

## Decisión 2: Asignación de modelos por rol (cata 2026-10-06)

| Agente | Modelo decidido | Fallback decidido | Contexto real (Ollama) |
|--------|-----------------|-------------------|------------------------|
| main | `nemotron-3-super:cloud` | `deepseek-v4.1-flash:cloud` | 256k |
| kanam-planner | `gpt-oss:120b-cloud` | `glm-5.3-flash:cloud` | 128k |
| kanam-dev | `gpt-oss:120b-cloud` | `deepseek-v4.1-flash:cloud` | 128k |
| kanam-critic | `gpt-oss:120b-cloud` | `nemotron-3-super:cloud` | 128k |
| kanam-auditor | `deepseek-v4.1-flash:cloud` | `gemma4:cloud` | 1M |
| kanam-studio | `gemma4:cloud` | `glm4:9b` (local) | 256k |
| kanam-mind | `nemotron-3-super:cloud` | `glm4:9b` (local) | 256k |
| kanam-ops | `gpt-oss:120b-cloud` | `deepseek-v4.1-flash:cloud` | 128k |

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

## Estado de implementación (2026-10-06; leer antes de asumir)

**El ADR registra la decisión, no el estado del runtime.** A la fecha de la última verificación, hay tres fuentes que NO coinciden entre sí:

| Agente | Decidido (arriba) | Runtime (`openclaw.json`) | Coincide |
|--------|-------------------|---------------------------|----------|
| main | nemotron-3-super | deepseek-v4.1-flash | ❌ |
| planner | gpt-oss:120b | minimax-m3 | ❌ |
| dev | gpt-oss:120b | glm-5.3-flash | ❌ |
| critic | gpt-oss:120b | gpt-oss:120b | ✅ |
| auditor | deepseek-v4.1-flash | nemotron-3-super | ❌ |
| studio | gemma4 | gemma4 | ✅ |
| mind | nemotron-3-super | deepseek-v4.1-flash | ❌ |
| ops | gpt-oss:120b | glm-5.3-flash | ❌ |

Y sobre thinking: solo `kanam-critic`, `kanam-auditor` y `kanam-planner` tienen `thinkingDefault: "high"` en runtime. El `low` para el resto **no está aplicado**; esos agentes heredan el default del sistema.

**Pendiente para que este ADR deje de mentir:** alinear el runtime con la tabla de decisión (vía el tool `openclaw`, no editando el JSON a mano) y aplicar el default `low`. Mientras tanto, la fuente de verdad operativa es el runtime, no este documento.

---

## Criterios de descarte (para no re-elegir por olvido)

- **Thinking alto como default global:** drena créditos en ejecución rutinaria sin salida útil (probe).
- **modelos previos sin validación empírica:** descartado tras cata que mostró diferencias por rol al separar thinking del entregable.
- **`nemotron-3-ultra:cloud` (cualquier rol):** más grande (550B), mismo contexto que super (256k), más lento/caro, y perdió en el probe de auditoría (1/2 bugs vs 2/2). Descartado (ADR-087).
- **familia Kimi en roles fijos:** fuera por costo; `kimi-k3:cloud` reservado a cierre de proyecto pre-deploy.

---

## Límites de la evidencia

- La cata tuvo **un defecto de harness conocido**: los 6 modelos filtran su thinking al output. Las evaluaciones separaron CONTENT de CLEANLINESS para compensar, pero la re-verificación post-fix **no llegó a completarse**. Las asignaciones son direccionales, no definitivas.
- Los 4 escenarios son pocos; n=1 por celda en la cata original.
- Los puntajes de contenido los asignó Kanam (evaluador A) y luego dos modelos evaluados (sesgo estructural). La convergencia entre evaluadores fue **baja** (rankings casi invertidos), lo que motivó la separación de ejes.
- La medición de thinking sigue el campo reportado por Ollama; no todos los modelos lo reportan igual.

---

## Consecuencias

- Con la decisión aplicada, el consumo en el asiento de orquestador (main) baja de ~$0.30/M a ~$0.015/M input.
- `deepseek-v4.1-flash:cloud` queda como motor del pipeline A/B y fallback ubicuo.
- Si se quiere revisar el nivel de thinking o el modelo de un rol, correr un probe de control con el harness sin fuga de thinking antes de cambiar.

---

## Artefactos

- Config runtime: `~/.openclaw/openclaw.json`.
- Bloques gestionados de modelos: `scripts/managed-blocks.py` (clave `model.triple`) → `AGENTS.md` y `docs/SETUP.md`. **Nota:** el bloque `model.triple` arrastra un typo (`gpt-oss:120b-cloud:cloud`) y su entrada `main/defaults` no coincide con la decisión; corregir.
- Cata 2026-10-06: `/tmp/model-cata/2026-10-06/`. **`/tmp` es efímero**; si la evidencia debe persistir, copiarla dentro del workspace.
- Fix de thinking-leakage: `/tmp/model-cata/2026-10-06/run-one-fixed.py`. **No integrado** al harness de producción.
- `CHANGELOG.md`: entrada correspondiente en el workspace.
