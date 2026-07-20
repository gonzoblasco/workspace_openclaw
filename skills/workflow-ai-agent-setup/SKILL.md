---
name: "workflow-ai-agent-setup"
description: "Workflow de construcción de agentes de IA: diseño, tools, prompts, RAG, MCP y skill authoring. Para el AI Developer Stack, no para OpenClaw."
---

# Propuesta: workflow-ai-agent-setup

## Contexto

Este workflow NO es para OpenClaw. OpenClaw es un sistema operativo para agentes, no un taller para construirlos. Las skills de construcción de agentes (loops, tools, prompts, RAG, MCP) pertenecen al AI Developer Stack.

## Inspiración

Del AI Developer Stack (gonzoblasco/ai-developer-stack):
- `ai-agents-architect` — loops ReAct/Plan-Execute, memoria, orquestación
- `agent-tool-builder` — tools robustas, JSON schemas, MCP
- `prompt-mastery` — prompting avanzado (CoT, Few-Shot)
- `prompt-engineer` — frameworks RTF, RISEN, RODES
- `rag-expert` — chunking semántico, reranking, hybrid search
- `mcp-builder` — servidores MCP en Python y TypeScript
- `meta-skill-antigravity` — TDD para crear skills
- `writing-great-skills` — principios de Matt Pocock para skills predecibles

## Lo que SÍ absorbe OpenClaw

### `writing-great-skills` → mejora de SKILL.md

Principios clave:
- **Predictibilidad** — la skill debe producir el mismo proceso cada vez
- **Progressive Disclosure** — 3 niveles: metadata (~100 tokens) → SKILL.md (<500 líneas) → resources (on demand)
- **Degrees of Freedom** — ajustar especificidad según fragilidad de la tarea
- **Leading Words** — usar conceptos preentrenados del modelo para anclar comportamientos

### `meta-skill-antigravity` → metodología de creación

- TDD aplicado a skills: test → implement → verify
- Iron Law: "El contexto es un bien público. No lo malgastes."

## Lo que NO absorbe (queda en AI Developer Stack)

- `ai-agents-architect` — loops de agentes
- `agent-tool-builder` — diseño de tools
- `prompt-mastery` / `prompt-engineer` — prompting avanzado
- `rag-expert` — sistemas RAG
- `mcp-builder` — servidores MCP

## Próximos pasos

1. Aprobar propuesta
2. Mejorar SKILL.md de OpenClaw con principios de writing-great-skills
3. Dejar el workflow de AI Agent Setup en el AI Developer Stack como referencia
