# BRIEF.md — Copilot Workflow Kit

> Phase 0 — Idea Intake
> Fecha: 2026-07-15

## Raw Idea

Un kit de skills reutilizables para desarrollo asistido por IA. Son archivos `SKILL.md` que definen comportamientos de agente: cómo commitear, cómo revisar un PR, cómo orquestar tareas dentro de un epic, cómo auditar seguridad.

Actualmente existe como `projects/--copilot-skills/` — una colección de 11 skills en `.agents/skills/` diseñados originalmente para Claude Code y Google Antigravity.

## Estado actual

- 11 skills en `.agents/skills/`:
  - **Genéricos (7):** commit, commit-formatter, pr, new-task, refactor, doc-writer, generic-docs-sync
  - **Propios (4):** copilot (orquestador), close-epic, pr-review, security-audit
- README.md con instrucciones de uso
- SKILL.md con índice completo
- CLAUDE.md con template de proyecto
- `.knowledge/` con ejemplos de análisis
- `.agents/antigravity-bridge.md` para integración con Antigravity IDE
- Sin repo en GitHub (solo local)
- Sin definición de producto

## Contexto

- Es un proyecto de Gonzo, categoría "proyectos de soporte"
- Originalmente para Claude Code, pero el patrón es universal para cualquier agente de IA
- OpenClaw ya tiene skills en el workspace (product-orchestrator, web-app-builder, etc.) — este kit es complementario, opera a nivel de código/task, no de producto

## Preguntas a resolver en Phase 1

1. ¿Es un producto para vender (template pago, CLI) o open source tool?
2. ¿Compite con/claude-code más skills nativos o es complementario?
3. ¿El público es devs individuales o equipos/startups?
4. ¿Tiene sentido como CLI (`npx create-copilot-kit`) o como template de GitHub?
