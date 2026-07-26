# Plan de Adopción: google/skills → Ecosistema OpenClaw

**Fecha:** 2026-07-23
**Contexto:** Revisión de https://github.com/google/skills — ~70 skills de Google para agentes AI.
**Objetivo:** Extraer patrones, estructuras y convenciones que mejoren nuestras skills del workspace.

---

## Progreso

### ✅ Fase 1: Frontmatter estandarizado — COMPLETADA (2026-07-23)
- 20/20 skills con frontmatter YAML unificado
- Formato: `name`, `metadata.category`, `metadata.tags`, `description`, `user-invocable`
- 6 categorías: Workflow (12), Governance (3), Product (2), Content (2), Contribution (1)
- `narrative-content` mantiene `argument-hint` (específico de esa skill)

### ✅ Fase 2: References/ — COMPLETADA (2026-07-23)
- 9 skills candidatas con contenido extraído a `references/`
- 13 nuevos archivos de referencia creados
- SKILL.md actualizados para referenciar los nuevos archivos
- Skills trabajadas: observability, knowledge-management, debug-investigation, performance-optimization, dependency-management, research-spike, engineering-governance, incident-response, release-management

| Skill | References creados |
|---|---|
| observability | alerting.md, dashboards.md (tenía metrics.md) |
| knowledge-management | artifacts.md, checklist.md |
| debug-investigation | experiments.md (tenía techniques.md) |
| performance-optimization | tools.md (tenía domains.md) |
| dependency-management | health-assessment.md, risk-analysis.md |
| research-spike | sources.md (tenía template.md) |
| engineering-governance | audit-checklist.md, rfc-template.md |
| incident-response | severity.md (tenía postmortem-template.md) |
| release-management | checklist.md (tenía strategies.md) |

### ✅ Fase 3: Cross-referencing — COMPLETADA (2026-07-23, mergeada con Fase 1)
- 20/20 skills con `## Related Skills` al final
- Cada skill linkea a 1-3 skills relacionadas con descripción del vínculo

### ✅ Fase 4: Issue #183 — COMPLETADA (2026-07-23)
- PR #196 creado: https://github.com/google/skills/pull/196
- Nuevo archivo: `references/verify-revision-state.md`
- SKILL.md actualizado para linkear el nuevo reference
- Recipe de 5 pasos: upload → monitor LRO → get default revision → fetch revision → report
- Output JSON con `runtime_loaded_revision: "unknown"` explícito
- Acceptance test documentado

---

## Diagnóstico Inicial

### Estado actual de nuestras skills (20 skills)

| Aspecto | Hoy | Problema |
|---|---|---|
| **Frontmatter** | Inconsistente. Algunas tienen `name`, `description`, `user-invocable`. Otras no. Ninguna tiene `metadata.category`. | Sin categorías, no podemos filtrar/agrupar skills programáticamente. |
| **References/** | Solo 7/20 skills tienen carpeta `references/`, y cada una tiene 1 archivo. Google tiene 6+ por skill. | Skills grandes (300+ líneas) mezclan contenido procedural con referencia. Difícil de mantener. |
| **Categorización** | Skills planas en `skills/`. Sin taxonomía. | No hay forma de decir "skills de accesibilidad" vs "skills de producto". |
| **Cross-referencing** | Algunas skills linkean a otras, pero sin convención. | Google usa `## Related Skills` al final de cada SKILL.md. |

### Lo que Google hace bien (y podemos copiar)

1. **Frontmatter YAML estandarizado** con `name`, `metadata.category`, `description`
2. **Carpeta `references/`** con sub-páginas temáticas (CLI, client libraries, MCP, IaC, IAM, core concepts)
3. **Categorización por metadata** — permite filtrado y agrupación
4. **`## Related Skills`** al final de cada skill — cross-referencing explícito
5. **Skills modulares** — cada skill cubre un producto/dominio específico, no mezcla

---

## Plan de Implementación

### Fase 1: Estandarización de Frontmatter (1 sesión)

**Qué:** Unificar el frontmatter YAML de todas las 20 skills.

**Formato target:**
```yaml
---
name: "skill-name"
metadata:
  category: "Workflow"  # o "Reference" / "Product" / "Template"
  tags:
    - tag1
    - tag2
description: "Descripción corta (<160 chars)"
user-invocable: false
---
```

**Categorías propuestas:**
| Categoría | Skills |
|---|---|
| `Workflow` | task-execution, review-quality, build-scaffold, pre-deploy-qa, debug-investigation, performance-optimization, dependency-management, release-management, incident-response, research-spike, vibe-code-cleanup, session-lifecycle |
| `Product` | product-discovery, accessibility-studio |
| `Governance` | engineering-governance, knowledge-management, observability |
| `Content` | narrative-content, tech-docs |
| `Contribution` | oss-contribution |

**Tags sugeridos:** `accesibilidad`, `testing`, `seguridad`, `documentacion`, `scaffold`, `bug`, `performance`, `dependencias`, `release`, `incidentes`, `producto`, `gobernanza`, `conocimiento`, `observabilidad`, `sesion`, `calidad`, `contenido`, `contribucion`

**Acción:**
- Editar SKILL.md de cada skill para estandarizar frontmatter
- Agregar `## Related Skills` al final de cada skill donde corresponda
- Commit al workspace git

---

### Fase 2: References/ para skills grandes (2-3 sesiones)

**Qué:** Extraer contenido de referencia de las skills más grandes a `references/`.

**Candidatos prioritarios** (skills >300 líneas o >3500 chars):

| Skill | Líneas | Chars | Qué extraer |
|---|---|---|---|
| `observability` | 354 | 3834 | Métricas, dashboards, alertas |
| `knowledge-management` | 341 | 3945 | Formatos de documentación, templates |
| `debug-investigation` | 333 | 3662 | Técnicas de debugging, comandos |
| `performance-optimization` | 320 | 3593 | Dominios de optimización, herramientas |
| `dependency-management` | 307 | 3765 | Estrategias, comandos, políticas |
| `research-spike` | 297 | 3684 | Templates, técnicas de investigación |
| `engineering-governance` | 295 | 4390 | Políticas, checklists, auditorías |
| `incident-response` | 291 | 3328 | Post-mortem template, runbooks |
| `release-management` | 352 | 3484 | Estrategias, checklists, comandos |

**Estructura target de references/:**
```
references/
├── cli-commands.md       # Comandos útiles
├── templates.md          # Templates (post-mortem, reportes, etc.)
├── checklists.md         # Checklists operativas
├── strategies.md         # Estrategias y enfoques
└── examples.md           # Ejemplos de uso
```

**Criterio de extracción:**
- Si un bloque de contenido es >20 líneas y es referencial (no procedural), va a `references/`
- El SKILL.md queda como flujo procedural + enlaces a references/
- Cada reference tiene un `## Related` al final linkeando de vuelta al SKILL.md

**Acción:**
- Por cada skill candidata, crear carpeta `references/` y migrar contenido
- Actualizar SKILL.md para referenciar los nuevos archivos
- Verificar que ningún enlace se rompa

---

### Fase 3: Cross-referencing sistemático (1 sesión, puede mergear con Fase 1)

**Qué:** Agregar `## Related Skills` al final de cada skill.

**Mapa de relaciones:**

| Skill | Relacionada con |
|---|---|
| `task-execution` | build-scaffold, review-quality, pre-deploy-qa |
| `review-quality` | task-execution, pre-deploy-qa, security-audit (si existe) |
| `build-scaffold` | task-execution, tech-docs |
| `pre-deploy-qa` | task-execution, review-quality, performance-optimization |
| `debug-investigation` | performance-optimization, incident-response |
| `incident-response` | debug-investigation, observability, postmortem |
| `observability` | performance-optimization, incident-response |
| `performance-optimization` | observability, debug-investigation |
| `dependency-management` | release-management, task-execution |
| `release-management` | dependency-management, task-execution |
| `product-discovery` | build-scaffold, tech-docs |
| `accessibility-studio` | review-quality, pre-deploy-qa |
| `engineering-governance` | knowledge-management, observability |
| `knowledge-management` | engineering-governance, tech-docs |
| `tech-docs` | knowledge-management, build-scaffold |
| `research-spike` | product-discovery, task-execution |
| `vibe-code-cleanup` | review-quality, debug-investigation |
| `session-lifecycle` | task-execution, knowledge-management |
| `oss-contribution` | review-quality, tech-docs |
| `narrative-content` | tech-docs |

**Formato:**
```markdown
## Related Skills

- [Task Execution](../task-execution): Para implementar lo definido aquí
- [Review & Quality](../review-quality): Para revisar antes de mergear
```

---

### Fase 4: Issue #183 — Contribución a google/skills (1 sesión, opcional)

**Qué:** Crear PR para el issue #183 — agregar recipe de verificación end-to-end al Skill Registry skill.

**Requisitos:**
- Leer el SKILL.md actual de `agent-platform-skill-registry`
- Entender el flujo: upload → LRO → default revision → runtime load
- Escribir el recipe documentado que pide el issue
- PR en inglés, tono técnico pero accesible

**Verificación:**
- El recipe debe cubrir: monitor LRO, get mutable skill, get-revision, reportar estado
- Debe incluir advertencia explícita de que registry default ≠ runtime loaded
- Ejemplo JSON de output esperado

---

## Timeline Estimado

| Fase | Duración | Dependencias | Prioridad | Estado |
|---|---|---|---|---|
| Fase 1: Frontmatter | ~1 sesión (2-3h) | Ninguna | 🔴 Alta | ✅ Completada |
| Fase 2: References/ | ~2-3 sesiones (4-6h) | Fase 1 | 🟡 Media | ✅ Completada |
| Fase 3: Cross-refs | ~1 sesión (1-2h) | Fase 1 (puede mergear) | 🟢 Hacer con Fase 1 | ✅ Completada |
| Fase 4: Issue #183 | ~1 sesión (2-3h) | Ninguna (independiente) | 🟢 Si hay ganas | ✅ Completada — PR #196 |

---

## Riesgos y Consideraciones

- **Riesgo de over-engineering:** No todas las skills necesitan `references/`. Skills chicas (<50 líneas) como `narrative-content` o `build-scaffold` no se benefician.
- **Riesgo de romper enlaces:** Al mover contenido a `references/`, verificar que los enlaces internos sigan funcionando.
- **Riesgo de inconsistencia temporal:** Durante la migración, algunas skills tendrán el nuevo formato y otras no. Aceptable mientras dure.
- **Costo de mantenimiento:** Más archivos = más que mantener. Pero el beneficio (skills más legibles y navegables) lo compensa.

---

## Criterio de Éxito

- ✅ Todas las skills tienen frontmatter YAML estandarizado con `metadata.category`
- ✅ Todas las skills tienen `## Related Skills` al final
- ✅ Skills >300 líneas tienen `references/` con contenido extraído
- ✅ `npx biome check --write .` pasa sin errores después de los cambios
- ✅ (Opcional) PR merged en google/skills para issue #183 — PR #196 abierto
