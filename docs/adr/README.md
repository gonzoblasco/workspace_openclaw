# ADRs Globales

Decisiones de arquitectura de alcance general, aplicables a cualquier proyecto del workspace.

## Indice

| # | Titulo | Origen |
|---|---|---|
| ADR-001 | [Patron convergente](./ADR-001-patron-convergente.md) | ai-engineering-bootcamp |
| ADR-002 | [Primitives, Conventions, Levers](./ADR-002-primitives-conventions-levers.md) | remix-book |
| ADR-003 | [Server/Client file naming convention](./ADR-003-server-client-file-convention.md) | remix-book |
| ADR-004 | [Next.js full-stack platform](./ADR-004-nextjs-fullstack-platform.md) | sportcars |
| ADR-005 | [Supabase BaaS](./ADR-005-supabase-baas.md) | sportcars |
| ADR-006 | [Capacidad Computacional - DeepSeek V4 Flash con Reasoning Maximum](./ADR-006.md) | kanam-workflow |
| ADR-007 | [Patrones de Agente Autonomo - Goal-Oriented Architecture](./ADR-007.md) | kanam-workflow |
| ADR-008 | [Replace Jest with Vitest](./ADR-008-vitest-over-jest.md) | testing-react-library |
| ADR-009 | [TypeScript for test files](./ADR-009-typescript-for-tests.md) | testing-react-library |
| ADR-010 | [Prefer screen queries over render destructuring](./ADR-010-screen-queries-over-destructuring.md) | testing-react-library |
| ADR-011 | [Use userEvent over fireEvent](./ADR-011-userevent-over-fireevent.md) | testing-react-library |
| ADR-012 | [Use jest-dom matchers for DOM assertions](./ADR-012-jest-dom-matchers.md) | testing-react-library |
| ADR-013 | [Vite as Default Bundler Over webpack](./ADR-013-vite-default-bundler.md) | fullstack-graphql-react |
| ADR-014 | [createRoot API for React Entry Point](./ADR-014-createRoot-api.md) | fullstack-graphql-react |
| ADR-015 | [Node --watch for Development Server Reload](./ADR-015-node-watch.md) | fullstack-graphql-react |
| ADR-016 | [Drizzle ORM as Default SQL ORM](./ADR-016-drizzle-orm.md) | fullstack-graphql-react |
| ADR-017 | [Apollo Client React Hooks from @apollo/client/react](./ADR-017-apollo-client-react-imports.md) | fullstack-graphql-react |
| ADR-018 | [Enfoque Iterativo para Adopcion de Tooling](./ADR-018-enfoque-iterativo-tooling.md) | react-18-design-patterns |
| ADR-019 | [Convencion de Nomenclatura TypeScript: Sin Prefijos I/T](./ADR-019-sin-prefijos-IT.md) | react-18-design-patterns |
| ADR-020 | [tsconfig Moderno con Vite (2026)](./ADR-020-tsconfig-moderno-vite.md) | react-18-design-patterns |
| ADR-021 | [Biome como Toolchain Unificado](./ADR-021-biome-toolchain.md) | react-18-design-patterns |
| ADR-022 | [Custom Hooks como Estandar para Compartir Logica](./ADR-022-custom-hooks-estandar.md) | react-18-design-patterns |
| ADR-023 | [Patron de Controlled Components con Single Change Handler](./ADR-023-controlled-components-single-handler.md) | react-18-design-patterns |
| ADR-024 | [CSS Modules con Vite (Zero-Config)](./ADR-024-css-modules-vite.md) | react-18-design-patterns |
| ADR-025 | [Memoizacion Bajo Demanda (No Prematura)](./ADR-025-memoizacion-bajo-demanda.md) | react-18-design-patterns |
| ADR-026 | [Concurrent Mode como Default (React 19)](./ADR-026-concurrent-mode-default.md) | react-18-design-patterns |
| ADR-027 | [Server Components como Estandar de SSR](./ADR-027-server-components-estandar.md) | react-18-design-patterns |
| ADR-028 | [bcrypt para Password Hashing (No SHA1)](./ADR-028-bcrypt-password-hashing.md) | react-18-design-patterns |
| ADR-029 | [Turborepo + pnpm como Estandar para Monorepos](./ADR-029-turborepo-pnpm-monorepo.md) | react-18-design-patterns |

## Formato

Cada ADR sigue el formato estandar (Contexto, Decision, Consecuencias, Alternativas) pero sin referencias al proyecto que lo origino. El campo `Origen` en el indice es solo trazabilidad.

## Como agregar

Cuando un ADR de proyecto se identifique como de alcance general, migrarlo aca:
1. Copiar el contenido.
2. Remover referencias especificas del proyecto.
3. Asignar el proximo numero disponible.
4. Agregar al indice.
5. Dejar una nota en el ADR original del proyecto linkeando al global.
