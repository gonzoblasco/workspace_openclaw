Yes, and it is the part that makes the association take effect.

Measured in Chromium 153 with the real `VisuallyHidden` wrapper: with `position: absolute` the input's containing block is inside the component, and `anchor()` / `anchor-size()` did not resolve to the anchor. The used values fell back to the wrapper (used `top` 0px, used `width` 145px, final box 153x21 - still the VisuallyHidden box). With `position: fixed` the input leaves that containing-block chain and the anchor resolves by name: the measured box matched the component (200x40 with the `inset` shorthand).

Control to isolate the cause: with the anchor as a sibling instead of an ancestor, `absolute` does work. So it is the ancestor relationship, not `absolute` itself.

It is also inert without support: with the anchor values dropped (emulating a browser without anchor positioning) the input kept its previous 1x1 VisuallyHidden geometry and did not become a viewport-sized box.

Note for the record: a transformed ancestor did not break it - the box still matched the component.
