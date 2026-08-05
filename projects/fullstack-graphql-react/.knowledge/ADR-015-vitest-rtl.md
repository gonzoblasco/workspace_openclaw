# ADR-015: Vitest + React Testing Library Instead of Mocha + Enzyme

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 11
**Scope:** Global

## Context

The book uses Mocha + Chai + Enzyme + JSDOM for testing. Enzyme is deprecated and incompatible with React 19. Mocha requires significant configuration for ESM and JSX support.

## Decision

Use Vitest + React Testing Library + jsdom for all testing.

## Rationale

- **Vitest:** Native ESM, Vite integration, fast, compatible with React 19
- **React Testing Library:** Encourages testing user behavior, not implementation details
- **Enzyme is deprecated:** No React 18/19 adapter, unmaintained since 2022
- **Chai not needed:** Vitest has built-in `expect` with jest-compatible matchers
- **jsdom:** Still the standard DOM environment for Node.js tests

## Key API Changes

| Book (Mocha + Enzyme) | Modern (Vitest + RTL) | Reason |
|---|---|---|
| `describe/it` from Mocha | `describe/it` from Vitest | Same API, different import |
| `chai.expect/should` | `expect` from Vitest | Built-in, jest-compatible |
| `enzyme.mount()` | `render()` from RTL | RTL tests user behavior |
| `wrapper.find().simulate()` | `fireEvent` / `userEvent` | RTL simulates real events |
| `wrapper.html()` | `screen.getByText()` / `container` | RTL queries by accessible roles |
| `jsdom` setup manual | `environment: 'jsdom'` in config | Vitest handles setup |

## Pattern

```jsx
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import MyComponent from './MyComponent.jsx';

describe('MyComponent', () => {
  it('renders and responds to click', () => {
    render(<MyComponent />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button'));
    expect(screen.getByText('Clicked')).toBeInTheDocument();
  });
});
```

## References

- https://vitest.dev
- https://testing-library.com/react
