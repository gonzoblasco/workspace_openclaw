# Cata de modelos Ollama Cloud — 2026-11-04

**Estado:** medición hecha, decisión pendiente
**Autor:** Kanam CORE
**Alcance:** catálogo cloud completo (24 modelos) + cata de 9 modelos sobre un artefacto con 4 bugs sembrados.

---

## 0. Corrección de encuadre (la que ordena todo)

Con el plan **Pro Legacy** el costo **no se mide en dinero ni en tokens facturados**: se mide en
**cuota de GPU** (barra de uso con reset) y **slots de concurrencia** (3).

Corolario medido el 2026-10-24: `glm-5.3-flash` gastó un tercio de la cuota semanal con un quinto
de los requests (**0,29 px/req** contra **0,053** de `deepseek-v4.1-flash`).

**Límite de resolución descubierto hoy:** la barra semanal tiene ~935 px de ancho para 4.407
requests de deepseek → **0,067 px por request**. Un request de cata es **invisible** en la barra.
Para medir candidatos nuevos la barra no sirve: sirven `request_count` exacto (`/api/usage`) y
`eval_count` (tokens de salida, que incluyen thinking).

---

## 1. El catálogo son 24, no 20

`https://ollama.com/search?c=cloud` carga por HTMX con scroll infinito
(`hx-get="/search?page=2"` + `hx-trigger="revealed"`). `web_fetch` y `curl` devuelven **solo los
primeros 20**. La lista completa requiere navegador con scroll.

Los 4 que faltaban en la lectura inicial: `gpt-oss`, `deepseek-v4-pro`, `kimi-k2.6`, `mistral-large-3`.

**Regla:** una página de listado leída con `web_fetch` no es el catálogo. Verificar con navegador.

---

## 2. Retiros confirmados por mail (2026-10-28) — NO están en las fichas

| Modelo | Retiro |
|---|---|
| `nemotron-3-nano:30b-cloud` | 2026-11-09 |
| `mistral-large-3:675b-cloud` | 2026-11-09 |
| `minimax-m2.7:cloud` | 2026-11-09 |

El aviso vive en el mail y en usage settings. `docs.ollama.com/cloud#retirements` solo dice "mirá
tus usage settings". **La ficha del modelo nunca lo avisa.**

Impacto verificado: **ningún rol activo los usa.** Las 4 apariciones están en
`modelPolicy.allow` (lista estática). `nemotron-3-nano:4b` ya respondía "model not found".

---

## 3. La cata

**Diseño:** artefacto `bench/base/reports.py` con 4 bugs sembrados (`bench/seed_bugs.py`:
BUG-1 y BUG-2 visibles en los tests, BUG-3 y BUG-4 ocultos). Prompt único de 9.177 caracteres con
spec + implementación + tests inline (los cloud no tienen shell ni filesystem), `temperature=0`,
`num_predict=8192`. Una llamada por modelo.

**Métrica:** recall por marcadores sobre content + thinking.

### Resultados

| Modelo | Recall | out_tok | thinking | latencia | Entrega |
|---|---:|---:|---:|---:|---|
| `gpt-oss:120b` | **4/4** | **2.546** | 8.954 c | **6,0 s** | ✅ |
| `muse-spark-open` | **4/4** | **2.648** | 9.607 c | 10,3 s | ✅ |
| `kimi-k3.1-pro` | **4/4** | 3.643 | 13.639 c | 64,9 s | ✅ |
| `mimo-v2.6-flash` | **4/4** | 5.868 | 18.734 c | 29,1 s | ✅ |
| `mistral-large-4` | **4/4** | 7.346 | 24.732 c | 58,3 s | ✅ |
| `mimo-v2.6-pro` | **4/4** | 8.192 (tope) | 27.123 c | 21,3 s | ✅ |
| `deepseek-v4.1-flash` | — | 8.192 (tope) | 32.683 c | 29,9 s | ❌ **0 content** |
| `minimax-m3.1-flash` | — | 8.192 (tope) | 31.696 c | 30,6 s | ❌ **0 content** |
| `clef` | n/a | — | — | 0,2 s | ❌ HTTP 400 |

### Re-test con tope alto (la prueba decisiva)

| Modelo | out_tok real | content | thinking | latencia | Recall |
|---|---:|---:|---:|---:|---:|
| `deepseek-v4.1-flash` | **9.161** | 1.599 c | 35.028 c | 32,0 s | **4/4** |
| `minimax-m3.1-flash` | 7.953 | 4.322 c | 27.039 c | 23,9 s | **4/4** |

**Consumo total de la cata: 48 requests, ~47.357 tokens de salida** (30.243 de la corrida base +
8.192 de la primera pasada fallida de deepseek y minimax + 9.161 y 7.953 de los re-tests con tope
alto). Es el 0,5% de la cuota semanal.

### Hallazgos

1. **El recall satura.** 6 de 6 modelos que entregaron encontraron los 4 bugs. La métrica no
   discrimina: el artefacto es demasiado fácil para este nivel. **No sirve para rankear calidad.**

2. **Los dos modelos "de casa" no entregaron EN LA PRIMERA CORRIDA — y era mi tope, no el modelo.**
   Con `num_predict=8192` quemaron todo en thinking y devolvieron 0 content. **Re-testeados con
   tope 24.000: los dos entregaron 4/4.** `deepseek` necesitó **9.161** tokens de salida — más que
   el tope original, por eso truncó. **No hay espiral infinita.** Lección: un `num_predict` bajo
   produce un falso negativo que se lee exactamente igual que el modo de fallo real de minimax.
   El ADR-102 ya advertía que minimax tenía espiral; este test muestra que con tope suficiente
   entrega, y que **deepseek consume MÁS que minimax en esta tarea** (9.161 vs 7.953).

3. **`clef` da 400 por diseño:** no es un modelo de chat, usa `/v1/systemone`. Confirma la ficha.

4. **Costo por entrega:** 2.546 tok (gpt-oss) a 9.161 (deepseek con tope alto) = **3,6× de spread**.
   Igual que el spread de cuota medido en octubre (5,5×).

### Límites de esta cata (honestos)

- **El tope de tokens hay que fijarlo por modelo, no global.** 8.192 truncó a 2 de 9 modelos y
  produjo un falso negativo. Toda corrida futura: `num_predict >= 16000` o sin tope.
- **Una sola llamada por modelo.** Sin repetición, no hay varianza.
- **Recall saturado** ⇒ no hay ranking de calidad. Falta una tarea discriminante (el prompt pesado
  de `model-cata` con 5-7 decisiones y la clase "premisa falsa").
- **`/api/usage?group_by=model` corta en 10 grupos**: los modelos nuevos caen en `remainder` y no se
  puede leer su delta individual.

---

## 4. Cuota medida sobre uso real (2026-11-04, panel)

Barra semanal: 933 px para 4.484 requests de deepseek → **0,065 px/req**.
Barra de sesión: 937 px, 287 requests de deepseek → **0,49 px/req**.

**Las dos ventanas no dan el mismo px/req** porque una request no cuesta lo mismo que otra
(depende de contexto y thinking). Por eso el costo de un modelo se expresa como **rango**.

| Medición | Resultado |
|---|---|
| 1 request de `kimi-k3.1-pro` | **7 px** = **4,7%** del consumo de la sesión |
| Equivalencia | 1 request de Kimi ≈ **14×** deepseek (sesión) a **22×** (semanal) |
| 35 requests de familia Kimi (semana) | 53 px = 18% de los px de deepseek con 0,8% de sus requests |

**Lección:** la estimación inicial del owner ("casi el 10%") era **2× la real**. La barra a ojo
sobreestima los modelos de color saturado y subestima los azules. Medir, no estimar.

### Licencia de Muse Spark Open (verificada 2026-11-04)

Muse Model License (Meta, 15/10/2026). La restricción de USD 20M aplica **solo** a
"Model as a Service" (exponer el modelo a terceros vía API). Textual: *"This Section 3 does not
apply to (a) **internal use**, research, or any commercial activity that is not Model as a Service"*.

- **Uso interno: sin restricción.**
- **Obligación real:** mostrar *"Built with Muse Spark Open"* en la UI de cada producto o servicio
  que lo use, o en documentación/settings. No aplica a tooling interno sin superficie pública.
- Se permite modificar, fine-tunear y crear derivados. Meta no reclama los outputs.

### Asignación resultante

| Uso | Modelo | Evidencia |
|---|---|---|
| Auditoría de camino (periódica, no de código) | `kimi-k3.1-pro` | 1 req = 4,7% de sesión; perfil 3T con factual accuracy. Uso puntual, nunca en pipeline |
| Alternativa interna / A del pipeline | `muse-spark-open` | 2.648 tok, 4/4, 10,3 s. Licencia OK para uso interno |
| A del pipeline (titular) | `gpt-oss:120b` | 2.546 tok, 6,0 s |
| B (revisa) | `deepseek-v4.1-flash` | mejor revisor medido (cata de roles) |
| CORE | `deepseek-v4.1-flash` | sin cambio |
| Triage / pre-filtro | `gemma4` | 1.769 req ≈ una línea de barra |

## 7. Cata discriminante: kimi-k3.1-pro vs deepseek-v4.1-flash (2026-11-04)

Tres tareas **sin código**, cada una con trampas verificables. `num_predict=20000`.

| Tarea | Marcadores | Kimi | DeepSeek | Juicio de Kanam |
|---|---|---|---|---|
| **T1 Planificación** | 4/4 | 4/4 | 4/4 | **DeepSeek** |
| **T2 Auditoría de camino** | 4/4 | 4/4 | 4/4 | **DeepSeek** |
| **T3 Creativo (voz)** | 4/5 | 4/5 | 4/5 | **Kimi** |

**Los marcadores volvieron a saturar.** No rankean; el juicio es de lectura, y eso queda dicho.

### T1 — Planificación: gana DeepSeek (ajustado)

Ambos cazaron las tres trampas: el paralelismo que come los 3 slots, el frente caro (feature+tests)

y el margen del 61,3% restante. Diferencia:

- **DeepSeek** operacionaliza el riesgo: *"~15% de la barra por día; si se acerca a 85-90% usado,
  corto requests de (a) hasta el reset"*. Un umbral accionable, no una advertencia.
- **Kimi** está mejor estructurado pero es más genérico (*"presupuestar sus bloques, limitar reintentos"*).
- Costo: Kimi 3.776 tok / 47,2 s · DeepSeek 6.034 tok / 23,4 s. **Kimi más barato en tokens,
  DeepSeek 2× más rápido.** (Otra vez: el costo depende de la tarea, no del modelo.)

### T2 — Auditoría de camino: gana DeepSeek (claro)

Ambos marcaron la circularidad del self-audit y del repair loop, y ambos dijeron "no construir más".
Diferencia:

- **DeepSeek encontró hallazgos que Kimi no vio:** el SSRF guard solo prueba los casos listados
  (*"no prueba ausencia de bypasses como DNS rebinding, redirects, proxies o IPv6 exóticas"*), y
  separó el caso `gpt-oss` como contraejemplo de "prompt model-agnostic".
- **Kimi** es correcto y prudente, pero se queda en lo declarado por el documento.
- Costo: Kimi 4.452 tok / **58,2 s** · DeepSeek 4.057 tok / **18,2 s**. DeepSeek gana en las tres.

### T3 — Creativo: gana Kimi

| | Kimi | DeepSeek |
|---|---|---|
| Apertura | *"Me hubiera gustado otro resultado en el proceso"* | *"Me rechazaron para [rol]"* |
| Petición | con alcance amplio y pregunta concreta | correcta |
| Cierre | *"si hay encaje, avancemos; si no, prefiero que me lo digas directo"* | *"si hay, lo vemos; si no, dímelo"* |
| Registro | conserva agencia, no se rebaja | seco hasta el borde de amargo |

**Kimi entendió que "confianza con filo" no es "decir un rechazo en voz pasiva".** DeepSeek fue
correcto en estructura pero el arranque con *"me rechazaron"* le cede el sujeto al otro.
Costo casi idéntico (1.386 vs 1.336 tok). **Kimi gana donde el matiz es el trabajo.**

### Veredicto de la cata discriminante

**No hay un ganador único, y esa es la respuesta correcta:**

- **DeepSeek** para trabajo operativo: planificar con umbrales, auditar buscando lo no declarado.
  Más barato en latencia (2,4× más rápido en el agregado) y más profundo en detección.
- **Kimi K3.1 Pro** para trabajo de **matiz**: voz, redacción, auditoría de camino cuando importa
  el juicio y no la lista. 14-22× el costo por request, justificado solo si se usa poco.

## 8. Distribución ideal por agente y uso

Criterios, en orden: (1) evidencia medida, (2) **diversidad de voces** (pedido explícito de Gonzo:
A ≠ B, no un monólogo), (3) cuota, (4) latencia.

| Slot | Modelo | Familia | Fundamento |
|---|---|---|---|
| `main` (CORE) | `deepseek-v4.1-flash` | DeepSeek | content 8.3 (mejor de la cata de roles) + 0,053 px/req |
| `kanam-dev` (A) | `gpt-oss:120b` | OpenAI | 2.546 tok, 6 s; el más barato por entrega |
| `kanam-ops` | `gpt-oss:120b` | OpenAI | latencia 3 s contra 40 s de deepseek en tarea de seguridad |
| `kanam-critic` (B) | `deepseek-v4.1-flash` | DeepSeek | mejor revisor medido (4/4, 9 hallazgos) |
| `kanam-auditor` (código) | `nemotron-3-super` | NVIDIA | 2/2 bugs en 3,6 s; ultra quedó descartado |
| `kanam-planner` | `deepseek-v4.1-flash` | DeepSeek | T1: único que dio umbral operativo de cuota |
| `kanam-mind` | `deepseek-v4.1-flash` | DeepSeek | 8.7, el mejor del rol |
| `kanam-studio` | `deepseek-v4.1-flash` → `glm-5.3-flash` (pasada profunda) | DeepSeek | ADR-080; ojo: el fallback cuesta 5,5× |
| Pipeline C (tests) | `minimax-m3.1-flash` | MiniMax | 17/40 wins absolutos |
| **Auditoría de camino** (periódica) | **`kimi-k3.1-pro`** | Kimi | T3 y T2: matiz. 1 req = 4,7% de sesión |
| **Redacción con voz** (LinkedIn, cartas) | **`kimi-k3.1-pro`** | Kimi | T3: el único que no se rebajó |
| Triage / pre-filtro | `gemma4` | Google | 0,5 s, 12 tok |

**Cinco familias en doce slots.** A (OpenAI) y B (DeepSeek) no comparten prior.

### Cambios vs la config actual

| Rol | Hoy | Propuesto | Motivo |
|---|---|---|---|
| `planner` | `gpt-oss` low | `deepseek` | T1: dio el umbral de cuota; gpt-oss no lo hizo |
| `planner` fallback | `gemma4` | `gemma4` (sin cambio) | — |
| `studio` | `gemma4:cloud` | `deepseek` | ADR-080: gemma4 alucinó un defecto de contraste |
| Purga | `minimax-m2.7`, `mistral-large-3`, `nemotron-3-nano:30b` | fuera | Se retiran el 2026-11-09 |

**Sin cambio:** `main`, `dev`, `ops`, `critic`, `auditor`, `mind`, pipeline A/B/C.

### Lo que NO recomiendo cambiar

- **No poner Kimi en ningún rol fijo.** 14-22× por request en un rol que corre todo el día agota la
  cuota. Es un convocado, no un titular.
- **No usar el mismo modelo en A y B.** Con deepseek en los dos, B valida el estilo de A por
  construcción.
- **No volver a `glm-5.3-flash` como default.** 0,29 px/req = 5,5× deepseek, medido.

## 9. Lo que NO cambia

- Ninguno de los 24 genera imágenes, audio, video ni documentos. `vision`/`audio` son **entrada**.
  `clef` devuelve probabilidades, no texto.
- `deepseek-v4.1-flash` sigue siendo el mejor medido en la cata de roles (content 8.3) y el más
  barato en cuota (0,053 px/req).
- Diversidad de voces en el pipeline: **A ≠ B**, confirmado por Gonzo. El mismo modelo en A y B no
  es un pipeline, es un monólogo.

## 10. Pendientes

- [ ] Tarea discriminante de calidad (prompt pesado, clase C "premisa falsa").
- [ ] Medir cuota por modelo de los 5 nuevos con 10 requests secuenciales cada uno.
- [ ] Purgar `minimax-m2.7`, `mistral-large-3`, `nemotron-3-nano:30b` de `modelPolicy.allow` antes
      del 2026-11-09.
- [ ] `num_predict` mínimo de 16.000 en toda cata futura (8.192 produjo falso negativo).

## Artefactos

- Harness: `bench/cata-2026-11-04/run_cata.py`
- Resultados crudos: `bench/cata-2026-11-04/results.json`
- Artefacto sembrado: `bench/cata-2026-11-04/work/`
