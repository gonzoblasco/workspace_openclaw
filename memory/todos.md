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

## Completados

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

