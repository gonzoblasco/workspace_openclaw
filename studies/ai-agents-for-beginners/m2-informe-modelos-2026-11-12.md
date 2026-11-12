# M2 - Práctica: informe comparativo de LLMs (consulta 2026-11-12)

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 2 — Hallucinations, Model Evolution, & Competitors (07:54–15:23)
- **Fuente:** Vane (prompt de Kanam, ejecutado por Gonzo)
- **Estado:** borrador para auditar; **no** es la tabla final del ejercicio.
- **Informe original:** adjunto `pasted-text-1794456834203.txt` de la sesión.

## Informe de Vane (verbatim)

## Informe comparativo de LLMs para construcción de agentes (consulta: 2026-11-12)

Este informe recopila datos verificables de seis modelos representativos para la construcción de agentes, seleccionados entre los proveedores OpenAI, Anthropic, Google, Meta/Llama, DeepSeek y Mistral, a fecha de consulta 2026-11-12. No incluye ranking, puntuación ni recomendación de uso; su único propósito es ofrecer cifras auditables. Cuando un dato no aparece publicado en las fuentes consultadas, se indica explícitamente como "no publicado", sin inferencias. Las discrepancias entre fuentes oficiales se listan en la sección correspondiente.

### Metodología y fuentes

Los datos se extrajeron de la documentación oficial y de las páginas de precios de cada proveedor, complementadas con fichas técnicas de OpenRouter para modelos de terceros. Para cada modelo se registraron: proveedor, nombre exacto, ventana de contexto, precio de entrada y salida por millón de tokens, fecha de corte de conocimiento, soporte de tool calling/function calling, licencia o modalidad, URL oficial y fecha de consulta. Las URL se incluyen al final del informe. La fecha de consulta unificada es 2026-11-12 para todas las filas.

---

### Tabla comparativa

| Proveedor | Modelo exacto | Ventana de contexto (tokens) | Precio (input / output por 1M tokens, USD) | Corte de conocimiento | Tool calling / function calling | Licencia o modalidad | Fecha de consulta |
|---|---|---|---|---|---|---|---|
| OpenAI | GPT-5.1 | 400.000 (máx. salida 128.000) | 1,25 / 10,00 (input cacheado 0,125) | 2024-09-30 | No publicado en los datos consultados | API propietaria | 2026-11-12 |
| Anthropic | Claude Sonnet 4.5 | 200.000 (máx. salida 64.000) | 3,00 / 15,00 | Fiable: 2025-01; datos de entrenamiento: 2025-07 | Sí (tool use documentado) | API propietaria | 2026-11-12 |
| Google | Gemini 2.5 Pro (`gemini-2.5-pro`) | Entrada 1.048.576 / salida 65.536 | No publicado en los datos consultados | 2025-01 | Sí (function calling listado como capacidad) | API propietaria (deprecado) | 2026-11-12 |
| Meta | Llama 4 Scout | 10.000.000 (entrenamiento/post-entrenamiento con 256.000) | No publicado en los datos consultados | No publicado | Parcial (ejemplo de function-composition en documentación) | Open weights (descargable en llama.com y Hugging Face) | 2026-11-12 |
| DeepSeek | DeepSeek-V4-Pro (`deepseek-v4-pro`) | 1.000.000 (máx. salida 384.000) | Cache-miss input 0,66 (pico 1,32) / output 1,98 (pico 3,96); cache-hit input 0,022 (pico 0,044) | No publicado | Sí (tool calls listado como feature) | API + open weights (licencia no publicada en los datos consultados) | 2026-11-12 |
| Mistral | Mistral Large 2407 | 131.000 | 2,00 / 6,00 (enrutamiento UE: 2,20 / 6,60) | 2024-03 | No publicado en los datos consultados | API propietaria (licencia no publicada en los datos consultados) | 2026-11-12 |

---

### Detalle por modelo

#### OpenAI — GPT-5.1

GPT-5.1 ofrece una ventana de contexto de 400.000 tokens y un máximo de 128.000 tokens de salida. Su fecha de corte de conocimiento es 2024-09-30. La modalidad de entrada/salida es texto (entrada y salida) e imagen (solo entrada); no soporta audio ni video. El esfuerzo de razonamiento admite valores none (por defecto), low, medium y high. El precio de la API es de 1,25 USD por millón de tokens de entrada, 0,125 USD por millón de tokens de entrada cacheados y 10,00 USD por millón de tokens de salida; existe precio de Batch API. Las instantáneas disponibles son `gpt-5.1` y `gpt-5.1-2025-11-13` (deprecada). Los límites de tasa publicados son: nivel Build 5.000 RPM / 1.000.000 TPM / 3.000.000 de cola de batch; nivel Launch 10.000 RPM / 4.000.000 TPM / 200.000.000 de cola de batch; nivel Grow 15.000 RPM / 40.000.000 TPM / 15.000.000.000 de cola de batch. El nivel Free no está soportado. La documentación consultada no publica soporte de tool calling/function calling para este modelo, por lo que se marca como "no publicado". La modalidad es API propietaria.

#### Anthropic — Claude Sonnet 4.5

Claude Sonnet 4.5 tiene una ventana de contexto de 200.000 tokens y un máximo de 64.000 tokens de salida. Se encuentra deprecado aunque sigue funcional, con retiro programado el 2026-11-30; el reemplazo recomendado es Claude Sonnet 5.5. El corte de conocimiento se publica en dos conceptos distintos: corte de conocimiento fiable enero de 2025 y corte de datos de entrenamiento julio de 2025. El pensamiento extendido está soportado; el esfuerzo por defecto no está soportado. La entrada acepta texto e imágenes y la salida es texto. El precio base es de 3 USD por millón de tokens de entrada y 15 USD por millón de tokens de salida. El prompt caching se tarifica así: escritura de caché de 5 minutos a 3,75 USD/MTok (1,25x), escritura de caché de 1 hora a 6 USD/MTok (2x) y lectura de caché a 0,30 USD/MTok (0,1x). La Batch API se tarifica a 1,50 USD/MTok de entrada y 7,50 USD/MTok de salida. La sobrecarga del system prompt para tool use es de 496 tokens en modo auto/none y 588 tokens en modo any/tool. La definición de la herramienta bash añade 244 tokens de entrada para Claude 4.6 y modelos anteriores, y 325 tokens para Claude 4.7 y posteriores y Claude Mythos Preview. La herramienta de editor de texto añade 745 tokens de entrada para Claude 4.6 y anteriores, y 974 tokens para Claude 4.7 y posteriores y Claude Mythos Preview. Claude 4.7 y posteriores y Claude Mythos Preview usan un tokenizador más reciente que produce aproximadamente un 30% más de tokens para el mismo texto. Claude Sonnet 4.5 no forma parte del grupo que incluye la ventana completa de 1 millón de tokens a precio estándar (ese grupo cubre Claude 4.6 y posteriores, excepto Haiku 5.5, y Claude Mythos Preview). La residencia de datos con multiplicador 1,1x aplica a Claude 4.6 y posteriores; los modelos anteriores, incluido Sonnet 4.5, no soportan inference_geo y usan siempre precio estándar. El tool calling está soportado y documentado mediante el sistema de tool use, con cargos adicionales basados en tokens totales, incluido el parámetro tools, más un system prompt automático. Las herramientas del lado del servidor pueden generar cargos adicionales basados en uso, por ejemplo búsqueda web a 10 USD por cada 1.000 búsquedas; las herramientas del lado del cliente se tarifican como solicitudes API estándar. La modalidad es API propietaria.

#### Google — Gemini 2.5 Pro

Gemini 2.5 Pro (`gemini-2.5-pro`) está deprecado: ya no es seleccionable en Google AI Studio y el acceso por API se limita a usuarios existentes hasta el 2026-12-01. A partir del 2026-12-01, todas las solicitudes a `gemini-2.5-pro` se enrutan automáticamente a Gemini 3.8 Flash (`gemini-3.8-flash`) y se facturan a las tarifas de Gemini 3.8 Flash. La entrada soporta audio, imágenes, video, texto y PDF; la salida es texto. El límite de tokens de entrada es 1.048.576 y el de salida es 65.536. Las capacidades soportadas incluyen ejecución de código, caché de contexto, búsqueda de archivos, function calling, grounding con Google Maps, grounding con Google Search, salidas estructuradas, thinking y contexto de URL. No soporta generación de audio, generación de imágenes ni Live API. Las opciones de consumo son Batch API, inferencia Flex e inferencia Priority. La última actualización es de junio de 2025. El corte de conocimiento es enero de 2025. La sección de precios está presente en la documentación pero no se muestran cifras específicas en los datos consultados, por lo que el precio se marca como "no publicado". El tool calling está soportado, ya que function calling figura entre las capacidades listadas. La modalidad es API propietaria, en estado deprecado.

#### Meta — Llama 4 Scout

Llama 4 Scout tiene 17.000 millones de parámetros activos, 16 expertos y 109.000 millones de parámetros totales; utiliza una arquitectura MoE. Cabe en una sola GPU NVIDIA H100 con cuantización Int4. Publica una ventana de contexto de 10.000.000 de tokens descrita como líder en la industria; fue pre-entrenado y post-entrenado con longitud de contexto de 256.000 tokens y probado en post-entrenamiento con hasta 8 imágenes, con pre-entrenamiento multimodal de hasta 48 imágenes. Llama 4 Maverick, variante hermana, tiene 17.000 millones de parámetros activos, 128 expertos y 400.000 millones de parámetros totales; cabe en un solo host NVIDIA H100; su versión experimental de chat obtuvo ELO 1417 y se describe con la mejor relación rendimiento-costo de su clase; también es multimodal. Llama 4 Behemoth, en vista previa, tiene 288.000 millones de parámetros activos, 16 expertos y casi 2 billones de parámetros totales, y supera a GPT-4.5, Claude Sonnet 3.7 y Gemini 2.0 Pro en varios benchmarks STEM. Los modelos Scout y Maverick están disponibles para descarga en llama.com y Hugging Face; la disponibilidad en socios llega en los días siguientes. Meta AI construida con Llama 4 está disponible en WhatsApp, Messenger, Instagram Direct y en el sitio web Meta.AI. La documentación incluye un ejemplo de system prompt de composición de funciones que exige usar únicamente las funciones listadas explícitamente, responder con conocimiento interno o mensaje de servicio no disponible si no hay servicio, y emitir únicamente llamadas a funciones en formato exacto, sin combinar texto y llamadas a funciones; el ejemplo incluye `get_weather` con parámetro requerido `city` y opcional `metric` (celsius o fahrenheit). Por ello se clasifica el soporte de tool calling como parcial, basado en el ejemplo documentado. No se publican precios de API, ventana de contexto para Maverick ni fecha de corte de conocimiento en los datos consultados; se marcan como "no publicado". La modalidad es open weights, con descarga disponible en llama.com y Hugging Face; los detalles de licencia no aparecen en los datos consultados. Sobre seguridad y alineación, la documentación menciona Llama Guard, Prompt Guard y CyberSecEval, una tasa de rechazo inferior al 2% en temas debatidos, rechazos desiguales por debajo del 1% y una inclinación política comparable a Grok.

#### DeepSeek — DeepSeek-V4-Pro

Según la documentación oficial de precios de DeepSeek, DeepSeek-V4-Pro (`deepseek-v4-pro`, versión DeepSeek-V4-Pro-0813) tiene una longitud de contexto de 1.000.000 de tokens y un máximo de salida de 384.000 tokens. Soporta modos non-thinking y thinking; incluye salida JSON, tool calls, Responses API, Anthropic API, Chat Prefix Completion (beta) y FIM Completion (beta, solo modo non-thinking); la visión no está soportada. La visión está soportada en DeepSeek Flash. Los precios por millón de tokens son: cache-hit input off-peak 0,022 USD y pico 0,044 USD; cache-miss input off-peak 0,66 USD y pico 1,32 USD; salida off-peak 1,98 USD y pico 3,96 USD. Las horas pico son 01:00-04:00 y 06:00-10:00 UTC de lunes a viernes, excluyendo festivos chinos; el resto es off-peak, incluidos fines de semana y festivos chinos. El límite de concurrencia para DeepSeek-V4-Pro es de 500. La Search API y la Fetch API se tarifican a 0,75 USD por cada 1.000 solicitudes exitosas. La facturación es gasto = número de tokens × precio; los cargos se deducen del saldo recargado o del saldo otorgado, usando primero el saldo otorgado; los precios del producto pueden variar. DeepSeek Flash (`deepseek-flash`; los modelos legacy `deepseek-v4-flash` y `deepseek-v4-flash-vision-exp` están retirados y se sirven mediante DeepSeek-V4.1-Flash-1017 al precio Flash) tiene contexto de 1.000.000 tokens, salida máxima de 384.000 tokens, soporta modos non-thinking y thinking (por defecto), e incluye salida JSON, tool calls, Responses API, Anthropic API, Chat Prefix Completion (beta), FIM Completion (beta, solo non-thinking) y visión. Sus precios son: cache-hit input off-peak 0,003 USD y pico 0,006 USD; cache-miss input off-peak 0,15 USD y pico 0,30 USD; salida off-peak 0,60 USD y pico 1,20 USD. Su límite de concurrencia es de 2.500. DeepSeek V3.2, según OpenRouter, tiene una ventana de contexto de 164.000 tokens, fue lanzado el 2025-12-01, soporta tool calling mediante el array de tools siguiendo la forma de OpenAI, con control de tool_choice; su precio con descuento es de 0,2088 USD de entrada y 0,3096 USD de salida por millón de tokens (28% de descuento), con un precio promedio real pagado de 0,1653 USD de entrada y 0,4482 USD de salida por millón de tokens; su mejor throughput es de 49 tok/s y su mejor latencia de 0,87 s. La fecha de corte de conocimiento no está publicada para DeepSeek V3.2 ni para DeepSeek-V4-Pro. El tool calling está soportado en ambos. La modalidad es API más open weights; la licencia específica no aparece en los datos consultados.

#### Mistral — Mistral Large 2407

Mistral Large 2407 tiene una ventana de contexto de 131.000 tokens, fue lanzado el 2024-11-19 y su fecha de corte de conocimiento es marzo de 2024. El precio es de 2,00 USD por millón de tokens de entrada y 6,00 USD por millón de tokens de salida, con enrutamiento en la UE a 2,20 USD y 6,60 USD por millón de tokens de entrada y salida respectivamente. El throughput P50 mejor entre proveedores es de 70 tok/s y la latencia P50 del mejor proveedor es de 0,54 s. La disponibilidad en 3 días fue de 99,96% y el uptime de 3 días de 100,00%. Las puntuaciones de benchmark publicadas incluyen: GPQA Diamond julio de 2024 47,2% y noviembre de 2024 48,6%; HLE 2,9% y 3,3%; MMLU-Pro 68,3% y 69,7%; MATH-500 71,4% y 73,6%; AIME 9,3% y 11,0%; AIME 2025 0,0% y 14,0%; LiveCodeBench 26,7% y 29,3%; IFBench 31,6% y 31,2%; AA-LCR 2,0%; τ²-Bench Telecom 33,0% y 30,7%; Terminal-Bench Hard 6,1%; CritPt 0,0%. El soporte de tool calling/function calling no está publicado en los datos consultados. La licencia o modalidad no está publicada en los datos consultados; el modelo se sirve vía API de Mistral.

---

### Discrepancias entre fuentes oficiales

- **Claude Sonnet 4.5 — dos cortes de conocimiento publicados:** la ficha oficial publica corte de conocimiento fiable enero de 2025 y corte de datos de entrenamiento julio de 2025, que no son la misma fecha. Se listan ambos sin reconciliarlos.
- **Claude Sonnet 4.5 — ventana de contexto:** la ficha oficial indica 200.000 tokens de contexto. La página de precios aclara que la ventana completa de 1 millón de tokens a precio estándar aplica a Claude 4.6 y posteriores (excepto Haiku 5.5) y a Claude Mythos Preview, no a Sonnet 4.5. Por tanto, no debe atribuirse 1M a Sonnet 4.5.
- **Llama 4 Scout — contexto de entrenamiento vs. contexto soportado:** se publica una ventana de contexto de 10.000.000 de tokens descrita como líder en la industria, pero el pre-entrenamiento y post-entrenamiento se realizaron con longitud de contexto de 256.000 tokens. Ambos valores aparecen en la documentación oficial y no se reconcilian.
- **DeepSeek — generaciones distintas con cifras incompatibles:** DeepSeek V3.2 (OpenRouter) publica 164.000 tokens de contexto y precios de 0,2088/0,3096 USD por millón, mientras que DeepSeek-V4-Pro (documentación oficial de DeepSeek) publica 1.000.000 tokens de contexto y precios de 0,66/1,98 USD por millón (cache-miss, off-peak). Son modelos distintos; no se deben mezclar sus cifras. En la tabla se usa DeepSeek-V4-Pro por ser la generación documentada en la fuente oficial de precios.
- **Mistral Large 2407 — enrutamiento:** los precios estándar son 2,00/6,00 USD por millón, mientras que el enrutamiento en la UE es de 2,20/6,60 USD por millón. Ambas cifras son oficiales y dependen de la región.
- **GPT-5.1 — entrada cacheada:** el precio de entrada estándar es de 1,25 USD por millón y el de entrada cacheada es de 0,125 USD por millón, una diferencia de 10x publicada en la misma ficha.
- **Gemini 2.5 Pro — deprecación y enrutamiento futuro:** el modelo está deprecado y, a partir del 2026-12-01, las solicitudes se enrutan automáticamente a Gemini 3.8 Flash con facturación a tarifas de Gemini 3.8 Flash, cuyos precios no aparecen en los datos consultados.
- **Claude Sonnet 4.5 — deprecación:** el modelo está deprecado y se retira el 2026-11-30, con Claude Sonnet 5.5 como reemplazo recomendado; no se dispone de precios ni contexto de Sonnet 5.5 en los datos consultados.
- **Claude — tokenizador:** Claude 4.7 y posteriores y Claude Mythos Preview usan un tokenizador más reciente que produce aproximadamente un 30% más de tokens para el mismo texto; esto afecta la comparabilidad de costos entre generaciones, aunque no se publica precio para esos modelos en los datos consultados.

---

### URLs oficiales (ficha o página de precios)

- OpenAI GPT-5.1 (ficha de modelo): https://platform.openai.com/docs/models/gpt-5.1
- OpenAI (precios de la API): https://openai.com/api/pricing/
- Anthropic Claude Sonnet 4.5 (ficha de modelo): https://platform.claude.com/docs/en/about-claude/models/overview
- Anthropic (precios): https://platform.claude.com/docs/en/about-claude/pricing
- Google Gemini 2.5 Pro (ficha de modelo): https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro
- Google (precios de la API de Gemini): https://ai.google.dev/gemini-api/docs/pricing
- Meta Llama 4 (fichas y formatos de prompt): https://www.llama.com/docs/model-cards-and-prompt-formats/llama4/
- Meta Llama (descargas): https://llama.com
- DeepSeek (precios y modelos): https://api-docs.deepseek.com/quick_start/pricing
- DeepSeek (plataforma): https://platform.deepseek.com
- Mistral (documentación de modelos): https://docs.mistral.ai/getting-started/models/
- Mistral (tecnología y precios): https://mistral.ai/technology/
- OpenRouter (Mistral Large 2407): https://openrouter.ai/mistralai/mistral-large-2407
- OpenRouter (DeepSeek V3.2): https://openrouter.ai/deepseek/deepseek-v3.2
- OpenRouter (Gemini 2.5 Pro): https://openrouter.ai/google/gemini-2.5-pro

---

### Limitaciones y notas para auditoría

- Los precios de Gemini 2.5 Pro, Llama 4 Scout y Mistral Large 2407 (licencia) no están publicados en los datos consultados; se marcan como "no publicado" y no se infieren. Para auditoría en clase se recomienda verificar directamente en las URL oficiales listadas.
- Las fechas de corte de conocimiento de Llama 4 Scout y de DeepSeek (V3.2 y V4-Pro) no están publicadas en los datos consultados.
- El soporte de tool calling para GPT-5.1 y Mistral Large 2407 no está publicado en los datos consultados, aunque ambos proveedores ofrecen capacidades de function calling en otros modelos documentados; no se extrapolan a los modelos listados.
- Las cifras de DeepSeek V3.2 provienen de OpenRouter y difieren de las de la documentación oficial de DeepSeek (V4-Pro/Flash); se presentan por separado para evitar mezcla.
- La modalidad open weights de Llama 4 se confirma por la disponibilidad de descarga en llama.com y Hugging Face; los detalles de licencia no aparecen en los datos consultados.
- La fecha de consulta unificada es 2026-11-12; los precios y límites pueden variar y los proveedores pueden actualizarlos sin previo aviso.

### Síntesis

A fecha 2026-11-12, los seis modelos auditados presentan ventanas de contexto que van desde 131.000 tokens (Mistral Large 2407) hasta 10.000.000 de tokens (Llama 4 Scout), con GPT-5.1 en 400.000, Gemini 2.5 Pro en 1.048.576 de entrada, DeepSeek-V4-Pro en 1.000.000 y Claude Sonnet 4.5 en 200.000. Los precios publicados por millón de tokens varían ampliamente: GPT-5.1 1,25/10,00; Claude Sonnet 4.5 3,00/15,00; Mistral Large 2407 2,00/6,00; DeepSeek-V4-Pro 0,66/1,98 (cache-miss, off-peak); mientras que Gemini 2.5 Pro y Llama 4 Scout no publican precios en los datos consultados. Dos modelos están deprecados (Gemini 2.5 Pro y Claude Sonnet 4.5), con fechas de retiro o enrutamiento automático documentadas. El soporte de tool calling se confirma para Claude Sonnet 4.5, Gemini 2.5 Pro y DeepSeek (V4-Pro/V3.2), se clasifica como parcial para Llama 4 Scout por el ejemplo documentado, y no está publicado para GPT-5.1 y Mistral Large 2407. Los cortes de conocimiento publicados son: GPT-5.1 2024-09-30, Mistral Large 2407 marzo de 2024, Gemini 2.5 Pro y Claude Sonnet 4.5 enero de 2025 (con Claude añadiendo julio de 2025 para datos de entrenamiento), y no publicados para Llama 4 Scout y DeepSeek. Esta tabla se ofrece únicamente como base de datos verificables para auditoría, sin recomendación de uso.

Citations:
[1] https://www.userightai.com/models/anthropic-claude-sonnet-45
[2] https://openrouter.ai/google/gemini-2.5-pro
[3] https://www.userightai.com/models/openai-gpt-51
[4] https://ai.google.dev/gemini-api/docs/pricing
[5] https://platform.claude.com/docs/en/about-claude/pricing
[6] https://ai.meta.com/blog/llama-4-multimodal-intelligence/
[7] https://openrouter.ai/mistralai/mistral-large-2407
[8] https://openrouter.ai/deepseek/deepseek-v3.2
[9] https://platform.claude.com/docs/en/models/sonnet-4-5/overview
[10] https://developers.openai.com/api/docs/models/gpt-5.1
[11] https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro
[12] https://www.llama.com/docs/model-cards-and-prompt-formats/llama4/
[13] https://api-docs.deepseek.com/quick_start/pricing/

## Auditoría de Kanam (2026-11-12)

### Veredicto corto

El informe es útil como primer barrido: trae cifras, fuentes y una sección de discrepancias. Pero **no responde la pregunta del ejercicio**: la mayoría de los modelos elegidos están deprecados o en retiro, y hay al menos un dato de tool calling incorrecto por omisión. Sirve como materia prima, no como tabla final.

### Verificación contra fuentes oficiales

| Dato del informe | Fuente oficial | Resultado |
|---|---|---|
| GPT-5.1: 400k contexto, 128k salida, corte 2024-09-30, $1.25/$10 | https://developers.openai.com/api/docs/models/gpt-5.1 | Contexto, salida, corte y precio **correctos**. La ficha oficial marca **Status: Deprecated** y lista `function_calling` entre las features soportadas. El informe dice "tool calling no publicado": **falso negativo**. |
| Claude Sonnet 4.5: 200k contexto, $3/$15, retiro 2026-11-30 | https://platform.claude.com/docs/en/models/overview | El modelo ya no está en la línea actual. La línea vigente es **Claude Fable 5.2, Opus 5.5, Sonnet 5.5 y Haiku 5.5**, todos con **1M de contexto**, **128K de salida** y corte **junio 2026**. Sonnet 5.5 cuesta **$2/$10**. La tabla usa un modelo saliente. |
| Gemini 2.5 Pro: deprecado, 1.048.576 entrada / 65.536 salida, corte ene-2025, precios no publicados | https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro | No pude verificar: el fetch entra en un loop de redirects. El propio informe dice que está deprecado y que desde 2026-12-01 se enruta a Gemini 3.8 Flash. **Queda como no verificado**, no como dato firme. |
| Llama 4 Scout: 10M contexto, 17B activos / 109B totales, 16 expertos, open weights, tool calling parcial | https://www.llama.com/docs/model-cards-and-prompt-formats/llama4/ | La página abierta muestra el prompt de composición de funciones, no la ficha completa. Los números son plausibles, pero **no quedaron verificados en esta pasada**. Verificar la model card antes de usarlos. |
| DeepSeek-V4-Pro: 1M contexto, 384K salida, tool calls, $0.66/$1.98 off-peak | https://api-docs.deepseek.com/quick_start/pricing | **Correcto**: 1M de contexto, 384K de salida, tool calls, precios $0.022/$0.66/$1.98 off-peak y $0.044/$1.32/$3.96 peak. Límite de concurrencia 500. |
| Mistral Large 2407: 131k contexto, $2/$6, corte mar-2024, tool calling no publicado | https://docs.mistral.ai/models | El modelo actual es **Mistral Large 4** (open-weight, multimodal, uso general). Mistral Large 2.0 (24.07) figura en la lista de **deprecados**. La fila del informe es histórica, no actual. |

### Tabla corregida (parcial, solo datos verificados)

| Proveedor | Modelo | Estado | Contexto | Precio in/out (1M) | Corte | Tool calling | Fuente |
|---|---|---|---|---|---|---|---|
| OpenAI | GPT-5.1 | **Deprecated** | 400k / 128k salida | $1.25 / $10 (cacheado $0.125) | 2024-09-30 | **Sí** (`function_calling`) | Ficha oficial OpenAI |
| Anthropic | Claude Sonnet 5.5 | **Current** | 1M / 128k salida | $2 / $10 | Jun 2026 | Sí (tool use) | Models overview |
| Anthropic | Claude Opus 5.5 | **Current** | 1M / 128k salida | $4 / $20 | Jun 2026 | Sí (tool use) | Models overview |
| DeepSeek | DeepSeek-V4-Pro | **Current** | 1M / 384k salida | $0.66 / $1.98 off-peak; $1.32 / $3.96 peak | No publicado | Sí (tool calls) | Pricing oficial |
| Meta | Llama 4 Scout | Current / open weights | 10M (según informe, **verificar**) | No publicado | No publicado | Parcial (según informe) | Model card (parcial) |
| Mistral | Mistral Large 4 | **Current** (listado) | No verificado | No verificado | No verificado | No verificado | Docs Mistral |
| Google | Gemini 3.8 Flash (reemplazo) | Current según informe | No verificado | No verificado | No verificado | No verificado | Solo informe |

### Lección de método

- **"No publicado" no es lo mismo que "no existe".** GPT-5.1 es el caso testigo: la ficha oficial lista `function_calling`, pero el informe no lo encontró y lo marcó como no publicado.
- **Un informe puede ser internamente coherente y estar respondiendo otra pregunta.** La selección de modelos es parte de la respuesta: si elegís modelos deprecados, la tabla no sirve para "hoy", aunque los números sean correctos.
- **Las fuentes terciarias sirven para cross-check, no para la fila final.** OpenRouter y UserRightAI pueden ayudar a detectar discrepancias, pero cada celda de la tabla final necesita una URL oficial del proveedor.
- **Lo que el informe hace bien:** separa discrepancias, no inventa datos faltantes y marca explícitamente lo que no encontró. Eso se conserva.

### Próximo paso (M2)

Segunda pasada con 4 modelos actuales, uno por proveedor, con columna **Estado** y URL oficial:
- OpenAI: GPT-5.1 está deprecado; hay que identificar el flagship actual.
- Anthropic: Claude Sonnet 5.5 (1M, $2/$10, Jun 2026).
- Google: Gemini 3.8 Flash (reemplazo del 2.5 Pro; verificar ficha).
- Meta: Llama 4 Scout (10M; verificar model card).
- DeepSeek: DeepSeek-V4-Pro (verificado).
- Mistral: Mistral Large 4 (verificar contexto/precio).

No cerrar la tabla hasta verificar cada celda contra la página oficial. El objetivo del M2 no es "tener seis filas", es **saber elegir modelos vigentes y auditar cada dato**.


<!-- project: github.com/gonzoblasco/workspace_openclaw -->
