# ADR-076: Ningun agente hereda un modelo local (cloud primero, locales como ultimo recurso)

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** sesion 2026-09-28 - un job de automatizacion fallaba por un modelo local que ya no estaba instalado
**Relacionado:** ADR-049 (Claude Code motor A/B), ADR-077 (pipeline A/B asimetrico), ADR-090 (la asignación de modelos por rol vigente, posterior a este ADR)
**Supersede:** la parte de `defaults.model` de la política de modelos vigente en 2026-09-28 (hoy retirada)

---

## Contexto

Gonzo, textual: **"estamos priorizando los modelos en la nube... los locales son solo para cuando no hay salida"**. Y un dato duro: **Gemma4:26B ya no esta instalado**.

El estado real estaba roto de una forma no obvia:

| Clave | Valor | Problema |
|---|---|---|
| `agents.defaults.model.primary` | `ollama/gemma4:26b` | Modelo **local** y **desinstalado** |
| `kanam-mind` | sin bloque `model` | **Heredaba** el default roto |
| `kanam-studio` | sin bloque `model` | **Heredaba** el default roto |

El mecanismo que hace esto no evidente: un agente **sin** bloque `model` no se queda sin modelo, **hereda `agents.defaults.model.primary`**. Por eso `kanam-mind` y `kanam-studio` eran los dos unicos agentes sin modelo explicito y los dos unicos montados sobre un modelo local inexistente.

**Sintoma en produccion:** `skill-collection-review:kanam-mind` fallaba con `prepared model runtime owner was not published`. `gateway-jobs-watcher` acumulo 15 corridas fallidas con `timeout en model-call-started`. La causa no era el job ni su timeout: era el modelo.

## Decision

**1. Ningun agente hereda ni define un modelo local como primario.** Cada agente tiene su `model.primary` explicito, o hereda un default que ya es cloud.

**2. Los modelos cloud van primero; los locales son el ultimo recurso.** El orden de `fallbacks` refleja esa prioridad: los cloud primero, los locales **instalados** al final.

**3. Un modelo citado en el config que no aparece en `ollama list` no puede ser primary ni fallback.** Falla en el momento de la llamada.

### Aplicado (verificado con `gateway config.get`)

| Clave | Antes | Despues |
|---|---|---|
| `defaults.model.primary` | `ollama/gemma4:26b` (local, ausente) | `ollama/gpt-oss:120b-cloud` |
| `main.model.primary` | `ollama/qwen3.8:27b-mlx` (local) | `ollama/deepseek-v4.1-flash:cloud` |
| `kanam-mind.model.primary` | (hereda) | `ollama/gpt-oss:120b-cloud` |
| `kanam-studio.model.primary` | (hereda) | `ollama/gpt-oss:120b-cloud` |

- Fallbacks de `main`: 27 -> 13. Los 9 cloud primero; despues los 4 locales **instalados**.
- Limpiadas 8 referencias a modelos no instalados (incluido `gemma4:26b`) de `fallbacks`, `modelPolicy.allow`, `models` y definiciones de proveedor.

### Resultado medido

Forzando la corrida de los dos jobs que fallaban, sin esperar el schedule:

| Job | Antes | Despues | Modelo efectivo |
|---|---|---|---|
| `gateway-jobs-watcher` | error (15 corridas) | **ok** | `deepseek-v4.1-flash:cloud` |
| `skill-collection-review:kanam-mind` | error | **ok** | `gpt-oss:120b-cloud` |

**El diagnostico era correcto: la causa era el modelo, no el job.**

## Correccion 2026-09-28 (misma sesion): el primary explicito SIN `fallbacks` clobbea los defaults

El fix de arriba introdujo una **regresion propia** que `doctor` detecto despues:

```
agents.entries.kanam-ops.model is { primary: "ollama/gpt-oss:120b-cloud" },
a object with no explicit "fallbacks" key. At runtime this clobbers
agents.defaults.model.fallbacks (ollama/deepseek-v4.1-flash:cloud,
ollama/gemma4:cloud), leaving the agent with no fallbacks.
```

Tres agentes (`kanam-dev`, `kanam-mind`, `kanam-ops`) quedaron con `primary` y **sin `fallbacks`**, y eso **no hereda**: pisa los defaults y los deja **sin ninguno**. Es el mismo tipo de error que el ADR venia a arreglar (un agente con un modelo roto sin red de contencion), reintroducido por la via opuesta.

**Corregido:** se les agrego `fallbacks` explicito, cloud-first y alineado con los defaults:

```
["ollama/deepseek-v4.1-flash:cloud", "ollama/glm-5.3-flash:cloud", "ollama/gemma4:cloud"]
```

Verificado: `doctor` ya no reporta el defecto.

**Leccion:** un `primary` explicito **no** hereda los `fallbacks` del default; los reemplaza. Al fijar un modelo por agente, declarar **siempre** la pareja `primary` + `fallbacks`. Un agente con primary y sin fallbacks queda mas fragil que antes del cambio que buscaba endurecerlo.

## Excepcion: embeddings

Los embeddings quedan en local (`qwen3-embedding:0.6b`, provider `ollama-local`). Son otra clase de tarea, corren bien en local y migrarlos encarece cada busqueda sin ganancia. Registrado como TODO por si el owner quiere revisarlo.

## Consecuencias

- **El cambio no requiere restart del gateway:** `config.get` refleja el valor nuevo sin reiniciar.
- Backup del config previo: `openclaw.json.bak-20260928-112321-pre-cloud-models`.
- **Via usada:** edicion directa del JSON con python (backup + validacion + `config.get` + `--accept` del baseline de drift). NO la herramienta `gateway`: un intento con `update.run` paso `path`/`value` que no son parametros de esa accion y disparo una actualizacion de version de OpenClaw sin querer.
- Un cambio de config medido antes **queda stale** en cuanto se agregan o quitan modelos. Re-medir, no confiar en la medicion previa.

## Skill relacionada

`model-config-policy` - el procedimiento completo de enumerar, separar cloud de local, poner explicito y verificar forzando la corrida del consumidor.
