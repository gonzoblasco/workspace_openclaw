Done, and it is better than what we had. Measured in Chrome 153 with the real component structure: the custom property removes the layout effect and the per-render `getComputedStyle`, and it also removes the caveat from 2026-09-19 - the name no longer needs a re-render, because the cascade resolves it.

One correction that the implementation needs, measured: the property has to be read on both sides. With it only on the input's `position-anchor`, a consumer that declares `anchor-name` through a class name is still masked by our inline default - the computed `anchor-name` stayed at the component default and the input stopped covering the component. Pointing both the host and the input at the same property fixes it:

```
host:  anchor-name:     var(--react-aria-anchor-name, --react-aria-checkbox-<id>)
input: position-anchor: var(--react-aria-anchor-name, --react-aria-checkbox-<id>)
```

The property inherits, so the override reaches the input from the host. Measured working in the cases that matter: no override, override through a class name, override on an ancestor, and override through the component's inline `style`.

This matches an existing pattern in the repo: `--trigger-anchor-point` (Popover, Tooltip), `--trigger-width` and `--table-row-level` are already public CSS variable API.

Two things worth your call:

1. Naming. I used `--react-aria-anchor-name`; happy to align it with whatever you prefer.
2. Since the override path is the custom property, a consumer setting `anchor-name` directly in a class name is no longer adopted - that is the tradeoff of dropping the `getComputedStyle`. The stylesheet test from the last round became a custom property test. If you would rather keep the direct `anchor-name` override working, we need the computed-style read back for that one case.

The per-instance id stays, for the reason you raised earlier and that I measured: with several elements sharing one `anchor-name`, every input resolved to the same anchor and none covered its own component. `anchor-scope` localizes a shared name, but it shipped later than anchor positioning (Chrome 131 vs 125), so a shared name would break in that window.
