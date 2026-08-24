# Video 5 - Step-by-Step Agentic Flow: Case Study

**Curso:** Inside Agentic AI: Foundations and Frontiers
**Track:** 1
**Fecha:** 2026-08-21

---

## Tesis

Caso real de chatbot de soporte autónomo que resuelve un issue **sin intervención humana**, mostrando el loop completo en acción.

## Escenario

- Input: "My Internet is down. Can't connect to anything." - sin rep de soporte humano, solo agente autónomo.
- **Goal del agente:** resolver issues de soporte comunes sin human handoff.
- **Equipado con:** knowledge base del producto + historial del cliente + backend APIs de diagnóstico.

## Los 4 pasos del flujo

### 1. Perception + intent
- Lee el mensaje, detecta intención = *Connectivity issue*.
- **Parsea señales de urgencia/frustración** (tono, puntuación).
- Extrae metadata de dispositivo / hora del día si está disponible.
- La comprensión fija el curso de acción.

### 2. Memory
- Chequea historial de soporte del cliente: fallo de modem la semana pasada, outages intermitentes, chat previo con "velocidades".
- **La memoria permite spotear patrones** y profundizar el entendimiento del issue actual.

### 3. Tool use + action execution
- Corre diagnóstico backend (API interna): estado del modem, señal, actividad de nodo.
- Encuentra el issue → **actúa**: resetea modem remotamente o prepara ticket de reemplazo.

### 4. Feedback loop + adaptation
- Pregunta "¿Te anda conectado?" y monitorea la respuesta.
- Según la respuesta **adapta**: prueba otro fix, hace seguimiento, o **escala a un humano** si el caso cae fuera de patrones esperados.
- Resultado: resuelto en <2 min, sin intervención humana.

## El flujo completo (resumen del loop)

1. **Input** (mensaje de usuario o señal de sistema)
2. **Perception** - interpreta significado y contexto
3. **Memory** - recuerda interacciones pasadas, datos
4. **Decision making** - pesa opciones según goal y contexto
5. **Tool action** - ejecuta función, llama API, recupera contenido
6. **Feedback loop** - evalúa si la acción logró el goal
7. **Adapt OR Escalate** - refina el enfoque o escala a proceso/humano
8. **Loop completo** - el flujo dinámico es lo que hace inteligente y en mejora al sistema

## Frases para el quiz

- "The agentic becomes better over time, learning from new patterns and feedback."
- "This dynamic flow is what enables agentic systems to behave intelligently and improve over time."
- "El escalate es parte del loop, no un fallo del sistema."

---

## Conexión con mi experiencia

El paso **adapt OR escalate** es el más relevante para el pipeline:
- El agente tiene un goal claro pero **escala cuando el caso cae fuera de patrones esperados** - no escala nunca ni siempre.
- **Memory para detectar patrones** (no solo responder): el modem fallido la semana pasada da profundidad al issue actual.
- **Feedback de verificación** ("¿anda ahora?") antes de cerrar - conecta con el video 3: "skipping verification leads to failure".

**Mi orquestador = el "escalar" del pipeline.** Cuando el Agente B produce un bug o el cross se sale de lo esperado, el humano-en-el-loop decide si el agente sigue solo o si escala. El video valida que **el escalate es diseño correcto**, no un defecto.
