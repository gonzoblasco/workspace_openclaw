# LinkedIn Post: global aria-posinset across menu sections (react-spectrum)

**Niche:** a11y (differentiator)
**Project:** adobe/react-spectrum
**PR:** #10554 (merged 2026-09-09 by yihuiliao)
**Date:** 2026-09-09

---

## Draft

Not every accessibility bug breaks something visibly. Some just disappear from the test suite one day, and nobody notices.

A few days ago I got a PR merged in Adobe React Spectrum that illustrates this point: it's a test-only PR, and that's exactly what makes it interesting.

**The context**

In a menu with sections (groups of items), the ARIA specification requires `aria-posinset` to be **global**: if there are 4 items spread across 2 sections, the positions run 1 through 4 continuously, consistent with `aria-setsize=4`. If a section restarts the count, screen readers announce positions that don't match reality ("item 1 of 2" when it's actually "item 1 of 4"), and navigation becomes confusing.

React Spectrum was already producing the correct values. The problem was that **nothing guaranteed it**: a future refactor of the index computation could silently reintroduce per-section restarts without any test failing.

**The test trap**

Writing the test looked trivial: render a menu with sections and assert the positions are 1, 2, 3, 4. But the first version had a flaw I didn't see myself: the helper building the mock "flattened" the sections into a plain list of items. The resulting DOM never contained the sectioned structure the test claimed to cover.

The test passed. But it wasn't testing what it said it was testing. A maintainer spotted it in seconds - and rightly so: it's exactly the kind of shortcut that gives false confidence.

**The fix**

The final version renders each section through the real hook (`useMenuSection`), including the labelled groups and their headings, and also covers sections without a heading (where the accessible name comes from `aria-label`). That way, any future change in section logic - not just the index computation - gets exercised by the test.

**Why it matters**

An accessibility test is only as good as the structure it exercises. If the setup simplifies the DOM down to a flat list, a green test is decoration. The rule I took away: the test must render the real component structure, fail when the behavior breaks, and verify exactly what the PR claims.

#Accessibility #ARIA #Testing #OpenSource #FrontendEngineering