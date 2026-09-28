# Post 6 - Lo que aprendí construyendo un sistema multi-agente (y qué haría distinto)

Cierre de la serie. Cinco semanas contando cómo construí Kanam OS: la arquitectura, el despacho, los handovers, la memoria compartida, el versionado. Hoy, lo que aprendí de verdad.

**Lección 1: Especializar es más barato que generalizar**

Un solo agente con todas las skills cuesta más en tokens, en precisión y en debugging que cinco agentes con dominios restringidos. La tentación inicial siempre es "un agente más inteligente". La respuesta correcta fue "agentes más chicos, mejor coordinados".

**Lección 2: La coordinación es el producto**

Dividir agentes es fácil. Que no se pisen es lo difícil. El protocolo de despacho y el Context Handover fueron más trabajo que la separación misma de los agentes. Y valieron cada hora invertida: sin protocolo explícito, multi-agente es multi-caos.

**Lección 3: La memoria compartida es el pegamento invisible**

Los agentes pueden tener contextos aislados, pero necesitan una fuente de verdad común. La base de vectores con RAG resolvió el dilema: aislamiento por defecto, conocimiento global bajo demanda.

**Lección 4: Todo versionado o no existe**

Skills, prompts, decisiones, configuraciones. Todo en Git, todo con historia. Los ADRs eliminaron las conversaciones repetidas: lo decidido, decidido está.

**Lo que salió mal (o casi)**

- Intenté cargar demasiada memoria en el bootstrap durante la transición. La respuesta correcta fue menos contexto, no más.
- Al principio el CORE ejecutaba tareas "para ir más rápido". Resultado: se convirtió en un generalista disfrazado. La regla "el CORE nunca ejecuta" tuvo que hacerse explícita.
- Subestimé cuánto iba a costar mantener el mapa de orquestación al agregar o quitar skills. Es deuda de gestión real.

**Qué haría distinto**

Empezaría con menos agentes: dos o tres, no cinco. Dejaría que la complejidad emerja de la necesidad real en vez de diseñarla por adelantado. El CORE y DEV eran inevitables; STUDIO llegó después, cuando había trabajo real para él.

**Por qué lo cuento**

Todo esto corre en mi máquina, en producción real, todos los días. No es un paper ni una demo de conferencia. Es infraestructura de trabajo que usa una persona real para trabajo real.

Si estás construyendo con agentes y te está pasando que "el agente generalista no escala", el camino es este: dividir, protocolar, compartir memoria, versionar todo.

Los ADRs y el código están en mi repo. Si querés charlar sobre arquitectura multi-agente, los comentarios están abiertos.

#AI #MultiAgent #SoftwareArchitecture #LLM #KanamOS #BuildInPublic

---
*Fuente: ADR-073, ADR-074 y aprendizajes operativos del workspace.*
