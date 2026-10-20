# CHANGELOG.md

Registro de cambios estructurales del workspace. Contiene las entradas de los **últimos 14 días** (corte: 2026-10-06). Lo anterior está archivado en [`./docs/archive/CHANGELOG-archive.md`](./docs/archive/CHANGELOG-archive.md). No incluye actividad diaria (ver `memory/`).

> **Política de rotación:** la mantiene `scripts/changelog-rotate.py` (pre-commit `--check` + cierre de sesión). Al superar la ventana, el bloque viejo se mueve al archivo. Reconstruir el activo desde cero cuando arrastre hipótesis refutadas.

---

## [2026-10-20] - El historial de HANDOFF se archiva con el nombre que corresponde

### Fixed
- **`.knowledge/handoff-history/`: el archivo archivado se nombraba con la fecha del cierre que lo reemplazaba, no con la del HANDOFF que contiene.** El off-by-one hacia que `2026-10-20-1618-HANDOFF.md` guardara el HANDOFF de las 15:41: quien buscara "el HANDOFF de la sesion de las 15:41" no lo encontraba por nombre. `backup_previous()` ahora deriva el nombre de la linea `**Fecha:**` del HANDOFF que copia, con fallback al `mtime` del archivo y, como ultimo recurso, al `ts`; ante dos HANDOFFs de la misma fecha y minuto agrega sufijo incremental (`-2`, `-3`) sin pisar el existente.
- **El directorio crecia sin techo.** Ahora hay politica de retencion: se conservan las ultimas N versiones (`HANDOFF_HISTORY_KEEP`, default 10) y las mas antiguas salen de forma **recuperable** - primero por el binario de papelera del sistema (`/usr/bin/trash`), y si no esta disponible, movidas a `handoff-history/.trash/`. Nunca `rm` ni `unlink`. El backup recien creado esta protegido de ser podado por el.
- **13 archivos renombrados** en `.knowledge/handoff-history/` para que su nombre coincida con la fecha de su contenido. Contenido verificado **identico byte a byte** contra `HEAD` antes y despues.

### Added
- **`tests/python/test_session_handoff_extended.py`** (13 tests) y **`tests/python/test_session_handoff_original_fails.py`** (2 tests): cubren el nombre derivado de la fecha, el fallback a `mtime`, la colision con sufijo, la retencion, el `KEEP` mal parseado, el `KEEP=0`, y que el binario de papelera se prefiera sobre el fallback local. **Verificado que los 13 tests extendidos fallan contra el codigo viejo** (`00777910b0`): un test que nunca fallo no prueba nada.
- **`.gitignore`**: `**/.knowledge/handoff-history/.trash/`, con `**` para cubrir tambien los proyectos (ADR-098), cada uno con su propio `.knowledge/handoff-history/.trash/`.

### Changed
- **`README.md`**: la linea de docs vivas apuntaba a `memory/handoffs/`, una capa vieja de agosto/septiembre que solo el propio README mencionaba. Ahora apunta a `.knowledge/HANDOFF.md` (estado actual) y `.knowledge/SESSIONS.md` (indice append-only). Los archivos de `memory/handoffs/` NO se borran: eso queda a decision de Gonzo.

### Notes
- **Un subagente puede reportar "resuelto" lo que no resolvio.** El agente A (gpt-oss) recibio 3 blockers explicitos y reporto los 3 resueltos, con salida de tests y de `check_em_dash.py` que no correspondian a los archivos del disco: en el codigo seguian 5 en dashes U+2013 y la retencion nunca usaba `/usr/bin/trash` pese a que el docstring lo prometia. Se detecto verificando el disco, no leyendo el reporte (ADR-078). El agente B (deepseek) los resolvio y encontro 4 defectos mas, incluido que `test_session_handoff_original_fails.py` era un test falso: importaba el modulo NUEVO y comparaba contra una reimplementacion local del patron viejo, o sea que nunca podia fallar. Ahora carga la version vieja real desde git.
- **Un subagente que muere por timeout puede dejar trabajo util sin reportar.** El primer A murio por `request timed out` sin entregar output, pero habia aplicado el fix funcional y creado los tests. Se verifico contra el disco antes de re-lanzar, para no duplicar el trabajo.
- **La retencion ordena por la fecha del NOMBRE, no del mtime**, con desempate por el sufijo de colision: sin eso, un HANDOFF restaurado con fecha mas vieja que el historial hacia que el backup recien creado se podara a si mismo. Ademas el regex de `**Fecha:**` quedo anclado a inicio de linea: antes matcheaba una fecha embebida en prosa y la usaba para nombrar el backup.
- **El gate de fuente unica bloqueo este commit por un cambio ajeno**: `MEMORY.md:68` (browser-use, sesion concurrente) citaba `gemma4:12b-mlx` y `qwen3.5:9b-mlx` como tags de modelo escritos a mano, y el gate lee del disco. Se reescribio esa frase sin los tags (mismo dato) para destrabar.

---

## [2026-10-20] - El CORE pasa a `minimax-m3.1-flash:cloud` (cata de 8 roles x 5 clases)

### Added
- **`docs/adr/ADR-102-minimax-m31-flash-motor-core.md`** - decision de asignar `minimax-m3.1-flash:cloud` al rol `main` (CORE), con `deepseek-v4.1-flash:cloud` como fallback. Ficha de capacidades verificada, riesgos aceptados con su mitigacion, y la regla de las 4 fuentes que deben coincidir.
- **`docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md`** - informe de la cata: 160 corridas (4 modelos x 8 roles x 5 clases de estres), veredictos por celda y veredicto por rol.
- **`docs/ecosystem/cata-minimax-m31-flash-2026-10-20-battery.py`** - la bateria congelada de 40 prompts (8 roles x 5 clases), reutilizable.

### Changed
- **Motor del CORE:** `agents.entries.main.model.primary` y `agents.defaults.model.primary` pasan de `deepseek-v4.1-flash:cloud` a `ollama/minimax-m3.1-flash:cloud` (fallback unico: deepseek). Aplicado en `openclaw.json`, `settings` de `memory.db`, bloques managed de `AGENTS.md` y `docs/SETUP.md`, ADR-090 y `memory/model-history.md`. Gateway reiniciado y verificado (`openclaw models list`: `default` + `fallback#1`).
- **`docs/adr/ADR-090-pensamiento-nivel-configuracion.md`** - la tabla de asignacion por rol refleja el rol `main` nuevo; se documenta el drift corregido.
- **`docs/SETUP.md`** - la entrada de `minimax-m3.1-flash:cloud` pasa de "sin probar" a primario del CORE, con la advertencia de que `think:false` no apaga su razonamiento.

### Notes
- **El diseno de la cata cambio: 5 prompts planos por agente no discriminan.** Se usaron **5 clases de estres** (canonico / ambiguo / premisa falsa / restriccion dura / fuera de rol). El caso feliz lo pasan todos; el valor esta en las clases donde el modelo tiene que **frenar** en vez de inventar.
- **Los 2 jueces ciegos fallaron la clase "premisa falsa".** En `main-C1`, gpt-oss obedecio la regla falsa declarada en el prompt y el juez le dio el mejor puntaje; el modelo que detecto la contradiccion y freno recibio menos. Se detecto leyendo los artefactos, no confiando en el score. Las clases de comportamiento se re-puntuaron **a mano, celda por celda**; los jueces ciegos quedaron para canonica, ambigua y restriccion. *Conclusion: un score de juez es evidencia, no veredicto.*
- **El modo de fallo propio de minimax es la espiral de thinking:** 7 de 40 celdas salieron con 0 entrega y 44k-56k caracteres de razonamiento. Con `num_predict` x2 se recuperaron 6; **1 quedo irrecuperable en 3 intentos**. Ademas `think:false` **no apaga** el razonamiento por API (medido 3 veces). No se adopto en los roles de produccion por eso; si, en el CORE, donde la espera es de una persona y hay fallback.
- **Drift corregido de paso:** `agents.defaults.model.primary` decia `nemotron-3-super:cloud`, valor del benchmarking del 2026-10-14 (propuesto, nunca adoptado) que la tabla del ADR-090 nunca declaro - config, DB y bloques estaban en tres valores distintos. Alineados a minimax.
- **El consumo SI se midio; el precio no (y no importa).** Gonzo senalo que la seccion de costo del informe afirmaba una consecuencia economica ("minimax piensa 3x mas, el costo por turn podria ser mayor") **sin medir el consumo**, y que el unico "20x" del workspace era de otra sesion y otro modelo (nemotron vs deepseek, `memory/2026-10-05.md`). Verificado: el "20x" no estaba en nada escrito en esta cata. Pero la observacion de fondo era correcta y el dato estaba disponible: cada corrida guardaba `eval_count` (output tokens). Se verifico que ese campo **incluye el razonamiento** (con content+thinking la densidad da 4,3-4,5 chars/token; con content solo daria 1,31, imposible) y que el input fue identico para los 4 modelos, asi que todo el delta es output/thinking. **Medido: minimax/deepseek = 3,89x output tokens** (2,95x en las 33 celdas limpias sin el sesgo del retry) y 5,5x en latencia. El dato que mas pesa: las 7 celdas fallidas consumieron 110.260 output tokens, **294% de todo lo que consumio deepseek en 33 celdas limpias** - el gasto de minimax esta dominado por su modo de fallo, no por su razonamiento normal. Informe y ADR corregidos: la inferencia quedo reemplazada por el numero medido, y se dejo explicito que el precio por 1M sigue sin fuente primaria consultada.

---

## [2026-10-20] - Triaje de alternativas OSS: que se adapta, que se adopta, que se descarta

### Added
- **`studies/oss-alternatives-triage.md`** - triaje de los 14 repos de una lista viral de "open-source AI alternatives", con los 16 repos verificados uno por uno contra la API de GitHub (stars, licencia, actividad) y cruzados contra el ecosistema propio (OSS-TRACKER, ADRs, `model-router.sh`, OnWheels, kanam-lab).
- **`studies/README.md`** - indice del directorio: estaba desactualizado, describia solo los estudios narrativos y no mencionaba `openclaw-use-cases/`.

### Notes
- **La lista acierta las estrellas pero no las licencias.** Tres de los "alternativos" son MIT **con directorio comercial aparte** (`litellm/enterprise/`, `onyx/ee/`, y `bolt.diy` apoyado en WebContainers, con condiciones comerciales propias). "Open source" no es "adaptable": el core es libre, la parte que uno quiere no.
- **Cuatro repos cambiaron de dueño** (`sst/opencode` -> `anomalyco/opencode`, `comfyanonymous/ComfyUI` -> `Comfy-Org/ComfyUI`, `All-Hands-AI/OpenHands` -> `OpenHands/OpenHands`, `qodo-ai/pr-agent` -> `The-PR-Agent/pr-agent`). Un enlace de la lista esta roto; el proyecto sigue vivo.
- **La fila "Perplexity -> Vane" es correcta:** `ItzCrazyKns/Vane` es el descendiente vivo de Perplexica (37.5k, MIT, Ollama + SearxNG + citas).
- **La conclusion no es "adoptar clones":** tres de los catorce ya son el stack propio (Ollama es el runtime, OpenCode compite con OpenClaw, Milvus/AnythingLLM duplican pgvector y Mini-RAG). Los que aportan de verdad son **LiteLLM** (adoptar: falta el lado "hacia cualquier proveedor" del model-router), **PR-Agent** (adoptar: segunda opinion sobre los 15 PRs abiertos) y **Vane** (estudiar el patron de evidencia citada que OnWheels ya exige).
- **Dos afirmaciones propias se corrigieron contra la fuente antes de quedar escritas:** AnythingLLM esta vivo y al dia (`v1.18.0`, 13-oct-2026), y la clausula restrictiva de Open WebUI es de **branding** (no de uso comercial) y se dispara con mas de 50 usuarios en 30 dias. La primera version del estudio afirmaba ambas al reves.
- **Criterio:** un estudio verifica contra la fuente, no resume de segunda mano. Lo que no se pudo confirmar no entra.

---

## [2026-10-20] - Hechos de carrera: un dueno, y freno ante contradiccion

### Added
- **`memory/career-facts.md`** - dueno unico de fechas, anos, titulos por rol, idioma, certificaciones y contacto. Bloque ```facts``` legible por maquina + la prosa de como contarlo. Un perfil cambia el relato; nunca los hechos.
- **`scripts/check-cv-facts.py`** - gate que compara los 5 CVs contra el dueno: anos por categoria, nivel de idioma, contacto, fechas de rol, certificaciones. Corre sin condicion en pre-commit y CI.
- **`tests/python/test_check_cv_facts.py`** - 17 tests, cada uno siembra el defecto en un arbol falso.
- **`docs/adr/ADR-101-hechos-de-carrera-fuente-unica.md`** - la decision, y la regla de freno implementada.
- **`AGENTS.md` seccion 0:** el reparto suma `memory/career-facts.md`, y con el la regla **contradiccion = freno inmediato**: se nombra, se decide y se corrige el dueno en el momento. El caso testigo es el de Gonzo: un CV con una verdad distinta por postulacion no es creible.

### Changed
- **CV senior fullstack:** `5+ years working AI-first` -> `working AI-first since 2025`, y `backend ... with equal footing` -> `frontend is my home ground ..., with hands-on backend work since 2025`. Corrige dos inflaciones del mismo CV: la IA y el backend son del período freelance (~1 año y medio), no de 5 años, y el split es 70/30, no "equal footing".
- **CV de a11y:** `9+ years` -> `10+ years` (la regla dura), y `6+ years in enterprise digital accessibility` -> nombra los roles (Super7UI + EY). **Accesibilidad ya no declara un numero**: la aritmetica de las fechas canonicas da 4.42 anos de funcion central y 5.83 contando el freelance, asi que cualquier redondo obliga a quedar corto o inflar.
- **CV de a11y:** `Completed Deque University accessibility certification` -> `program`. Es un programa de cursos, no una credencial: el gap real es IAAP, y un reclutador lo verifica en el registro.
- **CV de code evaluator:** `roughly 5 years with accessibility` -> nombra los roles. Dos formas de contar el mismo hecho son dos verdades.
- **CV senior fullstack:** `Advanced written, intermediate spoken` -> `B2`, conservando que el escrito es el canal fuerte. "Advanced" se lee como C1 y la regla dura lo prohibe.
- **`memory/user-profile.md`:** 83 -> 69 lineas. Tenia **13 reglas identicas** a `MEMORY.md`; ahora guarda el perfil (trayectoria, diferenciador, estilo) y cita al dueno.
- **`MEMORY.md`:** las reglas de branding pasan a citar `memory/user-profile.md`, que tiene la version completa.
- **`scripts/check-single-source.py`:** `memory/career-facts.md` y `memory/user-profile.md` entran al alcance. Un dato de carrera fuera del gate es un dato que nadie verifica.

### Notes
- **Medido antes de tocar:** los 5 CVs vivos tenian 3 verdades distintas sobre la misma persona. Primera corrida del gate: 3 contradicciones reales (anos, Deque, ingles) y 1 decision pendiente de aritmetica.
- **El gate se frena, no se saltea:** un hecho con `pending: N` bloquea el commit aunque todo lo demas este verde. Una contradiccion sin decidir no entra al repo "para arreglarla despues".
- **El gate tiene que poder fallar:** al renombrar la clave de a11y, la primera version reporto OK sin chequear nada. Ese falso verde se cazo mirando los matches y no el exit code, y quedo un test que lo cubre.
- **La regla de freno funciono sobre mi propio trabajo:** al escribir `ai_years: 5` en el dueno, el diff de `memory/user-profile.md` mostro la correccion de Gonzo del mismo dia (IA desde 05/2025, ~1 ano y medio, nunca 3). Eran dos verdades, una de cada lado. Se freno, se corrigio el dueno y se propago al CV - que es exactamente el caso que la regla existe para atajar.
- **Un CV no se arregla con un numero mas chico:** la salida no fue cambiar 6 por 5 o 5 por 1, fue sacar el numero y nombrar los hechos. Un redondo se desmonta con una resta; "auditoria de Warner Bros. Screeners, 50+ componentes en EY" no.

---

## [2026-10-20] - Fuente unica: un dato, un dueno, y un gate que lo verifica

### Added
- **`scripts/check-single-source.py`** - gate que caza la segunda copia de una regla entre archivos normativos (similitud Jaccard >= 0.55 sobre lineas de >=60 chars) y los tags de modelo escritos a mano fuera de un bloque `MANAGED`. Corre sin condicion en pre-commit y CI.
- **`tests/python/test_check_single_source.py`** - 11 tests. Cada uno siembra el defecto en un arbol falso; el ultimo exige que el gate distinga el caso limpio del sucio.
- **`docs/adr/ADR-100-fuente-unica-de-la-verdad.md`** - dueno declarado por familia de dato, y el porque de que la segunda copia sea un bug.
- **`AGENTS.md` seccion 0 - Fuente unica:** tabla de dueno por dato, en el unico archivo que **todos** los subagentes reciben.

### Changed
- **`MEMORY.md`** dejo de repetir iconos, pagos, pre-commit, validacion UI y herramientas: los cita desde `AGENTS.md`. La linea de pipeline A/B ya no declara un motor a mano.
- **`docs/ROADMAP.md`** perdio la tabla de 8 roles con modelo y fallback: mide estado, no declara asignaciones. Tambien dejo de redefinir `memory.db` y el estado de `soporteml`.
- **`docs/SETUP.md`** perdio el bloque "Modelo de trabajo (2026-08-30)" que se declaraba vigente y `SUPERSEDED` en la misma frase; queda el historial en `memory/model-history.md`.
- **`docs/NORTH.md`** deja el estado de `soporteml` a `MEMORY.md`.
- **`AGENTS.md`** cita skills reales: reemplaza `knowledge-management`, `incremental-implementation`, `background-execution` y `a11y-at-validation`, que **no existian en ningun arbol**, por `session-lifecycle`, `complexity-driven-pipeline`, `agent-orchestration-pipeline`, `verification-gates` y `engineering-governance`.

### Notes
- **El diagnostico:** no eran "demasiados md" (1.859), era que ningun archivo tenia dueno de un dato y ningun gate verificaba afirmaciones, solo rutas. Primera corrida del gate: **5 copias y 16 tags a mano** sobre un arbol que todos los demas gates daban verde.
- **El caso mas caro:** 4 skills citadas como "las mas usadas" que no existian. `check-refs.py` no las veia porque eran backticks sin `scripts/` ni `docs/`.
- **Sin excepcion por conveniencia:** "el subagente solo recibe AGENTS.md" era la excusa que habia duplicado los modelos en cuatro archivos. Si un dato tiene que estar ahi, ese es su dueno y los demas lo citan.

---

## [2026-10-19] - Los commits de cierre ya no se llevan el indice ajeno

### Added
- **`scripts/session-commit.sh`** - commitea SOLO las rutas nombradas despues de `--`. `git commit` sin pathspec commitea el indice entero, incluidas las rutas que otra sesion dejo staged; el pathspec es lo unico que lo aisla.
- **`scripts/with-lock.py`** - wrapper de shell sobre `flock` para scripts bash (macOS no trae `flock(1)`). Espera el lock por defecto; `--timeout` lo vuelve fail-fast con exit 75.
- **Tests:** `tests/python/test_session_commit.py` (reproduce el caso del 18/10 sobre un repo descartable) y `tests/python/test_with_lock.py` (exclusion, cola, fail-fast, liberacion).

### Notes
- **El incidente:** el 2026-10-18 un cierre dejo 13 archivos staged y otra sesion se los llevo en su commit de ADRs. No hubo conflicto ni aviso: el indice es estado global del repo.
- **`lockutil.py` ya existia** (2026-10-12) y protege escrituras a `memory.db` y `HANDOFF.md`, pero no el indice de git. Lo que faltaba era el pathspec, no otro lock.
- **Medido:** con el wrapper, `a.txt` staged por otra sesion sigue staged y fuera del commit (test `test_commits_only_named_paths`). Sin el wrapper, viajaba.


### Added
- **`projects/langchain-starter/scripts/scan_sources.py`** (commit `3e80c91` del repo del proyecto): scanner determinista de `docs/` + `skills/`, con exclusiones (`archive`, `archives`, `insights`, `node_modules`, `venv`, `__pycache__`, `.git`) y CLI `--list`, `--json`, `--root`.
- **`store.py --sources` / `--reset`**, ids estables `<source_type>::<ruta relativa>::<n>`, `content_hash` por archivo, y 6 tests nuevos (16 passed en total).

### Notes
- **Medido, no declarado:** 333 archivos (263 `docs` + 70 `skills`), 300.082 palabras, 3.190 chunks estimados. Esas son las cifras reales; el documento decía 4.423 vectores.
- **La colección NO se reconstruyó.** Sigue con 10 embeddings de un documento. Falta la corrida explícita de `--sources --reset`.
- **El pipeline A/B falló dos veces y la segunda fue peor:** A entregó código con 4 defectos reales; B (spawneado sin `model=`, así que corrió con `gpt-oss:120b`, el mismo que A) reportó 10 correcciones, `17 passed` y `33 files scanned` sin haber tocado un solo archivo. Verificado por mtime, grep y salida de tests. La lección quedó en `learnings` #274: el enforcement del pipeline cubre la declaración, no la ejecución; hay que pasar `model=` explícito al spawnear.
- **Bug de import resuelto en el CORE:** `import_module("scripts.scan_sources")` nunca funcionaba (`scripts/` no es paquete) y, al cargarlo por ruta, `dataclass(slots=True)` exigía registrar el módulo en `sys.modules` antes de `exec_module`.

---

## [2026-10-19] - ADR-099: LangChain como capa de ejecución, no orquestador

### Added
- **`docs/adr/ADR-099-langchain-capa-de-ejecucion.md`.** Cierra el backlog #80 con una decisión de frontera: OpenClaw orquesta (sesiones, subagentes, pipeline A/B, memoria, scheduling); LangChain ejecuta flujos dentro de un proyecto (cadenas con estado tipado, RAG, grafos, streaming HTTP). Incluye los cuatro disparadores que justifican usarlo, los cuatro casos donde no aplica, y las reglas de frontera (proceso separado, venv propio, sin acople por dependencias).
- **Índice de ADRs actualizado** (`### Herramientas transversales`), con la marca de grupo conceptual contra 073/074/083.

### Notes
- **Hallazgo medido, no declarado:** `docs/LANGCHAIN_STRATEGY.md` afirma un índice de **4.423 vectores sobre 445 archivos**; el disco tiene **10 embeddings de 1 documento** y `chroma.sqlite3` sin modificar desde el 2026-09-24. También declara un scanner de 3 fuentes que no existe (`store.py` recibe rutas por argumento) y 25 tests de `kanam-insight`, proyecto descontinuado. La corrección del documento va como todo #81, no como efecto colateral del ADR.
- **Verificación:** `check-adr-integrity.py` OK (54 ADRs, todos indexados, sin refs rotas); `check-refs.py --all` OK (520 rutas). Servicio del starter verificado vivo (`/health` 200).

---

## [2026-10-14] - Level 1: README arreglado (5 datos stale) + huérfanos resueltos

### Fixed
- **`README.md` tenia 5 datos stale, todos corregidos contra el disco:** ADRs ("86" -> 96), skills activas ("78" -> 99), roles de agente ("4" -> 7), skills del Core ("36" -> 27) y una fila fantasma (`sandbox/`, carpeta que no existe). Un router de entrada que miente sobre el nivel 1 es peor que uno que no lista: ensena a no confiar.

### Removed
- **`crew_onboarding_guide.md` retirado (a Trash).** Guia de onboarding del Crew escrita el 2026-10-01; describia un equipo de tres roles (Planner, UI/UX Auditor, Critic) que hoy son siete, y un flujo ("Golden Path") con un umbral SHARP <=18 que quedo desactualizado. Refleja un estado del proyecto que ya no existe, no es un documento vivo, y solo aparece en `memory/archive/` como historia.

### Notes
- **Huérfanos verificados y descartados (no tocados):** `kanam-lab.db` (0 bytes, en la raiz; el proyecto `kanam-lab` tiene el suyo en su carpeta - este no es referenciado por nadie); `pipeline-state.json` (ya en `.gitignore`, estado local); `.DS_Store` y `.pytest_cache/` (ya ignorados). No hay nada que limpiar: la basura ya esta cubierta por el `.gitignore`.
- **`DREAMS.md` verificado y sano:** rotacion mensual funcionando (`dreams-rotate.py --check` OK, 26 entradas activas de octubre, septiembre archivado en `memory/archive/dreaming/`). No se toca.
- **Verificacion:** `check-refs.py --all` OK (552 rutas); `check-bootstrap-budget.py` OK; pre-commit completo en el commit.

---

## [2026-10-14] - AGENTS.md reescrito de una sola pieza: 18.560 -> 12.300 chars

### Changed
- **`AGENTS.md` reescrito entero, no parchado.** Venia con injertos acumulados: secciones duplicadas por nombre (dos `### Added` bajo el mismo genero), bloques de modelo repetidos, fechas y anecdotas explicativas (`"Por que: el 2026-10-06 no abri 3 fichas..."`) metidas en el cuerpo del bootstrap, y jerarquia rota por `#### ` que hermanaba reglas de pesos dispares. Ahora es un texto corrido con cuatro secciones (Conducta, Sesion y memoria, Ingenieria, Referencias) + Tools + Desarrollo.
- **Criterio de corte (declarado en el header):** una regla se queda si cambia una accion concreta y no se deriva de otro lado; el "como", el "por que" y la receta paso a paso van a `docs/AGENTS-DETALLE.md`. El archivo baja un 34% sin perder ninguna regla dura.
- **Sin perdida, verificado por lista de 42 palabras clave** contra la version anterior: las 42 siguen presentes (la unica ausencia aparente, `atomicos`, era falsa: esta escrita con tilde, `atomicos`).

### Fixed
- **Reescritura literal, no refactor de fondo.** La regla `## 4. Referencias` se conserva (era una de las secciones vivas) y los dos bloques `<!-- BEGIN MANAGED -->` (modelo por agente, pipeline A/B) quedan intactos: los regenera `managed-blocks.py`, editarlos a mano habria roto el gate.

### Notes
- **Verificacion:** `check-bootstrap-budget.py` OK (AGENTS.md 12.300/20.000, margen +7.700; total 36.442/60.000); `check-refs.py --all` OK (552 rutas); `check-agent-skill-boundary.py` OK; `check_em_dash.py` OK; `managed-blocks.py check` OK.
- **Deuda anotada:** el resto del nivel 1 (MEMORY.md, USER.md, SKILLS-INDEX.md, DREAMS.md, huerfanos) queda pendiente de la misma revision.

---

## [2026-10-14] - CHANGELOG sale de la raiz y su ventana baja a 14 dias

### Changed
- **`CHANGELOG.md` se muda a `docs/CHANGELOG.md`.** Es un derivado regenerable (historia rotada), no nucleo de personalidad: no debe ocupar el nivel mas caro de bootstrap. La raiz del workspace queda mas limpia.
- **Ventana activa de 30 -> 14 dias** (`DEFAULT_DAYS` en `scripts/changelog-rotate.py`). El ritmo real del workspace metia 117 entradas / 268 KB en 30 dias; 14 dias deja el activo en ~30 entradas (~74 KB).
- **Refs actualizadas:** `AGENTS.md` (Workspace Git), `README.md` (tabla de entrada), `docs/SETUP.md` (fila del script) y `scripts/pre-commit.template` (trigger de staged de `docs/CHANGELOG.md`).

### Fixed
- **`scripts/check-refs.py` deja de escanear `docs/CHANGELOG.md`.** Al mudarlo a `docs/`, `--all` (`docs/**/*.md`) empezo a tratarlo como documento vivo y reportaba 11 refs de la epoca (APUESTAS/MAPA retirados, ADRs renombrados). El CHANGELOG esta en rotacion permanente: misma politica que su bloque archivado (`docs/archive/`), se lee como se escribio. Nuevo `SKIP_FILES`.

### Notes
- **Verificacion:** `py_compile` OK en los 2 scripts; suite Python 320/320 en verde; `changelog-rotate.py --check` OK (30 activas, 175 archivadas, corte 2026-09-30); `check-refs.py --all` OK (565 rutas).
- **Hallazgo del diagnostico:** la rotacion NO estaba rota (mi primera hipotesis fue erronea); el archivo estaba correcto *segun su politica*. El problema real era la politica (ventana demasiado generosa) + la ubicacion (raiz).

---

## [2026-10-13] - Cierre de sesion: el HANDOFF no puede perder una sesion (historial + indice)

### Added
- **`scripts/session-handoff.py` preserva el historial de cierres por proyecto.** El HANDOFF es last-writer-wins por diseno (es "estado actual"), asi que dos cierres sobre el mismo proyecto perdian el anterior. Ahora, dentro del mismo `file_lock` (B6): **(A)** el HANDOFF previo se respalda en `.knowledge/handoff-history/<YYYY-MM-DD-HHMM>-HANDOFF.md` antes de pisarlo; **(C)** cada cierre appendea una linea a `.knowledge/SESSIONS.md` (append-only, nunca pisa filas previas). El daily (DB) ya era append con fingerprint de sesion; el hueco estaba en el HANDOFF.

### Added
- **`tests/python/test_session_handoff.py` (3 tests):** primer cierre crea HANDOFF + indice sin historial; segundo cierre deja el HANDOFF nuevo, el anterior en `handoff-history/` y 2 filas en el indice; el indice es append puro (sin perder filas). Probados sobre `tmp_path`, nunca el workspace real.

### Notes
- **Por que:** pedido de Gonzo (2026-10-13): "tengo miedo cierre dos veces sesion en dos conversaciones distintas y se sobre escriban". El miedo era correcto en la forma: el HANDOFF pisa, el daily no. Se elige conservar el modelo mental del HANDOFF (estado actual) y blindar el historial por dos vias independientes, en lugar de convertir el HANDOFF en un documento acumulativo.
- **Verificacion:** `py_compile` OK; 320 tests Python de la suite en verde; `check_em_dash` OK; test E2E en `/tmp` (dos cierres) con backup y append confirmados. Commits `f3ca0e6322` (script + tests); CI `Skill Scripts CI` #38473178779 success.

---

## [2026-10-13] - `projects/` es una carpeta plana: se retira la capa "agregado" (y una afirmacion falsa mia)

### Removed
- **La capa "repo agregado" (`projects_openclaw`).** `scripts/aggregate-sync.sh` (root y copia de kanam-ops) pasa a **stub RETIRED** que falla con la razon; `init-project.sh` e `initial-setup.sh` dejan de registrar/armar el agregado. `docs/SETUP.md`, `AGENTS.md`, `docs/AGENTS-DETALLE.md`, la skill `workspace-portfolio-hygiene` (SKILL + reference) y `.gitignore` describen el modelo real.

### Fixed
- **Corregida una afirmacion falsa mia (2026-10-12):** anote en `docs/ROADMAP.md` que "`projects/.git` apunta hoy a `workspace_openclaw`". **Falso:** `projects/` nunca tuvo `.git` propio; `git -C projects` simplemente sube al `.git` del workspace y reporta *su* remote. Nota corregida en el lugar.

### Changed
- **Modelo de proyectos (confirmado por Gonzo 2026-10-13; consistente con ADR-098):** `projects/` es una carpeta contenedora plana, **ignorada 100%** por el workspace git; cada `projects/<slug>/` es **su propio repo** (incluye `.knowledge/`; la memoria viaja con el proyecto). No hay capa intermedia.
- **`init-project.sh` reescrito:** crea el proyecto con su `.knowledge/` **trackeado en el repo del proyecto** (se elimino el modelo de "blob en el workspace git", que bajo `/projects/` ignorado abortaba el script) y elimina el registro en el agregado.
- **`initial-setup.sh` reescrito:** el paso 2 pasa de "armar `projects/` como clon del agregado" a "asegurar la carpeta plana (NO un repo)"; `verify` reporta si `projects/` es un repo (error) y cuantos proyectos tienen su `.git` propio.
- **`ADR-066`:** nota fechada (el modelo de tracking evoluciono; la decision del ADR no cambia). **`kanam-os-layers-evaluacion.md`** y la linea de scripts de `agents/kanam-ops/AGENTS.md`: "triple-git"/`aggregate-sync` -> modelo vigente.

### Notes
- **Verificacion:** `bash -n` OK en los 4 scripts; `check-adr-integrity.py` y `check-adr-supersede.py` OK (96 ADRs); `check-refs.py --all` OK (559 rutas); sin guiones largos.
- **Retiro con motivo, no borrado silencioso (ADR-067 §4):** los scripts quedan como stub que nombra la razon; el repo `gonzoblasco/projects_openclaw` sigue archivado en GitHub.
- **Deuda anotada:** `sanitize-skills.py` y `publish-skills.sh` todavia tratan `projects_openclaw` como un slug interno a sanear (inocuo); dejados por ser de la via de publicacion de skills (archivada, ADR-079).

---

## [2026-10-12] - S1: la fuente unica de modelos es ADR-090 (cabeceras de 040/041/053 dejan de mentir)

### Changed
- **`ADR-090` declara `**Supersede:**` a ADR-053, ADR-040 y ADR-041.** Es la ley efectiva (pensamiento por agente + asignacion de modelos por rol, cata 2026-10-06); los tres predecesores ya no se leen como vigentes.
- **Cabeceras enmendadas a `Superseded`:** ADR-053 (`Superseded por ADR-090 (2026-10-05)`), ADR-040 (`Superseded por ADR-053 / ADR-090`), ADR-041 (`Superseded por ADR-045/046 / ADR-090`). Antes decian `Aceptado`/`Accepted` mientras su propio cuerpo registraba el reemplazo.
- **`docs/architecture/adr-corpus-overlap-audit.md`:** S1, S3 y S5 marcados RESUELTOS; el diagnostico original conservado en un `<details>`.

### Notes
- **Causa:** el cluster de modelos repartia la decision entre 15 ADRs y la cabecera de los predecesores no reflejaba el reemplazo, que vivia en prosa (cuerpo de 053). El guard ensanchado en el commit previo ahora cubre esa clase.
- **Sin cambio de config:** la ley viva (`ADR-090`) ya coincidia con `openclaw.json` y con el bloque `model-operativo` de `AGENTS.md`; la reparacion es de cabeceras, no de runtime.
- **Verificacion:** `check-adr-supersede.py` OK, `check-adr-integrity.py` OK (96 ADRs), 21 tests de los dos guardas en verde.
- **Residual de S1 (no tocado):** 045/046 ya estaban `Superseded`; 049 (Claude Code como motor A/B) sigue `Aceptado` y es una decision de harness, no de asignacion de modelos - fuera del alcance de S1.

---

## [2026-10-12] - Reintroducida `debugging-and-error-recovery` en kanam-dev + SKILLS-INDEX sincronizado

### Added
- **`agents/kanam-dev/skills/debugging-and-error-recovery/SKILL.md`:** skill de depuración que cierra tres referencias colgantes (`ci-cd-and-automation:190`, `doubt-driven-development:229`, `observability-and-instrumentation:22` citaban una skill que no existía en ningún árbol). Destila el método de diagnóstico (localizar → reproducir → falsificar hipótesis → corregir causa → probar el fix Y el fix del fix) más nuestras reglas duras: reproducir antes de arreglar, el primer error del log es un síntoma, un verde sin casos corridos no es verde, no arreglar enmascarando, contrato de evidencia, y el caso dev-vs-prod. Escrita en la convención de sus hermanas (inglés, estilo addyosmani).

### Changed
- **`SKILLS-INDEX.md` sincronizado con el disco (estaba desfasado en 3 árboles y 8 filas).** Totales re-medidos contra el CLI: dev 35→43, critic 1→2, auditor 1→5, total 84→99. Ocho skills que ya existían en disco y en el CLI pero no tenían fila: siete en dev (`api-integration-test`, `chaos-engineering`, `code-metrics`, `compatibility-testing`, `dependency-advisor`, `performance-benchmark`, `threat-modeling`, todas del commit `a68e19d819`) más `debugging-and-error-recovery`; en critic, `evidence-hunter`; en auditor, las cuatro hermanas de `surface-alignment-audit`. Nota de conteo agregada: `find agents/*/skills -name SKILL.md` sobrecuenta por los `node_modules` de `playwright-core` en el auditor; la autoridad es el CLI (`source == openclaw-workspace`).

### Notes
- **Reintroducción, no alta nueva.** `debugging-and-error-recovery` figuraba en la sección 4 (Retiradas) desde la reestructuración del 2026-09-22, retirada junto con su colección de origen. Al reescribirla con nuestras reglas duras (no es la versión vieja) se reintegra al inventario; queda anotado en su fila.
- **Contexto:** sale de la evaluación de `mergisi/awesome-openclaw-agents` (catálogo de 196 SOULs, no instalable). El único hueco sustantivo que apareció en el cotejo contra nuestra colección fue que tres skills citaban una skill de depuración ausente - un hueco propio, no una pieza faltante del repo externo.
- **Verificación:** `check-refs.py SKILLS-INDEX.md` OK (100 rutas); `check-agent-skill-boundary.py` OK; `check_em_dash.py` OK en ambos archivos; totales por árbol re-contados contra el disco.

---

## [2026-10-12] - ADRs de proyecto salen del corpus global (6a) y el guard de supersede deja de ser ciego al campo generico

### Changed
- **Movidos `docs/adr/ADR-068` y `ADR-091` al proyecto `soporteml`** (`projects/soporteml/.knowledge/adr/ADR-0001-soporteml-greenfield-desde-v1.md` y `ADR-0002-soporteml-v4-cierre-stripe.md`). Regla 3 de ADR-067 y `docs/adr/README.md` ("sin referencias al proyecto que lo originó"): un ADR cuyo sujeto es un proyecto vive con el proyecto, no en el corpus global. Renumerados en la serie del proyecto, fila quitada del índice global (huecos [68, 91] intencionales), y consumidores repuntados: `ADR-042`, `docs/NORTH.md`, `docs/ROADMAP.md`, `docs/LANGCHAIN_STRATEGY.md`, `MEMORY.md`.
- **`scripts/check-adr-supersede.py`: el grafo ahora tambien lee el campo generico `**Relacionado:**`.** Antes solo miraba los campos dedicados (`Supersede`/`Revierte`/`Reemplaza`), asi que un reemplazo TOTAL declarado en el campo generico era invisible: ADR-098 (`ADR-075 (superseded)`) y ADR-091 (`ADR-068 (... superado)`) vivian solo ahi. La relacion se reconoce cuando el contexto del citado (el parentesis) trae señal de reemplazo y NO de parcialidad ("parcial", "apartado", "seccion", "lista", "historico").

### Added
- **`tests/python/test_check_adr_supersede.py`: 4 tests nuevos** del camino `Relacionado` (total exige marca; parcial no; sin señal se ignora; la señal debe estar en el contexto del citado). Probados en negativo: neutralizar la rama nueva hace fallar exactamente `test_relacionado_declares_total_replacement`; restaurado, 12/12 en verde.

### Notes
- **Por que no se movio todo:** los ADRs de sujeto `kanam-os` (054, 094, 096) quedan **bloqueados**: `projects/kanam-os/.knowledge/` esta git-ignored (`.git/info/exclude`), asi que mudarlos ahi los deja **sin historial** (peor que dejarlos). ADR-063 (kanam-insight) queda bloqueado: el repo existe en GitHub pero el arbol local no esta clonado. Criterio de destino que faltaba: un ADR de proyecto solo se muda a un arbol **versionado** (`git ls-files .knowledge`). Registrado en `docs/architecture/adr-corpus-overlap-audit.md` §6a.
- **Verificacion:** `check-adr-integrity.py` OK (96 ADRs, huecos 68/91 informativos); `check-adr-supersede.py` OK; 21 tests de los dos guardas en verde; sin guiones largos en los archivos tocados.
- **Residual (no resuelto en este cambio):** `docs/learnings/proyectos.md` (vista DB-first, ADR-065) cita ADR-068/091 y **ademas** esta desactualizado respecto de la DB (207 lecciones vs 225). Se deja como deuda aparte: regenerarlo mezcla 18 lecciones ajenas a esta mudanza.

---

## [2026-10-12] - Segundo eje de la auditoría de ADRs: alcance (un ADR de proyecto vive con el proyecto)

### Added
- **`docs/architecture/adr-corpus-overlap-audit.md` §6:** segundo eje del análisis, a pedido de Gonzo: *"aquellos relacionados con un proyecto en particular viva con el proyecto y no más en el scope global; los ADR no tienen por qué tener mención a proyectos específicos"*. Separa 6a (sujeto de proyecto → mudar al proyecto; 6 ADRs candidatos) de 6b (mención de evidencia → ~70 archivos) y 6c (no hay guard de alcance).

### Notes
- **La regla ya existe y se viola igual:** `docs/adr/README.md:110` ("sin referencias al proyecto que lo originó") y `ADR-067 §3` ("los ADRs de un proyecto viven en el repo del proyecto"). Ningún script la verifica. Precedente aplicado una sola vez: `ADR-048` se movió a `projects/kanam-lab/.knowledge/adr/0002-ui-framework-gradio.md` el 2026-09-22.
- **Tensión registrada, sin barrer a ciegas:** el método del corpus se apoya en la evidencia (el caso real que motivó la decisión). ADR-067/078/088 citan proyectos como caso testigo; borrar la mención borra el *por qué*. Recomendación: aplicar 6a ya (concreto, ~6-8 mudanzas); 6b solo bajo una salida elegida por el owner (genericizar la evidencia vs acotar la regla como se acota el campo `Origen`).
- **Nada movido ni editado:** sigue siendo el registro del descubrimiento.

---

## [2026-10-12] - Auditoría de solapamiento del corpus de ADRs (una única fuente de verdad)

### Added
- **`docs/architecture/adr-corpus-overlap-audit.md`:** análisis de los 98 ADRs contra la regla de "una única fuente de verdad". Mapea los clusters temáticos (modelos 15 ADRs, memoria 12, multi-agente 11) e identifica cuatro ADRs que pisan una decisión viva sin declararlo en su cabecera.

### Notes
- **Los dos guardas dan verde y el problema existe igual:** `check-adr-integrity.py` (98 indexados, sin duplicados) y `check-adr-supersede.py` (grafo consistente) verifican *integridad de forma*, no *unicidad de decisión*. La causa raíz (S5): el grafo de supersede solo lee el campo de header del ADR reemplazante, así que un reemplazo declarado **en prosa** es invisible.
- **Casos vivos:** ADR-053 dice `Aceptado` pero está pisado por ADR-090 (prosa); ADR-068 dice `Aceptado` pero ADR-091 lo llama "superado"; y el bootstrap (`AGENTS.md:158-162`, `MEMORY.md:1,65`) sigue citando la ley muerta ADR-075 (`~/projects`) cuando la vigente es ADR-098 (`<workspace>/projects/`).
- **Qué NO se hizo:** no se tocó ningún ADR ni el bootstrap. Es el registro del descubrimiento; las reparaciones (ensanchar el guard, nombrar la fuente única de modelos, corregir el bootstrap, enmendar cabeceras) requieren autorización del owner.

---

## [2026-10-12] - El curso OpenClaw Use Cases se reinicia desde cero

### Removed
- **`studies/openclaw-use-cases/` (10 archivos):** INDEX + 9 lecciones (L01-L05 de la grilla vieja de 25, y L01-L03 de la migracion a 6 modulos). La carpeta acumulaba tres versiones del plan de modulos que no coincidian (INDEX vs daily 2026-10-10 vs `L01-lesson-overview.md`), ademas de numeracion inconsistente (`/25` vs `/30`). Decision de Gonzo (2026-10-12): borrar y rehacer el curso desde cero con un solo plan.

### Changed
- **`docs/adr/ADR-086-embudo-de-entrada-conversacional.md`:** la tabla de Implementacion y las Referencias ya no apuntan a `studies/openclaw-use-cases/` (retirado). La decision del ADR (el marco de los 5 patrones del embudo) sigue vigente; solo se retira el puntero al registro de estudio.

### Notes
- **Que NO se toco:** los otros tracks de estudio quedan intactos - `studies/narrative-engineering/` (3 casos completos, 4/4 ejes), `studies/design/` (plan abierto el 2026-09-14) y `docs/cpacc/` (semana 1 + meta de examen nov/dic). El pedido era reiniciar el curso de OpenClaw Use Cases, no barrer todo lo que se estudia.
- **Recuperable:** todo estaba trackeado y pusheado; el borrado se recupera del historial de git si hiciera falta.
- **Aprendizaje del Modulo 1 preservado:** los learnings derivados (`docs/learnings/pipeline-agentes.md`, `docs/learnings/metodologia.md`) y el ADR-086 viven fuera de la carpeta; no se pierden al reiniciar el curso.

---

## [2026-10-12] - El gate del pacto A/B deja de mentir: el estado de git ya no es una violacion

### Fixed
- **`scripts/check-pipeline-enforcement.py`: 5 bugs introducidos al agregarle la "verificacion de git".** (1) El parseo de `git status --porcelain` usaba un offset fijo `line[18:]` y `split()[1]`, y truncaba los paths (`9.md` en vez de `memory/2026-10-09.md`). (2) **Falso positivo grave:** un workspace limpio devolvia `exit 1` con la unica "violacion" = "Sin cambios detectables" - el estado de git se contaba como violacion del pacto A/B. (3) La verificacion de git estaba implementada **dos veces** (`_get_staged_paths_and_diff` y `find_violations`) con parseos divergentes. (4) Filtro muerto: `staged_files` filtraba los `??` pero nunca se usaba. (5) Mezcla de responsabilidades: `git status` es informativo, no rompe el pacto.

### Changed
- **Una sola fuente de git:** helper testeable `parse_porcelain()` (usa `line[3:]` correcto y desentrecomilla) + `_git_staged_report()`, que separa staged de untracked y devuelve `(paths, reporte)`. El reporte de git se imprime aparte en `main()` y **no cuenta como violacion**; el `exit code` depende solo de la consistencia de las 4 fuentes del pacto. Se elimino el bloque duplicado de `find_violations()`.

### Added
- **`tests/python/test_check_pipeline_enforcement.py`: 3 regresiones nuevas** (de 8 a 11 tests) que cubren exactamente estos bugs: parseo sin truncar, workspace sucio != violacion del pacto, y staged vs untracked separados.

### Notes
- **Verificacion:** `py_compile` OK; `11/11` tests pasan. E2E real sembrando un repo temporal: pacto consistente -> `OK` exit 0; deriva de modelo en `managed-blocks.py` -> caza 2 violaciones ("dos verdades" + "distinto del canon") exit 1. Sin el fix, el mismo repo daba un falso "VIOLADO" sobre un workspace limpio.
- **Leccion (reafirma ADR-083):** un guard que no puede distinguir limpio de sucio no es un guard. La verificacion de git se agrego al chequeo del pacto sin separar "informar" de "invalidar", y el resultado fue un gate que rompia commits por ruido.

---

## [2026-10-07] - El suite de skills deja de bloquear commits por archivos que no se commitean

### Fixed
- **`scripts/test-skills.sh`: el scope es ahora `git diff --cached` (staged), no el disco entero.** El pre-commit lo corre en cada commit y escaneaba todos los `SKILL.md` del disco, incluidos los `playwright-core` bajo `node_modules/` (3 por copia instalada) y los arboles de skills de agentes todavia no trackeados. Resultado: un commit que no tocaba nada de eso fallaba por em dashes ajenos y forzaba `--no-verify`. Reproducido 2026-10-07: `./scripts/test-skills.sh` reportaba 12 fallos de em dash, 0 de ellos en el commit.
- **`scripts/test-skills.sh`: `node_modules/` se poda del walk en TODOS los checks.** Los checks A (sintaxis) ya podaban; B/C/D/E no, y C (em dash) fallaba contra el codigo de terceros. Ahora el `find` usa `-prune` una sola vez y el barrido es uniforme.

### Added
- **`scripts/test-skills.sh --all`:** barre todo el arbol de skills en disco (lo que corre el CI, donde no hay staging). Con la guarda de CI: si `CI` esta seteado y no se paso `--all`, el script **aborta** en vez de salir verde sobre 0 archivos.
- **`tests/bash/test-skills-scope.bats` (5 tests):** prueba el scope staged, el prune de `node_modules`, el filtro de archivos fuera de los skill roots y el aborto en CI. Monta un arbol temporal con una copia del script real.

### Changed
- **`.github/workflows/skills-ci.yml`:** el step de sintaxis invoca `./scripts/test-skills.sh --all` (en CI no hay staging; el default veria 0 archivos).

### Notes
- **Verificacion (repro del pedido):** con un solo `docs/ROADMAP.md` staged, el hook corre y sale 0; con un `SKILL.md` staged bajo `skills/`, solo se revisa ese archivo. El barrido `--all` bajo de 12 a 6 fallos de em dash: los 6 restantes son SKILL.md reales de agentes (deuda de contenido preexistente, fuera de este commit).
- **Pendiente registrado:** los 6 `SKILL.md` con em dash (4 en `agents/kanam-auditor/`, 2 en `agents/kanam-critic/`), de los cuales 5 son arboles untracked, siguen sin guion comun. Los caza `--all`/CI, no el hook sobre esos commits.

---


### Added
- **`docs/ROADMAPS.md` (El Roadmap de Roadmaps):** el meta-roadmap del ecosistema de agentes. Indice unico del estado de madurez de los 7 roles (auditor, critic, dev, mind, ops, planner, studio), el camino de madurez M0-M5, la secuencia de escalada por dependencia (los gates de calidad primero) y las guardas de tracking. Premisa base: ausencia de `ROADMAP.md` = v0.1; meta de la ronda = v0.5 por rol; visión = v1.0.
- **`docs/checklists/roadmap-authoring-guide.md`:** el estandar de como se escribe un roadmap de rol (7 secciones obligatorias + vocabulario de version). Codifica el patron que auditor y critic ya usaban de hecho.
- **`scripts/check-roadmaps.py` + guard en el pre-commit:** verifica por rol la existencia de `agents/<rol>/ROADMAP.md`, su encabezado/version, sus secciones, el marcador de proyecto y la **coherencia de version** contra el indice. Nace porque el 2026-10-07 se descubrio que 5 de 7 roles no tenian roadmap y nada lo detectaba (ADR-083: una regla sin guarda se viola sola).
- **`agents/<rol>/ROADMAP.md` para los 5 roles que no lo tenian** (dev, mind, ops, planner, studio), autorados por cada rol via `sessions_spawn` y verificados por el CORE contra el filesystem.

### Changed
- **`agents/kanam-auditor/ROADMAP.md` y `agents/kanam-critic/ROADMAP.md`:** alineados al estandar (encabezado formal, secciones 1-7, agregadas "Lo que rechace" y "Red lines y criterio de cierre" donde faltaban). Contenido previo intacto.
- **`docs/checklists/roadmap-review-checklist.md`:** nueva seccion "Variante: revisar un ROADMAP de rol" (contra fuentes reales, con el guard como primer paso y la regla de que el archivo del rol gana sobre el indice).

### Notes
- **El ecosistema estaba, en el papel, 100% en v0.1 y solo 2 de 7 roles tenian mapa.** Ahora los 7 declaran su version y el camino a v0.5. Guard pasa 7/7.
- **Secuencia fijada:** critic y auditor primero (son los jueces; escalarlos antes de construir sobre ellos), despues dev, luego ops/mind, y planner/studio al final.

---

## [2026-10-07] - El Crew deja de ser tres roles sin skills: Planner y Auditor ganan el suyo

### Added
- **`agents/kanam-planner/skills/session-plan-orchestration/SKILL.md`:** primera skill del Planner. Orquesta la tarea como plan persistente (`.knowledge/session_plan.json` via `scripts/session_plan.py`): traza pasos, asigna roles en orden (implementacion -> Auditor -> Critic), evita la amnesia de sesion leyendo el `summary` al arranque, y no ejecuta el trabajo de ningun rol.
- **`agents/kanam-auditor/skills/surface-alignment-audit/SKILL.md`:** primera skill del Auditor. Auditoria de superficie contra el Design System: cruce de tokens (hex hardcodeado = error), filtro Anti-Slop, y contraste WCAG 2.2 **medido** por rol del token. Marca el deslinde forma vs sustancia con el Critic.
- **`agents/kanam-planner/skills/` y `agents/kanam-auditor/skills/`:** los dos arboles de rol no existian. Los tres roles del Crew (Planner, Critic, Auditor, creados el 2026-10-01) naciaron solo con AGENTS/IDENTITY/SOUL/USER y veian **cero** skills propias; sus jobs semanales de revision corrian sobre un directorio vacio.

### Changed
- **`SKILLS-INDEX.md`:** sumadas las filas de planner y auditor (1 cada uno) y las secciones 3.7/3.8; total de activas 78 -> 81 (critic + planner + auditor).

### Notes
- **El Crew completo ya tiene material propio.** Critic (`sharp-adversarial-review`), Planner (`session-plan-orchestration`) y Auditor (`surface-alignment-audit`) pasan `scripts/test-skills.sh` (51/51) y son visibles via `openclaw skills list --agent <id>`.
- **`session-plan-orchestration` corregida durante la creacion:** las refs a `session-start.sh`/`session-end.sh` apuntaban a `scripts/` (no existen ahi); viven en `skills/session-lifecycle/scripts/`. Lo cazo `test-skills.sh` (script refs 2 failed -> 0).

---

## [2026-10-07] - El Critic deja de ser un rol sin skills: nace `sharp-adversarial-review`

### Added
- **`agents/kanam-critic/skills/sharp-adversarial-review/SKILL.md`:** primera skill del rol Critic. El ritual de presión adversarial con la rúbrica SHARP: cómo puntuar los 5 ejes (Sharpness, Horizon, Asymmetry, Resistance, Parsimony) con evidencia citable, el mapa de veredicto (VETO en `<= 18`, Aprobado, ORO en `>= 24`) y el entregable del VETO (puntos de fricción obligatorios). Presta de `skills/verification-gates` la guarda de verde falso y de `skills/trust-vocabulary-report` el contrato de evidencia; marca el deslinde sustancia vs forma con el Auditor.
- **`agents/kanam-critic/skills/`:** el árbol de rol del Critic no existia. Su `workspaceDir` solo tenia AGENTS/IDENTITY/SOUL/USER, asi que el agente veia **cero** skills y su job semanal de revision corria sobre un directorio vacio.

### Changed
- **`SKILLS-INDEX.md`:** sumada la fila `agents/kanam-critic/skills/` (1) y la seccion 3.6; total de activas 78 -> 79.

### Notes
- **El job `skill-collection-review:kanam-critic` corria en error** (`Ls failed`): revisa el Skill Workshop del agente (`agent/workshop-skills/`), que estaba vacio. Con el arbol de rol ya en pie, el agente tiene material propio; el job queda sin bloqueo de arbol.

---

## [2026-10-06] - kanam-fixer: el alcance estaba definido; el ROADMAP mentia desde hacia 3 semanas

### Fixed
- **`docs/ROADMAP.md` §2.1 decia que `kanam-fixer` tenia "alcance SIN DEFINIR". Era FALSO.** El alcance se definio el 2026-09-14/15 (BRIEF + ROADMAP del proyecto, direccion confirmada por Gonzo) y el ciclo `0.0.1` cerro con evidencia ese mismo dia. Lo confirma `portfolio-strategy/ADR-001` §6. Otro falso pendiente (como el Tablero y el design system: gobernanza dormida acumulando estados viejos). Corregido: ancla formalizada, alcance definido, ciclo 0.0.1 cerrado / 0.0.2 abierto, npm `kanam-fixer@0.0.2`, repo publico. §2.1 pasa a 🟢.
- **`docs/NORTH.md`** (decision abierta #1): mismo falso pendiente corregido. Lo que sigue abierto no es la *definicion* del alcance sino la *validacion de impacto* del ancla (criterio H1).
- **`MEMORY.md`** (reconciliacion pedida por §2.1, medida contra `gh repo list`): sumados repos propios vivos que faltaban (`catalogo-de-venta-de-coches`, `create-stack`, `kanam-minesweeper`, `kanam-sudoku`, `match3`, `system-health-check`); aclarado que `kanam-forge` es fork (no propio) y que `kanam-insight` existe como repo (privado) aunque el proyecto esta descontinuado.

### Changed
- **`portfolio-strategy/.knowledge/ADR-001-portfolio-strategy.md`** (fuera del workspace): nueva seccion 8 que **verifica** el estado contra fuentes reales y cierra formalmente el pendiente de definicion de la seccion 6. El pilar Accesibilidad tiene ancla formal.

---

## [2026-10-06] - Integridad del bootstrap deja de ser un falso verde (ROADMAP 0.1)

### Added
- **`scripts/check-bootstrap-budget.py`:** guard del cap de inyeccion del runtime. Los archivos que OpenClaw inyecta en cada arranque (AGENTS/MEMORY/USER/SOUL/IDENTITY) se truncan EN SILENCIO al superar su cap. Mide en caracteres como el runtime (unidades UTF-16, no bytes: `wc -c` sobreestima en espanol por los acentos y da un margen falso). Caps verificados contra el codigo instalado (`dist/bootstrap-*.mjs`): 20.000 por archivo, 4.000 fijo para USER.md, 60.000 total. Modo reporte + bloqueante.
- **`tests/python/test_check_bootstrap_budget.py`:** 10 casos (mide UTF-16 como el runtime, cap propio de USER.md, borde exacto, la CLASE y el total, contrato de salida del script real).

### Changed
- **Pre-commit (sin condicion) + CI (`skills-ci.yml`):** el check corre siempre. Los archivos de bootstrap no cambian por un pathspec predecible; un trigger por diff dejaria pasar el crecimiento que ocurre en cualquier otra edicion.
- **`USER.md` (3.933 -> 3.600 chars, margen 67 -> 400):** el contenido de ENTORNO (canal remoto Telegram, gateway 24/7) se movio a `docs/SETUP.md`. Un archivo de bootstrap es contexto de cada turno; el entorno no lo es.
- **`MEMORY.md` (13.893 -> 13.705):** quitadas las referencias a harness (Claude Code, terminal harnesses, jsdom/headless); la leccion de fondo se conserva. Pedido de Gonzo para aflojar margen.
- **`docs/SETUP.md` seccion Red / remoto:** corregida la linea stale (decia Tailscale+PWA como canal; Telegram lo reemplazo el 2026-09-07) y absorbidos los dos bullets de entorno.

---

## [2026-10-06] - El design system gana su tema oscuro; kanam-os migra (ADR-096)

### Added
- **`design/tokens/themes/dark.tokens.json`:** tema oscuro del sistema base (el `kanam.css` base ES el claro). Paleta tomada del tema oscuro de kanam-os (probada), recalculada al piso WCAG. 11 pares verificados (text.primary 12.83:1, danger 7.50:1, brand 4.85:1).
- **`tests/python/test_check_design_tokens.py`:** caso del tema oscuro (existe + cumple).

### Changed
- **`design/tokens/build-tokens.py` + `scripts/check-design-tokens.py`:** `dark` sumado al REGISTRY y al guard. El build genera 7 hojas (antes 5).
- **`design/README.md`:** tabla de temas con `dark` + nota modo vs marca (el claro no necesita archivo: `kanam.css` = `:root`).

### Delegado
- **kanam-os migra a consumir `design/tokens/` (DEV, pipeline A/B).** Contrato en ADR-096: consume kanam.css + dark.css, sync en build (anti-drift), preserva el toggle server-side. Verificación del CORE sobre el repo real al cerrar.

### Fixed
- **Regresión detectada en la verificación:** `--k-brand-primary` del dark (`#4ea870`) daba 3.73-4.28:1 como texto sobre card/elevated (kanam-os lo usa así). Corregido a `#6ee7a0` (7-8:1). El guard medía brand solo sobre `surface.base` - **hueco cerrado**: ahora también sobre `card`/`elevated`.
- **kanam-os:** la migración de A aliasaba tokens inventados (`--k-bg`, `--k-text`...); B la corrigió a los tokens reales + cargó los CSS + hookeó el sync a npm. Verificado por el CORE: build verde, ambos temas, 200, color-contrast limpio salvo `aria-pressed` (preexistente) y opacity en `/learnings` (preexistente).

---

### Added
- **ADR-095** (`docs/adr/ADR-095-reevaluacion-decisiones-diseno.md`): re-evaluación pedida por Gonzo ("lo que ya está hecho de decisiones de diseño deben ser revaluadas").
- **`scripts/check-design-tokens.py`:** mide el contraste WCAG de los tokens de cada tema contra el piso por rol (texto 4.5:1, componente 3:1; los bordes decorativos no se exigen). Modo reporte + `--check` bloqueante. Cableado al pre-commit (cambios en `design/`) y al CI.
- **`tests/python/test_check_design_tokens.py`:** 8 casos (matemática WCAG, el guard puede fallar, bordes decorativos no son falso positivo, el sistema real pasa).

### Fixed
- **10 pares de tokens bajo el piso WCAG** en los 3 temas, corregidos preservando la identidad (un paso más oscuro del mismo tono, con primitivas existentes): el teal de marca como texto (3.74 -> 5.25), el ámbar de warning (3.45-3.64 -> 4.96-5.23), los `muted` de Plaza/Terrario (3.33-3.94 -> 5.23-5.69), el `info` de Terrario (4.32 -> 6.33).
- **Matrices `$contrast`:** los números de Plaza/Terrario eran a mano y nunca medidos (decían "danger 4.9", el real era 4.70). Reemplazados por valores medidos; el sistema base ahora **declara la suya** (antes no existía).

### Changed
- **`design/README.md`, `ADR-047`, `DECISIONS.md` §2.8, `docs/NORTH.md`:** corregidas las afirmaciones falsas. El design system **ya existe** (`design/`, ADR-047 desde 2026-09-14) - el "paso 0" era un falso pendiente; la precondición del auditor de diseño ya se cumple. Lo que queda es **adopción** (kanam-os usa un tema paralelo) + práctica (`studies/design/`).
- **Pre-commit + CI:** el cambio en `design/` regenera el `dist/` y corre el guard de contraste.

---

## [2026-10-06] - Reconciliación: una sola ruta (APUESTAS + MAPA retirados, kanam-insight descontinuado)

### Removed
- **`docs/APUESTAS.md` y `docs/MAPA-PROXIMOS-PASOS.md` eliminados.** Cuatro documentos decían "qué sigue" y se contradecían (NORTH/ROADMAP/APUESTAS/MAPA, fechas 10-06/10-06/09-24/09-14). Quedan dos con roles distintos: `NORTH` (el para qué) y `ROADMAP` (el cómo y en qué orden). El MAPA estaba stale (hablaba de kanam-lab/kanam-studio como eje; NORTH ya los sacó). El contenido de producto de APUESTAS pasó a `ROADMAP.md` §2.1.
- **`kanam-insight` descontinuado y fuera del roadmap.** No existe como proyecto (no está en `~/projects/`) y Gonzo confirmó que no recuerda haberlo querido. Fuera de NORTH, ROADMAP §2.1, MEMORY.md y el registro del proyecto.

### Added
- **`docs/ROADMAP.md` - "La ruta" (secuencia fijada).** Tramos T1 (OnWheels + design system + CPACC), T2 (caso de estudio + reactivar búsqueda laboral), T3 (UNA apuesta comercial), D (sistema como soporte). Resuelve la tensión: los tramos que facturan estaban fríos mientras los que no facturan consumían el tiempo.

### Changed
- **`docs/ROADMAP.md`:** §2.1 absorbe las apuestas de producto vivas (soporteml, kanam-fixer); la prioridad consolidada aclara que ordena por *importancia* y "La ruta" por *secuencia*.
- **`docs/NORTH.md`, `docs/LANGCHAIN_STRATEGY.md`, `docs/adr/ADR-063`, `docs/adr/ADR-091`, `docs/adr/ADR-085`, `README.md`, `MEMORY.md`:** reapuntados para no citar los docs retirados. ADR-063 queda como registro histórico de la decisión de stack de kanam-insight (estado del sujeto: DESCONTINUADO).

## [2026-10-06] - Etapa 4 de Kanam OS: accesibilidad medida, tests/node cableados, Tablero cerrado

### Added
- **ADR-094** (`docs/adr/ADR-094-etapa-4-a11y-scan-tests-node-tablero.md`): cierra/reubica los tres componentes de la Etapa 4.
- **`scripts/a11y-scan.mjs`:** mide accesibilidad real de una página viva con axe-core (OSS) + playwright-core, sin `axe-devtools` pago. Exit 2 si la infra (playwright/axe) no está: un gate que no puede correr no es un verde. El juicio (`classify`) es puro y testeable. **Primera corrida:** encontró `aria-allowed-attr` `critical` (`aria-pressed` sobre `<a href>`) en `kanam-os` `/todos`, `/fichas`, `/learnings` - bug real de accesibilidad.
- **`tests/node/run.sh`:** runner de los tests Node del workspace (antes `tests/node/` no corría en ningún lado).
- **`tests/node/a11y-scan.test.js`:** 8 casos del clasificador (umbral, impacto desconocido = peor caso, umbral inválido lanza).

### Changed
- **`tests/node/` cableado** al pre-commit (junto a bats y pytest) y al CI (nuevo step "Node functional tests").
- **`docs/ecosystem/DECISIONS.md` §2.5:** el Tablero se cierra - la superficie visual del backlog **es** `kanam-os /todos` (modelo **pull**, fuente de verdad `memory.db`). Falso pendiente de 6 días.
- **`docs/ecosystem/DECISIONS.md` §2.8:** la pata de **medición** a11y ya existe (`a11y-scan`).
- **`docs/NORTH.md`:** Etapa 4 - a11y medida, Tablero cerrado, especialistas diferidos a propósito (el esqueleto Crew+SHARP ya está; los 13 roles del Academic System son dispersión).

---

### Added
- **ADR-093** (`docs/adr/ADR-093-plan-de-sesion-persistente.md`): el plan de sesión como objeto persistente del sistema. Cierra el hueco declarado en `docs/NORTH.md` (la Etapa 2 tenía cinco gates que nadie invocaba).
- **`scripts/session_plan.py close`:** marca el plan `completed` y lo archiva en `.knowledge/archive/session_plan_<id>.json`. Defensivo e idempotente (sale 0 siempre: el cierre corre bajo `set -e`).
- **`tests/python/test_session_plan.py`:** 5 casos (path portable/sobrescribible, init, close+archivo, idempotencia, exit code del CLI).

### Changed
- **`scripts/session_plan.py` portable:** el path, antes clavado a `/Users/gonzoblasco/...`, ahora se deriva del script y es sobrescribible con `SESSION_PLAN_PATH`. El plan se muda de la raíz (`.session_plan.json`) a `.knowledge/session_plan.json`.
- **`session-start.sh`:** hook de arranque. Si hay un plan activo, lo presenta antes de scorear/buscar memoria ("retomando: estábamos en el paso X"). Elimina la amnesia de sesión que el `AGENTS.md` del planner ya prohibía y nada garantizaba.
- **`session-end.sh`:** hook de cierre. Cierra y archiva el plan.
- **`session-start.sh` (path obsoleto):** el HANDOFF se resolvía en `projects/$PROJECT/.knowledge/` - estructura **pre-ADR-075**, muerta desde 2026-09-26. Se alinea con `scripts/session-handoff.py` (workspace -> `.knowledge/` propio; proyecto -> `~/projects/<slug>/.knowledge/`).

### Docs
- **`docs/session-planning-hooks.md`:** estado `PARCIAL` -> `ADOPTADO`.
- **`docs/NORTH.md`:** Etapa 2 actualizada (2 de 5 gates cableados; los 3 restantes sin cablear a propósito, con motivo).

---

### Changed
- **`EVOLUTION.md` eliminado; su contenido vive en `docs/NORTH.md`.** El blueprint de madurez de Kanam OS (etapas + metodología) pasó a la nueva sección "El camino de madurez del sistema". Había tres documentos diciendo "hacia dónde va Kanam" (`NORTH`, `EVOLUTION`, capa 4 del `ROADMAP`): ahora hay uno. Refs de agentes reapuntadas: `agents/kanam-critic/AGENTS.md` y `agents/kanam-planner/AGENTS.md` (leían `EVOLUTION.md`); entity `.knowledge/entities/projects/kanam_os.md` actualizado.
- **Los 5 specs de Kanam OS Etapa 2 documentan su estado real.** No eran huérfanos: son las specs de implementaciones vivas que nadie cableó.
  - `docs/security-scan-spec.md` -> **ADOPTADO**: cableado al pre-commit.
  - `docs/skill-evals-spec.md`, `docs/skill-lifecycle-tracker.md`, `docs/regression-control-spec.md` -> **EXPERIMENTO NO ADOPTADO** (implementación existe, nada la invoca).
  - `docs/session-planning-hooks.md` -> **PARCIAL** (el `AGENTS.md` del planner la referencia; no hay hook automático).

### Added
- **`scripts/security-scan.py --staged`:** modo gate que escanea **solo el código ejecutable staged bajo un árbol de skills** (`skills/`, `agents/<rol>/skills/`). El modo original sobre `scripts/` daba falsos positivos sobre código propio (se marca a sí mismo por citar `/etc/passwd` como patrón, los triggers `.js` por usar `exec(`, `test-skills.sh` por navegar `./../..`); `--staged` los evita por scope.
- **Pre-commit (hook + template):** corre `security-scan.py --staged` ante cambios de `skills/` o `agents/` - el caso real de "skill de afuera".

### Fixed
- **`scripts/regression_gate.py` no compilaba:** un bloque ` ``` ` de markdown al EOF, una flecha rota en un f-string y un path absoluto `/Users/...`. Reparado.
- **`scripts/lifecycle_tracker.py`:** path absoluto `/Users/...` hardcodeado. Ahora deriva del propio script.

### Removed
- **`EVOLUTION.md`** (contenido absorbido en `docs/NORTH.md`).

## [2026-10-06] - Dream Diary en rotación mensual (DREAMS)

### Added
- **`scripts/dreams-rotate.py`:** mantiene `DREAMS.md` en el mes en curso; los meses anteriores se archivan por mes en `memory/archive/dreaming/DREAMS-YYYY-MM.md`. Idempotente, solo toca el contenido entre los marcadores del diary del plugin (deja el bloque `Deep Sleep` intacto), una entrada sin fecha no se archiva. `--check`, `--dry-run`, `--today`, `--root` (tests).
- **`tests/bash/dreams-rotate.bats`:** 7 casos (drift, rota, marcadores intactos, idempotencia, `--check` limpio, `--dry-run`, fecha inválida).

### Changed
- **`skills/session-lifecycle/scripts/session-end.sh`:** rota DREAMS en cada cierre, junto con el CHANGELOG. Sin gate en pre-commit porque `DREAMS.md` está gitignored (estado local del plugin).

## [2026-10-06] - CHANGELOG con ventana de 30 días y rotación automatizada (ADR-092)

### Added
- **`scripts/changelog-rotate.py`:** mantiene `CHANGELOG.md` en una ventana activa de ~30 días; lo viejo se archiva en `docs/archive/CHANGELOG-archive.md`. Idempotente, ordena por fecha descendente, regenera los headers. `--check` (exit 1 si hay drift), `--dry-run`, `--days N`, `--today` (tests).
- **`tests/python/test_changelog_rotate.py`:** 8 casos (split, ventana, idempotencia, acumulación sin duplicados, orden, exit codes de `--check`, `--dry-run` no escribe, fecha inválida).

### Changed
- **`.git/hooks/pre-commit` + `scripts/pre-commit.template`:** nuevo check (solo si `CHANGELOG.md` está staged) que corre `changelog-rotate.py --check` y falla si el activo está desfasado.
- **`skills/session-lifecycle/scripts/session-end.sh`:** rota el CHANGELOG en cada cierre de sesión, para que la ventana nunca quede vieja.
- **`docs/archive/CHANGELOG-pre-2026-09.md` → `docs/archive/CHANGELOG-archive.md`:** el archivo pasa a ser rodante único (lo mantiene el script), no un snapshot con nombre de fecha.
- **`memory/2026-10-06.md`:** la entrada de gobernanza de esta sesión (análisis + reconciliación de AGENTS.md/AGENTS-DETALLE.md/SETUP.md), que había quedado sin commitear.

### Fixed
- **`docs/archive/` agregado a `SKIP_DIRS` de `check-refs.py` y a `MD_EXEMPT` del hook:** la historia congelada cita rutas de la época (un ADR luego renombrado) y conserva guiones largos; no se reescribe (política de ADR-084/ADR-082, igual que `docs/records/`).
- **`mindstudio_proposal.md` eliminado:** propuesta de vendor sin refs en markdown trackeado ni valor durable (Gonzo, 2026-10-06).

### Removed
- **`proposal.md`** (duplicado byte-idéntico de `mindstudio_proposal.md`) y **`mindstudio_proposal.md`**.

## [2026-10-06] - Refactor de gobernanza: AGENTS.md, AGENTS-DETALLE.md y SETUP.md reconciliados

### Fixed
- **Contradicción `.knowledge/` resuelta.** `docs/AGENTS-DETALLE.md` decía que el workspace `trackea projects/**/.knowledge/` (modelo pre-ADR-075) mientras `AGENTS.md` decía lo contrario. Se reescribió la sección "Triple Git" completa al modelo ADR-075: proyectos en `~/projects/`, workspace sin `projects/` ni `.knowledge/`, agregado vía `aggregate-sync.sh`. Anotada la deuda de `init-project.sh` (todavía resuelve `PROJECTS_DIR=workspace/projects`).
- **`HEARTBEAT.md` fantasma.** `AGENTS.md` mandaba "editar `HEARTBEAT.md`"; ese archivo no existe (git log: `182635ee2b`, 2026-10-04). Reemplazado por el estado real: checklist silencioso vía `automations`, mapa en `docs/gateway-operations.md`.
- **Referencia a API legacy.** `cron(action: wake, ...)` → `automations(action: "wake", ...)` (la sintaxis vigente).
- **`nomic-embed-text` 768 dims → 1024 dims.** `docs/SETUP.md` decía que la búsqueda semántica usa embeddings de 768 dims; los scripts usan `qwen3-embedding:0.6b` (1024 dims). El `768` de los scripts es `n_context`/truncado, no la dimensionalidad.
- **`scripts/session-start.sh` roto en `SETUP.md`** → `skills/session-lifecycle/scripts/session-start.sh`.

### Changed
- **Bloques de modelo duplicados colapsados.** `AGENTS.md` tenía DOS bloques MANAGED con el mismo contenido (`model-triple` y `model-operativo`). Se eliminó `model-triple` de `AGENTS.md`; queda un único bloque (`model-operativo`). `managed-blocks.py`: entrada `model-triple` de `AGENTS.md` removida del REGISTRY. `docs/SETUP.md` conserva su `model-triple` (mide los modelos primario/auxiliar/alternativo, ejes distintos).
- **`AGENTS.md`: "Modelos y razonamiento" fuera de `Git & Commits`.** Esa sección y "Skills Mirror & Públicas" colgaban de `Git & Commits` sin ser git. Modelos pasó a `## 3. Ingeniería`; el bloque de skills públicas (archivado 2026-09-28) se comprimió a un párrafo con puntero al detalle.
- **Política de modelos unificada.** `AGENTS.md` ahora cita **ADR-090** como fuente de modelo+thinking y explicita que supersede ADR-053 y las secciones de modelo/thinking de ADR-040. `docs/SETUP.md` y `docs/AGENTS-DETALLE.md` marcaron ADR-040 como histórico y apuntan a ADR-090.
- **Red Lines y "External vs Internal" en español.** El propio archivo declara que el workspace privado va en español; eran las últimas líneas en inglés.
- **`type(#issue)` sin issue definido.** Se aclaró: sin ticket, `type: description`.
- **Formato `type(#issue)`:** documentado el caso sin issue asociado.
- **Fechas de cierre** de `AGENTS.md` y `docs/SETUP.md` actualizadas al 2026-10-06.

### Added
- **`AGENTS.md`: margen recuperado.** Bajó de 19.542 a ~18.955 chars (límite bootstrap 20K): el colapso de bloques y la compresión de la receta de skills devolvieron holgura.

### Fixed (seed)
- **`managed-blocks.py` DEFAULTS.** `thinking_default: high` → `off` (ADR-090) y `model_by_agent` alineado al ADR-090 (antes tenía la distribución pre-cata de 2026-10-05: `planner minimax-m3`, `dev/ops glm-5.3-flash`). Es semilla: la DB ya estaba correcta; faltaba el fallback.
- **`tests/python/test_managed_blocks.py`** actualizado al nuevo default (`thinking_default == "off"`).

### Verified
- `managed-blocks.py apply` idempotente (4 bloques "al dia"); `pytest` no corre en esta máquina (no instalado), bats sí.
- Gates del pre-commit en verde: `check-refs` (489 rutas), `check-adr-integrity` (91 ADRs), `check-pipeline-enforcement` (pacto A/B consistente), `check-agent-skill-boundary`, `check-content-dirs`.
- `AGENTS.md`: bloques MANAGED restantes = `model-operativo` y `pipeline-ab`.

## [2026-10-06] - Cierre de sesion con HANDOFF del proyecto + plantilla del informe

### Added
- **`scripts/session-handoff.py`:** genera/actualiza el `HANDOFF.md` del proyecto en curso (o del workspace) al cerrar sesion. Destino: `~/projects/<slug>/.knowledge/HANDOFF.md` (ADR-075); para el sistema, `<workspace>/.knowledge/HANDOFF.md`. Deriva el HANDOFF del informe de cierre (resumen + estado + proximos pasos + decisiones + archivos tocados). Normaliza guiones largos.
- **`memory/_templates/session-close.md`:** plantilla del informe detallado de cierre de sesion (el formato de `memory/YYYY-MM-DD.md` que Gonzo pidio registrar).

### Changed
- **`skills/session-lifecycle/scripts/session-end.sh`:** reescrito. Acepta `--status`, `--next-steps`, `--decisions`; el HANDOFF lo genera `session-handoff.py` en el destino correcto (el bloque viejo apuntaba a `projects/<slug>/.knowledge` y quedo obsoleto con ADR-075). Ahora el cierre deja **dos entregables**: informe en `memory/` + HANDOFF del proyecto.
- **`skills/session-lifecycle/SKILL.md`** y **`AGENTS.md`:** documentado el doble entregable y que **"guardar sesion" y "cerrar sesion" son el mismo disparador**.
- **`memory/README.md`:** plantilla `session-close.md` registrada.

### Verified
- `session-end.sh` probado end-to-end: genera HANDOFF del workspace y escribe el informe en la DB.

## [2026-10-06] - Pagos: Stripe como proveedor unico reconocido (ADR-042 superseded de nuevo)

### Changed
- **`docs/adr/ADR-042`:** reescrito y **renombrado** a `ADR-042-stripe-pagos.md` (el slug ya no dice `mercado-pago`). **Stripe es el proveedor de pagos unico reconocido del ecosistema**, sea o no un proyecto sobre Lovable. Mercado Pago queda **fuera como intencion** (no se borra su existencia ni el trabajo previo; deja de figurar como opcion prevista). No se reconocen otros proveedores. Supersede la version intermedia de la misma fecha ("eleccion por proyecto") y la original ("Mercado Pago obligatorio").
- **`docs/adr/README.md`:** fila 042 actualizada al titulo nuevo + slug nuevo.
- **`MEMORY.md`, `AGENTS.md`:** regla de pagos simplificada a "Stripe es el proveedor unico".
- **`docs/adr/ADR-091`:** punto 3 de la decision alineado (Stripe deja de ser "excepcion"; es el proveedor reconocido).
- **`docs/APUESTAS.md`:** nota de SoporteML ajustada.
- **DB (`memory/memory.db`, tabla `learnings`):** leccion durable agregada.

### Verified
- `check-adr-integrity.py` (91 ADRs), `check-refs.py`: OK. `git mv` conserva la historia del archivo.

## [2026-10-06] - SoporteML v4 cerrado; el producto sigue por la version funcional de Lovable con cobro por Stripe

### Added
- **`docs/adr/ADR-091-soporteml-v4-cierre-stripe.md`:** cierra SoporteML v4 (supera el greenfield de ADR-068) y registra que el producto sigue por la version funcional de Lovable (v1), ahora con **cobro por Stripe** habilitado en Argentina. Decision de alcance cerrada: **la version se queda en Lovable** (no migra a stack propio); sin pendientes abiertos. Indice `docs/adr/README.md` actualizado.

### Changed
- **`docs/adr/ADR-042`:** reescrito. Deja de ser "Mercado Pago obligatorio, Stripe por excepcion": ahora **el proveedor se elige por proyecto y se justifica**. Lovable -> Stripe (unica integracion de la plataforma); fuera de Lovable, Mercado Pago es opcion fuerte (no unica) y Stripe tambien es valido. La regla deja de limitar Stripe.
- **`docs/adr/ADR-091`:** la clausula de pagos pasa de "excepcion" a "opcion natural del entorno (Lovable)".
- **`docs/adr/ADR-042` (previo, misma fecha):** titulo/estado ajustados; nota de que Argentina ya opera con Stripe.
- **`MEMORY.md`:** entrada de SoporteML reescrita (v4 cerrado; sigue por Lovable v1 con Stripe); regla de pagos actualizada (eleccion por proyecto).
- **`AGENTS.md`:** regla de pagos ajustada (eleccion por proyecto; Lovable -> Stripe).
- **`docs/APUESTAS.md`:** apuesta 2 pasa de `soporteml-v4` a `soporteml` (version funcional de Lovable) con Stripe operativo.
- **`docs/NORTH.md`**, **`docs/ROADMAP.md`**, **`memory/user-profile.md`:** referencias a `soporteml-v4` actualizadas al estado nuevo.
- **DB (`memory/memory.db`, tabla `learnings`):** leccion durable agregada (categoria `proyectos`).

### Verified
- `check-adr-integrity.py` (91 ADRs), `check-refs.py`: OK.
- El cambio a Stripe ya asomaba en superficies de CV (2026-10-01) sin haberse propagado a las fuentes durables; este ADR cierra ese hueco.

## [2026-10-06] - Bootstrap bajo cap: ROADMAP y NORTH reconstruidos, AGENTS/MEMORY/USER trimados

### Fixed
- **Bootstrap truncado (regresión):** `AGENTS.md` (20.656), `MEMORY.md` (24.017) y `USER.md` (4.582) estaban **sobre su cap de inyección** (20.000 / 20.000 / 4.000 fijo) y se descartaba contenido en silencio en cada arranque. Ahora: `AGENTS.md` 19.041, `MEMORY.md` 14.062, `USER.md` 3.976. `SOUL.md` e `IDENTITY.md` ya estaban OK.
- **`USER.md`:** corregido doble guion (`--`) que debía ser lista; compactado sin perder reglas.

### Changed
- **`docs/ROADMAP.md`:** reconstruido desde cero contra fuentes reales. Se quitó la hipótesis ya refutada de "inestabilidad del gateway" (no hay reinicios espontáneos; el problema real era el truncado del bootstrap) y el falso verde de búsqueda laboral ("oferta aceptada" que nunca existió). Se agregó la capa *Ecosistema* (análisis de 20 repos, 2026-10-01) y el item 0.1 *Integridad del bootstrap*.
- **`docs/NORTH.md`:** reconstruido. Ubicaciones de proyectos corregidas a `~/projects/` (ADR-075), Horizonte 0 rearmado sobre el estado real (sin procesos abiertos), constelación actualizada (`kanam-onwheels`, `kanam-spec`, `ollama-visor`, etc.) y orden de apuestas de `docs/APUESTAS.md`.
- **`MEMORY.md`:** destilado. Historial de decisiones de modelo/engine movido a `memory/model-history.md`; entradas de proyecto comprimidas a lo vigente con puntero a `~/projects/<slug>/.knowledge/`; agregado `kanam-onwheels`; corregida la regla de modelos (hoy ADR-090, no ADR-053).
- **`AGENTS.md`:** comprimidas las secciones de Frontera de roles, Feedback en PRs y sandbox sin perder reglas; bloque de razonamiento actualizado a ADR-090.

### Added
- **`memory/model-history.md`:** archivo del historial de decisiones de motor/modelo (2026-08 a 2026-09), movido fuera de `MEMORY.md` para bajar el bootstrap.

### Verified
- `wc -c` de los 5 archivos de bootstrap: los tres grandes dentro de cap.
- `managed-blocks.py check`: sin drift. `check-refs.py` (147 rutas), `check-content-dirs.py` (10), `check-adr-integrity.py` (90 ADRs): OK.

## [2026-10-06] - Cata persistida y "thinking leakage" re-diagnosticado como artefacto del CLI

### Changed
- **`sandbox/model-cata-2026-10-06/`:** la cata de modelos (6 modelos × 6 roles × 4 escenarios, 144 corridas + 4 evaluaciones cross) se copió de `/tmp` (efímero) al workspace. `sandbox/` está gitignored: sobrevive reboot sin inflar el repo.
- **`docs/adr/ADR-090-pensamiento-nivel-configuracion.md`:** corregida la narrativa del "thinking leakage". No era defecto del harness de producción sino **artefacto del runner de la cata** (`ollama run`, que imprime el thinking a stdout mezclado con la respuesta).

### Added
- **`sandbox/model-cata-2026-10-06/run-one-api.py`:** runner de cata corregido. Llama a `POST /api/chat` y guarda el entregable en `raw_output` y el razonamiento en `thinking_output`, en campos separados. Reemplaza el `run-one.sh`/`run-one-safe.py` basados en CLI.
- **`sandbox/model-cata-2026-10-06/verify-no-leakage.py`:** sonda que verifica la separación thinking/content.

### Verified
- **Sonda `verify-no-leakage.py`:** 6 modelos × {think off, think high} → **0 fugas**. El campo `thinking` de la API llega poblado y separado del `content`; con `think:false` el thinking viene vacío.
- **Claude Code headless** (`claude -p --model deepseek-v4.1-flash:cloud`): output limpio, sin fuga. Es el motor estándar del pipeline A/B (ADR-049) y ya separaba el razonamiento.
- **Conclusión:** no había bug de producción que arreglar. Lo útil era persistir la evidencia y corregir la narrativa. El fix real para futuras catas es usar la API, no el CLI.

---

## [2026-10-06] - ADR-090 corregido: decisión de modelos por rol vs estado real del runtime

### Changed
- **`docs/adr/ADR-090-pensamiento-nivel-configuracion.md`:** reescrito. El documento estaba desactualizado y contenía una **ref cruzada rota** (citaba `ADR-210`, que no existe) que dejaba el corpus ADR desreconciliado (`check-adr-integrity.py` fallaba). Ahora:
  - Registra la decisión de thinking por agente y la asignación de modelos por rol surgida de la cata 2026-10-06.
  - Separa explícitamente **decisión** de **estado de implementación**: el runtime (`openclaw.json`) no coincide con la decisión en 6 de 8 agentes.
  - Reemplaza context windows estimados por contextos **medidos** con `ollama show` (gpt-oss 128k, deepseek 1M, nemotron 256k, gemma4 256k, minimax 500k, glm-5.3 1M).
  - Documenta los límites reales: cata con defecto de harness, n=1 por celda, evaluadores con sesgo estructural, re-verificación post-fix sin completar.
- **`docs/adr/README.md`:** título del índice alineado al nuevo alcance del ADR.
- **`ADR-090-*.md.backup`:** a la papelera (redundante con git).

### Notes
- **Por qué:** el ADR afirmaba cambios de modelo que nunca se aplicaron al runtime; un ADR que miente es peor que no tenerlo (regla de corpus ADR + README).
- **Verificación:** `check-adr-integrity.py` → `OK: 90 ADRs, todos indexados, sin duplicados ni refs rotas`.

### Changed (corrección 2026-10-06, decisión de Gonzo)
- **Decisión de modelos corregida:** `main` y `kanam-mind` NO van a nemotron-3-super ("se pierde y quiere resolver en lugar de conversar" en asientos de orquestación/diálogo); quedan en `deepseek-v4.1-flash:cloud`. El resto de la asignación por rol se mantiene.
- **Thinking corregido:** los tres de juicio (`kanam-critic`, `kanam-auditor`, `kanam-planner`) bajan de `high` a `low`; los cinco de ejecución (`main`, `kanam-dev`, `kanam-mind`, `kanam-ops`, `kanam-studio`) pasan a `off` explícito. Default global `off`.
- **Runtime aplicado y verificado:** los 8 agentes en `~/.openclaw/openclaw.json` coinciden con la decisión (model.primary, fallbacks, thinkingDefault), vía el tool `openclaw`, sin editar el JSON a mano.
- **Bloques gestionados regenerados:** corregido el uso de `managed-blocks.py` (el bloque de AGENTS.md lee `model_by_agent`, no `model.triple`); `AGENTS.md` y `docs/SETUP.md` alineados con el runtime.
- **ADR-090:** decisión y estado de implementación actualizados; se documenta que cambiar el modelo de `main` desde una sesión que corre sobre `main` bloquea el tool (`prepared model runtime plugin generation was superseded`) y se resuelve con restart.

---

### Changed
- **`agents/kanam-dev/scripts/validate-spec.sh`:** deja de ser un validador propio y **delega** en el validador compartido de la skill (`~/.agents/skills/spec-driven-development/scripts/validate-spec.sh`). Pasa a recibir el directorio de specs como argumento (default `./specs`) y a ejecutar el compartido vía `exec`. Fallback explícito con `exit 2` si el compartido no existe.

### Notes
- **Por qué:** la versión propia chequeaba **forma, no sustancia** (daba `exit 0` sobre una spec con el Brief vacío, sin Status y con placeholders de plantilla sin completar). Dos validadores con criterios distintos es peor que uno malo: el mismo archivo pasa en uno y falla en el otro, y no se sabe a cuál creer.
- **Verificación:** el script delega y corre (`bash agents/kanam-dev/scripts/validate-spec.sh <dir>`); el original queda recuperable en `git HEAD` y su copia `.bak-share-20261005` es redundante con git (se retira).
- **Origen:** cambio de una sesión previa del día quedó sin commitear en el árbol (mtime 12:24); se documenta el rationale y se registra acá.
- Sin commit: el Core verifica primero (ADR-078).

---
