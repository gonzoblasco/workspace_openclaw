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

**Tags:** soporteml-v3: modelo cloud de IA en loops + decisión Storybook

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

**Tags:** Cross-review multi-ronda con agentes paralelos atrapa bugs reales

---

## 2026-08-21 - El cross-review puede INTRODUCIR bugs, no solo atraparlos

**Context:** SoporteML V4 U7 (métricas de visitas de MeLi). El Agente A implementó `getItemVisits` parseando la respuesta como objeto plano `{ total_visits }` (correcto según la doc oficial). El Agente B, en su cross-review, "corrigió" el parseo asumiendo que la API devuelve un array `[{ id, total_visits }]` - sin verificar la doc real. El fix de B habría roto las visitas en producción (siempre 0).

**Resultado:** el orquestador (Kanam) verificó contra la doc oficial de MeLi (objeto plano, confirmado) y revirtió el parseo de B (commit `99a010e`), conservando la mejora válida de B (try/catch aislado). Luego hizo el parseo **defensivo** (`extractVisits`) que tolera objeto, array y mapa - 11 tests unitarios.

**Leccion:** el cross-review NO es infalible. Un revisor puede **introducir** una regresión basándose en una suposición falsa sobre el formato de una API externa, en vez de verificar. El orquestador debe:
1. **Verificar contra la fuente real** (doc de la API, spec, o probar el endpoint) antes de aceptar un fix de un agente - no confiar en el veredicto del revisor.
2. Distinguir las mejoras válidas del fix de un agente (puede mezclar lo bueno con lo roto) - conservar lo válido, revertir lo incorrecto.
3. Cuando no se pueda validar empíricamente (sin token/datos reales), hacer el código **defensivo** para los formatos posibles y cubrirlo con tests.

**Biases detectados:** anchoring del revisor (asumió el array por un patrón visto antes sin confirmar) + confirmation del autor (no defendió su parseo correcto porque el revisor "tenía razón").

**Tags:** El cross-review puede INTRODUCIR bugs, no solo atraparlos

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

**Tags:** Delegar a Qwen Code SIEMPRE, incluso en demos (buenas prácticas como prácticas)

---

## Cross-review A/B atrapa bugs de layout que Kanam no vio

En el rework del PR #10517 (react-spectrum, SR focus indicator), el Agente B detecto 3 bugs reales que yo no vi: (1) tests de browser falsos positivos - el input absolute+inset:0 sin position:relative en el label se estira al viewport, no al componente, y el test pasaba por la razon equivocada; (2) test de Radio media el label equivocado (querySelector('label') devuelve el <Label>Test</Label> que precede al del Radio, no el del Radio); (3) el fix requiere position:relative en el label (contenedor posicionado) que no estaba documentado. Todos verificados contra la fuente real. Leccion: los tests de layout en jsdom son falsos positivos - solo el browser real valida (getBoundingClientRect). Y el cross-review del pipeline A/B es valioso cuando se verifica cada hallazgo contra la fuente real, no confiando ciegamente en el veredicto del agente. Bias detectado: confirmation bias - asumi que el approach funcionaba porque mi verificacion standalone usaba position:relative en el label, sin darme cuenta de que el componente real no lo tiene.

**Tags:** layout, jsdom, browser, cross-review, falsos-positivos

---

## 2026-08-27 - MiniMax M3: setup costoso + agente se desvia fuera de scope

Prueba de MiniMax M3 como modelo de los agentes A/B (pedido de Gonzo). El setup/ajuste consume tiempo y el agente se desvio fuera de scope: reformateo files.ts (prohibido tocar) + dejo una carpeta .qwen/ en el proyecto. Se rescat el trabajo valido y se revirtio el desvio. El modelo default sigue siendo deepseek-v4-flash:cloud - no cambiar el motor del pipeline sin necesidad real, y al probar otro modelo acotar el scope del agente con mas fuerza.

**Tags:** minimax, modelo, desvio-scope, deepseek

---

## 2026-08-27 - Cross-review atrapo bug de default URL: host.docker.internal en analyzer que corre en el host

El agente B del cross-review detecto que lib/analyzer.ts usaba DEFAULT_OLLAMA_URL = host.docker.internal:11434, pero el analyzer corre en el HOST (next dev del orquestador), no dentro de un container, asi que ese hostname no resuelve y SIEMPRE caia al fallback. El wiring de U2 era correcto; el bug era del default de Fase A. Fix: localhost:11434 + override via OLLAMA_BASE_URL/OLLAMA_URL. Valida el modelo: el orquestador en MAX verifica contra la fuente real, no confia en el veredicto del agente.

**Tags:** cross-review, default-url, host.docker.internal, analyzer, host-vs-container

---

## 2026-08-27 - Validar formato UIMessage antes de escribir conversaciones

En Fase C el agente B sobrescribio una conversacion real (kanam-story 'hola', 120B) al probar con formato UIMessage incorrecto (content en vez de parts). No es repo git, irrecuperable. Se restauro a estado coherente. Regla: validar el formato del mensaje antes de persistir data real - los agentes pueden escribir sobre data real si no se valida el formato.

**Tags:** uimessage, formato, persistencia, data-real, agentes

---

## 2026-08-27 - Arquitectura rollup: vitest corre DENTRO del contenedor, no en el host

El npm install se hace dentro del contenedor Docker, asi el node_modules tiene binarios Linux (rollup-linux-arm64-musl). El agente corre vitest DENTRO del contenedor (funciona 28/28). Correr vitest desde el host de macOS falla con 'Cannot find module @rollup/rollup-darwin-arm64' - esperado, no es bug. Leccion: entender en que entorno corre cada cosa antes de debuggear.

**Tags:** rollup, vitest, contenedor, docker, arquitectura

---

## Review de PR ajeno #9869 (Tearsheet next layers): preguntamos por el comportamiento que el diff eliminaba (ModalBody -> div pelado, se perdia role=region/tabIndex/aria-label para contenido scrolleable). El autor lo restauro pasando level={0} explicito a ModalBody.

En review de PR ajeno, revisar el diff por lo que ELIMINA, no solo por lo que agrega. El comportamiento que se pierde al reemplazar un primitivo del design system por un elemento pelado es el hallazgo de mayor valor: el autor de #9869 restauro ModalBody por esa pregunta.

**Tags:** review,reflexion-post-tarea

---

## 2026-09-11 - kanam-tetris v0.2: review con harness instrumentado > review de lectura

Ciclo A/B de kanam-tetris v0.2 con deepseek-v4.1-flash. El Agente B no leyo el codigo y opino: construyo un harness instrumentado en Node y reprodujo los bugs con evidencia de ejecucion (timers medidos, conteo de celdas antes/despues). Encontro dos criticos que un review de lectura no habria cazado: (1) falta de guard del estado 'clearing' durante el flash de limpieza - mantener Espacio reseteaba el timer y congelaba la limpieza para siempre, y una flecha + Espacio estampaba bloques fantasma con score duplicado (invisible porque draw() suprime la pieza activa durante el flash); (2) lookup de wall kicks CCW espejado, PREEXISTENTE desde v0.1 - la tabla tenia las 8 filas correctas pero el indice leia la fila CW de la transicion inversa. Regla: cuando el bug depende de tiempo (timers, ventanas de input, estado transitorio), el reviewer debe EJECUTAR, no leer. Y cuando se revisa una base, revisar el INDICE/lookup, no solo los datos que indexa - el bug de v0.1 vivia en el indice, no en la tabla.

**Tags:** cross-review,harness,testing,tetris,pipeline-ab,v4.1,verificacion

---

## 2026-09-11 - deepseek-v4.1-flash validado como motor del pipeline A/B

Primer uso real de deepseek-v4.1-flash:cloud como motor de los agentes A/B (via Claude Code apuntando al gateway Ollama 127.0.0.1:11434), aplicando la pausa obligatoria del AGENTS.md (planifica MAX -> A escribe HIGH -> B revisa HIGH -> iterar -> revision final Kanam MAX -> push -> borrador). Resultado: ciclo completo sin intervencion de Kanam en el medio. El Agente A implemento 6 features complejas (hold, lock delay con cap, DAS/ARR, flash, pausa, high score) y SE AUTOCAZO un bug propio (Escape nunca pausaba por comparacion case-sensitive) - la autoverificacion del motor es un indicador de calidad. El Agente B produjo el mejor review del experimento y ademas declaro con honestidad lo que NO verifico (render/pixeles, alcanzabilidad de un caso de borde). Ambos agentes fueron honestos sobre los limites de su propio trabajo. Conclusion: v4.1 valido como motor de pipeline para tareas de escritura + review.

**Tags:** pipeline-ab,v4.1,motor,claude-code,ollama,tetris,validacion

---

## Revert del motor del pipeline a v4-flash por costo (ADR-046, revierte ADR-045)

El 2026-09-11 el motor de los agentes A/B del pipeline volvio de deepseek-v4.1-flash a deepseek-v4-flash por costo: medido en el uso semanal de Ollama Cloud, v4.1 consumia mas por request que v4 y glm (1.348 requests con la barra mas alta, contra 1.631 de v4 con la mas baja). La mejora de calidad de v4.1 sobre v4 no justificaba el gasto. v4.1 queda como fase de escalada para analisis complejo. El mecanismo real que forzaba v4.1 no era el ADR sino los overrides sticky de model-router.json (code, review, pipeline_ab), reseteados el mismo dia. Lo que NO cambia con el motor: el valor del review por ejecucion (harness instrumentado cuando el bug depende de tiempo) y la autoverificacion del motor - esas lecciones nacieron en el ciclo v0.2 con v4.1 y valen con cualquier modelo. Pendiente: v4 sera retirado en unas semanas (reemplazo por 4.1), reevaluar entonces.

**Tags:** pipeline-ab,v4-flash,v4.1,adr-046,costo,model-router

---

