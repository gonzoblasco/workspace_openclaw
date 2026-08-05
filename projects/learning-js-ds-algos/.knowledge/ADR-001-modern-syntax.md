# ADR-001: Modern JavaScript Syntax Overhaul

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book (2018, 3rd edition) uses `var`, constructor functions, and `prototype` for OOP. These patterns are outdated and considered bad practice in modern JavaScript (ES2026+).

**Decision:**
- Replace all `var` declarations with `const` (immutable bindings) or `let` (mutable bindings) as appropriate
- Replace constructor functions + `prototype` with ES6 `class` syntax
- Use template literals (`` `text ${expr}` ``) instead of string concatenation (`'text ' + expr`)
- Use ES modules (`import`/`export`) instead of global script tags for Node.js examples
- Use arrow functions where appropriate (callbacks, array methods)

**Consequences:**
- Code is idiomatic modern JavaScript, aligned with current best practices
- Easier to read and maintain
- Students learn patterns they'll actually use in real projects
- Minor divergence from the book text, but concepts remain identical

---

# ADR-002: ES Modules Over Inline Scripts

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book uses inline `<script>` tags and global function declarations. For Node.js examples, it uses CommonJS (`require`). Modern Node.js (v22 LTS) fully supports ES modules.

**Decision:**
- All code examples use ES module syntax (`import`/`export`)
- `package.json` includes `"type": "module"`
- Browser examples use `<script type="module">` where applicable
- Node.js examples run directly with `node filename.js`

**Consequences:**
- No `require()` calls
- Top-level `await` available
- Strict mode by default in modules
- Consistent module system across browser and Node.js

---

# ADR-003: No Global Package Installs

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book recommends `npm install http-server -g` for a local web server. Global installs are discouraged in modern Node.js workflows.

**Decision:**
- Use `npx http-server` instead of global install
- Alternatively, use Node.js built-in `node --watch` for development
- Project-level `package.json` scripts for common tasks

**Consequences:**
- No global dependencies
- Reproducible setup across machines
- One less thing to install
