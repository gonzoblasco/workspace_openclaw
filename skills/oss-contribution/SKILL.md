---
name: "oss-contribution"
description: "Workflow de OSS Contribution: contribución estratégica a repos externos. Reemplaza oss-contribute, sdd-brownfield."
---

# Workflow: OSS Contribution

## Skills que reemplaza
- `oss-contribute`
- `sdd-brownfield`

## Qué hace
Contribución estratégica a repositorios externos con Spec-Driven Development.

## Fases
1. **Pipeline** — selección de repos objetivo, tier ranking
2. **Triaje** — buscar issues sin PRs competidores, evaluar impacto
3. **Análisis** — entender el bug/feature, root cause analysis. Usar el análisis del reporter de issues. Complex issue ≠ complex fix. Revisar si el reporter ya identificó la causa raíz
4. **Implementación** — fork, branch, fix, tests, OpenSpec as-built/delta
5. **PR** — commit firmado SSH, descripción clara y humana (no generada). En repos Tier 0 (shadcn/ui, TanStack, Vercel): evitar trazas de automatización en commits y descripciones. Descripción humana, no generada
6. **Community** — comentar en issues relacionados, cross-referencing. Hacerlo después del PR, no antes, para evitar ruido si el PR no prospera
7. **Batch** — status check de PRs abiertos (🟢⚠️🔴)

## Outputs
- PRs a repos externos
- OpenSpec specs as-built o delta
- Reporte de estado de PRs abiertos
