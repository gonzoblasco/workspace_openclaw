# Dev skills: keep / merge / deprecate

## Decisión
- keep: 44 (all inventory items; no merges executed this session)
- merge candidates: 4 pairs (openspec vs openspec-pattern; performance-benchmark vs performance-optimization; hermes-* family overlap; idea-refine vs spec-driven-development)
- deprecated: 0 (nothing empty/dead; guard no delete unless empty)

## Anomalías (auditor)
- name missing: api-integration-test, chaos-engineering, code-metrics, compatibility-testing, dependency-advisor, performance-benchmark, threat-modeling (7)
- metadata missing: 37 skills
- Frontmatter gaps exceed 30 edits → parar y reportar (guardrail).

## 3 actionables (max)
1. Añadir `name`+`description`+`metadata` a frontmatter (DEV+AUDITOR, crit: 37 skills listos en <30 ediciones).
2. Consolidar pares openspec / performance (DEV, crit: un solo skill canónico por par).
3. Marcar hermes-openspec deprecado si docs/openspec lo reemplaza (DEV, crit: grep refs empty).

## Merge canonicity (tanda 2)
- Pair: openspec (canonical CLI usage) ← openspec-pattern (methodology/intent contract, references openspec). No deletion; cross-ref only.
