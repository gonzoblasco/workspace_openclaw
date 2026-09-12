# TODO.md - Backlog de Tareas

> Generado desde memory/memory.db (tabla todos). Fuente de verdad: la DB.
> Regenerar con: ./scripts/memory-db.sh export-todos

## Abiertos

- [ ] **[kanam-skills]** (medium) Dominio propio para kanam-skills
- [ ] **[kanam-skills]** (medium) Post de LinkedIn como portfolio
- [ ] **[kanam-skills]** (medium) Mejorar el preview de la skill page (ahora es pre con markdown crudo)
- [ ] **[a11y-fixer]** (medium) a11y-fixer: redefinir proyecto, agregar features
- [ ] **[]** (medium) Definir alcance de Fase 2 de SoporteML V4 (bandeja operativa: estado de preguntas, IA on-demand, publicar a MeLi, autopilot). Propuesta en artifact 9c009492-a0be-4815-af4b-1a2d8e602eca. Lunes.
- [ ] **[]** (medium) Crear carpeta sandbox/ para pruebas temporales (plugins, experimentos aislados) - no commitear al repo
- [ ] **[]** (medium) Analizar plugin github-workflow (chris-openclaw) en sandbox: estudiar approach de risk signals y agrupacion de PRs para optimizar pr-dashboard.sh y ritual de inicio
- [ ] **[]** (medium) OBSERVAR (de ClawHub models): memoria grafica / knowledge graph (Memory Graph, Graph Memory) - relaciones entre conceptos, futuro upgrade de QMD
- [ ] **[]** (medium) OBSERVAR (de ClawHub web): Deep Research multi-paso, Tavily Extract (paginas a markdown), Apify/scraping para sitios especificos
- [ ] **[]** (medium) OBSERVAR (de ClawHub tools): MCP Client/MCPBundles (acceso MCP estandar), Agent Collaboration OS / A2A / cross-agent orchestration
- [ ] **[]** (medium) OBSERVAR (de ClawHub runtime): observabilidad del agente con OpenTelemetry/Prometheus/Langfuse/Otel - metricas del pipeline (runtime, latencia, errores, SIGKILL) a futuro
- [ ] **[Deprecate del paquete npm 0.0.2 (288 descargas) que quedo publicado tras la fusion a kanam-forge. Requiere token npm valido (el de ~/.npmrc expiro, 401). Comando listo: npm deprecate @gonzoblasco/create-with-ai@0.0.2 'Fusionado a kanam-forge. Usa kanam-forge en su lugar.' Deprecar NO borra el paquete - lo marca como desaconsejado.]** (medium) Deprecar @gonzoblasco/create-with-ai en npm (no borrar)
- [ ] **[]** (medium) Pipeline A/B: Alternar Agente A y Agente B con glm-5.3-flash:cloud (motor actual desde 2026-08-29), via Qwen Code en Ollama
- [ ] **[workspace]** (medium) Validar GLM 5.3 Flash en tareas reales del pipeline A/B (escribir codigo, tests, PRs - no solo diseno de arquitectura). Ver ADR-041 pendiente 2
- [ ] **[workspace]** (medium) Probar input visual de GLM 5.3 Flash en caso real (mockup/screenshot -> UI o screenshot de error -> fix). Ver ADR-041 pendiente 3
- [ ] **[workspace]** (medium) Re-cata de modelos LLM ~2026-09-29: revisar novedades (GLM, Kimi, alternativas) y decidir si mantener el trio actual. Ver ADR-041 pendiente 4
- [ ] **[kanam-pulse]** (medium) Kickoff M1 kanam-pulse: extraer engine de system-health-check a packages/core (TS), 46 tests verdes, dashboard read-only
- [ ] **[kanam-pulse]** (medium) Traer codigo system-health-check desde MacBook Air (no tiene repo GitHub; el dir local solo tiene .knowledge/)
- [ ] **[]** (medium) Explorar Kanam Studio: Engine de Narrativa No Lineal y World-building con consistencia IA
- [ ] **[kanam-pulse]** (medium) kanam-pulse: evaluar envoltorio nativo a futuro (Electron/Tauri/React Native/nativa) SOLO despues de que la web v1 este completa y pulida. No bloquea nada hoy - es decision de distribucion futura. Nota: Tauri es candidata natural si algun dia se hace (mas liviana que Electron, binario unico)
- [ ] **[]** (medium) Clonar gonzoblasco/soporteml en projects/soporteml (GitHub es la fuente) y mudar ahi el puente Lovable MCP: hoy quedo ignorado por el gitignore del workspace. Respaldar .knowledge/ antes.
- [ ] **[]** (medium) Reparar scripts spin-review del 2026-08-30 o quarantinarlos en scripts/wip/: bugs listados en memory/HANDOFF-2026-08-30-soporteml-v1-lovable-mcp.md (jq, BSD date, overwrite de HANDOFF, em-dash check, require-in-ESM)
- [ ] **[]** (medium) Definir cliente MCP real para Lovable en OpenClaw (https://mcp.lovable.dev, OAuth): evaluar integracion nativa, SDK @modelcontextprotocol o via Claude Code. Contrato read-only: get_project, list_projects, query_database
- [ ] **[Definir roadmap de slices de Kanam Studio (grafo -> jugar -> IA de ramas -> canon checker -> export). Brief listo en projects/kanam-studio/.knowledge/BRIEF.md]** (medium) kanam-studio
- [ ] **[World-building con IA en Kanam Studio: personajes, mundo, reglas construidos y mantenidos con IA durante todo el viaje (no capa final). Version superada de kanam-story. Brief: projects/kanam-studio/.knowledge/BRIEF.md]** (medium) kanam-studio
- [ ] **[]** (medium) Verificar .env de soporteml (repo público trackea .env en HEAD, desapareció del disco - decidir si restaurar con secrets históricos o eliminarlo del historial)
- [ ] **[]** (medium) Desarchivar create-with-ai (archivado, fusionado en kanam-forge) para pushear commit local legítimo - decisión de Gonzo
- [ ] **[]** (medium) Fix memory-catalog-v2.py: IndexError en categorize_learning (compute_category_centroids, list index out of range) al correr el catalog tras guardar sesion 2026-09-06. No bloqueo el guardado (DB-first OK) pero las embeddings/semantic search quedan sin re-catalogar.
- [ ] **[workspace]** (medium) Activar gateway de OpenClaw en el Mac Mini como servidor fijo 24/7 del bot Telegram (@kanam_ai_bot). Hoy el canal esta configurado en la MacBook Air (2026-09-07). Al moverlo: deshabilitar el canal Telegram en la Air para evitar conflicto de long polling (error 409).
- [ ] **[workspace]** (medium) Actualizar skill model-cata para cubrir tests de CODIGO ejecutables (extraer bloque de codigo de la respuesta, correr suite oculta con node, pass/fail objetivo). Agregar: escalera L1-L5 (funcion pura, bordes ocultos, algoritmo O(1), DP con reconstruccion, parser desde cero), validacion obligatoria del test del test contra soluciones de referencia ANTES de medir, medicion de overhead fijo (cold start ~4s en v4.1) separado del throughput, y caveat de replicas. Nace de la cata v4-flash vs v4.1-flash del 2026-09-11.

## Completados

- [x] **[workspace]** CERRADO 2026-09-11. El .knowledge/BRIEF.md de kanam-tetris YA esta respaldado en el workspace (commit 4c8d6e8, archivo plano 100644, 121 lineas, verificado en origin/main). CAUSA RAIZ (verificada con experimento controlado, distinta a la asumida): NO es el triple-git ni la regla del .gitignore, es el .git ANIDADO. Git no puede indexar contenido de un dir que ya es repo: 'git add -f' devuelve exit 0 y NO stagea nada. kanam-tetris era el UNICO de los 14 proyectos asi. SOLUCION aplicada (workaround de docs/learnings/proyectos.md, verificado con el patron exacto): mover el .git temporalmente, force-add, restaurar. Una vez trackeado, un add -A normal lo actualiza sin -f. HALLAZGO NUEVO: la regla blanket del .gitignore es LOAD-BEARING - sin ella un add -A stagea el repo anidado como gitlink 160000 (lo que rompio el workspace). Se conservo y se corrigio el comentario, que afirmaba falsamente que el knowledge no se trackea. SIMULADO maquina B (clone del workspace + repo del proyecto en el mismo slug): pull = fast-forward limpio, BRIEF actualizado, repo anidado intacto. NADA publicado al repo publico del proyecto (decision de Gonzo si algun dia quiere ese camino).
- [x] **[workspace]** Decidir kanam-tetris: repo local listo (2 commits, sin push) pero el .git anidado bloquea el triple-git del workspace (git no trackea .knowledge con repo embebido). Opciones: (1) pushear a GitHub (kanam-tetris) cuando Gonzo lo decida, o (2) archivar como los demas (quitar .git local, trackear solo .knowledge). Mientras tanto .knowledge/BRIEF.md no viaja entre maquinas.
- [x] **[]** PORTAR (de ClawHub runtime): Task Notifier - notificacion desktop cuando un agente termina tarea (ya visto tambien en security), util para pipeline A/B
- [x] **[]** PORTAR (de ClawHub tools, Pipeline Architect) CANDIDATO FUERTE: estado durable + crash recovery + lifecycle para el pipeline A/B - que el plan de unidades sobreviva a SIGKILL/restarts con taskflow-like (list/get/resume), directo a nuestro problema de Qwen muriendo
- [x] **[]** PORTAR (de ClawHub web, Search Fusion): skill de busqueda federada - elegir provider/estrategia por intencion (research/keyword/coding) + dedupe de resultados. A nuestro modo con DuckDuckGo key-free + web_fetch + browser
- [x] **[]** PORTAR (de ClawHub media): skill de manejo de PDF/OCR local - extraer texto de PDFs, OCR de imagenes escaneadas, convertir formatos. Util para specs, documentos, recibos (familia PDF Extract/OCR/Convert del clawhub)
- [x] **[]** PORTAR (de ClawHub context, Session Compact): estructurar la compactacion con resumen tipo Scope/Recent requests/Pending work/Key files/Timeline en lugar de resumen generico
- [x] **[]** PORTAR (de ClawHub context) CANDIDATO FUERTE: compaction domain-aware con tiers 0-4 - skill que preserve arquitectura/ADRs/API contracts/seguridad al compactar sesiones de software (sesion-lifecycle + knowledge-management)
- [x] **[]** PORTAR (de ClawHub models, ToggleLogic sin licencia): rutas de modelo por tipo de tarea + overrides sticky + audit de decision de modelo en pipeline A/B
- [x] **[]** PORTAR (de ClawHub models) CANDIDATO #1: skill-ai-inject - auto-match de tareas con las 59 skills (cascada keyword L1 gratis -> embedding L2, Ollama-only con bge-m3/nomic). Resolver el problema de saber cual skill aplicar por tarea. Ver skill-router propio
- [x] **[]** PORTAR (de ClawHub channels): skill de URL pre-flight check local antes de web_fetch - esquema https + blocklist + typosquatting + payload injection (idea de PreClick, sin mandar URLs a terceros)
- [x] **[]** PORTAR (de ClawHub channels): flush de memoria antes de compactacion /new + limpiar metadata de conversacion al persistir (idea de Honcho)
- [x] **[]** PORTAR (de ClawHub channels): filtro de ruido en pipeline de memoria - no persistir HEARTBEAT_OK/cron/queued headers a memory.db/dailies (idea de Honcho Memory)
- [x] **[]** Analisis ClawHub por secciones (con Gonzo): gateway y security analizadas, github-workflow portado a github-pr-risk.sh. Seccion 'other' = low yield (providers redundantes con Ollama, canales no usados). Pendientes: secciones restantes para portar ideas a plugins/skills propios
- [x] **[oss]** Mejorar el OSS-TRACKER
- [x] **[workspace]** Erradicar em dashes (-) de TODO el workspace

