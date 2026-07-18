# Modal

Focus-trapped dialog following the WAI-ARIA Dialog pattern.

## ARIA Pattern

[Dialog (Modal)](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)

## Props

```typescript
interface ModalProps {
   title?: string;     // Heading for accessibility
   isOpen: boolean;    // Controlled open state
   onClose?: () => void;  // Callback when modal closes
}
```

## Keyboard Interactions

| Key | Behavior | ARIA Reference |
|-----|----------|-----------------|
| `Escape` | Close immediately, focus on next tabbable after close | APG: "close dialog with key" |
| `Tab` (forward/backward) | Cycle only within dialog content (not overlay) | APG: "keyboard focus management" |
| `Space` / `Enter` | Activate button if focused (when focused first tab) | APG: "panel activation" |

## Usage Example

```tsx
import { Modal } from '@gonzoblasco/accessible-ui';

function ConfirmAction() {
   const [isOpen, setIsOpen] = useState(false);

   return <>
      <button onClick={() => setIsOpen(true)}>Confirm?</button>
      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Confirmation">
         Are you sure?
      </Modal>
   </>;
}
```

## Implementation Details

### Focus Trap Strategy

1. **Capture initial focus** when modal opens (store in firstFocusableRef)
2. **Find all tabbable elements** within dialog (buttons, links, inputs, selectables)
3. **On Tab forward** → move to next tabbable, wrapping to last if no more
4. **On Tab backward** → move to previous tabbable, wrapping to first if no more
5. **On Escape close** → focus returns to initial saved element

### ARIA Compliance

- `role="dialog"` — Dialog container wrapper
- `aria-modal="true"` — Indicates modal behavior (required)
- `tabIndex="-1"` on dialog content (focus trapped, not part of natural tab order)
- Overlay backdrop with hidden attribute (not visible until open)

## Accessibility Highlights

| Requirement | Implementation | Status |
|-------------|----------------|--------|
| Dialog role | `role="dialog"` + `aria-modal="true"` | ✅ Implemented |
| Focus trap | Captures first focusable, wraps on Tab | ✅ Implemented |
| Escape close | Closes dialog with proper focus management | ✅ Implemented |
| Overlay click | Closes when clicking outside content | ✅ Implemented |

## Related Components

- [Combobox](../combobox/README.md) — Editable combobox with list autocomplete
- [Tabs](../tabs/README.md) — Keyboard-navigable tab groups

## Storybook Stories

```tsx
import { Modal } from "./modal";

// Controls: title (string), isOpen (boolean), onClose (function)
// Docs: View focus trap patterns and keyboard navigation table
```
