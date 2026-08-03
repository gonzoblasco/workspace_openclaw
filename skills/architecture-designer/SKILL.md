---
name: "architecture-designer"
description: "Design system architecture, write ADRs, evaluate trade-offs, and produce decision records for technical choices."
metadata:
  version: 1.0.0
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

## Output

### ADR format

Save as `.knowledge/ADRs/NNN-<short-title>.md`:

```markdown
# ADR-001: Use Supabase for auth and database

## Status
Accepted

## Context
We need auth, real-time updates, and managed Postgres for soporteml.

## Options Considered
1. **Supabase** — managed Postgres + auth + realtime
2. **Firebase** — managed NoSQL + auth
3. **Self-hosted Postgres + Keycloak** — full control, more ops

## Decision
Use Supabase.

## Consequences
- Faster setup and built-in auth
- Vendor lock-in to Supabase/Fly/Render
- Need RLS policies for multi-tenant safety
```

### System design doc

For larger systems:

```markdown
# System: <Name>

## Goals
## Actors
## Components
## Data Flow
## Deployment
## Security Boundaries
## Failure Modes
## Open Questions
```

## Workflow

1. **Frame the decision** — what problem are we solving?
2. **List options** — at least 2-3, with pros/cons.
3. **Apply constraints** — team skills, cost, scale, compliance.
4. **Choose** — pick one, explain why.
5. **Document** — write ADR or system design doc.
6. **Review** — get user approval before implementation.

## Research rules

- For pricing, features, or current versions: use `web_search` or `web_fetch`.
- For popularity/maintenance: check GitHub stars, npm downloads, last commit.
- Prefer existing solutions over custom unless there's a strong reason.

## Best practices

- Every non-obvious decision gets an ADR.
- Keep ADRs short: context, options, decision, consequences.
- Revisit ADRs when constraints change.
- Link ADRs from `.knowledge/README.md` or `AGENTS.md`.

## Integration

- Pair with `openspec` to derive implementation specs from architecture.
- Pair with `agent-workflow` for TDD execution.
- Pair with `deploy-agent` to realize deployment decisions.

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `tech-docs/scripts/generate-adr.sh "Titulo"` | Genera un ADR numerado en `docs/adr/` con el formato estandar. Usar en el paso 5 (Document). |
| `tech-docs/scripts/analyze_codebase.py` | Extrae informacion del codebase para informar decisiones arquitectonicas. Usar en el paso 1 (Frame the decision). |
| `product-discovery/scripts/generate-openspec.sh` | Deriva especificacion de implementacion desde la arquitectura. Usar con `openspec`. |
| `engineering-governance/scripts/detect-duplicates.sh` | Verifica que no existan ADRs duplicados o contradictorios. Usar antes de finalizar. |
