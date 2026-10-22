# LinkedIn Post - carbon #22887 (DRAFT)

**Status:** draft para revision de Gonzo
**Idioma:** inglés
**Tono:** pedagógico con sustancia - historia técnica con el qué + el proceso + el porqué. **NO es tutorial paso a paso.**
**Rol:** estilo de marca de Gonzo para posts de LinkedIn (la politica de los 3 nichos vive en `memory/user-profile.md` linea 47).
**Nicho:** a11y
**Proyecto:** carbon-design-system/carbon
**PR:** #22887
**Fecha:** 2026-10-12

---

## Post (versión borrador)

I just merged a PR into **Carbon Design System** that adds native support for the `aria-describedby` prop on the `ComposedModal` component. The change closes #21342, a known accessibility gap where screen-reader users could not programmatically associate a description with a modal dialog.

**What was missing?** The modal component previously only forwarded `aria-labelledby`. Without `aria-describedby`, developers could not provide a concise, contextual description for the dialog, leaving assistive technology users without crucial information about the modal’s purpose.

**How we fixed it.** We introduced a new optional prop `aria-describedby` and wired it through the component so that when the `enable-dialog-element` feature flag is active the attribute lands on the native `<dialog>` element; otherwise it falls back to the `<div role="dialog">` container. The implementation adds a single line change (`+63 -1`) and updates the TypeScript definitions accordingly.

**Why it matters.** Providing an accessible description allows screen readers to announce a brief, contextual message when a modal opens, improving the overall usability for users with visual impairments. It closes a gap that assistive technology users were living with, and it strengthens the library’s a11y posture.

**Friction point in review.** The maintainer pushed back on three things, and the first one is the interesting one: my first test referenced a `description-modal-id` element **without rendering it**, so it asserted the attribute was present on the dialog but proved nothing about whether the description actually existed in the page. The fix was to render the element alongside the modal. The other two were about not leaking implementation details - a reference to the internal `cds--modal-container` class in a comment, and a note to document the new prop properly instead of leaving it implicit.

The third round is the one I keep coming back to: the maintainer asked whether the review comments had actually been addressed, and the honest answer was that some had not. That was worth hearing.

The PR landed with a test that renders the description element and asserts the attribute reaches the native `<dialog>` when `enable-dialog-element` is on, plus the `div[role=dialog]` fallback. The merge commit `1709742020a4de25264060216ee8b7349581d9f1` landed on 12 Oct 2026.

**PR:** https://github.com/carbon-design-system/carbon/pull/22887

#accessibility #a11y #carbon #designsystem #reactjs #typescript #opensource #frontendengineering #uiux #screenreader #frontend

---

## Por qué este post es el modelo canónico (anatomía del estilo)

1. **Abre con el problema** desde la perspectiva de la accesibilidad, mostrando impacto real.
2. **Explica la solución** con foco en la lógica de la prop y la bandera de característica.
3. **Incluye decisiones de ingeniería** (añadir pruebas, mejorar documentación, eliminar referencias internas).
4. **Muestra evidencia** (cambio de línea, pruebas pasadas, revisión de comentarios).
5. **Cierra con llamado a la acción** invitando a la comunidad a probar el modal y compartir feedback.
6. **Tags** adecuados para alcance del nicho.

## Notas para futuros posts

- **Formato:** historia técnica con gancho + problema + decisión + cierre. ~250-350 palabras.
- **NO** tutorial paso a paso. Mantener guion comun (sin em-dash).
- **Enlaces**: PR + issue relacionados.
- **Revisar** con `scripts/check_em_dash.py` antes de enviar.

---

*Referencia del estilo de marca - 2026-08-25. Ver `memory/user-profile.md` (estrategia de 3 nichos).* 

