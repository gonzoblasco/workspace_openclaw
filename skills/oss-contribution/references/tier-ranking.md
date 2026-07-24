# Tier Ranking — OSS Contribution Reference

Clasificación de repositorios objetivo para contribuciones estratégicas.

## Tier System

### Tier 0 — High Impact, High Visibility
Repos con gran audiencia, PRs revisados rigurosamente.

- **shadcn/ui** — Componentes UI, audiencia masiva
- **TanStack (react-query, react-router, table)** — Librerías core del stack
- **Vercel (next.js, ai-sdk)** — Framework principal
- **Biome** — Toolchain del stack

**Estrategia:** PRs pequeños y precisos. Descripción humana, sin trazas de automatización. Bugs concretos sin competencia → PR rápido.

### Tier 1 — Strategic Value
Repos que usamos activamente o complementan el stack.

- **Supabase** — Backend principal
- **Radix UI / Ariakit** — Headless UI primitives
- **React Aria** — Accesibilidad
- **Playwright** — Testing E2E
- **Vitest** — Testing unitario

**Estrategia:** Features pequeños, mejoras de DX, fixes de accesibilidad.

### Tier 2 — Community Building
Repos donde construir presencia sin presión de review.

- **create-stack-next** — Proyecto propio, control total
- **workflow-kit** — Proyecto propio
- **Repos de accesibilidad** (axe-core, WAI-ARIA practices)
- **Documentación de frameworks**

**Estrategia:** Contribuciones regulares, issues, reviews de PRs ajenos.

## Opportunity Detection

```bash
# Find issues without PRs
gh issue list --repo <owner/repo> --label "good first issue" --json number,title,updatedAt

# Find issues with reproduction but no fix
gh issue list --repo <owner/repo> --state open --json number,title,body,comments

# Check for competing PRs
gh pr list --repo <owner/repo> --state open --json number,title,labels
```

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [PR Checklist](./pr-checklist.md) — Checklist para PRs
- [Community Guidelines](./community-guidelines.md) — Reglas de interacción
