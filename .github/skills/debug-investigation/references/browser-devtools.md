# Browser DevTools Guide — Debug Investigation Reference

Técnicas de debugging en Chrome DevTools.

## Console

### Conditional Breakpoints

```javascript
// Right-click line number → "Add conditional breakpoint"
// Only pauses when condition is true
x === undefined
user.id === 42
items.length > 100
```

### Console Utilities

```javascript
// Inspect element
$0  // Last inspected element
$$('button')  // All buttons
$x('//button')  // XPath

// Monitor events
monitorEvents(window, 'resize')
monitorEvents(document.body, 'click')

// Debug function calls
debug(myFunction)
undebug(myFunction)
```

## Sources Tab

### Blackboxing

Right-click script → "Blackbox script" to skip library code during debugging.

### Call Stack

- **Async stack traces:** Show full async chain
- **Frame navigation:** Click any frame to inspect scope/variables
- **Restart frame:** Right-click → "Restart frame" to re-run from that point

### Watch & Scope

- **Watch:** Add expressions to evaluate on every pause
- **Scope:** Local, Closure, Global variables
- **Breakpoints:** All breakpoints listed, toggleable

## Network Tab

### Filtering

```text
-status:404  // Show everything except 404s
larger-than:1k  // Responses > 1KB
method:POST  // Only POST requests
mime-type:application/json  // Only JSON responses
```

### Throttling

Network conditions → throttling → simulate Slow 3G/Offline.

### Blocking Requests

Right-click request → "Block request domain" to test without a dependency.

## Performance Tab

### Recording

1. Start recording
2. Reproduce the issue
3. Stop recording

### Reading the Flame Chart

- **Long tasks:** Red bars at top
- **Layout thrashing:** Purple bars (forced reflows)
- **JavaScript:** Yellow bars
- **Rendering:** Purple bars
- **Painting:** Green bars

### Key Metrics

- **FPS:** Green = 60fps, Red = dropped frames
- **CPU:** % used per frame
- **Network:** Request timing waterfall

## Application Tab

### Storage

- **Local Storage / Session Storage:** View and edit
- **IndexedDB:** Browse databases
- **Cookies:** View, edit, delete
- **Cache Storage:** Service Worker caches

### Service Workers

- **Offline:** Check "Offline" to test without network
- **Update on reload:** Force SW update
- **Bypass for network:** Skip SW for debugging

## Rendering Tab

- **Paint flashing:** Highlights repainted areas
- **Layout shift regions:** Shows CLS (Cumulative Layout Shift)
- **FPS meter:** Real-time frame rate
- **Emulate CSS media:** prefers-color-scheme, prefers-reduced-motion

## Memory Tab

### Heap Snapshot

1. Take snapshot
2. Reproduce the issue
3. Take another snapshot
4. Compare: "Summary" → "Comparison" → "Containment"

### Allocation Timeline

- Records allocations over time
- Useful for finding memory leaks
- Shows what functions allocate memory

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Techniques](../references/techniques.md) — Técnicas de debugging
- [Node Debugging](./node-debugging.md) — Debugging en Node.js
