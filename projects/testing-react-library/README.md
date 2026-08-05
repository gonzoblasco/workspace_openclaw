# Simplify Testing with React Testing Library

Working through Scottie Crump's book, updating patterns to modern standards (August 2026).

## Stack

- **Test runner:** Vitest (replaces Jest)
- **Framework:** React 19
- **Testing Library:** @testing-library/react 16
- **User events:** @testing-library/user-event 14
- **DOM matchers:** @testing-library/jest-dom 6
- **Linter/Formatter:** Biome
- **Language:** TypeScript

## Key Decisions

See [.knowledge/ADRs.md](.knowledge/ADRs.md) for all architectural decisions.

| Decision | Book | Ours |
|----------|------|------|
| Test runner | Jest | Vitest |
| Language | JavaScript | TypeScript |
| Components | Class-based | Functional + hooks |
| User events | fireEvent | userEvent |
| DOM assertions | toBeTruthy | toBeInTheDocument |

## Structure

```
projects/testing-react-library/
├── .knowledge/           # Institutional memory
├── chapters/
│   ├── chapter-01/       # Foundation concepts
│   └── ...
├── package.json
├── vitest.config.ts
└── biome.json
```

## Running Tests

```bash
npm test          # Run all tests once
npm run test:watch  # Watch mode
npm run lint      # Biome check
```
