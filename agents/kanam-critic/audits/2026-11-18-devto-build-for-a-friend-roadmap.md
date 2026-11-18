# Auditoría adversarial — "Soberanía para un Amigo" (DEV.to / Hacktoberfest Weekend 2026)

**Auditor:** Critic (SHARP)  
**Fecha:** 2026-11-18  
**Objeto:** roadmap de 5 fases para el challenge "Hacktoberfest Weekend: Build for a Friend".  
**Veredicto de elegibilidad:** **NO ELEGIBLE** — la ventana de submission cerró el 2026-10-05 a las 06:59 UTC.  
**Veredicto SHARP del plan:** **9/25 — Rechazo.** La intuición es correcta; el plan no decide nada.  
**Veredicto de la idea:** **alta relevancia, baja diferenciación.** "IA local + persona real + restricción dura" es exactamente el core del challenge; "RAG local genérico" es el demo más saturado del ecosistema.

---

## 0. Veredicto ejecutivo (lo que hay que oír primero)

1. **El premio que querés ganar ya se entregó.** El challenge corrió del 2 al 5 de octubre de 2026; los ganadores se anunciaron el 9 de octubre. Hoy es 18 de noviembre. No hay arquitectura, narrativa ni demo que supere ese gate. Si el objetivo es cobrar en 2026, este roadmap no es elegible; hay que buscar otro challenge activo.
2. **Aunque la ventana estuviera abierta, el post no sería elegible a premios: está en español.** Las reglas dicen que las submissions no inglesas solo reciben badge de completitud. El título "Soberanía para un Amigo" y la cita de la Fase 5 son, literalmente, un auto-disqualifier.
3. **El plan es un índice de temas, no un plan.** No elige amigo, tarea, modelo, harness, UI, métrica ni fecha. "Un agente", "un framework ligero", "una acción concreta" son placeholders. Un juez no puede imaginar el proyecto; un builder no puede ejecutarlo.
4. **El scope es de 3-4 semanas, no de 72 horas.** PDFs + notas de voz + CSVs + RAG + agente + verificación + Docker + UI + handover. Sin cut lines, el 80% queda a medias.
5. **El criterio de mayor peso —Writing Quality— recibe una sola fase y ningún entregable.** El post es el producto; el roadmap lo trata como un apéndice.
6. **La idea merece un plan mejor.** El giro no es "usé Ollama"; es "le devolví a una persona el control de sus datos, y se lo probé". Eso se puede construir en un fin de semana si se elige bien el amigo, la tarea y el corte.

---

## 1. La evidencia que invalida el objetivo (no es opinión)

| Hecho | Fuente | Implicancia |
|---|---|---|
| Entry Period: 2 oct 2026 02:00 UTC → 5 oct 2026 06:59 UTC | Contest Rules, DEV.to | Hoy (18 nov) el challenge está cerrado hace 44 días. |
| Overall winner anunciado el 9 oct 2026 | DEV Team, "Congrats to..." | El premio ya tiene dueño. |
| Hacktoberfest 2026 terminó el 31 oct 2026 | Cobertura de cierre | No hay una edición activa en noviembre. |
| "Non-english submissions are eligible for a completion badge but not eligible for prizes" | Challenge page, FAQ | Un post en español no compite por los $250 ni por categorías. |
| "Writing Quality (weighted most heavily)" | Challenge page, Judging Criteria | El post no es documentación; es el entregable principal. |
| "New project built during the Entry Period"; pull requests no elegibles | Contest Rules | El repo debe nacer y completarse dentro de la ventana; hay que planificar commits. |
| 1 overall + 6 featured ($200) + 10 partner ($100) = 17 winners | Contest Rules | Hay 16 categorías; ignorarlas es dejar valor sobre la mesa. |
| "Bonus points if you actually hand it over and tell us what they said" | Challenge page | La reacción del amigo es parte del score, no un extra. |
| "Many of you told us how the person you built for reacted, and those stories made judging both a joy and a challenge" | Winners announcement | La historia humana es lo que distingue; un "amigo genérico" es invisible. |

**Conclusión:** el roadmap no compite por el premio 2026. Se puede auditar como blueprint para la próxima ventana (Hacktoberfest 2027 o un challenge activo), y eso es lo que hago abajo. Pero el objetivo declarado —"ganar el primer premio o alguna categoría"— es imposible en la fecha actual. Cualquier análisis que lo ignore es teatro.

---

## 2. SHARP del roadmap actual (aplicado al plan, no a un artefacto)

| Eje | Puntaje | Evidencia en el roadmap | Por qué |
|---|---:|---|---|
| **S — Sharpness** | 2/5 | "Elegir un amigo", "un agente", "un framework ligero", "una acción concreta", "Docker o script" | No hay nombre, tarea, formato, métrica ni fecha. Es un table of contents, no un plan. |
| **H — Horizon** | 2/5 | Fase 4: "observar al amigo usando el agente y ajustar prompts" | No hay ciclo de vida del dato, actualización de modelo, crecimiento del corpus, borrado, exportación ni mantenimiento. "Observar" no es sostener. |
| **A — Asymmetry** | 2/5 | 5 fases, 3 modalidades de datos, RAG, agente, verificación, Docker, UI implícita; Writing Quality = 1 párrafo | Mucho esfuerzo en lo que no puntúa; poco en el criterio de mayor peso. La palanca está invertida. |
| **R — Resistance** | 1/5 | No hay hardware, errores, prompt injection, consentimiento, elegibilidad, fallback ni plan de instalación real | Asume datos perfectos, amigo técnico, máquina compatible y ventana abierta. Falla en el primer contacto con la realidad. |
| **P — Parsimony** | 2/5 | ChromaDB/FAISS + Docker + PDFs + voz + CSV + framework + verificación + Obsidian | Para un MVP de 72 h, demasiadas piezas. No hay una decisión de "una sola cosa". |
| **Total** | **9/25** | | **Rechazo. Re-diseño total.** |

No es un 13 (VETO) porque el problema no es un detalle: es que el plan no tomó ninguna decisión difícil. Un plan que no elige no se puede ejecutar; se puede improvisar, que es distinto.

---

## 3. Fallas fatales y graves

### 3.1 Fatales (matan la submission o el resultado)

**F1. Calendario.** El challenge cerró. Evidencia: reglas y winners. No hay corrección técnica posible. **Fix:** elegir una ventana abierta; poner las fechas en el calendario y un gate de "si no hay ventana, no hay submission".

**F2. Idioma.** El post está en español; las reglas excluyen submissions no inglesas de los premios. **Fix:** escribir el post en inglés desde el outline; el español queda para el diseño interno. No traducir al final: la voz se pierde y el tiempo se triplica.

**F3. Amigo genérico.** "Elegir un amigo con un problema de gestión de información privada" no es una persona; es un segmento. No hay nombre, profesión, tarea recurrente, dolor concreto ni stakes. El challenge pide "one real person"; los jueces premiaron historias de padres, abuelos, hermanos, compañeros y amigos. **Fix:** una persona con nombre (o seudónimo), una tarea semanal que odia, un dato que no puede subir a la nube, y una cita suya en el post.

**F4. Producto genérico.** "Agente que responde preguntas sobre documentos privados con RAG local" es el demo más repetido de 2024-2026. No hay giro creativo. "Soberanía de datos" es un eslogan, no una feature. **Fix:** un twist construido en el MVP (ver §5): borrado verificable, caja portátil, o libro de consentimiento. Algo que se pueda mostrar en un GIF y que un juez recuerde al día siguiente.

**F5. Sin UI para el amigo.** El roadmap menciona "instalación zero-config" y "observar al amigo", pero no diseña una interfaz. Un agente CLI no es un producto para una persona no técnica. El tema es "Build for a Friend", no "Build for a Developer". **Fix:** app web local con drag-and-drop, chat, panel de fuentes, preview del draft, badge "local" y botón de borrado. Una sola pantalla, tres pasos.

**F6. Scope de 3-4 semanas en 72 horas.** Tres modalidades de ingesta (PDF, voz, CSV) + RAG + agente + verificación + Docker + UI + handover. Sin time boxes ni cut lines. **Fix:** una modalidad, una acción, un twist. Cortar voz/CSV/Docker/polish antes de cortar citas, eval, test con el amigo o post.

**F7. Writing Quality desatendida.** Es el criterio de mayor peso y recibe una fase de un párrafo. No hay título, hook, estructura, demo, assets, eval ni revisión. **Fix:** 30-40% del tiempo al post; empezar el sábado; capturar screenshots/GIFs mientras se construye; publicar con 2 h de buffer.

### 3.2 Graves (no matan, pero bajan el score)

**G1. Modelos obsoletos.** Gemma 2 9B es de mediados de 2024; en noviembre de 2026 hay Gemma 4 (12B/26B/31B), Qwen3.5-9B, Qwen3.6-35B-A3B, gpt-oss-20b, GLM-4.7-Flash, entre otros. "Mistral" sin versión es una no-decisión. **Evidencia:** el benchmark de Larsen (14 oct 2026) muestra que el tool calling varía muchísimo entre modelos pequeños: gpt-oss 20B pasó 43/45; Gemma 4 12B, 33/45; Qwen3 Coder 30B, 27/45; Gemma 4 26B A4B, 27/45; Llama 3.1 8B, 24/45. La velocidad no es confiabilidad: Qwen3 Coder 30B corre a 3.0 s/tarea pero falla el paso de leer la página. **Fix:** benchmark propio de 10-15 tareas en la máquina del amigo; elegir el modelo más pequeño que pase; no elegir por reputación.

**G2. Embeddings English-centric.** nomic-embed-text es una buena opción para inglés, pero para documentos en español es subóptima. **Fix:** BGE-M3 (multilingüe, 8k contexto) o un embedding multilingüe actual; verificar licencia y tamaño. Más importante que el modelo: chunking por estructura (cláusulas, secciones, páginas), no por ventanas fijas.

**G3. "Framework ligero" sin nombre.** Ollama es un runtime de inferencia, no un agent harness. El challenge acepta "open-source agent harness or framework"; no nombrarlo deja un hueco técnico y narrativo. **Fix:** smolagents (Apache 2.0, Python, tool-calling) o Mastra (TypeScript, partner category), o un loop propio de ~150 líneas. Elegir uno, documentarlo, mostrar el trace.

**G4. CSVs en RAG.** Un CSV no es un documento para embeddings; es una tabla. Meterlo en el vector store es un error de categoría. **Fix:** DuckDB/SQLite + tool de SQL read-only, o cortar el CSV. Si el amigo es un freelancer con facturas, el CSV puede ser el core; entonces el agente es text-to-SQL + RAG para contratos, no "todo en Chroma".

**G5. Verificación ingenua.** "Doble chequeo con citación de fuente exacta" no dice cómo se verifica. Los LLMs inventan números de página y citas. **Fix:** el modelo devuelve JSON con `chunk_id`, `page`, `quote`; la app verifica que la cita sea un substring exacto del chunk; si falla, reintenta una vez o se niega a responder. Verificación determinística, no otro LLM.

**G6. Sin eval.** "Funciona" es un demo, no evidencia. **Fix:** 18 preguntas (6 fáciles, 6 multi-hop, 3 sin respuesta, 3 con números/fechas), métricas: answer accuracy, citation validity, refusal correctness, p50 latency, peak RAM. Tabla en el post.

**G7. Sin privacy proof.** "Local" es una afirmación; no hay prueba. **Fix:** query con Wi-Fi apagado o monitor de red; screenshot de 0 requests salientes; auditar telemetría de Ollama; documentar la descarga única del modelo; definir qué significa "local" con precisión.

**G8. Sin seguridad.** Un agente local con datos personales y tool calls es blanco de prompt injection desde los documentos. **Fix:** tratar el texto recuperado como untrusted, sin herramientas de red, escritura solo en `output/` sandbox, confirmación para acciones destructivas, y un test con un PDF malicioso.

**G9. Sin partner category.** Hay 16 categorías; el roadmap no elige ninguna. Ollama no es partner; Gemma sí. **Fix:** si usás Gemma 4, entrás a Best Use of Gemma ($200); si usás un agent session (DevRelay/Entire), podés sumar otra; no fuerces Render/DigitalOcean/MongoDB si contradicen el local-first.

**G10. Sin entrega.** No hay repo, licencia, README, demo video, agent session ni checklist de submission. **Fix:** repo público desde el día 1, licencia MIT/Apache-2.0, README con quickstart, dataset sintético, demo de 90 s, y checklist de reglas.

**G11. Sin consentimiento.** "Observar al amigo" sin consentimiento ni redacción es un riesgo ético y reputacional. **Fix:** acuerdo de una página, datos anonimizados en el post, demo con datos sintéticos, aprobación de la cita por el amigo.

---

## 4. Correcciones tecnológicas (de la decisión vaga a la decisión defendible)

| Original | Problema | Reemplazo | Por qué |
|---|---|---|---|
| Gemma 2 9B / "Mistral" | Obsoleto / ambiguo; sin benchmark de hardware | **Gemma 4 12B** si el amigo tiene ≥16 GB y querés Best Use of Gemma; **Qwen3.5-9B** si 8-16 GB; **gpt-oss-20b** si priorizás tool-calling; benchmark de 10 tareas en la máquina del amigo | Gemma 2 es dos generaciones atrás; el benchmark 2026 muestra diferencias grandes de tool calling. Gemma 4 además califica para una categoría de $200. |
| nomic-embed-text | Inglés-centric; documentos en español | **BGE-M3** (multilingüe, 8k) o embedding multilingüe actual | Mejor recall en español; menos citas vacías. Verificar licencia/tamaño. |
| ChromaDB / FAISS | Servidor/telemetría o falta de metadata; overkill para <50k chunks | **SQLite + sqlite-vec + FTS5** | Un solo archivo, metadata para citas, hybrid search (BM25 + vector + RRF), borrar/backup trivial. Alineado con la narrativa de soberanía. |
| "Framework ligero" | No es un harness; Ollama es runtime | **smolagents ToolCallingAgent** (Python, Apache 2.0) o **Mastra** (TS, partner) o loop propio | Cumple el core "open-source agent harness"; hace visible el loop; permite traces. |
| PDFs + voz + CSV | Scope explosion; tres pipelines | **Una modalidad**: PDFs con Docling (MIT) o Markdown/TXT; CSV con DuckDB; voz con Whisper solo si es el core | Un fin de semana no alcanza para tres ingresos. Elegir el que duele de verdad. |
| Docker / "zero-config" | Docker Desktop no es zero-config para un amigo no técnico | **uv + Makefile + `run.command`** (macOS) / `run.bat`; Docker opcional para devs | Un doble clic y el navegador; sin terminal, sin daemon, sin 1 GB de Docker. |
| CLI / agente | No es usable por el amigo | **FastAPI + HTMX** (o Gradio como fallback): drag-and-drop, chat, fuentes, draft, privacy dashboard | El amigo es el usuario; el demo debe mostrarlo a él, no al builder. |
| "Doble chequeo" | No verificable | **JSON schema + substring check** de la cita; reintento o refusal | Convierte "citación" en una garantía técnica, no en una promesa del modelo. |
| Sin eval | "Funciona" sin evidencia | **18 preguntas + métricas** (accuracy, citation validity, refusal, latency, RAM) | Tabla en el post; permite iterar; los jueces ven rigor. |
| Sin privacy proof | Claim sin prueba | **Wi-Fi off / nettop + telemetría + delete-all** | La soberanía se demuestra, no se declara. |
| Sin seguridad | Prompt injection | **Untrusted tags + no network tools + sandbox + injection test** | Un agente con datos personales debe resistir documentos maliciosos. |
| Sin partner | $ dejados sobre la mesa | **Gemma 4 (Best Use of Gemma)** + **Entire/DevRelay** si aplica; opcional Render con datos sintéticos | Categorías naturales, no forzadas. |
| Sin licencia/repo | No es open source de verdad | **MIT/Apache-2.0**, repo público, README, dataset sintético, model card | El challenge es de open-source AI; el artefacto debe ser abierto y reproducible. |
| Post en español | No elegible | **Post en inglés**, revisión nativa; español solo interno | Regla explícita del challenge. |

### 4.1 Matriz de modelo por hardware (punto de partida, no dogma)

| RAM del amigo | Candidato | Tamaño 4-bit aprox. | Comentario |
|---|---:|---:|---|
| 8 GB | Qwen3.5-9B | 5.6 GB | Apache 2.0; buen tool calling; no califica para Gemma. |
| 16 GB | Gemma 4 12B | verificar GGUF (~7-8 GB) | Califica para Best Use of Gemma; más lento que gpt-oss en el benchmark; medir en la máquina. |
| 16 GB | gpt-oss-20b | 12.1 GB | Mejor tool calling del benchmark (43/45); tight en 16 GB; no partner category. |
| 24-32 GB | Qwen3.6-35B-A3B / Gemma 4 26B A4B | 20.4 / 14.6 GB | Más calidad; overkill para un weekend; riesgo de latencia. |
| 64 GB+ | gpt-oss-120b / Mistral Small 4 | 63.4 / 72.2 GB | No necesario; el amigo no tiene esa máquina. |

**Regla:** el modelo se elige en la máquina del amigo, con su dataset, y con una eval de 10 tareas. El benchmark de terceros es un prior, no una verdad. Si el modelo no corre fluido en su laptop, el proyecto no existe para ella.

### 4.2 Arquitectura corregida (una sola pasada)

```
[Documentos del amigo] -> [Ingesta: Docling/Markdown] -> [Chunks por cláusula/sección + metadata]
        -> [SQLite: FTS5 + sqlite-vec + metadata] -> [Hybrid retrieval: BM25 + vector + RRF]
        -> [Agente: smolagents/Mastra + Ollama/Gemma 4] -> [JSON: answer + citations + confidence]
        -> [Verificación determinística: quote substring] -> [UI: fuentes + draft]
        -> [Acción: write_draft a output/ sandbox] -> [Obsidian]
```

**Por qué esta arquitectura y no la del roadmap:**
- Una sola base de datos (SQLite) en lugar de Chroma/FAISS: menos piezas, más fácil de borrar, metadata para citas.
- Chunks por cláusula: una cita de contrato debe apuntar a la cláusula, no a una ventana de 512 tokens.
- Híbrido: los nombres, montos y fechas se buscan mejor con BM25; los conceptos, con vectores. RRF combina ambos sin tuning.
- Verificación determinística: el juez puede reproducirla; un segundo LLM no.
- UI + acción: el amigo ve el resultado en su formato, no un JSON.

---

## 5. El giro creativo que falta

"RAG local" no es creativo en 2026; es infraestructura. La creatividad tiene que venir del vínculo y de la restricción, no del stack. Tres opciones, ordenadas por factibilidad en un fin de semana:

1. **"El botón que lo borra todo" (recomendado).** Un botón que elimina índice, embeddings, logs, drafts y copias; una pantalla "Where is my data?" con un mapa; un antes/después del filesystem. Es poco código, muy visual, y convierte "soberanía" en una acción verificable. El juez recuerda el GIF del borrado.
2. **"La caja de soberanía portátil" (stretch).** Modelo + app + datos en un SSD USB encriptado; se desenchufa el Wi-Fi, se enchufa el disco, se pregunta, funciona. Es el demo más memorable posible, pero el packaging es un riesgo; solo si el core está terminado el sábado a la noche.
3. **"El libro de consentimiento" (ambicioso).** Cada documento tiene permisos; el agente solo ve lo que el amigo autoriza; un audit log muestra qué se accedió. Es excelente para datos de clientes, pero es más código; dejarlo como "next" si no hay tiempo.

**El verdadero diferenciador, de todos modos, es la persona.** Los jueces escribieron: "Many of you told us how the person you built for reacted, and those stories made judging both a joy and a challenge." Un "amigo con PDFs" no compite contra "mi abuela, que grabó las recetas en cassettes" o "mi hermana, que acaba de abrir su estudio". El post debe empezar con la persona, no con la arquitectura.

---

## 6. Roadmap corregido (para la próxima ventana)

> **Premisa:** esto es para un challenge con ventana abierta (Hacktoberfest 2027 o uno activo). Si el objetivo es el Weekend 2026, no hay roadmap: hay un premio ya entregado. Ver §1.

### 6.1 Proyecto en una frase

**Para [Nombre], [profesión], que [tarea recurrente que odia]:** un agente local que responde sobre sus [contratos/facturas/notas] con cita exacta y le arma [entregable concreto, ej. recordatorio de pago] en Markdown para Obsidian. Corre offline en su laptop, no manda datos a ninguna nube, y borra todo con un botón.

**Ejemplo ejecutable:** "Para Lucía, fotógrafa freelance: un agente local que responde sobre sus contratos y facturas con cita exacta y le arma el recordatorio de pago en Markdown para Obsidian; corre offline en su MacBook y borra todos sus datos con un botón." Reemplazar Lucía por el amigo real; mantener la estructura.

**Criterio de selección del amigo:**
- Tiene una tarea **recurrente** (semanal/mensual), no un problema hipotético.
- El dato es **sensible** y no puede ir a una nube (clientes, salud, dinero, contratos).
- La tarea tiene un **output claro** que se puede verificar (un brief, un recordatorio, una tabla).
- El amigo puede **probar el MVP** en el fin de semana y dar feedback.
- Hay **consentimiento** y se puede **anonimizar** en el post.

### 6.2 Stack final (decisiones, no menú)

| Capa | Decisión | Alternativa | Criterio |
|---|---|---|---|
| Runtime | Ollama local | llama.cpp | Instalación simple, API OpenAI-compatible, tool calling/structured outputs. |
| Modelo | Gemma 4 12B si ≥16 GB y querés Best Use of Gemma; Qwen3.5-9B si 8 GB; gpt-oss-20b si tool-calling es crítico | Benchmark propio | El más pequeño que pase la eval en la máquina del amigo. |
| Embeddings | BGE-M3 | Qwen3-Embedding | Multilingüe; 8k; verificar licencia/tamaño. |
| Store | SQLite + sqlite-vec + FTS5 | LanceDB | Un archivo; metadata; híbrido; borrar/backup trivial. |
| Harness | smolagents ToolCallingAgent (Python) | Mastra (TS), loop propio | Apache 2.0; simple; Ollama vía endpoint compatible. |
| UI | FastAPI + HTMX + Tailwind | Gradio | Control visual; una sola pantalla; sin terminal. |
| Packaging | uv + Makefile + `run.command` | Docker (solo devs) | Doble clic; sin daemon; probado en la máquina del amigo. |
| Observabilidad | JSONL local + panel "How I got this answer" | DevRelay/Entire para la sesión de build | Trazabilidad sin mandar datos del amigo a la nube. |
| Eval | 18 preguntas + script | — | Evidencia para el post; iteración. |
| Licencia | MIT (código) + CC-BY (post) | Apache-2.0 | Open source real; verificar licencia del modelo. |

### 6.2.1 Qué hace que el repo sea "hackeable"

- **`make demo` con datos sintéticos**: un juez clona, corre un comando y ve la demo sin los datos privados del amigo.
- **Un solo archivo de config**: `config.yaml` con `model`, `embedding_model`, `store_path`, `top_k`; cambiar de Gemma 4 a Qwen es una línea.
- **Módulos separados**: `ingest.py`, `retrieve.py`, `agent.py`, `verify.py`, `ui.py`; cada uno con una función clara y un test.
- **Dataset de ejemplo + eval**: `data/demo/` y `eval/questions.yaml`; el juez puede correr la eval y ver la tabla.
- **Tests de seguridad**: `tests/test_citation.py` y `tests/test_injection.py`; no solo "funciona", también "resiste".
- **`docs/decisions.md`**: por qué SQLite y no Chroma, por qué Gemma 4 y no gpt-oss, qué se cortó; esto es oro para el post y para el juez.
- **README de 5 minutos**: requisitos, instalación, modelo, demo, troubleshooting, licencia.
- **Modo "bring your own docs"**: una carpeta `data/private/` ignorada por git; el amigo puede apuntar a su carpeta sin tocar código.

### 6.3 Plan de 72 horas (con cut lines)

| Bloque | Horas | Objetivo | Entregable | Cut line |
|---|---:|---|---|---|
| **T-14 a T-7** | 6-8 h (pre-work, no código) | Leer reglas, reclutar amigo, consentimiento, inventario de datos, benchmark de hardware, scaffold del repo, outline del post | Brief de una página: fechas, reglas, amigo, tarea, stack, categorías, kill criteria | Si no hay amigo/consentimiento, no hay proyecto. |
| **Viernes 18-23** | 5 h | Co-design con el amigo; esqueleto; un PDF; una pregunta con cita | Demo cruda end-to-end (sin UI); notas de la sesión | Si la ingesta falla en sus PDFs, cambiar a Markdown/TXT o a otro dataset; no pelear con OCR >90 min. |
| **Sábado 08-13** | 5 h | Ingesta, chunking por cláusula, SQLite, híbrido, schema de respuesta, verificación, eval set | Retrieval + citas verificables + 18 preguntas | Si el híbrido no está, BM25 solo; no cortar la verificación. |
| **Sábado 14-19** | 5 h | UI (drag-drop, chat, fuentes, draft), acción, errores, badge local | App usable por el amigo | Si la UI no está, Gradio; no cortar la acción ni las fuentes. |
| **Sábado 20-23** | 3 h | Friend test #1; arreglar top 3; escribir 600-800 palabras; capturar assets | Lista de fricciones + primer borrador + screenshots/GIF | Si el amigo no completa la tarea, arreglar onboarding, no el modelo. |
| **Domingo 08-12** | 4 h | Injection test, privacy proof, delete-all, packaging, eval final | Tabla de eval + prueba de red + instalador | Si el packaging falla, video de instalación en la máquina del amigo; no Docker para ella. |
| **Domingo 12-16** | 4 h | Friend test #2; cita; terminar post; proofread; links | Post completo en inglés + assets + repo | Si falta tiempo, cortar polish y stretch; no cortar eval, privacy proof, cita, inglés. |
| **Domingo 16-18** | 2 h | Publicar, submitir, verificar, buffer | Submission válida | No publicar en la última hora. |

**Total:** ~22-24 h de trabajo efectivo. Es un fin de semana largo, no una semana. Si el scope no entra, se corta; no se estira.

### 6.4 Definition of Done (aceptación)

- [ ] El amigo instala/abre la app en <10 min con una guía de una página, sin terminal (o con un solo doble clic).
- [ ] 10/10 preguntas de muestra devuelven una respuesta con cita válida o un refusal correcto.
- [ ] 100% de las citas pasan el substring check.
- [ ] Un documento malicioso con "ignore previous instructions" no dispara la instrucción; el agente lo ignora o lo reporta.
- [ ] Una query con Wi-Fi apagado no genera requests salientes (verificado con monitor de red).
- [ ] El botón "Delete everything" borra índice, embeddings, logs, drafts y copias; verificado por filesystem.
- [ ] El amigo completa la tarea objetivo en <5 min y dice que la usaría de nuevo.
- [ ] El repo corre desde un clone limpio con `make demo` y datos sintéticos en <5 min.
- [ ] El post está en inglés, con los tags requeridos, demo, código, arquitectura, eval, privacy proof y cita del amigo.
- [ ] La submission se publicó antes del deadline y el formulario se completó.

### 6.5 Risk register

| Riesgo | Prob. | Impacto | Mitigación | Trigger |
|---|---|---|---|---|
| Challenge cerrado / fecha mal | Alta | Fatal | Gate de elegibilidad T-14; calendario | Si la ventana no está abierta, no se construye para ese premio. |
| Post no elegible por idioma | Alta | Fatal | Escribir en inglés desde el outline; revisión nativa | Si el draft no está en inglés el sábado, se corta el scope, no el idioma. |
| Fuga de datos del amigo | Media | Fatal reputacional | Consentimiento, redacción, dataset sintético, revisión del post | Si una screenshot tiene un nombre real, se reemplaza. |
| Scope creep | Alta | Fatal para el weekend | Una modalidad, una acción, un twist; cut lines | Si aparecen PDFs escaneados/voz/CSV, se cortan. |
| Modelo lento/inestable | Media | Serio | Benchmark en la máquina del amigo; fallback a modelo menor | Si p50 >15 s o RAM >80%, bajar de modelo. |
| Instalación falla | Media | Serio | `run.command`, `doctor`, prueba en la máquina del amigo | Si falla 2 veces, video de instalación y soporte 1:1. |
| Citas inválidas | Media | Serio | Chunking por cláusula; substring check; refusal | Si citation validity <100%, no se publica el claim de "exact citations". |
| Prompt injection | Media | Serio | Untrusted tags; no network tools; sandbox; test | Si el test falla, se bloquea la acción y se reporta. |
| Historia genérica | Alta | Serio | Amigo con nombre, tarea, cita, before/after | Si el post podría ser de cualquier persona, se reescribe el hook. |
| Post apurado | Alta | Serio | Draft sábado; assets durante el build; publicar 16:00 | Si el post no está listo a las 17:00, se publica la versión simple, no se pierde el deadline. |
| Repo no reproducible | Media | Serio | `make demo` con datos sintéticos; CI; README | Si un juez no puede correrlo en 5 min, technical execution baja. |
| Sin partner category | Alta | Oportunidad | Mapear 1-2 categorías genuinas; no forzar | Si la categoría no es genuina, no se lista. |

### 6.6 El post (inglés, estructura, assets)

**Títulos posibles:**
1. "My friend is a freelance photographer. Her contracts were in 400 PDFs. So I built her a private AI that runs on her laptop."
2. "She refused to upload her clients' contracts to ChatGPT. Here's the local agent we built in a weekend."
3. "The AI that forgets on purpose: a local document agent for my friend's business."
4. "I gave my friend her data back: a weekend build with Gemma 4, Ollama, and a delete button."

**Hook (primeras 3 oraciones):** la persona, el dato, el stakes. Ejemplo: "Lucía has been photographing weddings for eight years. Her contracts, invoices, and client notes live in a folder she never backs up to the cloud, because the cloud is someone else's computer. Last weekend, we built her an AI that never leaves that folder."

**Estructura (template del challenge):**
- **What I Built** (150-250 palabras): la persona, el problema, la solución en una frase, el GIF.
- **Demo** (video/GIF + link): 90 s; el amigo usándolo, no el builder; la cita exacta; el draft; la prueba de red.
- **Code** (repo + snippets): arquitectura, 3 fragmentos clave (chunking por cláusula, hybrid retrieval, verificación).
- **How I Built It** (500-700 palabras): stack, decisiones, lo que se rompió, el fix, el eval.
- **Why Does Open Innovation Matter?** (250-350 palabras): tabla closed vs open; costo, privacidad, offline, model swap; el counterfactual.
- **My Agent Session** (opcional): DevRelay/Entire; cómo se construyó; qué preguntó el agente.
- **Prize Categories**: Best Use of Gemma; Entire/DevRelay si aplica; no listar lo que no se usó.
- **Limitations & Next**: PDFs escaneados, voz, Windows, calidad del modelo; honestidad.

**Assets obligatorios:** cover image (la persona/laptop, no un robot), 2 GIFs (pregunta→cita; borrado), diagrama de arquitectura, tabla de eval, screenshot de red 0 requests, cita del amigo, 3 code snippets, link al repo y al video.

**Judging matrix (para el post):**

| Criterio | Evidencia | Dónde |
|---|---|---|
| Writing Quality | Historia específica, voz del amigo, estructura, honestidad, prosa editada | Todo el post |
| Relevance | Persona real, tarea real, handover, reacción | What I Built + Demo |
| Creativity | Twist (delete button / caja / consent ledger), no "otro RAG" | What I Built + Demo |
| Technical Execution | Harness nombrado, híbrido, citas verificables, eval, injection test, instalación | How I Built It + Code |
| Partner Technology | Gemma 4; Entire/DevRelay; Render sintético si aplica | Prize Categories |
| Core open-source AI | Ollama + Gemma/Qwen + smolagents + BGE-M3 + SQLite; sin nube en el path crítico | How I Built It + Why Open |

### 6.7 Checklist de submission

- [ ] Ventana abierta; fechas y timezone confirmadas.
- [ ] Proyecto nuevo, construido dentro de la ventana; commits post-deadline anotados en README.
- [ ] Post en inglés; tags `devchallenge`, `weekendchallenge`, `hf26challenge` (o los de la edición).
- [ ] Template completo: What I Built, Demo, Code, How I Built It, Why Open, Agent Session, Prize Categories.
- [ ] Demo link o video; repo público; README con quickstart; dataset sintético.
- [ ] Arquitectura, eval, privacy proof, cita del amigo, limitaciones.
- [ ] Categorías de partner listadas solo si se usaron de verdad.
- [ ] Consentimiento del amigo; datos redactados; cita aprobada.
- [ ] Links probados; post proofread; cover image; tags.
- [ ] Submission form completado; post visible; backup del draft/video/repo.

### 6.8 La experiencia del amigo (product spec)

**Onboarding (3 pasos, una pantalla):**
1. "Elegí tu carpeta" (drag-and-drop o file picker).
2. "La indexamos en tu laptop" (progress bar; sin jerga de modelos).
3. "Preguntá lo que quieras" (3 preguntas de ejemplo en sus palabras).

**Pantalla principal:**
- Chat con ejemplos; panel de fuentes a la derecha con página/cláusula y cita exacta.
- Panel de draft con preview y botón "Guardar en Obsidian"; nada se envía solo.
- Badge "Local. Private. Yours." y contador "Network requests: 0" durante la query.
- Botón "Where is my data?" con mapa de archivos; botón "Delete everything" con confirmación y verificación.

**Errores (lenguaje humano + fix):**
- "Ollama no está corriendo" → botón "Iniciar Ollama".
- "No encontré eso en tus documentos" → sugerir reformular o mostrar los documentos más cercanos.
- "Este PDF es una imagen" → explicar que necesita OCR y ofrecer alternativa.
- Nunca un stack trace, nunca un JSON crudo.

**Handover:**
- Guía de una página en PDF/Markdown, con capturas.
- Video de 5 minutos mostrando la tarea real.
- "Qué hacer si se rompe" + ventana de soporte de 2 semanas.
- Acta de consentimiento: qué datos, qué acceso, qué se muestra en el post, cómo borrar, cómo revocar.

**Métricas de éxito:**
- Time-to-first-answer < 30 s (después de indexar).
- Time-to-complete-task < 5 min.
- Número de pedidos de ayuda en la primera sesión (ideal: 0).
- "¿La usarías de nuevo?" (sí/no) + cita textual.
- Antes/después: tiempo de la tarea con el método viejo vs. con el agente.

**Anti-patrones (prohibidos):**
- CLI, Docker Desktop para el amigo, "leé el README", jerga de modelos, requests ocultos, auto-send, datos reales en screenshots.

---

## 7. Por qué estos cambios son mejores (mecanismo, no opinión)

| Cambio | Mecanismo | Criterio que mejora | Efecto esperado |
|---|---|---|---|
| Gate de fecha/eligibilidad | Evita una disqualificación cierta | Relevance/compliance | No se pierde el trabajo en un premio cerrado. |
| Post en inglés | Cumple la regla de elegibilidad | Writing Quality | Sin esto, no hay premio posible. |
| Amigo específico | La historia se vuelve única e irrepetible | Relevance + Creativity + Writing | El juez recuerda a la persona, no el stack. |
| Una modalidad, una acción | Reduce el scope a lo que entra en 72 h | Technical Execution + Asymmetry | Se termina con calidad en vez de quedar a medias. |
| Modelo actual + harness nombrado | Tool calling confiable; cumple el core | Technical + Core open-source | Demo que no se rompe; arquitectura legible. |
| SQLite + híbrido + chunking por cláusula | Menos piezas; mejores citas; borrado simple | Parsimony + Technical | Citas exactas y historia de soberanía coherente. |
| Verificación determinística | Convierte la cita en una garantía | Resistance + Technical | El juez puede reproducir la validación. |
| Eval de 18 preguntas | Convierte "funciona" en evidencia | Writing + Technical | Tabla creíble; honestidad; iteración. |
| Privacy proof + delete button | Demuestra la tesis, no la declara | Creativity + Relevance | El GIF más memorable del post. |
| UI para el amigo | El amigo es el usuario, no el builder | Relevance + Technical | El demo muestra a la persona real. |
| 30-40% del tiempo al post | Alinea el esfuerzo con el criterio de mayor peso | Writing Quality | Post editado, no apurado. |
| Partner mapping | Captura valor opcional sin contaminar la historia | Partner Technology | $100-$200 adicionales posibles. |
| Repo/demo reproducible | Permite verificar el trabajo | Technical + Open-source | Un juez puede correrlo en 5 min. |
| Security/threat model | Un agente con datos personales debe resistir | Resistance | Menos riesgo de una demo vergonzosa. |
| Cut lines | Protegen el critical path | Asymmetry + Resistance | Se termina lo importante. |

---

## 8. Cierre

El roadmap actual tiene una intuición correcta y una ejecución equivocada. La intuición —IA local, datos privados, una persona real— es exactamente lo que el challenge premia. La ejecución —cinco fases abstractas, tres modalidades, un stack de buzzwords, una UI inexistente, un post en español y una ventana cerrada— no puede ganar.

El plan corregido hace tres cosas que el original no hace:
1. **Elige.** Un amigo, una tarea, una modalidad, un modelo, un harness, una acción, un twist.
2. **Prueba.** Eval, citas verificables, privacy proof, injection test, test con el amigo.
3. **Alinea el esfuerzo con el score.** Writing Quality es el criterio de mayor peso; el post recibe el 30-40% del tiempo y se escribe en inglés.

Si tuviera que resumirlo en cinco decisiones:
1. **No construyas para un premio cerrado.**
2. **No escribas en español un challenge que exige inglés.**
3. **No hagas un RAG genérico; hacé el agente de una persona específica con un twist demostrable.**
4. **No uses Gemma 2 ni Chroma/FAISS por inercia; usá Gemma 4/Qwen3.5 + SQLite + smolagents.**
5. **No dejes el post para el final; el post es el producto.**

_El Critic no busca el error, busca la excelencia. Este roadmap no la alcanza; el corregido tiene una chance._
