# Skills Changelog

Registro de cambios en skills del workspace. Cada entrada marca cuándo se creó, modificó, fusionó o eliminó una skill.

---

## [2026-08-03] — Nuevo skill pipeline-detector

### Added
- **pipeline-detector** — Build detection pipelines combining deterministic local rules with contextual AI analysis. Extraído del patrón "detectores locales + validación cruzada / IA contextual" del AI Engineering Bootcamp (apareció 5 veces: N3, N5, N6, N8, N9). Incluye `references/detector-templates.md` con templates reutilizables (secrets, SQL injection, XSS, style, vuln versions, diff analysis, CloudFormation, report markdown).

---

## [2026-07-25] — Refactor AGENTS.md: metodología movida a skills

### Modified
- **knowledge-management** — Added: Learning Signals, Conflict Resolution, Common Traps, DREAMS.md
- **session-lifecycle** — Added: Self-Reflection, WAL Protocol, Working Buffer, Compaction Recovery, Handoff entre Subagentes, Productividad & ADHD
- **review-quality** — Added: Confidence Tagging
- **debug-investigation** — Added: Relentless Resourcefulness, Structured Escalation
- **task-execution** — Added: Verify Implementation
- **engineering-governance** — Added: Growth Loops, Evaluación de Skills Externas

---

## [2026-07-25] — Nueva skill: github

### Added
- **github** — Comandos de `gh`, regla del guión común, referencia a gh-issue-planner

---

## [2026-07-23] — Skills Workspace Overhaul: 20 → 33 Skills

### Added
- **11 new skills** from external sources:
  - `cv-tailor`, `adhd-assistant`, `copy-editing`, `saas-metrics-coach`, `timeline-builder`
  - `campaign-plan`, `support-response-writer`, `brand-name-forge`, `code-mentor`
  - `mock-interview-drill`, `dev-guide-generator`
- **2 new skills** from partial-overlap integration:
  - `i18n-expert`, `sql-insight`

### Enriched
- All 20 original skills now have `references/` and `scripts/` directories
- 44 reference files, 49 scripts created
- 33 README.md files added

### Integrated
- Code to Diagram → `tech-docs`
- Ubiquitous Language → `product-discovery`
- OWASP Top 10 → `review-quality`
- Repo Audit → `engineering-governance`
- Log Error Digest → `debug-investigation`
- Story Map Builder → `product-discovery`
