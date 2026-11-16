# M6 - Entregable: temperatura 0 vs. temperatura 1 (medido)

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 6 — Hands-On Lab: Practice Labs & First API Call (38:29 – 45:01)
- **Fecha:** 2026-11-16
- **Consigna:** correr el programa dos veces con temperatura 0 y dos con temperatura 1, y anotar qué cambió y qué no.

## El programa

El curso propone siete líneas. Esta es la versión que corrí, contra Ollama local (sin API key, sin costo):

```python
import json, urllib.request

URL = "http://127.0.0.1:11434/api/generate"

def generate(prompt, temperature):
    body = json.dumps({
        "model": "gemma4:12b-mlx",
        "prompt": prompt,
        "stream": False,
        "think": False,                      # sin esto, los tokens se van en razonamiento
        "options": {"temperature": temperature, "num_predict": 60},
    }).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["response"].strip()

PROMPT = "Write one short sentence about a robot."

for temp in (0, 1):
    for run in range(1, 4):
        print(f"T={temp} run {run}: {generate(PROMPT, temp)}")
```

## Los resultados (crudos, sin editar)

`gemma4:12b-mlx`, prompt idéntico, 3 corridas por régimen:

### Temperatura 0 — con seed fija (seed=42)

```
1. The robot whirred to life and began its daily routine.
2. The robot whirred to life and began its daily routine.
3. The robot whirred to life and began its daily routine.
```

**1 de 3 distintas. `done_reason: stop` en las tres.**

### Temperatura 0 — sin seed

```
1. The robot whirred to life and began its daily routine.
2. The robot whirred to life and began its daily routine.
3. The robot whirred to life and began its daily routine.
```

**1 de 3 distintas.**

### Temperatura 1 — sin seed

```
1. The robot whirred to life and blinked its glowing blue sensors.
2. The robot whirred to life and began its daily routine.
3. The robot whirred to life, its sensors scanning the empty room.
```

**3 de 3 distintas.**

## Qué cambió y qué no

| Aspecto | Temperatura 0 | Temperatura 1 |
|---|---|---|
| Salidas distintas | **1/3** | **3/3** |
| Primera palabra | "The" | "The" (no cambió) |
| Sujeto | "The robot" | "The robot" (no cambió) |
| Estructura de la oración | "whirred to life and began its daily routine" | varía el complemento, no el arranque |
| Determinismo | sí (en esta medición) | no |

**Lo que cambió:** el complemento de la oración. Con T=0 siempre "began its daily routine"; con T=1 aparecen "blinked its glowing blue sensors" y "its sensors scanning the empty room".

**Lo que no cambió:** el arranque. Las tres salidas de T=1 empiezan igual ("The robot whirred to life"). Una temperatura alta no reescribe todo: **diversifica donde la distribución es plana**, y en las primeras palabras del prompt hay un patrón muy marcado que el modelo elige igual. La aleatoriedad es local, no global.

## Lo que este experimento corrige del curso

El curso afirma (00:41:02): *"Add temperature equals zero to the API call and you get the same answer every time you run it."*

En esta medición **sí se cumple** (1/3 en ambos regímenes de T=0). Pero hay que saber cuándo **no** se cumple:

1. **Con salidas largas, T=0 no garantiza igualdad.** En el experimento de `m5-prompts.md` (resúmenes de ~30 palabras), el par 1 dio **2/3 distintas a temperatura 0**. La causa probable: T=0 hace *greedy decoding* (siempre el token de mayor probabilidad), pero en hardware con batching, el orden en que se agrupan las operaciones puede cambiar el último dígito de un `float`, y eso basta para romper un empate entre dos tokens casi iguales de probabilidad. Un token distinto arrastra el resto de la oración.
2. **Sin seed, T=0 depende del proveedor.** Algunos proveedores no garantizan reproducibilidad a T=0 sin `seed` explícita. Ollama acá dio 1/3 igual, pero eso es una observación de este runtime, no un contrato.
3. **`seed` fija hace el comportamiento reproducible, no el resultado idéntico a otro proveedor.** Dos proveedores con el mismo `seed` y `temperature` no dan la misma salida: el muestreo depende de la implementación.

> **Regla que sale del laboratorio:** temperatura 0 es *casi* determinístico. Si un test depende de reproducibilidad exacta, fijá `seed` **y** comparalo con tolerancia, o no escribas el test sobre texto generado.

## Un fallo silencioso que vale la pena conocer

La primera corrida devolvió **salidas vacías** en los tres regímenes, todas reportadas como "1/3 distintas". El diagnóstico:

```json
{"response": "", "thinking": "* Input: \"Say hello in one word.\"\n* Constraint:", "done_reason": "length"}
```

El modelo **razona antes de responder**. Con `num_predict=40`, los 40 tokens se gastaron en `thinking` y `response` quedó vacío — con `done: true`. Cualquier script que solo mire `response` habría reportado "el modelo no responde nada" cuando en realidad estaba razonando.

**Dos lecciones que se llevan a producción:**
1. `think: false` va en el **body**, no en `options` (en Ollama). Es fácil de equivocar y el fallo es silencioso.
2. **Chequear `done` no alcanza.** Hay que mirar `done_reason`. `"length"` con `response` vacío significa "se quedó sin presupuesto", no "terminó bien".

## Criterios de corrección

- [x] Programa mínimo funcional, con el mecanismo del curso (SDK/cliente + llamada + imprimir salida).
- [x] Dos corridas (o más) por cada temperatura.
- [x] Qué cambió y qué no, con las salidas crudas.
- [x] Conexión con el fallo real encontrado (salidas vacías por razonamiento).
- [x] Se marca dónde la regla del curso tiene excepciones, en vez de darla por universal.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
