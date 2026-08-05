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

## Chapter 2

### Insight: Apollo Server's integration API changed twice in 5 years
From `apollo-server-express` (v3) with `applyMiddleware()` to `@apollo/server` (v4) with `expressMiddleware()` to `@apollo/server` (v5) with `@as-integrations/express5`. The core GraphQL server logic is unchanged — only the Express binding changed.

**Pattern:** When a library changes its integration API, check if the integration has been extracted to a separate package. Apollo Server 5 moved Express integration to `@as-integrations/express5`, keeping the core server package clean.

### Insight: Express 5 broke the wildcard catch-all
`app.get('*', ...)` was a standard Express 4 pattern. Express 5's `path-to-regexp` v8 no longer supports bare `*`. The fix is trivial (`app.use(...)` instead) but the pattern was so common that it breaks silently at startup.

**Pattern:** When upgrading Express 4 → 5, check all route patterns. Any `'*'` or unnamed wildcard parameters need updating. Express 5 uses named parameters only (`/:path*`).

### Insight: Node.js built-in features eliminate dev dependencies
`node --watch` (Node 22) replaces `nodemon` for most use cases. Native ESM (stable since Node 16) replaces `@babel/node` and Babel presets for server code. The trend is clear: Node.js is absorbing its own toolchain.

**Pattern:** Before adding a dev dependency for file watching, transpilation, or module loading, check if Node.js has a built-in equivalent. The gap between Node.js features and third-party tools is shrinking every LTS release.

### Insight: Tooling churn is the norm, concepts are stable
The book's webpack + Babel setup (2020) is completely replaced by Vite (2026), but the *concepts* are identical: bundler, transpiler, dev server, HMR, CSS handling, production build. The specific tools change, the architecture doesn't.

**Pattern:** When processing technical books, identify the *conceptual layer* (bundling, transpilation, state management) separately from the *tooling layer* (webpack vs Vite, Babel vs esbuild). Update the tooling, preserve the concepts.

### Insight: react-helmet is a cautionary tale
A once-standard package that went unmaintained for 6+ years. The community fork (`react-helmet-async`) exists but the real lesson is: prefer solutions built into the framework (React 19's document head API via `react-dom`) over third-party head managers when possible.

**Pattern:** Before adopting a third-party package for framework-level concerns (head management, routing, data fetching), check if the framework has a built-in solution first.

### Insight: Entry point APIs change, patterns persist
`ReactDOM.render` → `createRoot` is a signature change, not a conceptual one. The pattern of "render a React tree into a DOM node" is unchanged. The migration is mechanical.

**Pattern:** API deprecations in React are well-documented and usually have codemods. When processing a book that uses deprecated APIs, check the React blog for the migration path rather than trying to make the old code work.
