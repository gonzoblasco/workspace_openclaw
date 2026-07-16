---
name: "project-orchestrator"
description: "Product Owner/Manager end-to-end: evalúa ideas, define producto, prioriza MVP, y orquesta las demás skills para llevar productos de idea a deployado."
---

# Project Orchestrator

Evalúa ideas de producto, las define, prioriza un MVP, planifica roadmap, y orquesta las skills necesarias para ejecutar. Integra la metodología docs/code + LEARNINGS.md + HANDOFF.md.

## Filosofía

Cada proyecto vive en `projects/<slug>/` con dos subcarpetas:

```
projects/<slug>/
├── docs/       # Documentación interna: BRIEF, EVALUATION, DEFINITION, ROADMAP, STATUS, HANDOFF, ADRs, LEARNINGS
├── code/       # Código fuente (con su propio .git y remote)
└── HANDOFF.md  # (opcional) Documentación en raíz si no hay docs/ completa
```

- `docs/` = fuente de verdad del **qué** y **por qué**
- `code/` = implementación del **cómo**
- `projects/*/code/` en `.gitignore` del workspace
- Archivos de documentación que no existan se crean como placeholder en raíz

## Fases

### Phase 0: Intake
Recibir la idea cruda. Crear `projects/<slug>/docs/` con BRIEF.md.

**BRIEF.md debe contener:**
- Raw idea (una línea)
- Estado actual (qué existe, qué no)
- Contexto (por qué ahora, para quién)
- Preguntas a resolver en Phase 1

### Phase 1: Evaluation
Analizar mercado, competidores, viabilidad. Crear EVALUATION.md.

**Evaluar:**
- Competidores directos e indirectos
- Diferenciación real
- Viabilidad técnica
- Fit estratégico (¿alineado con la visión Kanam?)
- **Go/No-go** documentado

### Phase 2: Definition
Definir MVP concreto. Crear DEFINITION.md.

**DEFINITION.md debe contener:**
- Core value (una frase)
- In scope (MVP)
- Out of scope (post-MVP)
- Explicit non-goals
- User personas (2 máximo)
- User flows (2-3 críticos)
- Success metrics

### Phase 3: Roadmap
Planificar fases. Crear ROADMAP.md.

**ROADMAP.md debe contener:**
- Phase breakdown (fases con goal, deliverable, tasks)
- Skill mapping (qué skill ejecuta cada fase)
- Risk register (riesgos, impacto, probabilidad, mitigación)

### Phase 4: Execution
Orquestar las skills necesarias para ejecutar cada fase.

**Skills que puede orquestar:**
- `web-app-builder` — scaffold de apps web
- `sdd-brownfield` — Spec-Driven Development en proyectos existentes
- `agent-dispatcher` — delegar tareas a subagentes
- `agent-review` — verificar output antes de propagar
- `ux-a11y-studio` — diseño UX + accesibilidad

### Phase 5: Maintenance
Actualizar STATUS.md con cada hito. Registrar learnings.

**STATUS.md debe contener:**
- Estado actual (fase, blockers, next action)
- Lo que existe
- Próximo hito

**LEARNINGS.md debe poblarse después de cada sesión significativa:**
- Decisiones y por qué
- Lo que salió mal y cómo evitarlo
- Lo que salió bien y cómo repetirlo
- Descubrimientos inesperados

## Documentos estándar

| Archivo | Propósito | Creado en |
|---------|-----------|-----------|
| `BRIEF.md` | Idea cruda + contexto | Phase 0 |
| `EVALUATION.md` | Análisis de mercado + Go/No-go | Phase 1 |
| `DEFINITION.md` | MVP scope + personas + flows | Phase 2 |
| `ROADMAP.md` | Fases + risks | Phase 3 |
| `STATUS.md` | Estado actual + blockers | Phase 4+ |
| `HANDOFF.md` | Resumen ejecutivo para próxima sesión | Siempre en raíz |
| `LEARNINGS.md` | Lecciones aprendidas | Siempre en docs/ |
| `ADRs` | Decisiones de arquitectura | Cuando se tomen |

## Reglas

- Si tiene ciclo de Product Owner completo → `docs/` completo + `code/`
- Si es herramienta interna o experimento → solo `projects/<slug>/` sin docs completos
- Forks externos → HANDOFF.md explicando qué es
- Proyectos sin documentación completa → los archivos faltantes se documentan en HANDOFF.md en raíz
- El feedback de cada sesión se anota en LEARNINGS.md + memory/YYYY-MM-DD.md
- Lecciones transversales van a MEMORY.md
