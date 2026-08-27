# LinkedIn Post - astryx #5493 (DRAFT)

**Status:** BORRADOR (no publicado)
**Idioma:** inglés
**Tono:** pedagógico con sustancia - historia técnica con el qué + el proceso + el porqué. **NO es tutorial paso a paso.**
**Nicho:** a11y
**Enlace:** https://github.com/facebook/astryx/pull/5493 | Issue: https://github.com/facebook/astryx/issues/5476

---

## Post (borrador)

I said in my last post that I had a follow-up in review fixing the same class of dropped accessibility attributes in `List` / `TreeList`. It just landed in **astryx**. 🌿

The bug: `TreeList` destructured a fixed set of props with no rest spread, so every `BaseProps` attribute - `aria-*`, `role`, `tabIndex`, `id`, event handlers - was silently dropped before reaching the DOM. A tree without a visible header could not be named at all: a **screen reader** announced an unnamed tree, and nothing said which tree it was.

The fix was more than "add `...restProps`". Three decisions shaped it:

1. **`aria-label` / `aria-labelledby` land on the `<ul role="tree">` itself**, not the wrapping `<div>`. A tree is named where the tree role is, not on a layout node that does nothing semantically.
2. **A visible header keeps naming the tree.** When `header` is rendered, the generated header id wins over any caller `aria-labelledby` - so assistive tech hears the same name the user sees. A caller label only applies on the headerless path.
3. **The contract `role="tree"` is written after the rest spread.** A consumer passing `role="listbox"` can no longer clobber the semantic role that makes the tree a tree.

The review process was the sharpest part: three rounds, and each one caught a real gap - first the wrong target element, then the precedence rule I'd gotten backwards. Getting an accessible name right is genuinely harder than it looks, because it is about *who* you label and *when* the visible label should win.

Five regression tests, 81 passing. And the `List` half is handled separately by the maintainers - no duplicated work.

PR: https://github.com/facebook/astryx/pull/5493

#accessibility #a11y #openaccessibility #assistivetechnology #inclusivedesign #webdev #reactjs #typescript #opensource #frontendengineering #componentlibrary #screenreader #inclusive #frontend

---

## Chequeo de estilo

- **Gancho:** retoma el cierre del post anterior (#5419) - continuidad del nicho a11y, demuestra constancia.
- **Problema desde el usuario:** "a screen reader announced an unnamed tree" - relatable.
- **Decisión con criterio:** los 3 puntos (elemento correcto, precedencia del header, role después del rest) - demuestran criterio real de a11y.
- **Proceso:** 3 rondas de review, cada una en un gap real - muestra proceso sin ser tutorial.
- **Cierre:** 81 tests + el reparto con #5288 (sin pisar trabajo ajeno).
- **Sin em dashes:** verificado.
- **Idioma:** inglés (repo externo / LinkedIn).
- **Longitud:** ~310 palabras - en el rango del modelo canónico.

## Pendientes
- [ ] Revisar el texto final con Gonzo antes de publicar.
- [ ] Publicar en LinkedIn.
