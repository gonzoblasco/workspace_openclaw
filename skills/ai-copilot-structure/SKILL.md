---
name: "ai-copilot-structure"
description: "Generar estructura documentada de productos con OpenSpec, aplicable a cualquier proyecto. Documenta decisiones técnicas y de producto como fuente de verdad."
---

# AI Copilot Structure

**Purpose:** Generar estructura documentada de productos con OpenSpec, aplicable a cualquier proyecto (no solo UmbraWriter). Documenta decisiones técnicas y de producto como fuente de verdad.

**Version:** 1.0

**Rationale:** El nombre anterior era muy específico para un solo producto. Renombrar a `ai-copilot-structure` permite aplicar el mismo patrón de documentación de estructura a cualquier proyecto (BrainWeb, SoporteML v2, KanamAI, etc.).

**Workflow:**
1. Analizar requirements del producto
2. Crear structure docs con OpenSpec (BRIEF, DEFINITION, EVALUATION, ROADMAP)
3. Definir arquitectura técnica y decisiones clave
4. Establecer base para ADRs
5. Integrar con pipeline de sdd-brownfield

**Integration Points:**
- `product-orchestrator`: Fase definition
- `sdd-brownfield`: Specs as-built source
- `adr-framework`: Feed para ADRs iniciales
