---
name: "campaign-plan"
metadata:
  category: "Marketing"
  tags:
    - campana
    - marketing
    - lanzamiento
    - planificacion
description: "Generar brief completo de campaña de marketing: objetivos, audiencia, mensajes, canales, calendario de contenido y métricas de éxito."
user-invocable: false
---

# Workflow: Campaign Plan

## Propósito

Generar un brief completo de campaña de marketing con objetivos, audiencia, mensajes, estrategia de canales, calendario de contenido y métricas de éxito.

## Cuándo usarlo

- Planificar un product launch
- Campaña de lead generation
- Campaña de awareness
- Traducir un objetivo de marketing en un plan ejecutable

## Fases

### 1. Inputs
- Campaign goal (signups, awareness, leads, re-engagement)
- Target audience (demographics, roles, pain points)
- Timeline and budget
- Additional context (product, differentiators, previous campaigns)

### 2. Campaign Brief

1. **Overview** — name, one-sentence summary, primary objective (SMART)
2. **Target Audience** — primary segment, pain points, channels, buying stage
3. **Key Messages** — core message, 3-4 supporting, proof points
4. **Channel Strategy** — owned, earned, paid con justificación
5. **Content Calendar** — week-by-week con milestones y dependencias
6. **Content Pieces** — assets needed con prioridad y timeline
7. **Success Metrics** — primary KPI, secondary KPIs, tracking method
8. **Budget Allocation** — breakdown by channel (if provided)
9. **Risks & Mitigations** — 2-3 risks con estrategia
10. **Next Steps** — action items, approvals needed

## Outputs

- Campaign brief completo
- Content calendar semanal
- Content assets list
- KPI targets and tracking plan

## Helper Scripts

Scripts en `skills/campaign-plan/scripts/`:

| Script | Uso |
|---|---|
| `content-calendar-generator.sh [--output file]` | Genera un calendario de contenido Markdown a partir de prompts interactivos. Usar en Fase 2, punto 5 (Content Calendar). |

## Related Skills

- [Copy Editing](../copy-editing): Para editar copy de la campaña
- [Product Discovery](../product-discovery): Para definir producto antes de la campaña
