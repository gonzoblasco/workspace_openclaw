# Art. 1 - Del Monolito a la Orquestación Multi-Agente

> **Fuente:** ADR-073 (Arquitectura Multi-Agente)
> **Audiencia:** LinkedIn semanal - público técnico general
> **Formato:** post listo para pegar (≈ 1.800 caracteres)

---

## Versión LinkedIn (cuerpo del post)

Durante un año mi asistente personal fue un único agente cargado con decenas de skills.

Funcionaba. Hasta que dejó de funcionar.

El problema no fue el modelo. Fue el contexto.

Cada sesión cargaba todas las definiciones de skills, todos los scripts de tooling, todas las plantillas. La ventana de contexto se saturaba, las respuestas empezaban a alucinar instrucciones que no existían y la latencia subía con cada skill nueva.

Decisión (ADR-073): dejar de pensar en "un agente muy capaz" y empezar a pensar en "un equipo chico donde cada uno sabe lo suyo".

La nueva arquitectura es una orquestación multi-agente con cinco roles especializados:

- **Kanam CORE** - orquestación, memoria global, gobierno y estrategia.
- **Kanam DEV** - ingeniería de software, specs, TDD.
- **Kanam OPS** - infraestructura, gateway, seguridad.
- **Kanam MIND** - investigación, análisis, corpus.
- **Kanam STUDIO** - redacción, marca personal, prototipado.

Cada uno corre en su propio directorio, con sus propias skills, y carga solo lo que necesita para su rol. El CORE actúa como punto de entrada único: interpreta la intención, identifica al especialista y delega.

El resultado no fue "más IA". Fue menos IA malgastada. Menos contexto cargado, menos alucinación, menos latencia.

La magia no estuvo en hacer al agente más grande. Estuvo en dejar de pedirle que sepa todo.

---

## Notas técnicas (no publicar)

- **Trigger:** saturación de la ventana de contexto del modelo principal (`deepseek-v4-flash:cloud`).
- **Hipótesis validada:** menos skills cargadas por sesión = menos ruido en el prompt = mejor precisión.
- **Trade-off aceptado:** una capa de latencia de despacho entre CORE y especialista (mitigada por el protocolo definido en ADR-074).
- **Beneficio extra:** agregar un nuevo especialista (ej. `kanam-stories`) no desestabiliza al núcleo.
- **Alineación conceptual:** patrón "Modular Monolith" aplicado a la ventana de contexto de LLMs.
- **Glosario útil:** RAG (Retrieval-Augmented Generation), prompt, alucinación, ventana de contexto.

---

## Hashtags sugeridos

```
#InteligenciaArtificial #AgentesIA #ArquitecturaDeSoftware #LLM #IngenieríaDeSoftware #IA
```

---

## Por qué este post abre la serie

Es el único post conceptual. Define el "antes" (monolito) y el "después" (5 especialistas) sin entrar todavía en el cómo. Los artículos 2, 3 y 4 construyen sobre este piso.
