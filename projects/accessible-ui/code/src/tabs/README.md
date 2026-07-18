# Tabs

Keyboard-navigable tabbed interface with manual activation mode.

## ARIA Pattern

[Tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/)

**Decision:** Manual activation chosen over automatic. Better UX for keyboard users, simpler state management.

## Props

```typescript
type TabGroupProps = {
   label?: string;
   children: ReactNode;
};

type TabPanelProps = {
   value: number | string;
   label: string;
   children?: ReactNode;
};
```

## Keyboard Interactions

| Key | Behavior |
|-----|----------|
| `ArrowRight` | Next tab (wrap to first) |
| `ArrowLeft` | Prev tab (wrap to last) |
| `Home` | Focus first tab |
| `End` | Focus last tab |
| `Space` / `Enter` | Activate current tab (manual activation) |

## Usage Example

```tsx
<Tabs label="Tabs Group">
   <TabPanel value={0} label="Item 1">Content 1</TabPanel>
   <TabPanel value={1} label="Item 2">Content 2</TabPanel>
   <TabPanel value={2} label="Item 3">Content 3</TabPanel>
</Tabs>
```

## Hook

```tsx
import useTabs from "./use-tabs";

function Tabs(props: TabGroupProps): JSX.Element {
   const state = useTabs(props);
    // state.activeIndex, etc.
   return <div {...state.props} />;
}
```
