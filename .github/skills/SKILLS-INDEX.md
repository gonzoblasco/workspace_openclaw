# SKILLS-INDEX.md — Skills del Workspace

> Skills activas organizadas por categoría. Actualizado: 2026-08-06
>
> **Nota de consolidación:** En agosto 2026 se redujo el set de skills de 96 a 60 activas, adoptando las 24 skills de ingeniería de `addyosmani/agent-skills` como base y fusionando en ellas las funcionalidades de skills propias redundantes. Las skills redundantes fueron eliminadas (recuperables desde el historial de git, commit `ba12459`).

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
| [debugging-and-error-recovery](skills/debugging-and-error-recovery/) ⭐ | Triage de 5 pasos: reproduce, localize, reduce, fix, guard + logging forense + failure patterns. Fusiona: debug-agent, debug-investigation, failure-memory |

### Review
| Skill | Descripción |
|---|---|
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

### Meta
| Skill | Descripción |
|---|---|
| [using-agent-skills](skills/using-agent-skills/) | Mapea el trabajo entrante a la skill correcta y define reglas de operación compartidas |

## Core OpenClaw (Infraestructura Propia)

| Skill | Descripción |
|---|---|
| [session-lifecycle](skills/session-lifecycle/) | Ciclo de sesión completo: inicio, cierre, WAL protocol, handoff, ADHD productivity |
| [knowledge-management](skills/knowledge-management/) | Gobernanza de conocimiento, learning signals, conflict resolution, DREAMS |
| [memory-agent](skills/memory-agent/) | Memory Agent autónomo: consolida memoria, detecta patrones, mantiene knowledge |
| [openspec](skills/openspec/) | CLI de OpenSpec para spec-driven development |
| [background-execution](skills/background-execution/) | Patrones para ejecutar tareas en background: exec + process, worktrees |
| [engineering-governance](skills/engineering-governance/) | Evolución continua del AI Engineering OS, auditoría y mejora sistémica |
| [git-changelog](skills/git-changelog/) | Auto-genera CHANGELOG.md desde git history con conventional commits |

## Stack de Gonzo (Infraestructura Única)

| Skill | Descripción |
|---|---|
| [supabase-assistant](skills/supabase-assistant/) | Interact with Supabase projects: schemas, queries, types, migrations |
| [sql-insight](skills/sql-insight/) | Traducir lenguaje natural a SQL, optimizar queries, interpretar EXPLAIN |
| [db-readonly](skills/db-readonly/) | Queries read-only seguras a PostgreSQL y MySQL |
| [mcp-orchestrator](skills/mcp-orchestrator/) | Orquestación de MCP servers |

## Especializadas

| Skill | Descripción |
|---|---|
| [i18n-expert](skills/i18n-expert/) | Internacionalización/localización: setup, auditoría, reemplazo de strings, paridad de locales |
| [shortcuts-generator](skills/shortcuts-generator/) | Genera Shortcuts de Apple válidos desde lenguaje natural |
| [support-response-writer](skills/support-response-writer/) | Respuestas profesionales de customer support |
| [deepwiki](skills/deepwiki/) | Consulta documentación de repos GitHub via DeepWiki MCP |
| [tech-docs](skills/tech-docs/) | Documentación técnica: ADRs, README, API docs, CHANGELOG, guías |
| [oss-contribution](skills/oss-contribution/) | Workflow de contribución OSS: triaje, seguimiento de issues/PRs, community, registry |

## Seguridad y Red

| Skill | Descripción |
|---|---|
| [clawdstrike](skills/clawdstrike/) | Security audit del gateway OpenClaw |
| [network-scanner](skills/network-scanner/) | Escáner de red local para descubrir dispositivos |

## Carrera y Crecimiento

| Skill | Descripción |
|---|---|
| [mock-interview-drill](skills/mock-interview-drill/) | Simulacros de entrevistas: Behavioral (STAR), Technical, Case con diagnóstico |
| [cv-tailor](skills/cv-tailor/) | Optimizar CVs: matching de keywords, reescritura STAR con datos cuantitativos |

## Contenido y Creatividad

| Skill | Descripción |
|---|---|
| [copy-editing](skills/copy-editing/) | Edición profesional de copy: 7 sweeps de claridad, tono, beneficio |
| [narrative-content](skills/narrative-content/) | Taller de escritura de ficción: mentoría, técnicas, guía |
| [brand-name-forge](skills/brand-name-forge/) | Workshop sistemático de naming de marca: 8 métodos clásicos |
| [content-serializer](skills/content-serializer/) | Convertir contenido en posts multi-plataforma para LinkedIn y X |
| [deslop](skills/deslop/) | Limpia código AI slop de branches antes de PRs |
| [image-generation](skills/image-generation/) | Genera imágenes para juegos, web, mockups y proyectos creativos |
| [curriculum-builder](skills/curriculum-builder/) | Scaffold para tutores adaptativos con IA |

## Vida Diaria y Herramientas

| Skill | Descripción |
|---|---|
| [adhd-assistant](skills/adhd-assistant/) | Gestión de vida diaria para ADHD: planificación, desglose de tareas, energy windows, transition buffers, dopamine sequencing, shutdown ritual. Fusiona: adhd-daily-planner |
| [apple-photos](skills/apple-photos/) | Acceso terminal a Photos.app: buscar, listar, exportar |
| [calorie-counter](skills/calorie-counter/) | Tracking diario de calorías y proteína en SQLite local |
| [mlx-stt](skills/mlx-stt/) | Speech-to-text local en Apple Silicon con MLX |
| [checkmate](skills/checkmate/) | Goal-to-execution-to-verification loop con worker + judge |
| [github](skills/github/) | Official GitHub MCP server wrapper: security alerts, notifications |
| [godot-mcp](skills/godot-mcp/) | Aprender Godot 4.x paso a paso con asistencia de OpenClaw |

---

## Skills Eliminadas

58 skills redundantes fueron eliminadas en la consolidación (commit `ba12459`). Su funcionalidad fue absorbida por las fusiones. **Recuperables desde el historial de git** si alguna capacidad específica llegara a faltar.

**Además (2026-08-06):** `adhd-daily-planner` se fusionó dentro de `adhd-assistant` (energy windows, transition buffers, dopamine sequencing, shutdown ritual, recovery protocol). Recuperable desde git si hiciera falta.

**Totales activas:** 60 skills
