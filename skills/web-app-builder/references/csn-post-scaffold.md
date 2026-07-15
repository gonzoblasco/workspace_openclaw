# CSN Post-Scaffold (What CSN gives you + what to add)

## What CSN provides automatically

When you run `npx create-stack-next <name>`, you get:

- Next.js 15 + React 19 + TypeScript estricto
- Biome (lint + format)
- Vitest (unit tests) + Playwright (e2e)
- Zod (runtime validation)
- GitHub Actions CI (lint, typecheck, test, build)
- AGENTS.md (agent instructions)
- HANDOFF.md, CHANGELOG.md, ROADMAP.md
- OpenSpec integrated (specs + slash commands)
- `.openclaw/` config
- `.agents/` config
- `docs/` with architecture, decisions, contributing guide
- `template-api/` available with `--template api`

## What you need to add after CSN

Depends on the stack decision. Install only what the decomposition requires:

### If Supabase backend
```bash
npm install @supabase/supabase-js @supabase/ssr
```
Create `src/lib/supabase/client.ts`:
```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```
Create `src/lib/supabase/server.ts`:
```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll() },
        setAll(cookiesToSet) {
          try { cookieStore.setAll(cookiesToSet) } catch {}
        },
      },
    }
  )
}
```

### If Auth.js (Auth.js v5)
```bash
npm install next-auth@beta @auth/core
```
Follow Auth.js v5 setup for Next.js App Router. Configure provider, callbacks, middleware.

### If Drizzle ORM (instead of Supabase)
```bash
npm install drizzle-orm better-sqlite3
npm install -D drizzle-kit
```
CSN template-api already includes Drizzle + SQLite config. Use that as reference.

### If shadcn/ui
```bash
npx shadcn@latest init
# Add components as needed:
npx shadcn@latest add button card input form table dialog
```

### If Tailwind
CSN does NOT include Tailwind by default. If UI needs it:
```bash
npm install -D tailwindcss @tailwindcss/postcss postcss
```
Configure `tailwind.config.ts` and `postcss.config.js`.

### If Stripe/billing
```bash
npm install stripe @stripe/stripe-js
```
Create `src/lib/stripe.ts` with client and webhook handler.

### If WhatsApp API
```bash
npm install @whatsapp/whatsapp-web.js
# or use cloud API via fetch
```

### Verify after additions
```bash
npm run lint && npm run typecheck && npm run test:run && npm run build
```

All must pass. Fix any issues caused by new dependencies.