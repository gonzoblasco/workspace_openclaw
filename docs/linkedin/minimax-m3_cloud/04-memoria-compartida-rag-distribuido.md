# Art. 4 - La Memoria Compartida que Une a los Agentes

> **Fuente:** ADR-073 (Arquitectura Multi-Agente, sección "Inconsciente Colectivo") + ADR-074 (Context Handover)
> **Audiencia:** LinkedIn semanal - público técnico general
> **Formato:** post listo para pegar (≈ 2.300 caracteres)

---

## Versión LinkedIn (cuerpo del post)

Cinco cerebros separados suena a desastre de coordinación. Si DEV no sabe qué hizo MIND, ni qué decidió CORE, la coherencia se rompe en dos sesiones.

La pieza que lo sostiene es una sola: una base de datos SQLite local (`memory.db`) que todos comparten como fuente de verdad.

No hay cinco memorias. Hay una, con embeddings.

El CORE escribe cuando hay decisiones. DEV escribe cuando termina código. MIND escribe cuando consolida una investigación. OPS escribe cuando cambia una configuración. Y cuando un agente arranca y necesita contexto, hace una búsqueda semántica (RAG) sobre esa base y levanta solo los fragmentos relevantes para su tarea actual.

Ese es el truco: cada sesión carga poco en su prompt, pero accede a todo el historial cuando lo necesita vía búsqueda vectorial.

Los cuatro campos del "Context Handover" del artículo anterior encajan exactamente acá. Summary, Status, Next Steps y Resources son la unidad mínima que cada agente escribe al terminar su tarea, para que el siguiente pueda continuar sin re-descubrir.

La consecuencia operativa:

- Sesiones más cortas en tokens.
- Memoria persistente entre sesiones (aunque cada sesión arranca sin memoria in-process).
- Trazabilidad real: cuando alguien me pregunta "¿cuándo decidiste X?", está en la base, fechada, con la ADR que la justificó.

El sistema no escala porque le metimos más contexto al modelo. Escala porque le sacamos contexto inútil y le dejamos pedir solo lo que necesita, cuando lo necesita.

Eso es lo que yo llamo el "inconsciente colectivo" de Kanam OS: no es lo que el agente sabe en este momento. Es lo que el equipo ya sabe y puede recuperar.

---

## Notas técnicas (no publicar)

- **Diseño técnico (resumen honesto, sin exponer números internos críticos):**
  - Una base SQLite única (`memory.db`) accesible para los cinco agentes.
  - Embeddings almacenados como `BLOB float32` (ADR-057) para no pagar costo de serialización en cada query.
  - Búsqueda semántica (RAG) por agente, no global: cada rol hace queries con scope propio para minimizar tokens recuperados.
- **Trade-off intencional:** latencia de búsqueda semántica por turno. Aceptada a cambio de sesiones con prompts limpios.
- **Lo que NO va al post público:** nombres exactos de columnas, dimensiones del embedding, rutas al `.db`, scripts de mantenimiento. Eso es superficie interna.
- **Concepto de "inconsciente colectivo":** tomado del texto del ADR-073, reinterpretado para audiencia general. La metáfora funciona porque los humanos ya la entienden del psicoanálisis jungiano.
- **Reflexión editorial:** este artículo cierra la serie. Si la idea queda clara, el lector ya entiende por qué la serie vale la pena: cinco cerebros chicos coordinados por una memoria compartida valen más que un cerebro gigante que intenta saber todo.

---

## Hashtags sugeridos

```
#RAG #SQLite #ArquitecturaDeSoftware #LLM #MultiAgente #IngenieríaDeSoftware
```

---

## Por qué este post cierra la serie

El art. 1 fue el problema. El art. 2 el cómo se coordinan. El art. 3 el quiénes. Este art. 4 es el con qué conocimiento. Una vez publicado, la serie tiene una simetría: problema → mecanismo → actores → memoria.

Después de este post, si publicás más, ya estás en territorio de "profundización técnica" (pipeline A/B, scoring de complejidad, embeddings, ADR específicos). Ese es material para una segunda serie, no esta.

---

## Recomendación editorial

Releer la serie entera en orden antes de publicar. Que el artículo 1 funcione como pitch del 2, el 2 del 3, y el 3 de este. Si algún post puede leerse solo, mejor - pero la fuerza está en leerlos seguidos.
