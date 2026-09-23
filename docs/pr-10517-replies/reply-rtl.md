Correct, the browser tests are LTR only. I measured RTL in Chromium 153:

- physical `left` / `top` with `anchor()`: works in RTL.
- logical `inset-inline-start: anchor(left)`: broken in RTL - the input landed a full box width to the other side (-208px). `anchor(right)` was still 8px off.
- the `inset` shorthand `anchor(top) anchor(right) anchor(bottom) anchor(left)`: works in both LTR and RTL.

So yes to `inset`, no to the logical inline properties: `anchor()` takes physical sides, and routing them through a logical property flips them in RTL.

Measured bonus: the shorthand is also exact. With `width: anchor-size(width)` the box came out 8x6 px larger than the component (anchor-size sizes the content box, and the input's UA styles add border and padding). The shorthand sized it exactly, and so did `anchor-size` together with `box-sizing: border-box`.

I will switch to the shorthand and add an RTL browser test.
