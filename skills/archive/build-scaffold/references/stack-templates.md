# Stack Templates — Build Scaffold Reference

Templates de stack para distintos perfiles de proyecto.

## Next.js + shadcn/ui (recomendado)

```bash
# Scaffold
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd my-app
npx shadcn@latest init -d

# Post-scaffold
npx @biomejs/biome init
```

**Includes:**
- Next.js 15 (App Router)
- TypeScript 5.x
- Tailwind CSS v4
- shadcn/ui components
- Biome (lint + format)
- Vitest + Testing Library
- Playwright (E2E)

## Vite + React Router

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install react-router-dom
npx @biomejs/biome init
```

**Includes:**
- Vite 6
- React 19
- React Router v7
- TypeScript 5.x
- Tailwind CSS v4
- Biome (lint + format)
- Vitest + Testing Library

## Express API

```bash
mkdir my-api && cd my-api
npm init -y
npm install express cors helmet
npm install -D typescript @types/express @types/node tsx
npx tsc --init
npx @biomejs/biome init
```

**Includes:**
- Express 5
- TypeScript 5.x
- Biome (lint + format)
- Vitest
- tsx (dev runner)

## Supabase Edge Functions

```bash
npx supabase init
npx supabase functions new my-function
```

**Includes:**
- Deno runtime
- TypeScript
- Supabase CLI
- Local emulator

## Monorepo (Turborepo)

```bash
npx create-turbo@latest my-monorepo
cd my-monorepo
npx @biomejs/biome init
```

**Includes:**
- Turborepo
- pnpm workspaces
- Shared configs (TypeScript, Biome)
- Apps + packages structure

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Biome Setup](./biome-setup.md) — Configuración de Biome
- [CI Templates](./ci-templates.md) — Templates de CI/CD
