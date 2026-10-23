# LinkedIn Post: sortable headers announced as toggle buttons (ibm-products)

**Niche:** a11y (differentiator)
**Project:** carbon-design-system/ibm-products
**PR:** #9879 (merged 2026-10-07, commit e33f56ab) | Issue: #9839
**Date:** 2026-10-07
**Status:** PUBLICADO 07/10/2026
**Idioma:** ingles

---

## Post

A screen reader does not read what your component means. It reads what your markup declares. When the two disagree, the user hears the declaration - and acts on it.

A Datagrid had a sortable column header. Visually it was obvious: click to sort ascending, click again for descending, the little arrow flips. For a screen reader it was a **toggle button**. Not a sorted column - a toggle.

The reason was one attribute. The sortable header button rendered by `useSortableColumns` set `aria-pressed` to `true`/`false`. To a screen reader, a button with `aria-pressed` is a toggle button, and that is exactly how VoiceOver announced it: "toggle button", state pressed or not pressed. The current sort direction - ascending, descending, unsorted - never reached the user.

The confusing part: the direction was already announced, correctly, somewhere else. `aria-sort` lives on the `columnheader` element and carries the state. So the component was saying two different things at once: `aria-sort="ascending"` on the header, and `aria-pressed="false"` on the button inside it. The screen reader prioritized the toggle and dropped the semantics the user actually needed.

The fix was to stop saying the wrong thing. Remove `aria-pressed`, and the now-unused helper that computed it. Sort state stays on `aria-sort` in the columnheader - which is also what the core `@carbon/react` DataTable does. Its sort trigger does not use `aria-pressed` at all. Datagrid was the outlier.

The regression test asserts the sortable header button has no `aria-pressed` attribute. It fails on `main` (the attribute is there, set to `false`) and passes with the fix.

Two things I keep in mind from this one:

- **`aria-pressed` is not a state container. It is a role assignment.** The moment you set it, you have told assistive tech "this is a toggle." Use it only when the control really is a two-state toggle. For sort, the correct signal is `aria-sort` on the header - a different element, a different meaning.
- **Redundant ARIA is not harmless.** Two declarations for the same concept do not reinforce each other; they compete, and the wrong one can win. Before adding an attribute, check whether the correct semantics already exist elsewhere in the same widget.

If a component announces a control as something it is not, the fix is usually not "add more ARIA." It is "remove the attribute that lies."

PR: https://github.com/carbon-design-system/ibm-products/pull/9879

#accessibility #a11y #aria #screenreaders #datagrid #wcag #opensource #reactjs #frontendengineering #inclusivedesign

---

*Nota de estado: La fecha de publicacion no quedo registrada. La que se anota es la del merge del PR (#9879, 07/10/2026), que es la mejor evidencia disponible. Publicacion registrada por Gonzo el 2026-10-22; el `Status:` no se habia volteado.*
