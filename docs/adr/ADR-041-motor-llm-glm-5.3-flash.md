# ADR-041: Motor LLM del Sistema - GLM-5.3-Flash (Manual de Modelo)

**Status:** Accepted (2026-08-29)
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-08-29
**Origen:** workspace (comparativa empirica de 5 modelos, 2026-08-29, prompt de arquitectura de agentes)
**Complementa:** ADR-040 (Seleccion de Modelos por Tipo de Tarea). Su parte de defaults/fallbacks queda actualizada por este ADR.

## Decision

**GLM-5.3-Flash es el motor del sistema:** default de OpenClaw y motor de los agentes A/B del pipeline. DeepSeek V4 Flash queda FUERA del ecosistema (ver rollback).

**Regla de parametros: a GLM-5.3-Flash se le pasa CERO parametros de razonamiento.** Sin `reasoning_effort`, sin thinking config, sin knobs. Corre con el default del servidor. Razones:

1. Ollama no expone el knob (las opciones existentes en la UI no aplican a GLM), y decidimos NO hackearlo por otras vias.
2. La comparativa del 29/08 mostro que los mejores outputs de agudeza vinieron SIN razonamiento visible. Pasarle max a la fuerza seria repetir el ciclo de DeepSeek (filosofar, quemar tokens, ADR-040).
3. Simplicidad operativa: un solo modo de correr GLM, sin decidir niveles por tarea.

Nota tecnica: el default del backend de Z.ai es `reasoning_effort: max` (y el thinking no se puede deshabilitar: `thinking.type` solo acepta `enabled`). En la practica via Ollama se observa output agudo sin razonamiento visible. El modelo piensa por dentro de forma fija; no lo administramos nosotros.

## Context

El 29/08/2026 se paso UN mismo prompt pesado (diseno de agente autonomo de mantenimiento para monorepo TS publicado a npm, 7 secciones) a 5 modelos. Resultados en agudeza operativa:

1. **Kimi K2.7 Code (xhigh)** - mejor pensador. Tiers de autonomia ganados con metricas.
2. **GLM 5.3 (sin razonamiento visible)** - mejor criterio central. "El que planifica debe ser el que edita."
3. **Kimi K3 (xhigh)** - mejor presentador, pero invento numeros y esquivo la pregunta hard del prompt.
4. **GLM 5.3 Flash (sin razonamiento visible)** - el mejor "chico": orden de evidencia, red->green, limites verificables fuera del modelo.
5. **DeepSeek V4 Flash (xhigh)** - el mas estructurado, el menos agudo. En max filosofa (ADR-040).

**Costo (verificado 2026-08-29):**

| Modelo | Input / 1M | Output / 1M | Dato empirico |
|---|---|---|---|
| GLM-5.3-Flash | $0.075 | $0.25 | 1 request de Kimi K3 = **41 requests** de GLM Flash en consumo real de Ollama (medicion de Gonzo) |
| Kimi K3 | $3.00 | $15.00 | Razonamiento always-on: no se puede apagar |
| Ratio | 40x | 60x | Consistente con el 41x empirico |

La familia Kimi razona mejor (K2.7) pero a costo de cirugia. GLM Flash rinde a nivel de criterio con el modelo mas barato del set. La decision es de negocio, no solo tecnica.

## Ficha de Capacidades (verificada 2026-08-29 en docs.z.ai, Hugging Face, llmreference)

| Capacidad | Valor |
|---|---|
| Input | Texto, imagen, video, archivos (PDFs nativo) |
| Output | Texto. Max 128K tokens (131072) |
| Contexto | 1M tokens |
| Arquitectura | 320B totales / 18B activos (MoE, atencion hibrida sparse + linear) |
| Licencia | MIT (pesos abiertos en HF: zai-org/GLM-5.3-Flash) |
| Razonamiento | Always-on interno; reasoning_effort low/high/max en backend (default max). Ollama no lo expone |
| Tools | Function calling, structured output (JSON), prompt caching |
| Benchmarks | Terminal-Bench 2.1: 84.3 - Toolathlon: 78.4 - DeepSWE 1.1: 63.4 (Z.ai, 2026-08-26) |
| Historia | Ex "ox-alpha": probado en stealth con miles de millones de tokens de agentes de codigo reales en OpenRouter/OpenCode antes de su lanzamiento |

### Capacidades que cambian guias anteriores

Estas reglas de ADR-040 (Casos Especiales) quedan ACTUALIZADAS:

- **PDFs nativos:** ANTES "ningun modelo procesa PDFs nativamente". AHORA GLM-5.3-Flash acepta archivos como input. El flujo con `scripts/pdf-tool.sh` sigue siendo el fallback si el servicio falla.
- **Imagen en el loop de codigo:** GLM-5.3-Flash observa interfaces y resultados renderizados (visual coding). Capturas de UI, mockups y screenshots de error se procesan SIN cambiar de modelo.
- **Vision:** el default ya no es "solo texto". gemma4/minimax quedan como alternativa si GLM no esta disponible.
- **Deliverables Office:** soporta flujos hacia PPTX/PDF/DOCX/XLSX (segun Z.ai). Sin verificar en nuestro setup aun.

## Reglas de Uso (manual rapido)

1. **Default para todo lo diario:** sesiones, pipeline A/B (agentes en su default, sin parámetros), PRs, docs. Cero knobs.
2. **Vision/PDF:** pasar la imagen o el archivo directo. No cambiar de modelo por capacidad, solo por calidad de tarea (ver ADR-040 para especialistas).
3. **Sin caros en el ecosistema (2026-08-29):** `kimi-k3` y `deepseek-v4-pro` removidos de la config de OpenClaw junto con DeepSeek V4 Flash. Los tres volvibles desde el backup `~/.openclaw/openclaw.json.bak-20260829`. Si un problema requiere frontier, pedir autorizacion explicita a Gonzo y restaurar el modelo puntual.
4. **Kimi K2.7 Code:** el mejor pensador de la comparativa, sigue en la lista. Candidato a motor alternativo. Pendiente prueba en high (ver Pendientes).
5. **Si la tarea no da para GLM** (se traba, alucina, contexto exotico): escalar segun ADR-040 (glm-5.3, kimi-k2.7, gemma) y anotar el caso en el daily.
6. **A GLM jamas pasarle parámetros de razonamiento.** Si OpenClaw u Ollama exponen el knob en el futuro, abrir revision de este ADR antes de usarlo.

## Riesgos y Mitigaciones

| Riesgo | Mitigacion |
|---|---|
| Dependencia mono-familia (GLM/Z.ai) | Fallback `openrouter/auto` en config; `glm-5.3:cloud`, `kimi-k2.7-code:cloud` y `gemma4:cloud` en la lista de alternativas |
| Modelo muy nuevo (lanzamiento 2026-08-26) | Validado en batalla pre-lanzamiento (ox-alpha). Monitorear en tareas reales; diario registra fallos |
| Sin control de razonamiento desde Ollama | Aceptado por decision: default del servidor, sin administramos niveles |
| Rollback | Backup `~/.openclaw/openclaw.json.bak-20260829` (restaura default + lista con DeepSeek V4 Flash, K3 y pro) |

## Pendientes (por donde seguir)

1. **RESUELTO (2026-08-29 22:08): Kimi K2.7 Code en high probado** con el mismo prompt de arquitectura. Veredicto: solido pero SIN win claro sobre GLM Flash en lo visible (secciones 1-3; se trunco de nuevo antes de 4-7). Hallazgo clave: **el nivel de razonamiento le cambio el juicio arquitectonico** - en xhigh eligio single-agent con refutaciones operativas duras al multi-agente; en high eligio multi-agente de 9 workers (9 bootstraps por issue), contradiciendo su propio argumento xhigh y la evidencia acumulada. Aportes reales en high: artifacts estructurados como unico contrato entre workers, Safety Gatekeeper que "nunca ejecuta, solo bloquea", y convergencia con la regla decide-en-max/avanza-en-high. **Conclusion: el motor queda en GLM Flash; K2.7 sigue como especialista de codigo pesado (ADR-040), preferentemente en xhigh cuando el caso lo justifique.**
2. **Validar GLM Flash en tareas REALES del pipeline** (escribir codigo, tests, PRs). La comparativa midio diseno de arquitectura, no produccion. Registrar resultado en daily.
3. **Probar input visual en casos reales:** mockup -> UI (best practice oficial de Z.ai), screenshot de error -> fix.
4. **Re-cata en ~1 mes (fines de septiembre):** el mercado se mueve rapido; revisar si hay novedades en GLM 5.4/x o equivalentes.
5. **Si Ollama expone reasoning_effort:** revisar este ADR y el 040 antes de tocar nada.

## Consecuencias

### Positivas

- Un solo motor con criterio superior a DeepSeek Flash (evidencia: comparativa), multimodal nativo, y el mas barato de los capaces.
- Regla simple: cero parametros para GLM. El 90% de las decisiones de modelo desaparecen.
- Capacidades nuevas (PDF/imagen/video nativo) sin saltos de modelo.
- El 41x queda documentado: ahora SABEMOS cuanto cuesta el lujo de K3.

### Negativas

- Perdemos DeepSeek V4 Flash de la rotacion (era el default historico; su estilo "arquitecto exhaustivo" se pierde).
- El max del backend es un comportamiento fijo que no controlamos.
- ADR-040 requiere lectura combinada con este (sus defaults originales estan desactualizados aqui).

## Referencias

- Comparativa de 5 modelos, 2026-08-29 (memory/2026-08-29.md)
- Z.ai docs GLM-5.3-Flash: https://docs.z.ai/guides/vlm/glm-5.3-flash (consultado 2026-08-29)
- Hugging Face model card: https://huggingface.co/zai-org/GLM-5.3-Flash (consultado 2026-08-29)
- Precios: https://www.llmreference.com/model/glm-5.3-flash y /model/kimi-k3 (consultados 2026-08-29)
- Medicion empirica de consumo: Ollama usage, Gonzo, 2026-08-29 (41x)
- ADR-040: Seleccion de Modelos por Tipo de Tarea (perfiles de especialistas vigentes)