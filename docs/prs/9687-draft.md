## Why

Screen readers (VoiceOver, NVDA) draw their focus indicator around the native
`<input>` element, not around the visible component. In Checkbox and Radio the
input is rendered inside `VisuallyHidden`, which collapses it to 1x1px
(`width: 1px; height: 1px; position: absolute; clip: rect(0 0 0 0)`). The result
is that the screen reader focus ring shows up as a tiny square in the corner of
the component, disconnected from the visual focus. That is confusing for users
with low vision who rely on both the visual focus cue and the assistive
technology outline.

## What changed

Expose `inputClassName` and `inputStyle` on Checkbox, CheckboxField, Radio,
RadioField, CheckboxButton, and RadioButton so users can size and position the
hidden input to encompass the visible component (for example `inputStyle={{inset: 0}}`),
making the screen reader focus ring match the visual one.

The props follow the existing `inputRef` pattern already on these components and
are optional, so there is no behavior change by default.

## Testing

Added tests for Checkbox/CheckboxField and Radio/RadioField verifying that
`inputClassName` and `inputStyle` are applied to the native input, plus the
Button variants when passed directly. All 128 tests in the Checkbox and
RadioGroup suites pass, `check-types` and lint are clean.

Fixes #9687

## Findings

While implementing this fix I found a couple of related cases that are out of scope for this PR but worth flagging:

- **Switch uses the same pattern** as Checkbox and Radio: its native input is rendered inside `VisuallyHidden` and collapsed to 1x1px, so it likely has the same screen reader focus indicator issue. It does not have `inputClassName`/`inputStyle` either. Since #9687 only mentions Checkbox and Radio, I did not expand the scope here, but Switch is a good candidate for a follow-up.
- **Slider, Table, and HiddenDateInput** also render a native input inside `VisuallyHidden`. These are different cases (range input, selection, and date input respectively), but if the same fix is wanted across the library, the `inputClassName`/`inputStyle` pattern could be extended consistently.

Happy to follow up on Switch if the maintainers want it. Otherwise these are documented for future work.
