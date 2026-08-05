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
| ADR-008 | [Replace Jest with Vitest](./ADR-008-vitest-over-jest.md) | testing-react-library |
| ADR-009 | [TypeScript for test files](./ADR-009-typescript-for-tests.md) | testing-react-library |
| ADR-010 | [Prefer screen queries over render destructuring](./ADR-010-screen-queries-over-destructuring.md) | testing-react-library |
| ADR-011 | [Use userEvent over fireEvent](./ADR-011-userevent-over-fireevent.md) | testing-react-library |
| ADR-012 | [Use jest-dom matchers for DOM assertions](./ADR-012-jest-dom-matchers.md) | testing-react-library |

## Formato

Cada ADR sigue el formato estandar (Contexto, Decision, Consecuencias, Alternativas) pero sin referencias al proyecto que lo origino. El campo `Origen` en el indice es solo trazabilidad.

## Como agregar

Cuando un ADR de proyecto se identifique como de alcance general, migrarlo aca:
1. Copiar el contenido.
2. Remover referencias especificas del proyecto.
3. Asignar el proximo numero disponible.
4. Agregar al indice.
5. Dejar una nota en el ADR original del proyecto linkeando al global.
