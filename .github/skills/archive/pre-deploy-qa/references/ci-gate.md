# CI Gate Scripts — Pre-Deploy QA Reference

Scripts para integrar QA checks en pipelines CI/CD.

## GitHub Actions Gate

```yaml
# .github/workflows/pre-deploy.yml
name: Pre-Deploy QA
on:
  push:
    branches: [main]

jobs:
  qa-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - run: npx tsc --noEmit
      - run: npm test -- --run
      - run: npx @biomejs/biome ci .
      - run: npx lighthouse-ci https://staging.example.com
      - run: npm audit --audit-level=high
```

## Smoke Test Script

```bash
#!/usr/bin/env bash
# smoke-test.sh — Quick smoke tests after deploy
URL="${1:?Usage: $0 <url>}"

echo "🔍 Running smoke tests on $URL"

# Health check
curl -sf "$URL/health" > /dev/null && echo "✅ Health OK" || echo "❌ Health FAIL"

# Homepage
curl -sf "$URL" > /dev/null && echo "✅ Homepage OK" || echo "❌ Homepage FAIL"

# Auth
curl -sf "$URL/api/auth/session" > /dev/null && echo "✅ Auth OK" || echo "❌ Auth FAIL"

# Sitemap
curl -sf "$URL/sitemap.xml" > /dev/null && echo "✅ Sitemap OK" || echo "❌ Sitemap FAIL"

echo "Smoke tests complete"
```

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [QA Checklist](./qa-checklist.md) — Checklist detallada
