# M2 - Tabla final: modelos vigentes para construcción de agentes

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 2 — Hallucinations, Model Evolution, & Competitors (07:54 – 15:23)
- **Fecha de consulta:** **2026-11-16** (research completado; la primera pasada del 2026-11-12 dejó huecos que se cerraron acá)

## Tabla comparativa (modelos vigentes, un modelo por proveedor)

| Proveedor | Modelo exacto | Contexto | Precio (in / out, por 1M tokens, USD) | Corte de conocimiento | Tool calling | Licencia | URL oficial |
|---|---|---|---|---|---|---|---|
| **OpenAI** | `gpt-6-astra` | **1.050.000** (máx. entrada 922.000; salida 128.000) | **10,00 / 50,00** (caché 1,00; escritura 12,50) | **2026-04-30** | **Sí** (`function_calling` + `web_search`, `file_search`, `code_interpreter`, `computer_use`, `mcp`) | API propietaria | https://developers.openai.com/api/docs/models/gpt-6-astra |
| **Anthropic** | Claude Opus 5.5 (recomendado) · Sonnet 5.5 · Haiku 5.5 · Fable 5.2 | 1.000.000 (salida 128.000) | Opus **4,00 / 20,00** · Sonnet **2,00 / 10,00** · Haiku desde 0,10 / 0,50 · Fable **8,00 / 40,00** | Junio 2026 | Sí (tool use) | API propietaria | https://platform.claude.com/docs/en/models/overview |
| **Google** | `gemini-3.8-flash` | **1.048.576** (salida 65.536) | **0,75 / 3,75** (promo hasta 2026-12-31; luego 1,50 / 7,50) | **Marzo 2026** (algunos dominios ene 2025) | **Sí** (`function calling`) | API propietaria | https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash |
| **Meta** | Llama 4 Scout | **10.000.000** (Maverick: 1.000.000) | **Open weights** (sin precio de API) | **Agosto 2024** | **Sí** (`tool-calling` listado) | **Llama 4 Community License** (open weights) | https://www.llama.com/docs/model-cards-and-prompt-formats/llama4/ |
| **DeepSeek** | DeepSeek-V4-Pro | 1.000.000 (salida 384.000) | 0,66 / 1,98 off-peak · 1,32 / 3,96 pico · caché 0,022 | No publicado | Sí (tool calls) | API + open weights | https://api-docs.deepseek.com/quick_start/pricing/ |
| **Mistral** | `mistral-large-4` | **1.000.000** | **0,70 / 2,10** (caché 0,07) | No publicado en la ficha | **Sí** (`Function Calling` en `/v1/chat/completions`) | **Mistral Ecosystem Open Weight License** (open weights, 52B activos / 1,05T totales) | https://docs.mistral.ai/models/mistral-large-4 |

## Cómo se cerró cada hueco

| Hueco (12-nov) | Cómo se resolvió (16-nov) |
|---|---|
| OpenAI: flagship sin identificar | `platform.openai.com/docs/models` declara **GPT-6 Astra** como flagship. Ficha completa con contexto, precio, cutoff y features. |
| Google: precio y cutoff vacíos | La URL `.md` y el índice `llms.txt` fallaban por redirects; con `curl -L` se obtuvo la ficha. Precio promo $0,75/$3,75 hasta fin de 2026. |
| Mistral: "API propietaria" | **Falso**: Mistral Large 4 es **open-weight** bajo Mistral Ecosystem Open Weight License. Corregido. |
| Meta: sin cutoff ni tool calling | Ficha oficial: **cutoff agosto 2024**, `tool-calling` listado como capacidad, 10M contexto en Scout. |

## Correcciones a la versión anterior de esta tabla

1. **Mistral Large 4 no es API propietaria.** Es open weights (52B activos, 1,05T totales). El dato anterior estaba mal.
2. **Llama 4 no es "tool calling parcial".** La ficha lista `tool-calling` como capacidad del modelo. Lo "parcial" que había visto era un ejemplo de composición en el prompt, no una limitación.
3. **GPT-5.1 ya no es la referencia.** `gpt-6-astra` es el flagship; GPT-5.1 sigue en el catálogo a $1,25/$10 pero no es el modelo recomendado.

## Lo que sigue sin dato oficial

| Dato | Por qué |
|---|---|
| Gemini 3.8 Flash: corte de conocimiento | **Cerrado**: el model card de DeepMind declara **marzo 2026**, con algunos dominios limitados a enero 2025. La ficha de la API solo decía "Latest update: September 2026", que es otra cosa. |
| DeepSeek-V4-Pro: corte | La página de pricing no lo publica. |
| Mistral Large 4: corte | La ficha lista versión, licencia, params, precio, contexto y features; **no** el cutoff. |
| Meta Llama 4: precio | Es open weights: no hay precio de API que citar. Sí tiene cutoff (agosto 2024). |

**Cinco de seis filas tienen el corte de conocimiento.** Google lo publica en el model card (no en la ficha de la API); OpenAI lo publica en la ficha del modelo; Meta en la model card. DeepSeek y Mistral no lo publican en ningún lado que haya encontrado.

## Modelos alternativos del mismo proveedor (por si el flagship es caro)

| Proveedor | Alternativa | Precio in/out | Por qué elegirla |
|---|---|---|---|
| OpenAI | `gpt-6.1-sol` | 2,00 / 10,00 | "balance entre inteligencia y costo" (doc oficial) |
| OpenAI | `gpt-6-luna` | 0,10 / 0,50 | alto volumen, costo sensible |
| OpenAI | `gpt-6.1-terra` | 1,00 / 5,00 | intermedio, no mencionado en el doc de selección |
| Meta | Llama 4 Maverick | open weights | 1M contexto, 400B totales, 128 expertos |

**Nota de precio OpenAI:** `gpt-6-astra` cobra **2× en input y 1,5× en output** cuando el prompt pasa 272K tokens. Para un agente con contexto grande eso es una decisión de arquitectura, no un detalle.

## URLs oficiales consultadas (2026-11-16)

- OpenAI modelos: https://developers.openai.com/api/docs/models
- OpenAI GPT-6 Astra: https://developers.openai.com/api/docs/models/gpt-6-astra
- OpenAI precios: https://developers.openai.com/api/docs/pricing
- Anthropic: https://platform.claude.com/docs/en/models/overview
- Google Gemini 3.8 Flash: https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
- Google precios: https://ai.google.dev/gemini-api/docs/pricing
- Meta Llama 4: https://www.llama.com/docs/model-cards-and-prompt-formats/llama4/
- DeepSeek precios: https://api-docs.deepseek.com/quick_start/pricing/
- Mistral Large 4: https://docs.mistral.ai/models/mistral-large-4

## Pendiente real (no falencia)

- [ ] Cortes de conocimiento de DeepSeek-V4-Pro y Mistral Large 4: no aparecen en la ficha del modelo ni en la de precios. Requiere buscar en el paper técnico o el release notes.
