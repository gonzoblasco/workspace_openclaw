# ADRs Globales

Decisiones de arquitectura de alcance general, aplicables a cualquier proyecto del workspace.

## Indice

| # | Titulo | Origen |
|---|---|---|
| ADR-001 | [Product Pipeline Integration](./ADR-001-product-pipeline-integration.md) | kanam-workflow |
| ADR-002 | [OpenSpec as Primary Doc Format](./ADR-002-openspec-primary-doc-format.md) | kanam-workflow |
| ADR-003 | [Product Reset Phase Triggers](./ADR-003-product-reset-triggers.md) | kanam-workflow |
| ADR-004 | [Growth Strategy Triggers](./ADR-004-growth-strategy-triggers.md) | kanam-workflow |
| ADR-005 | [OSS Contribution Pipeline](./ADR-005-oss-contribution-pipeline.md) | kanam-workflow |
| ADR-006 | [Capacidad Computacional - DeepSeek V4 Flash con Reasoning Maximum](./ADR-006-capacidad-computacional-deepseek.md) | kanam-workflow |
| ADR-007 | [Patrones de Agente Autonomo - Goal-Oriented Architecture](./ADR-007-patrones-agente-autonomo.md) | kanam-workflow |
| ADR-008 | [Patron convergente](./ADR-008-patron-convergente.md) | ai-engineering-bootcamp |
| ADR-009 | [Primitives, Conventions, Levers](./ADR-009-primitives-conventions-levers.md) | remix-book |
| ADR-010 | [Server/Client file naming convention](./ADR-010-server-client-file-convention.md) | remix-book |
| ADR-011 | [Next.js full-stack platform](./ADR-011-nextjs-fullstack-platform.md) | sportcars |
| ADR-012 | [Supabase BaaS](./ADR-012-supabase-baas.md) | sportcars |
| ADR-013 | [Replace Jest with Vitest](./ADR-013-vitest-over-jest.md) | testing-react-library |
| ADR-014 | [TypeScript for test files](./ADR-014-typescript-for-tests.md) | testing-react-library |
| ADR-015 | [Data Fetching con TanStack Query](./ADR-015-data-fetching-tanstack-query.md) | testing-react-library |
| ADR-016 | [Prefer screen queries over render destructuring](./ADR-016-screen-queries-over-destructuring.md) | testing-react-library |
| ADR-017 | [Preferir Hooks sobre HOCs y Render Props](./ADR-017-hooks-sobre-hocs.md) | testing-react-library |
| ADR-018 | [Use userEvent over fireEvent](./ADR-018-userevent-over-fireevent.md) | testing-react-library |
| ADR-019 | [Use jest-dom matchers for DOM assertions](./ADR-019-jest-dom-matchers.md) | testing-react-library |
| ADR-020 | [Vite as Default Bundler Over webpack](./ADR-020-vite-default-bundler.md) | fullstack-graphql-react |
| ADR-021 | [createRoot API for React Entry Point](./ADR-021-createroot-api.md) | fullstack-graphql-react |
| ADR-022 | [Node --watch for Development Server Reload](./ADR-022-node-watch.md) | fullstack-graphql-react |
| ADR-023 | [Drizzle ORM as Default SQL ORM](./ADR-023-drizzle-orm.md) | fullstack-graphql-react |
| ADR-024 | [Apollo Client React Hooks from @apollo/client/react](./ADR-024-apollo-client-react-imports.md) | fullstack-graphql-react |
| ADR-025 | [Enfoque Iterativo para Adopcion de Tooling](./ADR-025-enfoque-iterativo-tooling.md) | react-18-design-patterns |
| ADR-026 | [Convencion de Nomenclatura TypeScript: Sin Prefijos I/T](./ADR-026-sin-prefijos-it.md) | react-18-design-patterns |
| ADR-027 | [tsconfig Moderno con Vite (2026)](./ADR-027-tsconfig-moderno-vite.md) | react-18-design-patterns |
| ADR-028 | [Biome como Toolchain Unificado](./ADR-028-biome-toolchain.md) | react-18-design-patterns |
| ADR-029 | [Custom Hooks como Estandar para Compartir Logica](./ADR-029-custom-hooks-estandar.md) | react-18-design-patterns |
| ADR-030 | [Patron de Controlled Components con Single Change Handler](./ADR-030-controlled-components-single-handler.md) | react-18-design-patterns |
| ADR-031 | [CSS Modules con Vite (Zero-Config)](./ADR-031-css-modules-vite.md) | react-18-design-patterns |
| ADR-032 | [Memoizacion Bajo Demanda (No Prematura)](./ADR-032-memoizacion-bajo-demanda.md) | react-18-design-patterns |
| ADR-033 | [Concurrent Mode como Default (React 19)](./ADR-033-concurrent-mode-default.md) | react-18-design-patterns |
| ADR-034 | [Server Components como Estandar de SSR](./ADR-034-server-components-estandar.md) | react-18-design-patterns |
| ADR-035 | [bcrypt para Password Hashing (No SHA1)](./ADR-035-bcrypt-password-hashing.md) | react-18-design-patterns |
| ADR-036 | [Turborepo + pnpm como Estandar para Monorepos](./ADR-036-turborepo-pnpm-monorepo.md) | react-18-design-patterns |
| ADR-037 | [Lucide como iconos base](./ADR-037-lucide-iconos-base.md) | react-18-design-patterns |
| ADR-038 | [Learnings con mirror en DB (categorias + consulta veloz)](./ADR-038-learnings-mirror-db.md) | workspace |
| ADR-039 | [Changesets - cuando usarlos y como (release de librerias)](./ADR-039-changesets-cuando-y-como.md) | workspace |
| ADR-040 | [Seleccion de Modelos por Tipo de Tarea](./ADR-040-modelos-seleccion-por-tarea.md) | workspace |
| ADR-041 | [Motor LLM del Sistema - GLM-5.3-Flash](./ADR-041-motor-llm-glm-5.3-flash.md) | workspace |
| ADR-042 | [Mercado Pago como Proveedor de Pagos (Nunca Stripe)](./ADR-042-mercado-pago-pagos-latam.md) | workspace |
| ADR-043 | [Complexity-Driven Pipeline (Orquestación por T-Score)](./ADR-043-complexity-driven-pipeline.md) | workspace |
| ADR-044 | [Methodology Audit - Marco de 8 Fases como Lente de Auditoría](./ADR-044-methodology-audit-framework.md) | workspace (propuesto) |

## Formato

Cada ADR sigue el formato estandar (Contexto, Decision, Consecuencias, Alternativas) pero sin referencias al proyecto que lo origino. El campo `Origen` en el indice es solo trazabilidad.

## Como agregar

Cuando un ADR de proyecto se identifique como de alcance general, migrarlo aca:
1. Copiar el contenido.
2. Remover referencias especificas del proyecto.
3. Asignar el proximo numero disponible.
4. Agregar al indice.
5. Dejar una nota en el ADR original del proyecto linkeando al global.
