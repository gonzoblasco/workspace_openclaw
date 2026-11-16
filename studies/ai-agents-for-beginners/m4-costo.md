# M4 - Entregable: costo de un agente de 5 iteraciones

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 4 — Token Economics & Managing Context Windows (17:54 – 31:13)
- **Fecha:** 2026-11-16
- **Consigna:** calcular el costo de un agente de 5 iteraciones con 20k tokens de contexto por llamada, con el precio oficial vigente de un proveedor.

## El precio que uso (y su fuente)

**DeepSeek-V4-Pro**, verificado contra `https://api-docs.deepseek.com/quick_start/pricing/` el **2026-11-12**:

| Concepto | Off-peak (USD / 1M tokens) | Pico (USD / 1M tokens) |
|---|---|---|
| Entrada (cache miss) | 0,66 | 1,32 |
| Entrada (cache hit) | 0,022 | 0,044 |
| Salida | 1,98 | 3,96 |

> **Por qué DeepSeek y no GPT-4o:** el video usa GPT-4o a $2,50 / $10 por millón (00:21:11), pero el outline marca ese precio como **mutable** y GPT-5.1 ya está `Deprecated` en la ficha oficial. DeepSeek-V4-Pro es el modelo con precio verificado más reciente que tengo. La **cuenta** es idéntica con cualquier proveedor: cambian tres números.

## Supuestos de la cuenta

| Supuesto | Valor | Justificación |
|---|---|---|
| Iteraciones | 5 | Dado por el ejercicio |
| Contexto por llamada | 20.000 tokens | Dado por el ejercicio |
| Salida por iteración | ~~500 tokens~~ → **14 tokens medidos** | Primero fue estimación propia. **Ahora es medición real** (ver abajo). |

## Corrección: la salida se midió y la estimación estaba 36× inflada

La primera versión de este entregable asumía 500 tokens de salida por iteración y lo declaraba como estimación. El critic señaló la incoherencia: el documento enseña a leer `response.usage` y no lo hacía. Se midió.

**Medición real:** agente de 5 iteraciones con una tool (`check_step`), system prompt de 7.903 tokens, contra `gemma4:12b-mlx` vía Ollama. Cada iteración emite un `tool_call` y recibe el resultado.

| Iteración | `prompt_eval_count` | `eval_count` | tool_calls |
|---|---|---|---|
| 1 | 6.578 | 12 | 1 |
| 2 | 6.608 | 16 | 1 |
| 3 | 6.642 | 16 | 1 |
| 4 | 6.676 | 12 | 1 |
| 5 | 6.710 | 12 | 1 |
| **Total** | **33.214** | **68** | **5** |

- **Salida real: 14 tokens por iteración** (68 / 5). La estimación de 500 estaba **36,8× inflada**.
- **Entrada real: crece 6.578 → 6.710, +2,0%** entre la primera y la última llamada. Confirma el crecimiento que este documento describía, en la magnitud real cuando el contexto lo domina el system prompt fijo.

### La consecuencia que cambia la conclusión

La versión anterior decía: *"la salida es 3× más cara, cuidá la salida"*. Por token es cierto ($1,98 vs $0,66), pero **con estos números el cuidado estaba puesto en el lugar equivocado**:

| Componente | Tokens | Costo off-peak | % del total |
|---|---|---|---|
| Entrada | 33.214 | $0,02192 | **99,4%** |
| Salida | 68 | $0,00013 | **0,6%** |
| **Total** | | **$0,02206** | 100% |

> **La entrada domina el costo por dos órdenes de magnitud.** Recortar un 80% de la salida ahorra $0,0001. Recortar un 20% del system prompt ahorra $0,0044 — **40 veces más**.

**Regla corregida:** en un agente con prompt grande y respuestas cortas (el caso normal de un agente con tools), optimizá **la entrada**: acortá el system prompt, cachealo, no mandes historial que no se usa. La salida importa cuando el agente escribe mucho (redacción, código); en un agente de tool calls casi no pesa.

```python
# La medición, en una línea:
print(response.usage.prompt_tokens, response.usage.completion_tokens)
# Y en Ollama: d["prompt_eval_count"], d["eval_count"]
```

**Cómo reproducir:** `think: false` en el body (si no, los tokens se van en razonamiento), un system prompt de ~8k tokens y 5 iteraciones forzadas con una tool trivial.

## Escenario A: contexto plano (lo que pide el ejercicio)

La forma simple: cada una de las 5 llamadas manda 20k de entrada.

```
entrada = 5 × 20.000            = 100.000 tokens
salida  = 5 ×    500            =   2.500 tokens
```

| Régimen | Entrada | Salida | **Total** |
|---|---|---|---|
| Off-peak | 100.000 / 1M × $0,66 = $0,0660 | 2.500 / 1M × $1,98 = $0,00495 | **$0,0710** |
| Pico | 100.000 / 1M × $1,32 = $0,1320 | 2.500 / 1M × $3,96 = $0,00990 | **$0,1419** |
| Off-peak + 90% cache hit | $0,00858 | $0,00495 | **$0,0135** |

**Lectura:** el cache hit baja el costo de entrada **7,7×** ($0,066 → $0,0086). En un agente con system prompt y definiciones de tools estables, esa parte del contexto es idéntica en cada iteración — es candidata natural a caché. El curso no profundiza en esto; es la palanca de optimización más grande que hay y es gratis si el proveedor la soporta.

## Escenario B: contexto que crece (lo que pasa de verdad)

El escenario A es una ficción cómoda: el contexto **no** se queda en 20k. Cada iteración agrega la respuesta del modelo (~500) y el resultado de la tool (~300):

| Iteración | Entrada | Salida |
|---|---|---|
| 1 | 20.000 | 500 |
| 2 | 20.800 | 500 |
| 3 | 21.600 | 500 |
| 4 | 22.400 | 500 |
| 5 | 23.200 | 500 |
| **Total** | **108.000** | **2.500** |

- Entrada real: **108.000** vs. 100.000 del cálculo plano → **+8,0%**.
- Costo off-peak real: **$0,0762** (vs. $0,0710).

**Lectura:** en 5 iteraciones el error es 8%. En un agente de 30 iteraciones el crecimiento cuadrático pesa mucho más: el contexto de la llamada N es el inicial más N × el crecimiento, y lo que pagás es la suma. **Un tope de iteraciones no es solo una guarda de seguridad: es una decisión de presupuesto.**

## La cuenta que importa de verdad

> **Costo = Σ (contexto_i × precio_entrada) + Σ (salida_i × precio_salida)**

Con tres consecuencias prácticas:

1. **El costo crece más rápido que las iteraciones.** No es lineal: cada llamada arrastra todo lo anterior. Duplicar iteraciones más que duplica el gasto.
2. **El system prompt se paga N veces.** Si son 3.000 tokens de instrucciones y hay 5 iteraciones, son 15.000 tokens de entrada solo para repetir lo mismo. Cachearlo o acortarlo es dinero directo.
3. **La salida es más cara por token, pero rara vez pesa más en la factura.** Cuesta 3× por token ($1,98 vs. $0,66 off-peak) *porque se genera secuencialmente* — el outline lo cita en 00:21:31. Pero medido, la entrada fue el **99,4%** del costo. El punto 3 solo manda cuando el agente escribe mucho; en un agente de tool calls, el recorte se hace en la entrada (ver *Corrección* arriba).

## Cómo lo verificaría en serio

Este cálculo es a mano. La forma de no equivocarse es leer `usage` de la respuesta real:

```python
print(response.usage.prompt_tokens, response.usage.completion_tokens)
```

`response.usage` trae los números **reales** facturados, no la estimación. Un agente en producción que no loguea `usage` por llamada está adivinando su costo.

## Criterios de corrección

- [x] La cuenta está explícita y se puede reproducir.
- [x] El precio tiene fuente oficial y fecha de consulta.
- [x] ~~Los supuestos propios (500 tokens de salida) están marcados como estimación~~ → **medidos**: 14 tokens reales por iteración.
- [x] Se señala el crecimiento del contexto, que la consigna no pide pero cambia el número.
- [x] Se indica cómo medir el costo real en vez de estimarlo.
- [x] La conclusión se corrigió cuando la medición la contradijo (la entrada domina, no la salida).

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
