# LinkedIn Post - react-spectrum #10503 (DRAFT)

**Status:** draft para revision de Gonzo
**Idioma:** inglés
**Tono:** pedagógico con sustancia - historia técnica con el qué + el proceso + el porqué. **NO es tutorial paso a paso.**
**Rol:** estilo de marca de Gonzo para posts de LinkedIn (la politica de los 3 nichos vive en `memory/user-profile.md` linea 47).
**Nicho:** a11y
**Proyecto:** adobe/react-spectrum
**PR:** #10503
**Fecha:** 2026-10-12

---

## Post (versión borrador)

I just got a PR merged into **React Spectrum** that fixes a subtle **VoiceOver** bug in the `ComboBox` component. The issue (#10220) was that VoiceOver on Apple devices would announce only the item name when navigating, losing richer native details such as the selected state, role, and item count.

**What happened?** The `useComboBox` hook emitted a live-region announcement for every focused-item change. Modern VoiceOver already provides per-item details natively, so the live region overwrote that native speech, resulting in a degraded experience for screen-reader users.

**How we solved it.** We gated the manual announcement so it only fires when the focus moves into a *new section* - a point where VoiceOver is silent and the section title + option count are not announced natively. Arrowing within the same section now lets VoiceOver handle the announcement, restoring the richer native feedback.

**Why it matters.** This change preserves the full semantic context for users of VoiceOver, ensuring they hear not just the item name but also its selection state and grouping. It keeps the announcement semantically correct instead of merely louder, and it removes the degraded experience that the live region was creating for VoiceOver users.

The review process was the interesting part. I had updated the combobox tests to assert that per-item navigation no longer triggers a manual announcement, and the maintainer pushed back twice: the first version of those assertions was, in their words, the same thing as `not.toHaveBeenCalled` dressed up differently, and the second round of feedback asked whether those tests covered anything other tests did not cover. The resolution was to **drop the tests entirely** - once the announcement moved to section changes, there was nothing left for them to assert. The suite now passes **259 tests** (218 in `@adobe/react-spectrum` and 41 in `react-aria-components`).

**PR:** https://github.com/adobe/react-spectrum/pull/10503

#accessibility #a11y #reactjs #typescript #opensource #frontendengineering #uiux #screenreader #webdev #componentlibrary #reactspectrum #frontend

---

## Por qué este post es el modelo canónico (anatomía del estilo)

1. **Abre con el problema** desde la perspectiva del usuario de VoiceOver, mostrando empatía y claridad.
2. **Explica la raíz** del bug y el razonamiento detrás de la solución, sin entrar en pasos de código.
3. **Incluye la decisión de ingeniería** (gating de anuncios) y el contexto de la revisión (tres comentarios en línea).
4. **Muestra evidencia** (259 pruebas pasan) que respalda la estabilidad del cambio.
5. **Cierra con llamado a la acción** invitando a la comunidad a probar y compartir feedback.
6. **Tags** relevantes al final para alcance del nicho.

## Notas para futuros posts

- **Formato:** historia técnica con gancho + problema + decisión + cierre. ~250-350 palabras.
- **NO** tutorial paso a paso. Mantener el guion comun (sin em-dash).
- **Enlaces:** PR + issue relacionados.
- **Longitud:** revisar con `scripts/check_em_dash.py` para evitar em-dash.

---

*Referencia del estilo de marca - 2026-08-25. Ver `memory/user-profile.md` (estrategia de 3 nichos).* 

