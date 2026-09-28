Yes, and it is the part that makes the association take effect.

Measured in Chrome 153 with the real `VisuallyHidden` wrapper: with `position: absolute` the input's containing block stays inside the wrapper and `anchor()` does not resolve against the anchor. The used values fell back to the wrapper (used `top` 0px, used `width` 145px, box 153x21 - still the VisuallyHidden box). With `position: fixed` the input leaves that containing-block chain and the anchor resolves by name: the box matched the component.

Control to isolate the cause: with the anchor as a sibling instead of an ancestor, `absolute` does work. So it is the ancestor relationship, not `absolute` itself.

It also stays inert without support. With the anchor values dropped (a browser without anchor positioning) the input kept its previous 1x1 VisuallyHidden geometry and did not become a viewport-sized box.

Two related measurements, both in real Chrome:

- A transformed ancestor does not break it; the box still matched the component.
- Scroll tracking is fine. Scrolling an `overflow: auto` container moves the component and the input together. An earlier measurement of mine that suggested otherwise was a false alarm: reading `getBoundingClientRect` in the same tick as the scroll returns the stale anchor position, and it settles on the next frame.
