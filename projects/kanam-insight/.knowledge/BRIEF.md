# BRIEF: kanam-insight

## Qué es

El motor de inteligencia transversal del workspace. Una capa de razonamiento que cruza proyectos, detecta patrones, mide deuda técnica y propone acciones. No es un chat: es un sistema que trabaja sobre los `.knowledge/` y `ADRs` de todos los proyectos para hacer emerger señales que la vista humana pierde.

## Por qué existe

Gonzo tiene ~12 proyectos activos en el workspace. Cada uno tiene su propio `.knowledge/` con ADRs, HANDOFF, STATUS, y decisiones. El problema: nadie cruza esa información. Patrones viven y mueren en silos. Un fix de a11y en `a11y-fixer` que se podría aplicar a `accessible-ui` queda enterrado. Un ADR obsoleto en `kanam-mind` queda activo sin que nadie lo note.

`kanam-insight` es la solución: un sistema local que lee todos los `.knowledge/`, construye una vista unificada, y entrega tres productos:

1. **Pattern Radar:** cruza decisiones y soluciones entre proyectos. Dice: "resolviste esto en X con Y, ¿lo aplicamos a Z?".
2. **Handoff Synthesizer:** al iniciar un proyecto, sintetiza el estado actual contra el `ROADMAP.md` y prioriza el día.
3. **Debt Detector:** identifica ADRs obsoletos, decisiones que fueron parches, y oportunidades de refactor con el stack actual.

## Stack (actualizado 2026-09-24, ver ADR-063)

- **Python**, reusando el `venv` de `langchain-starter`
- LangChain + ChromaDB (colección propia `insight_knowledge`)
- Ollama local: embeddings `qwen3-embedding:0.6b`, LLM `gemma4:cloud`
- Sin framework de tests todavía (deuda)

> **Cambio de stack (2026-09-24):** el spec original (2026-08-30) pedía TypeScript + Bun + SQLite-vec. Ese spec quedó **anterior** a la construcción de `langchain-starter` (2026-09-22), que ya resuelve ingesta, chunking, embeddings y retrieval. Se cambió a Python para reusar esa capacidad en lugar de reconstruirla en otro lenguaje. Razonamiento completo en **ADR-063**.

## Alcance de la primera versión

Solo `.knowledge/` de los proyectos (122 archivos, 24 proyectos). `docs/` y `memory/` quedan afuera de esta fase: los dailies son ruido para el retrieval (fechados, mezclan temas) y las entrevistas no aportan al cruce entre proyectos.

## Estructura

```
projects/kanam-insight/
├── .knowledge/           ← BRIEF, HANDOFF, STATUS
├── scripts/
│   ├── scan.py           ← scanner de .knowledge/ (stdlib, sin deps)
│   ├── index.py          ← indexado (chunking semántico -> Chroma)
│   └── radar.py          ← Pattern Radar + búsqueda con fuentes
├── config/chroma_db/     ← índice local (colección insight_knowledge)
└── README.md
```

## Diferenciador

No es un dashboard: es un motor de razonamiento. La diferencia con un grep/RAG básico es la **memoria institucional**: recuerda qué dijo en el pasado sobre cada proyecto y compara con el presente. Eso permite detectar contradicciones y obsolescencia, no solo similitud.

## Público

Gonzo (uso primario). CLI local-first, ejecutable desde el workspace.

## Estado

v0.1.0 - **los tres pilares operativos**, con 32 tests en verde.

| Pieza | Estado |
|---|---|
| Scanner (`scan.py`) | 3 fuentes: proyectos + `docs/` + `skills/` (442 archivos) |
| Indice (`index.py`) | 2557 vectores en `insight_knowledge` |
| Pattern Radar (`radar.py`) | cruce semantico entre proyectos + busqueda con citas |
| Debt Detector (`debt.py`) | 26 proyectos; deuda estructural y refs rotas |
| Handoff Synthesizer (`handoff.py`) | 26 proyectos; estado + desalineacion con el ROADMAP |

**Deuda registrada:** la ingesta es completa (`--reset` rearma todo), no incremental. Con 442 archivos tarda unos minutos; conviene incrementarla cuando el corpus crezca.

## Los tres pilares y su mecanismo real

Un hallazgo del ADR-062 aplica directo: *"el SQL estructurado sigue siendo la puerta principal; los vectores sirven para el caso donde no se recuerda la palabra exacta"*. Traducido a los tres pilares:

| Pilar | Mecanismo | Por qué |
|---|---|---|
| **Pattern Radar** | semántico (vectores + LLM) | El cruce entre proyectos exige encontrar lo mismo dicho con otras palabras |
| **Debt Detector** | estructural | ADR obsoleto = comparar fechas y estados, no similitud |
| **Handoff Synthesizer** | estructural | Estado real vs ROADMAP = comparar, no buscar |

Usar RAG para los dos últimos sería usar un martillo para atornillar.
