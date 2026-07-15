# Entity Type Template

Use this as the base for each entity type file.

```typescript
// src/types/<entity>.ts
import { z } from 'zod'

// === Schema ===
export const <Entity>Schema = z.object({
  id: z.string().uuid(),
  // Add fields from decomposition
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
})

// === Type ===
export type <Entity> = z.infer<typeof <Entity>Schema>

// === Input (for create) ===
export const <Entity>InputSchema = <Entity>Schema.omit({
  id: true,
  createdAt: true,
  updatedAt: true,
})
export type <Entity>Input = z.infer<typeof <Entity>InputSchema>

// === Update (for patch) ===
export const <Entity>UpdateSchema = <Entity>InputSchema.partial()
export type <Entity>Update = z.infer<typeof <Entity>UpdateSchema>
```

## Field type reference

Use these Zod types for common field patterns:

- `z.string()` — text
- `z.string().email()` — email
- `z.string().url()` — URL
- `z.string().uuid()` — UUID
- `z.number().positive()` — price/quantity
- `z.number().int()` — count
- `z.boolean()` — flag
- `z.date()` — date (or `z.string().datetime()` for ISO strings)
- `z.enum(['option1', 'option2'])` — enum/status
- `z.array(z.string())` — tags/list
- `z.record(z.string(), z.unknown())` — JSON/metadata
- `z.string().nullable()` — optional nullable field

## Relationships

- Foreign key: `z.string().uuid()` referencing another entity
- Many-to-many: use a junction table with two FK fields
- Self-reference: `z.string().uuid().nullable()` (parent_id)

## Validation rules

- Required: field is in the schema (not optional)
- Optional: `z.string().optional()`
- With default: `z.string().default('active')`
- Conditional: use `.refine()` or `.superRefine()`
- String length: `z.string().min(1).max(255)`
- Pattern: `z.string().regex(/^\d+$/)`