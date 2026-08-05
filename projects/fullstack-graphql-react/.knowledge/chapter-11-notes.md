# Chapter 11: Writing Tests for React and Node.js

## Core Concepts

1. **Vitest:** Fast, Vite-native test runner with built-in expect, mocking, and coverage
2. **React Testing Library:** Tests user behavior, not implementation details
3. **jsdom:** Browser-like DOM environment for Node.js tests
4. **Component testing:** Render components, assert on output, simulate events
5. **Test-driven development (TDD):** Write tests before implementation

## Key Changes from Book

| Book (Mocha + Enzyme) | Modern (Vitest + RTL) | Reason |
|---|---|---|
| Mocha + Chai | Vitest (built-in expect) | Faster, native ESM |
| Enzyme (deprecated) | React Testing Library | No React 19 support |
| `enzyme.mount()` | `render()` from RTL | Tests user behavior |
| `wrapper.find().simulate('click')` | `fireEvent.click()` | Simulates real events |
| `wrapper.html()` | `screen.getByText()` / `container` | Accessible queries |
| Manual jsdom setup | `environment: 'jsdom'` in config | Vitest handles it |
| `@babel/polyfill` | Not needed | Native ESM |

## Test Files Created

- `src/test/Loading.test.jsx` — Tests Loading component rendering and props
- `src/test/ErrorMessage.test.jsx` — Tests ErrorMessage with children
- `src/test/Dropdown.test.jsx` — Tests Dropdown open/close behavior

## Running Tests

```bash
cd projects/fullstack-graphql-react/chapter-04
npm test          # Run once
npm run test:watch  # Watch mode
```

## Test Patterns

### Component rendering
```jsx
render(<MyComponent />);
expect(screen.getByText('Hello')).toBeInTheDocument();
```

### Event simulation
```jsx
fireEvent.click(screen.getByText('Menu'));
expect(screen.getByText('Content')).toBeInTheDocument();
```

### Style assertions
```jsx
const el = container.querySelector('.my-class');
expect(el.getAttribute('style')).toContain('color: red');
```

### Children rendering
```jsx
render(<Wrapper><p>Child</p></Wrapper>);
expect(screen.getByText('Child')).toBeInTheDocument();
```
