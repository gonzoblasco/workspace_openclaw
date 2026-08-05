# ADR-016: Floyd-Warshall `Number.isFinite` Edge Case Fix

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book's Floyd-Warshall implementation uses `Number.isFinite(graph[i][j])` to check if an edge exists. However, the book's convention uses `0` to represent "no edge" in the adjacency matrix. `Number.isFinite(0)` returns `true`, so edges with weight 0 are treated as valid connections, and non-edges (also 0) are incorrectly treated as valid.

**The bug:**
```js
// Book's code (wrong for 0 = no-edge convention):
} else if (Number.isFinite(graph[i][j])) {
  dist[i][j] = graph[i][j];  // 0 is finite, so "no edge" becomes distance 0
```

**Decision:**
- Replace `Number.isFinite(graph[i][j])` with `graph[i][j] > 0`
- This correctly distinguishes between "no edge" (0) and actual edges (positive weights)
- For graphs that may include 0-weight edges, a different convention would be needed, but the book's examples only use positive weights

**Consequences:**
- Floyd-Warshall produces correct shortest paths for the book's example graphs
- The fix is consistent with how Dijkstra's algorithm handles the same matrix (it already uses `graph[u][v] !== 0`)
- If 0-weight edges were needed, we'd need a sentinel value (e.g., `Infinity` or `null`) instead of 0
