# Historial de decisiones de modelo / engine (2026-08 a 2026-09)

> Archivado desde `MEMORY.md` el 2026-10-06 para bajar ese archivo bajo el cap de bootstrap.
> Es **registro histórico**, no instrucción vigente. La política vigente es **ADR-090** (niveles de
> pensamiento y asignación por agente) y **ADR-076** (ningún agente hereda modelo local).
> Lo que sigue se conserva para no perder la trazabilidad de por qué se llegó al estado actual.

## Decisión de motor LLM (2026-08-30)

**Tema:** Consolidación de motor de trabajo para el pipeline A/B.
**Decisión:** `deepseek-v4-flash:cloud` como modelo preferido para los agentes de código y orquestación de pipeline, reemplazando temporalmente a `glm-5.3-flash:cloud` (detalle en `tools.md`).
**Motivación:** preferencia explícita de Gonzo tras la auditoría de coherencia; el modelo fue seleccionado por su *estructura* en tareas complejas, priorizando la consistencia operativa sobre la preferencia inicial del proveedor.
**Impacto:** los futuros *tasks* deben referenciar este cambio; cualquier uso de `glm-5.3-flash:cloud` debía pasar por un flag de excepción justificado.

## Revert a DeepSeek V4 Flash como default (2026-08-30)

**Tema:** Default de todo el sistema.
**Decisión:** `deepseek-v4-flash:cloud` vuelve a ser el default de TODO el sistema (OpenClaw + pipeline A/B), revirtiendo el cambio a `glm-5.3-flash:cloud`. La diferencia de calidad entre ambos es muchísima a favor de DeepSeek (decisión explícita de Gonzo).
**Acción:** `agents.defaults.model.primary = ollama/deepseek-v4-flash:cloud`. Backup previo: `~/.openclaw/openclaw.json.bak-20260830-revert-deepseek`. Gateway reiniciado y verificado.
**Impacto:** `glm-5.3-flash:cloud` queda disponible (multimodal) pero NO como default; su uso como default requiere flag de excepción.

> Nota (2026-09-29): `deepseek-v4-flash:cloud` fue **retirado por Ollama el 2026-09-25** (`ollama show` responde `was retired`). Todo lo de arriba es registro de las decisiones de agosto; el motor vigente pasó a `deepseek-v4.1-flash:cloud`.

## Config de Tools - entradas históricas

- **Modelos (2026-09-11, 19:30):** Primary de OpenClaw: `deepseek-v4-flash:0731`. **Motor del pipeline A/B: `deepseek-v4-flash:cloud`** (ADR-046, revierte ADR-045 por costo: v4.1 consumía más por request que v4 y glm con menos requests). Kanam en **thinking max**; agentes A/B en **high**. Fallback + vision: `glm-5.3-flash`. **deepseek-v4.1-flash** = fase de escalada para análisis complejo; potencial paso previo/reemplazo de Kimi K2.7 Code. Nota: v4 anunciado para dejar de existir en unas semanas (reemplazo por 4.1) - a reevaluar entonces.
- **Cambio de motor (2026-08-29):** DeepSeek V4 Flash -> GLM 5.3 Flash, tras comparativa de 5 modelos con un mismo prompt pesado de arquitectura de agentes. DeepSeek fue el más estructurado pero el menos agudo; GLM 5.3 Flash ganó en insights operativos y es multimodal nativo (imagen/video/PDF, 1M de contexto). Kimi K2.7 Code (xhigh) fue el mejor pensador (validado en high el 29/08: sólido, sin win claro sobre GLM Flash); retirado del ecosistema el mismo día.
- **Niveles de razonamiento (2026-08-29):** el max NO es driver de calidad (DeepSeek en max filosofa, ADR-040; Kimi K3 en xhigh inventó números). Los mejores outputs vinieron sin razonamiento visible. Agentes de código siempre en high; max solo para diseño difícil puntual. Para GLM: CERO parámetros, default del servidor (ADR-041).
- **Regla de costo (2026-08-29):** 1 request de Kimi K3 = 41 requests de GLM 5.3 Flash en consumo real (medición Ollama). K3 = cirujano, nunca default. Precios verificados: GLM Flash $0.075/$0.25 - K3 $3.00/$15.00 por 1M.
- **Purga de modelos (2026-08-30):** fuera del ecosistema `kimi-k3`, `deepseek-v4-pro`, `qwen3.5:cloud`, `nemotron-3-nano`, `gemma4:31b-cloud`. Quedan 8 en config: `deepseek-v4-flash` (default + motor pipeline), `glm-5.3-flash` (multimodal + escalada iter 3), `glm-5.3` (escalada familia), `gemma4:e4b-mlx` (local vision), `gemma4:cloud` (vision + tono/voz), `kimi-k2.7-code` (nivel superior, iter 4), `minimax-m3` (opcional), `qwen3.5:9b-mlx` (local scorer) + fallback `openrouter/free`. Kimi K2.7 Code y minimax-m3 VUELVEN al ecosistema (2026-08-30, decisión de Gonzo: "siempre hay un nivel superior"). Backup: `~/.openclaw/openclaw.json.bak-20260830-pipeline-glm`.
- **Nombres de modelo no intercambiables (2026-09-11):** el motor del pipeline corría con `--model deepseek-v4-flash:cloud`, que resuelve en Ollama. La entrada de OpenClaw `deepseek-v4-flash:0731` es solo para el runtime de OpenClaw y **NO resuelve** en Ollama (`ollama show deepseek-v4-flash:0731` falla).
