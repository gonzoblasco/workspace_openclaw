Agreed, and this is better than what we have. Measured in Chromium 153 with the real component structure: `position-anchor: var(--override, <default>)` on the input removes both the layout effect and the per-render `getComputedStyle`, and it also removes the caveat from 2026-09-19 - the name no longer needs a re-render to be picked up, because the cascade resolves it.

One correction, measured: the variable has to be read on both sides. With the variable only on the input's `position-anchor`, a consumer that declares `anchor-name` through a classname is still masked by our inline default - the computed `anchor-name` stayed at the component default and the input stopped covering the component. Wrapping the host declaration in the same variable fixes it:

```
host:  anchor-name:     var(--react-aria-anchor, --react-aria-checkbox-<id>)
input: position-anchor: var(--react-aria-anchor, --react-aria-checkbox-<id>)
```

The override then inherits from the host to the input. Measured working in three cases: no override, override through a classname, and override with no component default present.

This also matches an existing pattern in the repo: `--trigger-anchor-point` (Popover, Tooltip), `--trigger-width`, `--table-row-level` are already public CSS variable API.

Naming is yours. I would keep a `--react-aria-` prefix.

One tradeoff to confirm before I rework: consumers override with this variable instead of declaring their own `anchor-name`, so the stylesheet-classname test from the last round would be replaced by a variable test. If you want to keep `anchor-name`-by-classname working as-is, that path needs the `getComputedStyle` (or a stylesheet rule plus the variable), so it is one or the other.

Per your earlier note, the id stays per instance: measured with four hosts sharing one `anchor-name` and no `anchor-scope`, all four inputs resolved to the same anchor and none covered its own component. `anchor-scope` fixes it, but it shipped later than anchor positioning itself (Chrome 131 vs 125), so a static shared name would break in that window.
