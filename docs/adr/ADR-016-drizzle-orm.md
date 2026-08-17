# ADR-016: Drizzle ORM as Default SQL ORM

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Extracted from Full-Stack GraphQL + React book processing
**Scope:** Global - all new Node.js projects with SQL databases

## Context

Sequelize has been the dominant Node.js ORM for years, but the ecosystem has shifted. Prisma gained popularity but introduced complexity with its own CLI, schema format, and driver adapters. Drizzle ORM offers a simpler, SQL-native approach.

## Decision

Use Drizzle ORM as the default SQL ORM for new projects. Fall back to Prisma only when specific features (e.g., Prisma Accelerate, Pulse) are required.

## Rationale

- **SQL-like API:** Drizzle's query builder maps directly to SQL - `select`, `where`, `join`, `insert`, `update`
- **No CLI dependency:** Schema is plain code, migrations are optional (`drizzle-kit push` for dev, `drizzle-kit generate` for production)
- **TypeScript-first:** Full type safety without code generation
- **Database agnostic:** Same API for SQLite, PostgreSQL, MySQL, Turso, D1
- **Lightweight:** No model auto-loading, no hooks, no complex config
- **Zero-config dev:** SQLite for development, switch to PostgreSQL for production

## Pattern

```js
// schema.js
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';
export const users = sqliteTable('users', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name'),
});

// queries
import { db } from './database.js';
import { users } from './schema.js';
import { eq } from 'drizzle-orm';

const result = db.select().from(users).where(eq(users.id, 1)).get();
```

## When to Use Alternatives

- **Prisma:** When using Prisma Accelerate (edge caching), Pulse (change data capture), or when the team already knows Prisma
- **Knex.js:** When you need raw SQL with a query builder but no ORM features
- **Raw SQL:** For simple projects with few tables

## References

- https://orm.drizzle.team
- ADR-007: Replace Sequelize with Drizzle ORM
- ADR-008: SQLite for Development Instead of MySQL
