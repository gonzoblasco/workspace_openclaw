# Modal

Focus-trapped dialog following the WAI-ARIA Dialog pattern.

## ARIA Pattern

[Dialog (Modal)](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)

## Props

```typescript
type ModalProps = {
   title?: string;
   isOpen: boolean;
   onClose?: () => void;
   children?: React.ReactNode;
};
```

## Keyboard Interactions

| Key | Behavior |
|-----|----------|
| `Escape` | Close immediately, save focus on next tabbable |
| `Tab` (forward/backward) | Cycle only within dialog (not escape overlay) |
| `Space` / `Enter` | Activate button if focused |

## Usage Example

```tsx
<Modal isOpen={isOpen} onClose={onClose}>
   <h2 className="sr-only">{title}</h2>
   {/* content */}
</Modal>
```

## Hook

```tsx
import useModal from "./use-modal";

function Modal(props: ModalProps): JSX.Element {
   const state = useModal(props);
   // state.isOpen, state.focusTrap, etc.
   return <div {...state.props} />;
}
```
