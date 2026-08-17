# HANDOFF — kanam-story

## Session Context
- **Date:** 2026-08-17 13:30
- **Project:** kanam-story
- **Branch:** main
- **Release:** v0.16.1 + bloque de features post-release (sin bump de versión)

## Summary
Sesión larga de cierre del bloque post-v0.9.0 + avance de features. Se resolvieron los dolores pendientes del inventario y se expandió el co-writer. El proyecto quedó en **377 tests** (subió de 366). Todos los pendientes del daily previo están resueltos.

## Qué se hizo en esta sesión (13 commits)

### a11y
- **`58a6706`** — `--sl-danger` en tema claro de 2.78:1 → 5.22:1 (WCAG AA).
- **`f53a7e1`** — `ConfirmDialog` + `PromptDialog` reemplazan los 12 `window.prompt`/`confirm` nativos en 7 componentes (foco gestionado, aria-modal, Escape).
- **`e26c3d6`** — Fix lint: `useId()` + input no controlado (10 errores ESLint → 0).

### Mobile responsive (≤768px)
- **`164a406`** — Sidebar como drawer overlay con backdrop + topbar compacto (solo iconos).
- **`140616f`** — Padding reducido (main-content/editor/stack-section) + co-writer full-width.
- **`ea915cf`** — Modales full-width + ai-bar apilado + chapter reader compacto.

### PWA
- **`f3e41a7`** — Soporte PWA con Serwist (`@serwist/turbopack`): SW compilado en build via route handler (`/serwist/sw.js`), manifest, página offline (`/~offline`), SerwistProvider.
- **`6a01623`** — Iconos PWA reales (gradiente morado + K blanca, generados con PIL).

### Export
- **`3c1c012`** — Portada con metadata narrativa (POV + estilo) + pie con word count. `countWords()` pura y testeada.

### Co-writer (U5+)
- **`f5ee579`** — Nuevas acciones: `delete_character`, `delete_world` (destructivas), `update_project` (refina metadata del proyecto).
- **`f68aff9`** — Roles especializados: selector en el sidebar (Co-writer / Plot Doctor / Consistency Checker) que especializa el prompt via `buildAgentPrompt(role)` + `settings.agentRole`.
- **`912db24`** — Smoke test de roles (`scripts/smoke-roles.ts`), verificado con deepseek-v4-flash:cloud.

### Validación AT manual
- **Verificada por Gonzo** con VoiceOver (live region del chat + radio group del onboarding). Cierra pendiente del PLAN-FASE-4.md.

## What changed (archivos clave)
- `lib/export.ts` — metadata narrativa + word count + `countWords`.
- `lib/actions.ts` — cases `delete_character`, `delete_world`.
- `lib/agentReply.ts` — validación de las 3 acciones nuevas + `POV_VALUES`.
- `lib/agentPrompts.ts` — `buildAgentPrompt(role)` + `buildRoleIntro` (roles especializados).
- `lib/store.tsx` — handlers de las 3 acciones + deps.
- `lib/actionTargets.ts` — navegación contextual de las acciones nuevas.
- `components/ConfirmDialog.tsx`, `PromptDialog.tsx` (nuevos).
- `components/CoWriterSidebar.tsx` — selector de rol.
- `app/layout.tsx`, `next.config.ts`, `app/sw.ts`, `app/serwist/[path]/route.ts`, `app/~offline/`, `app/manifest.json`, `public/icon-*.png` — PWA.
- `scripts/smoke-roles.ts` (nuevo) — smoke test de roles.

## Quality baseline
- **377 tests passing** (subió de 366).
- `npm run build`, `npx tsc --noEmit`, `npm run lint` (ESLint) verdes.

## Next steps
1. **Smoke tests con Ollama** de los flujos de las acciones nuevas (`delete_character`, `update_project`) si se quiere validar el parseo con el modelo real.
2. Considerar **bump de versión** (el bloque de features post-v0.16.1 no tiene release).
3. Futuro: multi-usuario/sync (pendiente de largo plazo), mocks de tests frágiles.

## Open questions / caveats
- Los mocks de tests usan `as MockApp` tipado; al agregar campos nuevos al store hay que actualizarlos.
- Al cambiar la firma de `applyContentActions` (ahora devuelve `{undo, failed}`), cualquier nuevo caller debe adaptarse.
- El selector de rol del co-writer es un `<select>` simple; si crece, evaluar UI más rica (chips/tabs).
