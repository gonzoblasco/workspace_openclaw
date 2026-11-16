# M3 - Entregable: Diagrama app → API → modelo → respuesta

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 3 — Developer Fundamentals & Working with APIs (15:23 – 17:54)
- **Fecha:** 2026-11-12 · actualizado 2026-11-16
- **Consigna:** dibujar el diagrama app → API → modelo → respuesta **y marcar dónde vive cada decisión del agente**.

> Este archivo es el entregable que pide el outline: el diagrama y el dueño de cada decisión. Incluye además el lab de código (el "primer programa de 7 líneas") porque las siete decisiones del diagrama se ven mejor en el código que las implementa.

## El diagrama

```
┌──────────────┐   ┌────────────────────────┐   ┌──────────────┐   ┌───────────────┐
│   USUARIO    │   │        TU APP          │   │     API      │   │    MODELO     │
│  (lenguaje   │   │  (tu código, tu repo)  │   │  (contrato   │   │  (los pesos)  │
│   natural)   │   │                        │   │   HTTP)      │   │               │
└──────┬───────┘   └───────────┬────────────┘   └──────┬───────┘   └───────┬───────┘
       │                       │                       │                   │
       │ 1. intención          │                       │                   │
       ├──────────────────────>│                       │                   │
       │                       │                       │                   │
       │              [A] ¿qué entra al prompt?        │                   │
       │              [B] ¿qué tools se ofrecen?       │                   │
       │              [C] ¿cuánto historial viaja?     │                   │
       │                       │                       │                   │
       │                       │ 2. POST /chat/completions                 │
       │                       ├──────────────────────>│                   │
       │                       │   {model, messages, tools, ...}           │
       │                       │                       │                   │
       │                       │                       │ 3. forward        │
       │                       │                       ├──────────────────>│
       │                       │                       │                   │
       │                       │                       │      [D] predice   │
       │                       │                       │      token a token │
       │                       │                       │                   │
       │                       │ 4. respuesta (JSON o stream)              │
       │                       │<──────────────────────┤<──────────────────┤
       │                       │                       │                   │
       │              [E] ¿tool_call? entonces ejecuto │                   │
       │              [F] ¿finish_reason=stop? corto   │                   │
       │              [G] ¿429/5xx? reintento o aborto │                   │
       │                       │                       │                   │
       │ 5. texto final        │                       │                   │
       │<──────────────────────┤                       │                   │
       │                       │                       │                   │
```

## Dónde vive cada decisión

Esta es la parte que el ejercicio pide y que el dibujo solo no responde. **Siete decisiones, siete dueños.**

| # | Decisión | Dueño | ¿Por qué ahí? |
|---|---|---|---|
| **A** | Qué texto entra al prompt (system prompt, persona, instrucciones) | **Tu app** | El modelo no tiene instrucciones propias; recibe lo que le mandás. Si el system prompt es malo, el fallo es tuyo, no del modelo. |
| **B** | Qué tools se ofrecen y cómo se describen | **Tu app** | El schema de la tool es tu contrato. El modelo *elige* entre las que le diste; no puede inventar una que no esté en el array. |
| **C** | Cuánto historial viaja y, por lo tanto, cuánto cuesta | **Tu app** | Truncation, summarization o sliding window son decisiones de código. El modelo nunca "recuerda": recibe lo que le reenviás. |
| **D** | El siguiente token | **El modelo** | Es lo único que el modelo decide de verdad: la distribución sobre el siguiente token. Todo lo demás es consecuencia. |
| **E** | Si hay `tool_call`, ejecutar la tool y con qué argumentos validados | **Tu app** | El modelo *pide*; tu código *ejecuta*. Nunca al revés: si el modelo pudiera ejecutar, cada alucinación sería un efecto secundario. |
| **F** | Cuándo termina el loop | **Tu app** | `finish_reason` es un dato que el modelo devuelve; cortar (o no cortar) es una línea de tu `while`. Un loop sin tope de iteraciones es un bug de tu código, no del modelo. |
| **G** | Qué hacer ante `429`, `5xx`, timeout | **Tu app** | El modelo ni se enteró. Reintento con backoff, degradación o aborto: todo del lado tuyo. |

## La regla que sale del diagrama

> **El modelo decide una sola cosa: el siguiente token. Todo lo demás es código tuyo.**

Eso reordena el mapa mental: cada flecha del diagrama que *no* es "D" es una decisión que alguien programó. Cuando un agente falla, la pregunta útil no es "¿por qué el modelo se equivocó?" sino "¿cuál de las siete decisiones está mal tomada?".

- Si alucina datos: puede ser **A** (no le diste la fuente) o **E** (no le diste la tool que consulta).
- Si cuesta demasiado: es **C** o **F** (historial hinchado o loop largo).
- Si ejecuta algo peligroso: es **E** (validaste mal los argumentos) o **B** (le diste una tool que no debía tener).
- Si se cuelga: es **G** (no pusiste timeout).

---

# Lab: el primer programa (7 líneas)

El diagrama dice *qué* decide quién; el código muestra *cómo* se manda. Acá las decisiones **A**, **C** y **G** se ven en tres líneas concretas.

```python
from openai import OpenAI
client = OpenAI()

# El "corazón" del programa
response = client.chat.completions.create(
    model="gpt-4o",  # placeholder: ver nota sobre ciclo de vida abajo
    messages=[{"role": "user", "content": "Hola, ¿cómo puedes ayudarme?"}]
)

print(response.choices[0].message.content)
```

> **Aviso de ciclo de vida (2026-11-14):** `gpt-4o` funciona pero es un modelo de 2024. El curso documenta que `gpt-5.1` ya figura como **Deprecated** en la ficha oficial. En producción se usa un identificador vigente (`gpt-5.x`/`gpt-6.x`) leído de variable de entorno (`model=os.environ["MODEL"]`), nunca hardcodeado. Lo que **no** caduca es el mecanismo: `chat.completions` con una lista de `messages`.

### Análisis del código

- **`client.chat.completions.create`**: el endpoint estándar para modelos de chat. Es la flecha 2 del diagrama.
- **`messages`**: lista de diccionarios. Acá vive el **contexto** — y con él, la decisión **C**.
- **`role`**: `system` (instrucciones → decisión **A**), `user` (tus preguntas) o `assistant` (respuestas previas).

## Versión HTTP cruda (sin SDK)

Para ver qué pasa por debajo, esta es la petición `POST` que el SDK envía:

```python
import os
import json
import requests

headers = {
    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
    "Content-Type": "application/json",
}

data = {
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hola, ¿cómo puedes ayudarme?"}],
}

response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=headers,
    json=data,        # json=data fija el Content-Type; NO uses data=json.dumps()
    timeout=30,       # decisión G: sin timeout, la llamada puede colgarse para siempre
)
response.raise_for_status()   # un 429 o un 500 tambien son status 200 si no lo pedis

print(response.json()["choices"][0]["message"]["content"])
```

**Por qué el SDK y no HTTP crudo:** el SDK te da reintentos con backoff, manejo de `429`/`5xx`, streaming tipado, timeouts por defecto y objetos en vez de dicts anidados. La versión cruda de arriba *parece* equivalente, pero cada una de esas tres líneas (`json=`, `timeout=`, `raise_for_status()`) es una cosa que se olvida y rompe en producción — y las tres son la decisión **G**.

## Chat vs. API

| Característica | Chat (Web/App) | API (Developer) |
|---|---|---|
| **Estado** | El sistema recuerda el historial por vos. | Vos debés enviar todo el historial en cada llamada. |
| **Interacción** | Conversacional, lineal. | Funcional, basada en tareas (Request/Response). |
| **Control** | Limitado a las opciones de la interfaz. | Total sobre parámetros (Temperature, Top_P, Max Tokens). |
| **Contexto** | "Caja negra". | Vos decidís qué tokens entran y cuáles salen. |

**Regla de oro para el desarrollo:**
> "No asumas que el modelo recuerda la conversación anterior. Cada llamada a la API es una hoja en blanco **del lado del servidor**: si querés que 'recuerde', vos tenés que reenviarle el historial. La 'memoria' no vive en el modelo, vive en el array `messages` que le pasás."

## Lo que el diagrama NO dice (y conviene tener presente)

- **El "chat" del video es una app más.** Cuando usás la interfaz web de un proveedor, las siete decisiones existen igual: las tomó el proveedor y no las ves. Vos no tenés control sobre A, B ni C. La API devuelve ese control.
- **La API es un contrato, no una conversación.** Cada llamada es independiente. El estado de la "conversación" es una ilusión que construye el array `messages` que reenviás. Ese es el punto central del módulo siguiente.
- **El modelo está afuera de tu proceso.** No hay estado compartido ni sesión: hay request y response sobre HTTP. Por eso el diagrama es request/response y no un canal abierto.

## Criterios de corrección

- [x] El diagrama muestra los cuatro saltos: usuario → app → API → modelo → respuesta.
- [x] Cada decisión tiene dueño explícito (app vs. modelo).
- [x] Distingue lo que el modelo decide (el token) de lo que decide el código (todo el resto).
- [x] Explica por qué la tool la ejecuta la app y no el modelo.
- [x] Conecta cada punto de falla con la decisión concreta que hay detrás.
- [x] El código de 7 líneas es funcional y usa la sintaxis actual del SDK.
- [x] La diferencia entre SDK y HTTP crudo es clara.
- [x] Se explica por qué la API requiere que el historial se envíe manualmente.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
