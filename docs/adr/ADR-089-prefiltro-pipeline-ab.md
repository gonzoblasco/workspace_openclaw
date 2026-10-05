# ADR-089: Pre-filtro barato en el pipeline A/B (gemma4:cloud) con guard de falso negativo

**Fecha:** 2026-10-05
**Estado:** Aceptado
**Decisores:** Gonzo (pedido explicito: "deepseek como principal pero con un pre-filtro con gemma4:cloud")
**Origen:** Sesion 2026-10-05 - tras la cata del rol B (local vs cloud), Gonzo pidio optimizar el consumo de Ollama Cloud sin bajar la calidad del review.
**Relacionado:** ADR-077 (pipeline A/B asimetrico), ADR-088 (su enforcement), ADR-087 (cata por rol)

---

## Contexto

El rol **B** del pipeline A/B revisa con `deepseek-v4.1-flash:cloud` (ADR-077). Gonzo pregunto si un modelo local mas barato podia reemplazarlo para optimizar el consumo de Ollama Cloud.

Se midio (misma tarea de review con **3 defectos reales**, temperature 0):

| Modelo | Defectos reales | Falsos positivos | Tiempo | Entra en GPU |
|---|---|---|---|---|
| `deepseek-v4.1-flash:cloud` (B actual) | **3/3** | **0** | 3.2 s | nube |
| `gemma4:cloud` | 2/3 | 0 | **0.9 s** | nube |
| `gemma4:12b-mlx` (local) | 2/3 | 0 | 12 s | 19 GB |
| `glm-4.7-flash:q4_K_M` (local, 29.9B) | 2/3 | 3 | 47 s | offload CPU |
| `mistral-small3.2:24b` (local) | 1/3 | 2 | ~25 s | 15 GB |
| 9B locales (glm4, ornith, qwen) | <=1/3 | 1-2 | 8-25 s | si |

**Hallazgo central:** **ningun local reemplaza a deepseek.** El unico modelo que atrapa el defecto **semantico** (el `Math.min` que hace inalcanzable la rama `over` de `FitBar` - codigo muerto que el build y los tests no ven) es deepseek. `gemma4` (cloud y local) encuentra los 2 defectos **estructurales** (ESM `__dirname`, CSS huerfano) con **0 falsos positivos**, pero **se le escapa el semantico**.

> Ese falso negativo esta medido y es estable (3 corridas de `gemma4:cloud`: identicas). Es la razon de ser del guard de abajo.

## Decision

**B se queda en `deepseek-v4.1-flash:cloud` (el gate que decide).** Se le suma un **pre-filtro** `gemma4:cloud` que corre primero.

Ruta de modelos (fuente de verdad: `scripts/model-router.sh`):

```
pipeline_ab           -> gpt-oss:120b-cloud / deepseek-v4.1-flash:cloud   (A escribe / B decide)
pipeline_ab_prefilter -> gemma4:cloud
```

Flujo al delegar una revision:

```
1. PRE-FILTRO: gemma4:cloud revisa primero (~1s, ~170 tok). Triage rapido.
2. GATE: deepseek-v4.1-flash:cloud revisa y DECIDE. Su veredicto es el que vale.
   - Si el pre-filtro marco candidatos, deepseek los adjudica + su pasada independiente.
```

### Guard de falso negativo (la parte que evita bajar la vara)

El pre-filtro **no autoriza solo**. Por su FN medido en defectos semanticos:

- **Cambios que tocan logica / comportamiento / semantica:** pasan **SIEMPRE** por deepseek, aunque el pre-filtro diga "limpio".
- **Cambios puramente estructurales** (CSS, estilos, docs, config de formato) que el pre-filtro marca limpios: se puede omitir deepseek. Ahi el pre-filtro es confiable porque el FN observado no aplica a esa clase de cambio.

El ahorro de cloud viene de esa segunda clase; la calidad no baja porque la clase donde gemma4 falla nunca se saltea.

## Consecuencias

- **Consumo de Cloud:** en cambios estructurales limpios, se evita la llamada a deepseek. En todo lo que toca logica, el consumo es el de antes (mas ~1s/~170 tok del pre-filtro, despreciable).
- **El pre-filtro es de `gemma4:cloud`, no del local.** El local 12b hace lo mismo pero 13x mas lento y ocupando GPU; el cloud es ~1s y no toca recursos locales.
- **El enforcement de ADR-088 se extiende:** el gate `check-pipeline-enforcement.py` ahora tambien verifica que la ruta `pipeline_ab_prefilter` este declarada y sea consistente.
- **No se cambia el rol B ni el motor A.** Este ADR no supersede ADR-077: le suma una etapa de triage con su guard.

## Limites de la evidencia

- **Un tipo de tarea de review** (3 defectos, un diff chico), temperature 0. Es direccional: marca que gemma4 **no** es autorizante en semantica, no una rubrica completa.
- El FN podria no ser uniforme en diffs largos; el guard es conservador a proposito (ante la duda, deepseek corre).

## Artefactos

- `scripts/model-router.sh` - ruta `pipeline_ab_prefilter`.
- `scripts/managed-blocks.py` - setting `model_pipeline_prefilter` + bloque de AGENTS.md.
- `scripts/check-pipeline-enforcement.py` - verifica el pre-filtro.
- `sandbox/b-pipeline-cata/` (gitignored) - harness de la cata.
