---
pageType: claims
topic: models
owner: ADR-090
updatedAt: 2026-11-16T23:35:00-03:00
claims:
  - id: models.core-primary
    text: "El rol main (CORE) corre deepseek-v4.1-flash:cloud como primario."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:35:00-03:00
    evidence:
      - kind: settings
        key: model_by_agent
        expect: "main/defaults deepseek-v4.1-flash:cloud"
      - kind: adr
        path: docs/adr/ADR-090-pensamiento-nivel-configuracion.md
        expect: "deepseek-v4.1-flash:cloud"

  - id: models.dev-primary
    text: "El rol kanam-dev corre gpt-oss:120b-cloud como primario."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:35:00-03:00
    evidence:
      - kind: settings
        key: model_by_agent
        expect: "dev gpt-oss:120b-cloud"
      - kind: managed-block
        key: model-operativo
        expect: "dev gpt-oss:120b-cloud"

  - id: models.ops-primary
    text: "El rol kanam-ops corre gpt-oss:120b-cloud como primario."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:35:00-03:00
    evidence:
      - kind: settings
        key: model_by_agent
        expect: "ops gpt-oss:120b-cloud"
      - kind: managed-block
        key: model-operativo
        expect: "ops gpt-oss:120b-cloud"

  - id: models.auditor-primary
    text: "El rol kanam-auditor corre deepseek-v4.1-flash:cloud como primario."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:35:00-03:00
    evidence:
      - kind: settings
        key: model_by_agent
        expect: "auditor deepseek-v4.1-flash:cloud"
      - kind: managed-block
        key: model-operativo
        expect: "auditor deepseek-v4.1-flash:cloud"

  - id: models.critic-primary
    text: "El rol kanam-critic corre gpt-oss:120b-cloud como primario."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:35:00-03:00
    evidence:
      - kind: settings
        key: model_by_agent
        expect: "critic gpt-oss:120b-cloud"
      - kind: managed-block
        key: model-operativo
        expect: "critic gpt-oss:120b-cloud"

  - id: models.planner-primary
    text: "El rol kanam-planner corre gpt-oss:120b-cloud como primario, con gemma4:12b-mlx local como fallback."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:35:00-03:00
    evidence:
      - kind: settings
        key: model_by_agent
        expect: "planner gpt-oss:120b-cloud (fallback gemma4:12b-mlx local)"
      - kind: managed-block
        key: model-operativo
        expect: "planner gpt-oss:120b-cloud (fallback gemma4:12b-mlx local)"

  - id: models.mind-primary
    text: "El rol kanam-mind corre deepseek-v4.1-flash:cloud como primario."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:35:00-03:00
    evidence:
      - kind: settings
        key: model_by_agent
        expect: "mind deepseek-v4.1-flash:cloud"
      - kind: managed-block
        key: model-operativo
        expect: "mind deepseek-v4.1-flash:cloud"

  - id: models.studio-primary
    text: "El rol kanam-studio corre deepseek-v4.1-flash:cloud como primario, con gemma4:12b-mlx local como fallback."
    status: active
    confidence: 0.95
    updatedAt: 2026-11-16T23:35:00-03:00
    evidence:
      - kind: settings
        key: model_by_agent
        expect: "studio deepseek-v4.1-flash:cloud (fallback gemma4:12b-mlx local)"
      - kind: managed-block
        key: model-operativo
        expect: "studio deepseek-v4.1-flash:cloud (fallback gemma4:12b-mlx local)"

  - id: models.thinking-execution
    text: "Los cinco roles de ejecucion (main, dev, ops, mind, studio) corren thinking off."
    status: active
    confidence: 0.9
    updatedAt: 2026-11-16T23:35:00-03:00
    evidence:
      - kind: adr
        path: docs/adr/ADR-090-pensamiento-nivel-configuracion.md
        expect: "off` explícito para los cinco de ejecución"

  - id: models.thinking-judgment
    text: "Los tres roles de juicio (critic, auditor, planner) corren thinking low."
    status: active
    confidence: 0.9
    updatedAt: 2026-11-16T23:35:00-03:00
    evidence:
      - kind: adr
        path: docs/adr/ADR-090-pensamiento-nivel-configuracion.md
        expect: "`low` para los tres de juicio: critic, auditor, planner."
---

# Models

Los valores repetidos viven en la tabla `settings` de `memory.db` (bloques managed) y se
propagan a `AGENTS.md`. Este archivo es el chequeo: si un claim falla, la `settings`, el bloque
managed y `ADR-090` dejaron de decir lo mismo.

**Ojo:** la misma tabla vive bajo tres claves (`model_by_agent`, `model_triple`, `model.triple`).
Al 2026-11-16 `model.triple` **no** es un espejo: dice `main/defaults minimax-m3.1-flash:cloud`,
el valor superseded por ADR-107. Ver `docs/claims/workspace.md` para el estado de esa deuda.
