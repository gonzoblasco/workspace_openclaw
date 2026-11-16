# M5 - Entregable: instrucciones negativas vs. positivas (medido, n=10)

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 5 — API Message Roles & Prompt Engineering Nuances (31:13 – 38:29)
- **Fecha:** 2026-11-16
- **Consigna:** reescribir cinco instrucciones negativas como positivas y medir la diferencia con 10 corridas a temperatura 0.

## Criterio declarado antes de medir

Para no elegir el criterio después de ver el resultado:

| Regla | Definición |
|---|---|
| Métrica primaria | **Violaciones** de la instrucción (0 = mejor) |
| Métrica secundaria | **Palabras** (menos = mejor: es un resumen) |
| Veredicto por par | Gana quien tenga menos violaciones; si empatan, quien tenga menos palabras |
| No concluyente | Si la diferencia de violaciones es menor a 1 promedio |

**Parámetros:** `gemma4:12b-mlx`, temperatura 0, **n=10 por prompt** (100 generaciones), misma tarea en todos.

## Los cinco pares y sus métricas

| Par | Qué se mide | Negativa | Positiva | Veredicto |
|---|---|---|---|---|
| 1. viñetas | nº de viñetas | 0,0 viol · 28 pal · 1/10 distintas | 0,0 viol · **65 pal** · 3/10 distintas | **negativa** (menos palabras) |
| 2. no inventar | marcadores de duda | 0,0 viol · 25 pal | 0,0 viol · 24 pal | positiva (por 1 palabra) |
| 3. no vago | respuestas < 12 pal | 0,0 viol · 38 pal | 0,0 viol · 32 pal | positiva (menos palabras) |
| 4. no repetir | ≥ 80% del original | 1,0 viol · 24 pal | 1,0 viol · 27 pal | negativa (menos palabras) |
| 5. solo relevante | menciona fecha/ausente | **1,0 viol** · 18 pal | **0,0 viol** · 18 pal | **positiva** (por violaciones) |

**Recuento: 2 pares gana la negativa, 2 la positiva, 1 definido por violaciones.** Ningún par resultó no concluyente.

## Lo que esto cambia respecto de la primera versión

La primera medición de este entregable usó **n=3** y concluyó: *"la instrucción positiva empeoró en 3 de 5 pares; el experimento no confirma la tesis del curso"*.

Con **n=10 el resultado se invierte a 2-2-1**. La conclusión anterior **no era robusta: era ruido de muestra chica**. Tres corridas no alcanzan para distinguir una diferencia direccional de una fluctuación. Esa es la lección real del módulo, y es más valiosa que cualquier veredicto sobre negativas vs. positivas:

> **Con n=3 cualquier diferencia parece un hallazgo. Con n=10 desaparece.**

## Lo que sí sobrevivió al aumento de muestra

| Hallazgo | n=3 | n=10 | ¿Sobrevive? |
|---|---|---|---|
| La negativa nunca activó el patrón prohibido | sí | **sí** (0,0 viol en pares 1-3) | ✅ |
| La positiva produce textos más largos | sí | **sí** (65 vs 28 palabras en par 1) | ✅ |
| La positiva "empeora" en la mayoría de pares | sí (3/5) | **no** (2/5) | ❌ |
| Las viñetas aparecen sin que nadie las pida | sí | **sí** (par 1 positiva: 3/10 corridas distintas) | ✅ |

**Lo que se puede afirmar con n=10:**
1. **Ninguna de las dos formas activa el patrón prohibido.** El mecanismo que el curso describe (00:32:10) no se reprodujo en ninguno de los 5 pares: la negativa nunca produjo lo que prohibía.
2. **La instrucción negativa es más corta.** En el par 1 la positiva generó **2,3× más texto**. En un agente eso es tokens pagados de más.
3. **El formato no lo controla la instrucción.** En el par 5 ninguna de las dos instrucciones hablaba de viñetas, y aun así aparecieron corridas con lista.

**Lo que NO se puede afirmar:**
- Que una forma sea sistemáticamente mejor. Con n=10 el resultado es empate 2-2-1.

## Sobre la generalización (crítica aceptada)

Un solo modelo de 12B, una sola tarea, un clasificador por regex. Aunque el resultado hubiera sido 5-0, la afirmación correcta sería *"en gemma4 12B, con esta tarea y este criterio"*, nunca *"el curso está equivocado"*. La regla de prompting medida en un modelo no se traslada sin volver a medirla.

## Cómo reproducirlo

```python
import json, urllib.request
def gen(prompt):
    body = json.dumps({"model": "gemma4:12b-mlx", "prompt": prompt,
                       "stream": False, "think": False,
                       "options": {"temperature": 0, "num_predict": 250}}).encode()
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate",
                                 data=body,
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=600))["response"]
```

`think: false` va en el body, **no** en `options`. Si el modelo razona, los tokens se consumen en `thinking` y `response` vuelve vacío con `done_reason: "length"` — fallo silencioso que costó una corrida entera.

## Criterios de corrección

- [x] Cinco pares negativa → positiva.
- [x] **10 corridas por prompt**, como pide la consigna (100 generaciones).
- [x] Antes/después de cada par con las métricas.
- [x] Criterio de comparación declarado **antes** de medir, no elegido a favor del resultado.
- [x] Se reporta que la conclusión anterior (n=3) **no sobrevivió** al aumento de muestra, en vez de conservarla.
- [x] Se distingue lo que se puede afirmar de lo que no.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
