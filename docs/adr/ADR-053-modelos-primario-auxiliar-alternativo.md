# ADR-053: Modelos primario, auxiliar y alternativo (thinking HIGH unificado)

**Fecha:** 2026-09-22
**Estado:** Aceptado
**Decisores:** Gonzo (definicion explicita)
**Origen:** workspace (definido por Gonzo el 2026-09-22; el config habia derivado por cambios sin registrar)
**Relacionado:** ADR-040 (seleccion por tipo de tarea), ADR-041 (motor LLM GLM-5.3), ADR-045/046 (motor del pipeline), ADR-049 (Claude Code como motor A/B)
**Supersede:** la seccion de default/utility de ADR-040 y el apartado "Modelo definitivo" (Kanam MAX) de ese mismo ADR

---

## Contexto

Al auditar los ADRs contra el estado real (2026-09-22) aparecieron tres divergencias entre lo documentado y lo que el gateway corria:

| Aspecto | Documentado | Estado real (antes de este ADR) |
|---|---|---|
| Modelo primario | ADR-041: GLM-5.3-Flash | `ollama/minimax-m2.7:cloud` |
| Modelo auxiliar | ADR-041: GLM como fallback + vision | `ollama/gemma4:31b-cloud` |
| Thinking | ADR-040: Kanam en MAX | `high` |

El primario habia rotado cuatro veces en cinco dias sin decision registrada (`gpt-oss:120b` -> `gemma4:cloud` -> `minimax-m2.7`), y **ADR-040 linea 157 excluia explicitamente `minimax-m2.7`** del config automatico ("no aportan valor diferencial"). El thinking estaba en `high` desde al menos el 19/09, tambien sin registro.

Gonzo definio la configuracion objetivo explicitamente el 2026-09-22.

---

## Decision

1. **Modelo primario:** `deepseek-v4.1-flash:cloud`.
2. **Modelo auxiliar:** `gemma4:cloud` (tareas utilitarias).
3. **Modelo alternativo (fallback):** `glm-5.3-flash:cloud`.
4. **Thinking: `high` para todos los roles.** Se unifica en HIGH deliberadamente "para no gastar recursos innecesarios"; la ventaja de MAX no se considera necesaria hoy.

### Aplicado

Via `openclaw config patch` (8 updates, sin restart), en `~/.openclaw/openclaw.json`:

```
agents.defaults.model.primary      = ollama/deepseek-v4.1-flash:cloud
agents.defaults.model.fallbacks    = [ollama/glm-5.3-flash:cloud]
agents.defaults.utilityModel       = ollama/gemma4:cloud
agents.defaults.thinkingDefault    = high
agents.entries.main.model.primary  = ollama/deepseek-v4.1-flash:cloud
agents.entries.main.model.fallbacks= [ollama/glm-5.3-flash:cloud]
```

La allowlist `agents.defaults.models` no incluia ninguno de los tres modelos (solo `minimax-m2.7` y `openrouter/auto`); se agregaron los tres. Verificado live: `openclaw models status --plain` reporta `ollama/deepseek-v4.1-flash:cloud`.

### Verificacion de disponibilidad de modelos (2026-09-22)

Los tres modelos se probaron end-to-end contra el daemon: `deepseek-v4.1-flash:cloud`, `gemma4:cloud` y `glm-5.3-flash:cloud` respondieron `OK`.

**Ojo con la nomenclatura: la lista local y el catalogo cloud NO coinciden.** Un modelo puede no aparecer en `ollama list` y existir igual en Ollama Cloud, y viceversa, con nombres distintos:

| Local (`ollama list`) | Cloud (`ollama.com/api/tags`) |
|---|---|
| `gemma4:cloud` | `gemma4:31b` |
| `qwen3.5:cloud` | `qwen3.5:397b` |
| ~~`deepseek-v4-flash:cloud`~~ (retirado 2026-09-25) | ~~`deepseek-v4-flash:0731`~~ |
| `deepseek-v4.1-flash:cloud` | `deepseek-v4.1-flash` |

El catalogo cloud autoritativo es `https://ollama.com/api/tags` (20 modelos al 2026-09-22); el local es `curl -s http://127.0.0.1:11434/api/tags`. Los proveedores en config son `ollama` y `ollama-local` (daemon `11434`) y `ollama-cloud` (`https://ollama.com`). Antes de declarar un modelo inexistente, chequear AMBAS listas.

Nota de test: pedirle a un modelo con thinking activo una respuesta corta con `num_predict` bajo puede devolver contenido vacio porque el presupuesto se consume en el bloque `thinking`; no es un fallo del modelo. Verificar con presupuesto amplio o `stream:false` sin `num_predict`.

---

## Consecuencias

### Positivas
- El config vuelve a estar alineado con un ADR. Se cierra el drift de cinco dias.
- `minimax-m2.7` deja de correr como primario, lo que reconcilia el estado con la exclusion que ADR-040 ya declaraba.
- Un solo nivel de thinking (HIGH) simplifica: no hay que decidir nivel por rol ni mantener dos politicas.

### Negativas
- **Se pierde la distincion REVISAR/ADMINISTRAR vs CREAR/AVANZAR** que justificaba MAX en el orquestador (ADR-040). Consecuencia concreta y ya observada: la sesion de auditoria del 2026-09-22 corrio en HIGH, y fue exactamente una tarea de decision/critica (analisis de deuda de ADRs). Ese es el caso de uso donde MAX estaba pensado.
- `minimax-m2.7` sale del flujo; si en el futuro se quiere su perfil de concision, se convoca explicitamente.

### Regla de actualizacion
- Este ADR es la fuente de la verdad del primario/auxiliar/alternativo y del nivel de thinking.
- Cualquier cambio futuro de estos valores se documenta con un ADR que supersede a este, no editando el config por debajo.

---

## Alternativas consideradas

1. **Mantener Kanam en MAX y agentes en HIGH** (ADR-040): es la regla previa, mas granular, pero implica administrar dos niveles y consumir mas recursos. Gonzo la reemplazo explicitamente por HIGH unificado. Rechazada.
2. **Dejar `minimax-m2.7` como primario** y actualizar ADR-040 para admitirlo: reconcilia el config con la realidad actual, pero no es lo que Gonzo definio. Rechazada.
3. **Solo documentar el drift sin corregir el config:** deja el ADR describiendo algo que no corre, que es el problema que este ADR existe para cerrar. Rechazada.

## Actualizacion 2026-10-05 - distribucion por agente (supersede del trio)

La distribucion primario/auxiliar/alternativo de este ADR quedo **superseded** por la
distribucion por-agente del 2026-10-05 (config + AGENTS.md): cada rol tiene `model.primary`
+ `fallbacks` explicitos en `agents.entries` (main glm-5.3-flash, dev deepseek-v4.1-flash,
auditor nemotron-3-super, critic gpt-oss:120b, planner minimax-m3, mind deepseek-v4.1-flash,
ops glm-5.3-flash, studio gemma4; fallbacks en glm-5.3-flash, con locales glm4:9b para ops/studio).
El pipeline A/B mantiene su pareja asimetrica según ADR-077 (A gpt-oss:120b / B deepseek-v4.1-flash).

## Actualizacion 2026-09-29 - retiro de `deepseek-v4-flash`

`deepseek-v4-flash:cloud` fue **retirado por Ollama el 2026-09-25** (verificado con el daemon:
`ollama show deepseek-v4-flash:cloud` responde `was retired at 2026-09-25 00:00:00 -0700 PDT`,
ref `7e00c916-e009-455f-aa4c-f6f64a81a6bd`). Su lugar como motor de los agentes A/B del pipeline
lo ocupa **`deepseek-v4.1-flash:cloud`**, que deja de ser "fase de escalada" y pasa a ser el
reemplazo (la escalada sigue siendo `glm-5.3-flash:cloud`). Este ADR se conserva como registro de
la decision vigente a su fecha; las referencias a v4-flash que quedan en el texto son historicas.
