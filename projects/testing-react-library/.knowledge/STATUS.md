# STATUS

## Chapter 1 — Exploring React Testing Library ✅

### What Was Done

- Created project structure with `.knowledge/` (BRIEF, ROADMAP, ADRs, LEARNINGS, STATUS)
- Initialized npm project with modern stack (Vitest, React 19, RTL 14+, TypeScript, Biome)
- Implemented all example components from Chapter 1:
  - `Profile` — class component showing/hiding details (converted to functional)
  - `Login` — form with disabled submit until credentials entered
  - `Counter` — add/subtract buttons
- Wrote tests for each component using modern patterns:
  - `userEvent` instead of `fireEvent`
  - `screen` queries instead of render destructuring
  - jest-dom matchers (`toBeInTheDocument`, `toBeDisabled`, `toHaveFormValues`)
  - TypeScript throughout
- Documented 6 ADRs (4 migrated to global `docs/adr/`)
- All tests passing

### Key Deviations from Book

1. **Jest → Vitest:** Faster, native ESM, same API
2. **Class components → Functional:** Hooks are standard
3. **fireEvent → userEvent:** More realistic user simulation
4. **JavaScript → TypeScript:** Type safety
5. **Enzyme examples → Omitted:** Deprecated, not worth implementing

---

## Chapter 2 — Working with React Testing Library ✅

### What Was Done

- Implemented all example components from Chapter 2:
  - `Jumbotron` — presentational component with heading and text
  - `Travel` — presentational component with snapshot test
  - `Table` — component accepting employee array as props
- Wrote tests demonstrating:
  - `getByText` vs `getByRole` for the same element
  - Snapshot testing with `toMatchSnapshot()`
  - `toHaveAttribute()` for class verification
  - `getAllByRole` for counting rows
  - Iterating over mock data to verify all values
- Migrated general ADRs to `docs/adr/` (ADR-008 through ADR-012)
- All 22 tests passing

### Key Deviations from Book

1. **create-react-app → Vite:** CRA is deprecated; Vite is the modern standard
2. **Jest snapshots → Vitest snapshots:** Compatible API, same behavior
3. **Class components → Functional:** Hooks are standard

---

## Chapter 3 — Testing Complex Components ✅

### What Was Done

- Implemented all example components from Chapter 3:
  - `Vote` — useReducer-based voting with like/dislike, single-vote enforcement
  - `VoteBtn` — isolated button component with mock event handler
  - `EmployeeEmail` — input that generates email from name
  - `DrinkSearch` — API-driven search with MSW v2 mocks
  - `Register` — form submission with TDD approach
- Wrote tests demonstrating:
  - `userEvent` for clicks, typing, keyboard events
  - `vi.fn()` for mock functions (Vitest equivalent of `jest.fn()`)
  - MSW v2 with `http.get()` handlers (not deprecated `rest`)
  - `findBy*` for async elements, `queryBy*` for absence
  - TDD workflow (write test → fail → implement → pass → refactor)
- Updated DrinkSearch to handle HTTP error status codes (not just network errors)
- All 37 tests passing across 3 chapters

### Key Deviations from Book

1. **MSW v1 → MSW v2:** `rest.get()` → `http.get()`, `ctx.json()` → `HttpResponse.json()`
2. **`jest.fn()` → `vi.fn()`:** Vitest API
3. **Class Register → Functional:** Hooks from the start (book refactors to functional, we start there)
4. **Error handling:** Added `response.ok` check to catch HTTP errors (book only catches network errors)

---

## Chapter 4 — Integration Testing and Third-Party Libraries ✅

### What Was Done

- Implemented all example patterns from Chapter 4:
  - **Context API:** `RetailContext` with Provider, `Cart`, `ProductDetail`, `ProductCard`, `Retail`
  - **Integration tests:** View product details, add to cart, add to favorites
  - **Error boundary test:** Context error when used outside Provider
  - **Redux custom render:** `test-utils.tsx` with `configureStore` + `preloadedState`
  - **GraphQL via MSW v2:** `EmployeeFetcher` with fetch + MSW intercepting GraphQL endpoint
  - **MUI Vote:** `MuiVote` with `aria-label` for testability, retract vote logic
  - **MUI CustomerTable:** `CustomerTable` with `data-testid` for row selection, filter functionality
- Wrote 18 tests covering:
  - Integration (Retail flow: view details, add to cart, favorites)
  - Isolation (Cart, ProductDetail initial state)
  - Error states (context error, GraphQL error)
  - MUI components (Vote with aria-labels, CustomerTable with data-testid)
  - Redux custom render utility
- All 55 tests passing across 4 chapters

### Key Deviations from Book

1. **Apollo MockedProvider → MSW v2:** Apollo v4 removed MockedProvider; MSW is more portable
2. **MUI v5 Box props → MUI v6 `sx`:** API change in MUI v6
3. **`jest.spyOn` → `vi.spyOn`:** Vitest API
4. **`faker` → inline data:** Simpler, no extra dependency

---

## Chapter 5 — Refactoring Legacy Applications ✅

### What Was Done

- Built a `BudgetApp` component demonstrating a complete budgeting application
- Wrote **regression tests** for critical workflows (set income, create budget, delete budget, add expense)
- Demonstrated **Enzyme → RTL refactoring** with before/after code comparison
- Demonstrated **ReactTestUtils → RTL refactoring** with before/after code comparison
- Applied **testing best practices:**
  - Descriptive naming convention (`Component, given precondition, expected result`)
  - `screen` object instead of destructuring
  - `test.each` for data-driven tests
  - `findBy*` instead of `waitFor` + `getBy*`
  - Single assertions per logical test
- All 67 tests passing across 5 chapters

### Key Deviations from Book

1. **MUI upgrade demo → Custom BudgetApp:** Same concept, no MUI dependency needed
2. **Jest `test.each` → Vitest `test.each`:** Compatible API
3. **`jest.fn()` → `vi.fn()`:** Vitest API

---

## Chapter 6 — Additional Tools and Plugins ✅

### What Was Done

- Installed and configured **eslint-plugin-testing-library** and **eslint-plugin-jest-dom**
- Created `.eslintrc.json` with RTL and jest-dom best practice rules
- Updated `biome.json` with test-specific overrides (no console.log warnings in test files)
- Implemented **jest-axe** accessibility audits:
  - `NoAltImageButton` — fails audit (no alt text on image input)
  - `AltImageButton` — passes audit (with alt="login")
  - `InvalidList` — fails audit (img outside li)
  - `ValidList` — passes audit (img inside li)
- Documented Testing Playground and Wallaby.js (conceptual, no code needed)
- All 71 tests passing across 6 chapters

### Key Deviations from Book

1. **ESLint (primary) → Biome (primary):** Biome is faster, covers formatting + linting. ESLint config provided as complement.
2. **Wallaby.js (paid):** Not installed. Vitest watch mode provides sufficient feedback.
3. **CRA with built-in ESLint → Manual setup:** CRA is deprecated.

---

## Chapter 7 — End-to-End UI Testing with Cypress ✅

### What Was Done

- Installed and configured **Cypress** with `@testing-library/cypress`
- Created `cypress.config.ts` with base URL and viewport settings
- Wrote 4 Cypress test files:
  - `checkout-flow.cy.ts` — Complete checkout flow (shipping → payment → review → order)
  - `blog-flow.cy.ts` — Create and delete blog posts (CDD approach)
  - `api-tests.cy.ts` — CRUD API tests with `cy.request()`
  - `pom-pattern.cy.ts` — Page Object Model + custom commands
- Created 3 Page Objects: `HomePage`, `AddPage`, `PostDetailPage`
- Added npm scripts: `cy:open` (interactive) and `cy:run` (headless)
- Documented Gherkin/Cucumber and React DevTools concepts
- All 71 Vitest tests still passing

### Key Deviations from Book

1. **CRA + Next.js → Conceptual:** Cypress tests are written but need a running app to execute
2. **`cypress-cucumber-preprocessor` → Not installed:** Plugin has compatibility issues; concept documented
3. **JavaScript → TypeScript:** Consistency with the rest of the project

---

## Book Complete! 🎉

All 7 chapters of *Simplify Testing with React Testing Library* have been worked through.

### Project Stats

| Metric | Value |
|--------|-------|
| Chapters completed | 7/7 |
| Test files | 24 (Vitest) + 4 (Cypress) |
| Tests passing | 71 (Vitest) |
| Components built | 20+ |
| ADRs created | 6 (4 migrated to global) |
| Stack updates | Jest→Vitest, CRA→Vite, MSW v1→v2, MUI v5→v6 |

### What We Learned

1. RTL philosophy: test from user's perspective, avoid implementation details
2. Query priority: getByRole > getByLabelText > getByPlaceholderText > getByText > getByTestId
3. userEvent > fireEvent for realistic user simulation
4. MSW v2 for API mocking (REST + GraphQL)
5. Context API, Redux, and MUI testing patterns
6. Integration vs isolation testing strategies
7. jest-axe for automated accessibility audits
8. Cypress for E2E testing

### Next Steps

- Run Cypress tests against a real app
- Apply these patterns to real projects
- Continue with other Packt books in the series
