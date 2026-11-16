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
| Salida por iteración | 500 tokens | Estimación propia: un `tool_call` + razonamiento corto ronda eso. **No es dato del curso.** |

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
3. **La salida es 3× más cara que la entrada** ($1,98 vs. $0,66 en off-peak) *porque se genera secuencialmente* — el outline lo cita en 00:21:31. Pedir menos tokens de salida (respuestas cortas, `max_tokens` sensato) rinde más que recortar contexto.

## Cómo lo verificaría en serio

Este cálculo es a mano. La forma de no equivocarse es leer `usage` de la respuesta real:

```python
print(response.usage.prompt_tokens, response.usage.completion_tokens)
```

`response.usage` trae los números **reales** facturados, no la estimación. Un agente en producción que no loguea `usage` por llamada está adivinando su costo.

## Criterios de corrección

- [x] La cuenta está explícita y se puede reproducir.
- [x] El precio tiene fuente oficial y fecha de consulta.
- [x] Los supuestos propios (500 tokens de salida) están marcados como estimación, no como dato del curso.
- [x] Se señala el crecimiento del contexto, que la consigna no pide pero cambia el número.
- [x] Se indica cómo medir el costo real en vez de estimarlo.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
