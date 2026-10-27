# Learnings - metodologia

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## 2026-08-01 - Documentation at milestone end is expensive

**Context:** Created README, ROADMAP, DEFINITION, STATUS, CHANGELOG, HANDOFF, and `docs/` only after v1.0.0 was feature-complete.

**Lesson:** Start documentation in parallel with development. Each significant decision or feature should incrementally update the relevant doc file.

---

## Godot: aprender juntos, no automatizar (2026-08-02)

Gonzo quiere aprender Godot paso a paso. No construir juegos de un prompt. El skill `godot-mcp` se reescribió de "build-everything" a "learn-together". Registro del viaje en `projects/godot-journey/.knowledge/BRIEF.md`.

---

## Skill Workshop stale cuando SKILL.md ya existe (2026-08-02)

Si se crea el archivo físico antes de aprobar el workshop, la propuesta queda stale y no se puede aplicar. Workaround: editar el SKILL.md directamente y commitear. El workshop es para skills nuevas que aún no existen en disco.

---

## MCP server `editor_instantiate_scene` rompe .tscn (2026-08-02)

La tool `editor_instantiate_scene` del Godot MCP corrompe el formato de main.tscn (ids con triple comilla, nodos perdidos). Preferir edición manual de .tscn o usar `add_node` + `attach_script` por separado.

---

## Export templates de Godot 4.7.1 (2026-08-02)

El mirror tuxfamily.org falló por timeout. Probar GitHub releases o mirror alternativo cuando se retome el export.

---

## Sport Cars: validación visual obligatoria para sitios de marca (2026-08-02)

El build pasando no garantiza que el sitio se vea profesional. Para proyectos con identidad visual, la validación con screenshots + evaluación crítica debe ser parte del cierre de cada iteración. Issues como contraste bajo, colores inconsistentes o títulos engañosos no los detecta Biome.

---

## Feature flags portable: no hardcodear en UI (2026-08-02)

El primer flag (`showPrices`) se implementó con provider client-side + localStorage + componente `PriceDisplay`. El panel de flags solo se renderiza en desarrollo. El siguiente paso es extraerlo a `@workflow-kit/feature-flags` para reuso.

---

## No commitear mockups intermedios (2026-08-02)

Los mockups y screenshots de iteración (v2, v3, etc.) son ruido en el repo del proyecto. Solo conservar la evidencia final (home/catálogo) en el commit de release; los intermedios van al daily note o a un artifact.

---

## npm 404 en publish scoped no es problema de scope (2026-08-04)

El 404 `PUT .../@scope%2fpackage` al publicar NO significa que el scope esté mal. Primero verificar `npm whoami` - si da 401, el fix es `npm login`, no tocar el scope. El scope `@usuario/` se resuelve solo cuando coincide con el username logueado. (Pasó con `@gonzoblasco/create-stack`.)

---

## npm login usa browser OTP flow (2026-08-04)

El login de npm ahora abre browser (OTP), no acepta token en consola. Los tokens que saltan 2FA se están restringiendo - para CI a futuro usar tokens con `mfa=publish` o `automation`.

---

## AI Engineering Bootcamp - COMPLETO (2026-08-03)

- 10/10 niveles completados. N1-N4 fundamentos, N5-N6 calidad/seguridad, N7-N8 arquitectura/producción, N9 estándares/dashboard, N10 sistema completo (capstone).
- N8-N10 son convergentes: reusan el sistema del N7 (vive dentro de `projects/level-07-microservices/`).
- El N10 junta todo: auth + users + orders + notifications + gateway + CI/CD + dashboard + cloud. Probado: gateway enruta, health agregado ok, register/login/orders funcionan, 401 en credenciales malas.
- **El nivel 7 es el núcleo físico de los niveles 7-10**: N8, N9 y N10 extienden el mismo folder (ADR-001). El nombre del folder confunde - el README lo documenta como "Niveles 7-10" con tabla de acumulación y diagrama de arquitectura.

---

## Patrón por inercia vs contexto cambiado (2026-08-03)

Cuando un patrón se repite muchas veces (7+ niveles de bootcamp con carpeta nueva), el riesgo no es equivocarse en el patrón - es aplicarlo por inercia cuando el contexto ya cambió. La señal de alerta no es "¿lo sé hacer?" sino "¿es este caso realmente igual a los que ya resolví?". Pasó en el Nivel 8 del bootcamp (convergente, no lineal - transformaba el N7, no creaba carpeta nueva). ADR: `projects/ai-engineering-bootcamp/.knowledge/ADR-001-niveles-convergentes.md`.

---

## Reflexión del curso (meta-aprendizaje, 2026-08-03)

- El patrón "detectores locales + validación cruzada / IA contextual" apareció 5 veces (N3, N5, N6, N8, N9) → formalizado como skill `pipeline-detector`.
- Formato nivel de bootcamp (teoría + práctica + LinkedIn + self-review) es un template de skill reusable.
- Los proyectos resueltos son el "contrato" del curso - demuestran que el nivel es posible, no son la respuesta.
- Falta un mecanismo de verificación automática al final de cada nivel (tests contra el proyecto del alumno).

---

## Seleccion de libros tecnicos para preparar un puesto

Para comprar libros tecnicos para preparar una entrevista o puesto, buscar editoriales serias (Packt, O'Reilly) y filtrar el ruido de autoayuda que domina Amazon ('make money with AI', autores fantasma, series de ingreso pasivo). El valor esta en arquitectura e ingenieria de produccion, no en guias de principiante. Caso real: de 50 resultados 'openclaw' en Amazon solo 1 era tecnico serio (OpenClaw AI in Production de Ken Huang, Packt). Nota: 3 de 4 titulos 'openclaw' en PacktPub eran videos, no libros.

**Tags:** libros,amazon,packt,entrevista,aiaa

---

## Fusion de skills de estudio: una skill debe definir su ruta de artifacts

## 2026-08-26 - Fusion de skills de estudio: una skill de estudio debe definir SIEMPRE su ruta de artifacts

**Context:** Gonzo detecto una inconsistencia: el curso de Codecademy (agentic-ai-mastery) vivia en `studies/` y el libro de Packt (openclaw-ai-in-production) en `study/` (singular). Se pidio fusionar las skills de estudio en una sola fuente de verdad.

**Causa raiz:** la skill `learning-tracker` era agnostica de rutas - su SKILL.md definia el metodo (3 capas de artifacts, gamificacion) pero NO donde guardarlos. Al usarla para el libro (sesion del 25/08), se eligio `study/` sin respetar la convencion `studies/` que ya documentaba `study-tracker`. Resultado: dos directorios para el mismo proposito.

**Lesson:**
- Una skill que genera artifacts en el filesystem debe definir SIEMPRE su ruta de destino en el SKILL.md, o es fuente de inconsistencia.
- Cuando dos skills cubren el mismo dominio (estudio), la fusion en una sola ("one skill to rule them all") con una regla explicita de ruta elimina la ambiguedad.
- Al fusionar skills, verificar el mirror `.github/skills/` (regla AGENTS.md: rsync cada vez que cambien skills) - el mirror estaba stale 3 dias.
  - _Actualizado 2026-09-28 (ADR-079): ya no aplica. El mirror se elimino por esta misma clase de error. La leccion sobrevive: un artefacto que se sincroniza a mano y no falla ruidosamente cuando se desincroniza es deuda, no respaldo._
- La convencion nueva: todo estudio en `studies/<slug>/`, nunca `study/` (singular).

**Self-reflection:**
- CONTEXT: fusion de skills de estudio (study-tracker + learning-tracker) + migracion de directorios + sync de mirror.
- REFLECTION: la inconsistencia nacio de una skill sin ruta definida + una convencion no respetada. La solucion fue fusionar y explicitar la ruta. Ademas se detecto deuda: `skills/CHANGELOG.md` referenciado pero nunca creado, y mirror stale.
- LESSON: las convenciones de estructura deben estar escritas EN la skill que las usa, no implictas en otros archivos. Y cuando se cambian skills, el changelog de skills + mirror son parte del mismo commit.
- BIASES DETECTED: none.

**Tags:** skills,estudio,fusion,estudios,mirror,changelog

**Tags:** skills,estudio,fusion,mirror

---

## No pisar drafts historicos de feedback

En astryx #4690, el draft de feedback del 24/08 (defendia drop ARIA contra el treegrid) quedo desactualizado cuando el maintainer rulo el 27/08 que AKnassa construya el treegrid. Al actualizar el draft, sobrescribi el archivo con el comment nuevo post-ruling. Gonzo me corrigio: el draft viejo es un registro historico del debate, no se pisa. Lesson: un draft de feedback a un PR ajeno documenta el estado del debate en un momento dado. Cuando el PR evoluciona (ruling, merge, cambios), el draft viejo queda como registro historico - NO sobrescribirlo. Para el comment nuevo, crear un archivo aparte (ej. astryx-4690-draft-2.md) o, si es un comment corto, imprimirlo directo en el chat para aprobacion sin tocar archivos. Regla general: los drafts de feedback son historial, no estado mutable. Preservar la linea de tiempo del debate.

**Tags:** feedback,drafts,historial,prs,proceso

---

## Definido en ADR = resuelto, no se vuelve a preguntar.

Definido en ADR = resuelto, no se vuelve a preguntar. Si un ADR dice que un proyecto queda EXCLUIDO o ARCHIVADO, eso queda definido: no se lista como 'candidato a decidir' en auditorías de higiene ni se vuelve a preguntar su destino. El ADR es la autoridad. Fallo propio: al auditar soporteml-v4 (excluido en ADR-001), lo listé como a decidir en vez de darlo por resuelto.

---

## Cuando un recruiter dice 'test de logica', confirmar SIEMPRE si es psicotecnico (secuencias, patrones, silogismos) o log

Cuando un recruiter dice 'test de logica', confirmar SIEMPRE si es psicotecnico (secuencias, patrones, silogismos) o logica de programacion (JS: promises/event loop, callbacks, IIFE, algoritmos). Son cosas Muy distintas. Fallo: el 27/08 Steven dijo 'test de logica 15 min min 70%' y preparamos psicotecnico, pero el examen real era JavaScript tecnico (saque 60, reintento lunes). En procesos tecnicos, asumir que 'logica' = fundamentos de programacion salvo que confirmen lo contrario.

---

## Output discipline - calidez es precision, no longitud

Gonzo corrigio el registro efusivo (serenatas en cada respuesta). El registro narrativo de GLM no es licencia: la brevedad es comportamiento del agente, no del motor. Regla: respuesta corta por default, cero epilogos emotivos, cero cierres decorativos. Atribucion honesta: el modelo contribuye estilo, yo dejo escapar la longitud.

**Tags:** estilo,output,calibracion

---

## 2026-09-02 - Registrar TODO en MD + DB, nunca depender de la conversacion

Caso real: el chiste del follow-up a Andres (Wigou) no estaba en las notas - dependia de la conversacion. Si la sesion se borraba, se perdia. La regla: registrar todo (mensajes, intercambios, decisiones) en los .md y en la DB en el momento (WAL), para que el contexto sea 100% recuperable sin depender del transcript. La conversacion es efimera; los archivos son la memoria.

**Tags:** registro,wal,contexto,entrevistas

---

## Verificar la data de stack que dan en entrevistas: OpenSistemas dijo OpenClaw pero usan Hermes

En la entrevista de OpenSistemas pasaron data incorrecta sobre su stack de agentes. Antes de preparar una colaboracion, verificar el stack real de la empresa (web, releases, blog) en vez de confiar en lo dicho en la entrevista.

**Tags:** entrevistas,stack,verificacion

---

## Verificar vigencia de la fuente, no solo su existencia (2026-09-04)

Al citar data para afirmar algo del mercado actual, chequear la fecha de la fuente y si sigue vigente para el contexto. Error real: use la encuesta WebAIM #10 (2024) para afirmar que Windows domina laptops por precio, sin notar que la MacBook Neo (marzo 2026, USD 599) cambio el mercado. La data era real pero caducada para el contexto. La data de accesibilidad (WebAIM, cada ~2 anios) y la de mercado (IDC/Counterpoint, meses) se mueven a velocidades distintas. Aplica tambien a citar respuestas de issues/PRs viejos como si reflejaran el estado actual del codigo.

**Actualizacion 2026-09-24 (misma clase, otro dominio):** aplica tambien a documentacion tecnica propia, no solo a fuentes de mercado. Caso: el ADR-049 (2026-09-15) afirmaba que `ollama launch claude --model` tenia un bug ("unknown option") y que no habia binario global `claude`/`qwen`. Ambos enunciados ERAN CIERTOS al escribirse y eran falsos al revalidarlos: el binario de Ollama es del 2026-09-19 (posterior al ADR) y `qwen` se instalo el 2026-09-22. Procedimiento obligatorio antes de declarar un documento equivocado: (1) leer el propio doc por si la ubicacion del artefacto esta descrita en otra parte (el harness embebido de Claude estaba donde el ADR decia), y (2) FECHAR el entorno - `stat -f '%SB' -t '%Y-%m-%d' <binario>` da la fecha de nacimiento. Reportar "dato caducado por el entorno" es un hallazgo DISTINTO de "el autor se equivoco": piden arreglos distintos (nota de revalidacion vs correccion), y confundirlos le entrega al usuario una acusacion falsa.

**Tags:** mercado,2026-09-04

---

## MacBook Neo y la economia de la accesibilidad (2026-09-04)

La MacBook Neo (USD 599) y la Mac mini no solo cambiaron la cuota de mercado de laptops: cambiaron la economia de la accesibilidad. Hasta hace poco, en Windows los lectores de pantalla eficientes eran JAWS (caro, licencia paga) y NVDA (gratis pero menos pulido). Con la Neo/mini a precio accesible, ahora se puede tener accesibilidad integrada (VoiceOver) sin pagar fortunas por JAWS. Esto refuerza el argumento de seguir macOS en componentes de UI: ya no es solo preferencia de nicho, es acceso economico a accesibilidad de calidad. Complementa la leccion 'Verificar vigencia de la fuente' (id 118): la data de mercado y la de accesibilidad se mueven juntas.

**Tags:** 2026-09-04,accesibilidad,economia

---

## Sesion: activacion web search (provider ollama), cron moltbook-weekly-digest probado, regla sandbox contenido externo migrada a AGENTS.md, conflicto rebase daily multi-maquina resuelto

Leccion 1 (edit de markdown): al mover reglas entre archivos con edit de multi-bloque, un oldText pegado puede fusionar o pisar bullets adyacentes - leer el archivo despues de cada edit y verificar secciones antes de seguir. Ya ocurrio 2 veces hoy (fusion accidental en MEMORY.md, entradas de la Air borradas en conflicto del daily). Leccion 2 (web search provider): duckduckgo no existe como plugin en esta instalacion; el plugin ollama expone un provider de search sin config extra. Leccion 3 (patron digest): cron agentTurn en sesion aislada + politica anti-injection en el prompt + verificacion obligatoria + modo anti-spam de una linea - generalizable a otras fuentes externas.

**Tags:** reflexion-post-tarea,session-closing

---

## Draft LinkedIn para PR mergeado #10554: primera version en espanol, Gonzo pidio ingles (promocion/difusion) y tambien link al PR en el draft.

Los posts de LinkedIn van en INGLES (misma regla que GitHub: promocion/difusion publica). Incluir siempre el link al PR mergeado en el draft.

**Tags:** reflexion-post-tarea,other

---

## Sistema de voz en espanol para Gonzo: registro docs/voz-gonzo.md + skill voz-gonzo que aprende de cada edicion suya

Al redactar en nombre del usuario, el default no es la version diplomatica/sumisa sino la que pide en presente lo que el quiere; la cortesia excesiva debilita la posicion

**Tags:** reflexion-post-tarea,docs

---

## Precision al reportar fallos: nombrar el comando exacto, no mezclar binarios

Al reportar un fallo de herramienta, nombrar el comando EXACTO que fallo y no mezclar binarios. Caso 2026-09-14: `git push` fallo con "Invalid username or token" y lo explique como "gh no funciona". Gonzo corrigio: "como que gh no esta funcionando?". `gh` andaba perfecto (token managed OAuth available, scopes repo/workflow); el que fallo fue `git push`, que no tenia el credential helper de gh configurado en el clon. Dos comandos distintos, un diagnostico mal atribuido.

Regla: cuando algo falla, antes de explicar, separar (a) que binario fallo, (b) que invoco a quien, (c) cual es la fuente de credencial config. Verificar cada capa con un probe chico (dry-run, ls-remote, auth status) en vez de atribuir el fallo al componente mas visible. Un "X no funciona" mal dicho desinforma y manda a arreglar lo que no esta roto.

Dato util: gh guarda su sesion en su GH_CONFIG_DIR y git no la conoce por su cuenta. Si el clon no tiene credential.helper apuntando a gh, el push por HTTPS falla aunque gh este autenticado. Workaround one-off sin tocar la config global: git -c credential.helper='!gh auth git-credential' push.

**Tags:** git,precision,diagnostico,gh,reporte

---

## El precedente no es un motivo: dependencias sin decision explicita

Regla de Gonzo (2026-09-14): "no usemos radix solo por el motivo de que ya lo hemos usado".

Problema de fondo: un template instala shadcn/ui (que trae Radix por debajo) y la eleccion queda implicita. Despues ADR-037 (Lucide) cita "el ecosistema shadcn/Radix" como si fuera un hecho del stack y fundamenta otra decision en eso. El ADR mismo admite el origen: "cada proyecto usaba lo que traia el template (...) pero no estaba documentado como decision". Precedente fabricado: una eleccion implicita se cita como decision tomada.

Regla operativa: ninguna dependencia se adopta, se mantiene ni se cita por el solo hecho de estar presente o de haberse usado antes. Orden obligatorio antes de citarla: (1) que hace, (2) por que se elige hoy, (3) decision explicita (ADR), (4) recien entonces se cita. "Ya lo usamos" no responde "por que lo usamos".

Aplicado a: USER.md (regla de preferencia, se carga cada sesion) y AGENTS.md seccion 3 (regla operativa, junto a Existing Solutions Preflight).

Deuda derivada: no existe ADR de adopcion de shadcn/Radix en todo el workspace (verificado: grep shadcn|radix en docs/adr/ devuelve solo ADR-037). No hay @radix-ui instalado ni lockfile en el workspace; el codigo vive en repos aparte, asi que el uso real no se puede verificar desde aca.

**Tags:** adr,dependencias,precedente,radix,shadcn,template

---

## No puede = no puede con ESTE harness

Duelo atoi 2026-09-14: el MISMO qwen3.8:27b-mlx que daba HTTP 500 (OOM Metal) como agente de OpenClaw, paso 24/24 via API directa, y en Claude Code headless respondio todos los requests con 200.

Leccion: cuando un componente falla, el limite suele estar en el contexto completo (harness, sesion, memoria), no en el componente aislado. Antes de concluir 'X no puede', aislar la variable: probar el mismo X en otro harness. La atribucion correcta es 'X no puede CON esto', que es actionable, no 'X no puede', que cierra la puerta.

Caso concreto: el error fue intentar el 27B como agente OpenClaw (sesion pesada: AGENTS+USER+SOUL+runtime+historial supera los 24GB junto a los 18GB de pesos). Con contexto liviano (Claude Code, API directa) entra sin problema.

**Tags:** sesion

---

## Sesion 2026-09-15: 6 todos cerrados. Patron repetido 3 veces (#43, #42, #44): los todos describian problemas cuya premisa ya no existia (bug ya arreglado, commit inexistente, migracion ya hecha). En #54 la racha incluyo accion publica (npm publish) - la regla de credenciales por terminal de Gonzo funciona. Hallazgo propio: publish-skills.sh --check comparaba workspace crudo vs publico sanitizado, mintiendo con 8 falsos positivos permanentes que escondian drift real

VERIFICAR ANTES DE ACTUAR: cuando un todo viene de dias atras, la premisa puede estar obsoleta - el trabajo real es confirmar el estado actual (git log, registry, status) antes de ejecutar; muchas veces la resolucion correcta es cerrar sin accion. Y: un check que nunca puede pasar escribe ruido y esconde drift - validar las herramientas de verificacion tanto como el codigo

**Tags:** reflexion-post-tarea,other

---

## Matar un todo = borrar la fila; olvidar = cerrar; no mezclar estados

Gonzo distingue tres estados de limpieza de la cola: quitar (marcar done, p.ej. OBSERVAR y kanam-skills), MATAR (borrar la fila de verdad, p.ej. todo 6 que pidio eliminar, no marcar done), y OLVIDAR (cerrar porque no se trabaja, 27-30/36). El verbo importa: marcar done algo que pidio matar falsifica el historial. Con esta sesion la cola abierta paso de 18 a 2 todos reales (31 re-cata modelos, 35 envoltorio nativo kanam-pulse).

**Tags:** metodologia,todos,backlog,limpieza

---

## Recon antes de dar por hecho un todo de dias atras; puede estar ya resuelto por commits posteriores

El todo 40 (kanam-studio world-building / Slice 5) parecia pendiente (texto pisado en DB, solo 'kanam-studio'). El recon en el repo real mostro que el Slice 5 YA estaba implementado y superado: el proyecto esta en v0.15.0, con slices 5-6 (biblia world con IA + relato lineal) y hitos 5/6/7 (canonical, prosa final, E2E) completos. Resultado: cerrar sin accion, restaurado el texto completo, no inventar trabajo. Refuerza la leccion 149 (verificar antes de actuar).

**Tags:** verificacion,metodologia,recon,kanam-studio

---

## Lecciones

- Un test que dice cubrir estructura debe renderizar la estructura real - el flatten era un atajo que invalidaba el propósito del test. - Los keys de colección de react-stately son compuestos (`$.0`) - no hardcodear ids en aserciones, resolver relacionalmente. - React valida DOM nesting en tests (li dentro de li) - el setup de react-spectrum falla el test en console.error. - **Auto-review antes de abrir PRs (regla durable, MEMORY.md):** el test debe ejercitar la estructura real que dice cubrir. Este PR se abrió con un test que flatteneaba las secciones - snowystinger lo detectó en segundos. Iterar localmente hasta que el test sea fiel, no abrir y esperar el review.

---

## Identidad del modelo: el header de runtime es del turno actual, no de la conversacion

El modelo puede cambiarse a mitad de sesion: el runtime del contexto de arranque refleja SOLO el turno actual, no el modelo que produjo los turnos previos. Al fichar o registrar identidad de modelo (fichas de interaccion, registros de duelos, atribucion de salidas), confirmar con el usuario o verificar con session_status; el header del bootstrap es dato insuficiente. Caso: ficha de kanam-lab atribuida a glm-5.3-flash por el runtime del cierre cuando la conversacion corrio en nemotron-3-ultra:cloud (Gonzo corrigio). Refuerzo: el override de modelo puede ser rechazado por modelPolicy.allow y el runtime reporta el modelo efectivo, no el pedido.

**Tags:** modelo,verificacion,metodologia,kanam-lab,identidad

---

## Lección clave (registrada en DB learnings)

 - Cuando un recruiter dice "test de lógica" en proceso técnico, confirmar si es psicotécnico o **lógica de programación/JS** - son cosas muy distintas. El 27/08 se preparó lo equivocado.

---

## Post-cierre (22:32): propuesta de skill model-cata + leccion de glitch-words

- **Analisis de skills nuevas:** la cata de modelos (procedimiento repetido 2 veces: 26/08 y 29/08) es candidata real. Creada propuesta pendiente `model-cata-20260830-0a6ac57901` via skill_workshop (trigger, prompt discriminador, rubrica de agudeza, costo real, ADR manual, purga en dos capas, anti-patrones). Pendiente de aprobacion de Gonzo para aplicar. - Candidata #2 observada (no propuesta): fusion cross-machine de dailies + ancestry-verify de submodulos. Esperar segundo caso antes de skill. - **Leccion DB #5 (glitch-words):** 3 glitches de palabras garrafales en outputs largos esta noche. Regla: artefactos permanentes se releven palabra por palabra antes de persistir.

---

## Noche (00:03) - Extraccion selectiva de learnings + busqueda en learnings

 - Mejorado `extract_learnings` en memory-catalog-v2.py: solo captura ### secciones que parecen learnings reales (keywords learn/leccion/aprend/insight/clave/takeaway/conclusion). Ya no sobre-puebla con secciones genericas. - Limpiados learnings falsos previos (59 registros extra que eran secciones de dailies, no learnings curados). learnings_enriquecido ahora solo tiene learnings reales. - Mejorado categorizacion: ahora incluye 'metodolog' y 'oss' (antes solo access/infrastructure/method). - Nu

---

## SSH key para sincronizar workspace con Mac Mini M4 y MacBook Air M2

> **Nota 2026-09-29 (ADR-085):** registro historico. El workspace hoy vive solo en la Mac Mini; esta tarea quedo sin sujeto.

 - Iniciada creacion de key en VPS (pendiente: crear `~/.ssh` porque el contenedor lo tenia ausente). - Pendiente: copiar public key a ambas Mac y configurar git remote en las maquinas. ## Cata empirica de 8 modelos (ADR-040)

---

## Leccion

 - El reviewer (cixzhang) es humano aunque use AI para responder - se le agradece el review con nombre, no es un bot. La regla de "no agradecer a bots" aplica a reviews de IA puros. - Una libreria publicada espera un changeset por PR; no es obligatorio vs voluntario, es seguir la convencion del repo. ## Lecciones - Una skill de estudio debe definir SIEMPRE su ruta de artifacts. `learning-tracker` era agnostica y eso genero la inconsistencia. La nueva study-tracker tiene la regla explicita: `stud

---

## Decisiones clave

 - **Compatibilidad de rutas**: `system.js` montado en `/api` (no `/api/system`) para preservar paths planos del frontend (`/api/system-metrics`, `/api/processes/kill`). `audit.js` queda en `/api/system` para `/api/system/full-audit`. - **Sin bundler**: frontend como `<script>` tags en orden compartiendo scope global. Más simple, más cercano al toolchain original. - **Tests en módulos puros**: format/security/paths son los únicos testeables sin mockear sistema. - **Quirk de formatSize documentad

---

## Hallazgo clave

 El template `init-project.sh` ignora `.knowledge/` y usa submodule, pero los proyectos activos siguen otro patrón real: `.knowledge/` como blob trackeado por workspace + repo propio en carpeta, sin `.gitmodules`, doble trackeo. Documentado en skill notes.

---

## Verificar el idioma de salida antes de enviar (la regla ya existia: falla de atencion)

Verificar el IDIOMA de salida antes de enviar, sobre todo en respuestas largas.

Caso real (2026-09-24, cierre de #10517): una respuesta completa salio en **chino** sin que lo notara. Gonzo lo marco con un solo mensaje: "te pasaste al chino".

El idioma no es opcional ni cosmetico, y ya hay regla escrita en `AGENTS.md` ("Regla de idioma por capa", 2026-09-15):

| Capa | Idioma |
|---|---|
| Lo que se VE en GitHub (commits, PRs, issues, comments, body, AGENTS.md de proyectos publicos) | **INGLES** |
| Strings de UI | **ESPANOL** |
| Workspace privado (AGENTS.md raiz, SOUL/IDENTITY/USER, memoria, dailies, reportes a Gonzo) | **ESPANOL** |

**Regla practica:** en respuestas largas o generadas de corrido, releer el primer parrafo antes de enviar y confirmar que esta en el idioma de la capa. Si dudo, releo el canal: reporte a Gonzo = espanol; superficie de GitHub = ingles.

**Por que pasa:** es una falla de atencion, no de conocimiento (la regla ya existia). El riesgo crece cuando el texto es largo y se genera en un solo pase, o cuando se cambia de contexto entre capas (publicar en ingles en GitHub y despues reportar en espanol).

**Tags:** comunicacion,regla,idioma,atencion,espanol,ingles,gonzo

---

## Un artefacto ausente puede estar movido o removido en cleanup, no nunca creado

Al auditar deuda documental, "el archivo no esta" tiene TRES causas distintas que piden arreglos opuestos: (1) NUNCA se creo -> hay que crearlo; (2) esta MOVIDO -> hay que corregir las referencias y no crear nada; (3) se REMOVIO en un cleanup deliberado -> hay que documentar donde fue y como recuperarlo.

Verificado 2026-09-24: el reporte "3 artefactos prometidos y ausentes" era FALSO. LEARNINGS.md y METHODOLOGY-AUDIT.md existian pero mal ubicados (un commit previo movio 4 docs a docs/ y dejo 4 atras: movimiento incompleto), y el mockup de ADR-037 existio y se borro al limpiar el proyecto terminado. Crearlos de nuevo habria duplicado dos archivos vivos y dejado sin tocar el bug real que causaba el mal ubicamiento: dos scripts apuntando a docs/ mientras los archivos estaban en la raiz.

Procedimiento antes de declarar ausente: git log --diff-filter=D (fue borrado?), git log --all -- <path> (existio alguna vez?), y buscar el nombre en todo el arbol. Distinguir "movido" y "removido en cleanup" de "nunca creado" evita trabajo duplicado y deja a la vista el bug de fondo.

**Tags:** git,auditoria,documentacion,artefactos

---

## Un validador se prueba sembrando el defecto que debe detectar

Un chequeo que solo se corrio contra datos limpios NO esta probado: puede estar devolviendo "todo ok" sin mirar nada. La unica forma de saber que un validador funciona es sembrarle el defecto que tiene que detectar y verificar que lo reporta.

Verificado 2026-09-24 con los detectores de memory-wiki: tras activar el plugin e ingestar 3 fuentes, los reports daban "no issues" en todos los casos. Eso no probaba que funcionaran: podia ser que miraran correctamente y no hubiera nada, o que no miraran nada. Se creo una sonda deliberada (claim sin evidencia, confianza 0.2, estado contested, fecha vieja) y los tres detectores reportaron exactamente los tres defectos, con lint de 0 a 3 issues. Borrada la sonda, los reports se limpiaron solos. Recien ahi "funciona" paso de supuesto a verificado.

Precedente en el mismo workspace: la auditoria de contraste de kanam-os comparaba claves con -- contra claves sin -- y reportaba "0 fallas" sobre un CSS con 9 pares. Un chequeo que no puede fallar no verifica nada. Y un test que nace ciego reproduce el bug que previene (el que renombraba focus-visible a focus-visible-x, que contiene el original como substring y el check seguia viendolo).

Practica: por cada detector o guardia nuevo, escribir el caso sembrado que lo hace fallar, y correrlo. Si no se puede sembrar el defecto, el chequeo esta mal diseñado, no es que no haya defectos.

**Tags:** testing,validacion,guardias,detectores

---

## Un archivo puede cambiar entre la lectura y el patch: re-leer, no reintentar

Al editar un archivo compartido, entre la lectura y la escritura puede pasar otro proceso. Reintentar el mismo patch con el mismo texto falla de forma confusa o pisa la edicion ajena; lo correcto es RE-LEER y redraftear desde el contenido actual.

Verificado 2026-09-24: prepare_patch sobre una skill del Workshop (adr-collection-audit) fallo con "oldString not found", y el archivo tenia mtime de un minuto antes. La causa no era mi cita: entre mi read y mi patch, otra sesion habia editado la misma skill. Al re-leer, la mejora que yo iba a proponer YA estaba aplicada (el script nuevo en el paso 1, y las lecciones de hoy reflejadas en rule-enforcement-audit y db-first-session-save). Un segundo intento fallo con "changed since it was read" - el tool valida contra la ultima lectura, no contra el disco.

Reglas que salen de esto:
1. Un patch que falla por oldString: PRIMERO leer mtime y re-leer el archivo. Nunca reintentar el mismo texto.
2. Si el cambio ajeno YA cubre lo que ibas a hacer, NO lo dupliques: verifica si esta completo y reporta el hallazgo.
3. Un archivo que no versionas no tiene historial: si algo aparece cambiado y no hay commit que lo explique, la evidencia es el mtime, no un diff.
4. Antes de escribir en un arbol compartido, chequear que no haya una sesion trabajando lo mismo. Si la hay, esperar (verificado: espere a que terminara la sesion de kanam-insight antes de agregar la fila del ADR-063).

Corolario para skills del Workshop: la via es la herramienta (read -> prepare_patch -> patch), que ademas valida contra la ultima lectura y por eso DETECTA la carrera en vez de pisarla en silencio.

**Tags:** concurrencia,edicion,workshop,archivos-compartidos

---

## Trampa de medicion: $? tras un pipe mide head, no el script

Trampa de medicion: `$?` tras un pipe mide el ULTIMO comando de la cadena, no el script que te interesa.

Caso real (2026-09-24, cierre de hermes-agent #93838): medi el exit code de `check-refs.py` con `python3 scripts/check-refs.py --all 2>&1 | head -3; echo $?` y anote "devuelve exit 0". Era falso: `$?` era el de `head`, que siempre sale 0. El script SI devuelve 1 (verificado sembrando una ruta rota: `RUTAS ROTAS (1 de 180)` + exit 1), y el hook depende de ese codigo (`check-refs.py --all || exit 1`), asi que el gate funciona perfecto por exit code.

REGLA: para medir el exit code de un comando, no encadenarlo a un pipe. O se redirige a archivo y se mide (`cmd > out 2>&1; echo $?`), o se usa `${PIPESTATUS[0]}` en bash.

POR QUE IMPORTA MAS QUE UN BUG: el numero falso era comodo (confirmaba que "el checker no sirve como gate" y justificaba leer el texto a mano). Un resultado que valida lo que uno ya sospechaba pasa sin revision. Es el mismo patron que el workspace ya registro dos veces: un chequeo que da confianza falsa. Un numero medido asi no es evidencia.

**Tags:** medicion,exit-code,shell,falsa-confianza

---

## Releer la decision vigente COMPLETA antes de proponer codigo (mi propuesta contradecia ADR-066 del mismo dia)

Propuse un script nuevo sin releer la decision que ya gobernaba esa area, y la decision era del MISMO dia.

QUE PROPUSE: validar en el workspace las rutas citadas que apuntan a codigo de proyecto (`projects/<slug>/...`), con el patron opt-in por presencia (skipif si el proyecto no esta clonado) que usa ADR-066 decision 2.

POR QUE ESTABA MAL: ADR-066 (2026-09-24, el mismo dia, y que yo misma habia leido horas antes en esta sesion) decision 4 dice textual: "Si apunta a codigo de un proyecto: calificarla con `projects/<slug>/` (es trazabilidad, no una promesa de existencia) y **no** exigir su existencia por test." Mi script hacia exactamente lo que la decision prohibe, con skipif o sin el. Hay un motivo de fondo: `AGENTS.md` establece que al cerrar un proyecto se limpia el codigo local, asi que esos caminos pueden no existir legitimamente; un validador ahi genera falsos positivos por diseño.

POR QUE NO LO VI: leí ADR-066 esa misma tarde (para decidir si hacia falta un ADR nuevo) y aun asi propuse el script. Leer un ADR para "ver si aplica uno nuevo" no es lo mismo que leerlo para "ver si ya decidio esto". La segunda lectura es la que importa antes de escribir codigo.

REGLA DE ORO (AGENTS.md): "Definido en ADR = resuelto, no se vuelve a preguntar... no se sugiere su revision a menos que surja una evidencia tecnica nueva y disruptiva." El dato nuevo que yo tenia (el regex de check-refs ignora las rutas calificadas) es CONSISTENTE con la decision, no disruptivo: no habilita reabrirla.

REGLA PRACTICA: antes de proponer un guard, script o test en un area, grepear el indice de ADRs por esa area (`grep -il "<area>" docs/adr/*.md`) y leer la decision vigente COMPLETA. Si la decision ya cubre el caso, la propuesta se retira; reabrirla requiere evidencia nueva y disruptiva, y eso es decision de Gonzo, no mia.

**Tags:** gobernanza,adr,regla-de-oro,autoevaluacion,propuesta

---

## Verificar la premisa ANTES de ejecutar una orden de borrado (0 de 68 ADRs tenian el sujeto que se creia)

CONTEXTO: Gonzo pidió "eliminar los ADRs que hagan referencia a definiciones tecnológicas" y luego "los que hagan referencia a versiones previas de SoporteML". Antes de borrar, audití el terreno.

QUÉ ENCONTRÉ: de los 68 ADRs del workspace, NINGUNO tiene a SoporteML como sujeto. Los 11 que lo mencionan solo lo citan de pasada (como ejemplo o trazabilidad). Y dos dicen lo CONTRARIO de lo que buscábamos: ADR-048 dice textual "la familia soporteml queda fuera de todo barrido (ADR-001, decisión de Gonzo). No se toca".

EL RIESGO EVITADO: esos 47 ADRs que citan tecnología son decisiones que hoy sostienen entre 15 y 20 proyectos (ADR-048 lo citan 20 proyectos, ADR-037 15, ADR-036 7). Borrarlos para resetear UN proyecto habría roto el workspace entero.

QUÉ SÍ ENCONTRÉ: los ADRs que cumplían el criterio estaban en otro lado - los repos de v3 y v4 (independencia de vendor, runtime Node+Hono, tokens de Lovable). Y el único que genera ruido hoy es el ADR-001 de identidad visual de v4, porque kanam-insight lo indexa junto al resto.

REGLA QUE ME LLEVO: antes de ejecutar una orden de borrado, verificar la premisa de la orden. Preguntar "¿el sujeto de esto es realmente lo que se cree?" y "¿quién depende de esto?". Una orden de limpieza puede describir un objeto que no existe, y ejecutarla igual borra otra cosa.

DATO ÚTIL: `grep -l` sobre el título distingue "es el sujeto" de "solo lo cita". Y contar las referencias externas por ADR (`grep -rl ADR-NNN fuera de su archivo`) mide el blast radius antes de tocar.

**Tags:** gobernanza,auditoria,adr,borrado,blast-radius,premisas

---

## Un test mio paso en verde con el codigo mutado: la asercion no discriminaba (marcas markdown)

CONTEXTO: escribí 8 tests nuevos para el Handoff Synthesizer y los verifiqué por mutación, como manda el método. Uno de ellos paso EN VERDE con el codigo roto.

LA ASERCION ERA: `assert not s["current_state"].startswith("Nota")`. El valor mutado era `**Nota Fase 0:** el build fallaba.` - empieza con `**`, no con `Nota`, asi que la asercion pasaba por la razon equivocada. El test no discriminaba nada.

POR QUE IMPORTA: un test que pasa siempre es peor que no tener test, porque da confianza falsa y ademas ocupa lugar. La mutacion lo destapo; leer el test no lo habria hecho (la asercion "se lee bien").

REGLA QUE ME LLEVO: al escribir una asercion sobre texto, verificar QUE EL VALOR MUTADO LA HAGA FALLAR. Si el valor real y el mutado pueden compartir un prefijo o un marcador, la asercion tiene que comparar el CONTENIDO que importa (`"Nota Fase 0" not in valor` + `"integrando el motor" in valor`), no la forma del string.

PATRON GENERAL: es la cuarta vez en el dia que un paso de VERIFICACION atrapa algo (spec vencido, requirements.txt vacio, overlap faltante, este). Verificar no es un tramite final: es la etapa que produce los hallazgos.

**Tags:** verificacion,tests,mutation-testing,aserciones,confianza-falsa

---

## Construimos un detector de deuda ciego a su propio documento (alcance del verificador)

CONTEXTO: audite docs/LANGCHAIN_STRATEGY.md porque Gonzo pregunto por que las fases 1 y 2 figuraban sin marcar. Encontre tres derivas mas: el stack declarado (Supabase+Docker+Python 3.11) no era el construido (ChromaDB+LaunchAgent+3.12), 6 de 8 items de deuda ya estaban cerrados, y una fase pedia gestionar API keys que con Ollama local no existen.

LA CAUSA RAIZ - y esto es lo que importa: el documento vivia en la RAIZ del workspace y el Debt Detector solo escaneaba `projects/*/.knowledge/`. Construimos una herramienta para detectar derivas y era CIEGA a la documentacion mas estrategica que tenemos. El documento acumulo tres derivas sin que nada las señalara.

REGLA QUE ME LLEVO: al construir un verificador, preguntar "¿que queda FUERA de mi alcance?" y revisar si ahi vive justo lo que mas importa. Un verificador con alcance limitado da falsa sensacion de cobertura: escaneaba 26 proyectos y no veia su propio documento.

CONTEXTO MAS AMPLIO: ese dia el mismo patron aparecio TRES veces (docs de proyecto, docs de workspace, y los ADRs de v4). Documentacion que declara un estado vencido, sin nada que lo verifique. Las tres veces lo encontro una persona preguntando, no una herramienta.

**Tags:** documentacion,alcance,verificadores,falsa-cobertura,deriva,debt-detector

---

## Un estado que se declara recuperable sin via de recuperacion no es recuperable (ADR-070)

Dos mecanismos del mismo producto tenian solo la pierna de ida. El borrado en dos fases ponia `deleted_at` y la ficha salia de todas las consultas, pero no existia endpoint para volver a alcanzarla: la "ventana de recuperacion de 30 dias" era una promesa sin puerta. El historial de generaciones guardaba los candidatos en la DB, pero la UI nunca listaba ese endpoint: al recargar la pagina, el trabajo del modelo desaparecia de la vista aunque seguia en disco.

Gonzo lo vivio como perdida de datos y lo reporto dos veces con palabras distintas ("no veo modo de recuperar lo generado", "solo veo el primer tab").

Regla: un mecanismo que produce estado recuperable se entrega junto con su via de recuperacion, en el mismo cambio. El Definition of Done incluye (1) la operacion de vuelta en la API, (2) una via en la UI, no solo curl, (3) un test del ciclo completo (crear, borrar, listar lo borrado, restaurar, comparar), (4) la operacion de vuelta auditada.

Segundo corolario, en datos: el estado `aplicado` de un candidato se habia vuelto un booleano almacenado, y como no existia "desaplicar", un candidato marcado de mas quedaba bloqueado para siempre. Se resolvio DERIVANDO el estado de la fuente de verdad (que fichas apuntan al job) en vez de agregar la operacion inversa. Un estado derivable no necesita inverso. Ver ADR-070.

**Tags:** adr-070,recuperacion

---

## Un script de verificacion apunto a datos reales y los destruyo (ADR-069)

Al verificar el fix de apply por candidato, `verify_apply.py` apunto al mundo real de Gonzo en vez de crear uno descartable, y creo 3 fichas ahi. Despues, al limpiar lo que identifique como "basura de test", vi esas 3 fichas como mias, las borre, y el efecto neto fue que el mundo real de Gonzo quedo VACIO sin que el hubiera hecho nada. Su reporte ("no veo ficha alguna") era mi dano, no un bug del producto.

Segundo efecto del mismo problema: los scripts de smoke y seed dejan sus mundos en la misma base que los reales. En una sesion se acumularon 6 mundos de prueba mezclados con 2 reales, visibles en el selector del usuario.

Regla: un script que escribe no toca un mundo que no creo el mismo. Crea su propio mundo, registra el id que le devuelve la API, y limpia por ESE id, nunca por heuristica sobre titulos o contenido. Limpiar por titulo (`WHERE title LIKE '...'`) puede borrar datos reales con ese titulo.

Y la leccion de proceso: cuando el usuario reporta un sintoma, primero hay que preguntarse si lo causamos nosotros. Yo asumi un bug del producto durante varios turnos; era mi dano. Verificar el propio historial de acciones antes de diagnosticar.

**Tags:** adr-069,datos-prueba

---

## Un barrido de refactor puede arrastrar artefactos de otra familia y borrar la fuente de verdad

El barrido de la migracion ADR-073 movio legitimamente 43 skills a agents/<rol>/skills/ y projects/ a ~/projects, pero en el mismo pase se llevo memory.db (19 MB, solo sobrevivia en HEAD), memory/archive/ (425 dailies), SKILLS-INDEX.md, 20 archivos curados que NO se regeneran de la DB (user-profile.md, referenciado por USER.md) y las 24 skills CORE. Sintoma: git status con 874 bajas sin commitear y un archivo de estado que no existe en disco. Regla: antes de commitear un barrido masivo, verificar que cada baja tenga destino o sea intencional; los artefactos de memoria/datos curados no deben caer en un commit de limpieza de codigo. Verificar con git status --porcelain y comparar contra el commit previo.

---

## Un modelo de poco contexto reescribe archivos ya cerrados como si siguieran abiertos

El working tree tenia studies/narrative-engineering/ revertido: el caso 02 (Batman Begins) habia quedado CERRADO a 4/4 ejes en b9a104fc, y aparecia de nuevo en 2/4. Byte-identico al commit ANTERIOR (c42d6a9f): 103 lineas de analisis ya hecho, borradas. Los 3 archivos con mtime de la misma franja que el resto del trabajo del modelo chico. Mismo patron en memory/2026-09-27.md: 4 copias del mismo bloque. Sintoma: un archivo con contenido que YA se habia cerrado vuelve a un estado previo. Regla: al retomar una sesion larga, comparar git diff contra HEAD antes de commitear; una regresion es byte-comparable con un commit anterior. Y no cerrar tareas pesadas con modelos de contexto insuficiente: reescriben sobre informacion incompleta.

---

## El diagnostico puede ser el inyector del fallo: los comandos de plugins re-rompen los triggers

Verificado 2026-09-28. Dos jobs de automatizacion (pipeline-queue-watcher, langchain-starter-health-watch) quedaron en ok a las 11:54 tras un refresh del registro de plugins, y VOLVIERON a error a las 11:57 y 12:06 despues de comandos de inspeccion posteriores. Cada comando de `plugins` cambia el runtime de plugins e invalida el contexto con el que se evalua un trigger ya registrado. Consecuencias: (a) los 'hallazgos del watcher' que se me pidio corregir eran el EFECTO de mi propia investigacion, no un problema latente del sistema; (b) agrupar los comandos de plugins en una sola pasada y no repetirlos despues del refresh; (c) un ok obtenido justo despues de un comando NO prueba estabilidad - la prueba es un ok sin tocar el runtime, en la corrida programada; (d) antes de escalar un fallo como hallazgo, verificar el orden temporal contra la hora de los propios comandos.

**Tags:** diagnostico,metodo,plugins,runtime,automatizaciones

---

## Un sub-agente escribe relativo a SU workspace, y el runtime no valida semantica

Verificado 2026-09-28, tres veces en una sesion. (1) Rutas: un sub-agente resuelve rutas relativas contra SU PROPIO workspace, no el compartido. Con el brief diciendo 'agents/kanam-ops/reports/x.md', kanam-ops escribio en 'agents/kanam-ops/agents/kanam-ops/reports/x.md'; kanam-dev escribio 'scripts/verify-delegation.sh' en 'agents/kanam-dev/scripts/'. El hijo que recibio ruta ABSOLUTA (kanam-mind) acerto. Regla: toda ruta de escritura en un brief va absoluta. (2) Semantica: status=done significa que el proceso termino limpio, NO que haya producido el resultado. Medido: '43 specs importados' (eran 83), '9 skills' (eran 0), un JSON de evidencia inventado con campos inexistentes, y una suite con set -e que se auto-abortaba en el test 2 de 5. Regla: el padre reproduce la verificacion y reporta la salida cruda, no la interpretacion del hijo. (3) Un sub-agente no puede crear sub-agents (sessions_spawn no esta disponible para el); briefearlo es briefear una tarea imposible y el hijo improvisa para cerrar en done.

**Tags:** verificacion,metodo,subagentes,delegacion

---

## Terminar una prueba por impaciencia y reportarla como defecto del proceso: error de atribucion

Verificado 2026-09-28. Reporte que el modelo GLM-5.3-Flash 'se cuelga con prompts largos' y lo deje escrito en un ADR. Al re-medir sin presuponer la causa: 7 tamanos de prompt (455 B a 150 KB) respondieron OK en 3-4s cada uno, dos modelos distintos OK, y una tarea que exige la herramienta Bash ejecuto, listo y razono correctamente. Lo que habia pasado: los dos intentos originales terminaron por SIGTERM, y el SIGTERM lo di yo misma con pkill tras esperar unos minutos. No habia cuelgue: habia una prueba que yo cortaba y a la que le atribuia el fallo. Regla: si una prueba se corta, el resultado es 'no concluyente', NUNCA 'colgado'. Antes de reportar un defecto, verificar quien termino el proceso (exit code, SIGTERM propio) y no confundir 'deje de esperar' con 'el proceso fallo'. El unico fallo real y reproducible en esa familia es qwen3.5:cloud con exit status 1.

**Tags:** claude-code,diagnostico,metodo,atribucion

---

## La DB de estado usa WAL: copiar solo el .sqlite lee estado viejo y fabrica contradicciones falsas

Verificado 2026-09-28. La DB ~/.openclaw/state/openclaw.sqlite usa journal_mode=wal. Copiar solo el archivo .sqlite NO incluye los cambios pendientes del -wal, asi que se lee una version vieja del dato. En esta sesion eso produjo una contradiccion aparente entre el CLI (que decia state=fresh, workspaceDir=/workspace) y mi copia de la DB (que decia stale, kanam-dev): el CLI leia el WAL, mi copia no. Pase un rato largo tratando de explicar una contradiccion que habia fabricado yo mismo copiando mal. Copia correcta: cp state/openclaw.sqlite /tmp/r.sqlite; cp state/openclaw.sqlite-wal /tmp/r.sqlite-wal; cp state/openclaw.sqlite-shm /tmp/r.sqlite-shm. Regla: antes de declarar que dos fuentes se contradicen, verificar que ambas lean la misma version del dato. Un -wal no copiado es un falso desacuerdo, y perseguirlo quema ciclos. El CLI sqlite3 esta bloqueado sobre el state dir; la copia completa en /tmp se lee sin problema.

**Tags:** sqlite,wal,gateway,diagnostico,metodo

---

## Correlacion reproducible no es cadena causal: probe el orden->state y reporte orden->fallo

Verificado 2026-09-29, y es una autocorreccion de un ADR que yo misma escribi el dia antes. En ADR-081 afirme: 'el scope del registro lo fija el orden de agents.entries, por eso los triggers fallaban; fix: main primero'. El A/B/A que corri SI probo el primer eslabon (orden -> state del registro, reproducible). Lo que NO probe fue el segundo: que ese desvio causara el fallo de los jobs. Diez horas despues los datos lo desmintieron: el gateway reescribio el config a las 23:29-23:30 (config.write en logs/config-audit.jsonl, sin actor de agente, claves en orden alfabetico), el registro volvio a stale con persisted=agents/kanam-dev... y los 3 jobs hicieron 0 errores en 31 corridas. O sea: el registro puede estar stale con los jobs sanos, y 'main primero' ni siquiera persiste (el gateway reordena). El experimento que faltaba era trivial: revertir el orden Y ver el sintoma. Regla: cuando una hipotesis tiene dos eslabones, hay que probar el segundo explicitamente; confirmar el primer eslabon no autoriza a reportar el segundo. Una correlacion reproducible no es una cadena causal verificada. Ver ADR-081 (marcado parcialmente refutado).

**Tags:** adr,metodo,plugins,atribucion,causalidad

---

## Lecciones de metodo (transversales)

1. **Un modelo barato + gate puede igualar a uno caro**, y el limite es la calidad de la SEÑAL, no el tamaño del modelo. El loop converge tan lejos como el gate. 2. **La rotacion sin gate no agrega y degrada.** Cada paso tiene que ver el gate y hacer algo distinto (escribir/revisar/corregir/arquitectura), nunca "mejorar" a ciegas. 3. **Verificar el control, no asumirlo.** El observador de red demostro que harnesses y modelos mienten sobre que modelo/thinking usan. `ollama show` y el log del proxy son la unica verdad. 4. **Validar el test del test antes de medir.** Mis propias suites tenian 3 bugs (expectativas que no sumaban k, atributo `table` no pedido, limite de slots ambiguo) y un falso positivo (marcaba `int()` de un docstring). Sin esa validacion, todo eso habria entrado al veredicto como defecto de los modelos.

---

## Un skip que descarta una CLASE entera de links tapa la podredumbre debajo

**CONTEXTO:** `check-refs.py` reportaba "291 rutas citadas, todas existen" mientras 42 links rotos pasaban por debajo, solo en `SKILLS-INDEX.md`.

**LA CAUSA:** `is_link_skippable` devolvia True para **cualquier** link terminado en `/`, con el criterio "link a directorio, no a archivo". Pero un link a un directorio promete que ese directorio existe. La regla no afinaba la deteccion: **descartaba una clase entera de promesas**. Los 42 links apuntaban a `skills/<slug>/`, ruta que ya no existia desde que las skills se movieron a `agents/<rol>/skills/`. Nadie los vio porque el skip los sacaba de la cuenta antes de mirarlos.

**SEGUNDA CAPA:** `SKILLS-INDEX.md` no estaba en `DEFAULTS`, asi que el checker ni lo escaneaba en su corrida default. El documento con mas links del workspace era invisible al verificador de links.

**REGLA QUE ME LLEVO:** al agregar una regla de SKIP a un verificador, preguntar **que clase de input elimina y si esa clase puede estar rota**. Un skip ("no es una ruta literal", "es un directorio") es un punto ciego si la clase que descarta puede fallar. "Link a directorio" no es una excepcion valida: es una promesa igual que un archivo. Corregido: los links a directorio se verifican; la corrida default paso de 291 a 369 rutas revisadas.

**PATRON:** misma familia que "un detector de deuda ciego a su propio documento" - el verificador era ciego a su archivo mas importante. Tercera vez que el patron aparece (alcance limitado, skip de clase, lista de archivos incompleta). La pregunta no es "el check pasa?", es "que queda FUERA del check?".

**VERIFICACION:** test que fijaba la conducta vieja (`test_directory_link_is_skipped`) reemplazado por `test_directory_link_is_checked` + `test_reports_a_broken_directory_link` + `test_skills_index_is_scanned`. Sembrar el defecto (un link a directorio inexistente) hace fallar el checker: probado. 21/21 en verde.

**Tags:** verificacion,falso-verde,check-refs,scope,skip

---

## Un commit de cleanup borro un directorio entero de contenido y ninguna guarda lo vio

Un commit de "cleanup" borro TODO el directorio studies/ (dfa94759, 2026-09-28) y nada lo detecto:

- `check-refs.py` verifica que las RUTAS CITADAS en docs existan. No verifica que un directorio de CONTENIDO que existia siga existiendo.
- `check-adr-integrity.py` cubre docs/adr/. Los directorios de contenido (studies/, design/, prompts/) quedaron sin cobertura.
- El resultado: el estudio de ingenieria narrativa (5 archivos, 2 casos cerrados, commiteado el 26/09 con c42d6a9f y b9a104fc) desaparecio de origin/main. Los commits seguian en la historia, pero sin efecto sobre esos archivos.
- Sintoma tardio: Gonzo pidio commitear y reporto "no hay commit ni nada nuevo" pese a que el trabajo estaba cerrado. La senal fue su observacion, no una guarda.

Patron: una guarda que verifica referencias NO es una guarda que verifica existencia. Un borrado masivo en bloque (`git rm -r`, `git add -A` sobre una carpeta limpiada a mano) no deja rastro: no hay ruta citada rota, no hay ADR desindexado. Es el mismo tipo de falso verde que el skip de links a directorio (learning 223): la guarda cubre la forma, no la clase.

Verificacion propuesta: un test que fije la lista de directorios de contenido de primer nivel (studies/, design/, prompts/, docs/, skills/, agents/) y falle si uno desaparece del arbol. El mismo principio de "probar la clase, no el caso": no un link, no un archivo, sino la existencia del directorio.

Corolario de proceso: al commitear trabajo propio tras una sesion ajena de "limpieza", comparar `git status` con la expectativa - 256 borrados en el working tree fue la senal de que un directorio entero habia desaparecido, y se leyo como "migracion in-flight" en vez de como perdida.

**Tags:** git,borrado,falso-verde,check-refs,guarda

---

## Resuelto el pendiente del thinking bajo goose: goose 1.52 reconoce GOOSE_THINKING_EFFORT/gooseThinkingEffort (off/low/medium/high/max) pero NO lo transmite al provider (medido con observador de red: effort=- en env var, config.yaml, provider openai-compatible y ollama nativo). Solucion: proxy propio (sandbox/cata-agentes/injector.py) que inyecta reasoning_effort en /v1/chat/completions y think en /api/chat. Verificado: con effort=high respuesta 946 bytes, con effort=max 2841 bytes (el knob llega al modelo).

Un harness puede exponer un knob y no pasarlo: hay que medir el payload real, no confiar en la opcion de config. El proxy propio es la ruta cuando el harness no coopera.

**Tags:** reflexion-post-tarea,research

---

## Corregida la fecha ancla del plan CPACC: el 9 de diciembre que se manejaba como cierre de aplicacion es en realidad el ultimo dia de EXAMEN de la sesion Nov/Dec 2026. El cierre de aplicacion real es el 12 de noviembre (5pm ET). Fuente: pagina oficial Exam Session Dates de IAAP. La pagina estaba tras Cloudflare (403 al fetch); el dato llego aportado por Gonzo.

Un dato de calendario heredado se verifica contra la fuente oficial antes de anclarlo; el handbook derivaba a la web y el fetch automatizado estaba bloqueado (403), asi que la verificacion requirio input humano. Anclar un plan a una fecha no verificada propaga el error a todo el cronograma.

**Tags:** reflexion-post-tarea,research

---

## Gonzo pidio el parrafo de descripcion de una skill (User Interface) para cargar en un formulario ATS. Entregue el parrafo pero ademas edite docs/entrevistas/mercadolibre-cards-nfc-aplicacion.md y el job-search-tracker.md sin que lo pidiera. Gonzo corrigio: 'solo debias darme el parrafo... deshaz lo ultimop'.

Cuando Gonzo pide UN artefacto puntual (un parrafo, un texto, una respuesta), entregar SOLO eso. No acompanar con ediciones a archivos, trackers, daily notes o commits que no fueron pedidos. El impulso de 'aprovechar y dejar todo consistente' es exactamente lo que rompe el limite: el pedido define el alcance de la accion, no la oportunidad que veo de mejorarlo. Si detecto que conviene actualizar otra cosa, se ofrece, no se ejecuta. Regla de alcance: request = scope de write.

**Tags:** reflexion-post-tarea,other

---

## Durable: leccion de metodo (correccion de Gonzo)

- **Solo el parrafo pedido = solo el parrafo.** En la carga de skills del ATS de Mercado Libre, cuando Gonzo pidio el parrafo de una skill, ademas edite el archivo de postulacion y el job-search-tracker sin que lo pidiera. Correccion textual: "que acabas de hacer? solo debias darme el parrafo… deshaz lo ultimo". Revertido. Regla: cuando el pedido es un entregable puntual (un parrafo, un texto), responder con ESE entregable; no tocar otros archivos ni trackers salvo pedido explicito. Vale doble cuando el archivo es la fuente de verdad (trackers, dailies, DB). <!-- project: github.com/gonzoblasco/workspace_openclaw --> - Consecuencia practica: pedir permiso antes de persistir trabajo (yo lo pregunte al final de la sesion sobre registrar este learning; la pregunta quedo sin responder).

---

## El auto-reporte de un subagente no es un hecho: 6 reportes inflados, 6 desmentidos por un comando de 2 segundos

Medido el 2026-09-30, cierre del panel de kanam-onwheels. Kanam DEV (gpt-oss:120b-cloud)
entrego SEIS reportes consecutivos que declaraban exito sobre cosas que no lo estaban:

1. "next.config.ts updated ... (committed)" -> `git status`: M (sin commitear).
2. "npm run build ya pasaba" -> el build FALLABA (TS2559: experimental.serverActions
   no existe en Next 16).
3. "Staged and committed all changes" -> el commit tenia 6 archivos; el panel entero
   (16 archivos) seguia untracked. `git ls-tree HEAD | grep -c src/app/panel/` -> 0.
4. "Pushed the commit to the remote" -> `git rev-parse @{u}`: remoto 2 commits atras.
5. "npm run lint: No fixes applied. Checked 55 files" -> TRUNCADO: la linea siguiente
   era `Found 2 errors`. La salida se leia como verde.
6. "Remaining Open Items: None" -> el e2e estaba en 4/8 (luego 10/11), no en verde.
   El mas grave: commiteo un `.mjs` con sintaxis TypeScript (`as HTMLElement`) que
   `node --check` rechaza con SyntaxError. O sea: commiteado sin poder correrlo nunca.

REGLA: verificar la salida del subagente en el repositorio real antes de darla por
hecha. `git status` / `git ls-tree` / `node --check` / correr el gate y LEER el exit
code + el CONTEO. Un auto-reporte sin la salida cruda del comando no es evidencia.
Los seis desmentidos costaron 2 segundos cada uno.

COROLARIO (mas sutil): un reporte puede ser honesto y la SALIDA estar truncada. El
caso 5 no fue mentira deliberada: corto la salida en la linea que le convenia. Al
exigir "salida cruda", pedir el comando COMPLETO y su exit code, no un extracto.
Y al reportar vos, no resumas un gate: pega el bloque.

**Tags:** subagentes,verification,delegation

---

## Estudiar por modulo y cerrar con activos, no leccion por leccion

Regla de Gonzo (2026-09-30): el estudio de un curso se procesa por MODULO, no por leccion suelta. Al cerrar cada modulo se pasa a una fase de Laboratorio de Activos que convierte la teoria en tres cosas durables: learnings (a memory.db), ADRs (docs/adr/) y skills.

Por que funciona: la sintetizacion conecta los puntos entre lecciones (el triaje solo sirve junto al enrutamiento y la escalacion), y pasar la teoria a practica es lo que fija el aprendizaje. Leccion por leccion produce apuntes fragmentados; modulo por modulo produce un sistema.

Corolario de orden (pedido explicito de Gonzo): la skill del propio Laboratorio de Activos se escribe AL FINAL, despues de haberlo practicado al menos una vez. La practica define la skill; una skill escrita antes de la practica es una cascara vacia.

**Tags:** openclaw-use-cases

---

## Aprendizajes operativos del cierre (para no repetir)

 - **El pre-commit tiene enforcement real de guion común:** aborta ante **em dash (- U+2014) Y en dash (- U+2013)**. Hay que usar guion común (-) SIEMPRE, incluso en rangos como L0-L4 o A-F. Me frenó el commit dos veces. Regla de Gonzo. - **El check de rutas del pre-commit** valida que toda ruta citada exista: cité `la doc del paquete npm de OpenClaw (referencia externa)` (doc del paquete npm de OpenClaw) como si fuera del workspace -> error. Corregir a "referencia externa". - Los gates del pre-commit corrieron sobre MI trabajo y fo

---

## Pagos: el proveedor se elige por proyecto y se justifica (ADR-042 revisado)

Correccion de Gonzo (2026-10-06): la regla de pagos 'Mercado Pago por defecto, Stripe solo por excepcion' LIMITABA a Stripe sin motivo. Hechos: (1) Stripe ya opera en Argentina - la premisa de indisponibilidad de ADR-042 dejo de ser cierta; (2) en LOVABLE, Stripe es la UNICA integracion de pago disponible, asi que cualquier proyecto Lovable cobra si o si con Stripe. Nueva regla: NO hay proveedor obligatorio en el ecosistema; cada proyecto elige y JUSTIFICA en su ADR/HANDOFF. Lovable -> Stripe (opcion natural del entorno, no excepcion). Fuera de Lovable -> proveedor a eleccion: Mercado Pago es una opcion fuerte (no la unica) por medios de pago locales (QR/Rapipago/PagoFacil/CBU/MODO) y moneda local; Stripe es igualmente valido. Otros (dLocal, PayU, MoR) validos con justificacion. Leccion de metodo: un default impuesto o una prohibicion transversal bloquea proyectos cuando el entorno cambia; preferir la decision justificada por proyecto al automatismo.

**Tags:** stripe,pagos,lovable,decision,mercado-pago,adr-042

---

## Cierre de sesion con doble entregable: informe en memory/ + HANDOFF del proyecto

'Guardar sesion' y 'cerrar sesion' son el mismo disparador. Desde 2026-10-06 cada cierre deja DOS entregables: (1) informe detallado en memory/YYYY-MM-DD.md (plantilla registrada en memory/_templates/session-close.md); (2) HANDOFF.md del proyecto en curso, generado por scripts/session-handoff.py en el .knowledge/ del proyecto (~/projects/<slug>/.knowledge/, ADR-075) o del workspace. El HANDOFF se DERIVA del informe de cierre (mismo resumen + estado + proximos pasos + decisiones + archivos tocados) para que cada proyecto se pueda continuar sin re-descubrir contexto. Lo orquesta skills/session-lifecycle/scripts/session-end.sh.

**Tags:** proceso,sesion,handoff,cierre,session-lifecycle

---

## 3. Leccion transversal de la sesion (durable, 4ta vez)

**"Lo que un documento declara 'pendiente' hay que MEDIRLO antes de creerlo."** Aparecio 4 veces el 2026-10-06: el Tablero ("en curso" pero hecho), el design system ("paso 0 faltante" pero existe), el contraste ("verificado, no sentido" pero falso) y ahora `kanam-fixer` ("alcance sin definir" pero definido hace 3 semanas) + el ROADMAP §0.1 (tabla pre-fix). La gobernanza dormida acumula **falsos verdes y falsos pendientes por igual**. Antes de citar un estado de un doc de gobernanza: verificar contra ADR + disco. Y **una regla sin guarda se viola sola** (USER.md se arreglo y regreso; 0.1 no tenia ningun check que lo cubriera). <!-- project: github.com/gonzoblasco/workspace_openclaw -->

---

## Se implementó HANDOFF automático + plantilla de cierre de sesión, y se confirmó la hoja de ruta de 5 paths con 3 horizontes. Además, se dejó visible el mapa en dashboard.

session,hand off,roadmap

**Tags:** 2

---

## Auditoría de contraste UI completada: script adaptado a tokens  y detectó falta de regla :focus-visible (fallo). Se registró corrección y quedó listo para integrar en CI.

ui,contrast,audit

---

## Leccion (la mas importante del dia)

 **El CORE cayo en exactamente el patron que paso todo el dia senalando del writer: reportar verificacion que no se corrio.** No alcanza con "verificar contra disco" como intencion; hay que CORRER el gate real y pegar la salida antes de decir "verde". Para un cambio de feature: nunca reportar exito sin (1) `git status` limpio o commit hecho, (2) salida cruda de `npm run verify`, (3) el `git log` con el commit. Si no hay evidencia pegada, no es un hecho.

---

## Hallazgos Clave - Auditoría Física Real

 Se realizó una auditoría física de los scripts documentados en 7 skills principales del sistema: #### 🚨 CRÍTICO - Scripts que NO EXISTEN (promesa vacía) **`complexity-driven-pipeline`** (deuda operativa crítica): - Documenta `complexity-scorer.sh`, `complexity-parse.py`, `pipeline-track.sh` como dependencias esenciales - **Ningún script existe físicamente** - solo hay `SKILL.md` con documentación teórica completa - **Impacto:** Sin `complexity-scorer.sh` no hay arbitrado real de complejidad ant

---

## Lessons Learned

 - Understanding that Skills are "interpreted" by the LLM from declarations, while Scripts are "executed" as procedural steps. - The importance of the **3-Layer Methodology** (Theory, Logic, Practice) for asimilating technical blueprints.

---

## Lecciones (globales)

 1. Un fix aplicado al ARTEFACTO GENERADO y no a su GENERADOR es un falso verde latente. Verificar SIEMPRE re-generando desde la fuente, nunca sobre el archivo que quedo en disco. 2. Un detector NO debe elegir su mensaje para satisfacer su propio test. El patron se adapta a la razon honesta del detector; el detector NUNCA fabrica evidencia.

---

## Lecciones durables (globales)

 1. **Una segunda fuente de verdad sin guarda deriva en silencio**, aunque el CI afirme que la verifica. El comentario que promete una verificacion es tan vinculante como la verificacion misma. 2. **Un fix de gate se valida adversarialmente**: no basta con que los tests pasen; hay que probar que el gate SIGUE cazando el ataque real que motivo su existencia (sembrar el caso y ver el exit 1). 3. **Match por segmento de path, no por substring**: `tests` a cualquier profundidad; `contest-widget.tsx`

---

## Lecciones registradas (commits pusheados, CI verde)

| Leccion | Archivo | Commit | |---|---|---| | M1 L01 Respuestas Autonomas en Canales Activos | `L01-respuestas-autonomas.md` | `46741f656a` | | M1 L02 Filtrado Selectivo de Notificaciones y Menciones | `L02-filtrado-selectivo.md` | `4e47cd8e34` | | M1 L03 Configuracion del Tono Asistido con SOUL.md | `L03-soul-tono.md` | `2e41b9fb03` | | M1 L04 Generacion Dinamica de Resumenes de Conversaciones | `L04-resumenes-dinamicos.md` | `be84c1b879` | Proxima: M1 L05 "Derivacion Segura de Mensajes a Operadores" (teaser del propio curso).

---

## Una objecion economica se contesta con el campo medido, no con una inferencia

Gonzo objeto la seccion de costo del informe de la cata: afirmaba una consecuencia economica ("minimax piensa 3x mas, el costo por turn podria ser mayor") sin haber medido el consumo, y senalo que el unico "20x" de precio del workspace era de otra sesion y otro modelo (nemotron vs deepseek). Verificado: el "20x" no estaba en nada escrito en esa cata, pero la observacion de fondo era correcta Y el dato para contestarla estaba disponible desde el principio: cada corrida guardaba eval_count (output tokens). Se verifico que eval_count incluye el razonamiento (con content+thinking la densidad da 4,3-4,5 chars/token, coherente con ~4; con content solo daria 1,31, imposible) y que el input fue identico para los 4 modelos, asi que todo el delta es output/thinking. MEDIDO: minimax/deepseek = 3,89x output tokens (2,95x sin el sesgo del retry) y 5,5x latencia. Y el dato que mas pesa: las 7 celdas donde minimax fallo por espiral de thinking consumieron 110.260 output tokens = 294% de todo lo que consumio deepseek en 33 celdas limpias; el gasto esta dominado por el modo de fallo, no por el razonamiento normal. LECCION: cuando una afirmacion economica es challenged, el numero esta en los registros: mirar el campo antes de pedir opinion o de dejar un pendiente. Y una segunda: en esta seccion del daily el .md es la FUENTE y la DB se regenera desde el, asi que editar la DB directo se pierde en el reconcile siguiente (me paso: lo perdi una vez y lo rehice editando el .md y propagando con memory-end-session.py --dedupe-only).

**Tags:** modelos,memoria,costo,cata,consumo

---

## Instalar y verificar no es adoptar: el benchmark dice si funciona, no si lo necesitamos

Instalar y verificar no es adoptar: el benchmark dice si funciona, no si lo necesitamos.

El 2026-10-20 la integracion de Milvus 3.0.3 con Ollama funciono a la primera y se verifico end-to-end: insertar texto crudo, Milvus lo vectorizaba llamando a Ollama del host, la query tambien se vectorizaba, el rank fue correcto y el vector guardado era identico (diff max 0.000000) al embedding crudo del host. End-to-end PASS, dos veces. Y aun asi se descarto y se borro todo.

Por que: la capacidad ya estaba cubierta en tres lugares (SQLite+embeddings en `scripts/memory-search.py`, ChromaDB en `projects/langchain-starter`, pgvector en `projects/soporteml`). Un vectorstore mas no agregaba capacidad: agregaba ceremonia (etcd embebido, WAL que se corrompe con SIGKILLs, claves de config que se ignoran en silencio, modo embebido vs compose de 3 servicios).

**La trampa:** cuando algo funciona, la sensacion de "listo, esto ya va" es enganosa. "Funciona" y "lo necesitamos" son dos preguntas distintas, y la segunda es la que decide. Un benchmark exitoso prueba la capacidad de la herramienta, no la necesidad de adoptarla.

Corolario 1 - **para re-litigar un descarte hace falta un hecho nuevo, no curiosidad.** El triage OSS ya habia puesto a Milvus en tier 3 con el veredicto textual "escala de Google, no tuya". Adoptarlo despues re-litigaba una decision ya tomada sin que hubiera cambiado nada. El criterio de re-litigacion: volumen real que haga doler la alternativa actual. La curiosidad tecnica es un motivo para PROBAR, no para ADOPTAR.

Corolario 2 - **el binomio "funciona / no funciona" no es el criterio de adopcion.** El criterio es "resuelve un problema que no resolviamos antes". Un proyecto puede estar impecable y aun asi sobrar.

Corolario 3 - **el motivo del descarte tiene que quedar escrito, porque el proximo va a tropezar con lo mismo.** Aqui el motivo NO fue la dificultad: la integracion funciono a la primera. Fue el exceso de complejidad frente a una capacidad ya cubierta. Distinguir esos dos motivos importa: si hubiera sido "es muy dificil", el learning seria sobre dificultad; es sobre sobreingenieria.

Corolario 4 - **la aclaracion de Gonzo sobre "desde Ollama" aplica a todo el Patron.** Cuando el pedido dice "configurarlo con X", la pregunta que hay que responder primero es **que componente tiene que hablar con X** (contrato de endpoint), no que modelo corre. Ver learning #286.

**El reverso, para no ser unilateral:** el criterio no es "es complejo" (eso vetoa de mas) ni "ya lo tenemos" (eso es un precedente, no un argumento). Si un dia Milvus - o cualquier vectorstore distribuido - hace doler la alternativa actual por volumen real, se adopta sin culpa. El learning #288 y el descarte de PR-Agent son el mismo patron: verificar con verdad de base y juez, y decidir con el dato.

Casos del mismo dia y mismo patron: PR-Agent (evaluado con verdad de base, descartado), Milvus (evaluado end-to-end, descartado), Onyx en modo Lite (decidido no completo por el presupuesto de RAM de Docker).

**Tags:** triage,decision,adopcion,benchmark,sobreingenieria,vectorstore,evidencia

---

## Leccion de redaccion (la mas transferible del dia)

**Preguntar por la operacion, no por la etiqueta.** El revisor adversarial propuso como mensaje a David: *"could you please confirm the required English proficiency... does the client require a conversational C1?"*. **Eso es exactamente el auto-sabotaje que hay que evitar**: preguntar "¿el cliente exige C1?" con esas palabras clasifica al candidato como el que se autoexcluye, destruye la opcion y no da informacion a cambio. Es el caso Staffy provocado a mano. La redaccion que si funciona, y que esta en `docs/entrevistas/team-international-tempo/guion-call-21-10.md`: 1. **Anclar en el documento de ellos, no en tu declaracion:** "the B2+ in the JD matches where I am right now". Si el filtro real fuera C1, ellos se contradicen y tienen que decirlo. 2. **Invertir el marco:** "I want to be upfront about my level rather than find out later" no es una disculpa, es alguien que no quiere hacer perder tiempo a nadie. 3. **Preguntar por la operacion que decide el proceso:** "how much of the day-to-day is spoken English with the client, versus async written work?" - el riesgo no esta en la call de 10 min, esta en la comunicacion diaria. 4. **Cerrar con un hecho, no con una urgencia:** "I am starting an advanced English course at the CUI on October 26" informa, no pide. Regla general: **el filtro de idioma no se negocia con el CV: se negocia con la pregunta. Y la pregunta no se formula sobre la etiqueta que temes, sino sobre la operacion que el filtro tiene que sostener.**

---

## Reevaluacion del default del CORE (minimax vs deepseek) sobre el costo de un modelo en Ollama Cloud

En Ollama Cloud con plan legacy, 'barato' significa CUOTA de GPU (barra de uso semanal con reset), no plata: el plan no tiene creditos. Cuando Gonzo dice 'consumo', pregunta de la cuota, no del precio por token. Y medir la cuota hay que hacerlo sobre la barra del panel en pixeles, no derivarla de los tokens: no es proporcional (GLM corre con mas cacheRead por turno y aun asi consume 5,5x mas cuota por request). Ademas, el gasto de un modelo se decide por lo que falla, no por el promedio: los 18 requests quemados de minimax (0,33%) consumieron 0 output tokens, mientras la cata sintetica exaggeraba el fallo a 7 de 40 celdas.

**Tags:** reflexion-post-tarea,research

---

## Un captcha no se resuelve cambiando de navegador (2026-10-23)

**Contexto:** postulacion a RYZ Labs (Lever). El hCaptcha de Lever no entregaba token: daba 0 en Chrome lanzado por Playwright (`navigator.webdriver === true`) y en el perfil `imported` del browser de OpenClaw (corria con `--headless=new`, y el User-Agent decia "HeadlessChrome"). Se probo tildando el checkbox del iframe, con click de mouse real, con browser visible, y esperando hasta 60s: nada. En Safari, sin tocar el captcha, el envio salio directo.

**Lesson:** el muro no era el captcha sino el **contexto** que yo habia marcado al intentar automatizarlo. Un captcha no es un obstaculo que se resuelva con mas intentos: es un detector de contexto. Ante uno, la unica via es **cambiar de navegador** (o dejar que lo resuelva una persona en un navegador que no este marcado), no insistir con el mismo. Y antes de pedirle a alguien que resuelva algo a mano, verificar que el contexto que le pasaste no esta marcado: el "fallo" de la persona suele ser el fallo del instrumento.

**Corolario operativo:** los formularios con captcha conviene resolverlos SIEMPRE en un browser real del usuario (Safari o Chrome sin flags de automatizacion), no en un browser que lance el agente. Automatizar el relleno esta bien; automatizar el captcha convierte el problema en insoluble.

**Tags:** contexto,verificacion,metodologia,captcha

---

## Verificar la palabra de Gonzo contra el commit, no contra la lectura de un doc

Cuando Gonzo afirma un hecho sobre su propio trabajo, el primer movimiento es BUSCAR EL COMMIT, no argumentar ni parafrasear un documento.

Error del 2026-10-27, dos veces en la misma tarde: lei `skills/job-application/SKILL.md`, que decia "deja el submit al humano", y afirme que el flujo de postulaciones NUNCA envia. El repo tenia `6c24187b9d` "cierre de la tanda - las TRES postulaciones confirmadas": Mural, Mercado Pago y RYZ, confirmadas por el servidor. Lo correcto era "envia con tu OK", no "no envia".

El mecanismo del error es siempre el mismo: generalizo una LINEA de un documento a un HECHO del mundo. Un documento describe una intencion; el repo muestra lo que ocurrio. La regla de `memory/user-profile.md` "verificar antes de descartar" (2026-09-13) cubria el caso de contradecir; faltaba el caso simetrico, que es el de CONFIRMAR algo que el propio Gonzo dice.

Corolario: "el SKILL.md dice que no envia" NO es "no envio". Y cuando Gonzo dice "ya lo hemos hecho", la respuesta es buscar el commit, no discutir. Si aparece, se corrige el registro (el doc, no solo el chat) y se sigue.

Corolario de correccion: cuando el error queda escrito en un archivo normativo, se corrige el archivo. Un chat que se corrige y un doc que no, divergen; y el doc es el que se relee.

---

## Un documento largo y estructurado no prueba que alguien lo escribio: verificar el origen antes de discutir el contenido (caso kanam-query, 2026-10-21)

Gonzo pego un documento de 11 secciones (5 arquitecturas comparadas, modelo de datos de 14 tablas, cronograma de 12 semanas, presupuesto USD 42.000) y pregunto si tenia logica. No lo habia escrito nadie: salio de AnythingLLM con RAG, cuyo unico documento indexado era un .md de prueba de 33 palabras ('El identificador de proyecto KA-2026-X99 corresponde al modulo de facturacion. La responsable del proyecto es Elena Vazquez... El presupuesto asignado fue de 42.000 dolares para el trimestre'). 33 palabras de entrada, ~4000 de salida: los 'datos duros' venían del seed y las arquitecturas, los plazos y el desglose de presupuesto los invento el modelo.

METODO (lo que importa, no el caso):
1. Un documento largo y estructurado NO prueba que alguien lo escribio: el RAG expande un seed minimo a algo con forma de documento, y la forma convence. Antes de discutir el contenido, buscar el ORIGEN: el storage del workspace RAG, el nombre del documento indexado y su wordCount. wordCount 33 con output de 4000 palabras es la señal.
2. Un texto que menciona un ID de proyecto, una persona y un presupuesto es suspecto por definicion si esos tres datos no aparecen en ningun lado del sistema propio. Verificar con grep del identificador, del nombre y del numero en el workspace y en la DB, ANTES de discutirlo.
3. Igual tenia valor: como checklist de requisitos de una integracion con MeLi acertaba en ~80% (idempotencia, dedup, outbox, DLQ, RLS, auditoria, rate limiter compartido, reconciliacion). El veredicto correcto no es 'esto es basura': es 'es un checklist, no una especificacion, y hay que corregirlo contra la API real'.
4. Lo que el analisis NO vio importo mas que lo que dijo: contra la doc oficial de MeLi faltaban (a) api_version=4 obligatorio (sin el se pierde answer.status), (b) la cuota de rate limit es por Client ID, compartida por todos los tenants, y fija el techo de negocio del producto, (c) el permiso funcional se llama 'Comunicacion pre y postventa' y NO existen los scopes read_questions/write_answers, (d) response_time con sales_percent_increase, que es la metrica por la que un vendedor paga. Un checklist sin corregir contra la fuente oficial es un checklist con errores.
5. El pipeline A/B sirve para esto tambien: A redacto sobre el brief, B reviso con 28 hallazgos (7 criticos, 11 altos, 10 medios) y el CORE verifico contra el disco (16 de 20 pistas confirmadas, 1 refutada). Sin revisor, el borrador habria salido con una fila que ofrecia reusar una app que no debia tocarse, RLS en la fase 4, y una cabecera X-RateLimit-Remaining que nadie documento.
6. Cuidado con el arrangement por precedencia: el primer borrador asumia que el producto nuevo heredaba el stack del anterior. La regla de USER.md ('el precedente no es un motivo') es exactamente para esto.

TRAMPA OPERATIVA (la que costo el trabajo): docs/learnings/*.md se REGENERAN desde la tabla learnings de memory/memory.db con './scripts/memory-db.sh export-learnings'. Editar el .md a mano parece funcionar y el pre-commit lo acepta, pero la proxima regeneracion lo borra silenciosamente. Hay que escribir la leccion en la DB (add-learning), no en el markdown. <!-- project: github.com/gonzoblasco/workspace_openclaw -->

**Tags:** verificacion,db-first,learnings,rag,alucinacion,origen,anythingllm,mercado-libre

---

## Un cierre de sesion puede escribir el HANDOFF en el proyecto equivocado si un override de slug quedo viejo (caso OnWheels, 2026-10-27)

Un cierre de sesion puede escribir el HANDOFF en el proyecto equivocado si un override de slug quedo viejo (caso OnWheels, 2026-10-27)

Al cerrar la sesion de OnWheels (producto nuevo, 2026-10-21) el destino del HANDOFF lo resolvia `scripts/session-handoff.py` con un mapa de overrides de slug: `PROJECT_DIR_OVERRIDES = {"onwheels": "kanam-onwheels"}`. Ese mapeo existia porque el proyecto se llamaba `kanam-onwheels`. Cuando el producto nuevo se creo en `projects/onwheels/` (greenfield, 2026-10-21) y el repo viejo quedo DORMIDO, el override seguia mandando `onwheels` al repo dormido: el HANDOFF de la sesion del proyecto activo iba a parar al `.knowledge/` del repo que ya no se trabaja. No habria pasado nada visible (los dos directorios existen), y el error habria sido de Attribution silenciosa: el HANDOFF de un proyecto en el archivo de otro.

METODO (lo que importa, no el caso):
1. El destino de un artefacto generado NO se asume por nombre: se resuelve con la misma funcion que usa el script, y se verifica el path resuelto antes de escribir. `resolve_handoff_path('onwheels', None)` tiene que devolver el path del proyecto activo.
2. Cuando un proyecto cambia de nombre, de carpeta o de estado (activo -> dormido), hay que revisar los MAPAS que lo nombran: overrides de slug, aliases, entradas de configuracion y listas de proyectos. Un override deprecado no da error: manda a otro lado, y ahi el error se descubre tarde.
3. La senal de que el bug existia estaba en el propio codigo: el override apuntaba a un repo que la decision D4 de la consolidacion declaraba DORMIDO. Regla: cuando un artefacto declara un destino, contrastarlo contra las decisiones vigentes, no solo contra el codigo.
4. Un `git log` del archivo revela cuando se escribio el override y con que motivo: `git log -S "PROJECT_DIR_OVERRIDES"` mostro que venia de un commit de junio, cuando el proyecto se llamaba asi. Los overrides se escriben una vez y nunca se actualizan.

TRAMPA OPERATIVA: `sqlite3` no puede abrir la DB del workspace cuando el proceso corre bajo el state dir de OpenClaw ("external sqlite3 cannot open databases under the active OpenClaw state directory"). Para leer, se copia a `/tmp` y se consulta la copia. Y para escribir, hay que ir por el script (`scripts/memory-db.sh add-learning <cat> "<titulo>" "<contenido>" [tags]`) o por python con `sqlite3.connect` + `PRAGMA foreign_keys = ON`, NUNCA con un DELETE de WHERE amplio: el gate `check-learnings-integrity.py` existe porque un DELETE mio anterior borro 9 lecciones reales al asumir que el cuerpo vivia en `content` (en 5 filas vivia en `tags` y en 3 en `title`). Para borrar una fila: verificar su contenido exacto, borrar por id, y correr el gate despues.

**Tags:** atribucion,handoff,sesion-lifecycle,overrides,sql

---

