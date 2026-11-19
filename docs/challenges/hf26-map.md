# Hacktoberfest 2026 — Mapa de los 5 challenges DEV.to

**Estado del challenge:** cerrado. El Weekend corrió del 2 al 5 de octubre; las semanas 1 a 4 del 5 al 31 de octubre. Hoy es 2026-11-18. Este documento es **diseño y aprendizaje**, no una submission.

**Prompt base (idéntico en las 5):** construir algo con IA open-source en el núcleo — modelo open-weight, harness/framework open-source, inferencia local, o los tres. Y explicar por qué la innovación abierta importa para lo construido.

**Criterio de evaluación:** Writing Quality (peso máximo), Relevance, Creativity, Technical Execution, Partner Technology (opcional).

---

## El mapa

| # | Tema | Verbo | El giro real | Modelo open-source | Riesgo principal |
|---|---|---|---|---|---|
| 0 | Build for a Friend | **Ayudar** | Una persona concreta, con datos que no pueden ir a la nube | LLM local (Gemma 4) + RAG | Persona genérica; producto saturado (RAG) |
| 1 | Touch Grass | **Salir** | La pantalla es la parte más corta de la experiencia | BirdNET+ V3.0 + geo-model + Qwen3-VL-2B | Captura de audio en campo; ruido |
| 2 | Side Hustle | **Cobrar** | Alguien pagaría por esto hoy, no "algún día" | LLM local + tools de negocio | Ser un juguete, no un producto |
| 3 | Slow and Steady | **Delegar** | Trabaja mientras dormís; el usuario no hace nada | Agente + scheduler + visión | Prometer automatización que rompe |
| 4 | Ghost in the Machine | **Recordar** | El pasado se vuelve consultable, en tu máquina | STT local (Whisper) + LLM | Privacidad mal tratada en un tema íntimo |

**Patrón:** los 5 se resuelven con el mismo triángulo — **modelo local + tools + datos del usuario en su máquina**. Cambia el verbo y la historia, no la arquitectura. Eso permite cubrir los cinco sin construir cinco productos desde cero.

---

## Semana 0 — Build for a Friend

**Fecha:** 2-5 oct 2026 (72 h). **Premio:** $250 overall + 16 categorías de partner.

**Consigna:** construir algo que resuelva un problema real para **una persona específica**. Bonus si se lo entregás y contás qué dijo.

**Cómo lo abordamos:** Nido, un agente local para contratos y facturas de una fotógrafa freelance (caso de estudio, no persona real).

**Lecciones que quedaron:**

1. **La persona es el producto.** "Elegir un amigo con un problema de información privada" es un segmento, no una historia. Un juez no recuerda un stack; recuerda a quién ayudaste.
2. **El stack no impresiona.** RAG local es infraestructura en 2026. El giro tiene que estar en la restricción y en el vínculo.
3. **La escritura pesa más que el código.** El post es el entregable principal, y recibe 30-40 % del tiempo.
4. **La verificación determinística convierte una promesa en una garantía.** El substring check de citas es el ejemplo: se puede reproducir.
5. **Lo "local" hay que demostrarlo.** 0 requests salientes no es un claim, es una prueba con el Wi-Fi apagado.

**Artefacto real:** `projects/localdoc-agent/` — 7 pasos, 25 tests, eval 18/18.

---

## Semana 1 — Touch Grass

**Fecha:** 5-11 oct 2026. **Premio:** $250 overall + 16 categorías.

**Consigna:** algo que saque a la gente de la pantalla y la lleve al mundo. El mejor build hace que la pantalla sea la parte más corta de la experiencia.

**Candidato investigado:** "Field Notebook" — identificador de cantos de aves **offline** en un teléfono, que arma una entrada de diario de naturaleza.

**Hallazgos verificados (brief de MIND, 2026-11-18):**

- **BirdNET+ V3.0** (publicado 13 nov 2026): 11,709 especies, **Apache-2.0**, exportaciones ONNX/TFLite/Core ML, variantes *pruned* de **~72 MB** para móvil.
- **BirdNET V2.4** (el que muchos tutoriales usan) arrastra **CC BY-NC-SA 4.0**: no sirve para "open-source".
- **`birdnet-stm32` no sirve para teléfono**: es firmware para una placa con NPU.
- **Latencia no es el riesgo**: BirdNET Live mide ~84× tiempo real en un Pixel 10 Pro con el modelo pruned.
- **El geo-model** (`[lat, lon, semana]`, ~8 MB ONNX) es lo que convierte "un pájaro" en "el pájaro que puede estar acá en noviembre".

**El giro que sobrevive:** el clasificador da la especie; el geo-model restringe; el LLM **redacta** la entrada. La visión **no identifica plantas**: no hay evidencia de precisión y prometerlo sería vender humo.

**Evidencia que haría el post:** una detección **descartada** por el geo-model. Eso demuestra que la IA piensa, no que decora.

**Riesgos:** R1 licencia equivocada (copiar un tutorial de V2.4); R2 prometer identificación de flora; R3 tres falsos positivos en el demo.

---

## Semana 2 — Side Hustle

**Fecha:** 12-18 oct 2026. **Premio:** $250 overall + 17 categorías.

**Consigna:** algo que **alguien pagaría**. Freelancers, dueños de PyME, comunidades de nicho. Bonus por el primer usuario real ("¿usaron?, ¿te pagaron?, ¿qué pidieron?").

**Ideas oficiales:** ordenador de facturas local, redactor de listings para Etsy/eBay, traductor de menús para un restaurante específico.

**Por qué esta semana valida lo ya construido:** el primer ejemplo del challenge es literalmente Nido — documentos de clientes que no pueden salir de la laptop. La diferencia de la semana 0 es el encuadre: no "le ayudé a una amiga", sino "esto reemplaza una tarea que hoy le cuesta plata".

**El giro que propongo:** no otra herramienta para freelancers en general, sino **una sola decisión de negocio automatizada**: "¿a quién le tengo que cobrar hoy y qué le escribo?". El agente no hace facturación; hace **cobranza**, que es lo que duele.

**Modelo:** LLM local + tools de negocio (SQLite + reglas). Nada exótico.

**Riesgo:** ser un juguete. El test es si alguien paga aunque sea $5.

**Evidencia que haría el post:** mostrar el tiempo de la tarea antes y después, y el dinero cobrado.

---

## Semana 3 — Slow and Steady

**Fecha:** 19-25 oct 2026. **Consigna:** algo que **premie la vagancia**. Automatizar lo que se odia, o hacer la vida más fácil.

**Ideas oficiales:** resumen nocturno de chats grupales, cuento relajante offline, foto de heladera → lista de compras, ordenador de archivos y bandeja.

**Mi candidato:** **ordenador nocturno de archivos y bandeja de entrada**, corriendo local. El más "perezoso" del set, no depende de un modelo nuevo, tiene demo antes/después, y usa lo que ya sabemos hacer.

**La trampa:** "foto de heladera → lista de compras" suena a visión, pero en realidad es un agente con tools: visión para describir + lista base + lógica de reposición. La IA no "entiende" la heladera; lee la foto y produce un JSON. Es más honesto y más viable.

**El giro que gana:** que el agente corra **de noche** y el usuario vea el resultado ya hecho a la mañana. El valor no es el informe, es la ausencia de la tarea.

**Riesgo:** prometer automatización que rompe archivos. Un solo archivo movido a la carpeta equivocada mata la confianza. Mitigación: modo dry-run y un undo de 24 h.

**Evidencia que haría el post:** una carpeta real desastrosa, el antes, el plan del agente, y el después verificado.

---

## Semana 4 — Ghost in the Machine

**Fecha:** 26-31 oct 2026, cierre en Halloween y a las puertas del Día de los Muertos.

**Consigna:** algo espeluznante **o algo que honre el pasado**. El tema es intencionalmente amplio.

**Ideas oficiales:** terminal poseída, constructor de ofrendas virtuales, sesión espiritista de un lenguaje muerto, **herramienta de historia oral familiar**, generador de cuentos con logs de la casa.

**Mi candidato: historia oral familiar local.** No por Halloween, sino porque es el tema más fuerte de los cinco:

- Es Día de los Muertos de verdad, no decorado.
- Es privacidad real: las voces de una familia no van a un servidor.
- Es un modelo concreto y local: **Whisper** para transcribir.
- Tiene un demo que emociona: poner una grabación y ver el texto aparecer sin internet.
- Reusa exactamente el motor de Nido: ingesta → chunking → store local → consulta con citas, cambiando PDFs por audios y contratos por recuerdos.

**El giro que lo separa de "app de transcripción":** después de transcribir, el agente **entrevista**. Escucha lo grabado, detecta huecos ("mencionó a su hermana pero no el nombre") y hace la siguiente pregunta. El familiar mayor no tiene que saber qué contar: el agente lo guía.

**Riesgo:** es el tema más íntimo de los cinco. Tratar la privacidad mal no es un bug técnico, es una falta de respeto. Mitigación: todo local, borrado verificable, y nada de datos reales en el post sin permiso explícito.

**Evidencia que haría el post:** una entrevista real de 10 minutos, transcrita localmente, con el agente haciendo la segunda pregunta. Y el archivo final que se puede abrir sin la app.

---

## El método, resumido

Para cada semana, el mismo ciclo:

1. **Verificar la fuente.** El tema y las fechas se leen de la página, no de memoria. Nos pasó dos veces: un "Gemma 4 4B" que no existe, y BirdNET V2.4 vs V3.0 (licencia distinta).
2. **Auditar viabilidad antes de codear.** MIND investiga el modelo real: licencia, tamaño, plataforma, benchmark. Veredicto GO / NO-GO / GO CON CAMBIOS.
3. **MVP mínimo con lo que ya funciona.** RAG local, SQLite, FastAPI, modelos locales. Nada nuevo si no es el núcleo del tema.
4. **Evidencia honesta.** Qué funcionó y qué no, con números. Un post que admite un error vale más que uno que declara 95 % sin método.
5. **El post es el entregable.** Se escribe en paralelo, no al final.

## Lo que no se repite

- No se construyen 5 productos desde cero. Se construye **un motor y cinco relatos**.
- No se promete lo que no se midió (identificación de plantas, precisión sin eval).
- No se usa V2.4 cuando la licencia limpia es V3.0.
- No se deja el post para el último día.
- No se toma un dato del título: se verifica contra la fuente.

_Actualizado 2026-11-18. Fuentes: páginas de cada challenge en dev.to y el brief de `agents/kanam-mind/briefs/2026-11-18-birdid-offline-feasibility.md`._
