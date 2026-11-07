---
name: "openspec-pattern"
description: "Establishes the intent contract (OpenSpec) to prevent scope creep and technical debt. Use when a feature needs a written 'what' before implementation starts."
metadata:
  owner: kanam-dev
  status: active
---

# SKILL: OpenSpec Pattern (Intent-Driven Development)

## Version: 0.2-refined
## Status: PENDING_REVIEW

## 🎯 Core Concept
An OpenSpec is the definitive, structured contract defining *what* must be built, irrespective of *how* it is built. It moves the discussion from "how to code it" to "what problem are we solving and what are the non-negotiables."

## 🚀 Usage (The Workflow)
1. **Definition:** Create the OpenSpec file, detailing the intent.
2. **Guardrail Check (Radar):** Validate the spec against existing ADRs and the knowledge base before writing code.
3. **Execution:** Code is written ONLY to satisfy the Spec.
4. **Verification:** The final code/PR must satisfy 100% of the `AcceptanceCriteria` listed in the Spec.

## 🚦 Hard Gate: aprobación antes de construir

1. **Aprobación previa, sin excepciones:** antes de invocar cualquier skill de implementación, escribir código o arrancar un proyecto, presentar el diseño y obtener aprobación del humano, sin importar la complejidad percibida. "Simple" es justo donde los supuestos no examinados causan más desperdicio: el diseño puede ser corto (pocas frases para un proyecto simple), pero debe presentarse y aprobarse. El flujo se detiene en el diseño aprobado y nunca salta a construir.
2. **Alcance antes que detalle:** si el pedido describe múltiples subsistemas independientes (ej. chat + storage + billing + analytics), marcarlo de inmediato. No refinar detalles de algo que primero hay que descomponer: un contrato de intención por subsistema.
3. **Spec self-review (4 chequeos):** después de escribir el spec, revisarlo con ojos frescos:
   - Placeholder scan: ¿hay "TBD", "TODO" o partes incompletas?
   - Consistencia interna: ¿se contradicen las secciones?
   - Scope check: ¿es suficientemente enfocado para un solo plan?
   - Ambiguity check: ¿algún requisito admite dos interpretaciones? Elegir una y explicitarla.
   - Arreglar inline, sin re-revisar.

## ⚔️ Dependency
The Guardrail Check step needs a way to cross-reference ADRs and project knowledge. If your setup has no knowledge index, do that step manually against `docs/adr/`.

## 💥 Value
Prevents scope creep and technical debt by forcing alignment on **intent** before implementation complexity is added. It forces the discipline of writing down the 'Why' first.

## 📝 Example Snippet (for a feature)
\`\`\`yaml
spec_id: FEAT-001
title: User Profile Widget
description: A lightweight widget showing core user data.
constraints:
  - Must be accessible (a11y-check required).
  - Must not call external auth services (local-first constraint).
acceptance_criteria:
  - TC_001: Widget displays user.name.
  - TC_002: Widget displays user.avatarUrl.
  - TC_003: Load time < 500ms.
\`\`\`
