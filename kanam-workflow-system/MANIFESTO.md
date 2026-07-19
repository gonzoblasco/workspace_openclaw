# Kanam AI System — MANIFESTO v0.1

> "Un sistema, cuatro voces. Una fuente de verdad."

---

## El Problema

Tenemos 4 repos tratando de hacer lo mismo:

| Repo | Enfoque | Skills | Estado |
|------|---------|--------|--------|
| `gonzoblasco/workflow-kit` | Portable workflow skills (minimalista) | ~15 skills base | ✅ Activo |
| `gonzoblasco/antigravity-developer-stack` | Library enciclopédica (70+ skills) | 70+ skills por dominio | 🟡 Congelado |
| `gonzoblasco/copilot-skills` | Skills reutilizables concisas | ~15 skills modulares | 🔴 Frozen |
| `gonzoblasco/chatgpt-project-architect` | Metodología prompts robustos | Templates + patterns | 🟡 Frozen |

**El costo de la fragmentación:**
- Mantener 4 repos = 4x overhead en maintenance
- Drift de estándares: skills similares con implementaciones distintas
- Difícil tracking OSS: PRs dispersos en múltiples repos
- Confusión para AI agents que necesitan *single source of truth*

### Ejemplo de Doble Mantención

| Skill | workflow-kit | antigravity | copilot-skills | chatgpt-project |
|-------|--------------|-------------|----------------|-----------------|
| `copilot` (orquestador) | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| `pr-review` | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| `security-audit` | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| `new-task` | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| `close-epic` | ✅ Yes | ✅ Yes | ❌ No | ❌ No |

**3 skills que se replican 3 veces en los repos.** Sin unificación, eso es deuda técnica real.

---

## La Solución: Kanami Library Architecture

**Principios del Sistema Unificado:**

1. **Una fuente de verdad**: Un solo repos activo con 3 capas documentadas
2. **Fusion > Fragmentación**: Skills comunes viven en `base/`, otros se curan y archivalizan en `library/`
3. **Neutral branding**: KanamAI no está atado a marcas específicas (OpenClaw, Claude, Google, etc.)
4. **Legacy preservado**: Los 4 repos siguen existiendo como docs con links explícitos hasta el día cero de cierre

### Arquitectura de 3 Capas

```
kanam-workflow-system/
│
├── SKILL.md                       # El orquestador universal (Master)
├── MANIFESTO.md                  # Este documento — reglas del juego
├── README.md                      # Vista unificada con quickstart y diagramas
│
├── docs/
│     ├── workflow-structure.md    # Explica Pre-Flight + 5 Gates
│     ├── task-lifecycle.md        # Lifecycle de tasks/epics completo
│     └── frozen-repos.md          # Mapping: antiguo → nuevo + estado
│
├── skills/
│   │
│   ├── base/                   # Skills universales aplicables a cualquier dominio
│   │    ├── kanam-copilot.md    # Master workflow orchestrator
│   │    ├── kanam-pr-review.md   # Cognitive pre-merge linter
│   │    └── kanam-security-audit.md  # Threat model + multi-tenancy
│   │
│   ├── workflow/               # Workflows específicos por lifecycle
│   │    ├── kanam-new-task.md   # Task initialization: branch → impl → merge
│   │    ├── kanam-close-epic.md # Epic closure: audit, tag, CHANGELOG, release
│   │    └── kanam-pr.md         # PR creation, review, and merge lifecycle
│   │
│   └── library/                # Library curada de patrones genéricos (frozen)
│        ├── patterns-lifecycle/  # Patrones de workflow de antigractory (neutralized)
│        ├── prompt-systems/      # Metodología prompts genérica (ex-chatgpt-project)
│        └── anti-ai-patterns/    # Best practices contra "vibe coding" y AI debt
│
└── LEGACY.md                    # Historial completo del porqué y cómo
```

### Principio de Fusión

Cuando convergen skills de los 4 repos:

| Skill Convergente | Nuevos Namespaces | Repos Source | State |
|-------------------|-------------------|--------------|-------|
| `copilot` + `new-task` (orquestador + workflow master) | `kanam-copilot` | workflow-kit + antigravity + copilot-skills | ✅ Active |
| `pr-review` (x3 repos) | `kanam-pr-review` | workflow-kit + antigravity + copilot-skills | ✅ Active |
| `security-audit` (x2 repos) | `kanam-security-audit` | workflow-kit + antigravity | ✅ Active |
| `pr` + `close-epic` (lifecycle steps) | `kanam-pr`, `kanam-close-epic` | Unified lifecycle docs | ✅ Active |

**Resultado:** 3 skills base unificadas que cubren todos los workflows comunes.

---

## Nomenclatura Neutral

### El Marco KanamAI

> **KanamAI ≠ OpenClaw ≠ Claude ≠ Google = Gemini**
> 
> Kanam es el *framework* que enmarca AIMS (AI Instruction & Memory System).
> 
> Skills con prefix `kanam-*` son propias del framework KanamAI.
> 
> Los examples y docs pueden referenciar LLMs (qwen3.5, deepseek-v4, etc.) como *contextos de uso*, no definiciones.

### Prácticas de Naming

| Categoría | Ejemplo Neutral | Ejemplo Atado | ¿Qué usar? |
|-----------|-----------------|---------------|------------|
| **Master skill** | `kanam-copilot` | `antigravity-copilot` | ✅ `kanam-copilot` |
| **Workflow step** | `kanam-new-task`, `kanam-close-epic` | `workflow-new-task` | ✅ Prefix Kanam |
| **Library content** | `patterns-lifecycle/`, `prompt-systems/` | `antigravity-workflow/`, `chatgpt-patterns/` | ❌ No marca específica |
| **LLM references** | "qwen3.5 example", "deepseek integration" | "Claude Code skill", "Google Copilot" | ✅ Contextual only |

### Ejemplo de Uso Neutral

```markdown
# Kanam AI System — Workflow Usage (Neutral LLM Context)

When using qwen3.5-4b-mlx or deepseek-v4-flash:

```bash
kanam-copilot --project "brainweb" --task T01-ai-drawing-agent

# The agent reads SKILL.md and executes the unified workflow
# Reference antigravity patterns in docs if needed for examples
# Example patterns from /skills/library/patterns-lifecycle/ can assist
```

> **Rule:** Always name skills `kanam-*`. When mentioning LLMs, use neutral naming:
> - ✅ "qwen3.5-4b-mlx model"
> - ✅ "deepseek-v4-flash context"
> - ❌ "Claude Code agent"
> - ❌ "Google Copilot tool"

---

## Transición Planificada

| Fase | Repos Legacy | Acción | Fecha Límite | State |
|------|--------------|--------|---------------|-------|
| **F1** | `workflow-kit` + `copilot-skills` (4 repos) | Fusionar base skills → `kanam-*` | Q3 2026 | ✅ Active |
| **F2** | `antigravity-developer-stack` (70+ skills) | Curar patrones → `patterns-lifecycle/` (neutral names) | Q4 2026 | 🔴 Frozen |
| **F3** | `chatgpt-project-architect` | Migrar prompts → `prompt-systems/` (genéricos) | Q4 2026 | 🔴 Frozen |

### Criteria Go/No-Go

✅ **GO** cuando:
- Skills base tiene ≥90% cobertura de skills duplicadas anteriores
- Los 3 legacy repos no tienen PRs abiertos nuevos o pending review >30 días
- KanamAI community consolidada alrededor de un solo marco de reference
- Gonzo listo para migrar sin perder momentum OSS

🛑 **NO-GO** si:
- Hay features críticas en los 4 repos que no conviven (ej: antigravity tiene 70 skills, kanam-workflow solo 10)
- Los PRs abiertos bloquean merge sin resolver conflictos
- La migración requiere cerrar branches masivas con drift >50%

---

## Roadmap de Migración

| Week | Milestone | Deliverables |
|------|-----------|--------------|
| **W0** (Hoy) | Create repo + structure base | `kanam-workflow-system` repos, base/structure, MANIFESTO created |
| **W1** | Unify core skills | `kanam-copilot`, `kanam-pr-review`, `kanam-security-audit` merged |
| **W2** | Unified workflows | `kanam-new-task`, `kanam-close-epic`, `kanam-pr` lifecycle docs |
| **W3-W4** | Curate library | Neutral names for antigravity patterns, prompt systems → `patterns-lifecycle/`, `prompt-systems/` |
| **W5** | Frozen links | All legacy repos link to frozen-repos.md with migration status |
| **Ongoing** | Cleanup & track | Close legacy repos, update OSS PR contributions tracking |

---

## Final Word

> "Los patrones se escriben una vez. Se ejecutan 10x."
> 
> KanamAI System unifica lo mejor de 4 enfoques fragmentados en un solo marco coherente.
> 
> **Por que:** Drift eliminado, mantenimiento reducido, tracking OSS simplificado.
> 
> **Cuándo:** Cuando la deuda técnica de mantención > beneficio de diversidad.
> 
> **Cómo:** Fusion → Archive → Link → Cleanup.

---

*Last updated: 2026-07-19 • Kanam AI System v0.1 • Neutral LLM Framework*
