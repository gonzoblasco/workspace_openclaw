# HANDOFF — kanam-story

## Session Context
- **Date:** 2026-08-17 02:22
- **Project:** kanam-story
- **Branch:** main
- **Release:** v0.16.0 publicado y pusheado.

## Summary
Gran sesión de features sobre Kanam Story, del outline global a un co-writer más potente y con mejor UX. Se publicaron 7 releases (v0.11.0 → v0.16.0), cada uno con tests, build, TS y lint verdes. El proyecto quedó en **359 tests**.

## Releases de esta sesión
- **v0.11.0** — Panel de escenas huérfanas en el outline global (mover/vincular/ver/eliminar escenas sin capítulo).
- **v0.11.1** — Fix de a11y y consistencia de botones del outline (contraste AA del primario, labels visibles en iconos, variantes unificadas).
- **v0.11.2** — Self-review: fix del filtro de escenas huérfanas (`chapterId === ''` vs "sin beats") + `type="button"` en iconos.
- **v0.12.0** — `update_outline`: ediciones parciales del outline vía chat (renombrar/borrar capítulo, agregar/borrar/mover/editar beats) con undo.
- **v0.12.1** — Beats desde el manuscrito del autor vía chat (escena activa completa en contexto) + ids de beats expuestos en el contexto.
- **v0.13.0** — Sidebar de co-writer desde la escritura, con contexto acotado a la escena actual (no modifica otras escenas).
- **v0.13.1** — Fixes de chat: markdown renderizado, indicador "Pensando…", feedback de acciones fallidas (`applyContentActions` devuelve `{undo, failed}`).
- **v0.14.0** — Gestión de proyectos (borrar proyecto con cascade) + fix de generación de escena (reutiliza la única escena del capítulo).
- **v0.15.0** — Botón "Enriquecer" en perfiles de personajes y mundo (respetando el mundo literario, no se va de tema).
- **v0.15.1** — Fixes de editor/chat: cambios aceptados aparecen al instante, se preservan saltos de línea, sidebar ocupa todo el alto con input al pie.
- **v0.15.2** — Export solo historia (sin personajes/mundo/beats) + separador de escena (`---` en PDF, `· · ·` en DOCX).
- **v0.16.0** — Notas de continuidad por escena + acción `update_scene_notes` del agente.

## What changed (archivos clave)
- `types/index.ts` — `Scene.continuityNotes`, acciones `update_outline`, `update_scene_notes`.
- `lib/actions.ts` — estado puro con undo para `update_outline`, `update_scene_notes`.
- `lib/agentReply.ts` — validación + parsers (`parseEnrichedCharacter`, `parseEnrichedWorld`).
- `lib/agentPrompts.ts` — prompts de enriquecer personaje/mundo, beats desde manuscrito, notas de continuidad; ids de beats en contexto.
- `lib/store.tsx` — `deleteProject`, `enrichCharacter`, `enrichWorld`, `applyContentActions` con `{undo, failed}`, `ensureHtml` en rewrite/append.
- `lib/export.ts` — export solo historia + separadores.
- `components/` — `CoWriterSidebar`, `OrphanScenesPanel`, `MarkdownView` en chat, botones Enriquecer, notas de continuidad en editor.

## Quality baseline
- **359 tests passing.**
- `npm run build`, `npx tsc --noEmit`, `npm run lint` verdes.

## Next steps
1. Decidir el próximo bloque de features (U5+ de co-writer, polish de export, mobile/PWA, agentes especializados).
2. Verificar visualmente el sidebar y las notas de continuidad con una historia real.
3. Smoke tests con Ollama local para los flujos nuevos (enriquecer, notas de continuidad) si hace falta.

## Open questions / caveats
- `btn-outline-danger` (Bootstrap default) sobre fondo blanco del tema claro no cumple WCAG AA (2.78:1). Problema global a decidir (customizar danger o aceptar default).
- Los mocks de tests usan `as MockApp` tipado; al agregar campos nuevos al store hay que actualizarlos.
- Al cambiar la firma de `applyContentActions` (ahora devuelve `{undo, failed}`), cualquier nuevo caller debe adaptarse.
