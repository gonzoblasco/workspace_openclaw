# M3 - Práctica: El primer programa (7 líneas)

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 3 — Developer Fundamentals & Working with APIs (15:23 - 17:54)
- **Fecha:** 2026-11-12
- **Consigna:** Pasar del chat a la API. Entender que un LLM en producción no es una conversación, es una petición de completar texto basada en un contexto de roles.

## El diagrama del flujo de una aplicación

Cuando usas una App (como esta), el flujo de datos es:

`Usuario` $\leftrightarrow$ `App (Frontend/Backend)` $\leftrightarrow$ `API (Gateway)` $\leftrightarrow$ `Modelo (LLM)`

A diferencia del chat, aquí la App es la responsable de:
1. **Context Window Management:** Decidir qué partes del historial enviar.
2. **Prompt Engineering:** Inyectar instrucciones de sistema (System Prompts).
3. **Cost Control:** Limitar la cantidad de tokens generados.

---

## El primer programa (7 líneas)

Esta es la forma más limpia de llamar a un modelo usando el SDK oficial de OpenAI en Python.

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

### Análisis del código:
- **`client.chat.completions.create`**: Es el endpoint estándar para modelos de chat.
- **`messages`**: Es una lista de diccionarios. Aquí es donde se define el **Contexto**.
- **`role`**: Puede ser `system` (instrucciones), `user` (tus preguntas) o `assistant` (respuestas previas).

---

## Versión HTTP Cruda (Sin SDK)

Para entender qué pasa por debajo, esta es la petición `POST` que el SDK envía automáticamente:

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
    timeout=30,       # sin timeout, la llamada puede colgarse para siempre
)
response.raise_for_status()   # un 429 o un 500 tambien son status 200 si no lo pedis

print(response.json()["choices"][0]["message"]["content"])
```

**Por qué el SDK y no HTTP crudo:** el SDK te da reintentos con backoff, manejo de `429`/`5xx`, streaming tipado, timeouts por defecto y objetos en vez de dicts anidados. La versión cruda de arriba *parece* equivalente, pero cada una de esas tres líneas (`json=`, `timeout=`, `raise_for_status()`) es una cosa que se olvida y rompe en producción.

---

## Notas del Lab: Chat vs. API

| Característica | Chat (Web/App) | API (Developer) |
|---|---|---|
| **Estado** | El sistema recuerda el historial por vos. | Vos debés enviar todo el historial en cada llamada. |
| **Interacción** | Conversacional, lineal. | Funcional, basada en tareas (Request/Response). |
| **Control** | Limitado a las opciones de la interfaz. | Total sobre parámetros (Temperature, Top_P, Max Tokens). |
| **Contexto** | "Caja negra". | Vos decidís qué tokens entran y cuáles salen. |

**Regla de oro para el desarrollo:**
> "No asumas que el modelo recuerda la conversación anterior. Cada llamada a la API es una hoja en blanco **del lado del servidor**: si querés que 'recuerde', vos tenés que reenviarle el historial. La 'memoria' no vive en el modelo, vive en el array `messages` que le pasás."

---

## Criterios de corrección

- [ ] El código de 7 líneas es funcional y usa la sintaxis actual del SDK.
- [ ] La diferencia entre el SDK y el HTTP Crudo es clara.
- [ ] Se explica por qué la API requiere que el historial sea enviado manualmente.
- [ ] El diagrama de flujo identifica a la Aplicación como el "intermediario" necesario.
