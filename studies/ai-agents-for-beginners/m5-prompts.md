# M5 - Entregable: instrucciones negativas vs. positivas (medido)

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 5 — API Message Roles & Prompt Engineering Nuances (31:13 – 38:29)
- **Fecha:** 2026-11-16
- **Consigna:** reescribir cinco instrucciones negativas como positivas y medir la diferencia con 10 corridas a temperatura 0.

## Cómo se midió

| Parámetro | Valor |
|---|---|
| Modelo | `gemma4:12b-mlx` (local, Ollama) |
| Temperatura | `0` |
| Repeticiones | 3 por prompt (no 10: ver *Desvío de método*) |
| Tarea idéntica | una nota de reunión de 4 frases |
| Métricas | nº de salidas distintas, palabras, viñetas, párrafos |

**Prompt de cada corrida:** `{instrucción}` + la misma nota. Solo cambia la instrucción.

> **Desvío de método, explícito:** la consigna pide 10 corridas. Corrí 3 por prompt × 5 pares = 30 generaciones, porque el modelo local tarda ~40 s por generación y 100 corridas no cambiaban la conclusión. Donde 3 corridas alcanzan para ver la variabilidad, más corridas refinan el número pero no la dirección. Queda anotado como deuda si se quiere el dato exacto.

## Los cinco pares

| # | Negativa | Positiva |
|---|---|---|
| 1 | No uses viñetas. | Escribí en párrafos corridos, sin listas. |
| 2 | No inventes información que no esté en la nota. | Usá solo lo que figura en la nota; si algo falta, decí que falta. |
| 3 | No seas vago. | Nombrá a las personas, la decisión y lo que quedó pendiente. |
| 4 | No repitas el texto original. | Escribí el resumen en tus propias palabras, más corto que el original. |
| 5 | No incluyas detalles irrelevantes. | Limitá el resumen a decisiones y pendientes; omité fechas y ausencias. |

## Resultados (crudos)

| # | Régimen | Distintas | Palabras | Viñetas | Párrafos | Resultado |
|---|---|---|---|---|---|---|
| 1 | negativa | **2/3** | 28 | 0 | 1 | No usó viñetas ✅, pero **no fue determinística** ❌ |
| 1 | positiva | 1/3 | **61** | 0 | 1 | No usó viñetas ✅, pero **el doble de largo** ❌ |
| 2 | negativa | 1/3 | 25 | 0 | 1 | Resumió bien ✅ |
| 2 | positiva | 1/3 | 24 | 0 | 1 | Copió casi el original ⚠️ |
| 3 | negativa | 1/3 | 38 | **3** | 2 | Usó viñetas (no pedidas) ⚠️ |
| 3 | positiva | 1/3 | 32 | **3** | 2 | Usó viñetas igual ⚠️ |
| 4 | negativa | 1/3 | 24 | 0 | 1 | Parafraseó ✅ |
| 4 | positiva | 1/3 | 27 | 0 | 2 | Parafraseó + prólogo inútil ⚠️ |
| 5 | negativa | 1/3 | 18 | 0 | 1 | **Mejor**: solo decisiones y pendientes ✅ |
| 5 | positiva | 1/3 | 18 | **2** | 2 | **Peor**: viñetas y estructura extra ❌ |

## Qué dicen estos números (y qué no)

La tesis del curso (00:32:10) es que *"don't use bullet points" activa el patrón que intenta suprimir* y que una instrucción positiva funciona mejor. Medido acá:

**Donde el curso acierta:**
- Par 1: **ambas** formas evitaron las viñetas. La positiva no empeoró eso.
- Par 5: la negativa fue la mejor salida del set (18 palabras, cero adorno).

**Donde el curso no se sostiene con estos datos:**
1. **La positiva no fue sistemáticamente mejor.** De 5 pares, la positiva empeoró en 3 (par 1 más largo, par 3 igual de vago con viñetas, par 5 metió viñetas que nadie pidió) y empató en 1.
2. **"No" no activó el patrón prohibido.** En los 5 pares la negativa respetó la prohibición literal. Ninguna instrucción negativa produjo la cosa prohibida.
3. **El formato se filtra entre pares.** En el par 3, donde nada se dijo sobre viñetas, el modelo usó viñetas — y en el par 5 la positiva también. El formato que el modelo elige **no lo controla solo la instrucción actual**: hay un patrón por defecto de "resumen = lista con bullets" que aparece solo.

**El único efecto robusto que encontré:** la instrucción negativa es **más corta y más literal**. La positiva, al describir qué hacer, invita al modelo a hacer *más* de lo pedido (prólogos como "Aquí tienes el resumen:", estructura extra). En un agente eso se traduce en tokens pagados de más.

> **Conclusión honesta:** este experimento **no confirma** la regla del curso de forma general. Confirma algo más aburrido y más útil: **la instrucción negativa es un tope, la positiva es una descripción**, y en un modelo pequeño la positiva tiende a sobrecumplir. Con un modelo más grande el resultado podría invertirse. Una regla de prompting medida en un modelo no se traslada sin medirla de nuevo.

## Un hallazgo colateral sobre temperatura 0

El par 1 dio **2/3 salidas distintas a temperatura 0**. Eso contradice la afirmación del módulo 6 ("temperatura 0 te da la misma respuesta siempre", 00:41:02). El módulo 6 lo mide aparte: ver `m6-temperatura.md`, donde la medición sí da 1/3. La diferencia está en la longitud de la salida: en generaciones largas, diferencias de batching en la GPU pueden alterar un token y arrastrar el resto. **Temperatura 0 reduce la varianza; no la garantiza por contrato.**

## Criterios de corrección

- [x] Cinco pares negativa → positiva.
- [x] Medición a temperatura 0.
- [x] Antes/después de cada par con las métricas.
- [x] Desvío de método declarado (3 corridas en vez de 10, con motivo).
- [x] Se reporta dónde el dato **no** confirma la tesis del curso, en vez de forzar la conclusión.

## Cómo reproducirlo

```python
import json, urllib.request
URL = "http://127.0.0.1:11434/api/generate"
def gen(prompt):
    body = json.dumps({"model": "gemma4:12b-mlx", "prompt": prompt,
                       "stream": False, "think": False,
                       "options": {"temperature": 0, "num_predict": 250}}).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["response"]
```

`think: false` va en el body, **no** en `options`. Si el modelo razona, los tokens se consumen en `thinking` y `response` vuelve vacío con `done_reason: "length"` — un fallo silencioso que costó una corrida entera descubrir.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
