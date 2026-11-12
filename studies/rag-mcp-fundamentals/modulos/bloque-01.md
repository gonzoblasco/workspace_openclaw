# Bloque 1 — Qué es RAG y cuándo usarlo (módulos 1-7, 00:00 - 09:36)

> Clase de `studies/rag-mcp-fundamentals/`. Fuente primaria: el video. Lo que el ponente afirma como dato se contrastó contra documentación oficial y el estado real del workspace el 2026-11-11; lo verificado va marcado, lo que no, también.

## La idea en una frase

**RAG no es una técnica de recuperación: es una decisión sobre dónde vive el conocimiento.** Lo que sabés hoy vive en los pesos del modelo; con RAG lo sacás de ahí y lo ponés en un índice que actualizás cuando querés. Todo lo demás —embeddings, vector DBs, chunking— es cómo hacés esa mudanza.

Esa frase es la que hay que poder defender. Si entendés eso, el resto de la Parte 1 se ordena sola.

## El ejemplo del ponente, que es más importante de lo que parece

Pregunta: *"¿cuál es la política de reembolso para home office?"* a un LLM sin contexto. El ponente dice que va a alucinar o a dar una respuesta genérica (01:56). Es correcto y el mecanismo importa:

> El LLM **no sabe** que no sabe. No existe un "no tengo esa información" a menos que el prompt lo habilite.

Ese es el problema real. La solución manual —buscar el documento, pegarlo, pedirle que lo use— es RAG con un humano en el medio. RAG automatiza **el humano**, no el modelo.

### Las tres etapas, con sus nombres

| Etapa | Qué hace | Dónde falla |
|---|---|---|
| **Retrieval** | Buscar los fragmentos relevantes | Índice malo, chunking malo, query mal formulada |
| **Augmenting** | Armar el prompt con esos fragmentos | Prompt que ignora el contexto, contexto que no entra, orden mal puesto |
| **Generation** | El LLM responde sobre ese prompt | El modelo inventa igual, o no cita |

**Lo que el curso no dice y a vos te importa:** de las tres, **la que falla más seguido es augmenting**, no retrieval. Todo el mundo mide el score de similitud y nadie mide si el LLM usó el fragmento que le diste. En el workspace esto tiene nombre: `memory_search` devuelve el fragmento correcto y uno igual no puede saber si el agente lo leyó.

## La tabla que hay que memorizar: prompt / fine-tuning / RAG

El ponente la construye con el caso del **policy copilot** (04:12-08:15). Traducida a criterio reutilizable:

| Qué querés cambiar | Herramienta | Costo de actualizar | Cita fuentes |
|---|---|---|---|
| **Comportamiento, límites, seguridad** ("nunca reveles datos de empleados, redirigí a HR") | Prompt engineering | Segundos | No (pero no hace falta) |
| **Voz, estilo, tono, formato** | Fine-tuning | Días + GPU | No |
| **Hechos, políticas, precios, docs** | RAG | Minutos (reindexar) | **Sí** |

### Por qué el fine-tuning no sirve para hechos (los cinco motivos del ponente)

En 07:39-07:55 enumera cinco, y los cinco son correctos:

1. **Las políticas cambian** → reentrenar cada vez.
2. **Entrenar es caro y lento.**
3. **No hay citas** → el usuario no puede verificar de dónde salió.
4. **Más data de entrenamiento no es más precisión** (dato importante y contraintuitivo).
5. **Knowledge cutoff** → el modelo sólo sabe lo que estaba en el training.

Lo que falta en esa lista y es el motivo más fuerte hoy: **el fine-tuning no agrega información de forma confiable, agrega forma.** Un modelo fine-tuneado con 500 pares pregunta-respuesta de políticas va a responder *con el estilo de esas políticas*; si le preguntás algo que no estaba, inventa con más confianza que antes. El fine-tuning **reduce la incertidumbre aparente**, no la real. Por eso la regla del ponente —"great for stable unchanging patterns like communication style, but terrible for dynamic factual information" (07:55)— es exacta.

## Contraste con el workspace: acá ya hay RAG, y es un buen caso de estudio

Esto no lo dice el video, lo verifiqué contra el repo. El workspace ya corre un RAG propio para la memoria:

| Decisión | Qué usa el workspace | Qué enseña el curso | Veredicto |
|---|---|---|---|
| Modelo de embedding | `qwen3-embedding:0.6b` local, **1024 dims** | `all-MiniLM-L6-v2`, 384 dims, 22M params | El del workspace es más grande y más nuevo. El del curso es de 2021 y está en el puesto 13 de la tabla de abajo |
| Vector store | SQLite (`memory/vectors.db`, tablas `section_vectors` y `session_vectors`) | Chroma, luego Pinecone | **SQLite con BLOB es una decisión válida** para 3.300 vectores; Chroma sobra a esa escala |
| Similitud | `cosine_similarity` escrito a mano en Python | `np.dot` | El workspace hace lo correcto: **normaliza**. Sin normalizar, el dot product premia vectores largos, no similares |
| Chunking | 1.500 caracteres, hasta 3 chunks por sesión | 200-500 chars, overlap 50-100 | El workspace chunk-ea **mucho más grande** que lo que recomienda el curso. Ver el bloque 5 para discutirlo |

**Verificado hoy:** un vector en `session_vectors` mide **4.096 bytes = 1.024 floats de 32 bits, con norma 1.0** (ya normalizado al guardar). Eso confirma las 1024 dimensiones y que la similitud por dot product es equivalente a coseno. El chunk de ese registro tiene 1.009 caracteres.

**La lección de método:** cuando alguien dice "usá Chroma", la pregunta es *¿a qué escala?*. Con 3.317 vectores, un `SELECT` sobre SQLite y un dot product en Python tardan lo que un `ls`. La complejidad de una vector DB se paga a partir de decenas o cientos de miles de vectores, no antes. El curso no lo aclara porque su ejemplo son 500 documentos, que tampoco lo justifican.

## Lo que el curso da por sentado y no es gratis

- **"No background knowledge required"** (00:42): cierto para seguir el video, falso para implementarlo. El lab 1 asume que sabés crear un venv, instalar paquetes y leer un script.
- **El LLM que usa el ejemplo es ChatGPT.** En la práctica el 80% de los RAG internos terminan con un modelo propio o local, y ahí las decisiones de contexto y de temperatura cambian.
- **No menciona evaluación.** No hay una sola mención a medir si la respuesta recuperada era la correcta. Sin eso, RAG es una caja negra que a veces acierta. Es el hueco más grande de la Parte 1 y lo cubro en el bloque 6.

## Ejercicio del bloque

No es el del outline (ese es de reconocimiento). Este es el que vale:

**Escribí `mi-sistema.md` con cuatro bloques, en 10 líneas:**

1. **El documento privado.** Qué corpus tenés que un LLM no vio (docs internos, tu memoria, tus clases, un manual).
2. **La pregunta real.** Una pregunta concreta que hoy responderías a mano, con la respuesta correcta escrita al lado.
3. **La herramienta.** ¿La pregunta pide *forma* (estilo, formato, tono) o *hechos*? Si es forma → fine-tuning / prompt. Si es hechos → RAG. **Si no lo tenés claro, no es un caso de RAG todavía.**
4. **El costo de equivocarse.** Si el sistema responde mal, ¿quién lo nota y cuándo? Un RAG de políticas internas que falla callado es peor que no tener RAG.

Pasámelo y lo usamos como hilo conductor: los bloques 5 (chunking) y 6 (producción) los vas a leer contra *tu* corpus, no en abstracto.

## Banco de preguntas (respondelas antes de seguir)

1. ¿Por qué un LLM no puede decir "no sé" sin que el prompt lo habilite, y qué implica eso para el diseño del prompt de augmenting?
2. El ponente dice que el fine-tuning es "terrible for dynamic factual information". ¿Qué pasa exactamente si igual lo hacés con hechos que cambian todos los meses?
3. De las tres etapas de RAG, ¿cuál falla más seguido en producción y por qué no es la que todos miden?
4. El workspace usa SQLite en vez de Chroma. ¿En qué condición ese archivo se vuelve un problema?

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
