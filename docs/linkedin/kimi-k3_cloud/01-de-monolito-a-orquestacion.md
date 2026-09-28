# Post 1 - De un agente que hace todo a cinco cerebros que se especializan

Hace un tiempo construí lo que muchos construimos con LLMs: un agente generalista. Un solo agente, con todas las herramientas, todas las skills, toda la memoria cargada en cada sesión.

Funcionaba. Hasta que dejó de funcionar.

**El problema: la ventana de contexto no es infinita**

Cada sesión arrancaba cargando decenas de definiciones de skills y scripts. Ese bootstrap pesado tenía tres efectos reales:

- Ruido operativo: el modelo recibía instrucciones de cosas que no iba a hacer nunca en esa sesión.
- Más alucinaciones: a mayor saturación de contexto, peor precisión.
- Costo y latencia en crecimiento: tokens quemados antes de la primera tarea real.

**La decisión: orquestación multi-agente**

Migramos de un agente generalista a un sistema de cinco roles especializados, con workspaces aislados:

- **Kanam CORE** - orquestación, memoria global, estrategia. Es el único punto de entrada.
- **Kanam DEV** - ingeniería de software, specs, TDD.
- **Kanam OPS** - infraestructura, seguridad, tooling.
- **Kanam MIND** - conocimiento, research, aprendizaje.
- **Kanam STUDIO** - comunicación, redacción, marca personal.

**El detalle que lo cambia todo: el CORE no ejecuta, despacha**

El agente orquestador hace cuatro cosas, en este orden:

1. Interpreta la intención.
2. Identifica qué especialista tiene la skill necesaria.
3. Delega la tarea con un contexto mínimo y específico.
4. Recibe el resultado y sintetiza la respuesta final.

Cada especialista carga solo las skills de su dominio. La memoria compartida vive en una base de vectores común: cada agente recupera por RAG solo los fragmentos que necesita, sin pasar contextos masivos entre sesiones.

**Lo que ganamos**

- Menos tokens de bootstrap por sesión.
- Mayor precisión: cada modelo opera en un dominio restringido.
- Escalabilidad: sumar un sexto especialista no toca al núcleo.
- Todo versionado en Git: cada agente tiene su workspace trackeado.

**Lo que pagamos**

- Latencia de despacho: hay un salto extra entre el CORE y el especialista.
- Mantener el mapa de orquestación: cada skill nueva o eliminada impacta en el sistema.

¿Valió la pena? Absolutamente. Pero la parte más difícil no fue dividir los agentes: fue definir cómo se coordinan sin pisarse.

La próxima semana cuento el protocolo de coordinación: cómo se pasan contexto entre agentes sin que ninguno tenga que "re-descubrir" lo que otro ya hizo.

#AI #MultiAgent #SoftwareArchitecture #LLM #KanamOS

---
*Fuente: ADR-073 (Arquitectura Multi-Agente) y ADR-074 (Protocolo de Despacho).*
