# Migration Patterns — Dependency Management Reference

Patrones de migración para breaking changes en dependencias.

## Codemods

Muchas librerías proveen codemods para migración automática:

```bash
# React
npx react-codemod rename-unsafe-lifecycles

# Next.js
npx @next/codemod@latest new-link

# Material UI
npx @mui/codemod v5.0.0/preset-safe

# Jest
npx jest-codemods
```

## Deprecation Warnings

```bash
# Check for deprecation warnings at runtime
NODE_OPTIONS="--trace-warnings" node server.js

# Or check in logs
grep -r "deprecated" node_modules/$(dep-name)/*.js 2>/dev/null | head -20
```

## Dual Publish (ESM + CJS)

When migrating a library to ESM while maintaining CJS compatibility:

```json
{
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs"
    }
  }
}
```

## Breaking Change Detection

```bash
# Compare types between versions
npm install dep@old --no-save
npx tsc --noEmit 2>&1 | head -20

npm install dep@new --no-save
npx tsc --noEmit 2>&1 | head -20

# Use npm diff
npm diff dep@old..dep@new
```

## Rollback Plan Template

```markdown
## Rollback Plan

1. Revert package.json changes
2. Delete node_modules
3. Reinstall: npm ci
4. Verify: npm run build && npm run test
5. If CI fails, revert the revert commit
```

## Migration Checklist

- [ ] Read changelog/release notes
- [ ] Check for codemods
- [ ] Run type check before and after
- [ ] Run full test suite
- [ ] Check bundle size impact
- [ ] Verify in staging
- [ ] Document in CHANGELOG
- [ ] Update ADR if architecture changes

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Health Assessment](../references/health-assessment.md) — Evaluación de salud
- [Risk Analysis](../references/risk-analysis.md) — Análisis de riesgo
