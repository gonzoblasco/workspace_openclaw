# PROMPT — Agente A (VS Code) · U1: Barra de formato básica

> **Proyecto:** Kanam Story
> **Fase 3, Unidad 1 (U1)** — ver `PLAN-FASE-3.md` para el contexto completo del pipeline.
> **Fecha:** 2026-08-13

---

## Tu tarea (U1)

Agregar una **barra de formato básica** al editor de prosa (`components/Editor.tsx`): negrita, cursiva, subrayado, tachado, deshacer/rehacer.

## Contexto técnico (verificado)

- El editor usa **TipTap 3** con `StarterKit` (`@tiptap/starter-kit`). StarterKit **ya incluye** los marks (bold, italic, strike) y los nodos (heading, bulletList, orderedList) — los comandos están disponibles sin instalar nada.
- **No instalar** `@tiptap/extension-link` ni `@tiptap/extension-underline` en esta unidad (eso es la U2 de Agente B). Para subrayado, evaluar si StarterKit lo trae o si hay que agregar `@tiptap/extension-underline` — si hace falta, documentarlo en el commit para que B lo sepa.
- El editor ya tiene una barra de IA (`ai-bar`) con botones Write/Rewrite/Describe/Expand/Dialogue/Tension. La barra de formato va **separada** (arriba del texto, como Sudowrite), no mezclada con la de IA.
- Comandos TipTap disponibles: `editor.chain().focus().toggleBold().run()`, `toggleItalic()`, `toggleStrike()`, `undo()`, `redo()`.
- El editor se obtiene con `useEditor()` y se expone como `editor` en el componente. Los botones deben usar `editor.isActive('bold')` para el estado activo y `editor.can().chain().focus().toggleBold().run()` para habilitar/deshabilitar.

## Requisitos

1. Barra de formato visible arriba del área de texto (o flotante sobre la selección — decidí el que sea más limpio y consistente con el diseño actual).
2. Botones: **B** (negrita), *I* (cursiva), ~~S~~ (tachado), U (subrayado si está disponible), deshacer (↩), rehacer (↪).
3. Estado activo: el botón se resalta cuando el formato está aplicado en el cursor/selección.
4. Habilitado/deshabilitado: los botones se deshabilitan cuando no aplican (ej. undo cuando no hay historial).
5. **No romper** el autosave existente (debounce 600ms en `saveContent`) ni la barra de IA.
6. El usuario debe poder escribir, copiar/pegar y editar libremente (esto ya funciona; no romperlo).

## Criterios de aceptación (U1)

- [ ] La barra de formato aparece en el editor.
- [ ] Negrita, cursiva, tachado (y subrayado si aplica) funcionan sobre selección.
- [ ] Deshacer/rehacer funcionan.
- [ ] Estado activo de los botones correcto.
- [ ] Autosave y barra de IA intactos.
- [ ] Build + TS pasan, lint 0 errores, tests existentes verdes.

## Al terminar

1. Commit atómico en inglés: `feat: add basic formatting toolbar to editor (U1)`.
2. Push a `origin/main`.
3. Dejar mensaje claro de qué se hizo y qué necesita revisión (especialmente si hubo que agregar `@tiptap/extension-underline`).
4. Actualizar `PLAN-FASE-3.md` (marcar U1) y `STATUS.md`.

## Después de vos

**Agente B (ZCode)** revisa tu U1 y hace la U2 (listas + headings + enlaces). No avances a la U3 hasta que B haya revisado y pusheado la U2.
