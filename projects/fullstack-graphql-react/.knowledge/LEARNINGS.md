# LEARNINGS — Cross-Chapter Insights

*To be populated as we progress through chapters.*

## Chapter 1

### Insight: Tooling churn is the norm, concepts are stable
The book's webpack + Babel setup (2020) is completely replaced by Vite (2026), but the *concepts* are identical: bundler, transpiler, dev server, HMR, CSS handling, production build. The specific tools change, the architecture doesn't.

**Pattern:** When processing technical books, identify the *conceptual layer* (bundling, transpilation, state management) separately from the *tooling layer* (webpack vs Vite, Babel vs esbuild). Update the tooling, preserve the concepts.

### Insight: react-helmet is a cautionary tale
A once-standard package that went unmaintained for 6+ years. The community fork (`react-helmet-async`) exists but the real lesson is: prefer solutions built into the framework (React 19's document head API via `react-dom`) over third-party head managers when possible.

**Pattern:** Before adopting a third-party package for framework-level concerns (head management, routing, data fetching), check if the framework has a built-in solution first.

### Insight: Entry point APIs change, patterns persist
`ReactDOM.render` → `createRoot` is a signature change, not a conceptual one. The pattern of "render a React tree into a DOM node" is unchanged. The migration is mechanical.

**Pattern:** API deprecations in React are well-documented and usually have codemods. When processing a book that uses deprecated APIs, check the React blog for the migration path rather than trying to make the old code work.
