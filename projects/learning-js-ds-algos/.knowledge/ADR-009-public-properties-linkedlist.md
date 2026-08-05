# ADR-009: Public Properties for Inherited Data Structures

**Date:** 2026-08-05
**Status:** Accepted
**Context:** JavaScript `#` private fields (ES2022) are not accessible from subclasses. This creates a design tension: LinkedList, DoublyLinkedList, CircularLinkedList, and SortedLinkedList form an inheritance chain where the subclass needs access to `count`, `head`, and `tail`.

**Options considered:**
1. **Public properties** (book's approach) — works with inheritance, no encapsulation
2. **`#` private fields** — true encapsulation, but breaks inheritance entirely
3. **WeakMap** — works with inheritance, but verbose and harder to read
4. **Composition over inheritance** — cleanest but diverges significantly from the book

**Decision:**
- Use public properties (no `#`) for the LinkedList family (LinkedList, DoublyLinkedList, CircularLinkedList, SortedLinkedList)
- Use `#` private fields for standalone classes (Stack, Queue, Deque) that don't participate in inheritance
- Document this as a known limitation of JavaScript's private field implementation

**Consequences:**
- Inheritance works as the book intends
- Internal properties are accessible from outside (same as the book)
- Consistent with the book's approach — the book itself notes that JS doesn't have true private properties
- If TC39 adds `protected` in the future, we can migrate

---

# ADR-010: StackLinkedList Uses DoublyLinkedList Internally

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book implements StackLinkedList using DoublyLinkedList as internal storage, taking advantage of O(1) access to the tail for push/pop operations.

**Decision:**
- Implement StackLinkedList as a wrapper around DoublyLinkedList
- All Stack methods delegate to the internal DoublyLinkedList
- No inheritance — composition

**Consequences:**
- Clean separation of concerns
- O(1) push and pop (tail access)
- Reuses tested DoublyLinkedList code
- Matches the book's design
