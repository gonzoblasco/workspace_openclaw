# ADR-043: Complexity-Driven Pipeline (Orquestación por T-Score)

**Status:** Accepted (2026-08-31)
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-08-31
**Origen:** workspace (sesión 2026-08-30/31, cierre de proyecto)

## Contexto

El pipeline A/B de programación (Kanam planifica → Agente A escribe → Agente B revisa) trataba **todas las tareas igual**: mismo modelo, mismo nivel de thinking, misma profundidad de pipeline. Esto generaba dos problemas opuestos:

1. **Sobre-ingeniería:** tareas triviales (cambiar un color, corregir un typo) pasaban por el pipeline completo A+B, gastando 2-3 modelos y tiempo sin ganancia de calidad.
2. **Sub-ingeniería:** tareas críticas (migrar DB de producción, recrear billing) podían no recibir la verificación obligatoria ni el gate de confirmación que merecen por riesgo.

La regla del 2026-08-30 (`prompts/complexity-scorer.md`) ya intuía la solución (evaluar complejidad en 4 dimensiones) pero **nunca quedó cableada al pipeline real**. Estaba documentada, no ejecutada.

## Decision

**Antes de spawnear cualquier agente, Kanam ejecuta un evaluador de complejidad que produce un T-score (1-20) y con eso decide modelo, thinking, y profundidad del pipeline.**

### Dimensiones del score

Cada dimensión se puntúa 1-5; `T = A + B + C + D` (4-20):

| Dim | Nombre | 1 (bajo) | 5 (alto) |
|-----|--------|----------|----------|
| A | Alcance | un archivo | multi-repo |
| B | Abstracción | fix trivial | diseño de sistema |
| C | Riesgo | cosmético | crítico / pérdida de datos |
| D | Ambigüedad | cristalino | abstracto |

### Buckets y pipeline resultante

| T | Bucket | Pipeline | Thinking |
|---|--------|----------|----------|
| 1-6 | trivial | Kanam solo, sin agentes | off |
| 7-12 | low | Agente A escribe → Kanam revisa | high |
| 13-16 | medium | A escribe → B cross-review → Kanam aprueba | high |
| 17-20 | high | Kanam(max) diseña → A(high) ejecuta → B(high) revisa → verificación obligatoria | max (solo Kanam) |

### Escalada por riesgo (calibración 2026-08-31)

Si `C >= 4` **y** `T >= 14`, forzar bucket `high` (marca `escalated=1`), aunque la baja ambigüedad (D) deje el total < 17.

**Racional:** la ambigüedad (D) se puede clarificar preguntando; el riesgo de pérdida de datos de producción (C) no. Una tarea "clara pero peligrosa" (ej. migrar la DB de prod a sharding) no debe caer abajo del umbral solo porque sabe qué hacer.

### Cadena de modelos del scorer

El evaluador usa `gemma4:e4b-mlx` local primero (6.7x más rápido que qwen3.5, benchmark 2026-08-30), con fallbacks a `deepseek-v4.1-flash:cloud` → `gemma4:cloud` → `qwen3.5:9b-mlx`. El modelo de trabajo del pipeline (que escribe el código) es otro: `deepseek-v4.1-flash:cloud` default. El scorer local solo calcula el T-score.

## Implementación

- **`scripts/complexity-scorer.sh`** - evaluador principal. Devuelve JSON con T-score, bucket, modelo, thinking, agents, pipeline, escalada.
- **`scripts/complexity-parse.py`** - parser externo. Maneja JSON estricto o texto de "thinking" en prosa (los modelos locales ponen la respuesta en `thinking`, no en `response`, y cortan el JSON por `done_reason: length`).
- **`scripts/pipeline-track.sh`** - acepta `--score T` en `init` para persistir el score durable del run.
- **`skills/complexity-driven-pipeline/SKILL.md`** - skill que documenta el workflow completo.
- **`prompts/complexity-scorer.md`** - fuente única de verdad de las reglas; el script construye su system prompt a partir de ahí.
- **Integración session-lifecycle:** `session-start.sh` corre el scorer al iniciar sesión y persiste el T-score en el daily; `session-end.sh` lo recupera al cerrar. El daily queda con el T-score en inicio y fin.

## Consecuencias

- **Positivas:**
  - Tareas triviales ya no gastan pipeline completo (ahorro ~15 min/sesión).
  - Tareas críticas siempre reciben verificación + gate de confirmación de Gonzo (T≥17).
  - Decisión de complejidad es reproducible y auditable, no por intuición.
  - Cada sesión persistee el T-score en el daily → dataset de calibración automático.

- **Limitaciones asumidas:**
  - El T-score es una heurística del LLM evaluador, no una medida exacta. Puede requerir re-calibración periódica (el caso sharding mostró un falso "medium" que la escalada por riesgo corrigió).
  - Depende de que gemma4:e4b-mlx (o un fallback) esté disponible; si todos los modelos fallan, el scorer cae a `--score T` forzado manual.

## Alternativas

- **Pipeline fijo A/B para todo:** descartado. Desperdicia recursos en triviales y no protege los críticos.
- **Evaluación manual por intuición de Kanam:** descartado. No es reproducible, no deja trailing, y sesga según la fatiga o el contexto del momento.
- **Umbral lineal simple (sin escalada por riesgo):** descartado tras la calibración con 15 tareas. El caso "migrar DB a sharding" (T=16, C=5, D=1) probó que la suma lineal subestima tareas peligrosas pero claras.

## Validación (calibración 2026-08-31)

Corridas 15 tareas reales, de "cambiar el color de un botón" (T=4) a "recrear billing multi-tenant" (T=18):

- 14/15 correctas sin ajuste.
- 1 anomalía ("migrar DB a sharding multi-region", T=16 en vez de high) → resuelta con la regla de escalada por riesgo.
- Los 3 buckets extremos (trivial/low/medium/high) discriminaron bien en todo el espectro.

---

*Cierre de proyecto `complexity-driven-pipeline`. Registrado sesión 2026-08-30/31 en daily + DB.*

## Actualizacion 2026-09-29 - retiro de `deepseek-v4-flash`

`deepseek-v4-flash:cloud` fue **retirado por Ollama el 2026-09-25** (verificado con el daemon:
`ollama show deepseek-v4-flash:cloud` responde `was retired at 2026-09-25 00:00:00 -0700 PDT`,
ref `7e00c916-e009-455f-aa4c-f6f64a81a6bd`). Su lugar como motor de los agentes A/B del pipeline
lo ocupa **`deepseek-v4.1-flash:cloud`**, que deja de ser "fase de escalada" y pasa a ser el
reemplazo (la escalada sigue siendo `glm-5.3-flash:cloud`). Este ADR se conserva como registro de
la decision vigente a su fecha; las referencias a v4-flash que quedan en el texto son historicas.
