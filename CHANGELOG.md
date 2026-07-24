# CHANGELOG.md

## [2026-07-23] — Skills Workspace Overhaul: 20 → 33 Skills

### Added
- **11 new skills** from external sources:
  - `cv-tailor` — Optimización de CV con STAR y ATS
  - `adhd-assistant` — Gestión ADHD-friendly de vida diaria
  - `copy-editing` — 7 sweeps de edición de copy de marketing
  - `saas-metrics-coach` — Métricas SaaS con scripts calculadores
  - `timeline-builder` — Timelines HTML interactivos desde JSON
  - `campaign-plan` — Briefs completos de campaña de marketing
  - `support-response-writer` — Customer support con de-escalación
  - `brand-name-forge` — 8 métodos de naming de marca
  - `code-mentor` — Tutor de programación (8 modos de enseñanza)
  - `mock-interview-drill` — Simulacros de entrevistas con STAR
  - `dev-guide-generator` — Tutoriales técnicos completos
- **2 new skills** from partial-overlap integration:
  - `i18n-expert` — Internacionalización y localización
  - `sql-insight` — SQL, optimización y EXPLAIN

### Enriched
- **All 20 original skills** now have `references/` and `scripts/` directories
- **44 reference files** created across all skills (WCAG criteria, runbooks, ADR patterns, etc.)
- **49 scripts** created (shell + Python) for automation
- **33 README.md** files added — one per skill with purpose, usage, examples

### Integrated
- `Code to Diagram` → `tech-docs/scripts/analyze_codebase.py`
- `Ubiquitous Language` → `product-discovery/references/ubiquitous-language.md`
- `OWASP Top 10` → `review-quality/references/owasp-top-10.md`
- `Repo Audit` → `engineering-governance/scripts/` (hotfiles, ownership, secret-scan)
- `Log Error Digest` → `debug-investigation/scripts/analyze_logs.py`
- `Story Map Builder` → `product-discovery/scripts/generate_story_map.py`

### Changed
- Workspace skills count: 20 → 33
- Skills mirror synced to `.github/skills/`

### Next Steps
1. Test scripts in real scenarios (sql_query_helper, analyze_logs, generate_timeline)
2. Iterate on skills with 🟡 warnings (no references/scripts)
3. Use `cv-tailor` + `mock-interview-drill` for job search
4. Establish CHANGELOG update as session closure ritual
