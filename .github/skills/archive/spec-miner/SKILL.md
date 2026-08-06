---
name: "spec-miner"
description: "Analyze and reverse-engineer existing codebases: map architecture, extract contracts, identify dependencies, and generate summary specs."
metadata:
  version: 1.0.0
  author: Kanam
  tags: ["reverse-engineering", "code-analysis", "architecture", "documentation", "refactoring"]
allowed-tools:
  - read
  - exec
  - write
  - edit
  - skill_workshop
---

# Spec Miner

Analyze an existing codebase and produce a structured, human-readable specification of how it works. Inspired by the "Spec Miner" skill from the fullstack-dev-skills plugin, but focused on practical reverse engineering for brownfield projects.

## When to use

- You inherit or need to modify a codebase you didn't write.
- You need to understand the architecture before a refactor.
- You want to extract API contracts, data models, or business rules.
- You're preparing a handoff document or onboarding guide.
- You need to map dependencies between modules/services.
- You want to identify dead code, duplication, or tech debt hotspots.

## Workflow

1. **Scope the target** — file, module, service, or entire repo.
2. **Read key files** — entry points, config, package.json, main modules, tests.
3. **Map the structure** — directories, layers, public/private APIs.
4. **Trace data flow** — inputs, outputs, state, side effects.
5. **Extract contracts** — function signatures, types, schemas, API routes.
6. **Identify dependencies** — internal modules, external packages, infra.
7. **Flag risks** — circular deps, global state, untyped surfaces, missing tests.
8. **Write the spec** — save to `.knowledge/specs/extracted/<target>.md`.

## Output format

```markdown
# Spec: <Target Name>

## Purpose
One-sentence description.

## Entry Points
- `src/index.ts` — bootstraps the app
- `src/routes.ts` — registers HTTP routes

## Layers
| Layer | Responsibility | Key Files |
|---|---|---|
| API | HTTP handling | `src/routes/`, `src/middleware/` |
| Domain | Business logic | `src/services/` |
| Data | Persistence | `src/db/`, `src/models/` |

## Data Flow
1. Request → middleware → route handler
2. Handler calls service
3. Service queries DB via repository
4. Response mapped to DTO

## Contracts
### API
- `POST /users` — create user (body: CreateUserDTO)
- `GET /users/:id` — get user (returns UserDTO)

### Internal
- `createUser(data: CreateUserDTO): Promise<User>`

## Dependencies
- `express` — web framework
- `prisma` — ORM
- `zod` — validation

## Risks & Tech Debt
- Circular dependency between `users` and `auth` modules
- Several routes lack tests
- `any` types in `src/legacy/`
```

## Tools

- `read` — inspect files
- `exec` — run analysis commands (`tree`, `find`, dependency graphs, test coverage)
- `write/edit` — save extracted specs

## Best practices

- Start small: extract one module at a time, not the whole repo.
- Cross-check with tests: they reveal intended behavior.
- Don't rewrite code while mining specs. Read-only phase.
- Use the extracted spec as input for `openspec` or `agent-workflow` before changes.
- Save specs under `.knowledge/specs/extracted/` so they don't pollute source.

## Integration

- Pair with `agent-workflow` to plan refactors from extracted specs.

## Helper scripts relacionados

| Skill / Script | Uso |
|---|---|
| `tech-docs/scripts/analyze_codebase.py` | Analiza el codebase y extrae patrones para complementar el spec. Usar en pasos 2-4. |
| `product-discovery/scripts/generate-openspec.sh` | Genera un OpenSpec formal desde el spec extraido. Usar en el paso 8. |
| `knowledge-management/scripts/knowledge-graph.py` | Mapea relaciones entre documentos y modulos. Usar en paso 6. |

- Pair with `code-review-agent` to validate that changes match the spec.
- Pair with `architecture-designer` for larger restructuring.
