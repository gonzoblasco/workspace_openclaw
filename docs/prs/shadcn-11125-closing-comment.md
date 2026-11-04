Closing the loop after the merge

Merged as `4aaea19` on Nov 2. One correction to the second paragraph of my Aug 31 comment above, since it left the wrong impression of where this was stuck.

I said the bottleneck was that #11465 had sat on a single COMMENTED review for three weeks, and implicitly that a re-review was what it needed. That was wrong. Two days later shadcn took a pass and found three real bugs in `drainReleasedSpacer` that the jsdom suite structurally could not see - most notably that `syncAfterScroll` fires on the programmatic scroll that places an anchored turn, so in a real browser the drain yanked every anchored reply to the bottom, which is the exact bug this PR set out to fix. The blocker was the code, not the review latency, and daltino's re-review was never the thing standing in the way.

The merged version gates the drain on `anchored-to-message` / `settling-jump` / `autoscrollingRef`, recomputes the remaining room from absolute geometry on every event instead of subtracting a delta, and hands off to `scrollToEnd` only at the real bottom. Browser-mode tests cover both regressions.

Worth recording for anyone reading this later: the design that landed is the one @sandengocka proposed here on Aug 3 - gate the re-arm on `spacerHeight === 0`, drain in `handleResize` with `max(0, ...)`. My PR (#11465) implements it; the shape came from that comment.
