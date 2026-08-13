# PROMPT — Agente B (ZCode) · U2: Listas + headings + enlaces + underline

> **Proyecto:** Kanam Story
> **Fase 3, Unidad 2 (U2)** — ver `PLAN-FASE-3.md` para el contexto completo del pipeline.
> **Fecha:** 2026-08-13

---

## Tu tarea (U2) — dos partes

1. **REVISAR la U1** (barra de formato básica, commit `b5e9484` del Agente A). Corregir si hace falta.
2. **DESARROLLAR la U2**: completar la barra de formato con **listas (viñetas/numeradas), headings (H1/H2/H3), enlaces y subrayado**.

## Contexto técnico (verificado por Kanam — IMPORTANTE, corrige la nota del Agente A)

El Agente A dejó una nota diciendo que "StarterKit NO incluye underline" y que hay que `npm install @tiptap/extension-underline`. **Eso es incorrecto.** Verifiqué el código:

- **StarterKit 3.27.1 SÍ incluye** `Underline`, `Link`, `BulletList`, `OrderedList`, `Heading` por defecto. En `node_modules/@tiptap/starter-kit/dist/index.js` línea 85: `extensions.push(Underline.configure(...))`. Y el `.d.ts` expone `underline`, `link`, `bulletList`, `orderedList`, `heading` como opciones configurables.
- **NO hace falta instalar nada.** Las extensiones ya están en `node_modules/@tiptap/` (extension-underline, extension-link, extension-list, extension-heading) y StarterKit las incluye.
- El botón U quedó deshabilitado en la U1; tu trabajo es **habilitarlo** configurando el editor, no instalando el paquete.

## Qué hacer

### Parte 1 — Revisar la U1 (commit `b5e9484`)
- `git show b5e9484` para ver el diff (barra de formato en `components/Editor.tsx` + estilos en `app/globals.css`).
- Verificar: B/I/S funcionan, undo/redo funcionan, estado activo correcto, autosave y barra IA intactos.
- Corregir cualquier bug. Si está bien, dejarlo y seguir.

### Parte 2 — Desarrollar la U2
1. **Subrayado (U):** habilitar en el editor. Como StarterKit ya lo incluye, solo hay que asegurarse de que esté activo (si el `StarterKit.configure` actual no lo deshabilita, ya está). Habilitar el botón U con `toggleUnderline()`.
2. **Listas:** botones de viñetas (`toggleBulletList()`) y numeradas (`toggleOrderedList()`). Estado activo con `editor.isActive('bulletList')` / `editor.isActive('orderedList')`.
3. **Headings:** selector o botones H1/H2/H3 (`toggleHeading({ level: 1|2|3 })`). El editor ya configura `heading: { levels: [2, 3] }` — decidí si ampliar a H1 o mantener 2-3. Estado activo con `editor.isActive('heading', { level })`.
4. **Enlaces:** botón de enlace. Requiere seleccionar texto y pedir la URL (prompt simple o input inline). Usar `editor.chain().focus().setLink({ href }).run()` y `unsetLink()` para quitar. Estado activo con `editor.isActive('link')`.
5. **Estilos:** agregar los estilos de los nuevos botones en `app/globals.css`, consistente con la barra de formato existente (`.format-bar`, `.format-btn`).

## Criterios de aceptación (U2)

- [ ] Subrayado funciona (botón U habilitado).
- [ ] Listas viñetas y numeradas funcionan.
- [ ] Headings H1/H2/H3 funcionan (o 2-3 si decidís mantener).
- [ ] Enlaces: setear y quitar enlace sobre selección.
- [ ] Estado activo de todos los botones correcto.
- [ ] Autosave y barra IA intactos.
- [ ] Build + TS pasan, lint 0 errores, tests existentes verdes.

## Al terminar

1. Commit atómico en inglés: `feat: complete formatting toolbar with lists, headings, links and underline (U2)`.
2. Push a `origin/main`.
3. Dejar mensaje claro de qué se hizo, qué se corrigió de la U1 (si algo), y qué necesita revisión.
4. Actualizar `PLAN-FASE-3.md` (marcar U2) y `STATUS.md`.

## Después de vos

**Agente A (VS Code)** revisa tu U2 y hace la U3 (selección contextual IA). No avances a la U4 hasta que A haya revisado y pusheado la U3.
