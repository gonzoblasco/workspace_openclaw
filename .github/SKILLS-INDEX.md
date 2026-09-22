# SKILLS-INDEX.md - Skills del Workspace

> Skills activas organizadas por categoría. Actualizado: 2026-09-03
>
> **Nota de consolidación:** En agosto 2026 se redujo el set de skills de 96 a 60 activas, adoptando las 24 skills de ingeniería de `addyosmani/agent-skills` como base y fusionando en ellas las funcionalidades de skills propias redundantes. Las skills redundantes fueron eliminadas (recuperables desde el historial de git, commit `ba12459`).
>
> **Actualización 2026-08-17:** alineado con el estado real (63 skills). Se documentaron `a11y-at-validation` y `technical-book-processor` (existentes pero no listadas). Se movieron los checklists sueltos de `skills/references/` a `docs/checklists/` y se eliminaron los directorios zombies `architecture-designer` y `pre-deploy-qa` (vacíos).
>
> **Actualización 2026-09-03:** alineado con el estado real (81 skills). Se documentaron 15 skills existentes pero no listadas: `anti-ai`, `compaction-domain-aware`, `complexity-driven-pipeline`, `gateway-config`, `gateway-restart-helper`, `health-check-dashboard`, `model-cata`, `model-router-pro`, `openspec-pattern`, `pdf-tool`, `project-closure`, `search-fusion`, `skill-collection-maintenance`, `skill-router`, `study-tracker`.

## Ingeniería de Desarrollo (Base Addy Osmani + Fusiones)

> 24 skills de `addyosmani/agent-skills` cubren el ciclo completo Define → Plan → Build → Verify → Review → Ship. 5 de ellas fueron **fusionadas** con funcionalidades de skills propias de Kanam (marcadas ⭐).

### Define
| Skill | Descripción |
|---|---|
| [interview-me](skills/interview-me/) | Interrogatorio de 1 pregunta por vez hasta 95% de claridad del requerimiento real |
| [idea-refine](skills/idea-refine/) | Pensamiento divergente/convergente para afinar ideas vagas en propuestas concretas |
| [spec-driven-development](skills/spec-driven-development/) ⭐ | PRD completo (objetivos, arquitectura, data model, UI, acceptance criteria, traceability) antes de código. Fusiona: build-scaffold (OpenSpec), anydocs, spec-miner |

### Plan
| Skill | Descripción |
|---|---|
| [planning-and-task-breakdown](skills/planning-and-task-breakdown/) ⭐ | Descompone specs en tareas atómicas verificables con dependency ordering, estimación de timeline y planificación de GitHub issues. Fusiona: timeline-builder, gh-issue-planner, brw-plan-my-day |

### Build
| Skill | Descripción |
|---|---|
| [incremental-implementation](skills/incremental-implementation/) | Slices verticales finos - implementar, testear, verificar, commitear |
| [test-driven-development](skills/test-driven-development/) | Red-Green-Refactor, test pyramid (80/15/5), DAMP, Beyonce Rule |
| [context-engineering](skills/context-engineering/) | Curación del contexto del agente: rules files, context packing, MCP |
| [source-driven-development](skills/source-driven-development/) | Cada decisión de framework respaldada por documentación oficial citada |
| [doubt-driven-development](skills/doubt-driven-development/) | Revisión adversarial en contexto fresco: CLAIM → EXTRACT → DOUBT → RECONCILE → STOP |
| [frontend-ui-engineering](skills/frontend-ui-engineering/) ⭐ | UI de producción: accesible (WCAG 2.1 AA), responsive, design system. Fusiona: accessibility-studio, ui-design, ui-generation, anti-slop-design, a11y-audit-agent, sovereign-accessibility-auditor |
| [api-and-interface-design](skills/api-and-interface-design/) | Contract-first, Hyrum's Law, One-Version Rule, error semantics, boundary validation |

### Verify
| Skill | Descripción |
|---|---|
| [browser-testing-with-devtools](skills/browser-testing-with-devtools/) | Chrome DevTools MCP: DOM, console, network, performance en vivo |

| [a11y-at-validation](skills/a11y-at-validation/) | Cuándo la validación manual de accesibilidad es OBLIGATORIA (no opcional) en OSS, y cómo ejecutarla y documentarla. Basado en casos reales (radix-ui #4109/#4110) |
| [debugging-and-error-recovery](skills/debugging-and-error-recovery/) ⭐ | Triage de 5 pasos: reproduce, localize, reduce, fix, guard + logging forense + failure patterns. Fusiona: debug-agent, debug-investigation, failure-memory |

### Review
| Skill | Descripción |
|---|---|
| [agent-orchestration-pipeline](skills/agent-orchestration-pipeline/) | Orquestar 2+ agentes implementadores con cross-review multi-ronda: divide en unidades, asigna paridad A/B, coordina cierre. Validado en kanam-story Fase 3 |
| [code-review-and-quality](skills/code-review-and-quality/) ⭐ | Review de 5 ejes, severity labels, change sizing, mentorship feedback. Fusiona: anti-pattern-czar, code-review-agent, code-mentor, review-quality |
| [code-simplification](skills/code-simplification/) | Chesterton's Fence, Rule of 500, reduce complejidad preservando comportamiento |
| [security-and-hardening](skills/security-and-hardening/) | OWASP Top 10, auth patterns, secrets management, boundary system |
| [performance-optimization](skills/performance-optimization/) | Measure-first, Core Web Vitals, profiling, bundle analysis |

### Ship
| Skill | Descripción |
|---|---|
| [git-workflow-and-versioning](skills/git-workflow-and-versioning/) | Trunk-based, atomic commits, change sizing, commit-as-save-point |
| [ci-cd-and-automation](skills/ci-cd-and-automation/) | Shift Left, Faster is Safer, feature flags, quality gate pipelines |
| [deprecation-and-migration](skills/deprecation-and-migration/) | Code-as-liability, compulsory vs advisory deprecation, zombie code |
| [documentation-and-adrs](skills/documentation-and-adrs/) | ADRs, API docs, inline docs - documentar el *why* |
| [observability-and-instrumentation](skills/observability-and-instrumentation/) | Structured logging, RED metrics, OpenTelemetry, symptom-based alerting |
| [shipping-and-launch](skills/shipping-and-launch/) | Pre-launch checklists, feature flag lifecycle, staged rollouts, rollback |
| [project-closure](skills/project-closure/) | Cierre completo de proyecto: captura decisión, aprendizaje y estado en ADR + DB + skill. Reproducible con script |

### Meta
| Skill | Descripción |
|---|---|
| [using-agent-skills](skills/using-agent-skills/) | Mapea el trabajo entrante a la skill correcta y define reglas de operación compartidas |
| [agent-orchestration-pipeline-model-arbitration](skills/agent-orchestration-pipeline-model-arbitration/) | Arbitraje de modelo para pipeline A/B: reducir costos priorizando Kimi K2.7 Code solo cuando se justifica |
| [skill-router](skills/skill-router/) | Sugiere qué skill usar para una tarea dada: matchea el prompt contra las skills disponibles (keywords + embeddings semántico local) y devuelve top sugerencias |
| [skill-collection-maintenance](skills/skill-collection-maintenance/) | Mantenimiento de la colección de skills: diagnostica el cron semanal `skill-collection-review` fallando por tamaño y elimina skills limpiamente |
| [complexity-driven-pipeline](skills/complexity-driven-pipeline/) | Orquestación complexity-first: scorer de complejidad antes de spawnear agentes A/B. Decide modelo, thinking level y profundidad de pipeline |
| [model-cata](skills/model-cata/) | Ritual formal de comparación de modelos LLM: mismo prompt pesado, rúbrica de análisis crítico y decisión de motor/especialistas documentada en ADR |

## Core OpenClaw (Infraestructura Propia)

| Skill | Descripción |
|---|---|
| [session-lifecycle](skills/session-lifecycle/) | Ciclo de sesión completo: inicio, cierre, WAL protocol, handoff, ADHD productivity |
| [knowledge-management](skills/knowledge-management/) | Gobernanza de conocimiento, learning signals, conflict resolution, DREAMS |
| [memory-agent](skills/memory-agent/) | Memory Agent autónomo: consolida memoria, detecta patrones, mantiene knowledge |
| [openspec](skills/openspec/) | CLI de OpenSpec para spec-driven development |
| [memory-wiki-workflow](skills/memory-wiki-workflow/) | Flujo para usar memory-wiki como capa analítica de memoria: entities con claims, dashboards, síntesis y visualización markdown |
| [background-execution](skills/background-execution/) | Patrones para ejecutar tareas en background: exec + process, worktrees |
| [engineering-governance](skills/engineering-governance/) | Evolución continua del AI Engineering OS, auditoría y mejora sistémica |
| [git-changelog](skills/git-changelog/) | Auto-genera CHANGELOG.md desde git history con conventional commits |
| [openspec-pattern](skills/openspec-pattern/) | Contrato de intención (OpenSpec) para prevenir scope creep y deuda técnica: define el *what* antes del *how* |
| [compaction-domain-aware](skills/compaction-domain-aware/) | Compactación de contexto con conciencia de dominio: tiers de prioridad (Tier 0-4) para decidir qué preservar al compactar una sesión |
| [gateway-config](skills/gateway-config/) | Gestión de configuración del gateway OpenClaw en runtime: edición, health checks y tracking de cambios sin reinicios |
| [gateway-restart-helper](skills/gateway-restart-helper/) | Reinicio automático del gateway con health checks previos/posteriores y rollback seguro |
| [health-check-dashboard](skills/health-check-dashboard/) | Dashboard de monitoreo del gateway en tiempo real: memoria, CPU, conexiones activas, latencia, alertas por umbrales |
| [model-router-pro](skills/model-router-pro/) | Routing inteligente de modelos con fallback y balanceo entre instancias locales (Ollama) y cloud |

## Stack de Gonzo (Infraestructura Única)

| Skill | Descripción |
|---|---|
| [workspace-portfolio-hygiene](skills/workspace-portfolio-hygiene/) | Audita/limpia/estructura projects/*: clasifica gitlinks vs blobs, respeta decisiones de ADR, archiva repos, promueve carpetas a doble git |
| [supabase-assistant](skills/supabase-assistant/) | Interact with Supabase projects: schemas, queries, types, migrations |
| [sql-insight](skills/sql-insight/) | Traducir lenguaje natural a SQL, optimizar queries, interpretar EXPLAIN |

| [mcp-orchestrator](skills/mcp-orchestrator/) | Orquestación de MCP servers |

## Especializadas

| Skill | Descripción |
|---|---|
| [i18n-expert](skills/i18n-expert/) | Internacionalización/localización: setup, auditoría, reemplazo de strings, paridad de locales |

| [support-response-writer](skills/support-response-writer/) | Respuestas profesionales de customer support |
| [deepwiki](skills/deepwiki/) | Consulta documentación de repos GitHub via DeepWiki MCP |
| [tech-docs](skills/tech-docs/) | Documentación técnica: ADRs, README, API docs, CHANGELOG, guías |
| [oss-contribution](skills/oss-contribution/) | Workflow de contribución OSS: triaje, seguimiento de issues/PRs, community, registry |
| [search-fusion](skills/search-fusion/) | Búsqueda efectiva por intención: elige estrategia y herramientas según el tipo de búsqueda (research, keyword, answer, news) y fusiona fuentes |

## Seguridad y Red

| Skill | Descripción |
|---|---|
| [clawdstrike](skills/clawdstrike/) | Security audit del gateway OpenClaw |


## Carrera y Crecimiento

| Skill | Descripción |
|---|---|
| [mock-interview-drill](skills/mock-interview-drill/) | Simulacros de entrevistas: Behavioral (STAR), Technical, Case con diagnóstico |
| [cv-tailor](skills/cv-tailor/) | Optimizar CVs: matching de keywords, reescritura STAR con datos cuantitativos |

## Contenido y Creatividad

| Skill | Descripción |
|---|---|
| [copy-editing](skills/copy-editing/) | Edición profesional de copy: 7 sweeps de claridad, tono, beneficio |
| [brand-name-forge](skills/brand-name-forge/) | Workshop sistemático de naming de marca: 8 métodos clásicos |
| [content-serializer](skills/content-serializer/) | Convertir contenido en posts multi-plataforma para LinkedIn y X |
| [deslop](skills/deslop/) | Limpia código AI slop de branches antes de PRs |
| [image-generation](skills/image-generation/) | Genera imágenes para juegos, web, mockups y proyectos creativos |
| [curriculum-builder](skills/curriculum-builder/) | Scaffold para tutores adaptativos con IA |
| [technical-book-processor](skills/technical-book-processor/) | Procesa libros técnicos capítulo por capítulo: extrae learnings, formaliza ADRs, implementa ejercicios en un proyecto acompañante y commitea atómicamente. Deja trail público de aprendizaje (portfolio) |
| [anti-ai](skills/anti-ai/) | Elimina modismos y estructuras que delatan texto de IA para que suene humano. Incluye la regla del guion común. Usar antes de publicar posts, feedback o PRs |

## Vida Diaria y Herramientas

| Skill | Descripción |
|---|---|
| [adhd-assistant](skills/adhd-assistant/) | Gestión de vida diaria para ADHD: planificación, desglose de tareas, energy windows, transition buffers, dopamine sequencing, shutdown ritual. Fusiona: adhd-daily-planner |
| [adhd-output](skills/adhd-output/) | Formato de respuesta ADHD-friendly: acción primero, pasos numerados, next step concreto, sin preámbulo ni cierres. Adaptado de ayghri/i-have-adhd (MIT) |
| [apple-photos](skills/apple-photos/) | Acceso terminal a Photos.app: buscar, listar, exportar |
| [calorie-counter](skills/calorie-counter/) | Tracking diario de calorías y proteína en SQLite local |
| [mlx-stt](skills/mlx-stt/) | Speech-to-text local en Apple Silicon con MLX |
| [checkmate](skills/checkmate/) | Goal-to-execution-to-verification loop con worker + judge |
| [github](skills/github/) | Official GitHub MCP server wrapper: security alerts, notifications |
| [godot-mcp](skills/godot-mcp/) | Aprender Godot 4.x paso a paso con asistencia de OpenClaw |
| [cleanmymac-maintenance](skills/cleanmymac-maintenance/) | Protocolo flexible de mantenimiento con CleanMyMac CLI vía frases naturales |
| [study-tracker](skills/study-tracker/) | Estructura de cursos + gamificación (niveles/XP/badges) en una sola fuente de verdad bajo `studies/<slug>/` |
| [pdf-tool](skills/pdf-tool/) | Manejo local de PDFs: leer (texto, metadata, OCR) y generar (exportar markdown a PDF). 100% local (poppler + tesseract) |

---

## Skills Eliminadas

58 skills redundantes fueron eliminadas en la consolidación (commit `ba12459`). Su funcionalidad fue absorbida por las fusiones. **Recuperables desde el historial de git** si alguna capacidad específica llegara a faltar.

**Además (2026-08-06):** `adhd-daily-planner` se fusionó dentro de `adhd-assistant` (energy windows, transition buffers, dopamine sequencing, shutdown ritual, recovery protocol). Recuperable desde git si hiciera falta.

**Totales activas:** 82 skills
