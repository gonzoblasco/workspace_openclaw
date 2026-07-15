---
name: "web-app-builder"
description: "\"From idea to ready-to-code: discover, decompose, choose stack, scaffold, generate domain structure, and hand off to dev.\""
---

# Web App Builder

Use when someone has an idea for a web app and needs to go from "tengo una idea" to "proyecto listo para programar". Covers discovery, decomposition, stack decision, scaffolding, domain structure, and handoff — but does NOT write business logic or UI components.

## Scope

This skill is the bridge between idea and development. It does NOT write the app. It:

1. Defines the app with the user (iterative)
2. Chooses the right stack
3. Scaffolds the project (everything configured)
4. Generates domain structure (entities, types, schema, routes, specs)
5. Hands off to a development agent with full instructions

The development agent receives: project structure, OpenSpec specs, entity types, DB schema, route map, HANDOFF.md. It programs from there.

## Prerequisites

- Node.js 24+, npm/pnpm/bun
- `npx create-stack-next` available (for Next.js projects)
- Supabase CLI (if backend uses Supabase)
- Git configured

## Phase 1 — Discovery (with the user)

Goal: understand what they want to build. Iterate until the idea is clear enough to decompose.

1. **Ask what they want to build** — "quiero un CRM para vendedores de ML"
2. **Ask clarifying questions** (2-4 max, not an interrogation):
   - Who uses it? (single user, team, multi-tenant)
   - What are the main things they manage? (clients, sales, tasks...)
   - Any integrations? (payments, WhatsApp, email, external APIs)
   - Web-only or mobile too?
3. **Propose a brief** — 3-5 sentences describing the app. User confirms or corrects.
4. **Iterate** — if user says "también necesito X" or "no, eso no", update the brief. Repeat until user says "eso es" or similar.

Output of Phase 1: **App Brief** — a clear description of what to build.

## Phase 2 — Decomposition

Goal: break the app brief into concrete parts. Present to user for validation.

1. **Identify entities** — the core data objects (Client, Sale, Task, Message...). List with fields and relationships.
2. **Identify flows** — the main user journeys (create client, log sale, send message, view dashboard...). 3-7 flows max for MVP.
3. **Identify pages/views** — what screens the app needs. Map to flows.
4. **Identify integrations** — external services (Supabase, Stripe, WhatsApp API, ML API, email...). List what each does.
5. **Identify auth model** — no auth, single user, multi-user, multi-tenant. What roles if any.
6. **Present decomposition to user** in a compact format:
   - Entities (table or list)
   - Flows (numbered)
   - Pages (list)
   - Integrations (list)
   - Auth model (one line)
7. **Iterate** — user adds, removes, corrects. Repeat until user confirms.

Output of Phase 2: **Decomposition Document** — entities, flows, pages, integrations, auth.

## Phase 3 — Stack decision

Goal: choose the right technical stack based on the decomposition. Present reasoning to user.

### Decision matrix

- **CRUD / internal tool / dashboard** (no SEO needed, app-style) → Vite + React + Supabase
- **SaaS multi-tenant** (needs SSR, SEO, auth, billing) → Next.js (CSN) + Supabase + Auth.js
- **Landing / marketing / portfolio** (content-heavy, SEO critical) → Astro + React islands (or static HTML)
- **API / backend only** (no UI, pure endpoints) → CSN `--template api` or Hono
- **Multi-agent / complex realtime** (websockets, streams, orchestration) → Vite + React + Hono backend (case-by-case)

### When Next.js → use CSN

If the decision is Next.js, use `npx create-stack-next <name>`. CSN already provides:
- Next.js 15 + React 19 + TS estricto + Biome + Vitest + Playwright + Zod
- AGENTS.md, HANDOFF.md, CHANGELOG.md, ROADMAP.md
- OpenSpec integrated
- GitHub Actions CI

Skip manual setup — CSN does it. Go directly to Phase 5 (domain structure).

### When not Next.js → manual scaffold

For Vite + React, Astro, or other stacks, scaffold manually. See `references/vite-react-setup.md` and `references/astro-setup.md` for exact steps.

Every stack gets (no exceptions):
- TypeScript estricto + `noUncheckedIndexedAccess`
- Biome (lint + format)
- Vitest (unit tests)
- Zod (runtime validation)
- AGENTS.md (agent instructions, project-specific)
- HANDOFF.md (handoff log)
- CHANGELOG.md
- ROADMAP.md (with phases and epics from decomposition)
- OpenSpec (specs + changes structure)
- `.openclaw/` config
- GitHub Actions CI (lint, typecheck, test, build)

1. **Present stack decision to user** with reasoning. One paragraph, not a table.
2. **User confirms or adjusts** — they might say "use TanStack Start instead of Next.js" or "I want Drizzle not Supabase".
3. **Record the decision** as an ADR in `docs/decisions/`.

Output of Phase 3: **Stack Decision** — chosen stack + reasoning + ADR.

## Phase 4 — Scaffolding

Goal: create the project with everything configured. This is the 70% — detailed, complete.

### 4a — Next.js (via CSN)

```bash
npx create-stack-next <project-name>
# or with API template:
npx create-stack-next <project-name> --template api
cd <project-name>
```

Then:
- Install additional deps from stack decision (Supabase client, Auth.js, shadcn/ui, Drizzle if needed)
- Configure `.env.local` with placeholders for all env vars
- Initialize OpenSpec if not already: `npx openspec init` (CSN does this, verify)
- Verify: `npm run lint && npm run typecheck && npm run test:run && npm run build`

### 4b — Vite + React (manual)

See `references/vite-react-setup.md` for complete step-by-step.

Summary:
1. `npm create vite@latest <name> -- --template react-ts`
2. Install: Biome, Vitest, Zod, React Router, TanStack Query (if needed), Supabase client (if needed)
3. Configure: `tsconfig.json` (strict + noUncheckedIndexedAccess), `biome.json`, `vitest.config.ts`
4. Create structure: `src/components/`, `src/lib/`, `src/hooks/`, `src/pages/`, `src/types/`
5. Create: `AGENTS.md`, `HANDOFF.md`, `CHANGELOG.md`, `ROADMAP.md`, `.openclaw/`
6. Init OpenSpec: `npx openspec init`
7. Setup GitHub Actions: lint, typecheck, test, build
8. Verify: `npm run lint && npm run typecheck && npm run test:run && npm run build`

### 4c — Astro (manual)

See `references/astro-setup.md` for complete step-by-step.

### 4d — Verification gate

Before proceeding to Phase 5, verify:
```bash
npm run lint      # biome check
npm run typecheck # tsc --noEmit
npm run test:run  # vitest single run
npm run build     # production build
```

All must pass. If any fails, fix before continuing. No exceptions.

Output of Phase 4: **Working project skeleton** — lint, typecheck, tests, build all green.

## Phase 5 — Domain structure

Goal: generate the structural artifacts derived from the decomposition. This is NOT business logic — it's the skeleton of the domain.

1. **Entity types** — for each entity from Phase 2, create `src/types/<entity>.ts` with TypeScript interfaces. Include fields, relations, Zod schemas. Use `references/entity-template.md` as base.
2. **DB schema** — if using Supabase: write SQL migration in `supabase/migrations/` with tables, RLS policies, indexes. If using Drizzle: write `src/db/schema.ts`.
3. **Route structure** — create route files/ directories for each page from Phase 2. Empty but named correctly. Include layout if needed.
4. **OpenSpec specs** — write `openspec/specs/` with:
   - `entities.md` — entity definitions, fields, relationships
   - `flows.md` — user flows described step by step
   - `pages.md` — page list with what each shows and does
   - `auth.md` — auth model, roles, permissions
   - `integrations.md` — external services, what each does, config needed
5. **API routes** (if applicable) — create route handlers / endpoint files for CRUD operations on each entity. Empty handlers with correct signatures and Zod validation schemas.
6. **Seed data** (optional) — if user wants demo data, create `src/lib/seed.ts` with sample entities.

Do NOT implement business logic. Do NOT write UI components beyond placeholder text. Do NOT design visual layouts.

Output of Phase 5: **Domain skeleton** — types, schema, routes, specs. Everything structural, nothing behavioral.

## Phase 6 — Handoff

Goal: leave a development agent ready to code without asking anything.

1. **Write `HANDOFF.md`** using `references/handoff-template.md` as base. Must include:
   - **Project summary** — what the app does (from App Brief)
   - **Stack** — what was chosen and why (from Stack Decision)
   - **Entities** — list with fields and relations
   - **Flows** — numbered list with status (not started)
   - **Pages** — list with status (placeholder only)
   - **Integrations** — list with config status (not configured / configured)
   - **Auth** — model and status
   - **What's done** — everything the skill produced (scaffold, types, schema, routes, specs)
   - **What's NOT done** — what the dev agent needs to build (UI components, business logic, integrations wiring, tests for business logic)
   - **Next steps** — ordered list of what to do first, second, third. Be specific: "1. Implement ClientForm component in src/components/ClientForm.tsx using the Zod schema from src/types/client.ts"
   - **Gotchas** — anything tricky (env vars needed, external service setup, known issues)
   - **Commands** — how to run dev, test, build, deploy
   - **Env vars needed** — list with placeholder values

2. **Write `ROADMAP.md`** with phases and epics from the decomposition. Mark Phase 1 (MVP) as in progress with the specific epics.

3. **Write `CHANGELOG.md`** entry: "Initial project generation from web-app-builder skill" with everything that was created.

4. **Verify everything compiles:**
   ```bash
   npm run lint && npm run typecheck && npm run test:run && npm run build
   ```

5. **Git init + initial commit:**
   ```bash
   git init
   git add -A
   git commit -m "feat: initial project scaffold via web-app-builder"
   ```

6. **Update workspace memory** — `memory/YYYY-MM-DD.md` with what was built, where it lives, what's next.

Output of Phase 6: **Ready-to-code project** with HANDOFF.md that a development agent can read and start coding immediately.

## What this skill does NOT do

- Write UI components (beyond placeholder text in routes)
- Implement business logic
- Design visual/UX layouts
- Configure external services that need real credentials (Stripe, WhatsApp API, etc.)
- Write tests for business logic (only scaffold test setup)
- Deploy to production (only verify build works)

These are the development agent's job. The skill leaves everything ready for it.

## Iteration

The user can come back to the skill at any point:
- "Quiero agregar una entidad" → go to Phase 2, add entity, update specs, types, schema, routes, HANDOFF
- "Cambié de stack" → go to Phase 3, re-scaffold or migrate, update HANDOFF
- "Ya tengo el scaffold, ahora quiero definir otra feature" → Phase 2 for the new feature, Phase 5 for structure updates

The skill is iterative. Not all phases are required every time.

## References

- `references/vite-react-setup.md` — complete Vite + React scaffold steps
- `references/astro-setup.md` — complete Astro scaffold steps
- `references/csn-post-scaffold.md` — what CSN gives you and what to add after
- `references/entity-template.md` — template for entity type files
- `references/handoff-template.md` — template for HANDOFF.md output
