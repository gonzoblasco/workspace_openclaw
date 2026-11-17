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
    text: "Las tres claves de settings model_by_agent, model_triple y model.triple declaran el mismo valor, deepseek-v4.1-flash:cloud como primario de main/defaults."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:55:00-03:00
    evidence:
      - kind: settings
        key: model.triple
        expect: "main/defaults deepseek-v4.1-flash:cloud"
      - kind: settings
        key: model_triple
        expect: "main/defaults deepseek-v4.1-flash:cloud"
      - kind: settings
        key: model_by_agent
        expect: "main/defaults deepseek-v4.1-flash:cloud"
      - kind: file
        path: scripts/check-settings-aliases.py
        expect: "ALIAS_GROUPS"
---

# Workspace

Claims sobre como funciona el workspace mismo. Este archivo es el que mas cerca esta de la
clase de bug que motivo ADR-064: "el doc dice X, el runtime hace Y".

## Deuda cerrada el 2026-11-16

ADR-090 dice que "la misma tabla vive bajo tres claves y corregir solo las conocidas deja una
copia viva del valor viejo". Paso dos veces el 2026-11-04, y `model.triple` volvio a quedar
con `main/defaults minimax-m3.1-flash:cloud` mientras las otras dos decian `deepseek` desde
ADR-107. Doce dias de drift, invisibles hasta que el claim layer lo miro.

Cerrado con `scripts/check-settings-aliases.py`: declara el grupo de alias, `--fix` copia el
canonico (`model_by_agent`, la clave que lee el bloque de AGENTS.md) en los demas, y el
pre-commit lo corre siempre. `workspace.model-triple-key-was-stale` queda `retracted` como
historia; `workspace.model-keys-aligned` dice el estado de hoy.

Lo correcto a futuro es **no** tener tres claves - el script hace visible la copia, no la
elimina. Borrar `model.triple` y `model_triple` y dejar solo `model_by_agent` es la decision
que falta, y toca el esquema de `settings`, no un valor.
