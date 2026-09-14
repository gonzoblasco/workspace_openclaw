# LinkedIn Post: CreateFullPage focus on step change (ibm-products)

**Niche:** a11y (differentiator)
**Project:** carbon-design-system/ibm-products
**PR:** #9878 (merged 2026-09-14, commit 5d1ae52) | Issue: #9864
**Date:** 2026-09-14
**Status:** draft para revision de Gonzo
**Idioma:** ingles

---

## Post

The bug report said focus was lost. It was not lost. It went somewhere specific: the "Skip to main content" link at the top of the page.

In a multi-step `CreateFullPage`, a keyboard user presses Next and expects focus to land on the first interactive element of the newly visible step. Instead it jumped to the skip link - a nasty regression for anyone navigating with a keyboard, introduced between v2.43 and v2.44.

The root cause was an inference. A helper called `getActiveStep()` walked every step in the DOM and returned the first one whose ancestor chain had no `[inert]` attribute. The idea: "the visible step is the one that is not inert."

But `CreateFullPageStep` never sets `inert`. It hides non-active steps with `display: none`, through a CSS modifier class. So the walk always returned the first step in DOM order, no matter which step was actually active.

Then the hook did the reasonable thing with that wrong step: it found inputs inside it and called `.focus()`. Calling `.focus()` on an element inside a `display: none` subtree is a browser no-op. Focus never moved to the new step, stayed on the Next button or drifted to `<body>`, and the next tab stop picked it up - the skip link.

The fix was to stop inferring visibility from an attribute that was never set, and query the class the component already applies to the visible step. One `querySelector`, O(1), unambiguous.

The regression test renders two steps with real inputs, activates Next, and asserts that `document.activeElement` is the input of the visible step - and not the skip link, and not the body. It fails on main (the `waitFor` times out) and passes with the fix.

Two things I took from this one:

- **"Hidden" has more than one meaning in the DOM.** `inert`, `display: none`, `aria-hidden` and `visibility` each remove an element from a different surface: focus, layout, the accessibility tree, paint. Code that assumes one and gets another fails silently. No error, no exception, just wrong behavior.
- **The blast radius was worth spelling out.** The same hook is used by `CreateTearsheet`, whose steps do set `inert`. Both paths had to keep resolving correctly, so that went into the PR description before review, not after.

One note on the process: the maintainer flagged the component as heading toward deprecation, with an example pattern as the replacement. I kept the fix anyway - it is one line in a shared hook plus a test, no new API surface, and the bug is live for anyone on the published package today. Two maintainers approved it and it merged.

If you have a focus helper that decides "which container is visible" by looking for a marker attribute, check that the component actually sets that marker. That unverified assumption is the whole bug.

PR: https://github.com/carbon-design-system/ibm-products/pull/9878

#accessibility #a11y #keyboardnavigation #focusmanagement #wcag #opensource #reactjs #frontendengineering #inclusivedesign
