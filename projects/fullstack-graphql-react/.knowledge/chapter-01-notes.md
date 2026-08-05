# Chapter 1: Preparing Your Development Environment

## Core Concepts

1. **GraphQL vs REST:** GraphQL allows querying specific fields, making it efficient for multi-platform apps
2. **Apollo Server:** GraphQL server for Node.js ecosystem, works with Express.js
3. **React + Apollo Client:** Frontend integration for GraphQL
4. **Component architecture:** Split UI into reusable components
5. **useState hook:** State management in functional components
6. **Controlled inputs:** Form inputs bound to React state
7. **Virtual DOM:** Efficient re-rendering by diffing virtual vs real DOM

## Stack (Book Original)
- Node.js 14 LTS
- Express.js + Apollo Server
- MySQL + Sequelize ORM
- React + Apollo Client
- webpack 5 + Babel
- react-helmet

## Stack (Updated - August 2026)
- Node.js 22 LTS (jod)
- Express.js + Apollo Server (still standard)
- MySQL + Sequelize ORM (or Prisma as modern alternative)
- React 19 + Apollo Client
- **Vite 8** (replaces webpack + Babel)
- **react-helmet-async** (replaces deprecated react-helmet)
- **createRoot** API (replaces ReactDOM.render)

## Key Changes from Book

| Book | Modern Replacement | Reason |
|---|---|---|
| webpack 5 + Babel | Vite 8 | esbuild is 10-100x faster, zero-config JSX |
| react-helmet | react-helmet-async | react-helmet unmaintained since 2020 |
| ReactDOM.render | createRoot | Removed in React 19 |
| style-loader/css-loader | Vite native CSS | Vite handles CSS imports automatically |
| MiniCssExtractPlugin | Vite build (Rollup) | Automatic in production builds |
| .babelrc | Not needed | Vite uses esbuild, no Babel config required |

## Architecture (Logical Request Flow)
1. Client requests site → Express.js serves static HTML
2. Client downloads bundled JS (React app)
3. React app makes GraphQL requests to Apollo Server
4. Apollo queries data sources (SQL, third-party)
5. Apollo returns JSON → React renders as HTML

## ADRs Created
- ADR-001: Replace webpack + Babel with Vite
- ADR-002: Replace react-helmet with react-helmet-async
- ADR-003: Use createRoot instead of ReactDOM.render

## Running the Chapter 1 Project

```bash
cd projects/fullstack-graphql-react/chapter-01
npm run dev    # Development server
npm run build  # Production build
```
