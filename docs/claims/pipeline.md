---
pageType: claims
topic: pipeline
owner: ADR-077 / ADR-088 / ADR-089
updatedAt: 2026-11-16T23:40:00-03:00
claims:
  - id: pipeline.ab-writer-model
    text: "En pipeline_ab el agente A (escribe y corrige) corre gpt-oss:120b-cloud."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:40:00-03:00
    evidence:
      - kind: settings
        key: model_pipeline_a
        expect: "gpt-oss:120b-cloud"
      - kind: managed-block
        key: pipeline-ab
        expect: "A escribe y corrige** con `gpt-oss:120b-cloud`"

  - id: pipeline.ab-reviewer-model
    text: "En pipeline_ab el agente B (solo revisa) corre deepseek-v4.1-flash:cloud."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:40:00-03:00
    evidence:
      - kind: settings
        key: model_pipeline_b
        expect: "deepseek-v4.1-flash:cloud"
      - kind: managed-block
        key: pipeline-ab
        expect: "B solo revisa** con `deepseek-v4.1-flash:cloud`"

  - id: pipeline.abc-tests-model
    text: "En pipeline_abc el agente C (red de tests de regresion) corre minimax-m3.1-flash:cloud."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:40:00-03:00
    evidence:
      - kind: settings
        key: model_pipeline_c
        expect: "minimax-m3.1-flash:cloud"
      - kind: managed-block
        key: pipeline-abc
        expect: "C escribe la red de tests de regresión** con `minimax-m3.1-flash:cloud`"

  - id: pipeline.prefilter-model
    text: "El pre-filtro del pipeline corre gemma4:cloud y no autoriza solo: lo que toca logica o semantica pasa siempre por B."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:40:00-03:00
    evidence:
      - kind: settings
        key: model_pipeline_prefilter
        expect: "gemma4:cloud"
      - kind: managed-block
        key: pipeline-ab
        expect: "NO autoriza solo"

  - id: pipeline.asymmetry-principle
    text: "La decision vigente de ADR-077 es la asimetria: el revisor ve mas que el ejecutor, con modelos distintos por rol."
    status: active
    confidence: 0.9
    updatedAt: 2026-11-16T23:40:00-03:00
    evidence:
      - kind: adr
        path: docs/adr/ADR-077-pipeline-ab-asimetrico.md
        expect: "el revisor ve más que el ejecutor"

  - id: pipeline.enforcement-gate
    text: "El pipeline tiene un gate de enforcement ejecutable: scripts/check-pipeline-enforcement.py."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:40:00-03:00
    evidence:
      - kind: file
        path: scripts/check-pipeline-enforcement.py
---

# Pipeline A/B/C

El pipeline es la parte del workspace donde la "contradiccion entre lo documentado y lo que corre"
duele mas, porque define quien escribe y quien revisa. `scripts/check-pipeline-enforcement.py`
cubre el codigo; estos claims cubren **que modelo hace que**.

Nota: ADR-077 dice explicito que los modelos concretos del texto son historicos y la asignacion
vigente vive en ADR-090. El claim `pipeline.asymmetry-principle` apunta a la decision, no a los
modelos, justamente para no repetir esa trampa.
