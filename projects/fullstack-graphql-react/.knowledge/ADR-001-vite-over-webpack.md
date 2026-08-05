# ADR-001: Replace webpack + Babel with Vite

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 1
**Scope:** Global

## Context

The book uses webpack 5 with Babel presets (`@babel/preset-env`, `@babel/preset-react`) for bundling and transpilation. This was standard in 2020-2021 but has been superseded.

## Decision

Replace webpack + Babel with Vite 8 for all frontend bundling.

## Rationale

- **Zero-config JSX:** Vite uses esbuild for transpilation, which handles JSX natively without Babel presets
- **Native ESM:** Vite serves native ES modules in development, no bundling needed until production
- **Faster builds:** esbuild is 10-100x faster than Babel for transpilation
- **CSS handling:** Vite imports CSS natively, no need for `style-loader`/`css-loader`/`MiniCssExtractPlugin`
- **HMR:** Vite's HMR is instant and preserves state across edits
- **Production builds:** Vite uses Rollup internally, producing optimized bundles with automatic CSS extraction
- **Smaller config:** ~5 lines vs ~50 lines for webpack

## Consequences

- No `.babelrc` needed
- No `webpack.client.config.js` or `webpack.client.build.config.js`
- Entry point is `index.html` with `<script type="module">` instead of webpack HTML plugin
- `npm run dev` replaces `npm run client`
- `npm run build` replaces `npm run client:build`
- Development server port configured in `vite.config.js` instead of webpack devServer

## References

- https://vite.dev
- https://esbuild.github.io
