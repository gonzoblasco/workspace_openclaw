# EVALUATION.md — Copilot Workflow Kit

> Phase 1 — Product Evaluation
> Fecha: 2026-07-15

## Problem

Los desarrolladores que usan IA para codificar (Claude Code, Codex, Cursor, OpenClaw) repiten los mismos workflows una y otra vez: commitear con formato, revisar PRs, auditar seguridad, cerrar epics. No hay un kit portable y agnóstico que funcione en cualquier agente/herramienta.

## Audience

- **Devs individuales** que usan Claude Code, Codex, Cursor, OpenClaw
- **Equipos chicos** que quieren estandarizar su workflow con IA
- **Power users de AI coding agents** que ya escriben prompts custom
- Tamaño: nicho en crecimiento. El repo addyosmani/agent-skills tiene 78K stars, lo que indica DEMANDA real.

## Existing solutions

| Proyecto | Stars | Approach | Diferenciación |
|---|---|---|---|
| addyosmani/agent-skills | 78K | Skills de producción para Claude Code | Masivo, pero genérico. Skills "one-size-fits-all" |
| agentkit-cli | 1 | CLI tipo create-vite | Solo scaffold, no incluye skills |
| ood-labs/agent-workflow-bundle | 7 | Bundle portable | PowerShell, no portable real |
| ClaudSkills.com | — | Registry de SKILL.md | Solo listado, no kit |
| agentvoy | 7 | Multi-framework | Muy ambicioso, poco enfocado |

**Gap:** Nadie ofrece un **kit portable y agnóstico** que:
- Funcione en Claude Code, Codex, Cursor, OpenClaw, y cualquier agente que lea SKILL.md
- Incluya un **workflow completo** (Pre-Flight + Gates), no skills sueltos
- Sea **parametrizable** ({{FILL}}) para adaptarse a cada proyecto
- Venga con un **CLI** para instalarlo en un proyecto con un comando

## Differentiation

1. **Agnóstico de agente** — no solo Claude Code, también OpenClaw, Codex, Cursor
2. **Workflow completo** — no skills sueltos, sino un ciclo orquestado (Pre-Flight + 5 Gates)
3. **Parametrizable** — los {{FILL}} permiten adaptar a cualquier proyecto sin editar los skills
4. **CLI de instalación** — `npx create-copilot-kit` o `npx @kanam/copilot-kit init`
5. **Security-first** — el skill security-audit es único, nadie más lo tiene

## Revenue model

**Open source + GitHub Sponsors.** No es un producto para vender directamente. Pero:
- Es **portfolio piece** que muestra capacidad técnica y metodológica
- Puede generar **reconocimiento en la comunidad** (como addyosmani/agent-skills)
- **Diferenciador en entrevistas:** "creé un workflow kit para AI-assisted development usado por X personas"

## Technical feasibility

- **Ya existe** — los 11 skills están escritos y funcionando
- **Lo que falta:** CLI de instalación, docs pulidas, branding, repo público
- **Stack:** solo Markdown + shell scripts. No requiere build tooling complejo
- **Complejidad:** baja (es contenido, no código)
- **Tiempo estimado MVP:** 2-3 días

## Strategic fit

- **Fit con objetivos de Gonzo:** ALTO — es exactamente el tipo de proyecto que muestra metodología + open source + utilidad real
- **Fit con ecosistema Kanam:** ALTO — los skills se integran naturalmente con OpenClaw
- **Sinergia con create-stack-next:** podría incluirse como template opcional en el scaffold
- **Opportunity cost:** bajo — son 2-3 días de contenido + CLI, no compite con SoporteML v2

## Risks

| Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|
| addyosmani/agent-skills ya domina el espacio | Medio | Alta | Diferenciarse en workflow completo + agnosticismo + security-audit |
| Poca adopción | Medio | Media | Apuntar a nicho OpenClaw + comunidad dev tooling |
| Los skills se vuelven obsoletos por cambios en los agentes | Bajo | Media | SKILL.md es markdown, no depende de APIs |

## Verdict: 🟢 GO

### Recommendation
Convertir `--copilot-skills` en un producto open source llamado **Kanam Workflow Kit** (o similar). Incluye:
1. Los 11 skills existentes (refinados y documentados)
2. Un CLI de instalación (`npx @kanam/workflow-kit init`)
3. Docs de uso y adaptación
4. Compatibilidad explícita con Claude Code, Codex, Cursor, y OpenClaw

No compite con SoporteML v2 porque es contenido + CLI, no código complejo. 2-3 días de trabajo.
