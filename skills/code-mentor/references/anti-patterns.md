# Common Anti-Patterns

## React

### ❌ useState for derived state
```tsx
// Bad: derived state that can desync
const [fullName, setFullName] = useState(`${firstName} ${lastName}`)

// Good: compute it
const fullName = `${firstName} ${lastName}`
```

### ❌ useEffect for data fetching without cleanup
```tsx
// Bad: race condition on rapid navigation
useEffect(() => {
  fetch(`/api/user/${id}`).then(r => r.json()).then(setUser)
}, [id])

// Good: abort controller or use a data-fetching library
useEffect(() => {
  const controller = new AbortController()
  fetch(`/api/user/${id}`, { signal: controller.signal })
    .then(r => r.json())
    .then(setUser)
    .catch(e => { if (e.name !== 'AbortError') throw e })
  return () => controller.abort()
}, [id])
```

### ❌ Missing keys or index as key
```tsx
// Bad: index as key breaks on reorder
{items.map((item, i) => <Item key={i} {...item} />)}

// Good: stable unique id
{items.map(item => <Item key={item.id} {...item} />)}
```

### ❌ useMemo / useCallback everywhere
```tsx
// Bad: premature optimization, adds cognitive overhead
const handleClick = useCallback(() => doThing(value), [value])

// Good: only when passed to memo'd children or used in deps
const handleClick = () => doThing(value) // fine for native elements
```

## TypeScript

### ❌ any as escape hatch
```ts
// Bad: loses all type safety
const data: any = await fetchData()

// Good: unknown + type guard, or proper typing
const data: unknown = await fetchData()
if (isUser(data)) { /* data is User */ }
```

### ❌ Overly narrow types
```ts
// Bad: breaks when API adds fields
type User = { name: string; email: string }

// Good: only type what you use, or use Pick/Partial
type User = { name: string; email: string; [key: string]: unknown }
```

### ❌ enum for simple constants
```ts
// Bad: enum generates extra JS, non-standard
enum Status { Active, Inactive }

// Good: const assertion or string union
const Status = { Active: 'active', Inactive: 'inactive' } as const
type Status = (typeof Status)[keyof typeof Status]
// Or simply:
type Status = 'active' | 'inactive'
```

## Next.js

### ❌ 'use client' on entire page
```tsx
// Bad: loses all server rendering benefits
'use client'
export default function Page() { ... }

// Good: push 'use client' down to the interactive leaf
// page.tsx (server component)
import { InteractiveForm } from './form'
export default function Page() {
  const data = await fetchData() // server-side
  return <InteractiveForm initialData={data} />
}
```

### ❌ fetch in client component
```tsx
// Bad: exposes API route, loses server benefits
'use client'
useEffect(() => { fetch('/api/data').then(...) }, [])

// Good: fetch in server component, pass as props
export default async function Page() {
  const data = await fetch('https://...')
  return <ClientView data={data} />
}
```

## General

### ❌ Premature abstraction
```ts
// Bad: abstracting before you see the pattern
function createButton(variant: string, size: string, ...) { ... }

// Good: write it twice, abstract on the third use
<button className="primary large">Save</button>
<button className="primary small">Cancel</button>
// Now you see the pattern → extract
```

### ❌ Comments that explain what, not why
```ts
// Bad: explains what the code already says
// Loop through users
for (const user of users) { ... }

// Good: explains why
// Sort by join date to maintain FIFO queue semantics
for (const user of users) { ... }
```

### ❌ Catching errors without handling
```ts
// Bad: swallows the error silently
try { await riskyOp() } catch (e) { /* ignore */ }

// Good: at minimum log it, ideally handle or rethrow
try { await riskyOp() } catch (e) {
  console.error('riskyOp failed:', e)
  // fallback behavior or rethrow
}
```
