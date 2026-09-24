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
| ADR-044 | [Methodology Audit - Marco de 8 Fases como Lente de Auditoría](./ADR-044-methodology-audit-framework.md) | workspace |
| ADR-045 | [Motor del Pipeline A/B - DeepSeek V4.1 Flash](./ADR-045-motor-pipeline-deepseek-v4.1-flash.md) (superseded por ADR-046) | workspace |
| ADR-046 | [Revert del Motor del Pipeline A/B - DeepSeek V4 Flash (por costo)](./ADR-046-motor-pipeline-revert-deepseek-v4-flash.md) | workspace |
| ADR-047 | [Kanam Design System como identidad transversal de todo producto](./ADR-047-kanam-design-system.md) | workspace |
| ADR-048 | [Radix/shadcn como capa de UI - adopcion con criterio, no por precedente](./ADR-048-shadcn-radix-stack-ui.md) | workspace |
| ADR-049 | [Claude Code como motor del pipeline A/B (Qwen Code a fallback)](./ADR-049-claude-code-motor-pipeline-ab.md) | workspace |
| ADR-050 | [La memoria de Kanam OS sigue en SQLite local - umbral de migracion a Postgres/Supabase](./ADR-050-memoria-sqlite-local-umbral-migracion.md) | workspace |
| ADR-051 | [Regla de extraccion de lib/ai compartido (construir solo con divergencia real)](./ADR-051-regla-lib-ai-shared.md) | workspace |
| ADR-052 | [Engram como memoria persistente de los agentes de pipeline (standalone, no gentle-ai)](./ADR-052-engram-memoria-agentes-pipeline.md) | workspace |
| ADR-053 | [Modelos primario, auxiliar y alternativo (thinking HIGH unificado)](./ADR-053-modelos-primario-auxiliar-alternativo.md) | workspace |
| ADR-054 | [Kanam OS como app local de lectura sobre memory.db (Next.js + node:sqlite)](./ADR-054-kanam-os-app-local-memoria.md) | workspace |
| ADR-055 | [Bloques managed - settings de la DB propagados a documentos de identidad](./ADR-055-bloques-managed-settings-db.md) | workspace |
| ADR-056 | [Guardas de gobernanza en el pre-commit - guion comun y rutas citadas](./ADR-056-guardas-gobernanza-pre-commit.md) | workspace |
| ADR-057 | [Embeddings en BLOB float32, no JSON de texto](./ADR-057-embeddings-blob-float32.md) | workspace |
| ADR-058 | [Taxonomia normalizada, tabla gemela absorbida y una FK espuria](./ADR-058-taxonomia-normalizada-fk-espuria.md) | workspace |
| ADR-059 | [Contenido markdown descompuesto en campos consultables](./ADR-059-contenido-descompuesto-campos.md) | workspace |
| ADR-060 | [Foreign keys activas en todas las conexiones](./ADR-060-foreign-keys-activas.md) | workspace |
| ADR-061 | [Campos interpretados con revision, y un eje por columna](./ADR-061-campos-interpretados-con-revision.md) | workspace |
| ADR-062 | [Vectores re-cortados por unidad semantica, sin duplicar el texto](./ADR-062-vectores-rechunk-semantico.md) | workspace |
| ADR-063 | [kanam-insight en Python sobre LangChain, no en TypeScript con Bun](./ADR-063-kanam-insight-python-langchain.md) | workspace |
| ADR-064 | [memory-wiki como capa analitica de memoria (modo isolated)](./ADR-064-memory-wiki-capa-analitica.md) | workspace |
| ADR-065 | [DB-first vs doc-only - que documentos viven en el ciclo de la DB y cuales no](./ADR-065-db-first-vs-doc-only.md) | workspace |
| ADR-066 | [Los guardias del workspace no leen codigo de proyectos](./ADR-066-guardias-no-dependen-de-codigo-de-proyecto.md) | workspace |

## Formato

Cada ADR sigue el formato estandar (Contexto, Decision, Consecuencias, Alternativas) pero sin referencias al proyecto que lo origino. El campo `Origen` en el indice es solo trazabilidad.

### Campos del header

| Campo | Obligatorio | Contenido |
|---|---|---|
| `Fecha` | Si | `YYYY-MM-DD` |
| `Estado` | Si | `Aceptado` / `Superseded por ADR-NNN` / `Rechazado` |
| `Decisores` | Si | Quien decide (`Gonzo` / `Gonzo / Kanam`) |
| `Origen` | Si | De donde salio la decision (workspace, proyecto, libro, evaluacion externa) |
| `Relacionado` | No | ADRs vinculados |
| `Supersede` / `Revierte` / `Reemplaza` | No | Solo si aplica, con el ADR referenciado |

**Idioma del header: por generacion, no por archivo.** Los ADR-001 a ADR-046 (hasta 2026-09-14) usan los campos en ingles (`Status`, `Source`, `Scope`); los ADR-047 en adelante usan la forma en español (`Estado`, `Origen`, `Decisores`), consistente con la regla de idioma por capa del workspace. No es deuda: es un cambio de convencion deliberado y el corte esta limpio. Un ADR nuevo sigue el estilo de su generacion (hoy: español).

**`Source` y `Origen` coexisten en los ADR-020 a ADR-036 y NO son lo mismo:** `Origen` es el slug corto de procedencia (trazabilidad, `fullstack-graphql-react`) y `Source` la referencia bibliografica larga (`Extracted from Full-Stack GraphQL + React book processing`). En la generacion en español solo se conserva `Origen`.

**`Scope`** (solo los ADR-020 a ADR-039) declara el alcance de aplicacion (`Global - all React projects` / `Workspace - sistema de memoria`). Es el campo que separa una decision global de una de proyecto.

**Campos historicos sin poblado uniforme:** `Deciders` figura en 17 de los 46 ADR en ingles (los primeros, ADR-001 a ADR-007, y los ultimos del bloque, ADR-037 a ADR-046). Los ADR-008 a ADR-036 no lo llevan. Si se toca uno de esos archivos, agregarlo; no vale un barrido masivo por si solo.

## Como agregar

Cuando un ADR de proyecto se identifique como de alcance general, migrarlo aca:
1. Copiar el contenido.
2. Remover referencias especificas del proyecto.
3. Asignar el proximo numero disponible.
4. Agregar al indice.
5. Dejar una nota en el ADR original del proyecto linkeando al global.
