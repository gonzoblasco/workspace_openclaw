# Testing Setup for Accessibility

Configuración de herramientas de auditoría y testing de accesibilidad.

## Automated Tools

### axe-core (recomendado)

```bash
# CLI
npx @axe-core/cli https://example.com --exit

# En tests con Playwright
npm install -D @axe-core/playwright
```

```typescript
// playwright.config.ts
import { AxeBuilder } from '@axe-core/playwright';

test('should not have a11y violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

### Lighthouse CI

```bash
# Instalar
npm install -D @lhci/cli

# Configurar
npx lhci autorun --collect.url=https://example.com
```

```json
// .lighthouserc.json
{
  "ci": {
    "collect": {
      "numberOfRuns": 3,
      "settings": {
        "onlyCategories": ["accessibility"]
      }
    },
    "assert": {
      "assertions": {
        "categories:accessibility": ["error", { "minScore": 0.9 }]
      }
    }
  }
}
```

### WAVE CLI

```bash
npx wave-cli https://example.com --output report.json
```

## Manual Testing

### Keyboard Navigation Checklist

- [ ] Tab through all interactive elements
- [ ] Focus visible at all times
- [ ] No keyboard traps
- [ ] Skip link visible on first Tab
- [ ] Custom widgets follow ARIA keyboard patterns
- [ ] Focus order matches visual order

### Screen Reader Testing

**VoiceOver (macOS):** `Cmd + F5` to enable
- [ ] All content is announced
- [ ] Landmarks are identified
- [ ] Images have alt text
- [ ] Forms have labels
- [ ] Dynamic content is announced (aria-live)
- [ ] Custom widgets announce state changes

**NVDA (Windows):** Free, open source
- [ ] Same checks as VoiceOver

**JAWS (Windows):** Most common in enterprise
- [ ] Same checks as VoiceOver

## CI Integration

### GitHub Actions

```yaml
# .github/workflows/a11y.yml
name: Accessibility
on: [pull_request]
jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - name: Run axe-core
        run: npx @axe-core/cli http://localhost:3000 --exit
      - name: Run Lighthouse CI
        run: npx lhci autorun
```

## Playwright A11y Test Patterns

```typescript
// tests/a11y/navigation.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Keyboard navigation', () => {
  test('skip link is first focusable element', async ({ page }) => {
    await page.goto('/');
    await page.keyboard.press('Tab');
    const focused = page.locator(':focus');
    await expect(focused).toHaveAttribute('href', '#main-content');
  });

  test('all interactive elements are reachable', async ({ page }) => {
    await page.goto('/');
    const interactive = page.locator(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const count = await interactive.count();
    for (let i = 0; i < count; i++) {
      await page.keyboard.press('Tab');
      await expect(page.locator(':focus')).toBeVisible();
    }
  });
});
```

## Tools Comparison

| Tool | Type | Coverage | CI Ready | Cost |
|---|---|---|---|---|
| axe-core | Library/Rules engine | ~57 rules | ✅ | Free |
| Lighthouse | Audit tool | ~20 a11y audits | ✅ | Free |
| WAVE | Browser extension/API | Visual overlay | ⚠️ Limited | Free |
| Pa11y | CLI | axe-core based | ✅ | Free |
| Accessibility Insights | Extension | FastPass + Assessment | ⚠️ Limited | Free |
| Deque Axe DevTools | Extension + API | Full WCAG | ✅ | Paid |

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [WCAG 2.2 Criteria](./wcag-22-criteria.md) — Catálogo de criterios
- [ARIA Patterns](./aria-patterns.md) — Patrones WAI-APG
