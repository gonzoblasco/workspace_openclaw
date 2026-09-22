# SKILLS-INDEX.md - Skills del Workspace

> Skills activas organizadas por categoría. Actualizado: 2026-09-22
>
> **Nota de consolidación:** En agosto 2026 se redujo el set de skills de 96 a 60 activas, adoptando las 24 skills de ingeniería de `addyosmani/agent-skills` como base y fusionando en ellas las funcionalidades de skills propias redundantes. Las skills redundantes fueron eliminadas (recuperables desde el historial de git, commit `ba12459`).
>
> **Actualización 2026-08-17:** alineado con el estado real (63 skills). Se documentaron `a11y-at-validation` y `technical-book-processor` (existentes pero no listadas). Se movieron los checklists sueltos de `skills/references/` a `docs/checklists/` y se eliminaron los directorios zombies `architecture-designer` y `pre-deploy-qa` (vacíos).
>
> **Actualización 2026-09-03:** alineado con el estado real (81 skills). Se documentaron 15 skills existentes pero no listadas: `anti-ai`, `compaction-domain-aware`, `complexity-driven-pipeline`, `gateway-config`, `gateway-restart-helper`, `health-check-dashboard`, `model-cata`, `model-router-pro`, `openspec-pattern`, `pdf-tool`, `project-closure`, `search-fusion`, `skill-collection-maintenance`, `skill-router`, `study-tracker`.
>
> **Actualización 2026-09-22:** sincronizado con el estado real tras la reestructuración de skills. **60 skills activas**, verificado contra `openclaw skills list --json` (fuente `openclaw-workspace`). Se removieron 24 entradas stale, se documentó `publish-skills` y se limpiaron 19 directorios vacíos de `skills/`. Ojo: 13 de las 24 stale existen todavía en `projects/kanam-skills/skills` (repo público), no en el workspace.

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

### Review
| Skill | Descripción |
|---|---|
| [agent-orchestration-pipeline](skills/agent-orchestration-pipeline/) | Orquestar 2+ agentes implementadores con cross-review multi-ronda: divide en unidades, asigna paridad A/B, coordina cierre. Validado en kanam-story Fase 3 |
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
| [agent-orchestration-pipeline-model-arbitration](skills/agent-orchestration-pipeline-model-arbitration/) | Arbitraje de modelo para pipeline A/B: reducir costos priorizando Kimi K2.7 Code solo cuando se justifica |
| [skill-router](skills/skill-router/) | Sugiere qué skill usar para una tarea dada: matchea el prompt contra las skills disponibles (keywords + embeddings semántico local) y devuelve top sugerencias |
| [skill-collection-maintenance](skills/skill-collection-maintenance/) | Mantenimiento de la colección de skills: diagnostica el cron semanal `skill-collection-review` fallando por tamaño y elimina skills limpiamente |
| [publish-skills](skills/publish-skills/) | Publica skills del workspace (privado) al repo publico como artefacto generado: sanitizacion en memoria, allowlist para altas y verificacion post-apply |
| [complexity-driven-pipeline](skills/complexity-driven-pipeline/) | Orquestación complexity-first: scorer de complejidad antes de spawnear agentes A/B. Decide modelo, thinking level y profundidad de pipeline |
| [model-cata](skills/model-cata/) | Ritual formal de comparación de modelos LLM: mismo prompt pesado, rúbrica de análisis crítico y decisión de motor/especialistas documentada en ADR |

## Core OpenClaw (Infraestructura Propia)

| Skill | Descripción |
|---|---|
| [session-lifecycle](skills/session-lifecycle/) | Ciclo de sesión completo: inicio, cierre, WAL protocol, handoff, ADHD productivity |
| [knowledge-management](skills/knowledge-management/) | Gobernanza de conocimiento, learning signals, conflict resolution, DREAMS |
| [openspec](skills/openspec/) | CLI de OpenSpec para spec-driven development |
| [memory-wiki-workflow](skills/memory-wiki-workflow/) | Flujo para usar memory-wiki como capa analítica de memoria: entities con claims, dashboards, síntesis y visualización markdown |
| [engram-project-memory](skills/engram-project-memory/) | Engram: memoria persistente de proyecto para agentes de pipeline (Qwen/Claude Code) vía MCP. Cuándo guardar, cuándo buscar, handoff y recovery pos-compaction (ADR-052) |
| [background-execution](skills/background-execution/) | Patrones para ejecutar tareas en background: exec + process, worktrees |
| [engineering-governance](skills/engineering-governance/) | Evolución continua del AI Engineering OS, auditoría y mejora sistémica |
| [git-changelog](skills/git-changelog/) | Auto-genera CHANGELOG.md desde git history con conventional commits |
| [openspec-pattern](skills/openspec-pattern/) | Contrato de intención (OpenSpec) para prevenir scope creep y deuda técnica: define el *what* antes del *how* |
| [compaction-domain-aware](skills/compaction-domain-aware/) | Compactación de contexto con conciencia de dominio: tiers de prioridad (Tier 0-4) para decidir qué preservar al compactar una sesión |
| [gateway-config](skills/gateway-config/) | Gestión de configuración del gateway OpenClaw en runtime: edición, health checks y tracking de cambios sin reinicios |

## Stack de Gonzo (Infraestructura Única)

| Skill | Descripción |
|---|---|
| [workspace-portfolio-hygiene](skills/workspace-portfolio-hygiene/) | Audita/limpia/estructura projects/*: clasifica gitlinks vs blobs, respeta decisiones de ADR, archiva repos, promueve carpetas a doble git |
| [supabase-assistant](skills/supabase-assistant/) | Interact with Supabase projects: schemas, queries, types, migrations |
| [sql-insight](skills/sql-insight/) | Traducir lenguaje natural a SQL, optimizar queries, interpretar EXPLAIN |

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
| [content-serializer](skills/content-serializer/) | Convertir contenido en posts multi-plataforma para LinkedIn y X |
| [deslop](skills/deslop/) | Limpia código AI slop de branches antes de PRs |
| [technical-book-processor](skills/technical-book-processor/) | Procesa libros técnicos capítulo por capítulo: extrae learnings, formaliza ADRs, implementa ejercicios en un proyecto acompañante y commitea atómicamente. Deja trail público de aprendizaje (portfolio) |

## Vida Diaria y Herramientas

| Skill | Descripción |
|---|---|
| [checkmate](skills/checkmate/) | Goal-to-execution-to-verification loop con worker + judge |
| [github](skills/github/) | Official GitHub MCP server wrapper: security alerts, notifications |
| [cleanmymac-maintenance](skills/cleanmymac-maintenance/) | Protocolo flexible de mantenimiento con CleanMyMac CLI vía frases naturales |
| [pdf-tool](skills/pdf-tool/) | Manejo local de PDFs: leer (texto, metadata, OCR) y generar (exportar markdown a PDF). 100% local (poppler + tesseract) |

---

## Skills Eliminadas

58 skills redundantes fueron eliminadas en la consolidación (commit `ba12459`). Su funcionalidad fue absorbida por las fusiones. **Recuperables desde el historial de git** si alguna capacidad específica llegara a faltar.

**Además (2026-08-06):** `adhd-daily-planner` se fusionó dentro de `adhd-assistant` (energy windows, transition buffers, dopamine sequencing, shutdown ritual, recovery protocol). Recuperable desde git si hiciera falta.

**Reestructuración 2026-09-22:** 24 entradas del índice apuntaban a skills ya eliminadas. Removidas del índice (no del historial):

`adhd-assistant`, `adhd-output`, `anti-ai`, `apple-photos`, `brand-name-forge`, `calorie-counter`, `code-review-and-quality`, `code-simplification`, `curriculum-builder`, `db-readonly`, `debugging-and-error-recovery`, `gateway-restart-helper`, `godot-mcp`, `health-check-dashboard`, `image-generation`, `mcp-orchestrator`, `memory-agent`, `mlx-stt`, `model-router-pro`, `network-scanner`, `playwright-e2e-reactflow`, `shortcuts-generator`, `study-tracker`, `using-agent-skills`.

**Totales activas:** 60 skills (verificado con `openclaw skills list --json`, fuente `openclaw-workspace`).
