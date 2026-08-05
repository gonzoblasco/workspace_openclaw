# ADR-014: Graph Adjacency List Over Adjacency Matrix

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book presents three graph representations: adjacency matrix, adjacency list, and incidence matrix. For the algorithms in this book (BFS, DFS, shortest path, MST), the adjacency list is the most practical choice.

**Options considered:**
1. **Adjacency matrix** — O(1) edge lookup, but O(V²) memory; sparse graphs waste space
2. **Adjacency list** — O(V + E) memory, efficient for sparse graphs; O(degree) edge lookup
3. **Incidence matrix** — useful when edges > vertices, but uncommon

**Decision:**
- Use adjacency list backed by Dictionary (from Chapter 8)
- Dictionary key = vertex name, value = array of adjacent vertices
- Graph class is standalone with `#` private fields (no inheritance)
- Shortest path and MST algorithms use adjacency matrix as input (standard convention for those algorithms)

**Consequences:**
- Memory-efficient for the sparse graphs used in the book's examples
- BFS/DFS naturally work with adjacency lists
- Dijkstra/Floyd-Warshall/Prim/Kruskal receive adjacency matrix as parameter (not from Graph class)
- Clean separation: Graph class for traversal, matrix functions for path/MST algorithms
