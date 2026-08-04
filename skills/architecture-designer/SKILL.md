---
name: "architecture-designer"
description: "Design system architecture, write ADRs, evaluate trade-offs, and produce decision records for technical choices."
metadata:
  version: 2.0.0
  author: Kanam
  tags: ["architecture", "adr", "system-design", "trade-offs", "decisions"]
allowed-tools:
  - read
  - write
  - edit
  - exec
  - web_search
  - web_fetch
  - skill_workshop
---

# Architecture Designer

Make technical decisions explicit. This skill helps design system architecture, compare options, and document the result as Architecture Decision Records (ADRs).

## When to use

- Choosing a tech stack for a new project or feature.
- Deciding between library A and library B.
- Designing data flow, deployment topology, or service boundaries.
- Evaluating trade-offs (performance, cost, maintainability, team skills).
- Preparing a handoff or onboarding doc with system context.
- Planning migrations or refactors.
- **Documenting process decisions** (not just technical ones) — ADRs capture *why* something was done, even if the answer is "defer" or "don't do it".

## ADR format

Save as `.knowledge/adr/NNN-<short-title>.md` (or `docs/adr/` for older projects).

```markdown
# ADR-NNN: <Título corto>

## Estado
Aceptado | Propuesto | Rechazado | Deprecado | Superseded by ADR-MMM

## Contexto
¿Qué problema estamos resolviendo? ¿Qué restricciones existen? ¿Qué información tenemos?

## Decisión
¿Qué elegimos y por qué?

## Consecuencias

### Positivas
- ...

### Negativas
- ...

### Mitigaciones
- ...

## Alternativas consideradas
1. **Opción A:** por qué no.
2. **Opción B:** por qué no.

## Referencias
ARCHITECTURE.md, DEFINITION.md, otros ADRs, links externos
```

### Reglas del formato (aprendidas de 12 ADRs reales)

1. **Contexto concreto** — no "necesitamos una base de datos". Decir "necesitamos persistir leads, conversaciones, knowledge base, eventos y cache de inventario con mínima operación" (ADR-005 de sportcars).
2. **Alternativas con por qué no** — cada opción descartada lleva su razón. No listar por listar.
3. **Consecuencias separadas** — positivas, negativas, y mitigaciones. Las mitigaciones son obligatorias cuando hay negativas.
4. **Referencias a otros docs** — ARCHITECTURE.md, DEFINITION.md, DATA_MODEL.md, otros ADRs. Los ADRs no existen en el vacío.
5. **Decisiones de proceso también** — "deferir integración con Pilot al post-MVP" (ADR-001 sportcars) o "niveles convergentes, no lineales" (ADR-001 bootcamp) son decisiones válidas.
6. **Notas de revisión futura** — si la decisión depende de algo que puede cambiar (credenciales, escala, etc.), poner una nota de cuándo revisarla.

## Workflow

### 1. Frame the decision
- ¿Qué problema resolvemos?
- ¿Qué restricciones tenemos? (tiempo, costo, skills, compliance, escala esperada)
- ¿Quién necesita participar de esta decisión?

### 2. Research options
- Para precios/features/versiones: `web_search` o `web_fetch`.
- Para popularidad/mantenimiento: GitHub stars, npm downloads, last commit, activity.
- Para compatibilidad: revisar stack existente del proyecto.
- Preferir existente sobre custom salvo razón fuerte.

### 3. Apply constraints
- Team skills: ¿el equipo conoce esta tecnología?
- Costo: ¿gratis/ freemium/ pago? ¿cómo escala?
- Tiempo: ¿esto retrasa el MVP?
- Vendor lock-in: ¿qué tan fácil es migrar después?

### 4. Choose and document
- Escribir el ADR en `.knowledge/adr/` o `docs/adr/`.
- Numeración secuencial por proyecto (001, 002...).
- Linkear desde `.knowledge/README.md` o `AGENTS.md` del proyecto.

### 5. Review
- Mostrar al usuario para aprobación antes de implementar.
- Si hay ADRs existentes, verificar que no contradigan ni dupliquen.

## Estructura de archivos

```
.knowledge/
├── adr/
│   ├── 001-primer-decision.md
│   ├── 002-segunda-decision.md
│   └── ...
├── README.md       (linkea los ADRs)
└── ...
```

Para proyectos que usan `docs/adr/` (como quedamos), es válido mantener esa estructura. La convención nueva es `.knowledge/adr/`.

## Integración con otras skills

| Skill | Relación |
|---|---|
| `openspec` | La arquitectura definida acá se documenta como spec de implementación con OpenSpec. Flujo: ADR → OpenSpec → implementación. |
| `agent-workflow` | El rol "architect" produce ADRs como output. |
| `spec-miner` | Para reestructuraciones grandes, pair con spec-miner para extraer la arquitectura actual antes de proponer cambios. |
| `engineering-governance` | Las ADRs alimentan las reglas de gobierno del proyecto. |

## Lecciones de 12 ADRs existentes

### Lo que funciona
- **Contexto concreto** con restricciones reales (tiempo, acceso, skills) — ADR-001 sportcars (no tenemos credenciales de Pilot) es el mejor ejemplo.
- **Alternativas con por qué no** — cada opción descartada tiene su razón, no es ruido.
- **Mitigaciones obligatorias** — toda consecuencia negativa tiene un plan.
- **Decisiones de proceso** — ADR-001 bootcamp (niveles convergentes) y ADR-004 quedamos (sin admins) son decisiones de diseño de proceso, no técnicas, y son igual de valiosas.
- **Referencias cruzadas** — los ADRs que linkean a otros docs (ARCHITECTURE.md, DEFINITION.md) son más fáciles de encontrar y contextualizar.

### Lo que no funciona
- **ADR sin contexto** — "elegimos X" sin decir por qué es inútil a los 3 meses.
- **Alternativas sin razón de rechazo** — listar opciones sin explicar por qué no se eligieron es ruido.
- **Consecuencias sin mitigación** — "es más caro" sin "usamos free tier y monitoreamos" es una queja, no una decisión.

## Referencias

- [ADR template](./references/adr-template.md) — blank ADR para copiar
- [System design template](./references/system-design-template.md) — para diseños más grandes
- [Decision matrix template](./references/decision-matrix.md) — para comparaciones cuantitativas

## Ejemplos

- [ADR-001 sportcars: Deferir Pilot](./examples/sportcars-ADR-001-deferir-pilot.md) — decisión de proceso con restricción externa
- [ADR-003 quedamos: Matching algorithm](./examples/quedamos-ADR-003-matching.md) — decisión técnica con algoritmo detallado
- [ADR-001 bootcamp: Niveles convergentes](./examples/bootcamp-ADR-001-convergentes.md) — lección de proceso documentada como ADR
