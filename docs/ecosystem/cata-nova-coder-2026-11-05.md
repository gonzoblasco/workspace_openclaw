# Cata: Nova-Coder (Moderno Tech) vs modelos locales — 2026-11-05

**Modelo evaluado:** `ModernoTech/Nova-Coder` (HF) → `hf.co/ModernoTech/Nova-Coder:Q4_K_M` vía Ollama
**Baseline local:** `gemma4:12b-mlx`, `qwen3.5:9b-mlx`
**Hardware:** Mac mini M4, 10 cores, 24 GB RAM, macOS 27.2
**Alcance:** solo locales. Cero cloud. Cata chica por pedido de Gonzalo.

---

## 1. Veredicto en una línea

Nova-Coder **no es un modelo nuevo**: es `second-state/DeepSeek-Coder-V2-Lite-Instruct-GGUF` requantizado y rebrandeado. **Quedó primero en la cata de código (16/29) pero su default de contexto lo hace inusable sin tuning**, y en la práctica genera a 44 tok/s mientras consume 57 GB de memoria virtual con swap al 100%.

---

## 2. Qué es realmente el modelo

| Dato | Hallazgo | Fuente |
|---|---|---|
| Repo origen | `second-state/DeepSeek-Coder-V2-Lite-Instruct-GGUF` | campo `originRepo` del JSON de HF |
| Arquitectura | `DeepseekV2ForCausalLM`, 27 capas, 64 expertos enrutados, 6 activos | `config.json` + card |
| Parámetros | 15.7B totales (el card dice "~16B"); **DEEPSEEK LITE = 2.4B activos por token** | `api/ps` → `parameter_size: 15.7B` |
| Contexto declarado | 163.840 tokens | card + `api/ps` |
| Licencia | MIT (DeepSeek copyright 2023) + DeepSeek License Agreement | `LICENSE`, `LICENSE-DEEPSEEK-MODEL-NOTICE.md` |
| Downloads / likes | 61 / 0 (subido hoy mismo) | API de HF |
| Benchmarks propios | **ninguno**; el card lo admite: "No se publican benchmarks propios verificables" | card, sección Limitaciones |

El card se contradice: presenta "~16B parámetros" y compara con Nova Prime diciendo que más parámetros no implica mejor código, sin aclarar que es un MoE de 2.4B activos. Técnicamente honesto en la tabla de quantizaciones y en las limitaciones; **marketing en todo lo que rodea al nombre**.

---

## 3. Benchmark técnico (medido, no estimado)

| Métrica | ctx 8.192 (acotado) | ctx 163.840 (default del repo) |
|---|---|---|
| Prompt corto ("Di hola") | ~11 s | **208 s** (timeout a 900 s con prompt de 2 líneas) |
| Generación | **44–46 tok/s** | < 0.5 tok/s (swap thrashing) |
| Memoria del runner | ~17 GB VRAM | **57 GB totales, 69 % CPU / 31 % GPU** |
| Swap del sistema | normal | **15.9 GB de 16.4 GB usados** |

**El default del repo es una trampa.** Ollama toma `context_length` del GGUF (163.840) y arma el KV cache para eso. En 24 GB de RAM el modelo queda mayormente en CPU con swap saturado: la primera request tardó **16 min 55 s** en devolver 90 tokens. Con `num_ctx: 8192` el mismo modelo es perfectamente usable.

> Caveat del duelo atoi (2026-09-13) aplicado acá: **no es que "no pueda", es que no puede con ESTA configuración**. Cualquiera que lo levante sin tocar `num_ctx` va a concluir que el modelo es basura, y el problema es el cache de contexto.

---

## 4. Cata de código (suite oculta)

**Metodología:**
- 6 funciones, 29 casos ocultos, dificultad creciente (normalización de strings con reglas AR, chunks, top-k, DP con reconstrucción, parser recursivo desde cero, merge de intervalos).
- **Validación del test del test:** la suite corre 29/29 contra una solución de referencia escrita a mano. Solo entonces se mide.
- Mismo prompt verbatim para los tres modelos, `temperature: 0`, `num_ctx: 8192`.
- Un solo intento por caso (sin re-prompt). Los modelos de razonamiento que gastan el presupuesto en "thinking" y devuelven `content` vacío se cuentan como fallo de **entrega**, no de lógica.

| Función | Casos | Nova Q4_K_M | gemma4:12b | qwen3.5:9b |
|---|---:|---:|---:|---:|
| `normalize_phone` | 8 | **2** | 0 (entrega rota) | 0 (entrega rota) |
| `chunk_text` | 4 | **2** | **4** | 0 (entrega rota) |
| `top_k_words` | 3 | **2** | 0 (entrega rota) | 0 (entrega rota) |
| `coin_change` (DP + path) | 4 | **4** | **4** | **4** |
| `evaluate` (parser desde cero) | 6 | **4** | 0 | 0 (entrega rota) |
| `merge_intervals` | 4 | **2** | 0 | **4** |
| **TOTAL** | **29** | **16 (55 %)** | **8 (28 %)** | **8 (28 %)** |

**Ninguno aprueba.** 16/29 para el ganador es un resultado malo en términos absolutos: falla más de la mitad de los casos ocultos.

### Patrones observados

- **Nova** es el único que entrega código limpio y consistente en las 6. Sus fallos son de alcance de reglas (normalización telefónica: nunca acertó los 8 casos; el "15" local le rompe el parseo) y de bordes en `evaluate` — nunca devolvió basura.
- **gemma4 y qwen3.5** son modelos "thinking": el 100 % de sus respuestas empezaron como razonamiento y muchas **nunca llegaron a un bloque de código**. Con `num_predict` bajo devuelven `content` vacío y todo el texto en `thinking`. Como agentes esto es peor que un código malo: es no entregar.
- Donde los tres coinciden (coin_change) el problema es fácil y estructurado; donde divergen (parser, DP con reglas) se separan.

### Caveat importante sobre el scoring

Un subconjunto de fallos de gemma y qwen es de **extracción**, no de lógica: el runner tomó razonamiento como código cuando no había bloque ```` ```python ````. El retry con prompt más estricto terminó incompleto (se cortó a los 90 min). **Los números 8/29 son un piso, no una medida fina.** Aun así, el orden entre Nova y los otros dos no cambia: Nova entrega siempre, los otros fallan en entrega.

---

## 5. Comparación de uso real en el stack

| | Nova Q4_K_M | gemma4:12b-mlx | qwen3.5:9b-mlx | Cloud (referencia) |
|---|---|---|---|---|
| Rol actual | ninguno | fallback local de main | — | primario |
| Tamaño en disco | **10 GB** | 7.7 GB | 8.9 GB | — |
| RAM en inferencia | **17 GB** | 9.3 GB | 9.3 GB | — |
| tok/s (ctx 8k) | **44** | 28 | 14 | N/A |
| Entrega de código | **consistente** | errática (thinking) | errática (thinking) | — |
| Default usable sin tuning | **no** | sí | sí | N/A |

Nova es el más rápido de los tres y el más caro en memoria. Con el router actual (cloud primero, locales como último recurso) **no compite**: un 15.7B MoE / 2.4B activos de 2024 no reemplaza a `deepseek-v4.1-flash` ni a `gpt-oss:120b`.

---

## 6. Riesgos y banderas

1. **Rebranding sin declarar el origen en el nombre.** El nombre "Nova Coder" y la marca no son lo que corre. Quien lo adopte sin leer el JSON de HF no sabe que usa DeepSeek de 2024.
2. **Default de contexto destructivo.** Es el hallazgo más accionable: cualquier uso out-of-the-box termina en swap.
3. **Sin benchmarks, 61 descargas.** No hay evidencia independiente de calidad.
4. **Vendor nuevo y sin historial.** `ModernoTech` no tiene otros modelos con tracción.
5. **Licencia:** MIT + DeepSeek Agreement. Uso comercial permitido con restricciones de uso; si se usa en producto, hay que citar ambas.

---

## 7. Recomendación

**No adoptar.** No por el modelo (es un DeepSeek-Coder-V2-Lite competente y rápido), sino porque:
- no aporta nada que los locales no tengan,
- no compite con el router cloud,
- y el costo de memoria (17 GB) es el triple que el de gemma4 para un salto de calidad que no se puede demostrar.

**Si se quiere un local de código**, hay mejores candidatos que ya están en el stack cloud (`kimi-k2.7-code`, `glm-5.3`) y ninguno pasa por un vendor sin evidencia.

**Lo que sí vale la pena retener:**
- El **hallazgo de `num_ctx`**: cualquier modelo nuevo se debe levantar con contexto acotado y medir la penalización antes de juzgarlo.
- El **hallazgo de los thinking models**: gemma4 y qwen3.5 no entregan código sin prompt de salida estricto. Eso afecta su rol como *fallback* de main. Ver TODO.
- El **harness**: `/tmp/cata_nova/` tiene referencia + suite + runner. Sirve para la próxima cata.

---

## 8. Artefactos

- Suite: `/tmp/cata_nova/suite.py`, referencia `/tmp/cata_nova/ref_solutions.py`
- Salidas por modelo: `/tmp/cata_nova/out/{modelo}_{funcion}.{py,raw.txt}`
- Prompts congelados: `/tmp/cata_nova/prompts.json`
- Modelo descargado: `hf.co/ModernoTech/Nova-Coder:Q4_K_M` (10 GB en disco)

**Reproducir:**
```bash
ollama pull hf.co/ModernoTech/Nova-Coder:Q4_K_M
cd /tmp/cata_nova && python3 -u run_cata3.py
```

---

*Cata del 2026-11-05. Ninguna corrida usó modelos cloud. Tiempos medidos en la Mac mini, no estimados.*
