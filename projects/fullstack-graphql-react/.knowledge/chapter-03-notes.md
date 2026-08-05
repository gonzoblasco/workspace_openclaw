# Chapter 3: Connecting to the Database

## Core Concepts

1. **GraphQL is database agnostic:** Apollo doesn't care where data comes from
2. **ORM (Object-Relational Mapping):** Abstraction layer between code and database tables
3. **Database models:** Define table structure, field types, constraints
4. **Migrations:** Version-controlled database schema changes
5. **Seeders:** Test data for development
6. **Foreign keys:** Relationships between tables (one-to-one, one-to-many, many-to-many)
7. **Join tables:** Required for many-to-many relationships in SQL
8. **CASCADE deletes:** Deleting a user also deletes their posts
9. **Resolvers with DB:** Replace in-memory data with database queries

## Key Changes from Book

| Book (2020) | Modern (Aug 2026) | Reason |
|---|---|---|
| Sequelize ORM | Drizzle ORM | Modern, TypeScript-first, zero-config |
| MySQL server | SQLite (better-sqlite3) | Zero setup for development |
| `sequelize-cli` | `drizzle-kit push` | Schema sync instead of migration files |
| `queryInterface.bulkInsert` | `db.insert().values()` | Native Drizzle API |
| `Model.findAll()` | `db.select().from(table)` | SQL-like query builder |
| `belongsTo`/`hasMany` | Manual JOINs | More explicit, no magic |
| `babel-plugin-require-context-hook` | Not needed | Drizzle doesn't auto-load models |
| phpMyAdmin | Not needed | SQLite file, inspect with any SQLite viewer |
| MySQL foreign keys | SQLite foreign keys | Same concept, slightly different syntax |

## Database Schema

```
users (id, avatar, username, created_at, updated_at)
posts (id, text, user_id -> users.id, created_at, updated_at)
chats (id, created_at, updated_at)
messages (id, text, user_id -> users.id, chat_id -> chats.id, created_at, updated_at)
user_chats (user_id -> users.id, chat_id -> chats.id, created_at, updated_at)
```

## Relationships
- **User → Post:** One-to-many (user has many posts, post belongs to user)
- **User ↔ Chat:** Many-to-many (via user_chats join table)
- **Chat → Message:** One-to-many (chat has many messages)
- **User → Message:** One-to-many (user has many messages)

## ADRs Created
- ADR-007: Replace Sequelize with Drizzle ORM
- ADR-008: SQLite for Development Instead of MySQL

## Running the Chapter 3 Project

```bash
cd projects/fullstack-graphql-react/chapter-03
npm run seed       # Insert test data
npm run server     # Development server with auto-reload
```

Test GraphQL:
```bash
# Query posts with users
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ posts { id text user { username } } }"}'

# Query chats with users and messages
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ chats { id users { id username } messages { id text user { username } } } }"}'

# Add a post
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { addPost(post: {text: \"Hello\"}) { id text user { username } } }"}'
```
