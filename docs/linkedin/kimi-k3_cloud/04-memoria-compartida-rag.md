# Post 4 - Memoria compartida: cinco agentes, un solo inconsciente colectivo

Tengo cinco agentes especializados trabajando en paralelo. Cada uno ve solo una parte del sistema. Y sin embargo, ninguno está desconectado del todo.

La pieza que los une: una memoria compartida que funciona como inconsciente colectivo.

**El dilema del contexto aislado**

Cuando dividís un agente generalista en especialistas, ganás precisión pero arriesgás algo: que cada agente se vuelva un silo. Que DEV no sepa lo que OPS hizo ayer. Que MIND investigue algo que STUDIO ya documentó la semana pasada.

La solución ingenua sería pasar el contexto completo entre agentes. Eso nos devuelve al problema original: saturar la ventana de contexto de cada uno con información que no necesita.

**La solución: RAG sobre una fuente de verdad compartida**

En Kanam OS, la memoria vive en una base de datos de vectores (`memory.db`) que es la fuente de verdad compartida para todos los agentes.

El funcionamiento:

- Cada agente arranca su sesión con contexto aislado: solo las skills y scripts de su dominio. Bootstrap liviano, sin ruido.
- Cuando un agente necesita memoria, la busca vía RAG: recupera solo los fragmentos relevantes para su tarea actual.
- Nunca recibe un volcado masivo de contexto. Recibe respuestas puntuales a preguntas puntuales.

**El contraste con el modelo anterior**

El agente generalista cargaba toda la memoria "por las dudas". Los especialistas cargan ninguna memoria "hasta que la necesitan".

El resultado:

- Tokens de bootstrap reducidos drásticamente.
- Precisión mayor: cada agente opera en su dominio, pero con acceso puntual al conocimiento global.
- Cero re-descubrimiento: si algo se decidió hace dos meses y está en la memoria, cualquier agente lo encuentra.

**Por qué importa la decisión de diseño**

La tentación al construir sistemas multi-agente es compartir todo entre todos. "Por si acaso lo necesitan". Eso mata la especialización: terminas con cinco agentes saturados en vez de uno.

La regla que aplicamos: contexto aislado por defecto, memoria global bajo demanda.

Es la misma lógica de cualquier sistema distribuido bien diseñado: cada nodo es independiente, pero todos comparten el mismo estado de verdad. La diferencia es que acá los nodos son LLMs y el estado de verdad es una base de vectores.

**Lo que falta contar**

Tenemos agentes especializados, un protocolo de despacho, handovers estructurados y memoria compartida. ¿Cómo versionamos todo esto sin caos?

La próxima semana: Git como sistema nervioso de Kanam OS.

#AI #MultiAgent #SoftwareArchitecture #LLM #KanamOS #RAG

---
*Fuente: ADR-073 (Arquitectura Multi-Agente, sección Gestión de Memoria y Contexto).*
