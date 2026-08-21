# Video 2 - What Makes AI Agentic?

**Curso:** Inside Agentic AI: Foundations and Frontiers
**Track:** 1
**Fecha:** 2026-08-21

---

## Tesis

"Traditional AI predicts. Agentic AI perceives, decides, and acts - not just when prompted, but proactively."

## Tabla comparativa (clave para el quiz)

| Dimensión | Traditional AI | Agentic AI |
|---|---|---|
| **Behavior** | **Reactive** - espera input, da respuesta | **Goal-directed** - trabaja hacia un propósito, elige cómo actuar |
| **Decision-making** | **Ninguna** - no pesa alternativas | **Autónomo** - elige entre acciones, ajusta su camino |
| **Tool use** | **No usa tools** - solo computación interna | **Usa tools y APIs** - interactúa con sistemas externos |
| **Memory** | **Stateless** - cada request independiente | **Corto/largo plazo** - recuerda y aprende, continuidad |
| **Learning post-deploy** | **Congelado** - no mejora solo, necesita retrain humano | **Adapta** - aprende y se ajusta |

## Puntos clave

1. **Loan approval (2020 vs 2025):** modelo entrenado en 2020 sigue decidiendo con patrones de ese año aunque la economía cambie. "Locked into its original logic." Tradicional no aprende en producción; agentic sí.

2. **El gato:** un modelo de visión busca patrones fijos (orejas, bigotes, pelaje). Si le mostrás un *sketch* o un *almohadón con forma de gato*, no razona que "podría ser un gato en forma nueva". Reacciona a pixels, no a conceptos.

3. **Proactividad (diferenciador):** agente de viajes que, al cancelarse el vuelo, no espera input - escanea itinerario, chequea alternativas y te reubica solo, antes de que notes el problema. "Follows goals, not just inputs."

4. **Real-time flexibility:** si el hotel elegido se llena, no falla - busca alternativas, chequea ratings/proximidad, actualiza el plan, sigue cumpliendo el goal.

5. **Analogía cierre:**
   - Tradicional = **especialista que responde preguntas** (preciso, rápido, limitado al scope).
   - Agentic = **asistente que gestiona tareas** (le decís qué lograr, él descifra cómo, delega, consulta, se ajusta).

6. **Contrapeso - riesgos:** autonomía para actuar independiente introduce desafíos. Un mal juicio, input sesgado o mal uso de un tool puede tener consecuencias serias. De ahí el énfasis en *accountability*.

---

## Definición para el quiz

> "Agentic AI es IA que puede operar con autonomía, perseguir objetivos, tomar decisiones basadas en su entorno, y adaptarse con el tiempo - percibiendo, decidiendo y actuando proactivamente en lugar de solo reaccionar a los inputs."

---

## Conexión con mi experiencia

Mi stack cumple las 5 dimensiones de lo agentic: goal-directed (pipeline), tools (Ollama, git, browser, exec), memoria (daily notes, MEMORY.md, handoffs), adaptación (MEMORY.md se actualiza con lecciones). La diferencia con un agente de libro: la verificación final y el escalar los hago como humano-en-el-loop - que es justamente el diseño responsable que el video pide al final.
