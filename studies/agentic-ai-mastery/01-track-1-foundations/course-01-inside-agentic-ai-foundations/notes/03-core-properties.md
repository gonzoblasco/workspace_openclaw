# Video 3 - Core Properties of Agentic AI Systems

**Curso:** Inside Agentic AI: Foundations and Frontiers
**Track:** 1
**Fecha:** 2026-08-21

---

## Tesis

"Traditional AI predicts. Agentic AI perceives, plans, and acts."

## Las 8 propiedades núcleo

Se leen como un ciclo: el agente **percibe** → **razona/planea** → **actúa** → **verifica** → y con **memoria + feedback + self-reflection** mejora con el tiempo.

### 1. Autonomía
"Misión, no guion." Recibe el objetivo y avanza solo. Pero **no es libertad total**: opera dentro de *guardrails* (reglas, políticas, filtros de seguridad). Balance = *autonomy with accountability* - libertad de camino, límites de alcance.

### 2. Goal-directed behavior
No corre funciones aisladas, busca un *outcome*. Estrategiza: elige herramientas, secuencia pasos y **decide qué NO hacer** (evita detours). Ej.: resumir un paper para audiencia de negocios = no es condensar texto, es adaptarlo al lector.

### 3. Perception
No es leer palabras, es **interpretar significado y transformar datos crudos en señales accionables**. Incluye: entender intención ("necesito ayuda con mi factura"), extraer hallazgos de un PDF, escuchar sistemas vivos (health, stock), y en agentes avanzados multimodalidad (imagen, sonido, IoT).

### 4. Reasoning & Planning
Encadena acciones en orden correcto (viaje = vuelos + visa + fechas + hotel). Evalúa **trade-offs** (precisión, costo, velocidad, relevancia). Con *dynamic planning*: cuando cambia el contexto (tool falla, prompt cambia, doc ilegible), **revisa y replanifica** en vez de seguir a ciegas.

### 5. Action execution
Transforma planes en resultados: tool calls, APIs, workflows, formularios. Incluye interacción con el mundo externo (emails, usuarios, APIs) que forma el feedback loop. **Crítico: verificar el resultado** (¿se guardó? ¿el email salió?) - omitirlo = fallos no detectados.

### 6. Memory
Da continuidad: evita repetir, referencia respuestas previas, mantiene contexto entre pasos y sesiones. A largo plazo habilita *learning y personalization*. Ej.: agente de soporte que recuerda tu issue previo.

### 7. Feedback sensitivity
Si algo no funciona (usuario corrige, tool falla repetido), **no persiste a ciegas: cambia de enfoque**. Ej.: web scraper con datos vacíos no logra "éxito" y sigue - detecta el mismatch. Loops de feedback habilitan **mejora a largo plazo**.

### 8. Self-reflection
El nivel más alto: el agente **evalúa su propio razonamiento antes de que el error cause daño**. Se pregunta "¿este plan cumple el objetivo? ¿Hay alternativas mejores?". Detecta alucinaciones y tool use inválido cuestionando su propio output (re-leer, fact-check). Lleva al agente "de *doers* a *thinkers*".

## Cierre (frase de cierre, útil para el quiz)

> "Agentic systems aren't just tools, they're systems that sense, think, act, and improve."

---

## Matiz crítico: feedback vs. self-reflection

- **Feedback sensitivity** - detectar que algo salió mal y pivotar. Ocurre **después** de la acción.
- **Self-reflection** - cuestionarse **antes** de que el error cause daño. Ocurre **pre-acción**.

## Conexión con mi experiencia

Mi lección del cross-review (Agente B introdujo un bug al "corregir" código correcto) fue un fallo de **self-reflection**: el Agente B confió en suposiciones falsas en vez de verificar contra la fuente. Mi fix - verificar contra la doc real antes de aceptar el fix - es un *guardrail externo* que el curso no menciona: la reflexión del agente no basta, hace falta **verificación contra el mundo real**. Material de entrevista: sé dónde falla la teoría y cómo diseñar alrededor.
