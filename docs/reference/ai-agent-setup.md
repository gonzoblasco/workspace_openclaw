---
name: "workflow-ai-agent-setup"
description: "Workflow de referencia para construcción de agentes de IA: diseño, tools, prompts, RAG, MCP y skill authoring. No operativo en OpenClaw."
---

# Workflow: AI Agent Setup

## Propósito
Workflow de referencia. Documenta cómo se construyen agentes de IA, para entender la relación entre el humano y el agente. No es operativo en OpenClaw — las skills de construcción de agentes pertenecen al AI Developer Stack.

## Fases

### 1. Arquitectura del Agente
Diseño del loop de razonamiento (ReAct, Plan-Execute), arquitectura de memoria (corto plazo, largo plazo, episódica), orquestación multi-agente.

### 2. Tools
Diseño de tools robustas con JSON Schemas claros. Principio: el LLM nunca ve el código, solo ve el schema y la descripción. Una tool con documentación clara funciona; una perfectamente implementada con descripción vaga falla.

### 3. Prompting
Prompting avanzado: Chain-of-Thought, Few-Shot, Progressive Disclosure. Los prompts son código — requieren el mismo rigor.

### 4. Optimización de Prompts
Frameworks estructurados: RTF, RISEN, RODES, RACE. Transformar prompts crudos en instrucciones optimizadas.

### 5. RAG
Sistemas de Retrieval-Augmented Generation: chunking semántico, hybrid search (keywords + vectores), reranking. Principio: nunca confiar en retrieval crudo, siempre rerankear.

### 6. MCP
Servidores Model Context Protocol en Python (FastMCP) y TypeScript (MCP SDK). Tool discoverability, error recovery, context management.

### 7. Meta-skill
Metodología TDD para crear skills: test → implement → verify. Progressive disclosure en 3 niveles: metadata (~100 tokens) → SKILL.md (<500 líneas) → resources (on demand).

### 8. Autoría de Skills
Principios de Matt Pocock para skills predecibles: predictibilidad (mismo proceso cada vez), progressive disclosure, degrees of freedom, leading words.

## Outputs
- Documentación de referencia para construir agentes
- Principios de skill authoring aplicables a OpenClaw

## Nota
Este workflow no se ejecuta. Es referencia conceptual para entender cómo funciona la relación humano-agente.
