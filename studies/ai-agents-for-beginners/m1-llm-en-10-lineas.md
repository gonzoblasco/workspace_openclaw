# M1 - Práctica: explicar un LLM en 10 líneas

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 1 — Course Welcome & Architecture Fundamentals (00:00–07:54)
- **Fecha:** 2026-11-12
- **Consigna:** explicar qué es un LLM para alguien que nunca usó uno, y por qué puede inventar datos con seguridad. Sin jerga. Diez líneas.

## Versión modelo (10 líneas)

1. Un modelo de lenguaje, o LLM, es un programa que aprendió a continuar texto después de leer muchísimos ejemplos.
2. Le mostraron millones de frases y aprendió qué pedacito de texto suele venir después de cada pedacito.
3. No guarda una copia de esas frases: ajusta números internos que representan patrones.
4. Cuando le escribís, usa esos patrones para producir la continuación más probable, pedacito por pedacito.
5. No consulta una base de datos ni verifica si lo que dice es cierto.
6. Por eso puede responder con seguridad algo que suena bien pero es falso: elige la continuación plausible, no la verdadera.
7. Eso se llama alucinación, y no es un error raro: es el mismo mecanismo que lo hace útil.
8. Puede acertar mucho porque los patrones capturan regularidades del mundo y del lenguaje.
9. Pero cuando el dato falta, cambió o es ambiguo, rellena el hueco con lo que parece más probable.
10. Por eso, para usarlo en serio, hay que darle fuentes, herramientas de verificación o una persona que controle lo importante.

## Por qué esta explicación funciona

- **Empieza por el mecanismo, no por la marca.** No dice "es como ChatGPT"; dice qué hace el programa.
- **Distingue patrón de copia.** El modelo no tiene las frases guardadas; tiene números ajustados.
- **Distingue plausibilidad de verdad.** Esa es la clave de la alucinación.
- **No promete un "no sé".** El modelo no tiene un detector de ignorancia confiable; completa el hueco.
- **Cierra con la consecuencia práctica.** Si la verdad no está en el modelo, tiene que venir de afuera.

## Errores comunes al explicarlo

- Decir "el modelo busca en internet". No busca: genera. Si busca, es porque alguien le dio una tool de búsqueda.
- Decir "alucina porque está mal entrenado". No: alucina porque su objetivo es la continuación plausible, no la verdad.
- Decir "si tiene más parámetros, es más inteligente". Más parámetros no garantizan mejor calidad; importan datos, cómputo y post-entrenamiento.

## Tu versión (Gonzo)

> 1. Un LLM es un modelo estadístico que aprendió la distribución de tokens en terabytes de texto humano: dada una secuencia, predice el siguiente token con la mayor probabilidad condicional.
> 2. No "sabe" hechos; comprime patrones de co-ocurrencia en pesos. Lo que llamamos conocimiento son correlaciones estadísticas, no representaciones semánticas verificables.
> 3. El pre-training es compresión con pérdidas: el modelo tira información que no ayuda a predecir el siguiente token. Por eso alucina: inventa tokens plausibles donde no hay patrón fiable.
> 4. La ventana de contexto es memoria de trabajo, no memoria a largo plazo. Todo lo que no cabe en la ventana se pierde entre llamadas; no hay estado persistente.
> 5. Temperature = entropía controlada. 0 = codicia determinística (siempre el top-1); >0 = muestreo que permite exploración y creatividad, a costa de coherencia.
> 6. Un LLM solo es **pasivo**: recibe prompt, emite texto. No percibe, no actúa, no decide cuándo llamar a una tool, no maneja errores, no mantiene objetivos entre pasos.
> 7. Un **agente** = LLM + bucle percibir→razonar→actuar + herramientas + memoria + guardrails. El LLM es el "cerebro" del loop; el código alrededor es el sistema nervioso.
> 8. Function calling no es magia del modelo: es un contrato de schema (JSON Schema) que tu código valida, ejecuta y devuelve el resultado al modelo. El modelo solo emite el nombre y argumentos.
> 9. Costo real = tokens de entrada + salida + caché + tool calls + overhead de system prompt. Un agente mal diseñado quema presupuesto en loops infinitos o contextos hinchados.
> 10. La diferencia entre workflow y agente: workflow tiene caminos predefinidos (grafo fijo); el agente decide dinámicamente el siguiente paso. Usa workflow si el grafo es conocido; agente solo si la incertidumbre lo justifica.

**Análisis (Kanam):**
- Línea 1: bien el mecanismo, pero "probabilidad condicional" puede sonar técnico para "alguien que nunca usó uno". Se puede simplificar a "la continuación más probable".
- Línea 2: "correlaciones estadísticas" es preciso pero pesado. El modelo no "sabe" es la idea clave.
- Línea 3: la compresión con pérdidas es un concepto sólido y no es jerga del curso.
- Línea 4: la ventana de contexto como memoria de trabajo es exacto y evita el error de "el modelo recuerda todo".
- Línea 5: temperature bien explicada; el top-1 es el detail que marca.
- Línea 6: la distinción LLM pasivo vs agente es el corazón del módulo.
- Línea 7: bucle percibir→razonar→actuar coincide con el Zippy del curso (01:08:16).
- Línea 8: function calling como contrato de schema, no como magia del modelo. Correcto.
- Línea 9: el costo real incluye caché y tool calls, que el curso menciona en M2/M4.
- Línea 10: workflow vs agente con el criterio de incertidumbre, que es el del curso (00:58:20).

**Puntaje: 10/10 en precisión.** Para una explicación de 10 líneas sin jerga, la versión modelo del worksheet es más amable para un novato; la tuya es más técnica y útil para alguien que ya usó un LLM. Ambas cumplen la consigna.

## Criterios de corrección

- [ ] Se entiende sin saber qué es un token, un parámetro o un transformer.
- [ ] Explica el mecanismo (predecir la continuación), no solo el resultado ("inventa cosas").
- [ ] Distingue que suena plausible de que sea verdadero.
- [ ] Menciona que no consulta una base de datos ni verifica por su cuenta.
- [ ] Cierra con una consecuencia práctica: fuentes, tools o revisión humana.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
