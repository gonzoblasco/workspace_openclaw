Summary of the rework. All review threads are addressed and the branch is green.

## Approach

The behavior is now on by default: no new public props, and no opt-in styling for consumers. The hidden native input is anchored to its component's outer element with CSS Anchor Positioning, so the screen reader focus ring (VoiceOver and NVDA draw it around the native input) lines up with the visible component instead of collapsing to the 1x1px `VisuallyHidden` box.

This replaces the earlier `inputStyle`/`visuallyHiddenStyle` approach, which required consumers to hand-wire a positioned containing block, a stretched wrapper and a stretched input.

## What changed

- **`hiddenInputAnchor.ts`** (new helper, internal)
  - `getAnchorStyles` declares the component's outer element as the anchor.
  - `getHiddenInputStyles` positions the input over that anchor.
  - The anchor name is a custom property, `--react-aria-anchor-name`, read on both the host and the input. Custom properties inherit, so one declaration from a class name or an ancestor reaches both sides.
- **`Checkbox.tsx`, `RadioGroup.tsx`**
  - Per-instance anchor name from `useId` (`react-aria/useId`), sanitized for a valid `<dashed-ident>`, replacing `Math.random`.
  - The layout effect and the per-render `getComputedStyle` are gone; the cascade resolves the name.
  - The extra anchor ref merge is gone.
- **Stories**: the two screen reader focus ring stories are removed. The behavior is on by default, and the browser tests are the coverage.

`--react-aria-anchor-name` follows existing public CSS variable API in the repo (`--trigger-anchor-point`, `--trigger-width`, `--table-row-level`). Happy to rename it if you prefer something else.

## Decisions that are load bearing

Each of these is measured, and two of them only show up in one engine:

- **`position: fixed` is required.** With `absolute` the input's containing block stays inside `VisuallyHidden` and `anchor()` does not resolve against the anchor; the used values fall back to the wrapper. `fixed` leaves that containing-block chain so the anchor resolves by name. Control: with the anchor as a *sibling* instead of an ancestor, `absolute` does resolve, so it is the ancestor relationship, not `absolute` itself.
- **`inset` for the offsets, `anchor-size` for the size.** `inset` is the RTL-correct choice: routing `anchor(left)` through a logical property mirrored the input to the wrong side (measured -208px in RTL). `inset` alone does not size the input though. A checkbox or radio input is a replaced control with an intrinsic size, and WebKit positions it without stretching it (measured: left at its 12x12 intrinsic box, covering none of the component), while Chromium stretches it. Both declarations are needed, and with both the input box matches the component exactly.
- **The name must be per instance.** With several elements sharing one `anchor-name`, every input resolved to the same anchor and none covered its own component, because a name resolves to a single anchor. `anchor-scope` localizes a shared name, but it shipped later than anchor positioning (Chrome 131 vs 125), so a shared name would break in that window.

Without anchor positioning support the declarations are inert and the input keeps today's 1x1px behavior.

## Tests

Six real-browser layout tests (jsdom does no layout, so it cannot validate this): the input covers the component for Checkbox and Radio, each instance anchors to itself, RTL, and the custom property override through both a stylesheet class and inline style. On engines without support they skip.

`test-browser` runs chromium, firefox and webkit, and all three are green. The first push of this rework failed WebKit and Firefox, and both were real: the WebKit failure was the missing `anchor-size` (not visible in Chromium, which was the only engine I had installed locally), and the Firefox one was a per-instance assertion that needed to sit behind the support check.

## Scope

Unchanged from the PR description: `Switch` renders its native input the same way and likely has the same focus indicator issue, and `Slider`, `Table` and `HiddenDateInput` also wrap a native input in `VisuallyHidden`. Both are follow-ups, and the helper here would be the place to extend.
