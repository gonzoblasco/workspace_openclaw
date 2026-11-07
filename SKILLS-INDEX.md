# SKILLS-INDEX - Skills del workspace

> Índice canónico del árbol de skills *git-tracked*. Verificado por última vez: **2026-11-06**.
> Este archivo **no lleva su propio changelog**: cada cambio va a `CHANGELOG.md` y al historial de git.

---

## 1. Qué es este índice y cómo se cuenta

**Alcance.** Solo el árbol versionado del workspace:

- `skills/` - skills del Core (transversales, infraestructura propia).
- `agents/<rol>/skills/` - skills propias de cada rol.

**No entran:** las skills bundled de OpenClaw, las del Workshop (`~/.openclaw/agents/<id>/agent/workshop-skills/`), las `managed`, `extra` y `custodian`. Esas pertenecen a las superficies del CLI, no a este repo. Tampoco entra `projects/kanam-skills` (repo público, archivado).

**Autoridad.** `openclaw skills list --agent <id> --json`, filtrando `source == "openclaw-workspace"`. El CLI sabe qué tiene el runtime; contar directorios no lo sabe. En un workspace multi-agente el comando necesita `--agent`, porque cada agente ve su propio árbol.

**Totales vigentes (medidos, no heredados):**

| Árbol | Activas |
|---|---|
| `skills/` (Core) | 35 |
| `agents/kanam-dev/skills/` | 44 |
| `agents/kanam-mind/skills/` | 11 |
| `agents/kanam-ops/skills/` | 4 |
| `agents/kanam-studio/skills/` | 7 |
| `agents/kanam-critic/skills/` | 2 |
| `agents/kanam-planner/skills/` | 5 |
| `agents/kanam-auditor/skills/` | 5 |
| **Total activas** | **112** |

> **El ciclo SDD (9 skills `hermes-*`) se movió del árbol del Core al de `kanam-dev` el 2026-09-29** (ADR-083).
> Estaba en `skills/`, así que el Core veía el playbook de ingeniería - `hermes-builder` dice
> "implementation. Writes the change's code" - y lo ejecutó. En aquel corte los totales por árbol
> pasaron de 36→27 (Core) y 25→34 (dev) sin cambiar el total: fueron movimientos, no altas ni bajas.

Además hay **1 placeholder**: `agents/kanam-mind/skills/study-tracker/` (`user-invocable: false`). El CLI lo lista igual (`source: openclaw-workspace`), así que está contado dentro de los 11 de `kanam-mind`; se conserva solo para resolver referencias legacy.

> **Nota de conteo (2026-10-12).** El conteo por árbol es el del CLI (`source == openclaw-workspace`), no el de directorios: `agents/<rol>/skills/*/node_modules/**/SKILL.md` (los trae `playwright-core` en `kanam-auditor`) no entra. `find agents/*/skills -name SKILL.md` cuenta esos `node_modules` y sobrecuenta.

---

## 2. Metodología

### 2.1 Por qué hay dos árboles

Un mismo runtime con roles distintos necesita dos niveles de alcance:

- `skills/` guarda lo **transversal** (session, memoria, git, docs, pipeline) y las **capacidades propias del Core**. El Core es el punto de entrada y router: ejecuta sus propias skills y delega el resto.
- `agents/<rol>/skills/` guarda lo **propio del rol**. Ese rol las ve; otro agente no debería ejecutarlas.

Mover una skill de `skills/` a `agents/<rol>/skills/` cambia quién la ve y quién responde por ella. No es cosmético.

### 2.2 Dónde va una skill nueva

1. ¿La usa más de un rol, o es infraestructura del workspace? → `skills/`.
2. ¿Es la forma de trabajar de un rol puntual? → `agents/<rol>/skills/`.
3. Dudas de si merece existir: `docs/skills-promotion-criteria.md` (regla del 3x para promover a estándar; poda a los 30 días sin uso).

### 2.3 Ciclo de vida

- **Alta propia:** `skill_workshop` (proposal → apply). No se escriben archivos de Workshop a mano.
- **Import de terceros:** llega rompiendo convenciones y hay que normalizarlo al ingresarlo, porque el pre-commit juzga **toda** la colección, no solo lo staged (un import bloquea commits que ni lo tocan).
- **Retiro:** se quita del árbol y se registra el nombre en la sección 4 de este archivo; el historial queda en git.
- **Frontmatter:** el bloque `---` tiene que ser lo primero del archivo. Un comentario antes lo deja fuera del catálogo sin error.

### 2.4 Definir vs consumir

- **El Core define** sus skills (las de la sección 3.1) y las ejecuta.
- **El Core no ejecuta** skills de otro rol: las delega. **Y no las ve.** Una skill de rol vive en
  `agents/<rol>/skills/`, nunca en `skills/`. Lo que el Core ve, el Core lo ejecuta: la separación
  de árboles *es* la separación de responsabilidades, no una convención de carpeta.
- **Verificación mecánica:** `python3 scripts/check-agent-skill-boundary.py` falla si una skill del
  ciclo de desarrollo está en el árbol del Core, si una skill vive en dos árboles, o si el ciclo SDD
  quedó incompleto en su rol. Corre en el pre-commit.
- **Cada rol define** las suyas y responde por ellas. Para saber si un agente puede ejecutar algo,
  no leas su prompt: mirá qué árbol ve.

### 2.5 Contrato de este archivo

- **Inventario, no historial.** Las notas de mantenimiento viven en `CHANGELOG.md`; el "por qué" de cada cambio, en git.
- **Todo link apunta a una ruta real** a la fecha indicada arriba. `scripts/check-refs.py` escanea este archivo en su corrida default y falla si un link no resuelve.
- **El total se re-mide en cada pasada** contra el CLI, no se copia del encabezado anterior.

---

## 3. Inventario

### 3.1 Core - `skills/` (34)

| Skill | Qué hace |
|---|---|
| [session-lifecycle](skills/session-lifecycle/) | Ciclo de sesión completo: inicio, cierre, WAL, handoff. Reemplaza 4 skills de sesión |
| [job-application](skills/job-application/) | Busqueda y postulacion laboral: descubre vacantes, arma el CV contra el JD, llena el formulario del ATS (Lever/Ashby/Eightfold) y verifica el envio. Deja el submit para Gonzo |
| [engineering-governance](skills/engineering-governance/) | Evolución continua del AI Engineering OS: auditoría de workflows, consolidación de learnings, mejoras sistémicas |
| [compaction-domain-aware](skills/compaction-domain-aware/) | Compactación con conciencia de dominio: tiers de prioridad (Tier 0-4) para decidir qué preservar |
| [complexity-driven-pipeline](skills/complexity-driven-pipeline/) | Orquestación complexity-first: scorer antes de spawnear agentes A/B; decide modelo, thinking level y profundidad |
| [model-cata](skills/model-cata/) | Ritual de comparación de modelos LLM: mismo prompt, rúbrica crítica y decisión de motor en ADR |
| [sdd-agent-loop](skills/sdd-agent-loop/) | Loop de agentes por etapas con gate humano |
| [verification-gates](skills/verification-gates/) | Guardas que no dan falso verde: 0 casos corridos, SKIP vs OK, lector honesto |
| [path-audit](skills/path-audit/) | Auditoría de CAMINO por hito de versión (0.5, 1.0): rumbo, próximo paso y afirmaciones no probadas. No lee código |
| [regression-net](skills/regression-net/) | Pipeline C: convierte cada finding de B en un test y valida por mutación. Gate: toda mutación detectada |
| [voz-gonzo](skills/voz-gonzo/) | Redacción con la voz de Gonzo desde `docs/voz-gonzo.md`, con gate de reglas prohibidas ejecutable |
| [trust-vocabulary-report](skills/trust-vocabulary-report/) | Reportar trabajo delegado sin inflarlo: niveles de confianza por etapa |
| [checkmate](skills/checkmate/) | Loop goal → ejecución → verificación con worker + judge |
| [skill-router](skills/skill-router/) | Sugiere qué skill usar para una tarea (keywords + embeddings locales) |
| [capability-index](skills/capability-index/) | Responde '¿tenés X?' con cuatro estados verificados (existe / existe en rol Y / no existe + alternativa / ambiguo), cita ruta verificada |
| [find-skills](skills/find-skills-skill/) | Busca y descubre skills de OpenClaw en ClawHub y otras fuentes |
| [skill-collection-maintenance](skills/skill-collection-maintenance/) | Diagnostica el cron semanal de revisión y elimina skills limpiamente |
| [publish-skills](skills/publish-skills/) | ARCHIVADA. Historial de cómo se publicaba la colección al repo público |
| [workspace-portfolio-hygiene](skills/workspace-portfolio-hygiene/) | Audita/limpia `projects/*`: gitlinks vs blobs, archivo, promoción a doble git |
| [tech-docs](skills/tech-docs/) | Documentación técnica: ADRs, README, API docs, CHANGELOG, guías |
| [git-changelog](skills/git-changelog/) | Genera `CHANGELOG.md` desde git history con conventional commits |
| [github](skills/github/) | Operaciones con `gh` + GitHub MCP: PRs, issues, CI, reviews, notificaciones |
| [supabase-assistant](skills/supabase-assistant/) | Supabase vía MCP: schemas, queries, tipos, migraciones, logs |
| [sql-insight](skills/sql-insight/) | NL a SQL, optimización e interpretación de EXPLAIN (SQLite y PostgreSQL) |
| [pdf-tool](skills/pdf-tool/) | PDFs local: leer (texto, metadata, OCR) y generar. 100% local (poppler + tesseract) |
| [ai-toolbox](skills/ai-toolbox/) | Registro vivo de las herramientas IA de la maquina: que hay, que corre y como se levanta |
| [word-docx](skills/word-docx/) | Crear, inspeccionar y editar DOCX: estilos, numeración, tracked changes, tablas, secciones |
| [cleanmymac-maintenance](skills/cleanmymac-maintenance/) | Mantenimiento con CleanMyMac CLI disparado por frases naturales |
| [deslop](skills/deslop/) | Limpia código AI slop de un branch antes del PR |
| [superpowers](skills/superpowers/) | Workflow spec-first con TDD y ejecución por subagentes |
| [self-improving-agent](skills/self-improving-agent/) | Captura aprendizajes, errores y correcciones en markdown para mejora continua |
| [planner-delegation](skills/planner-delegation/) | Cómo llama el CORE al Planner: cuándo un objetivo es programa, prompt, entregable y verificación del plan antes de ejecutar |
| [task-prep](skills/task-prep/) | Prepara una tarea de grabación de pantalla (Mercor/Odin) antes de grabar: criterio, investigación, guion y checklist |

### 3.2 kanam-dev - `agents/kanam-dev/skills/` (44)

> Ciclo completo Define → Plan → Build → Verify → Review → Ship. Base: `addyosmani/agent-skills`; ⭐ = fusionada con capacidades propias de Kanam.

| Fase | Skill | Qué hace |
|---|---|---|
| Define | [interview-me](agents/kanam-dev/skills/interview-me/) | Interrogatorio de 1 pregunta por vez hasta ~95% de claridad |
| Define | [idea-refine](agents/kanam-dev/skills/idea-refine/) | Divergencia + convergencia para afinar ideas vagas |
| Define | [spec-driven-development](agents/kanam-dev/skills/spec-driven-development/) ⭐ | PRD completo antes de código |
| Plan | [planning-and-task-breakdown](agents/kanam-dev/skills/planning-and-task-breakdown/) ⭐ | Spec a tareas atómicas verificables, con orden y dependencias |
| Build | [incremental-implementation](agents/kanam-dev/skills/incremental-implementation/) | Slices verticales finos: implementar, testear, verificar, commitear |
| Build | [test-driven-development](agents/kanam-dev/skills/test-driven-development/) | Red-Green-Refactor, pirámide de tests, DAMP, Beyonce Rule |
| Build | [context-engineering](agents/kanam-dev/skills/context-engineering/) | Curación del contexto del agente: rules files, context packing, MCP |
| Build | [source-driven-development](agents/kanam-dev/skills/source-driven-development/) | Cada decisión de framework respaldada por doc oficial citada |
| Build | [doubt-driven-development](agents/kanam-dev/skills/doubt-driven-development/) | Revisión adversarial en contexto fresco antes de que algo quede firme |
| Build | [design-direction](agents/kanam-dev/skills/design-direction/) | Dirección de arte antes de codear: las 4 preguntas (propósito, tono, restricciones, diferenciación), herramienta funcional vs pieza memorable, y el orden layout → tema → animación → código |
| Build | [frontend-ui-engineering](agents/kanam-dev/skills/frontend-ui-engineering/) ⭐ | UI de producción accesible (WCAG 2.1 AA), responsive, design system |
| Build | [api-and-interface-design](agents/kanam-dev/skills/api-and-interface-design/) | Contract-first, Hyrum's Law, One-Version Rule, error semantics |
| Build | [api-integration-test](agents/kanam-dev/skills/api-integration-test/) | Contratos entre servicios end-to-end: esquema, flujos multi-servicio, error propagado |
| Build | [debugging-and-error-recovery](agents/kanam-dev/skills/debugging-and-error-recovery/) | Del síntoma a la causa probada: localizar, reproducir, falsificar, probar el fix (y el fix del fix). **Reintroducida el 2026-10-12** |
| Build | [openspec-pattern](agents/kanam-dev/skills/openspec-pattern/) | Contrato de intención antes del código, contra scope creep y deuda |
| Build | [openspec](agents/kanam-dev/skills/openspec/) | CLI de OpenSpec: proposals, spec deltas, design, tasks, archive |
| Verify | [browser-testing-with-devtools](agents/kanam-dev/skills/browser-testing-with-devtools/) | Chrome DevTools MCP: DOM, console, network, performance en vivo |
| Verify | [cross-engine-css-measurement](agents/kanam-dev/skills/cross-engine-css-measurement/) | "Funciona en Chrome, falla en WebKit": causas aisladas con sondas mínimas |
| Verify | [a11y-at-validation](agents/kanam-dev/skills/a11y-at-validation/) | Cuándo la validación manual con AT es obligatoria en OSS, y cómo documentarla |
| Verify | [compatibility-testing](agents/kanam-dev/skills/compatibility-testing/) | Matriz real de entornos (motores, OS, dispositivos): evidencia por combinación, gate de CI |
| Verify | [chaos-engineering](agents/kanam-dev/skills/chaos-engineering/) | Resiliencia por inyección controlada de fallos: hipótesis de estado estable, blast radius |
| Verify | [code-metrics](agents/kanam-dev/skills/code-metrics/) | Métricas objetivas con umbral explícito: cobertura, complejidad, duplicación, hotspots |
| Review | [security-and-hardening](agents/kanam-dev/skills/security-and-hardening/) | OWASP Top 10, auth patterns, secrets, límites del sistema |
| Review | [threat-modeling](agents/kanam-dev/skills/threat-modeling/) | Modelado de amenazas: activos, actores, STRIDE/PASTA, scoring, mitigaciones |
| Review | [performance-optimization](agents/kanam-dev/skills/performance-optimization/) | Measure-first, Core Web Vitals, profiling, bundle analysis |
| Review | [performance-benchmark](agents/kanam-dev/skills/performance-benchmark/) | Benchmark reproducible: línea base, comparación tras el cambio, decisión con evidencia |
| Ship | [git-workflow-and-versioning](agents/kanam-dev/skills/git-workflow-and-versioning/) | Trunk-based, commits atómicos, change sizing |
| Ship | [ci-cd-and-automation](agents/kanam-dev/skills/ci-cd-and-automation/) | Shift Left, feature flags, pipelines con quality gates |
| Ship | [dependency-advisor](agents/kanam-dev/skills/dependency-advisor/) | Dependencias: inventario, salud, riesgo/licencia, justificación y plan de migración |
| Ship | [deprecation-and-migration](agents/kanam-dev/skills/deprecation-and-migration/) | Code-as-liability, deprecación obligatoria vs advisory, zombie code |
| Ship | [documentation-and-adrs](agents/kanam-dev/skills/documentation-and-adrs/) | ADRs, API docs, docs inline: documentar el *why* |
| Ship | [observability-and-instrumentation](agents/kanam-dev/skills/observability-and-instrumentation/) | Structured logging, RED metrics, OpenTelemetry, alertas por síntoma |
| Ship | [shipping-and-launch](agents/kanam-dev/skills/shipping-and-launch/) | Checklists pre-launch, feature flag lifecycle, rollouts, rollback |
| Ship | [project-closure](agents/kanam-dev/skills/project-closure/) | Cierre de proyecto: decisión, aprendizaje y estado en ADR + DB + skill |
| Ship | [kanam-dev-surface](agents/kanam-dev/skills/kanam-dev-surface/) | La superficie del pipeline: intake que falla antes de leer código, plantillas por tipo de tarea, estaciones con exit codes honestos y handoff que no cierra sin evidencia |

**Hermes SDD** - el ciclo de desarrollo por etapas, importado de `mcabreradev/hermes-sdd-agency`
el 2026-09-28 y **movido aquí desde `skills/` el 2026-09-29** (ADR-083). Es el playbook de
implementación: vivía en el árbol del Core, que así lo podía ejecutar. El Core lo *orquesta*
(`sdd-agent-loop`), no lo ejecuta.

| Etapa | Skill | Qué hace |
|---|---|---|
| discovery | [hermes-discovery](agents/kanam-dev/skills/hermes-discovery/) | Reconocimiento del proyecto: describe lo que existe, con evidencia |
| openspec | [hermes-openspec](agents/kanam-dev/skills/hermes-openspec/) | Dueño del ciclo OpenSpec: convierte ideas en specs válidas |
| architect | [hermes-architect](agents/kanam-dev/skills/hermes-architect/) | Diseño técnico: decisiones, límites y riesgos, no implementación |
| planner | [hermes-planner](agents/kanam-dev/skills/hermes-planner/) | Desglose en tareas ejecutables, ordenadas y verificables |
| builder | [hermes-builder](agents/kanam-dev/skills/hermes-builder/) | Implementación: escribe el código del cambio y nada más |
| reviewer | [hermes-reviewer](agents/kanam-dev/skills/hermes-reviewer/) | Revisión adversarial del builder: busca defectos y los prueba |
| qa | [hermes-qa](agents/kanam-dev/skills/hermes-qa/) | Validación del comportamiento contra la spec, con ejecución real |
| pr-reviewer | [hermes-pr-reviewer](agents/kanam-dev/skills/hermes-pr-reviewer/) | Revisión adversarial de un PR publicado, con experiencia de dominio |
| release | [hermes-release](agents/kanam-dev/skills/hermes-release/) | Cierre del cambio: consistencia del diff, versionado, notas, archivado |

### 3.3 kanam-mind - `agents/kanam-mind/skills/` (11)

| Skill | Qué hace |
|---|---|
| [evidence-gate-executable](agents/kanam-mind/skills/evidence-gate-executable/) | Encadena el gate ejecutable: `kb-audit`, `kb-ingest`/`kb-search` y `brief-journal` (veredicto reproducible, cita verificada) |
| [research-brief-protocol](agents/kanam-mind/skills/research-brief-protocol/) | Formato obligatorio del brief: frame antes de buscar, stop criterion, etiquetas obs/inf/unk |
| [source-verification-gate](agents/kanam-mind/skills/source-verification-gate/) | Puerta previa a escribir: bloquea toda afirmación sin fuente abierta y fecha chequeada |
| [evidence-chain-audit](agents/kanam-mind/skills/evidence-chain-audit/) | Audita un artefacto terminado: cada cita debe sostener su conclusión y cada link resolver |
| [knowledge-management](agents/kanam-mind/skills/knowledge-management/) | Gobernanza del conocimiento: learning signals, resolución de conflictos, DREAMS |
| [memory-wiki-workflow](agents/kanam-mind/skills/memory-wiki-workflow/) | Capa analítica de memoria: entities con claims, dashboards y síntesis |
| [engram-project-memory](agents/kanam-mind/skills/engram-project-memory/) | Memoria persistente de proyecto para agentes de pipeline vía MCP (ADR-052) |
| [deepwiki](agents/kanam-mind/skills/deepwiki/) | Consulta documentación de repos GitHub vía DeepWiki MCP |
| [search-fusion](agents/kanam-mind/skills/search-fusion/) | Búsqueda por intención: elige estrategia y herramientas, y fusiona fuentes |
| [technical-book-processor](agents/kanam-mind/skills/technical-book-processor/) | Procesa libros técnicos capítulo por capítulo: learnings, ADRs, ejercicios |

*(+ `study-tracker`: placeholder, ver sección 1.)*

### 3.4 kanam-ops - `agents/kanam-ops/skills/` (4)

| Skill | Qué hace |
|---|---|
| [background-execution](agents/kanam-ops/skills/background-execution/) | Tareas en background: exec + process, worktrees en paralelo, auto-notify |
| [gateway-config](agents/kanam-ops/skills/gateway-config/) | Config del gateway en runtime: edición, health checks, tracking sin reinicios |
| [clawdstrike](agents/kanam-ops/skills/clawdstrike/) | Security audit del gateway OpenClaw |
| [skill-vetter](agents/kanam-ops/skills/skill-vetter/) | Vetting de seguridad antes de instalar una skill de terceros |

### 3.5 kanam-studio - `agents/kanam-studio/skills/` (7)

| Skill | Qué hace |
|---|---|
| [oss-contribution](agents/kanam-studio/skills/oss-contribution/) | Contribución OSS estratégica: triaje, sin pisar PRs, seguimiento de hilos |
| [support-response-writer](agents/kanam-studio/skills/support-response-writer/) | Respuestas de customer support: preventa, posventa, reclamos, devoluciones |
| [copy-editing](agents/kanam-studio/skills/copy-editing/) | Edición de copy: 7 sweeps de claridad, tono, beneficio, prueba, especificidad |
| [content-serializer](agents/kanam-studio/skills/content-serializer/) | Convierte contenido en posts multi-plataforma para LinkedIn y X |
| [i18n-expert](agents/kanam-studio/skills/i18n-expert/) | i18n/l10n: setup, auditoría, reemplazo de strings, paridad de locales |
| [cv-tailor](agents/kanam-studio/skills/cv-tailor/) | Optimiza CVs contra el JD: keywords, reescritura STAR, compatibilidad ATS |
| [mock-interview-drill](agents/kanam-studio/skills/mock-interview-drill/) | Simulacros de entrevista: Behavioral (STAR), Technical, Case, con diagnóstico |

### 3.6 kanam-critic - `agents/kanam-critic/skills/` (2)

| Skill | Qué hace |
|---|---|
| [sharp-adversarial-review](agents/kanam-critic/skills/sharp-adversarial-review/) | Presión adversarial con la rúbrica SHARP: puntúa 5 ejes con evidencia citable, emite VETO / Aprobado / ORO y devuelve los puntos de fricción obligatorios |
| [evidence-hunter](agents/kanam-critic/skills/evidence-hunter/) | Caza evidencia verificable en el repo para sustentar los ejes SHARP: convierte afirmaciones del autor en pruebas automáticas y arma la tabla de evidencia citada |

### 3.7 kanam-planner - `agents/kanam-planner/skills/` (5)

| Skill | Qué hace |
|---|---|
| [session-plan-orchestration](agents/kanam-planner/skills/session-plan-orchestration/) | Orquesta la tarea como plan persistente (`.knowledge/session_plan.json`): traza pasos, asigna roles en orden y evita la amnesia de sesión |
| [program-orchestration](agents/kanam-planner/skills/program-orchestration/) | Convierte un objetivo multi-sesión en un programa con pasos, dueños, criterios de salida, dependencias y evidencia |
| [crew-dispatch](agents/kanam-planner/skills/crew-dispatch/) | Convierte un paso en un contrato de ejecución (agente, modelo, alcance, evidencia); en Fase 1 el CORE ejecuta el spawn |
| [plan-playbooks](agents/kanam-planner/skills/plan-playbooks/) | Biblioteca de planes recurrentes: feature delivery, OSS PR, evaluación de modelos, postulación y auditoría/incidente |
| [plan-review](agents/kanam-planner/skills/plan-review/) | Review semanal y cierre de programa: progreso, bloqueos, estancados y top 3 de la semana |

### 3.8 kanam-auditor - `agents/kanam-auditor/skills/` (5)

| Skill | Qué hace |
|---|---|
| [surface-alignment-audit](agents/kanam-auditor/skills/surface-alignment-audit/) | Audita la superficie contra el Design System: cruce de tokens, filtro Anti-Slop y contraste WCAG medido por rol |
| [design-system-enforcer](agents/kanam-auditor/skills/design-system-enforcer/) | Guardián preventivo: valida componentes antes del merge contra los tokens declarados, detecta hardcode y veta el "AI Look" |
| [accessibility-oracle](agents/kanam-auditor/skills/accessibility-oracle/) | Auditoría a11y en runtime: Playwright + axe-core, navegación por teclado, foco visible, con evidencia visual |
| [pixel-diff](agents/kanam-auditor/skills/pixel-diff/) | Desalineación visual real vs especificación: el CSS contra los tokens y screenshots contra baseline de CI |
| [surface-pipeline](agents/kanam-auditor/skills/surface-pipeline/) | Orquestador de la auditoría de superficie: corre las tres anteriores en secuencia y emite un único veredicto (APROBADO/ADVERTENCIA/RECHAZADO) |

---

## 4. Retiradas

Nombres que existieron y ya no están. Se listan para distinguir una baja deliberada de un olvido. El detalle y el "por qué" viven en `CHANGELOG.md` y en git; no se borran de acá.

- **Consolidación de agosto 2026** (commit `ba12459`): 58 skills redundantes eliminadas; su funcionalidad se absorbió en las fusiones ⭐ de kanam-dev. Recuperables desde el historial de git.
- **`adhd-daily-planner`** (2026-08-06): fusionada en `adhd-assistant` (a su vez retirada después).
- **Reestructuración 2026-09-22:** `adhd-assistant`, `adhd-output`, `anti-ai`, `apple-photos`, `brand-name-forge`, `calorie-counter`, `code-review-and-quality`, `code-simplification`, `curriculum-builder`, `db-readonly`, `debugging-and-error-recovery`, `gateway-restart-helper`, `godot-mcp`, `health-check-dashboard`, `image-generation`, `mcp-orchestrator`, `memory-agent`, `mlx-stt`, `model-router-pro`, `network-scanner`, `playwright-e2e-reactflow`, `shortcuts-generator`, `using-agent-skills`.
- **`study-tracker`:** no retirada como archivo, degradada a placeholder (sección 1).

---

## 5. Herramientas de verificación

| Comando | Qué verifica |
|---|---|
| `openclaw skills list --agent <id> --json` | Autoridad sobre qué skills tiene el runtime, con `source` por skill |
| `python3 scripts/check-refs.py` | Que cada link de este archivo resuelva a una ruta real |
| `./scripts/test-skills.sh` | Frontmatter, sintaxis, refs a scripts y links entre skills |
| `python3 scripts/check-agent-skill-boundary.py` | Que la frontera CORE/rol se respete: ciclo SDD fuera del árbol del Core, sin duplicados, ciclo completo. Corre en el pre-commit |

---

_Reescrito de cero el 2026-09-29: nueve bloques "Actualización <fecha>" que se contradecían se reemplazaron por este documento. Estructura: qué es y cómo se cuenta → metodología → inventario → retiradas → verificación. Los totales se miden contra el CLI, no se heredan._
