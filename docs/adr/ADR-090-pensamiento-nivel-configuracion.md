# ADR-090: Política de niveles de pensamiento por agente y asignación de modelos por rol

**Fecha:** 2026-10-14 (corregido 2026-10-18; rol `main` reasignado 2026-10-20 por ADR-102; reasignado otra vez 2026-10-28 por ADR-107; tabla corregida 2026-11-04)
**Estado:** Aceptado (verificado contra el runtime 2026-11-04 tras la correccion de planner/studio)
**Decisores:** Gonzo / Kanam
**Origen:** cata por rol (2026-10-06, `docs/ecosystem/cata-por-rol-modelos-2026-10-05.md + benchmarking Nemotron (2026-10-14)
**Relacionado:** la cata por rol (evidencia en `docs/ecosystem/`), ADR-088 (pipeline A/B enforcement), ADR-089 (pre-filtro A/B), **ADR-107 (swap deepseek/minimax en CORE y defaults, vigente)**
**Supersede:** la política de asignación de modelos por tarea anterior a la cata (los ADRs de modelo previos quedaron retirados)

---

## Contexto

Un probe de orquestación (2026-10-05) reveló que el thinking alto por defecto consumía presupuesto sin producir respuesta útil. La cata por rol del 2026-10-06 reasignó modelos por agente con evidencia. Un benchmarking posterior (2026-10-14) comparó Nemotron 3 Super/Ultra vs DeepSeek V4.1 Flash y **propuso** migrar la mayoría de los roles a `nemotron-3-super:cloud` - pero esa asignación **nunca se aplicó al runtime**: una versión anterior de este ADR la declaraba "aplicada y verificada" y era falsa (detectado por el review K3 del 2026-10-18).

## Decisión

### 1. Asignación de modelos por rol (VIGENTE, verificada 2026-10-28)

Fuente de verdad: `openclaw.json` + tabla `settings` de `memory.db` (`model_by_agent`, bloque managed `model-operativo` en `AGENTS.md`). Tres fuentes coinciden.

**Cambio del 2026-10-28 (ADR-107):** el rol `main` (CORE) y los defaults de agente vuelven a `deepseek-v4.1-flash:cloud` con fallback `minimax-m3.1-flash:cloud`. Motivo: ahorro medido de ~20% de cuota en uso real. ADR-102 (minimax en el CORE) queda **superseded**; la cata que lo fundó (8.9 vs 7.8 en `main`) sigue siendo la medición del modelo, pero dejó de justificar la asignación.

**Correccion del 2026-11-04 (decision de Gonzo):** dos filas de esta tabla no coincidian con el runtime y una contradecia al ADR de modelo visual de STUDIO.

- **`studio` vuelve a `deepseek-v4.1-flash:cloud`.** Esta tabla lo tenia en `gemma4:cloud`, pero el ADR de modelo visual de STUDIO (`docs/ecosystem/studio-modelo-visual.md`, 2026-09-28, Estado Aceptado, nunca superseded) habia decidido lo contrario con evidencia: `gemma4` **alucino un defecto de contraste** que medido daba 7,27:1. Las dos fuentes vigentes decian cosas distintas sobre el mismo rol; se resuelve a favor de la decision con evidencia medida.
- **Fallback de `studio`: `gemma4:12b-mlx` (local), no `glm-5.3-flash`.** El ADR de STUDIO pedia `glm-5.3-flash` para la pasada profunda, pero ese modelo cuesta **5,5x** deepseek por request (0,29 px/req medido). El fallback tiene que ser barato y existir en disco.
- **Fallback de `planner`: `gemma4:12b-mlx` (local), no `glm-5.3-flash`.** Esta tabla declaraba `glm-5.3-flash` y la config tenia `gemma4:cloud`: drift que nadie habia reconciliado. Se alinea al modelo local que existe.
- **`planner` conserva `gpt-oss:120b-cloud` como primario.** La cata del 2026-11-04 mostro que `deepseek` daba un umbral de cuota mas accionable, pero la diferencia no justifica mover un rol que funciona: se deja como estaba y se registra la medicion.

Las tres fuentes (config, `settings` de la DB y bloque managed) coinciden tras la correccion. Ojo con la DB: la misma tabla vive bajo **tres** claves (`model_by_agent`, `model_triple`, `model.triple`) y corregir solo las conocidas deja una copia viva del valor viejo.

**Drift corregido el 2026-10-20:** `agents.defaults.model.primary` decía `nemotron-3-super:cloud`, modelo que la tabla de este ADR nunca declaro (venia del benchmarking del 14/10 que no se adopto). Config, DB y bloques quedaban en tres valores distintos. Alineado en ese momento a `minimax-m3.1-flash:cloud`.

| Agente | Primario | Fallback | Thinking |
|--------|----------|----------|----------|
| main (CORE) | `deepseek-v4.1-flash:cloud` (desde 2026-10-28, ADR-107) | `minimax-m3.1-flash:cloud` | `off` |
| kanam-dev | `gpt-oss:120b-cloud` | `deepseek-v4.1-flash:cloud` | `off` |
| kanam-ops | `gpt-oss:120b-cloud` | `deepseek-v4.1-flash:cloud` | `off` |
| kanam-planner | `gpt-oss:120b-cloud` | `gemma4:12b-mlx` (local) | `low` |
| kanam-critic | `gpt-oss:120b-cloud` | `nemotron-3-super:cloud` | `low` |
| kanam-auditor | `deepseek-v4.1-flash:cloud` | `gemma4:cloud` | `low` |
| kanam-mind | `deepseek-v4.1-flash:cloud` | `gemma4:cloud` | `off` |
| kanam-studio | `deepseek-v4.1-flash:cloud` | `gemma4:12b-mlx` (local) | `off` |

**Pipeline A/B** (ADR-077/088/089): A `gpt-oss:120b-cloud` / B `deepseek-v4.1-flash:cloud`; pre-filtro `gemma4:cloud` (no autoriza solo: lo que toca lógica pasa siempre por B). Fuente operativa: `scripts/model-router.sh model pipeline_ab`.

**Criterio costo/beneficio (2026-10-18):** los roles de ejecución y orquestación de alto volumen corren `gpt-oss:120b-cloud` o `deepseek-v4.1-flash:cloud` según demanda de contexto; los roles de juicio con `low` thinking. Cambios de modelo se evalúan con una cata (skill `model-cata`) y se aplican **fuera** de una sesión que corra sobre el agente modificado.

### 2. Política de thinking por agente (VIGENTE, verificada 2026-10-18)

- `off` explícito para los cinco de ejecución: main, dev, ops, mind, studio.
- `low` para los tres de juicio: critic, auditor, planner.
- Default global: `off`.
- Escalado por complejidad: `complexity-scorer` puede subir a `high`/`max` puntualmente.
- `max`: reservado a decisión dura one-shot (adjudicación de reviews en conflicto, pre-merge complejo).

## Registro del benchmarking 2026-10-14 (NO aplicado - propuesta no adoptada)

El benchmarking midió Super/Ultra/Flash en 10 tareas representativas con thinking separado del entregable. Hallazgos válidos como dato:

- **Nemotron 3 Ultra (~550B):** sin ventaja de calidad sobre Super; timeouts en tareas de mayor alcance; mismo contexto (256k); más caro y lento. **Descartado para cualquier rol.**
- **Nemotron 3 Super (~120B):** el más rápido y fiable del set, <10% del coste de Flash por request. Sigue siendo candidato legítimo para roles de alto volumen si se re-evalúa con cata.
- **DeepSeek V4.1 Flash (~763B):** su ventana de 1M tokens es el diferenciador real para verificación profunda.

**Por qué no se adoptó la propuesta:** la asignación quedó escrita en el ADR pero nunca se aplicó a `openclaw.json` ni a la tabla `settings`; el bloque "Estado de implementación ✅" que la declaraba aplicada era falso. Lección registrada: **una asignación de modelos no está "decidida" hasta que config + DB + bloques gestionados coinciden y se verifica con `managed-blocks.py check`.**

## Criterios de descarte (para no re-elegir por olvido)

- **`nemotron-3-ultra:cloud` (cualquier rol):** más grande, mismo contexto que super, más lento/caro, perdió el benchmarking. Descartado.
- **Thinking alto como default global:** drena créditos en ejecución rutinaria sin salida útil (probe 2026-10-05).
- **Familia Kimi en roles fijos:** fuera por costo; `kimi-k3:cloud` reservado a trabajo profundo puntual autorizado por Gonzo (ej: el review de ADRs del 2026-10-18).

## Límites de la evidencia

- El benchmarking 2026-10-14 es direccional (n=1 por celda, tareas chicas, temperature 0). El runner final separó thinking de content vía `/api/chat` (sin fuga de razonamiento al entregable).
- Los puntajes de contenido los asignó Kanam como evaluador y se validaron separando los ejes CONTENT vs CLEANLINESS (`harness-model-comparison`).

## Regla de mantenimiento (2026-10-18)

**Este ADR describe el runtime; no lo prescribe.** Al cambiar un modelo por rol:

1. Aplicar el cambio al config (`openclaw.json`) fuera de la sesión del agente afectado.
2. Actualizar la tabla `settings` (`managed-blocks.py set model_by_agent "..."` + `apply`).
3. Reescribir la tabla de este ADR con la fecha de verificación.
4. Correr `managed-blocks.py check` y confirmar que config = DB = bloques = ADR.

Si las cuatro fuentes no coinciden, el corpus miente: eso es un defecto ALTA, no una deriva aceptable.

## Correccion estructural 2026-11-17: una sola clave

La advertencia de §1 ("la misma tabla vive bajo tres claves y corregir solo las conocidas deja
una copia viva del valor viejo") se cumplio dos veces el 2026-11-04 y una tercera entre el 04 y
el 16: `model.triple` conservo `minimax-m3.1-flash`, el valor superseded por ADR-107, doce dias.
Alinear las tres claves no alcanzaba: tres valores iguales siguen siendo tres duenos.

Decision (pedido explicito de Gonzo, 2026-11-17):

- **Se borran `model_triple` y `model.triple` de `settings`.** Queda `model_by_agent`, la clave
  que lee el bloque `model-operativo` de `AGENTS.md`. Ningun bloque ni script lee las otras dos.
- **`managed-blocks.py set` escribe una sola clave.** Acepta un alias como *nombre de entrada*
  (lo resuelve al canonico y avisa), nunca como destino: escribir los dos es lo que mantenia el
  duplicado vivo.
- **`managed-blocks.py retire-aliases [--force]`** borra las copias y **se frena si un alias
  difiere del canonico**: una copia con otro valor es una decision que alguien perdio, no basura.
- **`seed` nunca crea un alias.** Una clave que ningun bloque lee no es un default.
- **`scripts/check-settings-aliases.py` invierte su regla:** antes exigia que las tres claves
  coincidieran; ahora exige que **no exista** ninguna copia. Si una reaparece, el gate falla con
  el nombre de la clave y el valor.

Verificado en negativo: sembrar un `model.triple` a mano hace fallar el gate; `retire-aliases`
lo limpia; un `set` posterior deja la DB en 10 claves y el gate en verde; los seis bloques
managed siguen rindiendo sin drift.

## Artefactos

- Config runtime: `~/.openclaw/openclaw.json` (verificado 2026-10-18).
- Bloques gestionados: `scripts/managed-blocks.py` (claves `model_by_agent`, `thinking_default`; **`model.triple` se retiro el 2026-11-17**, ver abajo) → `AGENTS.md` (bloques `model-operativo`, `pipeline-ab`) y `docs/SETUP.md` (bloque `model-triple`, que toma `model_primary`/`model_auxiliary`/`model_alternative`).
- Benchmarking 2026-10-14 (registro): `model_comparison_final.md`, `super_20261014_232744.json`, `nemotron_ultra_full_20261014_222950.json`, runner `bench_model_suite.py` (workspace, sin commitear).
- Review que detectó la derivación: `docs/records/2026-10-18-review-profundo-adrs.md`.