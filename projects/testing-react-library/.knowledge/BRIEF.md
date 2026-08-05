# BRIEF — Simplify Testing with React Testing Library

## Source

- **Book:** *Simplify Testing with React Testing Library* by Scottie Crump (Packt Publishing)
- **Edition:** Original (no specific edition noted)
- **Goal:** Work through each chapter, extracting practical knowledge, updating deprecated patterns to modern standards (August 2026), and documenting decisions via ADRs.

## Approach

- Each chapter produces a working project or set of examples within this monorepo
- Where the book uses deprecated packages/versions, update to current LTS equivalents
- Where the book is theoretical, extract principles and implement with modern tooling
- All code in TypeScript unless the chapter explicitly uses JS-only patterns
- Vitest replaces Jest (faster, compatible API, native ESM)
- React 19 + Testing Library 14+ as baseline

## Stack (August 2026)

- **Runtime:** Node.js LTS (current)
- **Package manager:** npm
- **Test runner:** Vitest (replaces Jest)
- **Framework:** React 19
- **Testing Library:** @testing-library/react 14+
- **DOM matchers:** @testing-library/jest-dom (latest)
- **Linter/Formatter:** Biome
- **Pre-commit:** simple-git-hooks (Biome check + Vitest run)

## Structure

```
projects/testing-react-library/
├── .knowledge/           # Institutional memory (BRIEF, ADRs, LEARNINGS, STATUS, ROADMAP)
├── chapters/
│   ├── chapter-01/      # Each chapter gets its own workspace
│   ├── chapter-02/
│   └── ...
├── package.json          # Root workspace config
├── biome.json
└── README.md
```
