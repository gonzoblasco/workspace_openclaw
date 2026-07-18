# Source Structure

## Core Components

| Component | Location | ARIA Pattern | Status |
|-----------|----------|--------------|--------|
| Combobox | `combobox/` | Editable + List Autocomplete | ⏳ Ready for implementation |
| Modal | `modal/` | Dialog | ⏳ Ready for implementation |
| Tabs | `tabs/` | Tab Group | ⏳ Ready for implementation |

## Hook System

```typescript
// Core hooks exported from this directory
- useCombobox: Manage combobox state & keyboard navigation
- useModal: Focus trap + modal lifecycle
- useTabs: Tab group state management
- useAriaExpanded: Helper for aria-expanded attribute
- useAriaSelected: Helper for aria-selected attribute (required)

## File Structure

```
src/
├── combobox/       # Combobox component & hook
│   ├── Combobox.tsx
│   ├── use-combobox.ts
│   ├── README.md
│   └── __test__/    # Tests (rendering, keyboard, axe audit)
├── modal/          # Modal component & hook
│   ├── Modal.tsx
│   ├── use-modal.ts
│   ├── README.md
│   └── __test__/    # Tests
├── tabs/           # Tabs component & hook
│   ├── Tabs.tsx
│   ├── use-tabs.ts
│   ├── README.md
│   └── __test__/    # Tests
├── use-aria.ts     # Shared ARIA helpers

## Next Steps

1. Implement full Combobox with focus management
2. Implement Modal focus trap + ESC close
3. Implement Tabs manual activation mode
4. Write complete test suites (vitest + axe-core)
5. Build Storybook stories from component READMEs