# LinkedIn Post - astryx #4605 (draft)

**Status:** draft para revisión de Gonzo
**Idioma:** inglés
**Tono:** historia de dev, natural, no corporativo

---

## Post

Some fixes are invisible. This one is a single line of CSS that took three weeks to land - and it's the kind of change that makes the web a little more usable for people who don't see color the way most of us do.

A few weeks ago I opened an issue on **astryx** (Facebook's open-source React component library): the current page in the breadcrumb trail was distinguished from the links *only by color*. A link is `--color-text-secondary`, the current page is `--color-text-primary`. If you can't perceive that color difference - color blindness, low vision, a high-contrast display - the breadcrumb silently fails WCAG 2.1 SC 1.4.1 (Use of Color). You'd have no idea where you are in the site.

The fix sounds trivial: add `font-weight: var(--font-weight-semibold)` to the current item's style, on top of the `aria-current="page"` that was already there for screen readers. Now the current page reads as current by *weight*, not just by color.

But the interesting part is what happened between the issue and the merge.

My first version of the PR was a mess. I'd accidentally let unrelated commits from a color-contrast branch leak into it. A reviewer would have been right to close it. So I rebased onto `main`, cleaned the scope down to exactly one change, and re-verified everything: 25/25 tests, lint clean, package boundaries clean.

Then something genuinely cool happened. astryx runs a nightly "component auditor" that found the *same* bug I'd filed - and explicitly deferred it to my PR, rather than landing a color-only patch that would have conflicted with the proper fix. The audit literally cited my open PR as the right way to solve it.

That's the part I love about open source: the system itself pointed at the correct fix. The maintainer who reviewed it said it was "the fix the Breadcrumbs audit pointed at."

Merged today. One line of CSS, three weeks of patience, and a breadcrumb that now tells you where you are - even if you can't see the difference between two grays.

If you build UI, go check your breadcrumbs. If the current item is only distinguished by color, you have the same bug I had.

---

## Notas para Gonzo

- **Longitud:** ~300 palabras, formato de historia con gancho + desarrollo + cierre con call-to-action.
- **Guion comun** en todo el texto (verificado, sin em dash).
- **Enlaces a incluir:**
  - PR: https://github.com/facebook/astryx/pull/4605
  - Issue: https://github.com/facebook/astryx/issues/4421
- **Opcional:** taggear a astryx / Facebook Open Source si querés más alcance.
- **Ajuste de tono:** si lo querés más corto o más técnico, decime y lo reescribo.
