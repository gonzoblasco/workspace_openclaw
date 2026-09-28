¿Cómo puede una IA saber qué decidimos hace tres meses sin que tengamos que recordárselo cada vez?

El problema de la mayoría de las herramientas actuales es que su "memoria" es un historial de chat. Si el historial es muy largo, se pierde; si es corto, se olvida.

En **Kanam OS**, la memoria es una infraestructura de datos, no un texto lineal.

Estamos implementando una arquitectura de **Triple Capa de Memoria**:

1. **Memoria de Corto Plazo:** La sesión actual (lo que estamos haciendo ahora).
2. **Memoria de Largo Plazo:** El corpus de conocimiento (documentación, proyectos, historial).
3. **Memoria de Decisiones (ADRs):** Esta es la joya de la corona.

¿Por qué es tan importante la tercera? Porque la IA suele "alucinar" sobre cómo funcionan las cosas. Al tener una base de datos de **Architectural Decision Records (ADRs)**, el sistema no tiene que "adivinar" si usamos X o Y. Él sabe que *decidimos* X en la fecha Y por la razón Z.

Es la diferencia entre una IA que intenta recordar tus palabras y un sistema que entiende tu historial de decisiones técnicas.

#AI #SoftwareArchitecture #KnowledgeManagement #KanamOS #LLMs