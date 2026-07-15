# HANDOFF.md Template

This is the output format for Phase 6. Fill in all sections.

```markdown
# HANDOFF — <project-name>

**Generated:** <date>
**By:** web-app-builder skill

---

## Project Summary

<2-3 sentences from the App Brief — what the app does, who it's for>

## Stack

- **Framework:** <Next.js 15 / Vite + React / Astro>
- **Backend:** <Supabase / Drizzle / none>
- **Auth:** <Auth.js / Supabase Auth / none>
- **UI:** <shadcn/ui / Tailwind / none>
- **Testing:** Vitest + Playwright
- **Linting:** Biome
- **CI:** GitHub Actions

**Reasoning:** <1-2 sentences on why this stack>

## Entities

| Entity | Fields | Relations |
|--------|--------|-----------|
| <Entity1> | id, name, email, createdAt | has many <Entity2> |
| <Entity2> | id, title, status, <Entity1>Id | belongs to <Entity1> |

## Flows

1. <Flow 1> — NOT STARTED
2. <Flow 2> — NOT STARTED
3. <Flow 3> — NOT STARTED

## Pages

| Route | Description | Status |
|------|-------------|--------|
| `/` | Home/dashboard | placeholder |
| `/clients` | List + create clients | placeholder |
| `/clients/[id]` | Client detail | placeholder |

## Integrations

| Service | Purpose | Config Status |
|---------|---------|--------------|
| Supabase | DB + Auth | configured (placeholders) |
| Stripe | Billing | NOT CONFIGURED (needs API keys) |

## Auth

Model: <multi-tenant / single user / none>
Roles: <list or none>

## What's Done

- [x] Project scaffolded (<stack>)
- [x] TypeScript configured (strict + noUncheckedIndexedAccess)
- [x] Biome configured
- [x] Vitest configured
- [x] GitHub Actions CI
- [x] AGENTS.md created
- [x] Entity types generated: <list>
- [x] DB schema/migration created
- [x] Route structure created
- [x] OpenSpec specs written: entities, flows, pages, auth, integrations
- [x] Env vars placeholders in `.env.local`
- [x] Build passes (lint + typecheck + test + build)

## What's NOT Done (dev agent's job)

- [ ] UI components for each page
- [ ] Business logic for each flow
- [ ] Integration wiring (Supabase queries, Stripe webhooks, etc.)
- [ ] Tests for business logic
- [ ] Real environment variables
- [ ] Deploy

## Next Steps (for dev agent)

1. **<First thing to build>** — be specific: "Implement ClientList component in `src/components/ClientList.tsx` that fetches from Supabase and displays in a table. Use the Client type from `src/types/client.ts`."
2. **<Second thing>** — "Implement ClientForm with react-hook-form + Zod resolver using ClientInputSchema."
3. **<Third thing>** — "Wire up the /clients route to use ClientList and ClientForm."

## Gotchas

- <Any tricky thing: env vars, service setup, known issues, breaking changes>
- <e.g. "Supabase RLS policies are in the migration but NOT applied — run `supabase db push` after setting up the project">
- <e.g. "Auth.js v5 requires AUTH_SECRET env var — generate with `openssl rand -base64 32`">

## Commands

```bash
npm run dev          # dev server
npm run lint         # biome check
npm run lint:fix     # biome check --write
npm run typecheck    # tsc --noEmit
npm run test         # vitest (watch)
npm run test:run    # vitest (single run)
npm run build        # production build
```

## Env Vars Needed

```env
# .env.local (copy from .env.example)
NEXT_PUBLIC_SUPABASE_URL=<placeholder>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<placeholder>
# Add others as needed
```
```