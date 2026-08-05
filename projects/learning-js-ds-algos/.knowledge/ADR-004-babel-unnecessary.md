# ADR-004: Babel.js and Transpiling Are Unnecessary for This Project

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book dedicates significant space to Babel.js, `.mjs` files, `--experimental-modules` flag, and transpiling ES2015+ to CommonJS. These were necessary workarounds in 2018 when Node.js didn't support ES modules natively.

**Decision:**
- No Babel.js dependency in this project
- No transpiling step
- All code runs natively on Node LTS (v22.x) as ES modules
- `package.json` with `"type": "module"` is sufficient
- If browser compatibility were needed, we'd use a bundler (Vite/esbuild), not Babel standalone

**Consequences:**
- Zero build step for development
- Simpler project setup
- Students see the real modern workflow, not historical workarounds
- The concepts (modules, imports/exports) are the same, just without the ceremony

---

# ADR-005: TypeScript as devDependency, Not Global Install

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book recommends `npm install -g typescript`. Global installs are discouraged in modern Node.js workflows.

**Decision:**
- TypeScript is added as a devDependency if/when needed
- Use `npx tsc` to compile
- No global TypeScript install

**Consequences:**
- Reproducible across machines
- Version-locked per project
- Consistent with ADR-003 (no global package installs)

---

# ADR-006: ES Modules Are the Default, No Flags Needed

**Date:** 2026-08-05
**Status:** Accepted
**Context:** The book describes `.mjs` extension and `--experimental-modules` flag as requirements for ES modules in Node.js. These were experimental in Node 8.5 (2017) and stable since Node 14 (2020).

**Decision:**
- All `.js` files are ES modules via `"type": "module"` in package.json
- No `.mjs` extension needed
- No `--experimental-modules` flag
- `import`/`export` work natively

**Consequences:**
- Cleaner file extensions
- No special flags to remember
- Code matches what developers actually write today
