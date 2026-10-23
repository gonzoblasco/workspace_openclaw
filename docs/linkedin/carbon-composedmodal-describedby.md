# LinkedIn Post - carbon #22887 (DRAFT)

**Status:** PUBLICADO 22/10/2026
**Publicado en:** https://www.linkedin.com/posts/gonzalo-blasco_accessibility-a11y-carbon-share-7519182890929160192-QjBO/
**Idioma:** inglés
**Tono:** pedagógico con sustancia - historia técnica con el qué + el proceso + el porqué. **NO es tutorial paso a paso.**
**Rol:** estilo de marca de Gonzo para posts de LinkedIn (la politica de los 3 nichos vive en `memory/user-profile.md` linea 47).
**Nicho:** a11y
**Proyecto:** carbon-design-system/carbon
**PR:** #22887
**Fecha:** 2026-10-12

---

## Post (versión borrador)

I just merged a PR into **Carbon Design System** that adds native support for the `aria-describedby` prop on the `ComposedModal` component. The change closes #21342, a known accessibility gap where screen-reader users could not programmatically associate a description with a modal dialog. 🌿

**What was missing?** The modal only forwarded `aria-labelledby`. Without `aria-describedby`, developers could not give the dialog a concise, contextual description, and assistive technology users got the title with nothing about what the modal was for.

**How we fixed it.** A new optional `aria-describedby` prop, wired through so that when the `enable-dialog-element` feature flag is on the attribute lands on the native `<dialog>` element, and otherwise falls back to the `div[role="dialog"]` container.

**The review process was the interesting part.** The maintainer pushed back on three things, and the first one is the one I keep coming back to: my first test referenced a `description-modal-id` element without rendering it, so it asserted the attribute was present on the dialog but proved nothing about whether the description actually existed in the page. The fix was to render the element alongside the modal. The other two were about not leaking implementation details - a reference to the internal `cds--modal-container` class in a comment, and documenting the new prop properly instead of leaving it implicit.

And then the maintainer asked whether the review comments had actually been addressed, when some of them had not. That was worth hearing.

The PR landed with a test that renders the description element and asserts the attribute reaches the native `<dialog>` when the flag is on, plus the `div[role="dialog"]` fallback.

If your dialog has a title but no description, that is a gap your users cannot see either.

PR: https://github.com/carbon-design-system/carbon/pull/22887

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

