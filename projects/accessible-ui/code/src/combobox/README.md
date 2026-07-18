# Combobox

Editable combobox with list autocomplete powered by WAI-ARIA APG pattern.

## ARIA Pattern

[Editable Combobox with List Autocomplete](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/)

## Props

```typescript
interface Option {
   value: string;  // Unique value used for selection
   label?: string; // Displayed text (optional, can differ from value)
}

interface ComboboxProps {
   options: Option[];    // Options list for filtering and selection
   value?: string;      // Controlled value via React state
   onChange?: (v: string) => void;  // Callback when value changes
   disabled?: boolean;   // Input disabled state
}
```

## Keyboard Interactions

| Key | Behavior | ARIA Reference |
|-----|----------|-----------------|
| `ArrowDown` | Focus next option in panel (wrap to first) | APG: "keyboard focus navigation" |
| `ArrowUp` | Focus previous option (wrap to last) | APG: "focus management" |
| `Enter` / `Space` | Toggle panel (if empty) or select suggestion (if text typed) | APG: "panel toggle activation" |
| `Escape` | Close panel, revert value | APG: "close combobox" |

## Usage Example

```tsx
import { Combobox } from '@gonzoblasco/accessible-ui';

function SearchBox() {
   const [selectedOption, setSelected] = useState<Option>({ value: "apple", label: "Apple 🍎" });
   const [options, setOptions] = useState([
      { value: "apple", label: "Apple 🍎" },
      { value: "banana", label: "Banana 🍌" }
   ]);

   return <Combobox 
      options={options}
      value={selectedOption.value}
      onChange={(v) => setSelected({ value: v, label: selectedOption.label })}
   />;
}
```

## Implementation Details

### Hook System (`useCombobox`)

Returns pure functions of inputs for unit testing:

```typescript
{
   expanded: boolean;        // Panel open state
   focusedOption: number | null;  // Currently focused option index
   currentValue: string;  // Current value (for debounced filtering)
   togglePanel: () => void;      // Toggle panel visibility
   selectOption: (index: number) => void; // Select option with propagation
}
```

### Debouncing Strategy

- **300ms delay** for filtering to prevent excessive DOM updates during rapid typing
- **Controlled value** via React props (value, onChange) — uncontrolled fallback handled by hook state
- **Input tracking** separate from controlled value for UX (filter while typing)

## ARIA Compliance Checklist

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| `role="combobox"` | ✅ | Rendered on input wrapper |
| `aria-expanded` | ✅ | Reflects expanded state, updates on toggle |
| `aria-controls` | ✅ | References listbox element ID |
| `aria-autocomplete` | ✅ | Set to `"list"` per APG requirements |
| Focus management | ✅ | Proper focus flow from input → panel |
| Keyboard navigation | ✅ | Full arrow wrap + Enter/Space toggle + Escape close |

## Accessibility Highlights

1. **Input disabled** = `aria-disabled="true"` set on wrapper
2. **Panel hidden** until toggled, but visible when needed (accessibility contrast)
3. **Option aria-selected** = reflects current focus state for screen readers
4. **Proper focus order** → input first, then options in DOM order

## Related Components

- [Modal](../modal/README.md) — Focus-trapped dialog
- [Tabs](../tabs/README.md) — Keyboard-navigable tab groups
- [useCombobox](./use-combobox.ts) — Hook system for internal state management

## Storybook Stories

```tsx
import { Combobox } from "./combobox";

// Controls: Options (array), value (string), onChange (function), disabled (boolean)
// Docs: View ARIA attributes reference table and keyboard navigation patterns
```
