# LEARNINGS — Chapter 1

## Core Concepts

### DOM Testing Library Philosophy
- Tests should simulate real user behavior, not implementation details
- Prefer accessibility-first queries: `getByRole` > `getByLabelText` > `getByPlaceholderText` > `getByText`
- The `screen` object is the primary interface for queries
- Regular expressions in queries make tests case-insensitive (more user-like)

### Implementation Details — Why Avoid Them
- Testing state values, method names, or CSS classes creates brittle tests
- Refactoring internal code breaks tests even when functionality is unchanged
- False negatives waste time and reduce trust in the test suite
- **Analogy:** Driving a car — you don't need to know how the engine works to drive

### How to Think Like a User (Black-Box Testing)
- "What would a user see/do/expect?"
- Test outcomes, not internals
- Example: Counter component → test that clicking Add increments the displayed value, not that `state.count` changes

### jest-dom Advantages
- Descriptive matchers: `toBeInTheDocument()`, `toBeDisabled()`, `toHaveFormValues()`
- Better error messages that show the actual DOM element
- Chainable with `.not` for negative assertions

## Modern Updates (vs Book)

| Book | Our Stack | Reason |
|------|-----------|--------|
| Jest | Vitest | Faster, native ESM, compatible API |
| JavaScript | TypeScript | Type safety, modern standard |
| React class components | Functional components | Hooks are the standard since React 16.8 |
| `fireEvent` | `userEvent` | More realistic user simulation |
| `toBeTruthy()` for DOM | `toBeInTheDocument()` | More descriptive, better errors |
| Enzyme (in examples) | Not used | Deprecated, RTL is the standard |

## Key Patterns Established

1. **Query priority:** `getByRole` → `getByLabelText` → `getByPlaceholderText` → `getByText` → `getByTestId` (last resort)
2. **Assertion style:** Use jest-dom matchers for DOM assertions
3. **Test structure:** Arrange (render) → Act (userEvent) → Assert (expect + jest-dom)
4. **Cleanup:** Vitest + RTL handle automatic cleanup between tests

## Chapter 2 — Working with React Testing Library

### Test Structure (Arrange-Act-Assert)
1. **Arrange:** `render(<Component />)` — RTL puts it in a div, attaches to DOM, auto-cleans up
2. **Act:** Query elements with `screen.getByRole()`, `screen.getByText()`, etc.
3. **Assert:** `expect(element).toBeInTheDocument()` with jest-dom matchers

### Presentational Components
- Components without state, just display data (props or hardcoded)
- Two testing strategies:
  - **Snapshot tests:** `expect(container).toMatchSnapshot()` — catches unexpected HTML changes
  - **Query-based tests:** Verify specific elements/data are in the DOM

### Snapshot Tests
- Provided by Vitest (compatible with Jest snapshots)
- Good for: static/presentational components with stable output
- Update with `npm test -- -u` or press `u` in watch mode
- **Caveat:** Can produce false positives if developers blindly update snapshots. Use sparingly.

### Debug Method
- `screen.debug()` — logs entire component DOM to console
- `screen.debug(element)` — logs specific element
- Great for troubleshooting, remove before committing

### Key Differences from Book

| Book | Our Stack | Reason |
|------|-----------|--------|
| create-react-app | Vite + manual setup | CRA is deprecated; Vite is the modern standard |
| Jest snapshots | Vitest snapshots | Compatible API, same behavior |
| `const { container } = render(...)` | Same, but prefer `screen` queries | container is fine for snapshots |
| Class components | Functional components | Hooks are standard |

## Chapter 3 — Testing Complex Components

### User Events
- **fireEvent:** Lower-level, synchronous, simulates individual events. Fine for simple clicks but misses real browser behavior chains.
- **userEvent:** Higher-level, async, simulates full event chains (focus, keydown, input, keyup, blur). **Always prefer userEvent.**
- `userEvent.setup()` creates a configured instance per test
- `user.type(element, text)` simulates real typing
- `user.keyboard('{Enter}')` simulates key presses

### Testing Event Handlers in Isolation
- Use `vi.fn()` (Vitest) / `jest.fn()` (Jest) to create mock functions
- Pass mocks as props to test child components in isolation
- Assert with `toHaveBeenCalled()` and `toHaveBeenCalledTimes()`
- **Caveat:** Testing in isolation can't verify full integration (e.g., button disabled state after click requires parent component)

### MSW (Mock Service Worker) v2
- Intercepts HTTP requests at the network level, returns mock data
- **MSW v2** uses `http.get()` instead of `rest.get()` (v1 API)
- Setup: `setupServer(...handlers)` for Node.js (tests), `setupWorker(...handlers)` for browser (dev)
- Lifecycle: `beforeAll(listen)` → `afterEach(resetHandlers)` → `afterAll(close)`
- Override handlers per-test with `mockServer.use(...)`
- Great for: testing API success, empty results, error states without real network calls

### Query Types
| Query | When to Use | Behavior on Not Found |
|-------|-------------|----------------------|
| `getBy*` | Element is expected to be in DOM now | Throws immediately |
| `findBy*` | Element appears after async operation | Retries for a few seconds, then throws |
| `queryBy*` | Verifying element is NOT in DOM | Returns null (no throw) |

### TDD (Test-Driven Development) Workflow
1. **Red:** Write a failing test first
2. **Green:** Write minimum code to pass
3. **Refactor:** Clean up code while tests stay green
4. Repeat

### Key Differences from Book

| Book | Our Stack | Reason |
|------|-----------|--------|
| MSW v1 (`rest`) | MSW v2 (`http`) | v2 is current; v1 deprecated |
| `jest.fn()` | `vi.fn()` | Vitest API |
| Class components for Register | Functional + hooks | Modern standard |
| `fireEvent` examples | Omitted (userEvent only) | Already covered in ADR-011 |

## Chapter 4 — Integration Testing and Third-Party Libraries

### Integration vs Isolation
- **Integration testing:** Test components with real dependencies (other components, context providers). More value per test, closer to production use.
- **Isolation testing:** Mock dependencies with `vi.fn()`. Better for edge cases, form validation, error states. Faster but less realistic.
- **Rule of thumb:** Integration for happy paths, isolation for edge cases and error states.

### Context API Testing
- Wrap component in the real `Provider` within the test
- Test child components in isolation by wrapping only them (e.g., `<RetailProvider><Cart /></RetailProvider>`)
- Test integration by wrapping the parent component (e.g., `<RetailProvider><Retail /></RetailProvider>`)
- **Error boundary test:** Use `react-error-boundary` + `vi.spyOn(console, 'error')` to verify context errors

### Redux Testing
- Create a **custom render** utility that wraps components in `<Provider store={store}>`
- Use `configureStore` from Redux Toolkit with `preloadedState` for test-specific data
- Export the custom render from a `test-utils.tsx` file, re-export everything from RTL
- This keeps test code clean (no visible Provider wrapping)

### GraphQL Testing
- **MSW v2** can intercept GraphQL requests just like REST (same `http` handler)
- Alternative: `MockedProvider` from Apollo (but Apollo v4 removed it — use MSW instead)
- Test loading, success, and error states

### MUI (Material-UI) Testing
- Add `aria-label` to MUI `Button` components for testability (MUI forwards it to the DOM)
- Use `data-testid` as last resort when `getByRole` can't select elements
- MUI v6 changes: `Box` no longer accepts styling props directly (use `sx` prop)
- Disabled MUI buttons use `pointer-events: none` — `userEvent` respects this

### Key Differences from Book

| Book | Our Stack | Reason |
|------|-----------|--------|
| Apollo MockedProvider | MSW v2 for GraphQL | Apollo v4 removed MockedProvider |
| MUI v5 Box props | MUI v6 `sx` prop | API change in MUI v6 |
| `jest.spyOn` + manual restore | `vi.spyOn` + `vi.restoreAllMocks()` | Vitest API |
| `faker` (deprecated) | Inline test data | `@faker-js/faker` available if needed |

## Chapter 5 — Refactoring Legacy Applications

### Regression Testing Before Dependency Updates
- Write integration tests for critical workflows **before** touching dependencies
- Run tests in watch mode while updating to catch regressions immediately
- RTL tests don't need updating when source code changes (they test behavior, not implementation)

### Enzyme → RTL Refactoring
- **Enzyme problems:** Tests implementation details (component names, method names, state, CSS classes)
- **RTL solution:** Test from user's perspective (what the user sees and does)
- Key changes:
  - `mount(<App />)` → `render(<App />)`
  - `wrapper.find('Component').props().method()` → `user.click(screen.getByRole(...))`
  - `wrapper.find('h3#income').text()` → `screen.getByRole('heading', { name: /income/i })`
  - No more manual cleanup (RTL handles it)

### ReactTestUtils → RTL Refactoring
- **ReactTestUtils problems:** Manual DOM (createElement, appendChild, querySelector), manual cleanup, manual act()
- **RTL solution:** All of that is handled automatically
- Key changes:
  - `ReactDOM.render(<App />, container)` → `render(<App />)`
  - `container.querySelector('h3#income')` → `screen.getByRole('heading', ...)`
  - `document.body.removeChild(container)` → not needed

### Testing Best Practices
1. **Naming convention:** `Component, given precondition, expected result`
2. **Use `screen` object** instead of destructuring from `render`
3. **Use `test.each`** for data-driven tests (multiple inputs, same logic)
4. **One assertion per logical test** — if one assertion failing hides others, split them
5. **Use `findBy*`** instead of `waitFor` + `getBy*` for async elements
6. **Use `queryBy*`** for asserting element absence (doesn't throw)

### Key Differences from Book

| Book | Our Stack | Reason |
|------|-----------|--------|
| MUI v1 → v4 upgrade | Concept demonstrated with custom BudgetApp | Same concept, no MUI dependency needed |
| Jest `test.each` | Vitest `test.each` | Compatible API |
| `jest.fn()` | `vi.fn()` | Vitest API |

## Chapter 6 — Additional Tools and Plugins

### ESLint Plugins (Complementary to Biome)
- **eslint-plugin-testing-library:** Enforces RTL best practices (prefer screen queries, no debug in committed code, prefer findBy* over waitFor)
- **eslint-plugin-jest-dom:** Enforces jest-dom matchers (toBeChecked, toHaveClass, toHaveStyle)
- **Note:** This project uses Biome as primary linter. ESLint config provided as `.eslintrc.json` for those who want both.
- Key rules configured:
  - `testing-library/prefer-screen-queries`: error
  - `testing-library/no-debug`: warn (reminder to remove before commit)
  - `jest-dom/prefer-checked`: error (use `toBeChecked()` instead of `toHaveProperty('checked', true)`)
  - `jest-dom/prefer-to-have-class`: error (use `toHaveClass()` instead of checking `.className`)

### jest-axe — Automated Accessibility Audits
- **Install:** `npm install --save-dev jest-axe`
- **Setup:** Import `axe` and `toHaveNoViolations`, extend expect
- **Usage:** `const results = await axe(container); expect(results).toHaveNoViolations()`
- **What it catches:**
  - Image buttons without alt text (`input-image-alt`)
  - Invalid list structure (img outside li)
  - Missing form labels
  - And many more WCAG violations
- **Limitations:** Automated tools can't catch everything (e.g., expanded abbreviations, logical reading order). Manual auditing is still required.

### Testing Playground
- **Website:** https://testing-playground.com — paste HTML, click elements, get suggested queries
- **Chrome Extension:** Works in DevTools with live JS/CSS
- **In-code:** `screen.logTestingPlaygroundURL()` logs a URL to the website with your component's HTML
- **Limitation:** Only suggests `getBy*` queries — may need to adapt to `findBy*` for async elements

### Wallaby.js
- Paid tool (not installed). Provides in-editor test feedback, time-travel debugging, inline coverage.
- Not needed for this project — Vitest watch mode + terminal provides sufficient feedback.

### Key Differences from Book

| Book | Our Stack | Reason |
|------|-----------|--------|
| ESLint (primary) | Biome (primary) + ESLint config | Biome is faster, covers formatting + linting |
| Wallaby.js (paid) | Not installed | Vitest watch mode is sufficient |
| CRA with built-in ESLint | Manual setup | CRA is deprecated |

## Chapter 7 — End-to-End UI Testing with Cypress

### Cypress Overview
- **End-to-end testing framework** that runs in the browser (not a browser driver like Selenium)
- Provides interactive Test Runner (`cypress open`) and headless mode (`cypress run`)
- Auto-waits for commands and assertions before proceeding
- Supports Chrome, Firefox, Edge, and Electron browsers
- Built on Mocha (test runner) + Chai (assertions) + jQuery (DOM queries)

### Cypress Testing Library
- `@testing-library/cypress` adds DOM Testing Library queries to Cypress
- Only `findBy*` methods are included (support Cypress retry-ability)
- Enables accessible queries: `cy.findByRole('textbox', { name: /first name/i })`
- Install: `npm install --save-dev @testing-library/cypress`
- Setup: `import '@testing-library/cypress/add-commands'` in `cypress/support/commands.ts`

### Cypress-Driven Development (CDD)
- Write the test first, then build the UI to make it pass
- Similar to TDD but at the E2E level
- Cypress Test Runner auto-reloads on file changes
- Great for seeing the app in a specific state while building features

### Design Patterns
1. **Page Object Model (POM):** Class-based representation of each page with methods for interactions
   - Pros: Abstracts away multiple lines, single source of truth
   - Cons: Can lead to duplicate test steps across tests
2. **Custom Commands:** `Cypress.Commands.add('createBlogPost', (post) => { ... })`
   - Reusable across tests
   - Can use `cy.request()` to bypass UI for setup (faster tests)

### API Testing with Cypress
- `cy.request()` makes HTTP requests directly (no browser needed)
- Use `cy.request('POST', '/api/add', data)` to create data
- Use `cy.request('GET', '/api/posts')` to read data
- Use `.as('alias')` + `cy.get('@alias')` to reference responses
- Great for: testing API endpoints, setting up test data, cleaning up after tests

### Gherkin/Cucumber
- **Gherkin:** Behavior-driven language using Given/When/Then
- **Plugin:** `cypress-cucumber-preprocessor`
- Feature files (`.feature`) contain plain-English scenarios
- Step definitions map Gherkin steps to Cypress code
- Benefits: Communication with non-technical stakeholders, living documentation

### React Developer Tools with Cypress
- Install `react-devtools` as dev dependency
- Add `<script src="http://localhost:8097"></script>` to app HTML
- Run app + Cypress + react-devtools simultaneously
- Inspect component tree, props, and state during test execution

### Key Differences from Book

| Book | Our Stack | Reason |
|------|-----------|--------|
| CRA + Next.js examples | Conceptual (no app to test) | Cypress tests are written but need a running app |
| `cypress-cucumber-preprocessor` | Not installed | Plugin has compatibility issues; concept documented |
| JavaScript test files | TypeScript test files | Consistency with the rest of the project |
