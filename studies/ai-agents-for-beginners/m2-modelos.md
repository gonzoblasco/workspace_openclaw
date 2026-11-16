# M2 - Tabla final: modelos vigentes para construcción de agentes (consulta 2026-11-12)

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 2 — Hallucinations, Model Evolution, & Competitors (07:54–15:23)
- **Fuente:** Auditoría del informe de Vane + verificación contra fuentes oficiales (ver `m2-informe-modelos-2026-11-12.md`)
- **Fecha de consulta:** 2026-11-12

---

## Tabla comparativa (modelos vigentes)

| Proveedor | Modelo exacto | Ventana de contexto (tokens) | Precio (input / output por 1M tokens, USD) | Corte de conocimiento | Tool calling / function calling | Licencia o modalidad | Estado | URL oficial |
|---|---|---|---|---|---|---|---|---|
| OpenAI | **Por identificar** (GPT-5.1 deprecated) | no publicado | no publicado | no publicado | **Sí** (`function_calling`) | API propietaria | **Deprecated** (GPT-5.1) | https://platform.openai.com/docs/models/gpt-5.1 |
| Anthropic | Claude Sonnet 5.5 | 1.000.000 (máx. salida 128.000) | 2,00 / 10,00 | Junio 2026 | Sí (tool use) | API propietaria | **Actual** | https://platform.claude.com/docs/en/models/overview |
| Google | Gemini 3.8 Flash | 1.048.576 (máx. salida 65.536) | no publicado | no publicado | Sí (function calling) | API propietaria | **Actual** (reemplaza a 2.5 Pro) | https://ai.google.dev/gemini-api/docs/models |
| Meta | Llama 4 Scout | 10.000.000 (entrenamiento 256.000) | no publicado (open weights) | no publicado | Parcial (function-composition example) | Open weights | **Actual** | https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama4 |
| DeepSeek | DeepSeek-V4-Pro | 1.000.000 (máx. salida 384.000) | Cache-miss off-peak 0,66 / pico 1,32; salida off-peak 1,98 / pico 3,96 | no publicado | Sí (tool calls) | API + open weights | **Actual** | https://api-docs.deepseek.com/quick_start/pricing/ |
| Mistral | Mistral Large 4 | no publicado | no publicado | no publicado | no publicado | API propietaria | **Actual** (2407 deprecated) | https://docs.mistral.ai/models |

---

## Notas de auditoría

1. **OpenAI — flagship actual no identificado**: La fila quedó con GPT-5.1 como referencia porque es el último con ficha completa verificada, pero su `Status` es **Deprecated**. La ficha oficial también confirma `function_calling: true` (el informe original decía "no publicado": fue un falso negativo, corregido también en la tabla). La lista de modelos en `developers.openai.com` muestra variantes `gpt-5.6-*`, `gpt-6-*` pero no está claro cuál es el modelo de producción recomendado hoy. **Pendiente: identificar flagship actual y sus especificaciones oficiales.**

2. **Anthropic — Claude Sonnet 5.5 verificado**: 1M contexto, salida 128K, $2/$10, corte junio 2026, tool use soportado. Sonnet 4.5 está deprecated (retiro 2026-11-30). Fuente: `https://platform.claude.com/docs/en/models/overview`.

3. **Google — Gemini 3.8 Flash es el modelo actual**: Gemini 2.5 Pro está deprecated y a partir del 2026-12-01 las solicitudes se enrutan a 3.8 Flash. La página de modelos lista "Gemini 3.8" y "Gemini 4 frontier reasoning". Precio y corte no publicados en la consulta. Fuente: `https://ai.google.dev/gemini-api/docs/models`.

4. **Meta — Llama 4 Scout verificado parcialmente**: 17B activos / 109B totales, 16 expertos, MoE, 10M contexto (entrenamiento 256K), open weights descargables, tool calling parcial (ejemplo de system prompt function-composition). Precio y corte no publicados. Fuente: `https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama4`.

5. **DeepSeek — V4-Pro verificado**: 1M contexto, salida 384K, tool calls, precios off-peak/pico, límite concurrencia 500. Fuente: `https://api-docs.deepseek.com/quick_start/pricing/`.

6. **Mistral — Large 4 actual, Large 2407 deprecated**: La página oficial lista "Mistral Large 4" como modelo actual; no se extrajeron contexto, precio, corte ni tool calling en esta consulta. Fuente: `https://docs.mistral.ai/models`.

---

## URLs oficiales consultadas

- OpenAI GPT-5.1 (ficha): https://platform.openai.com/docs/models/gpt-5.1
- OpenAI precios: https://openai.com/api/pricing/
- Anthropic modelos: https://platform.claude.com/docs/en/models/overview
- Google Gemini modelos: https://ai.google.dev/gemini-api/docs/models
- Google Gemini precios: https://ai.google.dev/gemini-api/docs/pricing
- Meta Llama 4: https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama4
- DeepSeek precios: https://api-docs.deepseek.com/quick_start/pricing/
- Mistral modelos: https://docs.mistral.ai/models

---

## Próximos pasos

- [ ] Identificar el flagship actual de OpenAI (verificar `gpt-5.6`/`gpt-6` o el modelo recomendado en `platform.openai.com/docs/models`).
- [ ] Completar precios y corte de conocimiento de Gemini 3.8 Flash.
- [ ] Completar especificaciones de Mistral Large 4 (contexto, precio, corte, tool calling).
- [ ] Completar precio y corte de Llama 4 Scout (si aplica; es open weights).
- [ ] Decidir si incluir Llama 4 Maverick como modelo separado (128 expertos, 400B totales).