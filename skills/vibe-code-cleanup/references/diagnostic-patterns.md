# Diagnostic Patterns — Vibe Code Cleanup Reference

Patrones comunes de deuda técnica en código generado por IA.

## Red Flags

| Pattern | Severity | Fix |
|---|---|---|
| `any` types everywhere | 🔴 High | Replace with explicit types |
| Functions > 150 lines | 🔴 High | Extract into sub-functions |
| Hardcoded secrets | 🔴 High | Move to env vars |
| Duplicated code blocks | 🟡 Medium | Extract to shared helper |
| No error handling | 🟡 Medium | Add try/catch or Result type |
| Commented-out code | 🟡 Medium | Remove or uncomment |
| Magic numbers/strings | 🟡 Medium | Extract to constants |
| Inline styles | 🟡 Medium | Move to CSS/Tailwind |
| No loading states | 🟡 Medium | Add Suspense/loading |
| Console.log debugging | 🟢 Low | Remove |

## Quick Scan (60 seconds)

```bash
# Count files and lines
find . -name "*.ts" -o -name "*.tsx" | wc -l
find . -name "*.ts" -o -name "*.tsx" | xargs wc -l | tail -1

# Find red flags
grep -r "any" --include="*.ts" --include="*.tsx" | wc -l
grep -r "console\.log" --include="*.ts" --include="*.tsx" | wc -l
grep -r "TODO\|FIXME" --include="*.ts" --include="*.tsx" | wc -l
grep -r "password\|secret\|api_key" --include="*.ts" --include="*.tsx" | wc -l
```

## Refactoring Order

1. **Safety first:** Remove secrets, add error handling
2. **Structure:** Extract long functions, remove dead code
3. **Types:** Replace `any`, add interfaces
4. **Consistency:** Standardize patterns, naming
5. **Polish:** Comments, docs, edge cases

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Cleanup Checklist](./cleanup-checklist.md) — Checklist de limpieza
