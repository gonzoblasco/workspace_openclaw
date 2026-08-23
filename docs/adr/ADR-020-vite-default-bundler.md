# ADR-020: Vite Default Bundler

**Status:** Accepted
**Fecha:** 2026-08-05
**Origen:** fullstack-graphql-react
**Source:** Extracted from Full-Stack GraphQL + React book processing
**Scope:** Global - all new React/TypeScript projects

## Context

webpack 5 with Babel has been the standard React bundler for years. However, the ecosystem has shifted. Vite offers a fundamentally faster development experience by leveraging native ESM and esbuild.

## Decision

Use Vite as the default bundler for all new frontend projects. webpack is only considered when a specific plugin or requirement has no Vite equivalent.

## Rationale

- **Speed:** esbuild transpilation is 10-100x faster than Babel
- **Zero-config JSX:** No Babel presets needed for React/JSX
- **Native ESM:** Dev server serves native modules, no bundling until production
- **CSS:** Native CSS import support, no loaders needed
- **HMR:** Instant hot module replacement that preserves state
- **Production:** Rollup-based builds with automatic code splitting and CSS extraction
- **Ecosystem:** All major libraries (React, Vue, Svelte, Solid) have first-class Vite support
- **Config:** ~5 lines vs 50+ lines for equivalent webpack config

## Consequences

- No `.babelrc` or Babel config files
- No webpack config files
- Entry point is `index.html` with `<script type="module">`
- `npm run dev` for development, `npm run build` for production
- Port and proxy config in `vite.config.js`

## Migration Path (from webpack)

1. `npm create vite@latest . -- --template react`
2. Move `index.html` to root with `<script type="module">` entry
3. Move `src/` contents, remove webpack configs and Babel config
4. Replace `ReactDOM.render` with `createRoot` (see ADR-003)
5. Update npm scripts

## References

- https://vite.dev
- https://esbuild.github.io
- ADR-003: Use createRoot instead of ReactDOM.render
