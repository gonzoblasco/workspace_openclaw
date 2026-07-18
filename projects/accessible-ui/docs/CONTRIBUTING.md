# Contributing to accessible-ui

Thank for taking the time to contribute to accessible-ui!

## Getting Started

```bash
git clone https://github.com/gonzoblasco/accessible-ui.git
cd accessible-ui
npm install
```

## Development

```bash
npm run storybook   # open Storybook
npm run test       # run tests once
npm run test:watch # watch mode
```

## Commit Guidelines

Use conventional commits following this format:

```
<type>(?<optional_description>: <subject>

[optional body]

[optional reference]
```

Types: `feat` | `fix` | `docs` | `test` | `chore`

Example: `feat: add focus trap to Modal component`

## Testing Strategy

All components must pass:
1. Rendering tests (aria roles/attributes check)
2. Keyboard user-event sequences from WAI-APG table
3. axe-core audit with zero violations

See [DEFINITION.md](./DEFINITION.md) for full test strategy.

## Code of Conduct

Same as main repo policies.
