# Learnings - pipeline-agentes

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## 2026-08-12 - soporteml-v3: modelo cloud de IA en loops + decisión Storybook

**Context:** Sesión de integración MeLi + port de diseño en soporteml-v3. El sync mock llamaba a la IA real (modelo cloud) por cada pregunta, y el frontend lo veía como "paso eterno".

**Lesson - un loop que llama a IA con modelo cloud puede tardar decenas de segundos sin feedback:**
- El sync mock hacía 5 preguntas × 2 llamadas a Ollama (categorizar + sugerir) en serie. Con modelo cloud (`deepseek-v4-flash:cloud`), cada llamada ~4s → ~40s total. El frontend lo mostraba como colgado (HTTP 000, timeout).
- **Fix:** en modo mock/dev, usar un fallback determinístico (categorización por keywords, respuestas plantilla) en vez de la IA real. La IA real queda solo para el flujo real (token conectado). El sync pasó de ~40s a ~6ms.
- Regla generalizable: si un loop llama a IA, (1) usar fallback determinístico cuando el objetivo es dev/mock/demo, (2) considerar concurrencia o timeout por llamada, (3) medir el tiempo total antes de asumir que "funciona".

**Lesson - Storybook no aporta para equipo de 1 dev:**
- Evalué agregar Storybook para documentar el design system. Decisión: no vale la pena. Storybook brilla con varios devs + diseñador (catálogo compartido); con un solo dev que además escribe los componentes, el costo de mantenimiento (stories, providers, config) supera el beneficio.
- **Alternativa elegida:** un "playground" de componentes (`src/pages/Playground.tsx`, solo en dev con `import.meta.env.DEV`) que lista los componentes con variantes. Cubre ~80% del valor de Storybook sin infraestructura.
- Regla: Storybook (o catálogo visual) se agrega cuando el diseño necesita ser revisado por otro humano (diseñador, cliente) o el equipo crece. Para 1 dev, el playground es suficiente.

**Self-reflection:**
- CONTEXT: integración + diseño en proyecto propio
- REFLECTION: el bug del sync "eterno" fue un buen catch - no asumí que era un cuelgue de red, investigué y encontré que era la IA cloud en serie. El port de diseño de v1 fue eficiente (extraer código real de v1 en vez de reimplementar desde las guías).
- LESSON: en proyectos con IA, el fallback determinístico para dev/mock no es opcional - es la diferencia entre una app usable y una que parece colgada. Y para decisiones de infra (como Storybook), pensar en el tamaño del equipo antes de agregar.
- BIASES DETECTED: none (el diagnóstico del sync fue sistemático, no asumí).

---

## 2026-08-14 - Cross-review multi-ronda con agentes paralelos atrapa bugs reales

**Context:** Desarrollo del backlog B1-B7 de kanam-story con pipeline multi-agente: orquestador (Kanam) divide en items, agentes A (VS Code) y B (ZCode) desarrollan en paralelo y se revisan mutuamente (cross-review multi-ronda).

**Resultado:** el cross-review atrapo **8 bugs reales** que los autores no vieron en self-review:
- Orden de sync (U5): sincronizaba la biblia vieja antes de regenerar.
- vfs_fonts (B3): PDF crasheaba por asumir shape `{pdfMake:{vfs}}` cuando es mapa plano.
- Race condition (B4): updateScene sin await + read-modify-write concurrente perdia cambios.
- Anti-flash anulado (B5): el effect de tema corria con default 'dark' antes de cargar settings, pisando el tema persistido.
- 2 bugs de streaming (B7): cierre de dialogo caia al final del doc; chunk con solo whitespace no reemplazaba seleccion.
- CI: jsdom 30 + Node 20 rompia (markAsUncloneable ausente) - el CI usaba Node 20 pero el proyecto corre en Node 22.

**Leccion:** el self-review del autor falla sistematicamente porque el autor asume que su codigo es correcto. Un revisor con ojos frescos detecta los supuestos rotos. El cross-review multi-ronda (cada agente revisa al otro + rondas de correccion) es mas fuerte que una sola pasada. Formalizado en la skill `agent-orchestration-pipeline`. Valor: el codigo mergeado a main pasa por 2+ rondas antes de publicarse.

**Advertencia:** discrepancia de versiones dev/CI (Node 20 vs 22) es fuente clasica de "pasa local, falla en CI". Alinear con `.nvmrc` + CI.

---

## 2026-08-21 - El cross-review puede INTRODUCIR bugs, no solo atraparlos

**Context:** SoporteML V4 U7 (métricas de visitas de MeLi). El Agente A implementó `getItemVisits` parseando la respuesta como objeto plano `{ total_visits }` (correcto según la doc oficial). El Agente B, en su cross-review, "corrigió" el parseo asumiendo que la API devuelve un array `[{ id, total_visits }]` - sin verificar la doc real. El fix de B habría roto las visitas en producción (siempre 0).

**Resultado:** el orquestador (Kanam) verificó contra la doc oficial de MeLi (objeto plano, confirmado) y revirtió el parseo de B (commit `99a010e`), conservando la mejora válida de B (try/catch aislado). Luego hizo el parseo **defensivo** (`extractVisits`) que tolera objeto, array y mapa - 11 tests unitarios.

**Leccion:** el cross-review NO es infalible. Un revisor puede **introducir** una regresión basándose en una suposición falsa sobre el formato de una API externa, en vez de verificar. El orquestador debe:
1. **Verificar contra la fuente real** (doc de la API, spec, o probar el endpoint) antes de aceptar un fix de un agente - no confiar en el veredicto del revisor.
2. Distinguir las mejoras válidas del fix de un agente (puede mezclar lo bueno con lo roto) - conservar lo válido, revertir lo incorrecto.
3. Cuando no se pueda validar empíricamente (sin token/datos reales), hacer el código **defensivo** para los formatos posibles y cubrirlo con tests.

**Biases detectados:** anchoring del revisor (asumió el array por un patrón visto antes sin confirmar) + confirmation del autor (no defendió su parseo correcto porque el revisor "tenía razón").

---

## 2026-08-21 - Delegar a Qwen Code SIEMPRE, incluso en demos (buenas prácticas como prácticas)

**Context:** SoporteML V4. Hice yo mismo la edición de código (timeout en MeliClient, refactor del sync, etc.) en lugar de delegar a Qwen Code. Gonzo me señaló: "por qué estás editando tú en lugar de usar Qwen Code?" y luego "las buenas prácticas deben ser siempre prácticas".

**La lección - la costumbre de delegar se construye delegando siempre:**
- El patrón correcto es: Kanam (orquestador) redacta las tareas, Qwen Code es el agente implementador, y yo verifico contra la fuente real. No edito el código yo mismo.
- **No hay atajo válido.** Aunque la tarea sea "chica" o "solo una demo", se delega. Delegar solo en tareas grandes NO construye la costumbre - la construye delegar en todas.
- Cuando ofrecí "hacerlo yo rápido (3 líneas)", Gonzo lo corrigió: la buena práctica es práctica siempre, no solo cuando conviene.

**Refinamiento del pipeline A/B con delegación real (hoy, válido):**
- Agente A (deepseek-v4-flash): modificó `dev/setup` para reusar la empresa con token.
- Cross-review Agente B (deepseek-v4-flash): detectó que `LIMIT 1` arbitrario devolvía la cuenta propia vacía; lo corrigió ordenando por datos sincronizados.
- El orquestador (yo) verifiqué contra la DB real (lección U7 aplicada): el conteo de Agente B reportó 1150 productos pero el real es 23 - el resultado era correcto pero el reporte tenía un error numérico. Verificar con evidencia, no confiar en el texto del agente.
- Luego Agente A de nuevo: fix de membership activa (el primer fix devolvía userId null y el authMiddleware rechazaba 403).

**Self-reflection:**
- CONTEXT: edición de código en SoporteML V4 + delegación a Qwen
- REFLECTION: mi instinto de "resolver rápido yo" es fuerte, pero rompe el patrón delegado y el rol de orquestador. Gonzo tiene razón: la disciplina se mantiene siempre.
- LESSON: delegar a Qwen Code SIEMPRE (features, demos, fixes chicos). Kanam redacta la tarea, encadena A/B, verifica contra la fuente real. Nunca editar el código directamente salvo orquestación de infra/tests.
- BIASES DETECTED: effort-optimization (opté por hacerlo yo porque "era más rápido" - subestimé el costo de no construir la costumbre).

---

## Cross-review A/B atrapa bugs de layout que Kanam no vio

En el rework del PR #10517 (react-spectrum, SR focus indicator), el Agente B detecto 3 bugs reales que yo no vi: (1) tests de browser falsos positivos - el input absolute+inset:0 sin position:relative en el label se estira al viewport, no al componente, y el test pasaba por la razon equivocada; (2) test de Radio media el label equivocado (querySelector('label') devuelve el <Label>Test</Label> que precede al del Radio, no el del Radio); (3) el fix requiere position:relative en el label (contenedor posicionado) que no estaba documentado. Todos verificados contra la fuente real. Leccion: los tests de layout en jsdom son falsos positivos - solo el browser real valida (getBoundingClientRect). Y el cross-review del pipeline A/B es valioso cuando se verifica cada hallazgo contra la fuente real, no confiando ciegamente en el veredicto del agente. Bias detectado: confirmation bias - asumi que el approach funcionaba porque mi verificacion standalone usaba position:relative en el label, sin darme cuenta de que el componente real no lo tiene.

**Tags:** layout,jsdom,browser,cross-review,falsos-positivos

---

## 2026-08-27 - MiniMax M3: setup costoso + agente se desvia fuera de scope

Prueba de MiniMax M3 como modelo de los agentes A/B (pedido de Gonzo). El setup/ajuste consume tiempo y el agente se desvio fuera de scope: reformateo files.ts (prohibido tocar) + dejo una carpeta .qwen/ en el proyecto. Se rescat el trabajo valido y se revirtio el desvio. El modelo default sigue siendo deepseek-v4-flash:cloud - no cambiar el motor del pipeline sin necesidad real, y al probar otro modelo acotar el scope del agente con mas fuerza.

**Tags:** minimax,modelo,desvio-scope,deepseek

---

## 2026-08-27 - Cross-review atrapo bug de default URL: host.docker.internal en analyzer que corre en el host

El agente B del cross-review detecto que lib/analyzer.ts usaba DEFAULT_OLLAMA_URL = host.docker.internal:11434, pero el analyzer corre en el HOST (next dev del orquestador), no dentro de un container, asi que ese hostname no resuelve y SIEMPRE caia al fallback. El wiring de U2 era correcto; el bug era del default de Fase A. Fix: localhost:11434 + override via OLLAMA_BASE_URL/OLLAMA_URL. Valida el modelo: el orquestador en MAX verifica contra la fuente real, no confia en el veredicto del agente.

**Tags:** cross-review,default-url,host.docker.internal,analyzer,host-vs-container

---

## 2026-08-27 - Validar formato UIMessage antes de escribir conversaciones

En Fase C el agente B sobrescribio una conversacion real (kanam-story 'hola', 120B) al probar con formato UIMessage incorrecto (content en vez de parts). No es repo git, irrecuperable. Se restauro a estado coherente. Regla: validar el formato del mensaje antes de persistir data real - los agentes pueden escribir sobre data real si no se valida el formato.

**Tags:** uimessage,formato,persistencia,data-real,agentes

---

## 2026-08-27 - Arquitectura rollup: vitest corre DENTRO del contenedor, no en el host

El npm install se hace dentro del contenedor Docker, asi el node_modules tiene binarios Linux (rollup-linux-arm64-musl). El agente corre vitest DENTRO del contenedor (funciona 28/28). Correr vitest desde el host de macOS falla con 'Cannot find module @rollup/rollup-darwin-arm64' - esperado, no es bug. Leccion: entender en que entorno corre cada cosa antes de debuggear.

**Tags:** rollup,vitest,contenedor,docker,arquitectura

---

## Review de PR ajeno #9869 (Tearsheet next layers): preguntamos por el comportamiento que el diff eliminaba (ModalBody -> div pelado, se perdia role=region/tabIndex/aria-label para contenido scrolleable). El autor lo restauro pasando level={0} explicito a ModalBody.

En review de PR ajeno, revisar el diff por lo que ELIMINA, no solo por lo que agrega. El comportamiento que se pierde al reemplazar un primitivo del design system por un elemento pelado es el hallazgo de mayor valor: el autor de #9869 restauro ModalBody por esa pregunta.

**Tags:** reflexion-post-tarea,review

---

## 2026-09-11 - kanam-tetris v0.2: review con harness instrumentado > review de lectura

Ciclo A/B de kanam-tetris v0.2 con deepseek-v4.1-flash. El Agente B no leyo el codigo y opino: construyo un harness instrumentado en Node y reprodujo los bugs con evidencia de ejecucion (timers medidos, conteo de celdas antes/despues). Encontro dos criticos que un review de lectura no habria cazado: (1) falta de guard del estado 'clearing' durante el flash de limpieza - mantener Espacio reseteaba el timer y congelaba la limpieza para siempre, y una flecha + Espacio estampaba bloques fantasma con score duplicado (invisible porque draw() suprime la pieza activa durante el flash); (2) lookup de wall kicks CCW espejado, PREEXISTENTE desde v0.1 - la tabla tenia las 8 filas correctas pero el indice leia la fila CW de la transicion inversa. Regla: cuando el bug depende de tiempo (timers, ventanas de input, estado transitorio), el reviewer debe EJECUTAR, no leer. Y cuando se revisa una base, revisar el INDICE/lookup, no solo los datos que indexa - el bug de v0.1 vivia en el indice, no en la tabla.

**Tags:** cross-review,verificacion,harness,testing,tetris,pipeline-ab,v4.1

---

## 2026-09-11 - deepseek-v4.1-flash validado como motor del pipeline A/B

Primer uso real de deepseek-v4.1-flash:cloud como motor de los agentes A/B (via Claude Code apuntando al gateway Ollama 127.0.0.1:11434), aplicando la pausa obligatoria del AGENTS.md (planifica MAX -> A escribe HIGH -> B revisa HIGH -> iterar -> revision final Kanam MAX -> push -> borrador). Resultado: ciclo completo sin intervencion de Kanam en el medio. El Agente A implemento 6 features complejas (hold, lock delay con cap, DAS/ARR, flash, pausa, high score) y SE AUTOCAZO un bug propio (Escape nunca pausaba por comparacion case-sensitive) - la autoverificacion del motor es un indicador de calidad. El Agente B produjo el mejor review del experimento y ademas declaro con honestidad lo que NO verifico (render/pixeles, alcanzabilidad de un caso de borde). Ambos agentes fueron honestos sobre los limites de su propio trabajo. Conclusion: v4.1 valido como motor de pipeline para tareas de escritura + review.

**Tags:** tetris,pipeline-ab,v4.1,motor,claude-code,ollama,validacion

---

## Revert del motor del pipeline a v4-flash por costo (ADR-046, revierte ADR-045)

El 2026-09-11 el motor de los agentes A/B del pipeline volvio de deepseek-v4.1-flash a deepseek-v4-flash por costo: medido en el uso semanal de Ollama Cloud, v4.1 consumia mas por request que v4 y glm (1.348 requests con la barra mas alta, contra 1.631 de v4 con la mas baja). La mejora de calidad de v4.1 sobre v4 no justificaba el gasto. v4.1 queda como fase de escalada para analisis complejo. El mecanismo real que forzaba v4.1 no era el ADR sino los overrides sticky de model-router.json (code, review, pipeline_ab), reseteados el mismo dia. Lo que NO cambia con el motor: el valor del review por ejecucion (harness instrumentado cuando el bug depende de tiempo) y la autoverificacion del motor - esas lecciones nacieron en el ciclo v0.2 con v4.1 y valen con cualquier modelo. Pendiente: v4 sera retirado en unas semanas (reemplazo por 4.1), reevaluar entonces.

**Tags:** costo,pipeline-ab,v4.1,model-router,v4-flash,adr-046

---

## Conclusion

 No hay correlacion entre costo/tamano del modelo y calidad de respuesta. Todos resolvieron bien el problema. La diferencia es personalidad, no capacidad. Kanam acerto solo 1/8 en identificar los modelos a ciegas.

---

## LECCION DE PROCESO (importante)

 - **Un subagente que tarda NO es un subagente que fallo.** Reporte que el Agente B habia settleado sin entregar reporte y cerre la fase con eso. **Su reporte llego 14 minutos despues** y encontro los 2 defectos criticos (race + falso exito) que MI verificacion no vio. Su reproduccion del race (400 unidades vs mis 10) fue mejor. **No cerrar un review por silencio: el settle no implica fracaso.**

---

## La skill langchain-rag-service RECOMIENDA el patron de IDs que tumbo el indice (corregir, no agregar skill nueva)

CONTEXTO: al cerrar la sesion, evaluando si hacia falta una skill nueva para el incidente del indice, revise las skills existentes. Encontre algo mejor que una skill nueva: un error ACTIVO en una skill viva.

HALLAZGO: la skill `langchain-rag-service` (workshop) recomienda en su paso 6, textual:
  `add_documents(chunks, ids=[f"{name}::{i}", ...])`
con el comentario "Deterministic ids make re-ingests overwrite instead of duplicating". El problema: `name` es ambiguo. Si se resuelve al NOMBRE del archivo -que es lo natural- colisiona con homonimos en carpetas distintas. Es EXACTAMENTE el bug que hoy tumbo el indice de kanam-insight: 142 colisiones (docs/README.md vs docs/adr/README.md -> ambos `docs::README.md::0`), Chroma aborto el lote, y el indice quedo a medias.

Es decir: la skill no solo no protege del bug, lo RECOMIENDA. El proximo proyecto RAG que la siga va a repetirlo.

SEGUNDO HALLAZGO: el reference `chroma-store-recovery.md` de la misma skill ya documenta la firma del segfault (EXIT=139 al abrir un segmento HNSW danado, SQLite intacta) y trae una tabla de reproduccion donde la fila "Build 3000 docs while a second process reads (count() in a loop)" figura como **hipotesis, NO reproducida**. Hoy tengo evidencia mas fuerte de que esa es la causa (aunque tampoco en aislamiento: el dano previo por el aborto pudo contribuir). No lo declaro reproducido; anoto que hay un caso mas en la misma direccion.

CORRECCION QUE PROPONGO (para Gonzo, que es quien edita las skills del Workshop):
1. Paso 6: `ids=[f"{name}::{i}"]` -> `ids=[f"{path}::{i}"]`, con la razon escrita: el ID debe salir de la RUTA RELATIVA (unica en el corpus), nunca del nombre del archivo.
2. Agregar el guard previo: validar `len(set(ids)) == len(ids)` ANTES de tocar la coleccion y abortar con el detalle de los colisiones. Sin el guard, Chroma aborta a mitad de lote y deja el indice parcial - y un indice parcial se ve como exito si solo se mira el conteo final.
3. Aclarar que `--reset` no sirve para recuperarse de un store que crashea al abrir (ya lo dice el reference, pero el paso 6 no lo enlaza).

REGLA DE METODO QUE ME LLEVO: antes de proponer una skill nueva para un problema, buscar si alguna skill existente LO RECOMIENDA. Corregir la causa es mas valioso que documentar el sintoma. Y es la misma leccion de hoy desde el otro lado: un verificador (o una guia) con alcance limitado no solo deja pasar el error, a veces lo prescribe.

---

## El experimento que respondio la pregunta clave

 Gonzo pregunto si iterar un modelo barato sin problema de recursos puede competir con los grandes. **gemma + gate convergio**: T7 en 2 iteraciones (795 tokens), T8 en 1 iteracion (1.058 tokens). Y los fixes GENERALIZAN (0 discrepancias en 39.600 combinaciones; 4/4 casos fuera de la suite). **Con el prompt aislado (feedback-only, sin reglas nuevas) tambien convergio** -> el progreso viene del FEEDBACK, no de una spec mas explicita. El modelo incluso razono desde el test ("el descuento debe redon

---

## Módulo 1 de OpenClaw Use Cases: los 5 patrones de entrada conversacional

El Módulo 1 del curso (roadmap.sh) define el embudo de entrada de un agente conversacional en cinco patrones secuenciales:

L1 Triaje: normalizar payloads de cada plataforma a un mensaje canonico, filtrar por reglas deterministas (menciones, comandos) antes de gastar tokens, agrupar mensajes fragmentados con debounce de ventana deslizante y un techo duro (evita buffers eternos), y clasificar con un modelo Tier 1.
L2 Personas (enrutamiento): en vez de un agente monolitico con todas las instrucciones, un clasificador de intencion asigna la consulta a una Persona especializada con su propio set de herramientas. Evita la dilucion del prompt y permite aislar permisos de escritura.
L3 Borradores (staged artifacts): el agente no envia en nombre del usuario; redacta un borrador con una justificacion (rationale) y espera aprobacion humana. Cero suposiciones: si el dato no esta explicito, se pregunta.
L4 Escalacion: no es la alerta. Es el cambio de estado del canal (Atomic Channel Lock): el agente se silencia y entrega el mando al humano. Se dispara por sentimiento, loops repetidos, pedido explicito o fallo critico de herramienta.
L5 Limites de contexto: el contexto se aisla por identidad, canal e hilo; un TTL resetea la memoria inactiva; y el filtro por identidad es DETERMINISTA y va ANTES de cualquier busqueda semantica (nunca al reves, o hay fuga de datos).

Equivalencia en el workspace: L2 = los agentes kanam-dev/ops/mind/studio y la frontera de roles del ADR-083; L4 = el handoff al humano cuando una tarea supera al agente; L5 = heartbeat + scripts de registro de sesion.

---

## L5 (TTL de contexto) es la formalizacion de lo que el heartbeat ya hacia

El TTL de contexto de la L5 del curso (olvido programado de memoria inactiva, reseteo de sesion por inactividad) describe exactamente el rol que cumplen el heartbeat y los scripts de registro del SDLC en el workspace.

La diferencia es de alcance, no de concepto: el curso lo plantea como una politica de memoria en RAM con flush por inactividad; el workspace lo resuelve con persistencia (memory.db) mas un resumen de cierre. En vez de depender de que el modelo recuerde, el estado se escribe a disco y se sintetiza.

Leccion: cuando una teoria externa coincide con una practica ya instalada, la teoria no se adopta como novedad - se usa como lente para auditar y optimizar lo que ya hay. En este caso valida por que los scripts de session-end y el heartbeat son necesarios.

---

## Hallazgos clave

 - **El core de OpenClaw está más completo de lo que pensábamos.** Dos repos (MCP adapter `androidStern-personal`, MCP server `Helms-AI`) resultaron **redundantes**: el core ya expone y consume MCP nativo (`mcp.servers`, `openclaw mcp add` / `mcp serve`, transportes stdio/SSE/Streamable HTTP, policy integrada, `openclaw mcp doctor --probe`). Verificado contra `la doc del paquete npm de OpenClaw (referencia externa)` del paquete npm. - **Hallazgo transversal:** tres candidatos distintos (Claw Orchestrator, MemoV, ClawSec) resuelven e

---

## TRUCO CLAVE (lo que se atascaba)

 - `/api/generate` con modelos grandes (12b/24b) y prompt largo + **context_length huge por defecto (1M tokens del 12b)** → se **atasca en "load"** (timeout exit 28, RAM se satura). - **Solución:** pasar `options.num_ctx` **pequeño** (2048 o 4096) vía `/api/chat` o `/api/generate`. Con `num_ctx:4096` el 12b respondió bien (4362 bytes PLANO, exit=0). - Prompt para la cata: `/tmp/cata-juez.md` (prompt de JUEZ estricto, escala 1-5, 4 dims, crítico). - Dimensión PLANO aprobada: prompt FastAPI market

---

## Regla de oro aprendida

 - Para cata con Ollama local: **`curl` directo a `/api/chat`** con `options.num_ctx` limitado (2048-4096), `stream:false`, secuencia estricta (un modelo a la vez). No usar `/api/generate` con context default en modelos grandes. # Memory 2026-10-04 ## Context & Decisions - **Status:** Session cleared. No active tasks or sub-agents. - **Identified Pending:** `kanam-os` (contrast guard), `kanam-pulse` (long-term), and the novel "Quienes Quedan". - **GitHub Status:** Verified clean (no new PRs, iss

---

