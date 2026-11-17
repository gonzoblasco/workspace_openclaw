---
pageType: claims
topic: workspace
owner: AGENTS.md / ADR-064 / ADR-083
updatedAt: 2026-11-16T23:45:00-03:00
claims:
  - id: workspace.source-of-truth
    text: "memory.db es la fuente de verdad de la memoria; los .md son vistas regenerables."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:45:00-03:00
    evidence:
      - kind: file
        path: AGENTS.md
        expect: "memory/memory.db` es la fuente de verdad"

  - id: workspace.core-does-not-implement
    text: "El CORE orquesta, no implementa: escribir codigo, deployar o redactar es de DEV, OPS, MIND y STUDIO (ADR-083)."
    status: active
    confidence: 0.9
    updatedAt: 2026-11-16T23:45:00-03:00
    evidence:
      - kind: file
        path: AGENTS.md
        expect: "el CORE orquesta, no implementa"

  - id: workspace.one-machine
    text: "Solo hay una maquina: la Mac Mini corre el gateway y el workspace vive ahi (ADR-073). No hay pull de otras maquinas."
    status: active
    confidence: 0.9
    updatedAt: 2026-11-16T23:45:00-03:00
    evidence:
      - kind: file
        path: AGENTS.md
        expect: "Máquinas:** solo la **Mac Mini**"

  - id: workspace.claims-format-lives-in-git
    text: "La capa de claims vive en docs/claims/ dentro del repo, no en un vault fuera de git."
    status: active
    confidence: 0.9
    updatedAt: 2026-11-16T23:45:00-03:00
    evidence:
      - kind: file
        path: docs/claims/README.md
        expect: "A **claim** is a single asserted fact"
      - kind: file
        path: scripts/check-claims.py

  - id: workspace.wiki-detectors-work
    text: "Los detectores de memory-wiki funcionan: verificados en negativo el 2026-11-16 con una entity sonda que cada report nombro y que se limpio al removerla. Lo que faltaba era sustrato de claims, no el plugin."
    status: active
    confidence: 0.9
    updatedAt: 2026-11-16T23:45:00-03:00
    evidence:
      - kind: file
        path: docs/ecosystem/memory-wiki-capa-analitica.md
        expect: "Detectores ejercitados con una sonda deliberada"

  - id: workspace.wiki-claims-layer-was-empty
    text: "Al retirar memory-wiki el vault tenia 86 fuentes ingestadas y una sola entity con 4 claims, por eso todos los reports daban cero."
    status: active
    confidence: 0.9
    updatedAt: 2026-11-16T23:45:00-03:00
    evidence:
      - kind: file
        path: docs/claims/README.md
        expect: "86 ingested sources, **one** entity with 4 claims"

  - id: workspace.model-triple-key-was-stale
    text: "Al 2026-11-16 la clave settings model.triple declaraba main/defaults minimax-m3.1-flash:cloud, valor superseded por ADR-107: doce dias de drift entre tres claves que debian ser el mismo dato. Corregido el mismo dia."
    status: retracted
    confidence: 0.9
    updatedAt: 2026-11-16T23:55:00-03:00
    evidence:
      - kind: file
        path: docs/claims/workspace.md
        expect: "doce dias de drift"

  - id: workspace.model-keys-aligned
    text: "La tabla settings guarda la asignacion de modelos bajo una sola clave, model_by_agent: los alias model_triple y model.triple fueron borrados el 2026-11-17."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-17T00:12:00-03:00
    evidence:
      - kind: settings
        key: model_by_agent
        expect: "main/defaults deepseek-v4.1-flash:cloud"
      - kind: file
        path: scripts/check-settings-aliases.py
        expect: "no alias key exists in"
      - kind: file
        path: scripts/managed-blocks.py
        expect: "UNA sola clave"

  - id: workspace.settings-write-path-is-single
    text: "managed-blocks.py set escribe solo la clave canonica y acepta un alias unicamente como nombre de entrada; retire-aliases borra las copias y se frena si un alias difiere del canonico."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-17T00:12:00-03:00
    evidence:
      - kind: file
        path: scripts/managed-blocks.py
        expect: "def cmd_retire_aliases"
      - kind: file
        path: scripts/managed-blocks.py
        expect: "UNA sola clave (2026-11-17)"
---

# Workspace

Claims sobre como funciona el workspace mismo. Este archivo es el que mas cerca esta de la
clase de bug que motivo ADR-064: "el doc dice X, el runtime hace Y".

## Deuda cerrada el 2026-11-17

La historia, completa, porque la trampa se repite:

1. **2026-11-04, dos veces en un día:** la DB guardaba la asignación de modelos bajo tres
   claves (`model_by_agent`, `model_triple`, `model.triple`). Cada sesión que "corregía" una
   dejaba las otras con el valor viejo (primero `glm4:9b`, después planner/studio).
2. **Hasta el 2026-11-16:** `model.triple` volvió a quedar con `minimax-m3.1-flash` mientras
   ADR-107 ya decía `deepseek`. Doce días de drift, invisibles.
3. **2026-11-16:** se alinearon las tres claves y se agregó `check-settings-aliases.py`, que
   las vigilaba. Eso trataba la copia como normal: tres valores iguales siguen siendo tres
   dueños.
4. **2026-11-17:** se cerró de raíz. `managed-blocks.py set` escribe **una sola** clave y
   acepta un alias solo como nombre de entrada; `retire-aliases` borra las copias y se frena
   si un alias difiere del canónico; `seed` nunca crea un alias; el gate exige que **no
   exista** ninguna copia.

Verificado en negativo: sembrar un `model.triple` a mano hace fallar el gate, y `retire-aliases`
lo limpia. Un `set` después del retiro deja la DB en 10 claves y el gate en verde.

Queda una sola clave: `model_by_agent`, la que lee el bloque de `AGENTS.md`.
