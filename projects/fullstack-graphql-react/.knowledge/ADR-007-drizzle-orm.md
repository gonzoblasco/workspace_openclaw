# ADR-007: Replace Sequelize with Drizzle ORM

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 3
**Scope:** Global

## Context

The book uses Sequelize ORM with MySQL for database access. Sequelize requires:
- `sequelize-cli` for migrations and seeds
- `babel-plugin-require-context-hook` for auto-loading models
- Complex configuration with `config/index.js` and environment switching
- Manual model association setup

## Decision

Replace Sequelize with Drizzle ORM using SQLite (via better-sqlite3) for development.

## Rationale

- **TypeScript-first:** Drizzle is built for TypeScript/ESM from the ground up
- **No CLI magic:** Schema is plain code, no CLI-generated boilerplate
- **SQL-like API:** Drizzle's query builder maps directly to SQL concepts
- **Zero-config migrations:** `drizzle-kit push` syncs schema to DB automatically
- **Lightweight:** No model auto-loading, no hooks, no complex config
- **SQLite for dev:** Zero setup, no MySQL server needed for development
- **Same concepts:** Models, migrations, seeds, relationships — all present

## Consequences

- Schema defined in `drizzle/schema.js` instead of Sequelize model files
- Migrations via `drizzle-kit push` instead of `sequelize db:migrate`
- Seeds are plain JS files using Drizzle API instead of `queryInterface.bulkInsert`
- No `sequelize-cli`, no `babel-plugin-require-context-hook`
- Database is SQLite file (`drizzle/dev.db`) instead of MySQL server
- For production, switch datasource to PostgreSQL/MySQL with same Drizzle API

## Pattern Comparison

| Concept | Sequelize (Book) | Drizzle (Modern) |
|---|---|---|
| Schema definition | Model class + migration file | Plain JS object in schema file |
| Migrations | `sequelize db:migrate` | `drizzle-kit push` |
| Seeds | `queryInterface.bulkInsert` | `db.insert(table).values(...)` |
| Queries | `Model.findAll({ where: ... })` | `db.select().from(table).where(eq(...))` |
| Relationships | `belongsTo`, `hasMany` | Manual JOINs or relations API |
| DB setup | MySQL server required | SQLite file, zero setup |

## References

- https://orm.drizzle.team
- https://github.com/JoshuaWise/better-sqlite3
