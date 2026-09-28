Correction to my note above, because the browser suite proved it wrong.

I wrote that `inset` alone was exact and that `anchor-size` made the box 8x6px too large. The first half was wrong: `inset` positions the input but does not size it, and that is not visible in Chromium, which was the only browser I had checked.

A checkbox or radio input is a replaced control with an intrinsic size. WebKit leaves it at that intrinsic box: measured 12x12, covering none of the component. Chromium stretches the control from `inset` alone, so the tests passed there and failed on WebKit. That is what the CI `test-browser` job caught after the first push.

The fix is to set both: `inset` for the offsets (still the RTL-correct choice) and `width`/`height: anchor-size()` for the size. With both, the input box matches the component exactly. There is also a follow-up correction on the per-instance assertion, which needed to move inside the support check for Firefox.

Both are in the tree now and the browser suite is green across chromium, firefox and webkit.
