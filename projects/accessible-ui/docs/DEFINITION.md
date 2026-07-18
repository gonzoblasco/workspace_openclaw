# accessible-ui — Definition v1.0

## Metas Core (MVP)

### Combinados: Combobox

**Functional requirements:**
- Editable input que acepta `value`, `onChange` como props de React
- Lista desplegable con opciones filtradas por texto
- Autocomplet suggestions en tiempo real (debounce 300ms)
- Focus management: foco entra desde input → lista, salte hacia input al seleccionar

**ARIA compliance:**
```typescript
{
   "role": "combobox",
   "aria-expanded": true/false,
   "aria-controls": idList,
   "aria-label": label,
   "aria-autocomplete": "list" // CRITICAL: indica que es autocomplete
}
```

**Keyboard interactions:**
- `Enter` / `Space`: toggle panel (si no hay text) OR select suggestion (text typed)
- `ArrowDown`: focus next option en lista
- `ArrowUp`: focus previous option
- `Escape`: close panel, revert value

### Modal: Dialog

**Functional requirements:**
- Overlay backdrop con opacity controlable
- Focus trap dentro del dialog (primario → foco de salida → return)
- Cierre ESC y click outside
- ARIA roles: `role="dialog"`, `aria-modal="true"`

**Keyboard interactions:**
- `Escape`: close immediately, save focus on next tabbable
- `Tab` forward/backward: cycle dentro del dialog only (no escape overlay)
- `Space` / `Enter`: activate button primario (si está focused)

### Tabs: Panel de pestañas

**Functional requirements:**
- Group container con panel items
- Manual activation mode (arrows solo move focus, Enter/Space activan)
- Panel active controlable vía API o keyboard
- ARIA live region announcements

**ARIA compliance:**
```typescript
{
   "role": "tablist",
   "aria-label": label,
   "role": "tabpanel",
   "aria-selected": true/false,
   "aria-labelledby": tab-link-id
}
```

**Keyboard interactions:**
- `ArrowRight`: next tab (wrap to first)
- `ArrowLeft`: prev tab (wrap to last)
- `Home`: focus first tab
- `End`: focus last tab
- `Space` / `Enter`: activate current tab (manual activation)

## Architecture Decisions

### Headless Strategy

Components return hooks que proporcionan state management:

```typescript
// Combobox example
function useCombobox(props: ComboboxProps): ComboboxState {
   const [expanded, setExpanded] = useState(false);
   const [options, setOptions] = useState([]); // filtered
   // focus management logic...
}
```

This allows consumers to react:
- Badge when panel expanded
- Extend behavior without forking
- Unit test pure functions

### Testing Integration

**Three layers:**
1. **Vitest rendering**: Check ARIA attributes/roles in initial state
2. **User-event keyboard**: Run full sequences from WAI-APG table
3. **axe-core audit**: Assert zero violations, catch valid HTML but invalid ARIA

### Component Pattern

```typescript
interface ComboboxProps {
   value?: string;
   onChange?: (v: string) => void;
   options: Option[];
   disabled?: boolean;
}

function Combobox(props: ComboboxProps): JSX.Element {
   const state = useCombobox(props);
   // render with controlled behavior from hook
}
```

## Stack Decisions

| Tech | Version | Rationale |
|------|---------|-----------|
| React | 19 | Latest FC model, concurrent rendering ready |
| TypeScript | 5.6+ | Best TS version for project (stable generics) |
| Vite | 6.x | Fast HMR, small bundles, modern tooling |
| Vitest | 2.x | Modern testing, similar API to JSDT |
| Storybook | 10.x | Latest docs + addon-a11y |
| Tailwind CSS | v4 | CSS-first, arbitrary values |

## Dependencies Baseline

```json
{
   "dependencies": {
      "react": "^19.x",
      "typescript": "^5.6",
      "react-dom": "^19.x"
   },
   "devDependencies": {
      "@types/react": "^19.x",
      "@vitejs/plugin-react": "^4.x",
      "vitest": "^2.x",
      "@testing-library/jest-dom": "^6.x",
      "@testing-library/user-event": "^14.x",
      "@storybook/preview": "^10.x",
      "@testing-library/react": "^16.x",
      "jest-axe": "^8.x"
   }
}
```

## ARIA Decisions por Component

| Component | APG Pattern | Decision | Rationale |
|-----------|-------------|----------|-----------|
| Combobox | Editable + List Autocomplete | `aria-autocomplete="list"` | Required by combobox pattern |
| Modal | Dialog | `role="dialog"`, aria-modal="true" | Standard pattern requirement |
| Tabs | Tabs | Manual activation chosen | Better UX for keyboard, simpler state than automatic |

---

## Next Steps

- **Phase 1**: Implement combobox (first core component)
- **ADR-002**: Storybook integration plan
- **ADR-003**: Testing strategy implementation details
