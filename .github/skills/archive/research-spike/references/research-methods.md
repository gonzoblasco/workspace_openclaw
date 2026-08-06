# Research Methods — Research Spike Reference

Métodos de investigación para spikes técnicos.

## Information Gathering

### Primary Sources (prefer these)
- Official documentation
- Source code / GitHub
- RFCs and specs
- Author blog posts
- Conference talks

### Secondary Sources
- Blog posts and tutorials
- Stack Overflow
- Reddit / Hacker News
- YouTube videos

### Evaluation Criteria
- **Authority:** Is the source official or from a recognized expert?
- **Date:** Is it current? (check publish date)
- **Relevance:** Does it address our specific question?
- **Depth:** Does it cover edge cases and trade-offs?

## Experiment Design

### A/B Comparison

```bash
# Compare two approaches
# Approach A
time node -e "approachA()"
# Approach B
time node -e "approachB()"
```

### Prototype Checklist

- [ ] Minimal: only what's needed to answer the question
- [ ] Throwaway: not intended for production
- [ ] Documented: what was tested, what was learned
- [ ] Reproducible: someone else can run it

## Decision Framework

| Criterion | Weight | Option A | Option B |
|---|---|---|---|
| Performance | 30% | 8/10 | 6/10 |
| Maintainability | 25% | 7/10 | 8/10 |
| Learning curve | 20% | 6/10 | 9/10 |
| Ecosystem | 15% | 9/10 | 5/10 |
| Cost | 10% | 7/10 | 8/10 |
| **Weighted score** | **100%** | **7.35** | **7.15** |

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Spike Template](../references/template.md) — Template de reporte
- [Research Sources](../references/sources.md) — Fuentes de investigación
