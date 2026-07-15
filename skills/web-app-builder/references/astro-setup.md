# Astro Setup (Complete)

Use when stack decision is Astro (content-heavy, SEO critical, landing, portfolio, marketing).

## Steps

### 1. Scaffold
```bash
npm create astro@latest <project-name> -- --template minimal --no-install
cd <project-name>
npm install
```

### 2. Add React integration (for interactive islands)
```bash
npx astro add react --yes
```

### 3. Install dependencies
```bash
npm install -D @biomejs/biome vitest
npm install zod
# If Supabase:
npm install @supabase/supabase-js
# If UI components:
npm install tailwindcss @radix-ui/react-dialog lucide-react
```

### 4. Configure TypeScript
`tsconfig.json`:
```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "noUncheckedIndexedAccess": true,
    "jsx": "react-jsx",
    "react-jsx": "react"
  },
  "include": ["src", "tests"],
  "exclude": ["dist"]
}
```

### 5. Configure Biome
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

### 6. Configure Vitest
`vitest.config.ts`:
```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
  },
})
```

### 7. Package scripts
```json
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "lint": "biome check src",
    "lint:fix": "biome check src --write",
    "typecheck": "astro check && tsc --noEmit",
    "test": "vitest",
    "test:run": "vitest run"
  }
}
```

### 8. Folder structure
```
src/
  components/   # Astro + React components
  layouts/      # page layouts
  pages/        # routes (file-based)
  lib/          # utilities
  types/        # entity types
  styles/       # global CSS
```

### 9. Agent files
Create `AGENTS.md`, `HANDOFF.md`, `CHANGELOG.md`, `ROADMAP.md` (from web-app-builder phases).

### 10. OpenSpec
```bash
npx openspec init
```

### 11. CI (GitHub Actions)
Same pattern as Vite setup — lint, typecheck, test, build.

### 12. Verify
```bash
npm run lint && npm run typecheck && npm run test:run && npm run build
```

All must pass.