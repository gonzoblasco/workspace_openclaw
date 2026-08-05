# ADR-008: SQLite for Development Instead of MySQL

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 3
**Scope:** Global

## Context

The book requires installing and configuring a MySQL server for development, including phpMyAdmin, Apache, and PHP. This is heavy overhead for a development environment.

## Decision

Use SQLite (via better-sqlite3) for local development. Keep the schema portable so switching to MySQL/PostgreSQL for production is straightforward.

## Rationale

- **Zero setup:** No MySQL server, no Apache, no phpMyAdmin
- **File-based:** Database is a single file (`dev.db`), easy to reset and version-control
- **Same SQL:** SQLite supports most SQL standard features including foreign keys, indexes, transactions
- **Drizzle ORM:** Schema is database-agnostic; switching to PostgreSQL/MySQL only requires changing the driver
- **Portable:** Works on any OS without package manager differences

## Consequences

- No MySQL installation needed
- No phpMyAdmin or Apache setup
- Database file can be deleted and recreated at any time
- Foreign key constraints must be enabled explicitly (`PRAGMA foreign_keys = ON`)
- Some MySQL-specific features (e.g., `FULLTEXT` indexes) are not available
- Production deployment would use PostgreSQL or MySQL with the same Drizzle schema

## References

- https://www.sqlite.org
- https://orm.drizzle.team/docs/quick-sqlite/better-sqlite3
