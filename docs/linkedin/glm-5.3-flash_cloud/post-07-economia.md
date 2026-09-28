# Post 7/8 - "La economía de los tokens: lo que nadie te cuenta"

Hablemos de dinero, o mejor dicho, de la métrica que en la práctica ES dinero en sistemas de IA: el contexto.

Antes de la migración multi-agente, mi setup era caro de una forma poco visible. Cada sesión arrastraba decenas de skills en el contexto, aunque el 95% no aplicara a la tarea. Cada pregunta pagaba el peaje completo.

El cambio de arquitectura no me dio solo orden. Me dio una ecuación distinta:

Por agente:
- Contexto base mínimo: solo las skills del dominio.
- Memoria por demanda: RAG en vez de historial completo.
- Sin ruido cruzado: DEV no carga skills de diseño, STUDIO no carga scripts de deploy.

El efecto en la práctica:

1. Menos tokens de entrada por tarea (el bootstrap por agente es una fracción del monolito).
2. Menos retrabajos: menos alucinaciones significa menos iteraciones de corrección, y cada iteración es tokens.
3. Latencia más predecible: el especialista procesa menos material antes de empezar.

El trade-off honesto: la delegación agrega una capa. Cada despacho tiene un costo de comunicación (el prompt de contexto de tarea, el handover de vuelta). En tareas triviales, ese overhead puede hacer que el sistema completo pague más que un agente único.

¿Cuándo conviene entonces? Cuando el trabajo es sostenido y variado: proyectos reales, con muchas sesiones, donde el ahorro por sesión se acumula y la reducción de errores se paga sola. Para un "hazme un script rápido", el monolito gana.

Esa es la lección que me llevo: no existe la arquitectura mejor, existe la arquitectura adecuada a tu escala. La mía dejó de ser adecuada cuando el contexto dejó de entrar.

#IA #LLM #CostOptimization #Engineering #KanamOS