¿Cómo coordinas un equipo de especialistas cuando el "jefe" es una IA?

El gran desafío de la IA multi-agente no es solo que el modelo sepa hacer la tarea; es cómo se pasan la posta sin perder el hilo de la conversación.

En **Kanam OS**, la clave es el **Protocolo de Despacho (ADR-074)**.

Imaginen una empresa donde el Director de Operaciones (Kanam CORE) recibe un pedido. Él no hace el trabajo técnico; él identifica quién es el experto adecuado y le asigna la misión.

Así es como funciona nuestra arquitectura:

1. **Interpretación:** El CORE entiende la intención del usuario.
2. **Selección:** Identifica qué agente especialista posee la Skill necesaria (por ejemplo, Kanam DEV para código o Kanam OPS para infraestructura).
3. **Delegación:** El CORE invoca al especialista con un "Contexto de Tarea" específico.
4. **Sínteis:** El especialista ejecuta, devuelve el resultado y el CORE lo presenta de forma coherente al usuario.

Esto permite que cada agente se mantenga en su "zona de genialidad", evitando que el sistema se sature con información innecesaria. Es eficiencia pura aplicada a la inteligencia artificial.

#AI #AgenticWorkflows #KanamOS #SoftwareArchitecture #MultiAgentSystems