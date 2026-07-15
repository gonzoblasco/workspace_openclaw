# Vite + React Setup (Complete)

Use when stack decision is Vite + React (no SSR needed, app-style, internal tool, dashboard).

> **Last verified:** 2026-07-15 with Vite 8, React 19, TypeScript 6, Biome 2.5, Vitest 4, Tailwind v4

## Steps

### 1. Scaffold
```bash
npm create vite@latest <project-name> -- --template react-ts
cd <project-name>
```

### 2. Install dependencies
```bash
npm install
npm install -D @biomejs/biome vitest @testing-library/react @testing-library/jest-dom jsdom @types/node
npm install zod react-router-dom @tanstack/react-query
# If Supabase:
npm install @supabase/supabase-js
# If forms:
npm install react-hook-form @hookform/resolvers
# If charts:
npm install recharts
# If UI components (Tailwind v4):
npm install tailwindcss @tailwindcss/vite lucide-react
# shadcn/ui: install per-component via npx shadcn@latest add <component>
```

### 3. Configure TypeScript
`tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },
    "ignoreDeprecations": "6.0"
  },
  "include": ["src"]
}
```

> **Note:** `baseUrl` is deprecated in TS 7.0 but still needed for path aliases in Vite. `ignoreDeprecations: "6.0"` silences the warning. Without `baseUrl`, use `paths` with relative resolution and `moduleResolution: "bundler"` only.

### 4. Configure Biome (2.5+)
`biome.json`:
```json
{
  "$schema": "https://biomejs.dev/schemas/2.5.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": true
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "assist": {
    "actions": {
      "source": {
        "organizeImports": "on"
      }
    }
  },
  "linter": {
    "enabled": true,
    "rules": {
      "preset": "recommended"
    }
  },
  "css": {
    "parser": {
      "tailwindDirectives": true
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "asNeeded"
    }
  }
}
```

> **Breaking changes from Biome 1.x → 2.x:**
> - `organizeImports` top-level key → moved to `assist.actions.source.organizeImports`
> - `linter.rules.recommended: true` → `linter.rules.preset: "recommended"`
> - Schema version must match installed version (`npx biome --version` to check)
> - `css.parser.tailwindDirectives: true` is REQUIRED for Tailwind v4 `@theme` blocks
> - Run `npx biome migrate` when upgrading between major versions

### 5. Configure Vitest
`vitest.config.ts`:
```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'node:path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test-setup.ts'],
  },
})
```

`src/test-setup.ts`:
```typescript
import '@testing-library/jest-dom/vitest'
```

> **Note:** Add `resolve.alias` for `@/*` paths to work in test files too, matching `tsconfig.json` paths.

### 6. Vite config (with Tailwind v4)
`vite.config.ts`:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'node:path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

> **Tailwind v4:** Uses `@tailwindcss/vite` plugin (NOT PostCSS like v3). Install with `npm install tailwindcss @tailwindcss/vite`. CSS uses `@import "tailwindcss"` instead of `@tailwind base/components/utilities`.

### 7. Vite env types
`src/vite-env.d.ts`:
```typescript
/// <reference types="vite/client" />
```

> **Required:** Without this, `import.meta.env` and CSS imports fail typecheck.

### 8. Package scripts
`package.json` scripts (replace defaults from Vite scaffold):
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "biome check src",
    "lint:fix": "biome check src --write",
    "typecheck": "tsc --noEmit",
    "test": "vitest",
    "test:run": "vitest run",
    "test:e2e": "playwright test",
    "preview": "vite preview"
  }
}
```

> **Note:** Vite scaffold generates `"lint": "oxlint"` — replace with Biome. Also remove `oxlint` from devDependencies if present.

### 9. Folder structure
Create:
```
src/
  components/   # reusable UI components
    ui/         # shadcn/ui components
  pages/        # route pages (one per route)
  lib/          # utilities, api clients, config
  hooks/        # custom hooks
  types/        # entity types with Zod schemas
  test/         # test utilities
```

### 10. Agent files
Create `AGENTS.md`:
```markdown
# AGENTS.md

> Instructions for AI agents working on this project.

## Stack
- Vite + React 19 + TypeScript estricto
- Biome (lint + format)
- Vitest (unit tests) + Playwright (e2e)
- Zod (runtime validation)
- [Additional: React Router, TanStack Query, Supabase, etc.]

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

## Conventions
- TypeScript estricto. No `any` unless absolutely necessary (with comment).
- Imports sorted alphabetically, grouped (external, internal, types).
- Components: PascalCase. Hooks: camelCase with `use` prefix. Utils: camelCase.
- Validation with Zod for all external input.
- Unit tests next to code: `*.test.ts`. E2E in `tests/e2e/`.
```

Create `HANDOFF.md`, `CHANGELOG.md`, `ROADMAP.md` (from web-app-builder phases).

### 11. OpenSpec
```bash
npx openspec init
```

### 12. CI (GitHub Actions)
`.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '24'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run test:run
      - run: npm run build
```

### 13. Trivial test (for verification gate)
`src/test/scaffold.test.ts`:
```typescript
import { describe, expect, it } from 'vitest'

describe('scaffold', () => {
  it('should have vitest configured', () => {
    expect(true).toBe(true)
  })
})
```

> **Required:** Without at least one test file, `vitest run` exits with code 1 and the verification gate fails.

### 14. Verify
```bash
npm run lint && npm run typecheck && npm run test:run && npm run build
```

All must pass. Fix any issues before proceeding.

## Common pitfalls (learned from real scaffolds)

| Problem | Cause | Fix |
|---|---|---|
| `TS5101: baseUrl deprecated` | TS 6+ deprecates `baseUrl` | Add `"ignoreDeprecations": "6.0"` to `tsconfig.json` |
| `TS2339: Property 'env' does not exist on 'ImportMeta'` | Missing Vite client types | Create `src/vite-env.d.ts` with `/// <reference types="vite/client" />` |
| `TS2882: Cannot find module for side-effect import of CSS` | Same as above — missing Vite types | Same fix |
| `Biome: unknown key 'organizeImports'` | Biome 2.x moved it to `assist.actions.source` | Use `"assist": { "actions": { "source": { "organizeImports": "on" } } }` |
| `Biome: 'recommended' deprecated` | Biome 2.x renamed to `preset` | Use `"linter": { "rules": { "preset": "recommended" } }` |
| `Biome: schema version mismatch` | Hardcoded schema URL doesn't match installed version | Use `npx biome --version` to get exact version, match schema URL |
| `Biome: Tailwind-specific syntax is disabled` | Tailwind v4 `@theme` blocks not recognized | Add `"css": { "parser": { "tailwindDirectives": true } }` to biome.json |
| `Biome: noNonNullAssertion on getElementById('root')!` | Biome 2.x flags non-null assertions | Use `const root = document.getElementById('root'); if (!root) throw new Error(...)` |
| `Vitest: no test files found, exit code 1` | Empty project has no tests | Add a trivial test in `src/test/scaffold.test.ts` |
| `Vite lint script is 'oxlint' not 'biome'` | Vite scaffold defaults to oxlint | Replace with `"lint": "biome check src"` in package.json |
| Path alias `@/*` doesn't work in tests | Vitest doesn't read tsconfig paths | Add `resolve.alias` in `vitest.config.ts` matching tsconfig paths |