# ADR-015: BinarySearch `lesserOrEquals` Bug Fix

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book's binary search implementation uses `lesserOrEquals(low, high, compareFn)` as the while-loop condition. The `lesserOrEquals` function calls `compareFn(a, b)` which compares values, not indices. Since `low` and `high` are array indices (numbers), using `compareFn` on them is incorrect — it treats indices as values to compare.

**The bug:**
```js
// Book's code (wrong):
while (lesserOrEquals(low, high, compareFn)) { ... }

// lesserOrEquals calls compareFn(low, high)
// compareFn compares values, not indices
// For indices 0 and 7: compareFn(0, 7) returns LESS_THAN → works by accident
// But the intent is wrong — it should just be low <= high
```

**Decision:**
- Replace `lesserOrEquals(low, high, compareFn)` with `low <= high`
- The `lesserOrEquals` function is still available for value comparisons where needed
- This is a correction to the book's code, not a style choice

**Consequences:**
- Binary search works correctly for all inputs
- No accidental reliance on numeric comparison of indices
- The fix is minimal (one line change)
