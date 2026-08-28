# Draft - Bug report to react-spectrum PR #10517

**Context:** After validating the story I added (story + VoiceOver check), I noticed the native browser chrome for the checkbox/radio input is visible on top of the custom SVG even with the fix applied. This is a deeper preexisting bug in RAC Checkbox/RadioGroup that the current fix does not solve.

**Goal:** report the bug clearly with technical evidence, ask for guidance before implementing a larger change. No greeting, no thanks. English, no em dash.

---

## Draft comment (English, on the PR conversation)

Validated the story I added (`CheckboxScreenReaderFocusRing` and `RadioGroupScreenReaderFocusRing`) on Chrome desktop with VoiceOver - the focus indicator tracks the checkbox and its label, which is exactly the reported issue.

Validating visually also surfaced a deeper preexisting bug in RAC Checkbox and RadioGroup that the current fix does not solve, and I want to flag it before we go further with the current approach.

**Observation:** in Chrome desktop (with system theme), the native browser chrome for the checkbox/radio input is rendered on top of the custom SVG mark when the component is checked. This is visible on:

- `CheckboxExample` (no fix, original story) - the native check square shows inside the SVG box.
- `RadioGroupExample` and `RadioGroupControlledExample` (no fix) - the native radio dot shows inside the SVG ring.
- `CheckboxScreenReaderFocusRing` and `RadioGroupScreenReaderFocusRing` (with the fix applied) - the native chrome becomes more prominent because the stretched input is now positioned over the custom SVG.

So the current fix exposes four style props that solve the bounding box issue (the input now covers the visible component) but does not solve the native chrome overlay. In fact, by stretching the input over the visible component, the native chrome overlay is now bigger and more obvious.

**Root cause:** the hidden input has `appearance: auto` (the default), so the browser renders the native widget on top of any CSS clip the VisuallyHidden wrapper applies. The VisuallyHidden wrapper clips the bounding box, but the native widget render does not respect CSS clip in modern Chrome/Firefox/Safari. The fix would need to set `appearance: none` on the input for the chrome to actually be hidden, but that is not something a consumer should have to know to add manually.

This means the smaller API you suggested is not just a nice-to-have - it is necessary to solve the actual bug. A single boolean prop that internally does the positioning correctly AND applies `appearance: none` to the input would solve both the SR focus ring and the native chrome overlay in one place, and it cannot be used to accidentally regress the appearance of the component.

Two questions before I rework the PR:

1. Does the boolean prop direction sound right, or would you prefer something different (a separate `inputClassName` only, or keeping the four props and documenting the `appearance: none` requirement)?
2. Should the boolean default to `true` (fix the chrome overlay for everyone, since it is currently a bug) or `false` (opt-in, to avoid any visual change for existing users)?

Want me to put together the smaller prop proposal once we agree on the direction?

---

## Notes

- Reports the bug from a place of evidence, not from "the fix is wrong". Acknowledges the fix works for what it claims to do (focus ring alignment), but exposes a deeper preexisting bug.
- The two questions at the end are the concrete ask: direction + default. This lets the maintainer steer without us designing against speculation.
- No greeting, no thanks. Direct to substance per Gonzo's rule (no thanks to bots/long conversations).
- Check with `scripts/check_em_dash.py` before publishing.
- Screenshots of the visual bug are in Gonzo's chat - if he wants to attach them to the PR comment, he can paste them in directly (GitHub comments do not accept local file attachments).