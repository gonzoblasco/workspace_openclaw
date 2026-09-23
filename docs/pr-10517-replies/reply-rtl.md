Correct, the tests were LTR only, and I measured RTL in Chrome 153:

- Physical `left` / `top` with `anchor()`: works in RTL.
- Logical `inset-inline-start: anchor(left)`: broken in RTL - the input landed a full box width on the other side (measured -208px). `anchor(right)` was still 8px off.
- The `inset` shorthand (`anchor(top) anchor(right) anchor(bottom) anchor(left)`): works in both LTR and RTL.

So the code now uses the `inset` shorthand, and there is an RTL browser test.

The logical inline properties do not work here because `anchor()` takes physical sides; routing them through a logical property flips them in RTL.

One extra measurement while switching: the shorthand is also exact. With `width: anchor-size(width)` the box came out 8x6px larger than the component (`anchor-size` sizes the content box, and the input's UA border and padding are added on top). The shorthand sized it exactly. The previous test passed anyway because it allowed up to 2px of overshoot, so it was not catching that.
