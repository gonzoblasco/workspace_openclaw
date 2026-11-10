# Clase: Codex & AI Coding Agents — Learn Agentic Coding

- Fuente: https://www.youtube.com/watch?v=ajfQWhGQGLE
- Canal: Scrimba (freeCodeCamp en YouTube)
- Expositor: Tom Chant, Head of Education en Scrimba
- Duración: 1:50:43 (6643 s)
- Idioma: inglés · Transcript: `transcripcion.md` (ASR, 2.968 cues)
- Curso interactivo: https://scrimba.com/learn-agentic-coding-c0g68l84pg — el código de cada lección vive ahí, no en el video
- Clase creada: 2026-11-10

## Por qué esta clase importa para Gonzo

El curso enseña exactamente lo que ya se práctica en este workspace — AGENTS.md, skills, plan mode, characterization tests, permisos — pero desde la óptica de Codex y con una diferencia útil: **el curso pone el énfasis en el criterio de verificación**, no en la herramienta. Sirve de tres formas:

1. **Contraste externo** con la metodología propia (pipeline A/B, gates de verificación, plan mode del Planner).
2. **Vocabulario estándar** que el mercado usa en entrevistas: plan mode, characterization tests, red/green de TDD, sandbox_mode, approval policy, MCP.
3. **Material para clase**: los ejercicios se pueden re-correr acá con los agentes del workspace.

## Resultado esperado

Al terminar la clase, se puede:

1. Escribir un prompt con contexto + resultado esperado + restricciones, y distinguirlo de un comentario-prompt (`// TODO for AI`).
2. Configurar instrucciones persistentes con AGENTS.md en tres scopes (global, proyecto, carpeta) y explicar la precedencia.
3. Usar plan mode para tareas ambiguas: pedir el plan, criticarlo, agregar edge cases, recién después implementar.
4. Escribir una skill reproducible (tarea + propósito + formato + knowledge capture) y decidir cuándo es una skill y cuándo es un prompt.
5. Proteger código legacy con characterization tests antes de refactorizar, y distinguirlos de tests de especificación (TDD).
6. Mantener Git limpio: commits chicos, revisión de diffs, separación de config files por herramienta.
7. Evitar que el agente exponga secretos: `.env` + `.gitignore`, nunca loggear claves, revisar diffs antes de commitear.
8. Ajustar permissions (approval policy + sandbox_mode) y `config.toml`, entendiendo el riesgo de cada nivel.
9. Conectar un MCP server (shadcn) y explicar el loop agente → server → resultado → criterio.

## Cómo se usa esta clase

No es un resumen para leer de corrido: es el **esqueleto** de una sesión de estudio conmigo. El modo que funciona:

1. Elegís un módulo del mapa temporal.
2. Yo te doy la lección corta (5-8 min) con las citas y los timestamps para que verifiques en el video.
3. Vamos a las preguntas de ese módulo del banco.
4. Si hay ejercicio, lo hacés sobre un proyecto real tuyo del workspace y yo reviso el entregable.
5. Al cerrar el módulo anoto un párrafo en `memory/YYYY-MM-DD.md` con lo que quedó y lo que falta.

**Ojo con el orden:** M1-M5 construyen el andamiaje (prompt → instrucciones → plan → skills), M6-M7 son verificación, M8-M9 son seguridad, M10-M12 son control del entorno, M13 es tools externas. Se puede saltear M10 si no vas a usar Codex concreto.

## Mapa temporal

Fuente primaria: el índice de capítulos de la descripción oficial del video.

| Tiempo | Bloque | Módulo |
|---|---|---|
| 0:00:00 | Intro to Agentic Coding | M1 |
| 0:04:58 | Intro to the Course | M1 |
| 0:09:34 | Prompting Basics | M2 |
| 0:15:09 | Comment Prompts | M2 |
| 0:19:42 | Two Problems | M3 |
| 0:23:39 | Initialising a Project | M3 |
| 0:26:48 | Multiple AGENTS.md files | M3 |
| 0:28:46 | Plan Mode | M4 |
| 0:36:35 | Skills Fundamentals | M5 |
| 0:40:36 | Skills challenge 1 | M5 |
| 0:44:58 | Skills Challenge 2 | M5 |
| 0:47:19 | Skills Challenge 2 Solution | M5 |
| 0:50:33 | Testing set up | M6 |
| 0:55:17 | Characterisation test challenge | M6 |
| 1:01:13 | Testing pitfalls | M6 |
| 1:05:24 | Test Driven Development | M7 |
| 1:11:09 | Git Hygiene | M8 |
| 1:13:49 | Version control & config files | M8 |
| 1:15:58 | Secrets | M9 |
| 1:22:54 | VS Code Codex Extension | M10 |
| 1:26:46 | Context | M11 |
| 1:29:33 | Context Management | M11 |
| 1:34:20 | Permissions | M12 |
| 1:36:09 | config.toml | M12 |
| 1:39:46 | config.toml challenge | M12 |
| 1:43:50 | MCP setup | M13 |
| 1:46:44 | MCP shadcn | M13 |

## Módulos

### Módulo 1 — Qué es agentic coding (0:00 – 9:34)

**Objetivo:** definir "agente" por su capacidad de **cerrar el loop** (actuar → verificar resultado → iterar), no por el modelo.

- El agente tiene autonomía para: leer y editar archivos, escribir código, correr comandos y tests, iterar hasta que la tarea está satisfactoria, y usar tools.
- *Cita (1:18):* "agentic refers to the capacity to make decisions and adapt based on feedback from the results of its own actions... it's basically closing the loop between writing code and verifying that it works."
- Los tres riesgos del agente: **expone secretos**, **expone datos de cliente**, **genera apps que no funcionan**; y en calidad: código mediocre, difícil de mantener, mal documentado.
- *Cita (2:55):* "human input is not just desirable, it's a necessity." — de la ideación al deploy.
- Comparación de herramientas: Codex, Claude Code, Copilot, Devin, Windsurf, Cursor. El agente es **una categoría**, no una empresa.
- Tres formas de uso: **CLI** (terminal), **IDE** (VS Code y similares), **desktop/web**; el mismo agente suele estar en varias. El curso usa la IDE por cercanía al código.

**Ejercicio:** escribir en 3 líneas qué hace un agente que un "chat que escribe código" no hace, y nombrar el momento exacto en que el agente verifica su propio trabajo.

---

### Módulo 2 — Prompting: contexto, resultado y restricciones (9:34 – 19:42)

**Objetivo:** dejar de pedir "lo que querés" y empezar a especificar **qué, con qué, y qué no**.

- Demo: pedir "un botón más" produce **código duplicado** (dos funciones casi iguales, DRY roto). El agente resolvió el pedido literal, no el problema.
- *Cita (12:03):* el prompt bien armado cubre tres áreas: "what the agent's going to do, what the context is, and what the output should look like" — el orden es **task / context / output**.
- El agente imita el patrón **existente** del código, así que el contexto que se le muestra decide la calidad: *"if you show it a small amount of your code, it might be a good idea to show one or two model [examples]"* (11:36–12:00).
- Caveat: *"AI can intuitit a lot... it's definitely not always necessary"* (15:32) — el agente no ve lo que no le mostrás; inferir estilo sin contexto es apostar.
- **Comment prompts:** una instrucción escrita como comentario encima de la función (`// TODO for AI: refactor to async/await`). Ventajas: queda en el código, sirve como brief a futuro, permite "do all of the TODOs" en lote. Se puede marcar con un tag propio para hacer un pedido por lotes.

**Ejercicio:** tomar una función del workspace y escribir un comment-prompt de 5 líneas con contexto + resultado + restricción. Ejecutarlo y comparar el diff contra pedir lo mismo sin contexto.

---

### Módulo 3 — Los dos problemas y las instrucciones persistentes (19:42 – 28:46)

**Objetivo:** entender por qué el contexto de la conversación no alcanza y cómo AGENTS.md lo resuelve.

**Problema 1 — inconsistencia entre personas:** cada integrante le pide al agente distinto, y el estilo se vuelve incoherente (*cita, 21:28: "that makes this code harder to maintain for a team"*).
**Problema 2 — la ventana de contexto:** *"the model will get overwhelmed"* (22:10) y *"the information in it gets truncated and some of it will get lost"* (22:29). La conversación larga no es memoria.

La solución son instrucciones persistentes: `/init` en Codex genera un **AGENTS.md** con lo fundamental del stack, la estructura y las convenciones. Se guarda en el repo, viaja con el proyecto y **sobrevive a la truncación**. Es **cross-tool**: lo leen Codex, Cursor y otros.

**Tres scopes y precedencia:**
1. **Global** (home del usuario, `~/AGENTS.md`): preferencias personales para todos los proyectos.
2. **Proyecto** (raíz del repo): stack, arquitectura, estilo, comandos.
3. **Carpeta** (`specs/AGENTS.md`): convenciones solo para esa subtree.

*Cita (28:19):* "It's going to read the global scope first, then the project scope, and then the folder scope" — el orden de lectura es global → proyecto → carpeta; el más cercano gana donde haya conflicto. Regla práctica: lo que sirve a varios proyectos va global; lo específico, cerca del código.

**Ejercicio:** escribir el AGENTS.md de un proyecto propio con 5 secciones (stack, estructura, estilo, comandos de test, qué no tocar) y justificar cada línea con un caso en que el agente se equivocó por no tenerla.

---

### Módulo 4 — Plan Mode (28:46 – 36:35)

**Objetivo:** usar plan mode para tareas **ambiguas o multipaso**, y no para todo.

- *Caveat explícito (29:09):* "Most people don't need plan mode very often" — la mayoría de las tareas están bien acotadas y no lo necesitan — plan mode no es para cambios lineales.
- Caso del video: sección "recently viewed articles" con persistencia en localStorage. El plan lista archivos a tocar, decisiones (dónde persistir, cuántos ítems) y el impacto.
- El valor: **detectar lo que no especificaste**. *Cita (33:01):* "has it specified where on the [page] it goes? Is it going right at the bottom [or] the header?" — esos huecos se resuelven en el plan, no después del código.
- El loop: pedir el plan → **criticarlo** → pedir edge cases ("¿qué pasa si el artículo se borra después de ser visto?") → el agente **agrega al plan, no al código** → recién ahí implementar.
- La implementación luego va rápido *"because it's done a lot of the planning"* (~35:11).

**Ejercicio:** elegir una feature de 3+ archivos, correr solo el plan, y encontrar por lo menos **dos huecos** antes de dejar implementar. Medir cuánto tardó el plan vs. cuánto el arreglo posterior.

---

### Módulo 5 — Skills (36:35 – 50:33)

**Objetivo:** pasar de prompts repetidos a procedimientos reproducibles.

- Una skill es **un wrapper reusable alrededor de un prompt** que vive en el repo (`.codex/skills/`), no en la conversación.
- Ejemplo mínimo: skill "file tree" — genera el árbol del código y lo escribe en `tree.md`; se invoca con `/` en el chat.
- *Cita (39:37):* "An agent is great at general tasks, but the agent is completely clueless about the specific decisions your team has taken... It doesn't know your house coding and commenting style." Lo que una skill agrega es **conocimiento y opinión**.
- *Cita (39:59):* "we can't assume that information given to the agent in a prompt will always be available to it" — por eso la skill vive en el file system y es portable — la skill no depende del contexto de la sesión y **viaja entre proyectos**.
- **Anatomía de una buena skill** (el template que el curso propone): tarea, propósito, formato de salida, **knowledge capture** (qué mirar del repo antes de actuar), y límites (qué no tocar).
- *Cita (41:54):* "This is where we're going to give it something which it can't possibly know" — el **knowledge capture** apunta al código que define el house style.

**Ejercicio (el "skills challenge 1" del curso):** crear una skill `house-style` que refactorice bucles `for`/`while` a métodos de array, leyendo el estilo del repo. **Entregable:** la skill en disco + un refactor real aplicado con ella.

**Ejercicio 2 (challenge 2):** crear `stylist-dev`, una skill de debug específica del repo: constraints de plataforma, dependencias pinneadas y lista de quirks conocidos. **Entregable:** la skill + un bug resuelto citando qué parte de la skill lo resolvió.

---

### Módulo 6 — Characterization tests (50:33 – 1:05:24)

**Objetivo:** poder cambiar código legacy sin romper lo que ya funciona.

- El código legacy del caso (`scheduler.js`) fue creciendo a lo largo de meses: **nadie entiende qué hace** y cambiarlo rompe cosas en silencio.
- Un characterization test **no testea lo que el código debería hacer: testea lo que hace**, y congela ese comportamiento.
- *Cita (53:10):* el test sirve "to protect the [behavior] during refactor or when adding new [code]".
- Dos partes: (1) el test pasa **antes** de tocar nada, (2) el test corre **automáticamente después de cada cambio**.
- Esa es la regla: si el test sigue verde, el comportamiento está protegido. *Cita (54:35):* el test corre solo después de cada cambio; si queda verde, la feature está protegida.
- **Pitfall central (1:05:24+):** el agente tiende a escribir el test **mirando el código**, no el comportamiento. Un test que replica el bug congela el bug. Hay que **verificar manualmente** qué dice el test antes de aceptarlo, y correrlo en rojo contra un cambio para comprobar que efectivamente detecta algo.
- Pitfall 2: el agente corrió los tests, falló, **cambió el código** en vez de arreglar el test o pedir permiso.

**Ejercicio:** sobre un módulo propio con lógica de fechas/reglas, escribir un characterization test con un caso por regla (feriado, borde, solapamiento). **Entregable:** tests verdes antes y después de un refactor, con un commit intermedio que rompa el comportamiento y las pruebas de que el test lo detecta.

---

### Módulo 7 — TDD con agentes (1:05:24 – 1:11:09)

**Objetivo:** invertir el orden y usar el test como **especificación**.

- En el módulo anterior, el agente escribió código y test; en el test de descuento encontró un caso de **redondeo** (276.97: ¿redondear el total o cada ítem?) que era **una decisión de negocio**, no de implementación.
- *Cita (1:04:59):* "don't ask the agent to write code and create tests for it in the same pass" — y *(1:11:00, ~1:05:17)* "this is an agent looking in the mirror. It didn't encode a wrong answer. It encoded an answer [nobody decided]". El agente no debe decidir la política.
- **TDD:** especificar el test primero (descuento de 15% sobre `SMILE15`, redondeo **a dos decimales al final**), correrlo en **rojo (red)**, y pedirle al agente que haga pasar el test. El test fallido es el objetivo.
- *Cita (1:08:28):* "the test is failing as expected... this is what [we call] the red phase".
- El agente agrega casos de borde por su cuenta (case sensitivity, inputs inválidos) — eso está bien **si** se revisan.
- Caveat final: el agente produce **tests basura en cantidad**. *Cita (1:10:0x):* "sloppy, quick, lazy prompts do get you a [bad result]... as long as you're aware of [that], have the agent write [from] a specification" — es más confiable.

**Ejercicio:** tomar una regla de negocio (descuento, impuesto, límite) y escribir el test **antes**, incluyendo el redondeo explícito. Pedirle al agente solo hacerlo pasar. **Entregable:** el test que falló primero, el commit del código, y una nota de qué decisión tomó el test y no el agente.

---

### Módulo 8 — Git hygiene y config files (1:11:09 – 1:15:58)

**Objetivo:** que el agente no convierta el historial en un pantano.

- *Cita (1:11:14):* "agents love to write code. You can give [it a task and it writes] out 500 or a thousand lines of code. Now, before that code goes live... somebody needs to review it. And that someone should be a human".
- El commit es la unidad de **revisión**: pedir cambios chicos y lógicos. Un commit = un cambio revisable; no "update the hover state on the navbar" mezclado con "implement same day delivery".
- Aunque el agente pueda hacer commit, **quien revisa el diff es una persona**. Los diffs se miran siempre — es la red de seguridad de todo lo anterior.
- **Config files van al repo:** AGENTS.md, config de la herramienta, y todo lo que afecte cómo trabaja el equipo. Los que son personales (credenciales, preferencias locales) van a `.gitignore`.
- Riesgo de multi-herramienta: si un colega usa Claude Code y otro Codex, hay **dos archivos de config** que pueden contradecirse. Preguntar explícitamente al agente "check for clashes" es una práctica válida.

**Ejercicio:** revisar los últimos 5 commits propios y marcarlos con ✅/❌ por atomicidad y por "podría explicarlo en una frase". Rehacer uno que falle.

---

### Módulo 9 — Secretos (1:15:58 – 1:22:54)

**Objetivo:** que el agente no pueda filtrar credenciales, aun equivocándose.

- Los secretos son datos de config por entorno (API keys, DB, tokens); se leen vía `process.env`, nunca hardcodeados.
- `.env` en **un solo lugar**, `.gitignore` **antes** del primer commit. *Cita (1:19:07):* "or shared carelessly and be compromised" — una vez que salió, se rota — una vez pusheado, no se "arregla" borrando: se rota.
- Los dos errores de la demo: (1) **loguear** un secreto (`console.log` con el token) — los logs terminan en logs de servidor o en chats; (2) **devolverlo al cliente** en una respuesta HTTP.
- El agente **lee los secretos del entorno** y puede usarlos donde no corresponde: *"agents do sometimes cut corners and take risks"* (1:18:24) es una descripción de comportamiento del modelo, no un defecto raro.
- Reglas del curso, en su orden: **no hardcodear**, **no loggear**, **no devolver al cliente**, **revisar diffs**, **rotar si se expuso**. Y `.env*` en `.gitignore`.

**Ejercicio:** hacer una pasada de búsqueda de secretos (`grep -E 'sk-|api[_-]?key|token'` sobre el código, excluyendo `.env`) en un proyecto propio y documentar cada hallazgo con severidad y acción.

---

### Módulo 10 — La extensión de VS Code (1:22:54 – 1:26:46)

**Objetivo:** conocer el entorno donde se corre el agente del curso.

- Instalación de la extensión de Codex en VS Code y login con la cuenta de OpenAI.
- **Reasoning level:** más razonamiento = más tokens = más caro. Para tareas comunes, bajarlo; para problemas complejos, subirlo. No hay degradación notoria al usar menos, pero sí costo que sube.
- **Modo rápido / velocidad**: "greater speed equals higher cost" (1:25:36) — la velocidad no es gratis.
- El menú de contexto (ahora escondido en la UI) muestra qué archivos entran al prompt. Buen recordatorio de que la UI **cambia**: lo que no se encuentre puede estar en otro lado.

**Ejercicio:** identificar en la UI de tu editor las tres palancas (modelo/reasoning, permisos, contexto) y anotar dónde vive cada una; en 30 días re-verificar (la lección sobre la mutabilidad de la UI).

---

### Módulo 11 — Contexto y su gestión (1:26:46 – 1:34:20)

**Objetivo:** entender la ventana de contexto como recurso físico, no como "memoria infinita".

- Contexto = **todo** lo que se le manda al modelo: instrucciones, archivos relevantes, historial de la conversación. El historial es la parte más grande.
- *Cita (1:28:30):* cuando la ventana se llena, el agente hace una de dos cosas: **comprime a un resumen** (lossy) o **trunca** (pierde lo viejo). Ambas producen comportamiento errático.
- El agente (en Codex/Scrimba) muestra un **ícono circular** que mide el porcentaje de ventana usado. Se puede activar en settings; la mayoría lo tiene oculto.
- *Cita (1:31:29):* "it's good practice to use one session per task" — sesión por tarea, no una sesión eterna.
- Herramientas para resetear: `/new` (nueva sesión) o el comando de VS Code "Developer: Reload Window". En Codex hay **compacting** automático, y en algunas versiones un `/compact`/resumen que se puede pedir explícitamente.
- *La estrategia del curso:* lo que importa debe vivir en **AGENTS.md** (persistente), no en la conversación. Lo que se pierde al truncar no debería ser lo importante.

**Ejercicio:** en una sesión larga, activar el medidor de contexto, anotar el % al empezar y al terminar la tarea, y listar qué información se perdió en el camino. Decidir qué de eso debería haber estado en AGENTS.md.

---

### Módulo 12 — Permisos y config.toml (1:34:20 – 1:43:50)

**Objetivo:** controlar qué puede tocar el agente, y con qué granularidad.

- **Approval policy** (cuándo pide permiso): `untrusted` (pregunta todo), `on-request` (pregunta para lo riesgoso), `never` (no pregunta nada). *Cita (1:37:31):* con `on-request` "codeex will do its thing without asking for permissions. But some higher risk actions will require your permission" (1:35:00: borrar archivos, instalar paquetes, correr comandos de terminal).
- **sandbox_mode** (qué puede tocar): `read-only` (inspecciona, no edita), `workspace-write` (edita el workspace, no afuera), `danger-full-access` (todo, incluido fuera del workspace). *Cita (1:38:34–1:39):* `read-only` "does exactly what you would expect. Codeex can inspect files, but it can't [edit]"; `danger-full-access` es lo que el nombre advierte — el nombre advierte.
- **config.toml**: archivo humano-legible, **global** (`~/.codex/config.toml`) o **por proyecto**. Ahí viven default model, reasoning, approval y sandbox.
- Precedencia y trampa: el **scope de proyecto** puede ser ignorado si VS Code no considera el repo como "trusted". *Cita (1:42:10):* hay que marcar el workspace como confiable en la config global para que el `config.toml` del proyecto se lea.
- *Cita (1:41:04):* "config.toml will not take effect until [the] codex session is restarted" — los cambios requieren reinicio del agente/ventana.
- Lección de método: **no confiar en la captura de pantalla de una config**: leer el archivo que realmente está vigente y verificar en la UI que el modelo mostrado cambió.

**Ejercicio (challenge del curso):** cambiar el modelo default a uno más barato en el `config.toml` global, reiniciar, y **verificar en la UI** que cambió. Entregable: la ruta del archivo usada, el valor antes/después y la prueba de que se aplicó.

---

### Módulo 13 — MCP (1:43:50 – fin, 1:50:43)

**Objetivo:** entender MCP como el protocolo que da tools externas al agente, y verlo funcionar.

- MCP (Model Context Protocol) = protocolo abierto para que el agente acceda a **tools y fuentes de datos externas**. Permite "retrieve current [data]" en lugar de confiar en el entrenamiento.
- **El loop de MCP:** el agente razona qué necesita → llama a la tool del **MCP server** → el server ejecuta → el agente evalúa el resultado → itera. *Cita (1:44:50):* "the results are returned to the agent... and the agent evaluates [them]"; el loop repite hasta completar la tarea o topar el límite (1:45:13).
- **Problema resuelto:** sin MCP, el agente inventa componentes de UI a mano (bordes inconsistentes, radios distintos, sombras distintas). Con el **MCP de shadcn**, consulta el catálogo real de componentes y usa los que existen.
- Setup: un MCP server se registra en la config del agente; el agente lo descarga/ejecuta. Puede ser scope de proyecto o global; el curso lo deja en la config del proyecto.
- *Cita (1:48:37):* el agente devolvió "a long list of 61 UI components" en 26 segundos, y el expositor lo marca como evidencia de que la información vino del server y no del modelo.
- El beneficio final: el agente deja de inventar y empieza a **usar el design system** porque tiene la tool para consultarlo.

**Ejercicio:** conectar cualquier MCP server a un agente y escribir una prueba que falle si el server no está disponible (preguntar por un dato que solo el server tiene). **Entregable:** la config + la prueba.

---

## Ejercicios por bloque

- [ ] M1: 3 líneas sobre "cerrar el loop", con el momento de verificación identificado.
- [ ] M2: comment-prompt de 5 líneas vs. prompt sin contexto, diff comparado.
- [ ] M3: AGENTS.md con 5 secciones, cada una justificada por un error real.
- [ ] M4: plan de una feature de 3+ archivos con 2 huecos encontrados **antes** de implementar.
- [ ] M5: skill `house-style` + refactor aplicado; skill de debug de repo específico.
- [ ] M6: characterization tests verdes antes y después de un refactor; prueba de que detectan un cambio.
- [ ] M7: test escrito primero (red) + código después (green), con la decisión de negocio explicitada en el test.
- [ ] M8: auditoría de 5 commits propios por atomicidad; uno rehecho.
- [ ] M9: barrido de secretos con severidad y acción por hallazgo.
- [ ] M10: mapa de palancas (modelo, permisos, contexto) y su ubicación en la UI.
- [ ] M11: medición de % de contexto en una sesión larga + qué debería haber estado en AGENTS.md.
- [ ] M12: cambio de modelo en config.toml verificado en la UI (no solo en el archivo).
- [ ] M13: MCP server conectado + prueba de que el dato vino del server.

## Banco de preguntas para estudiar

1. **Plan mode:** ¿qué tipo de tarea NO merece plan mode, y qué se pierde si lo usás igual?
2. **AGENTS.md:** ¿por qué el scope más cercano gana al global? ¿Qué pasa si los dos dicen cosas contradictorias?
3. **Skills vs. prompts:** si un procedimiento se repite 3 veces por semana, ¿es skill o es un prompt guardado? ¿Qué tiene que tener para ser skill?
4. **Characterization vs. TDD:** los dos usan tests, pero ¿qué protege cada uno y qué decisión toma cada uno? ¿Por qué el orden importa?
5. **El bug de redondeo:** ¿quién debería decidir redondear por ítem o por total, y cómo se codifica esa decisión para que el agente no la re-decida?
6. **Secretos:** enumerá las cuatro barreras del curso y decime cuál falla primero si el agente no revisa diffs.
7. **Contexto:** ¿por qué poner las reglas en AGENTS.md en vez de repetirlas al inicio de cada sesión? ¿Qué pasa con el compacting?
8. **Sandbox y approvals:** ¿qué combinación usarías para un repo legacy que no conocés, y por qué?
9. **MCP:** ¿cuál es la diferencia entre "el agente sabe de shadcn" y "el agente consulta el MCP de shadcn"? ¿Cómo probás que está usando el server?

## Notas editoriales

- **Nombres corregidos por ASR:** Scrimba, Tom Chant, Codex, AGENTS.md, config.toml, shadcn, npm, `process.env`, `.env` / `.env.local`. Glosario completo en `transcripcion.md`.
- **Claims con cifra:** "61 componentes" es un dato observado en la demo, no un benchmark. "1 million tokens" de ventana se menciona como ejemplo; el valor concreto depende del modelo y cambia — no se debe citar como constante.
- **UI mutable:** el video avisa explícitamente que la UI de Codex cambia ("they've changed again by the time you watch it", ~1:26:1x). Todo lo que sea ubicación de botones o menús se re-verifica contra la versión instalada antes de enseñarlo como vigente.
- **Material del curso:** el código de cada lección vive en Scrimba, no en el video. Los ejercicios de acá son reconstrucciones propias, no links al curso.
- **Acciones externas:** el curso invita a crear cuenta en Scrimba/OpenAI; el workspace no lo hace sin pedido explícito.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
