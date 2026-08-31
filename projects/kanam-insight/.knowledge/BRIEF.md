# BRIEF: kanam-insight

## Qué es

El motor de inteligencia transversal del workspace. Una capa de razonamiento que cruza proyectos, detecta patrones, mide deuda técnica y propone acciones. No es un chat: es un sistema que trabaja sobre los `.knowledge/` y `ADRs` de todos los proyectos para hacer emerger señales que la vista humana pierde.

## Por qué existe

Gonzo tiene ~12 proyectos activos en el workspace. Cada uno tiene su propio `.knowledge/` con ADRs, HANDOFF, STATUS, y decisiones. El problema: nadie cruza esa información. Patrones viven y mueren en silos. Un fix de a11y en `a11y-fixer` que se podría aplicar a `accessible-ui` queda enterrado. Un ADR obsoleto en `kanam-mind` queda activo sin que nadie lo note.

`kanam-insight` es la solución: un sistema local que lee todos los `.knowledge/`, construye una vista unificada, y entrega tres productos:

1. **Pattern Radar:** cruza decisiones y soluciones entre proyectos. Dice: "resolviste esto en X con Y, ¿lo aplicamos a Z?".
2. **Handoff Synthesizer:** al iniciar un proyecto, sintetiza el estado actual contra el `ROADMAP.md` y prioriza el día.
3. **Debt Detector:** identifica ADRs obsoletos, decisiones que fueron parches, y oportunidades de refactor con el stack actual.

## Stack

- TypeScript (Node CLI + librerías)
- Ollama (LLM local: `glm-5.3-flash:cloud`)
- LanceDB o SQLite-vec (embeddings + búsqueda semántica local)
- Bun (runtime + tests)
- Biome (lint)
- Vitest (tests)

## Estructura

```
projects/kanam-insight/
├── .knowledge/          ← BRIEF, HANDOFF, STATUS, ADRs
├── src/
│   ├── index.ts         ← CLI entrypoint
│   ├── scanners/        ← lectores de .knowledge/, ADRs, código
│   ├── analyzers/       ← lógica de pattern/debt/handoff
│   ├── llm/             ← cliente Ollama, prompts
│   └── db/              ← índice local (SQLite-vec)
├── tests/
└── package.json
```

## Diferenciador

No es un dashboard: es un motor de razonamiento. La diferencia con un grep/RAG básico es la **memoria institucional**: recuerda qué dijo en el pasado sobre cada proyecto y compara con el presente. Eso permite detectar contradicciones y obsolescencia, no solo similitud.

## Público

Gonzo (uso primario). CLI local-first, ejecutable desde el workspace.

## Estado

v0.1.0 — Spec v1 en construcción.
