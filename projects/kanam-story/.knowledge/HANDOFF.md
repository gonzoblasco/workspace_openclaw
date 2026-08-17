# HANDOFF — kanam-story

## Session Context
- **Date:** 2026-08-17 16:51
- **Project:** kanam-story
- **Branch:** main
- **Release:** v0.17.0

## Summary
Sesión de cierre del bloque post-v0.16.1 + release v0.17.0 + smoke tests de acciones nuevas. El proyecto quedó en **377 tests**. Se definió la estrategia de monetización (3 públicos) y se diseñó el feature flag del co-writer (revertido por ahora).

## Qué se hizo en esta sesión

### Release v0.17.0
- **`cb80bdc`** — bump a v0.17.0 + CHANGELOG + tag + GitHub Release. Cierra el bloque post-v0.16.1: roles especializados (Plot Doctor, Consistency Checker), PWA, mobile responsive, diálogos accesibles (ConfirmDialog/PromptDialog), export polish.

### Smoke tests de acciones nuevas
- **`scripts/smoke-actions.ts`** (nuevo) — valida con Ollama real que el modelo parsea `delete_character`, `delete_world`, `update_project`. **3/3 OK** (todas las acciones parseadas y válidas). El modelo además responde con criterio (avisa consecuencias, pregunta por referencias).

### Feature flag del co-writer (diseñado, revertido)
- **`2f5130e`** — feature flag `NEXT_PUBLIC_ENABLE_COWRITER` en `lib/features.ts` (co-writer deshabilitado en open source).
- **`8eb6275`** — **REVERTIDO** por decisión de Gonzo: el co-writer sigue habilitado en open source hasta que exista el backend SaaS con usuarios. El flag queda documentado en el historial de git para recuperarlo cuando toque.

## Estrategia de monetización (definida con Gonzo)

**3 públicos que conviven:**
1. **Open source (gratis, local-first)** — el producto completo, BYOK → Ollama. Embajador de marca + portfolio.
2. **SaaS BYOK (5 USD/mes)** — mismo producto + sync en la nube + multi-dispositivo + registro. El usuario trae su LLM (OpenAI-compatible).
3. **SaaS premium (con LLM incluido)** — DeepSeek V4 Flash server-side. Más caro.

**Bonus de pago:** el co-writer (el corazón) es exclusivo de pago. El open source conserva el producto de escritura completo (editor, Story Bible, outline, export, PWA) pero sin el chat con manos. **Se activa cuando exista el backend + auth + billing.**

## Quality baseline
- **377 tests passing.**
- `npm run build`, `npx tsc --noEmit`, `npm run lint` verdes.

## Next steps
1. **Aplicar los fixes de la auditoría del co-writer** (IDs de personajes/mundo + unificar contexto).
2. **Auditar los otros specs** (editor, outline, biblia, brújula, persistencia) contra el comportamiento real.
3. **Generalizar el BYOK** a cualquier endpoint OpenAI-compatible (preparación para SaaS).
4. **Futuro:** backend + auth + billing (Supabase), sync IndexedDB ↔ nube, activar el feature flag del co-writer.

## OpenSpec (inicializado 2026-08-17)

- **`openspec/`** inicializado con schema `spec-driven`.
- **`openspec/project.md`** - visión, stack, dominio, estrategia de 3 públicos.
- **`openspec/config.yaml`** - contexto del proyecto + reglas para el CLI.
- **6 specs de casos de uso core** (34 requirements): co-writer (9), editor (6), outline-beats (6), proyecto-persistencia (5), biblia-viva (4), brújula-narrativa (4).
- **Auditoría del co-writer realizada** (2026-08-17): 4 hallazgos - ver `openspec/audits/co-writer-2026-08-17.md`.

## Auditoría del co-writer (2026-08-17) - 4 hallazgos, TODOS APLICADOS

> Ver `openspec/audits/co-writer-2026-08-17.md`. Fixes en commit `f618a38`.

1. ✅ **ALTO (IDs):** el contexto del chat ahora incluye IDs de personajes/mundo (antes solo escenas/beats).
2. ✅ **MEDIO (inContext):** el filtro `inContext` ahora es consistente - personajes excluidos en chat Y editor.
3. ✅ **MEDIO (brújula):** la brújula ahora se incluye en el editor (antes solo en el chat).
4. ✅ **MEDIO (continuidad):** las notas de continuidad ahora se incluyen en el editor (antes solo en el chat).

**Causa raíz resuelta:** `buildContext` (editor) ahora recibe el mismo contexto enriquecido que `buildAgentContext` (chat).
**Tests:** 382 (subió de 379, +3 tests de los fixes). Build + tsc + lint verdes.

## Next steps
1. **Auditar los otros specs** (editor, outline, biblia, brújula, persistencia) contra el comportamiento real.
2. **Generalizar el BYOK** a cualquier endpoint OpenAI-compatible (preparación para SaaS).
3. **Futuro:** backend + auth + billing (Supabase), sync IndexedDB ↔ nube, activar el feature flag del co-writer.

## Open questions / caveats
- El feature flag del co-writer está en el historial de git (`2f5130e`), revertido por `8eb6275`. Recuperar cuando exista el SaaS.
- Los mocks de tests usan `as MockApp` tipado; al agregar campos nuevos al store hay que actualizarlos.
- Al cambiar la firma de `applyContentActions` (ahora devuelve `{undo, failed}`), cualquier nuevo caller debe adaptarse.
