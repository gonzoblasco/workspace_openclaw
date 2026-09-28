Correct, the tests were LTR only, and I measured RTL in Chrome 153:

- Physical `left` / `top` with `anchor()`: works in RTL.
- Logical `inset-inline-start: anchor(left)`: broken in RTL - the input landed a full box width on the other side (measured -208px). `anchor(right)` was still 8px off.
- The `inset` shorthand (`anchor(top) anchor(right) anchor(bottom) anchor(left)`): works in both LTR and RTL.

So the code now uses the `inset` shorthand for the offsets, `anchor-size` for the size, and there is an RTL browser test.

The logical inline properties do not work here because `anchor()` takes physical sides; routing them through a logical property flips them in RTL.

One correction to my own earlier note: I first measured `anchor-size` on its own coming out 8x6px larger than the component and concluded the shorthand alone was enough. That was wrong, and the browser suite caught it. `inset` positions the input but does not size it: a checkbox or radio input is a replaced control with an intrinsic size, and WebKit leaves it at that intrinsic box (measured 12x12, covering none of the component) while Chromium stretches it. Both declarations are needed, and with both the input box matches the component exactly.
