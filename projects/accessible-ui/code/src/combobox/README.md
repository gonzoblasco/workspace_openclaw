# Combobox

Editable combobox with list autocomplete powered by WAI-ARIA APG pattern.

## ARIA Pattern

[Editable Combobox with List Autocomplete](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/)

## Props

```typescript
type Option = { value: string; label?: string };
type ComboboxProps = {
   options: Option[];
   value?: string;
   onChange?: (v: string) => void;
   disabled?: boolean;
};
```

## Keyboard Interactions

| Key | Behavior |
|-----|----------|
| `ArrowDown` | Focus next option in panel |
| `ArrowUp` | Focus previous option |
| `Enter` / `Space` | Toggle panel (if empty) or select suggestion (if text typed) |
| `Escape` | Close panel, revert value |

## Usage Example

```tsx
<Combobox
   options={[
      { value: "apple", label: "Apple 🍎" },
      { value: "banana", label: "Banana 🍌" }
   ]}
   value="apple"
   onChange={(v) => console.log(v)}
/>
```

## Hook

```tsx
import useCombobox from "../use-combobox";

function Combobox(props: ComboboxProps): JSX.Element {
   const state = useCombobox(props);
   // state.expanded, state.focusedOption, etc.
   return <div {...state.props} />;
}
```
