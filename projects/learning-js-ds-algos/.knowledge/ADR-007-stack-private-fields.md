# ADR-007: Stack Implementation — Object-Based with # Private Fields

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book presents three Stack implementations: array-based, object-based with WeakMap for privacy, and discusses Symbol/underscore conventions. The book was written before `#` private fields were standardized (ES2022).

**Decision:**
- Implement Stack using a plain object (`{}`) for storage, with `#count` and `#items` as native private fields
- This gives true privacy (cannot be accessed from outside the class) without WeakMap ceremony
- The array-based version is documented in comments for reference
- The WeakMap/Symbol approaches are not implemented (they were workarounds for pre-ES2022)

**Consequences:**
- True encapsulation — `#items` and `#count` are inaccessible from outside
- Clean syntax — no WeakMap.get/set boilerplate
- Better performance than WeakMap approach (no extra map lookup)
- All methods remain O(1) as in the book's object version
- Cannot be inherited (private fields are not accessible in subclasses), but Stack is not meant to be extended

---

# ADR-008: Native Node.js Test Runner Over Mocha

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book uses Mocha + Chai for testing, with Webpack + Babel for bundling. Node.js now has a built-in test runner (`node --test`) since v18, stable in v22 LTS.

**Decision:**
- Use `node --test` with `node:assert` for testing
- No Mocha, Chai, or other test dependencies
- Tests live alongside source code as `*.test.js` files

**Consequences:**
- Zero test dependencies
- Runs with a single `node --test` command
- Consistent with ADR-004 (no Babel/transpiling)
- Slightly different API from Mocha (describe/it are available via `node:test`)
