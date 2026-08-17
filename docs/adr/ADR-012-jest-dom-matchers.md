# ADR-012 - Use jest-dom Matchers for DOM Assertions

**Status:** Accepted  
**Date:** 2026-08-05  
**Context:** Jest provides generic matchers like `toBeTruthy()`, `toBeFalsy()`, and `toEqual()` that can be used for DOM assertions. However, `@testing-library/jest-dom` provides specialized DOM matchers that are more descriptive and provide better error messages.  
**Decision:** Always use jest-dom matchers for DOM-related assertions. Specifically:
- `toBeInTheDocument()` / `not.toBeInTheDocument()` for DOM presence (never `toBeTruthy()` / `toBeFalsy()`)
- `toBeDisabled()` / `toBeEnabled()` for disabled state (never `hasAttribute('disabled')`)
- `toHaveFormValues()` for form data (never manual property checks)
- `toHaveTextContent()` for text content
- `toHaveAttribute()` for attribute checks
- `toHaveClass()` for class checks
- `toHaveStyle()` for style checks
- `toHaveValue()` for input values
- `toBeChecked()` for checkbox/radio state
- `toBeVisible()` for visibility checks
- `toBeEmptyDOMElement()` for empty elements

**Consequences:**
- More readable test assertions (intent is clear from the matcher name)
- Better error messages on failure (shows the actual DOM element with attributes)
- Consistent with Testing Library best practices
- Requires `@testing-library/jest-dom` as a dev dependency
- Setup: `import '@testing-library/jest-dom/vitest'` in setup file (Vitest) or `import '@testing-library/jest-dom'` (Jest)

**Error message comparison:**
- `expect(el).toBeTruthy()` → "Expected: truthy, Received: null" (unhelpful)
- `expect(el).toBeInTheDocument()` → "Expected element to be in the document, Received: <button disabled class="btn">Submit</button>" (helpful, shows the element)

**Origin:** Simplify Testing with React Testing Library (Packt)
