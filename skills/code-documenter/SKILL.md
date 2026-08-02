---
name: "code-documenter"
description: "Generate inline documentation, OpenAPI specs, READMEs, and handoff docs from code."
metadata:
  version: 1.0.0
  author: Kanam
  tags: ["documentation", "openapi", "readme", "handoff", "comments", "dx"]
allowed-tools:
  - read
  - write
  - edit
  - exec
  - skill_workshop
---

# Code Documenter

Generate useful technical documentation from code. Not pointless comments that repeat the code, but explanations of *why*, *how to use*, and *what the boundaries are*.

## When to use

- A function or module is complex enough to need explanation.
- You need an OpenAPI spec from existing API routes.
- You want a README for a project, package, or module.
- You're handing off a feature and need context docs.
- You want a CHANGELOG entry for a release.
- You need examples for a public API.

## What not to document

- Self-evident code (`// increment counter`)
- Trivial getters/setters
- Anything that duplicates the function name

## Documentation types

### 1. Inline documentation

Add comments for:
- Non-obvious algorithms or business rules
- External assumptions
- Error handling strategies
- Performance trade-offs

### 2. Function/module JSDoc/TSDoc

```typescript
/**
 * Normalizes a Mercado Libre listing title for search.
 * - Trims whitespace
 * - Removes special characters that break tokenization
 * - Lowercases for consistent matching
 *
 * @param rawTitle - Original title from ML API
 * @returns Clean title ready for indexing
 * @throws {InvalidTitleError} if rawTitle is empty or exceeds 255 chars
 */
```

### 3. OpenAPI specs

From API routes, extract:
- Paths and methods
- Request/response schemas
- Auth requirements
- Error responses

Save as `openapi.yaml` or similar.

### 4. READMEs

Structure:
- What is this
- Install / setup
- Usage example
- API surface
- Development commands
- Decision records

### 5. Handoff notes

For a completed feature, write:
- What was built
- Why these decisions were made
- How to extend it
- Known limitations

Save as `.knowledge/HANDOFF.md` or `.knowledge/handoffs/<feature>.md`.

## Workflow

1. **Target** — choose file, module, or API surface.
2. **Read** — understand what it does.
3. **Identify gaps** — what's missing or unclear.
4. **Draft** — write docs inline or in dedicated files.
5. **Review** — check accuracy, tone, and completeness.
6. **Commit** — docs go with the code.

## Tools

- `read` — inspect code
- `write/edit` — add comments, READMEs, OpenAPI files
- `exec` — run doc generators if available (TypeDoc, Swagger, etc.)

## Best practices

- Document intent, not mechanics.
- Keep docs close to code.
- Update docs when code changes.
- Use examples for public APIs.
- Prefer English for code-facing docs (matches your GitHub rule).

## Integration

- Pair with `spec-miner` to document code you didn't write.
- Pair with `agent-workflow` so documentation is a task in the plan.
- Pair with `openspec` to derive docs from agreed specs.
