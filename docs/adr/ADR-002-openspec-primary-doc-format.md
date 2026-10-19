# ADR-002: kanam-spec Primary Doc Format

**Status:** Accepted  
**Deciders:** Gonzo / Kanam  
**Fecha:** 2026-07-19  
**Actualizado:** 2026-10-15  
**Origen:** kanam-workflow / kanam-spec-nextgen

## Decision

Adoptar **kanam-spec** (formato spec-driven con secciones fijas) como formato de documentación primario en todas las etapas del ciclo de definición de producto, reemplazando markdown fragmentado y artefactos ad-hoc.

## Contexto

Durante la integración de spec-driven development, los proyectos acumularon documentación en múltiples formatos sin esquema consistente. El formato kanam-spec - desarrollado en `kanam-spec-nextgen` y validado en `kanam-spec`, `kanam-onwheels`, `soporteml` - demostró que una estructura fija de secciones garantiza cobertura, permite regeneración por sección y evita scope creep.

**Lo que NO es kanam-spec:**
- No es OpenSpec con frontmatter YAML (esa variante se exploró y descartó)
- No es markdown libre - cada sección tiene contrato obligatorio
- No es un template que se rellena - es un documento vivo que se versiona y audita

## Estructura del Formato kanam-spec

Cada spec es un archivo `.md` con **7 secciones obligatorias** en orden fijo:

```markdown
# kanam-spec Specification

## Overview
Descripción de alto nivel: qué es, para qué, contexto.

## Goals
Objetivos medibles (no tareas). Cada goal tiene criterio de éxito.

## Requirements
### Functional
- FR-1: Requisito con SHALL/MUST
### Non-functional
- NFR-1: Requisito con SHALL/MUST

## Non-goals
Lo que explícitamente NO se hace (previene scope creep).

## Scenarios
Casos de uso narrativos que cubren happy path + edge cases.

## Acceptance Criteria
Criterios de aceptación verificables, uno por requisito core.

## Verification Plan
Cómo se verifica cada acceptance criterion (comando, test, inspección).
```

## Artefactos por Proyecto

```
projects/<slug>/
├── .knowledge/
│   ├── BRIEF.md              # kanam-spec: problem statement, audience, success metrics
│   ├── STATUS.md             # Estado por etapa + decisiones (D1, D2...) con verificación
│   ├── specs/
│   │   ├── SPEC-001-<capacidad-core>.md
│   │   └── SPEC-002-<capacidad-core>.md
│   ├── KNOWLEDGE.md          # Negocio, dominio, decisiones cerradas, reutilización, riesgos
│   └── HANDOFF.md            # Contexto de continuidad (regenerado al cerrar sesión)
├── docs/
│   ├── architecture.md       # Decisiones CON alternativa descartada + invariantes + test
│   ├── CONTEXT.md            # Glosario autoritativo: un término por concepto
│   ├── data-model.md         # Esquema como contrato, excepciones declaradas
│   └── adr/
│       ├── index.md
│       └── ADR-NNNN-*.md     # Una decisión durable por ADR
```

## Gates de Validación (medibles)

| Check | Comando | Esperado |
|-------|---------|----------|
| Contrato H1 | `grep -c '^# kanam-spec' <spec>` | 1 |
| 7 secciones | `grep -c '^## ' <spec>` | 7 |
| FR/NFR con SHALL/MUST | `grep -c 'SHALL\|MUST' <spec>` | ≥ número de requisitos |
| Acceptance Criteria | `grep -c '^## 5\.' <spec>` | 1 (sección única) |
| Verification Plan | `grep -c '^## 7\.' <spec>` | 1 (sección única) |
| Validación spec-driven | `openspec validate <spec>` | 0 errores |

> **Nota:** `openspec validate` es el checker del proyecto `kanam-spec` (no `kanam-spec-nextgen`). El glob es `<dir>/*.md` sin recursar; apuntar al directorio correcto: `openspec validate projects/<slug>/.knowledge/specs/`

## Skills Relacionadas (verificado 2026-10-18)

Las skills del ciclo viven en el **workshop del CORE** (`~/.openclaw/agents/main/agent/workshop-skills/`); el CORE las orquesta y delega la implementación (ADR-083):

- `spec-discovery-creation` / `spec-draft-creation` (CORE workshop) - Generan specs kanam-spec desde idea (endpoint kanam-spec-nextgen + Ollama)
- `spec-validation` (CORE workshop) - Corre el checker de specs (wrapper del validador compartido de `spec-driven-development`, que vive en DEV)
- `product-definition-cycle` (CORE workshop) - Orquesta el ciclo que produce estos artefactos
- `spec-driven-development`, `openspec` (DEV, `agents/kanam-dev/skills/`) - Implementación según el spec

## Referencias

- [ADR-001](./ADR-001-product-pipeline-integration.md): Ciclo de definición de producto (4 etapas)
- [ADR-003](./ADR-003-product-reset-triggers.md): Triggers de avance en el ciclo
- `kanam-spec-nextgen/server/index.mjs`: Endpoint discovery que genera specs
- `kanam-spec/openspec/`: Validador y catálogo de secciones (proyecto separado, no en workspace)

---

*Reescrito 2026-10-15: elimina OpenSpec frontmatter ficticio; refleja kanam-spec real (7 secciones fijas, validación openspec, artefactos en .knowledge/ y docs/). Corregido 2026-10-18 (review K3): skills mapeadas al sistema multiagente real.*