# Post 5 - Git como sistema nervioso: cómo versionamos cinco agentes sin caos

Versionar código es problema resuelto. Versionar cinco agentes de IA que se llaman entre sí, cada uno con sus propias skills, scripts y configuraciones, es otra cosa.

En Kanam OS lo resolvimos con una decisión simple: cada agente es un workspace independiente, y todo queda trackeado por Git.

**La estructura**

Los cinco agentes viven en rutas separadas dentro del workspace:

- El CORE vive en la raíz: es el punto de entrada y donde reside la gobernanza.
- Los especialistas viven en `/workspace/agents/`: `kanam-dev`, `kanam-ops`, `kanam-mind`, `kanam-studio`.

Cada uno de esos directorios contiene las skills, scripts y prompts específicos de ese rol. Todo eso entra a Git. Si mañana alguien (o yo mismo) quiere auditar qué skill tenía DEV hace un mes, `git log` se lo cuenta.

**Por qué esto es más importante de lo que parece**

Los sistemas multi-agente suelen tener un punto ciego: las definiciones de los agentes viven en configuraciones ocultas, paneles web o prompts que nadie versiona. Cuando algo se rompe, no hay historia.

Nosotros aplicamos una regla de software tradicional a infraestructura de IA: si no está versionado, no existe.

Eso habilita tres cosas:

- **Auditoría**: cada cambio en una skill queda registrado con autor, fecha y motivo.
- **Rollback**: si una skill nueva rompe el comportamiento de un agente, volvemos a la versión anterior en minutos.
- **Evolución visible**: el sistema entero es legible como código. No hay magia oculta.

**Las decisiones viven en ADRs**

Los cambios arquitectónicos grandes no son solo commits: son Architecture Decision Records. Cada ADR documenta contexto, decisión y consecuencias.

Esta serie de posts, de hecho, está basada en dos ADRs reales: el 073 (por qué pasamos a multi-agente) y el 074 (cómo se coordinan).

La regla: lo que está definido en un ADR está resuelto. No se vuelve a discutir salvo que aparezca evidencia técnica nueva. Eso elimina una fuente enorme de ruido: las conversaciones que se repiten cada dos meses.

**Lo que esto habilita**

Con agentes versionados y decisiones documentadas, el sistema se vuelve legible para cualquiera que entre nuevo. Incluyendo un "yo futuro" que no se acuerda por qué tomó una decisión.

El conocimiento no vive en mi cabeza ni en chats perdidos. Vive en el repo.

**Cierre de la serie**

Ya contamos la arquitectura, el despacho, los handovers, la memoria y el versionado. La próxima semana, el post final: las lecciones de verdad, lo que salió mal y qué haría distinto.

#AI #MultiAgent #SoftwareArchitecture #LLM #KanamOS #GitOps

---
*Fuente: ADR-073 (Consecuencias: Versionado) y práctica documentada del workspace.*
