# Skills Archive - Skills Archivadas

Este directorio contiene skills que fueron **archivadas** durante la consolidación del set de skills (agosto 2026). Su funcionalidad fue absorbida por skills fusionadas o ya no son necesarias en el stack activo.

**Nada se borró.** Todo está preservado aquí por si necesitamos recuperar una capacidad específica.

---

## Criterios de Archivado

1. **Duplicadas de las skills de Addy Osmani** (`addyosmani/agent-skills`) adoptadas como base.
2. **Funcionalidad absorbida** en skills fusionadas (ej: `accessibility-studio` → `frontend-ui-engineering`).
3. **Meta-skills** redundantes con `using-agent-skills`.
4. **No aplican** al stack actual o son experimentos abandonados.

---

## Mapa de Archivado → Reemplazo

### Fusionadas en `frontend-ui-engineering`
| Archivada | Funcionalidad absorbida |
|---|---|
| accessibility-studio | WCAG 2.1 AA, ARIA, focus management, screen reader testing |
| ui-design | Component architecture, design system integration |
| ui-generation | AI generation prompts para componentes |
| anti-slop-design | Anti-patterns de "AI aesthetic" |
| a11y-audit-agent | Auditoría de accesibilidad |
| sovereign-accessibility-auditor | Auditoría de accesibilidad |

### Fusionadas en `code-review-and-quality`
| Archivada | Funcionalidad absorbida |
|---|---|
| anti-pattern-czar | Detección de anti-patterns |
| code-review-agent | Review de 5 ejes |
| code-mentor | Feedback de mentoría |
| review-quality | Confidence tagging |

### Fusionadas en `debugging-and-error-recovery`
| Archivada | Funcionalidad absorbida |
|---|---|
| debug-agent | Triage de 5 pasos |
| debug-investigation | Logging forense |
| failure-memory | Patrones de fallo |

### Fusionadas en `spec-driven-development`
| Archivada | Funcionalidad absorbida |
|---|---|
| build-scaffold | OpenSpec scaffolding |
| anydocs | Artefactos de documentación |
| spec-miner | Extracción de specs |

### Fusionadas en `planning-and-task-breakdown`
| Archivada | Funcionalidad absorbida |
|---|---|
| timeline-builder | Estimación de timelines |
| gh-issue-planner | Planificación de GitHub issues |
| brw-plan-my-day | Descomposición de tareas |

### Reemplazadas por skills de Addy
| Archivada | Reemplazo de Addy |
|---|---|
| deploy-agent, deploy-pilot | ci-cd-and-automation + shipping-and-launch |
| pre-deploy-qa, release-management | shipping-and-launch |
| qa-patrol, quality-gate | test-driven-development + code-review-and-quality |
| build-discipline | incremental-implementation + test-driven-development |
| dev-workflow-orchestrator, execution-agent, orchestrator-agent, agent-workflow | using-agent-skills |
| architecture-designer | api-and-interface-design + documentation-and-adrs |
| design-orchestrator | frontend-ui-engineering + spec-driven-development |
| pipeline-detector, arc-trust-verifier, api-guardian | api-and-interface-design + security-and-hardening |
| research-spike, oss-agent, oss-contribution, research-agent | source-driven-development |
| governance-agent | engineering-governance |
| session-context, context-anchor, context-aware-delegation, context-slimmer | context-engineering |
| task-execution | incremental-implementation |
| handoff-matrix | session-lifecycle |
| dev-chronicle | knowledge-management + git-changelog |
| code-documenter | documentation-and-adrs |
| dev-guide-generator | tech-docs |
| product-discovery, campaign-plan | idea-refine |
| dependency-management | deprecation-and-migration |
| saas-metrics-coach | observability-and-instrumentation |
| incident-response, observability | observability-and-instrumentation + debugging |
| vibe-code-cleanup | code-simplification + code-review-and-quality |
| versioned-reports, tide-watch | knowledge-management |

---

## Mantenidas (no archivadas, infraestructura única de Gonzo)

Estas skills son infraestructura propia o de vida diaria que NO se archivan:

- **Infraestructura OpenClaw core:** session-lifecycle, knowledge-management, memory-agent, openspec, background-execution, engineering-governance
- **Stack de Gonzo:** supabase-assistant, sql-insight, db-readonly, mcp-orchestrator
- **Especializadas:** i18n-expert, shortcuts-generator, support-response-writer, deepwiki
- **Vida/carrera:** adhd-assistant, adhd-daily-planner, mock-interview-drill, cv-tailor, apple-photos, calorie-counter
- **Creativas:** copy-editing, narrative-content, brand-name-forge, content-serializer, deslop, image-generation

---

## Cómo recuperar una skill archivada

```bash
# Mover de vuelta a skills/
mv skills/archive/<nombre> skills/
```

---

## Cómo verificar que una fusión preservó todo

Cada skill fusionada lista sus fuentes en `## Resources` / `## References` al final del SKILL.md. Si una capacidad específica falta, revisar la skill archivada original en `archive/<nombre>/`.
