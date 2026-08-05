# ADR-013: MaxHeap via ReverseCompare (Composition Over Duplication)

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book presents MinHeap and MaxHeap as separate classes. MinHeap has all the logic (insert, extract, siftUp, siftDown). MaxHeap is identical except the comparison is reversed.

**Options considered:**
1. **Duplicate code** — copy MinHeap and flip comparisons (book's alternative)
2. **Extend MinHeap with reverseCompare** — inherit all methods, reverse comparison function
3. **Abstract Heap class** — most OOP-correct but overengineered for this case

**Decision:**
- MaxHeap extends MinHeap and passes a reversed comparison function via `reverseCompare`
- No methods are overridden — all behavior is inherited
- `reverseCompare` simply swaps arguments: `(a, b) => compareFn(b, a)`

**Consequences:**
- Zero code duplication
- If MinHeap has a bug, MaxHeap inherits the fix automatically
- The pattern is reusable for any data structure that needs reversed ordering
- Slightly less obvious than explicit code, but well-documented
