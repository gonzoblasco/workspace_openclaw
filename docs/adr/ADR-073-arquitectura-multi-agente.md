# ADR-073 - Transición a Arquitectura de Orquestación Multi-Agente

**Date:** 2026-09-26
**Status:** Accepted
**Context:** El workspace de Kanam OS había crecido hasta convertirse en un "monolito" de skills y scripts. La carga de decenas de definiciones de skills en cada sesión estaba saturando la ventana de contexto del modelo, generando ruido operativo, aumentando la probabilidad de alucinaciones y ralentizando la respuesta.

## Decision

Migrar de un único agente generalista a un sistema de **Orquestación Multi-Agente** basado en roles especializados y workspaces aislados.

### 1. Estructura de Agentes
Se definen cinco roles operativos con sus propios entornos de ejecución:

| Agente | Responsabilidad | Ubicación |
|---|---|---|
| **Kanam CORE** | Orquestación, Memoria Global, Gobierno y Estrategia | `/workspace/` (Raíz) |
| **Kanam DEV** | Ingeniería de Software, Producto, OpenSpec, TDD | `/workspace/agents/kanam-dev/` |
| **Kanam OPS** | Infraestructura, Gateway, Seguridad, Tooling | `/workspace/agents/kanam-ops/` |
| **Kanam MIND** | Conocimiento, Research, Vida, Aprendizaje | `/workspace/agents/kanam-mind/` |
| **Kanam STUDIO** | Comunicación, Redacción, Marca Personal, OSS | `/workspace/agents/kanam-studio/` |

### 2. Mecanismo de Despacho (Orquestación)
- El **Kanam CORE** actúa como el punto de entrada único.
- Se transforma el `SKILLS-INDEX.md` en un **Mapa de Orquestación**.
- El CORE utiliza el `skill-router` para identificar la capacidad requerida y delega la tarea al agente especialista mediante `sessions_spawn` o `sessions_send`.

### 3. Gestión de Memoria y Contexto
- **Contexto Aislado:** Cada agente carga solo las skills y scripts necesarios para su rol, reduciendo drásticamente el ruido en el prompt.
- **Inconsciente Colectivo:** Se mantiene la base de datos de vectores (`memory.db`) como fuente de verdad compartida. Los agentes recuperan fragmentos específicos de memoria vía RAG, eliminando la necesidad de pasar contextos masivos entre sesiones.

## Consequences

### Positive
- **Eficiencia de Tokens:** Reducción significativa del consumo de tokens de bootstrap.
- **Precisión:** Mayor enfoque del modelo al operar en un dominio restringido.
- **Escalabilidad:** Permite agregar nuevos especialistas (ej. `Kanam STORIES`) sin afectar la estabilidad del núcleo.
- **Versionado:** Al residir los agentes en `/workspace/agents/`, todas sus skills y scripts quedan trackeados por Git.

### Negative
- **Latencia de Despacho:** El proceso de delegación añade una capa de comunicación entre el CORE y el Especialista.
- **Complejidad de Gestión:** Requiere mantener la coherencia del mapa de orquestación cuando se añaden o eliminan skills.

## Notes
- Este patrón se alinea con la arquitectura de "Modular Monolith" y "Multi-Agent Reference Architecture" para optimizar la ventana de contexto de LLMs.
- La migración incluyó una limpieza de skills obsoletas (`complexity-driven-pipeline`, etc.) para asegurar que el nuevo sistema arranque sin deuda técnica.
