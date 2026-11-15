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
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hola, ¿cómo puedes ayudarme?"}]
)

print(response.choices[0].message.content)
```

### Análisis del código:
- **`client.chat.completions.create`**: Es el endpoint estándar para modelos de chat.
- **`messages`**: Es una lista de diccionarios. Aquí es donde se define el **Contexto**.
- **`role`**: Puede ser `system` (instrucciones), `user` (tus preguntas) o `assistant` (respuestas previas).

---

## Versión HTTP Cruda (Sin SDK)

Para entender qué pasa por debajo, esta es la petición `POST` que el SDK envía automáticamente:

```python
import requests
import json

headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hola, ¿cómo puedes ayudarme?"}]
}

response = requests.post("https://api.openai.com/v1/chat/completions", 
                         headers=headers, 
                         data=json.dumps(data))

print(response.json()['choices'][0]['message']['content'])
```

---

## Notas del Lab: Chat vs. API

| Característica | Chat (Web/App) | API (Developer) |
|---|---|---|
| **Estado** | El sistema recuerda el historial por vos. | Vos debés enviar todo el historial en cada llamada. |
| **Interacción** | Conversacional, lineal. | Funcional, basada en tareas (Request/Response). |
| **Control** | Limitado a las opciones de la interfaz. | Total sobre parámetros (Temperature, Top_P, Max Tokens). |
| **Contexto** | "Caja negra". | Vos decidís qué tokens entran y cuáles salen. |

**Regla de oro para el desarrollo:**
> "No asumas que el modelo recuerda la conversación anterior. Cada llamada a la API es una hoja en blanco. Si querés que 'recuerde', tenés que enviarle el historial de nuevo."

---

## Criterios de corrección

- [ ] El código de 7 líneas es funcional y usa la sintaxis actual del SDK.
- [ ] La diferencia entre el SDK y el HTTP Crudo es clara.
- [ ] Se explica por qué la API requiere que el historial sea enviado manualmente.
- [ ] El diagrama de flujo identifica a la Aplicación como el "intermediario" necesario.
