# Tabs

Keyboard-navigable tabbed interface with manual activation mode.

## ARIA Pattern

[Tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/)

**Decision:** Manual activation mode chosen over automatic. Better UX for keyboard users, simpler state management.

## Props

```typescript
interface TabGroupProps {
   label?: string;  // Accessibility text (required if children has no labels)
   options: Option[]; // Array of tab options with value and label
   children: React.ReactNode; // Tabs content panels
}

type Option = { 
   value: number | string; // Unique identifier for each panel
   label: string; // Displayed text for the option
};
```

## Keyboard Interactions

| Key | Behavior | ARIA Reference |
|-----|----------|-----------------|
| `ArrowRight` | Next tab (wrap to first) | APG: "keyboard focus navigation" |
| `ArrowLeft` | Prev tab (wrap to last) | APG: "focus management" |
| `Home` | Focus first tab | APG: "panel navigation shortcuts" |
| `End` | Focus last tab | APG: "panel navigation shortcuts" |
| `Space` / `Enter` | Activate current tab (manual activation mode) | APG: "panel activation methods" |

## Usage Example

```tsx
import { Tabs } from '@gonzoblasco/accessible-ui';

function DocumentTabs() {
   const options = [
      { value: 0, label: "Overview" },
      { value: 1, label: "Settings" },
      { value: 2, label: "Help" }
    ];

   return <TabGroup 
      options={options} 
      children={...}
    />;
}
```

## Implementation Details

### Hook System (`useTabs`)

Returns pure functions for unit testing:

```typescript
{
   activeIndex: number;     // Currently active panel index
   togglePanel: (index: number) => void; // Toggle selection
   navigateNext: () => void; // Move to next panel
   navigatePrev: () => void; // Move to previous panel
}
```

### Manual Activation Mode

| Event | Action | Rationale |
|-------|--------|-----------|
| `ArrowRight`/`ArrowLeft` | Focus moves, no state change | Better UX — arrows indicate navigation, not activation |
| `Space` / `Enter` | Activate current tab | Matches native HTML `<details>` + `<summary>` pattern |

## Accessibility Highlights

| Requirement | Implementation | Status |
|-------------|----------------|--------|
| Tablist role | `role="tablist"` on wrapper | ✅ Implemented |
| Panel roles | `role="tabpanel"` with aria-selected | ✅ Implemented |
| Active panel selection | Dynamic aria-selected attribute | ✅ Implemented |
| Keyboard navigation | Full arrow/keys support | ✅ Implemented |

## Related Components

- [Modal](../modal/README.md) — Focus-trapped dialog
- [Combobox](../combobox/README.md) — Editable combobox with autocomplete
