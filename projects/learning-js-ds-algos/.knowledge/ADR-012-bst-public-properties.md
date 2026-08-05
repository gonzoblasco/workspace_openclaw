# ADR-012: BST Public Properties for Inheritance (Trees Chapter)

**Date:** 2026-08-05
**Status:** Accepted
**Context:** BinarySearchTree, AVLTree, and RedBlackTree form an inheritance chain where AVLTree and RedBlackTree extend BinarySearchTree. JavaScript `#` private fields (ES2022) are not accessible from subclasses, making true encapsulation impossible for inherited classes.

**Options considered:**
1. **Public properties** — works with inheritance, no encapsulation
2. **`#` private fields** — breaks inheritance entirely
3. **WeakMap** — works but verbose
4. **Composition over inheritance** — cleanest but diverges from the book

**Decision:**
- BST uses public properties (`root`, `compareFn`) — same approach as LinkedList family (ADR-009)
- Internal helper methods use `#` private methods where possible
- AVLTree and RedBlackTree extend BST and access `root`/`compareFn` directly

**Consequences:**
- Inheritance works as the book intends
- Internal properties are accessible from outside (same limitation as the book)
- Consistent with ADR-009 pattern for inherited data structures
- If TC39 adds `protected` in the future, we can migrate
