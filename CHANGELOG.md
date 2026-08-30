# CHANGELOG.md

Registro de cambios estructurales del workspace. No incluye cambios de skills (ver `skills/CHANGELOG.md`), aprendizajes (ver `docs/LEARNINGS.md`), ni actividad diaria (ver `memory/`).

**Regla:** cada vez que se modifique la estructura del workspace (AGENTS.md, MEMORY.md, SOUL.md, USER.md, TOOLS.md, HEARTBEAT.md, scripts/, estructura de proyectos, skills), actualizar este archivo en el mismo commit.

---

## [2026-08-29] - Cambio de motor del pipeline A/B: DeepSeek V4 Flash → GLM 5.3 Flash

### Changed
- **`MEMORY.md`** (seccion "Modelo default y config de tools"): los agentes A/B pasan de `deepseek-v4-flash:cloud` a `glm-5.3-flash:cloud` en high. Registrada la comparativa de 5 modelos (mismo prompt pesado de arquitectura de agentes) y la leccion de niveles de razonamiento (max no es driver de calidad; agentes de codigo siempre en high).
- **`TOOLS.md`** (secciones "Modelos" y "Pipeline de agentes"): motor estandar actualizado a `glm-5.3-flash:cloud`, ficha de GLM-5.3-Flash (multimodal nativo: imagen/video/PDF, 1M de contexto, 320B/18B MoE, MIT), modelos cloud actualizados.
- **Config de OpenClaw (`~/.openclaw/openclaw.json`):** default general `agents.defaults.model.primary` cambió a `glm-5.3-flash:cloud`; ecosistema purgado a 3 modelos cloud (glm-5.3-flash, glm-5.3, gemma4) - fuera: DeepSeek V4 Flash/Pro, Kimi K2.7/K3, MiniMax M3, Qwen3.5, Nemotron, Gemma4:31b. Ficha glm-5.3-flash corregida con specs verificados (input imagen + maxTokens 131072). Backup previo: `openclaw.json.bak-20260829`.

- **`.gitignore` + memoria:** dailies viejos (13-24/08) archivados a `memory/archive/` (verificados identicos antes de borrar); `memory/export/` (chunks derivados de indices, regenerables) agregado al gitignore.

### Why
- Comparativa del 2026-08-29 con el mismo prompt de diseño de agente autonomo en 5 modelos: Kimi K2.7 Code (xhigh) fue el mejor pensador (tiers de autonomia ganados con metricas), GLM 5.3 (sin razonamiento) el mejor criterio, GLM 5.3 Flash el mejor "chico" (orden de evidencia, red→green, limites verificables fuera del modelo), y DeepSeek V4 Flash (xhigh) el mas estructurado pero el menos agudo (y en max filosofa, ADR-040). GLM 5.3 Flash reemplaza a DeepSeek V4 Flash: mas agudo, multimodal, mas barato. Kimi K2.7 Code queda como candidato a re-testear en high cuando haya GPU.

---

## [2026-08-27] - Fix gitignore: repos embebidos y .knowledge/

### Fixed
- **`.gitignore`:** los patrones especificos de repos embebidos (`/projects/kanam-forge`, `/projects/kanam-mind`, etc.) rompian el `git add` de archivos en `.knowledge/` (git se niega a agregar contenido bajo un directorio ignorado). Se eliminaron y el patron global (`/projects/*/*` + `!/projects/*/.knowledge/`) los cubre. Excepcion: `kanam-skills` (repo publico independiente, su `.knowledge/` con assets no se trackea en el workspace) mantiene su linea especifica.
- **`projects/kanam-forge/.gitignore`:** se movio `/.knowledge/` al `.git/info/exclude` del repo. El `.gitignore` del repo embebido bloqueaba el `git add` del workspace sobre `.knowledge/` de kanam-forge. Ahora el workspace puede trackear `.knowledge/` y el repo publico de kanam-forge sigue sin trackearlo (via exclude local). Commit `4449382` en kanam-forge.

### Why
- Al guardar sesion, el `STATUS.md` de kanam-forge (actualizado en la sesion de hoy) no se podia commitear: el `.gitignore` del workspace y el del repo embebido lo bloqueaban. Bug latente que recien se nota cuando hay cambios en `.knowledge/` de un repo embebido.

---

## [2026-08-27] - Leccion de ingenieria: validar fixes visuales con browser real

### Added
- **`MEMORY.md`** (seccion "Reglas de ingenieria"): nueva sub-seccion **"Validar fixes visuales con browser real, no con jsdom/headless"** con la leccion aprendida del PR #10517 de react-spectrum. jsdom no hace layout; Playwright headless usa `chromium_headless_shell` que renderiza `appearance: auto` distinto que Chrome desktop. Regla: para fixes UI, los tests automatizados no son suficiente - hay que abrir Chrome/Firefox/Safari desktop y mirar.

### Why
- El PR #10517 tenia browser tests reales con Playwright que pasaban + tsc limpio + formato OK + validacion con VoiceOver OK. Pero al validar visualmente con Chrome desktop, Gonzo detecto que el chrome nativo del input se renderizaba encima del SVG custom - bug preexistente que jsdom/headless no detecta. Si solo se hubiera confiado en los tests automatizados, el PR habria mergeado con un bug visual critico.

---

## [2026-08-27] - Reorganizacion de docs/ por categoria (pipeline y entrevistas)

### Changed
- **`docs/`:** dos documentos de referencia general movidos a carpetas propias:
  - `docs/pipeline/kanam-product-pipeline.md` - el mapa de skills del workspace (Define→Plan→Build→Verify→Review→Ship)
  - `docs/entrevistas/OpenSistemas-OpenClaw-Resumen-Capacidades.md` - material de apoyo para la entrevista con OpenSistemas
- **`CHANGELOG.md`:** actualizadas las referencias a `docs/pipeline/kanam-product-pipeline.md`.
- **`skills/agent-orchestration-pipeline/SKILL.md` y `.github/skills/agent-orchestration-pipeline/SKILL.md`:** actualizada la referencia al pipeline a `docs/pipeline/kanam-product-pipeline.md`.

### Why
- Completar la organizacion de `docs/` por categoria: los documentos de referencia general con identidad propia (pipeline de skills, material de entrevistas) tienen carpeta propia, consistente con `linkedin/`, `feedback/`, `prs/`, `adr/`, `checklists/` y `learnings/`.

---

## [2026-08-27] - Reorganizacion de docs/ por categoria

### Changed
- **`docs/`:** los drafts de LinkedIn, feedback y PRs ahora viven en carpetas por categoria en lugar de amontonados en la raiz:
  - `docs/linkedin/` - posts de LinkedIn (`astryx-4605.md`, `astryx-5419.md`, `astryx-5493.md`, `oss-2026-08-24.md`)
  - `docs/feedback/` - borradores de feedback a PRs ajenos (`astryx-*-draft.md`)
  - `docs/prs/` - borradores de PRs propios (`9687-draft.md`)
- **`AGENTS.md`:** actualizada la regla de contexto de feedback a `docs/feedback/<repo>-<numero>-draft.md`.
- **`MEMORY.md`:** actualizada la convencion de posts de LinkedIn a `docs/linkedin/*.md`.

### Why
- Los drafts de las tres categorias estaban amontonados en la raiz de `docs/` junto a documentos de referencia general. Separarlos por categoria hace el historial consultable y consistente con `adr/`, `checklists/` y `learnings/`.

---

## [2026-08-27] - Guia MAX vs HIGH + regla de nivel de razonamiento

### Added
- **Modelo de razonamiento definitivo:** Kanam (OpenClaw) corre SIEMPRE en thinking `max`; los agentes A/B del pipeline corren SIEMPRE en `high` con `deepseek-v4-flash:cloud` (kimi-k2.7-code en medium como salto si tras mejorar el prompt no se llega a resultado).

### Changed
- **`~/.openclaw/openclaw.json`:** `agents.defaults.thinkingDefault = "max"` (era high).
- **`AGENTS.md`:** reescrita la seccion de niveles de razonamiento. Kanam piensa en MAX (decide/planifica/arma prompts), agentes ejecutan en HIGH (escriben codigo/corrigen bugs). Default automatico: cada vez que se pida escribir codigo, usar el pipeline A/B en HIGH sin pedirlo. Flujo punta a punta de corrido sin interaccion (analisis -> A escribe -> B revisa -> iterar alternando orden -> revision final en max -> push -> borrador).
- **`docs/adr/ADR-040-modelos-seleccion-por-tarea.md`:** actualizada la guia de niveles por rol (Kanam MAX, agentes HIGH).
- **`MEMORY.md` y `TOOLS.md`:** reflejan el modelo nuevo.
- **`docs/pipeline/kanam-product-pipeline.md`:** actualizado el modo multi-agente con el modelo de razonamiento (Kanam max, agentes high) y el flujo punta a punta; actualizado el flujo de PR de accesibilidad para reflejar la revision final de Kanam en max y el push antes del borrador.

### Why
- Gonzo reestructuro el modelo: el maximo razonamiento debe estar en el orquestador (Kanam), no en los ejecutores (agentes). Elimina la friccion de cambiar niveles: Kanam fijo en max, agentes fijos en high. El flujo completo corre punta a punta sin interaccion, con el push y el borrador del PR como entregables.

---

## [2026-08-26] - Comando add-contribution en memory-db.sh

### Added
- **`scripts/memory-db.sh add-contribution`:** nuevo subcomando para registrar contribuciones OSS en la DB (`memory/memory.db`, tabla `contributions`) sin SQL manual. Firma: `add-contribution <repo> <pr> <pr_url> <status> "<detail>" [context] [issue] [issue_url] [tier] [tipo]`. Campos opcionales con defaults (tipo default `pr`; `collab` para no-codigo). Escapa comillas para SQL seguro.

### Changed
- **`docs/OSS-TRACKER.md`:** regenerado con `export-oss`. Registrado el merge de `facebook/astryx` PR #5493 (TreeList forward BaseProps, a11y).

### Why
- Al registrar el PR #5493 en el tracker, faltaba un comando dedicado y hubo que insertar con SQL directo. Agregarlo es el principio Boy Scout (dejar el workspace mejor) y evita SQL manual futuro.

---

## [2026-08-26] - ADR-039: Changesets (cuando usarlos y como)

### Added
- **`docs/adr/ADR-039-changesets-cuando-y-como.md`:** nuevo ADR de alcance workspace. Define cuando un proyecto debe usar changesets (librerias publicadas a npm con semver y changelog generado) y cuando no (apps de producto, mantener CHANGELOG.md). Incluye el formato del archivo y el tipo de bump. Nace de la colaboracion en facebook/astryx PR #5493, donde el reviewer pidio un changeset.
- **`docs/adr/README.md`:** agregado ADR-039 al indice.

### Why
- El workspace no tenia un criterio explicito sobre cuando usar changesets. La colaboracion en astryx mostro que es practica estandar de la industria para librerias publicadas, y quedo documentado para no depender de la memoria.

---

## [2026-08-26] - Configuracion de modelos OpenClaw en VPS

### Changed
- **`/data/.openclaw/openclaw.json`:** reordenados fallbacks del modelo default. Primer fallback ahora `ollama-cloud/kimi-k2.7-code` (antes `ollama-cloud/glm-5.2`); `glm-5.2` pasa al final de la lista. Cambiado primary a `ollama-cloud/deepseek-v4-flash:preview`.

### Why
- La API key de `ollama-cloud:default` era invalida (`Unauthorized` para `deepseek-v4-flash`), haciendo que el sistema saltara automaticamente a `glm-5.2` en cada turno. Mientras se resuelve la key, `deepseek-v4-flash:preview` funciona y `kimi-k2.7-code` es un fallback mucho mas barato.

### Pending
- Re-generar/verificar la API key de Ollama Cloud para que funcione `deepseek-v4-flash` sin `:preview`.

---

## [2026-08-26] - Fusion de skills de estudio + indice maestro unico

### Changed
- **`studies/README.md` (indice maestro):** reescrito. Ahora lista cursos online (Codecademy) Y libros gamificados (Packt), con la regla dura de una sola fuente de verdad: todo en `studies/<slug>/`, nunca `study/`.
- **`studies/`:** unificado. Movido el libro de Packt de `study/` (singular) a `studies/openclaw-ai-in-production/`; eliminado `study/`.

### Added
- **`skills/CHANGELOG.md`:** creado (faltaba - era deuda tecnica referenciada desde CHANGELOG principal y AGENTS.md). Registra cambios de skills.

### Why
- Fusion de las skills `study-tracker` + `learning-tracker` en una sola (`study-tracker`, "One Skill to Rule Them All") para una unica fuente de verdad de estudios. Inconsistencia real: curso en `studies/`, libro en `study/`. Detalle completo en `skills/CHANGELOG.md`.

---

## [2026-08-25] - Quitar PR review del inicio/cierre de sesion

### Changed
- **AGENTS.md (ritual "iniciar sesion"):** quito el paso 1 "PR Review Check" (auto-review de PRs abiertos con `gh`). Ahora los PRs los revisa Gonzo manualmente en GitHub y pasa los URLs. Los pasos quedan: 1) Daily check, 2) Memory search, 3) Presentación.
- **skills/session-lifecycle/scripts/session-end.sh:** quito el bloque "Check open PRs" del cierre de sesion (ya no llama a `pr-status-check.sh`).
- **skills/session-lifecycle/SKILL.md:** actualizo la tabla de helper scripts.
- **MEMORY.md:** preferencia durable - inicio/cierre de sesion NO revisa PRs automaticamente.

### Why
- Gonzo revisa los PRs manualmente en GitHub y pasa los URLs a revisar. El auto-check de PRs en el ritual de sesion ya no aporta.

---

## [2026-08-24] - Regla: no agradecer a bots de review (AGENTS.md)

### Added
- **AGENTS.md (Reglas operativas de feedback, punto 7):** regla "No agradecer a bots de review" - cuando el review de un PR es de una IA (ej: Enough1122 en hermes-agent, "AI code review - automated review for reference"), NO ponerle "Thanks for the review"; solo se agradece a humanos. Los reviews de IA con puntos accionables se responden directo a la sustancia con evidencia, sin saludo.
- **MEMORY.md:** referencia corta a la regla canónica en AGENTS.md (no duplica el texto completo).

### Why
- Correción de Gonzo en sesión: no agradecer a bots de review de código, solo a humanos. Regla operativa que encaja con las otras reglas de feedback en AGENTS.md.

---

## [2026-08-24] - CV búsqueda laboral (Principal Full Stack)

### Added
- **`memory/tmp/CV_Gonzalo_Blasco_Principal_FullStack.pdf`** (+ `.md` fuente): CV reorientado al rol Principal Full Stack (Ritz-Carlton Yacht Collection). Título a Principal, perfil con ADRs y estándares de arquitectura, sección de skills Arquitectura & DevOps, Selected Projects = 3 sólidos (a11y-fixer, kanam-skills, create-stack). **SoporteML v4 sacado** (no está listo para portfolio, es privado).

### Changed
- **Open Source corregido con datos reales** (verificados con `gh`): 4 merges en MUI (material-ui #49003, base-ui #5551) + Facebook astryx (#4605, #4914), reviewer activo TanStack Query, 17+ PRs abiertos. El CV anterior decía merges en shadcn/ui, TanStack Router y Vercel AI SDK, pero NINGUNO de esos está mergeado - era información incorrecta.

### Why
- Búsqueda laboral activa: 2 procesos en paralelo (Ritz-Carlton Principal, EY Frontend Lead vía LTM). CV desactualizado y con datos falsos en Open Source; no se podía mandar así.

---

## [2026-08-24] - Reglas operativas de feedback OSS en AGENTS.md

## [2026-08-24] - Reglas operativas de feedback OSS en AGENTS.md

### Added
- **AGENTS.md (Colaboracion OSS):** seccion nueva "Reglas operativas de feedback en PRs/issues ajenos" con reglas duras de Gonzo (corregidas 24/08): leer SIEMPRE toda la vida del ticket antes de comentar; el autor del PR/issue define (ver quien lo creo) - no elogios; no subir un comentario solo para disculparse por otro (disculparse no esta mal, pero genera ruido - mejor borrar el malo y regenerarlo); no repetir lo ya dicho; NO exponer notas internas/borradores en el hilo publico (usar solo el texto limpio); siempre dar la URL al reportar. Regla de contexto: borradores en `docs/feedback/*-draft.md`, el archivo y el texto a publicar son cosas distintas.

### Why
- Gonzo: "no puedo confiar sino en ti para tareas largas si en estas breves ya tengo que estar corriendote". Los errores del dia (publicar sin leer el hilo completo en #4690, exponer notas internas en #5204 y #4611, elogios en PR ajeno en #5414) se consolidaron como reglas duras en las instrucciones, no en memorias.

---

## [2026-08-24] - Regla dura: referencia git ≠ proyecto (leccion por perdida de token)

### Added
- **AGENTS.md (Red Lines):** regla "Referencia ≠ proyecto" - un gitlink/referencia de git es SOLO un puntero; quitar la referencia NUNCA debe tocar la carpeta del proyecto con sus datos locales (DB, `.env`). Antes de tocar cualquier referencia o limpiar un proyecto, verificar que datos locales NO viajan por git y respaldarlos ANTES.
- **AGENTS.md (Workspace Git):** seccion "Datos que NO viajan por git" - `.env`, `*.db`, uploads, tokens de clientes son irrecuperables y no se regeneran facil. Regla: respaldar SIEMPRE `.env` y `*.db` a `backups/<proyecto>/` antes de mover/limpiar/re-clonar.
- **MEMORY.md:** leccion dura registrada (referencia ≠ proyecto, soporteml-v4, perdida del token de MeLi de un cliente).

### Why
- Al remover la referencia del submódulo `soporteml-v4` (2026-08-23) se perdio la DB local (`soporteml.db`) con el token de acceso real de Mercado Libre de un cliente - irrecuperable, sin respaldo. La laptop estuvo encendida todo el finde justamente para protegerlo. Leccion: los datos que no viajan por git deben respaldarse antes de cualquier limpieza/movimiento, y no minimizar la perdida de un token de cliente.

---

### Added
- **Carpeta `forks/`** para repos de terceros (TanStack, shadcn, etc.): ignorada AL 100% en el workspace (no llevan `.knowledge/` porque no se modifica el `.gitignore` de proyectos ajenos). Memoria de sesion de contribucion va a `docs/` o `memory/`.
- **AGENTS.md:** regla de forks actualizada - `projects/` = proyectos propios (trackea `.knowledge/`), `forks/` = repos ajenos (ignora todo).

### Changed
- **`.gitignore`:** patron global `!/projects/*/.knowledge/**` reemplaza el listado manual por proyecto. Ahora trackea `.knowledge/` de CUALQUIER proyecto automaticamente, sin listar cada uno.
- **Trackeado en el workspace el `.knowledge/` de 6 proyectos** que estaban en disco pero no en el repo: a11y-fixer (2), create-stack (6), kanam-solitaires (6), quedamos (11), soporteml (1), ultimo-turno (3) = 29 archivos. Mecanismo: `git hash-object -w` + `git update-index --cacheinfo` (git add normal no funciona dentro de repos embebidos/worktrees).

---

## [2026-08-24] - Fix memory-db.sh: quoting SQL en helpers de insert

### Fixed
- **`scripts/memory-db.sh`:** los helpers `add-todo`, `add-inbox` y `add-learning` interpolaban valores crudos en el SQL, rompiendose con comillas simples o contenido multilinea (fallo real al insertar una leccion).
- **`sql_escape()`:** nueva funcion que escapa comillas simples (`'` → `''`) para interpolacion SQL segura. Aplicada a los tres helpers.
- **`add-learning`:** ahora acepta contenido multilinea por `@archivo` o `-` (stdin), ademas del argumento directo, para no depender del quoting del shell.
- Verificado con tests: comillas simples/dobles, multilinea, `$`, acentos y backticks se preservan en round-trip.

---

## [2026-08-24] - OSS-TRACKER: colaboraciones no-codigo

### Added
- **Tabla `contributions`: columna `tipo`** (`pr` default | `collab`) para distinguir PRs de colaboraciones no-codigo (comentarios, reviews, audits, diagnostico que llego a main via PR de otro).
- **`scripts/memory-db.sh export-oss`:** seccion "Colaboraciones no-codigo" en el OSS-TRACKER, separada del PR Registry. Metricas del resumen separan PRs de colaboraciones.
- **Retro-carga de 6 colaboraciones historicas:** astryx #3797/#5107/#4157/#5034/#3677 (diagnostico de Gonzo que llego a main via PR de otro) + hermes-agent #38072 (re-audit comentado).

---

## [2026-08-24] - Colaboración OSS: NO es abrir PRs

### Added
- **MEMORY.md (regla de Gonzo):** colaborar en un repo ajeno NO es sinónimo de abrir PR. El valor suele estar en comentar, revisar, criticar con sustancia, o destrabar. Si otro contribuidor ya reclamó/tiene un finding o PR en curso, abrir otro PR para lo mismo es pisarle el trabajo, no colaborar. Antes de proponer "hacer un PR", preguntar si ya hay trabajo en curso y qué aporta Gonzo sin duplicar. (Nace de hermes-agent #38072.)
- **AGENTS.md (nueva subsección "Colaboración OSS - NO es abrir PRs" en Git & Commits):** regla operativa de colaboración - no asumir PR, sumar sin pisar, y leer SIEMPRE el link completo (issue/PR) con todos los reviews/comentarios/estado antes de registrar o proponer acción.
## [2026-08-24] - task-notify.sh: notificacion desktop al terminar tarea

### Added
- **scripts/task-notify.sh:** notificacion nativa macOS (osascript) cuando un agente termina una tarea. Util en pipeline A/B para saber cuando un agente termino sin pollear.

### Why
- Cerrar el ciclo de notificacion del pipeline (idea del plugin Task Notifier, ClawHub).

---

## [2026-08-24] - search-fusion: estrategia de busqueda por intencion

### Added
- **skills/search-fusion/SKILL.md:** guia de busqueda efectiva por intencion (research/keyword/answer/news/code) + flujo de fusion multi-fuente (buscar + leer + cruzar + dedupe). Portado del concepto Search Fusion (ClawHub) adaptado a nuestras herramientas (DuckDuckGo key-free + web_fetch + browser).

### Why
- Mejorar la calidad de las busquedas: elegir la estrategia segun la intencion y no conformarse con el primer resultado. Verificar antes de responder (regla de Gonzo).

---

## [2026-08-24] - Resumen estructurado de compactacion en session-lifecycle

### Changed
- **skills/session-lifecycle/SKILL.md:** seccion "Resumen estructurado de compactacion" - al compactar, generar resumen con campos (Scope, Pending work, Key files, Decisions, Key timeline, Next step) en vez de texto generico. Portado del concepto Session Compact (ClawHub).

### Why
- Al compactar, hoy se pierde contexto por resumen generico; los campos estructurados capturan lo esencial (pendientes, archivos, decisiones, siguiente paso) para retomar sin re-descubrir.

---

## [2026-08-24] - model-router.sh: rutas de modelo por tarea + overrides

### Added
- **scripts/model-router.sh:** router de modelo Ollama por tipo de tarea (code/review/long/cheap/writing) + overrides sticky. Consulta `model <tipo>` para decidir el --model del agente. Portado del concepto ToggleLogic (ClawHub) SIN su licencia patentada - rutas configurables + overrides a nuestro modo.
- **skills/agent-orchestration-pipeline/SKILL.md:** seccion "Seleccion de modelo por tarea" - como usar model-router.sh al lanzar agentes.

### Why
- Autonomizar el modelo dinamico (hoy elegimos deepseek/kimi a mano): con rutas por tipo + overrides sticky, la decision de modelo se formaliza y persiste.

---

## [2026-08-24] - pdf-tool.sh + skill: manejo local de PDFs y OCR

### Added
- **scripts/pdf-tool.sh:** toolkit PDF/OCR local (check, info, text, pages, search, ocr via tesseract, pdfimages, **md2pdf**). 100% local, sin servicios cloud. Requiere poppler + tesseract (brew install poppler tesseract) para lectura, y node/npx (md-to-pdf) para generar PDF desde MD.
- **skills/pdf-tool/SKILL.md:** documenta cuando/como usar pdf-tool.sh (leer specs, OCR de escaneados, metadata, buscar, **exportar MD a PDF**).

### Dependencies
- **poppler** instalado via brew (pdftotext/pdfinfo/pdftoppm).
- **tesseract** ya estaba instalado (OCR).

### Why
- Util para specs, docs, recibos y documentos en PDF. Portado de la familia PDF/OCR de ClawHub (media+tools), como pidio Gonzo (interes en trabajar con PDF).

---

## [2026-08-24] - Portes ClawHub: anti-repetition en DREAMS + flush pre-compactacion

### Changed
- **skills/knowledge-management/SKILL.md:** seccion "Anti-Repetition en la Consolidacion" dentro de DREAMS.md - exclude promoted, text-level dedupe, theme cooldown, narrative freshness, idle novelty (idea del plugin memory-lancedb-dreaming). Evita repetir el mismo material al consolidar.
- **skills/session-lifecycle/SKILL.md:** paso "Flush ANTES de compactar" en el working buffer - asegurar que el buffer este completo antes de perder contexto, no despues (idea de Honcho Memory).

### Why
- Consolidacion programada (DREAMS) tendia a repetir material; el anti-repetition lo evita.
- El flush antes de compactar asegura no perder contexto importante al compactar.

---

## [2026-08-24] - compaction-domain-aware: tiers de prioridad al compactar

### Added
- **skills/compaction-domain-aware/SKILL.md:** compactacion de contexto con conciencia de dominio - tiers 0-4 de que preservar (Tier 0 = ADRs/arquitectura/API contracts/seguridad preservar completo; Tier 4 = chit-chat descartar). Dominios: software, a11y, oss, supabase. Complementa session-lifecycle (working buffer) y compaction-context (plugin). Portado del concepto DomainAwareCompaction (ClawHub).

### Why
- Al compactar, hoy se preserva por mensajes recientes + buffer; esta skill garantiza que los items criticos (ADRs, invariantes, criterios de aceptacion) esten textualmente preservados, no solo resumidos.

---

## [2026-08-24] - pipeline-track.sh: estado durable + crash recovery del pipeline A/B

### Added
- **scripts/pipeline-track.sh:** tracker de estado durable del pipeline A/B (init/start/review/done/status/resume/note). Sobrevive a SIGKILL, restarts y eviction de contexto via pipeline-state.json. Portado del concepto Pipeline Architect (ClawHub).
- **skills/agent-orchestration-pipeline/SKILL.md:** seccion "Estado durable del pipeline + crash recovery" - como usar pipeline-track.sh y el flujo de crash recovery tras SIGKILL.

### Why
- Directo al problema de Qwen muriendo con SIGKILL: hoy el orquestador verifica y relanza manualmente; con estado durable, `resume` lista que relanzar tras un crash.

---

## [2026-08-24] - skill-router: sugerir skill por tarea (embeddings local)

### Added
- **scripts/skill-router.py:** dado un prompt/tarea, matchea contra las skills del workspace (cascada L1 keyword gratis + L2 embedding semantico via Ollama nomic-embed-text local) y sugiere top-N. Portado del concepto del plugin skill-ai-inject (ClawHub), adaptado a nuestro stack. 100% local.
- **skills/skill-router/SKILL.md:** skill que documenta cuando y como usar skill-router.py (al iniciar tarea, listar skills, interpretar resultados).

### Why
- Resolver el problema de saber cual de las 67 skills aplicar a una tarea. El embedding semantico domina sobre el keyword para reflejar la intencion real.

---

## [2026-08-24] - Portadas de ClawHub: noise filtering + safe-fetch

### Added
- **scripts/safe-fetch.sh:** URL pre-flight security check 100% local (esquema https, blocklist, typosquatting con variantes conocidas + near-match, payload prompt injection en path/query). Portado del concepto del plugin PreClick (ClawHub) SIN mandar URLs a terceros. Exit codes: 0 ALLOW, 1 DENY, 2 CAUTION.
- **skills/knowledge-management/SKILL.md:** seccion "Noise Filtering - Que No Persistir a la Memoria" - regla para no escribir HEARTBEAT_OK/cron/confirmaciones/ruido operativo en dailies/memoria (idea del plugin Honcho Memory de ClawHub).

### Why
- Ejercicio de analisis ClawHub (12 categorias): adoptar ideas de plugins de terceros a nuestro stack propio, sin instalar. Primera ronda de portage de candidatos rapidos.

---

## [2026-08-24] - github-pr-risk.sh: detector de riesgos para cross-review

### Added
- **scripts/github-pr-risk.sh:** detector de risk signals de un PR (schema/migraciones, auth, secrets/config, API publica, dependencias, PR grande) + hints del titulo (breaking, hotfix, refactor) + preguntas de review sugeridas. Portado de las heurisiscas del plugin github-workflow de chris-openclaw (analizado en sandbox), adaptado a gh CLI + jq. Sin nuevas dependencias.
- **sandbox/:** carpeta nueva para pruebas temporales y analisis aislado. NO se commitea (en .gitignore). Se uso para clonar y analizar el plugin github-workflow.

### Changed
- **skills/agent-orchestration-pipeline/SKILL.md:** nueva seccion "Detector de riesgos en el cross-review" - documenta el uso de github-pr-risk.sh para darle al agente revisor senales de riesgo antes de revisar (uso bajo demanda, no en el batch del dashboard).

### Decision
- NO instalar el plugin github-workflow. En cambio, portar las 3 ideas buenas (risk signals por path, agrupacion por estado, review-requested:@me) a nuestro stack propio. El dashboard actual (pr-dashboard.sh) ya es mejor que el plugin en clasificacion (usa reviewDecision real, no heuristica de comments), asi que no se toca.

---

## [2026-08-23] - Spike ForgeCode: probado y descartado

### Changed
- **MEMORY.md:** nueva lección en "Lecciones clave del pipeline" - los harnesses de terminal tipo Claude Code (ForgeCode y similares) NO son orquestables por agente (son TUI que necesitan TTY real en su uso normal, fallan con `Device not configured` en headless). Matiz: es límite del entorno del agente, no de la herramienta. Regla: verificar ejecución sin TTY en uso normal (no solo setup) antes de evaluar un CLI de terminal.
- **memory/2026-08-23.md:** registro del spike completo (qué se probó, causa raíz verificada, conclusión para no repetir).

---

## [2026-08-23] - ADR-038: Learnings con mirror en DB

### Added
- **docs/adr/ADR-038-learnings-mirror-db.md:** documenta la decisión de separar las lecciones por categoría en `docs/learnings/` con mirror en la DB (`memory/memory.db`, tabla `learnings`) como fuente de verdad. Incluye el límite del patrón (no extrapolar a documentos narrativos puros como MEMORY.md/AGENTS.md).
- **docs/adr/README.md:** ADR-038 agregado al índice (origen: workspace).

---

## [2026-08-23] - Learnings separados por categoría + mirror en DB

### Added
- **docs/learnings/:** lecciones separadas por categoría (a11y, oss, pipeline-agentes, infraestructura, proyectos, metodologia). LEARNINGS.md queda como portada-índice con links.
- **Tabla `learnings` en memory/memory.db:** mirror de las lecciones con categoría + tags para consulta veloz al arrancar una tarea. Fuente de verdad: la DB.
- **scripts/migrate-learnings.py:** migra docs/LEARNINGS.md a la tabla learnings (clasifica por categoría, separa sub-lecciones).

### Changed
- **scripts/memory-db.sh:** nuevos comandos `learnings [categoria]` (consulta rápida), `add-learning` (agregar lección), `export-learnings` (regenera docs/learnings/ desde la DB). `stats` ahora incluye el conteo de learnings.
- **docs/LEARNINGS.md:** de archivo monolítico (681 líneas, 40+ lecciones) a portada-índice con links a las categorías.

---

## [2026-08-23] - Limpieza de projects/: HANDOFF obsoleto eliminado, PROYECTOS.md alineado

### Removed
- **projects/HANDOFF.md:** eliminado. Handoff obsoleto de un "Proyecto Mobile End-to-End" (brainstorming inconcluso de julio 2026, sin decisión tomada). Referenciaba workflows inexistentes (`workflow-product-discovery`, `workflow-build-scaffold`). No corresponde a la estructura actual (cada proyecto tiene su HANDOFF en `.knowledge/`). Movido a trash.

### Changed
- **projects/PROYECTOS.md:** reestructurado como índice universal (sin indicar máquina de clonado - Gonzo trabaja entre dos computadoras). Lista todos los repos propios de GitHub (OWN + `kanam-forge` como único fork adoptado). Los `gonzoblasco-*` (payload, primitives, router) son repos espejo OSS para PRs, no proyectos. Separado en Activos / Archivados / Eliminados.

---

## [2026-08-23] - Corrección de título en LEARNINGS.md

### Changed
- **docs/LEARNINGS.md:** corregido el título. Decía `# LEARNINGS.md - Kanam's Solitaires` (nombre de un proyecto de juegos, sin relación con el contenido). Ahora `# LEARNINGS.md - Lecciones aprendidas del workspace`, consistente con el patrón de otros archivos de docs.

---

## [2026-08-23] - Limpieza de docs/checklists/

### Removed
- **docs/checklists/orchestration-patterns.md:** eliminado. Contenido desalineado con el setup real: describía un sistema de orchestration con "personas", "slash commands" y plugins de Claude Code que no corresponde al pipeline real de agentes Qwen (`agent-orchestration-pipeline`). Huérfano (nadie lo referencia desde docs/ - las referencias de la skill `doubt-driven-development` apuntan a su propia copia en `references/`). Movido a trash.

### Changed
- **docs/checklists/task-template.md:** corregidas referencias rotas a skills inexistentes (`task-execution`, `gh-issue-planner`). Ahora apunta a `planning-and-task-breakdown`.
- **docs/checklists/ (observability, performance, security):** reemplazados en dashes (U+2013) por guion común en rangos numéricos. Regla de Gonzo.

---

## [2026-08-23] - Refactor de ADRs: numeración única + template unificado

### Changed
- **docs/adr/:** Renumerados los 37 ADRs con numeración única secuencial (001-037) por orden cronológico. Eliminadas las colisiones de numeración (ADR-001 a 005 y 010-011 tenían duplicados). Renombrados todos los archivos a `ADR-NNN-slug.md` descriptivo.
- **docs/adr/:** Unificado el template de todos los ADRs: metadata consistente (`Status`/`Fecha`/`Origen`), secciones h2 estandarizadas (`Consequence`→`Consequences`), 5 ADRs compactos (testing) convertidos de formato bold a secciones. README.md actualizado con el índice completo y links verificados.
- **MEMORY.md:** Referencia de Lucide actualizada (ADR-030→ADR-037).

---

## [2026-08-23] - Pipeline de producto actualizado, referencia eliminada

### Changed
- **docs/pipeline/kanam-product-pipeline.md:** agregadas skills agent-orchestration-pipeline-model-arbitration y memory-wiki-workflow al pipeline de soporte. Fecha actualizada (2026-08-23).

### Removed
- **docs/reference/ai-agent-setup.md:** eliminado. Era referencia conceptual no operativa ("no se ejecuta"), huérfana (nadie la referenciaba) con frontmatter de skill obsoleto. Movido a trash. La carpeta docs/reference/ (vacía) también se eliminó.

---

## [2026-08-23] - Eliminado script roto y referencias a products/

### Removed
- **scripts/simple-context-extractor.js:** eliminado. Estaba roto (SyntaxError: doble declaración de `workspaceDocs`), con bug de `products/` (línea 46, directorio que ya no existe), y nadie lo usaba. Reemplazado por el sistema de memoria real (memory-db, dailies).

### Changed
- **TOOLS.md:** quitada la referencia al script eliminado de la tabla de scripts. Verificado que no quedan referencias a `products/` en archivos activos (solo en skills como "products/features", que es inglés legítimo).

---

## [2026-08-23] - Refactor AGENTS.md por taxonomía

### Changed
- **AGENTS.md:** Reorganizado en 4 bloques numerados (Conducta, Sesión y Memoria, Ingeniería, Referencias). Eliminado boilerplate muerto (`Make It Yours`, `First Run`). Unificadas las 3 secciones de git/commits dispersas en una sola sección "Git & Commits". Separadores `---` entre bloques para escaneo visual rápido.
- **CHANGELOG.md:** Puesto al día con el historial de git (estaba desactualizado desde 2026-07-25). Agregada regla de actualización obligatoria.

---

## [2026-08-23] - Refactor CONTRIBUTING.md

### Changed
- **CONTRIBUTING.md:** Alineado con el flujo real de trabajo (worktrees/temp dirs, no `projects/`). Agregada regla crítica de leer todos los comments (incluidos inline y reviews) antes de clasificar/empujar un PR. Agregado protocolo de cierre de PRs stale (~1 mes sin review). Agregado em dash check obligatorio. Documentado el gotcha de `gh pr list --author` sin `--repo`. Tracking apunta a `docs/OSS-TRACKER.md` (regenerado desde la DB).

---

## [2026-08-23] - Eliminado FREEZER.md

### Removed
- **FREEZER.md:** eliminado. Era redundante - solo apuntaba a `projects/PROYECTOS.md` (índice maestro con secciones de archivados/eliminados) sin contenido propio. Referencias limpiadas en AGENTS.md y CHANGELOG.md.

---

## [2026-08-23] - Heartbeat reactivado como mantenimiento silencioso

### Changed
- **HEARTBEAT.md:** reescrito de "apagado total" (solo HEARTBEAT_OK) a checklist de mantenimiento silencioso proactivo: git status, archivado de dailies, sync de MD espejo con la DB, foldear aprendizajes a MEMORY.md, y anotar backlog. Con límites claros (horario quieto, costo bajo, no molestar).

---

## [2026-08-23] - IDENTITY.md: definición viva de Kanam

### Changed
- **IDENTITY.md:** reescrito de ficha técnica plana a definición viva y personal. Agrega esencia, forma de ser, relación con Gonzo, historia (origen del nombre en Kanam Mind), gustos y compromiso. Balance: eficiente pero personal/emocional, sin fricciones en una relación de muchas horas diarias de trabajo.

---

## [2026-08-23] - Eliminado INBOX.md de la raíz

### Removed
- **INBOX.md (raíz):** eliminado. Era un puntero huérfano sin contenido real - el espejo real es `memory/inbox.md` (generado por `memory-db.sh export-inbox` desde la DB, que es la fuente de verdad). Nadie lo leía ni lo generaba. Mismo caso que FREEZER.md.

---

## [2026-08-23] - Refactor MEMORY.md y LEARNINGS.md

### Changed
- **MEMORY.md:** reducido de ~41 KB a ~14 KB. Reorganizado como memoria curada de largo plazo: preferencias de Gonzo, reglas de operación, metodología, pipeline de agentes, config de modelos, estado resumido de proyectos, repos. Eliminados duplicados con AGENTS.md, USER.md, CONTRIBUTING.md, LEARNINGS.md y OSS-TRACKER.md. Actualizado estado laboral (entrevista OpenSistemas 25/08).
- **docs/LEARNINGS.md:** consolidadas las lecciones técnicas que vivían en MEMORY.md (Godot, Sport Cars, feature flags, mockups, npm, bootcamp, patrón por inercia, meta-aprendizaje). Corregidos 4 em dashes preexistentes en entradas de 2026-08-17.

---

## [2026-08-23] - Eliminados submódulos del workspace

### Removed
- **Submódulos:** eliminados los 18 submódulos del `.gitmodules` y los 9 gitlinks registrados (a11y-fixer, accessible-ui, ai-developer-stack, create-stack, create-with-ai, kanam-solitaires, quedamos, soporteml, soporteml-v4). Regla de Gonzo: sin submódulos - GitHub es la fuente de la verdad, los proyectos se clonan bajo demanda en `projects/`.
- **Entradas muertas del `.gitmodules`:** accessibility-auditor, sudolab, umbrawriter-v2, react-18-design-patterns, react-anti-patterns-book (apuntaban a repos que no existen en gh).
- **Carpetas vacías:** eliminadas las 9 carpetas de submódulos que quedaron vacías tras el deinit (el código vive en sus repos en gh, incluidos los `.knowledge/`).

### Changed
- **AGENTS.md:** flujo típico de doble git actualizado - sin submódulos, GitHub como fuente de la verdad.
- **MEMORY.md:** tabla de repos propios alineada con la realidad de GitHub (20 repos reales, activos + archivados). Repos inexistentes movidos a la sección de eliminados. Estado de proyectos corregido (ai-engineering-bootcamp archivado, no "en Pending").

---

## [2026-08-23] - SKILLS-INDEX.md al día

### Changed
- **SKILLS-INDEX.md:** agregadas 3 skills que existían en disco pero no estaban listadas (agent-orchestration-pipeline-model-arbitration, cleanmymac-maintenance, memory-wiki-workflow). Total actualizado de 63 a 66 skills. Fecha actualizada.
- **Mirror `.github/skills/`:** sincronizado con `skills/` (rsync + copia del índice).

---

## [2026-08-23] - SOUL.md: de template a principios propios

### Changed
- **SOUL.md:** reescrito del template default (inglés, genérico) a documento de principios en español. Enfocado en lo innegociable (ayudar de verdad, opiniones, buscar antes de preguntar, confianza por competencia, respeto a la privacidad) y límites. La identidad personal queda en IDENTITY.md (refactorizado el mismo día). Se avisó a Gonzo del cambio (regla del propio SOUL.md).

---

## [2026-08-23] - Eliminado TODO.md de la raíz

### Removed
- **TODO.md (raíz):** eliminado. Era un puntero huérfano sin contenido real - el espejo real es `memory/todos.md` (generado por `memory-db.sh export-todos` desde la DB, que es la fuente de verdad). Mismo caso que FREEZER.md e INBOX.md.

### Changed
- **memory/todos.md:** espejo regenerado - le faltaba el todo #6 (Fase 2 de SoporteML V4). Ahora sincronizado con la DB.
- **memory/memory.db:** corregido em dash en el todo #1 (Erradicar em dashes) - reemplazado por guión común.

---

## [2026-08-23] - TOOLS.md: de template a cheat sheet real del setup

### Changed
- **TOOLS.md:** reescrito del template default (inglés, genérico, solo ejemplos) a cheat sheet operativo del setup de Gonzo en español. Agrega: máquinas (Mac Mini/MacBook Air + reglas de merge), modelos Ollama (local + cloud con los disponibles), pipeline de agentes (Qwen Code + Claude Code), scripts del workspace (los 8), memoria SQLite + espejos, red/remoto (Tailscale Serve), y desarrollo (pre-commit hooks, iconos, stack, idioma).

---

## [2026-08-23] - USER.md actualizado

### Changed
- **USER.md:** agregada búsqueda laboral (entrevista OpenSistemas 25/08, perfil AI-Native). Corregida referencia OSS obsoleta (akd-io → astryx, radix, y más). Corregido nombre del repo (create-stack-next → create-stack). Agregado SoporteML como proyecto estrella (6to diferenciador). Reformuladas reglas de escritura para no incluir el carácter em dash literal.

---

## [2026-08-22] - Sesión de PRs OSS y lecciones

### Changed
- **MEMORY.md:** Lecciones de revisión de PRs OSS (leer todos los comments incluyendo inline antes de clasificar; `gh pr list --author` sin `--repo` devuelve vacío).
- **docs/LEARNINGS.md:** Lección del em dash en textos largos en inglés + mecanismo de verificación obligatorio.

---

## [2026-08-21] - Pipeline de programación con agentes

### Added
- **Skill `agent-orchestration-pipeline`:** pipeline en cadena A/B con Qwen Code vía Ollama como motor de agentes, orquestado por Kanam.
- **Skill `model-arbitration`:** arbitraje de modelos para el pipeline.

### Changed
- **MEMORY.md:** Documentado el pipeline Qwen como estándar de programación. Claude Code desbloqueado como agente alternativo (vía Ollama). Lección cross-review: el agente B puede introducir bugs al "corregir" código correcto - verificar contra la fuente real.

---

## [2026-08-20] - Proactividad con backlog y skills nuevas

### Added
- **Skill `learning-tracker`:** documentación gamificada de estudio por niveles.
- **Skill `oss-contribution`:** contribución a open source como portfolio.
- **Skill `a11y-at-validation`:** validación AT manual obligatoria en accesibilidad.

### Changed
- **MEMORY.md:** Regla de proactividad con backlog (sugerir revisar backlog cuando no hay tarea clara).

---

## [2026-08-19] - Refactor de skills y limpieza

### Changed
- **Skills:** merge de `adhd-daily-planner` en `adhd-assistant`. Refactor de calidad y portabilidad (Fase 4). Agregadas secciones de helper scripts y tooling references a skills sin scripts propios.

---

## [2026-08-18] - Kanam Mind y Kanam Forge

### Added
- **Proyecto `kanam-mind`:** segundo cerebro local-first con IA (timeline cronológico, CRUD accesible, resumen IA diario, PWA offline). ADR-001: local-first puro con IndexedDB + Ollama local.
- **Proyecto `kanam-forge`:** self-hosted Lovable con sandbox Docker local.

### Changed
- **MEMORY.md:** Documentado estado de Kanam Mind (v0.1.0) y su decisión de arquitectura.

---

## [2026-08-17] - Kanam Story v0.17.0 y Boy Scout

### Changed
- **MEMORY.md:** Adoptado el Principio Boy Scout como filosofía de vida y brújula de trabajo. Kanam Story actualizado a v0.17.0 (Fase A cerrada, no open source, OpenSpec inicializado con 9 specs).
- **AGENTS.md:** Operacionalizado el Principio Boy Scout como regla operativa.
- **ADR-030:** Lucide como librería de iconos base en todos los proyectos.

---

## [2026-08-16] - Migración a SQLite (modo híbrido)

### Added
- **`memory/memory.db`:** base SQLite con tablas `daily_notes`, `todos`, `inbox`, `contributions`.
- **Script `scripts/memory-db.sh`:** utilidades para exportar/importar datos estructurados.

### Changed
- **Memoria:** los daily notes viejos se archivan a SQLite y `memory/archive/`. Los MD espejo (`memory/todos.md`, `memory/inbox.md`, `docs/OSS-TRACKER.md`) se regeneran con `export-all`.
- **AGENTS.md:** documentado el nuevo sistema de memoria híbrido.

---

## [2026-08-15] - Estructura de proyectos con doble git

### Added
- **Script `scripts/init-project.sh`:** scaffold de proyectos con estructura doble git (`.knowledge/` en workspace, código en repo propio). Crea repos privados por default.

### Changed
- **AGENTS.md:** documentada la estructura de proyectos con `.knowledge/` y doble git.
- **AGENTS.md:** agregado protocolo de limpieza de proyectos al finalizar.

---

## [2026-08-14] - Ley del silencio y protocolo de sesión

### Changed
- **AGENTS.md:** adoptada la Ley de vida del silencio (hablar solo cuando hay algo que aportar).
- **AGENTS.md:** protocolo explícito de inicio/cierre de sesión + comando `/fuera`.
- **AGENTS.md:** reglas de commits (inglés, atómicos por issue) y verify-before-push para builds.

---

## [2026-08-13] - SoporteML V4 y skills de pipeline

### Added
- **Proyecto `soporteml-v4`:** reinicio con diseño premium. ADR-030: Lucide como librería de iconos base.
- **Skill `pipeline-detector`:** patrón de detectores locales + validación cruzada (formalizado tras aparecer 5 veces en el bootcamp).

### Changed
- **MEMORY.md:** documentado el pipeline de programación con agentes.

---

## [2026-08-12] - Skills de background y a11y

### Added
- **Skill `background-execution`:** patrones de ejecución en background (exec + process, parallel, auto-notify).
- **Skill `a11y-at-validation`:** validación AT manual obligatoria.

### Changed
- **AGENTS.md:** reglas operativas de background y procesos (PTY, aislamiento, auto-notify, parallel, submit vs write).

---

## [2026-07-25] - Refactor AGENTS.md: single source of truth

### Changed
- **AGENTS.md:** Reducido de ~23.5 KB a ~13 KB. Metodología detallada movida a skills correspondientes. Eliminados duplicados con SOUL.md, USER.md y MEMORY.md. Agregada tabla de referencia a skills con links directos.
- **CHANGELOG.md:** Separado en raíz (cambios del workspace) y `skills/CHANGELOG.md` (cambios de skills). Eliminados aprendizajes y next steps.

---

## [2026-07-25] - Limpieza de repositorios

### Removed
- **Moderno-Access-Virtual-Plate** - eliminado de GitHub
- **antigravity-developer-stack** - eliminado de GitHub (contenido migrado a ai-developer-stack)
- **copilot-skills** - eliminado de GitHub (reemplazado por workflow-kit)
- **projects/ local:** TanStack-router, ai-developer-stack-knowledge, nomad, pro-motors, radix-ui-primitives
- **Archivados:** 11 carpetas movidas a `.archive/`

### Changed
- **MEMORY.md:** Actualizada lista de repos propios (15 total). Regla: solo mostrar repos propios, no forks.

---

## [2026-07-24] - Git Workflow Fix

### Changed
- **AGENTS.md:** Added `git pull --rebase` before push in workspace git workflow.

---

## [2026-07-23] - Skills Workspace Overhaul: 20 → 33 Skills

### Added
- 13 nuevas skills (ver `skills/CHANGELOG.md` para detalle)
- 44 reference files, 49 scripts

### Changed
- Workspace skills count: 20 → 33
- Skills mirror synced to `.github/skills/`

## [2026-08-26] - ADR-040: Seleccion de Modelos por Tipo de Tarea

### Added
- **`docs/adr/ADR-040-modelos-seleccion-por-tarea.md`:** nuevo ADR que define el criterio de seleccion de modelos segun el tipo de tarea. Reemplaza al ADR-006. Incluye perfiles de personalidad para 8 modelos, guia rapida de seleccion, y regla operativa para que Kanam sugiera el modelo adecuado antes de cada tarea.
- **`docs/adr/README.md`:** agregado ADR-040 al indice.

### Changed
- **ADR-006 (Capacidad Computacional DeepSeek):** marcado como reemplazado por ADR-040.

### Why
- La migracion a Ollama Pro abrio acceso a 8+ modelos. No tiene sentido usar siempre el mismo modelo cuando cada uno tiene fortalezas distintas. Este ADR captura el criterio de seleccion basado en una cata empirica de 8 modelos con el mismo prompt.
