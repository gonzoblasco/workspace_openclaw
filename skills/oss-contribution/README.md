# OSS Contribution

Contribución estratégica a open source.

## ¿Para qué sirve?

Para **contribuir a repositorios open source** de forma estratégica. Incluye triaje de issues para encontrar oportunidades, implementación con Spec-Driven Development, PRs con descripción humana, y seguimiento batch de PRs abiertos.

## ¿Cuándo usarlo?

- Cuando querés contribuir a shadcn/ui, TanStack, Vercel, Biome, Supabase
- Cuando querés hacer triaje de issues para encontrar oportunidades
- Cuando necesitás dar seguimiento a PRs abiertos

## ¿Cómo se usa?

### Workflow completo

1. **Pipeline** — selección de repos objetivo, tier ranking
2. **Triaje** — buscar issues sin PRs competidores
3. **Análisis** — entender el bug/feature, root cause
4. **Implementación** — fork, branch, fix, tests, OpenSpec
5. **PR** — commit firmado SSH, descripción humana (no generada)
6. **Community** — comentar en issues relacionados, cross-referencing
7. **Batch** — status check de PRs abiertos

### Scripts útiles

```bash
# Ver estado de PRs abiertos
./scripts/pr-status-check.sh --author gonzoblasco

# Buscar issues sin PR en un repo
./scripts/triage-issues.sh shadcn-ui/ui --label "bug"

# Setup de fork para contribuir
./scripts/setup-fork.sh tanstack/query
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/tier-ranking.md` | Tier 0/1/2 con estrategia por nivel |
| `references/pr-checklist.md` | Checklist pre/post PR, tone por tier |
| `references/community-guidelines.md` | Bots vs humanos, cuándo no intervenir |

## Skills relacionadas

- [Review & Quality](../review-quality) — Para revisar PRs antes de enviar
- [Technical Documentation](../tech-docs) — Para documentar contribuciones
