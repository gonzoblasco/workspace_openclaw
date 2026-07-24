# Biome Setup — Build Scaffold Reference

Configuración óptima de Biome para proyectos scaffolded.

## Initial Setup

```bash
# Install
npm install -D --save-exact @biomejs/biome

# Init (creates biome.json)
npx @biomejs/biome init
```

## Recommended Configuration

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": {
        "noUnusedVariables": "error",
        "useExhaustiveDependencies": "warn"
      },
      "style": {
        "noNonNullAssertion": "warn",
        "useConst": "error",
        "useTemplate": "error"
      },
      "suspicious": {
        "noExplicitAny": "warn",
        "noConsoleLog": "warn"
      },
      "a11y": {
        "noSvgWithoutTitle": "error",
        "useKeyWithClickEvents": "error",
        "useValidAriaProps": "error",
        "useValidAriaValues": "error",
        "useHeadingContent": "error",
        "useAltText": "error",
        "useAriaActivedescendantWithTabindex": "error",
        "useAriaPropsForRole": "error"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "semicolons": "always",
      "trailingCommas": "all"
    }
  }
}
```

## shadcn/ui Ignore

Agregar al `biome.json` para evitar falsos positivos de a11y en componentes de shadcn:

```json
{
  "files": {
    "ignore": ["src/components/ui/*"]
  }
}
```

## VS Code Integration

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "biomejs.biome",
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  },
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[javascript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[json]": {
    "editor.defaultFormatter": "biomejs.biome"
  }
}
```

## Pre-commit Hook

```bash
# Using simple-git-hooks
npx simple-git-hooks
```

```json
// package.json
{
  "simple-git-hooks": {
    "pre-commit": "npx biome check --write --no-errors-on-unmatched --files-ignore-unknown=true . && git add -A"
  }
}
```

## CI Check

```yaml
# .github/workflows/lint.yml
- name: Lint
  run: npx biome ci .
```

## Post-Scaffold Command

Siempre correr después de scaffoldear:

```bash
npx biome check --write .
```

Si no, el primer CI falla porque Biome lintea su propio `biome.json`.

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Stack Templates](./stack-templates.md) — Templates de stack
- [CI Templates](./ci-templates.md) — Templates de CI/CD
