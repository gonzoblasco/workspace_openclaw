# Post 3 - El Context Handover: cómo se pasan la posta los agentes sin perder información

Cuando un agente de Kanam OS termina una tarea, no dice "listo" y se va. Entrega un paquete.

Ese paquete se llama Context Handover, y es probablemente la pieza más importante de todo el sistema multi-agente.

**El problema que resuelve**

En un sistema con varios agentes especializados, el riesgo no es que un agente falle. El riesgo es que el siguiente agente tenga que re-descubrir todo lo que el anterior ya hizo.

Imaginen este flujo real:

- DEV refactoriza un módulo y lo deja listo para producción.
- OPS tiene que deployarlo, pero no sabe qué archivos cambiaron ni por qué.
- MIND tiene que actualizar la memoria del proyecto, pero no sabe qué decisión técnica se tomó.

Sin handover, cada agente empieza de cero. Con handover, cada uno arranca con el mapa completo.

**La estructura del paquete**

Cada finalización de tarea incluye un bloque de Estado de Contexto con cuatro campos:

- **Summary**: qué se logró, en una línea.
- **Status**: estado actual del activo (Draft, Ready, Merged).
- **Next Steps**: qué falta para completar la tarea.
- **Resources**: rutas a archivos creados o modificados.

Cuatro campos. Nada más. Suficiente para que cualquier agente (o humano) retome sin fricción.

**Cuando una tarea necesita más de un especialista**

El protocolo de coordinación para tareas multi-agente tiene cuatro pasos:

1. El CORE identifica la **tarea primaria**.
2. Selecciona al **especialista principal**.
3. Ese especialista identifica si necesita apoyo de otro (ejemplo: DEV pide a OPS que deploye lo que terminó).
4. El CORE coordina la intervención del segundo agente.

El punto clave: no es el CORE el que decide todo el flujo de antemano. El especialista principal, que es quien mejor entiende su tarea, es quien pide el apoyo cuando lo necesita.

**Lo que esto cambia en la práctica**

Antes del handover estructurado, coordinar dos agentes era como un juego de teléfono: cada uno interpretaba lo que creía que el otro había hecho.

Ahora es una cadena de producción: cada eslabón entrega un paquete completo, verificable, al siguiente.

**Lo que sigue**

Ya vimos cómo se dividen los agentes, cómo el CORE despacha y cómo se pasan contexto. Pero hay una pregunta pendiente: ¿dónde vive la memoria de todo esto?

La próxima semana: memoria compartida y RAG. El inconsciente colectivo de Kanam OS.

#AI #MultiAgent #SoftwareArchitecture #LLM #KanamOS

---
*Fuente: ADR-074 (Protocolo de Despacho y Coordinación Multi-Agente).*
