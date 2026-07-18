# accessible-ui 🌿

A headless accessible component library built with React and TypeScript.

Each component exposes unstyled, composable primitives. You provide the class names — the library provides the ARIA semantics, keyboard navigation, and focus management.

## Components

| Component | Desc | ARIA Pattern |
|-----------|------|---------------|
| [Combobox](src/components/combobox/README.md) | Editable combobox with list autocomplete | [Editable Combobox with List Autocomplete](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) |
| [Modal](src/components/modal/README.md) | Focus-trapped dialog | [Dialog (Modal)](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) |
| [Tabs](src/components/tabs/README.md) | Keyboard-navigable tabbed interface | [Tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/) |

## Methodology

### Headless pattern

Components ship with zero styles. Each primitive accepts `className` (and any standard HTML attribute) so the styling layer is entirely in your hands — Tailwind, CSS Modules, plain CSS. The behavior contract is the component's API; the visual contract is yours.

State management is extracted into custom hooks (`useModal`, `useTabs`, `useCombobox`) that are returned to the consumer. This means:
- You can read and react to state (e.g. show a badge when a panel is active).
- You can extend behavior without forking the component.
- Testing the logic layer is straightforward because the hooks are pure functions of their inputs.

### ARIA references

Every component follows the [WAI-ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/patterns/) pattern for its widget type:

| Component | APG Pattern |
|-----------|-------------|
| Combobox | Editable Combobox with List Autocomplete |
| Modal | Dialog |
| Tabs | Tabs |

Where the APG offers multiple valid approaches, each component's README documents which option was chosen and why — including the screen-reader and keyboard trade-offs that drove the decision.

### Testing strategy

Each component has three layers of tests:

1. **Rendering** — correct ARIA roles, attributes, and DOM structure are present in the initial state.
2. **Keyboard interaction** — `@testing-library/user-event` drives the keyboard sequences from the APG pattern table.
3. **Accessibility audit** — `jest-axe` runs `axe-core` against the rendered output and asserts zero violations.

Tests run in jsdom via Vitest. The `@testing-library/react` render utilities are used directly — no custom wrappers — so test setup is minimal and the tests read close to how a user interacts with the component.

## Development

```bash
npm install
npm test             # run all tests once
npm run test:watch   # watch mode
npm run storybook    # open Storybook
```

## Stack

- React 19, TypeScript
- Vite (app bundler), Vitest (test runner)
- Storybook 10 with addon-a11y and addon-docs
- Tailwind CSS v4 (demo styles only — components are unstyled)
