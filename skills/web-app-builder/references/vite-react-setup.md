# Vite + React Setup (Complete)

Use when stack decision is Vite + React (no SSR needed, app-style, internal tool, dashboard).

## Steps

### 1. Scaffold
```bash
npm create vite@latest <project-name> -- --template react-ts
cd <project-name>
```

### 2. Install dependencies
```bash
npm install
npm install -D @biomejs/biome vitest @testing-library/react @testing-library/jest-dom jsdom
npm install zod react-router-dom @tanstack/react-query
# If Supabase:
npm install @supabase/supabase-js
# If forms:
npm install react-hook-form @hookform/resolvers
# If charts:
npm install recharts
# If UI components:
npm install tailwindcss @radix-ui/react-dialog @radix-ui/react-dropdown-menu lucide-react
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
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
```

### 4. Configure Biome
`biome.json`:
```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": { "recommended": true }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  }
}
```

### 5. Configure Vitest
`vitest.config.ts`:
```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
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

### 6. Package scripts
`package.json` scripts:
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

### 7. Folder structure
Create:
```
src/
  components/   # reusable UI components
  pages/        # route pages (one per route)
  lib/          # utilities, api clients, config
  hooks/        # custom hooks
  types/        # entity types with Zod schemas
  test/         # test utilities
```

### 8. Agent files
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

### 9. OpenSpec
```bash
npx openspec init
```

### 10. CI (GitHub Actions)
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

### 11. Verify
```bash
npm run lint && npm run typecheck && npm run test:run && npm run build
```

All must pass. Fix any issues before proceeding.