# ADR-036: Turborepo Pnpm Monorepo

**Status:** Accepted
**Fecha:** 2026-08-05
**Origen:** react-18-design-patterns
**Source:** React 18 Design Patterns - Chapter 14 (MonoRepo Architecture)
**Scope:** Global - aplica a cualquier proyecto con multiples paquetes

## Context

El libro implementa un monorepo con:
- NPM Workspaces para gestion de paquetes
- `npm-run-all` para ejecutar scripts en paralelo
- Webpack 5 manual con presets separados (common, development, production)
- ESLint + Prettier para linting/formateo
- `ts-node` + `ts-node-dev` para ejecutar TypeScript

Esta configuracion requiere ~500 lineas de configuracion solo para Webpack, mas configuraciones de ESLint, Prettier, Babel, y TypeScript.

## Decision

Usar **Turborepo + pnpm** como estandar para monorepos en 2026.

### Configuracion minima

```json
// package.json (raiz)
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "lint": "biome check .",
    "format": "biome format --write ."
  },
  "devDependencies": {
    "turbo": "^2",
    "@biomejs/biome": "^1.9",
    "typescript": "^5"
  }
}
```

```yaml
# turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {},
    "typecheck": {
      "dependsOn": ["^build"]
    }
  }
}
```

```yaml
# pnpm-workspace.yaml
packages:
  - "packages/*"
```

### Estructura

```
my-monorepo/
├── packages/
│   ├── api/          # @my/api - Vite + Drizzle
│   ├── frontend/     # @my/frontend - Next.js App Router
│   ├── ui/           # @my/ui - Tailwind + React
│   └── utils/        # @my/utils - tsup
├── turbo.json
├── pnpm-workspace.yaml
├── biome.json
└── package.json
```

## Rationale

1. **Turborepo:** caching inteligente, ejecucion paralela, dependencias entre paquetes, zero-config
2. **pnpm:** mas rapido que npm, eficiente en disco (hard links), estrictos (solo dependencias declaradas)
3. **Biome:** reemplaza ESLint + Prettier, un solo binario
4. **Vite/tsup:** reemplazan Webpack 5 manual, zero-config para cada paquete
5. **Menos configuracion:** ~50 lineas vs ~500 del libro

## Consequences

- Proyectos nuevos con monorepo usan Turborepo + pnpm
- Migracion desde npm workspaces requiere cambiar package manager y agregar turbo.json
- Cada paquete puede usar su propio build tool (Vite, tsup, Next.js)
- Biome unifica linting y formateo en todos los paquetes

## Referencias

- Turborepo: https://turbo.build/repo
- pnpm workspaces: https://pnpm.io/workspaces
- Biome: https://biomejs.dev
- Vite: https://vitejs.dev
- tsup: https://tsup.egoist.dev
