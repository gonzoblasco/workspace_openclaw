# Video 4 - Inside the Agentic Loop

**Curso:** Inside Agentic AI: Foundations and Frontiers
**Track:** 1
**Fecha:** 2026-08-21

---

## Tesis

"Un agente no solo responde: junta información, decide, actúa, reflexiona, y lo hace de nuevo, más inteligente cada vez."

## El loop (ciclo central del curso)

```
Perception -> Reasoning -> Action
        ^
                              + Feedback + Memory (dan forma a pasos futuros)
```

Los agentes no se detienen tras actuar. El feedback y la memoria retroalimentan el ciclo, permitiendo mejorar en cada vuelta. "The loop repeats to achieve evolving goals, adjusting course along the way."

## Componentes del loop

### 1. Perception (entrada)
- Lee mensajes, datos o input de sensores. La puerta de entrada - "cómo ve el mundo".
- **No es solo absorber, es interpretar**: qué pide el usuario, cuál es el estado actual.
- Esa comprensión dispara el razonamiento.

### 2. Reasoning (pensar y planear)
- Interpreta objetivos y contexto (¿qué intento lograr?).
- Selecciona tools o pasos del plan (calculadora, DB, email).
- **Evalúa posibles outcomes**: "si hago esto, ¿me acerco al objetivo?" - acá emergen la inteligencia y la estrategia.

### 3. Action (ejecutar)
- Ejecuta el plan: tool calls, APIs, scripts, Slack.
- El resultado puede ser **visible** (reservar) u **oculto** (modificar estado interno: intenciones, motivaciones, focus areas).

### 4. Feedback (aprender del resultado)
- Recibe resultado o confirmación (¿envió el email? ¿la API devolvió datos válidos?).
- Detecta errores, sorpresas o mismatches; si algo inesperado pasa, lo reconoce y ajusta.
- Actualiza próximos pasos o estrategia de goal. El feedback loops back al razonamiento/planning, volviendo al agente más resiliente.

### 5. Memory (acumular experiencia)
- Guarda acciones, resultados, interacciones - **a través de sesiones**, no solo temporal.
- Habilita contexto y aprendizaje a largo plazo (preferencias de usuario, qué tools funcionaron).
- Impulsa mejora continua: cada ciclo vuelve al agente más eficiente, preciso y alineado.

## Ejemplo: Travel Planner

- Input: "planeá un viaje de 3 días a Tokio por < 80,000 rupias."
- Lee input, trae datos de vuelos, chequea precios de hoteles, redacta itinerario, reserva tickets.
- Con el tiempo aprende preferencias: sugiere comida vegetariana, vuelos nocturnos, hoteles boutique según lo que le gustó antes.

## Frases para el quiz

- "What makes agents powerful is not just that they can think, but that they can **keep thinking**."
- "Feedback and memory make agents adaptive. These systems don't just react, they **evolve**."
- "Perception, planning, action, feedback, and memory" = el loop que da inteligencia real.

---

## Conexión con mi experiencia

El loop describe literalmente el pipeline Qwen:
- **Perception** - leer el transcript/contexto o la spec.
- **Reasoning** - Kanam redacta la tarea, el agente elige cómo.
- **Action** - Ollama, git, exec.
- **Feedback** - cross-review A→B + verificación contra la fuente.
- **Memory** - MEMORY.md, daily notes, handoffs - a través de sesiones.

Clave que el curso subraya y valido en práctica: "these systems don't just react, they evolve." Las lecciones (SIGKILL, cross-review, Agente B) se registran en memoria y cambian el comportamiento de sesiones futuras. El agentic loop en mi cuerpo.
