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

  - id: workspace.model-triple-key-is-stale
    text: "La clave settings model.triple no es espejo de model_by_agent: declara main/defaults minimax-m3.1-flash:cloud, valor superseded por ADR-107."
    status: active
    confidence: 0.85
    updatedAt: 2026-11-16T23:45:00-03:00
    evidence:
      - kind: settings
        key: model.triple
        expect: "main/defaults minimax-m3.1-flash:cloud"
      - kind: settings
        key: model_by_agent
        expect: "main/defaults deepseek-v4.1-flash:cloud"
---

# Workspace

Claims sobre como funciona el workspace mismo. Este archivo es el que mas cerca esta de la
clase de bug que motivo ADR-064: "el doc dice X, el runtime hace Y".

## Deuda detectada el 2026-11-16

`workspace.model-triple-key-is-stale` no es un claim de politica: es una **observacion**
deliberada, con evidencia de los dos lados, para que deje de ser invisible. ADR-090 dice
que "la misma tabla vive bajo tres claves y corregir solo las conocidas deja una copia viva
del valor viejo". Al 2026-11-16 eso sigue pasando: `model.triple` conserva `minimax-m3.1-flash`.

Ese claim es **activo** porque describe el estado real. Cuando se corrija la clave, el claim
pasa a `retracted` y se agrega uno nuevo que diga que las tres claves coinciden.
