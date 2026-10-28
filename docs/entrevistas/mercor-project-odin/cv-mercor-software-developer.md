# Gonzalo Blasco

**Senior Software Engineer (10+ years)** | Remote LATAM (aligned to US EST) | +54 11 4937 4656 | gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco


## Professional Summary

Software engineer with **10+ years** of end-to-end production experience, working daily on macOS with VS Code, Terminal, Git, npm/pnpm/bun, Docker, and CI in GitHub Actions. Proficient in JavaScript, TypeScript, React, and Next.js. Explains the reasoning behind each decision, through code review, in-sprint developer guidance, and written specs. Shipped AI-native products and accessibility fixes with WCAG 2.2 AA as a system criterion rather than a final check. 11 merged pull requests in production component libraries.


## Core Skills

- **Languages & Frameworks:** JavaScript, TypeScript, React, Next.js, Vite, HTML5, CSS3, Tailwind CSS
- **Developer Tools:** VS Code, Terminal, Git, npm/pnpm/bun, Docker, CI/CD pipelines (GitHub Actions, Playwright, and Vitest)
- **AI-augmented workflow:** Claude Code, Codex, OpenClaw AI-Engineering OS (quarantine -> analyze -> verify -> adopt)
- **Accessibility (quality bar):** WCAG 2.2 AA, ARIA patterns, screen-reader testing (NVDA, VoiceOver, JAWS), Axe DevTools, Lighthouse
- **Backend & Data:** Node.js, Supabase (PostgreSQL, Auth, RLS, Edge Functions), pgvector, Stripe billing integration
- **Open-source contribution:** 11 merged PRs in major component libraries (React Spectrum, Carbon, MUI, Facebook astryx)


## Professional Experience

### Freelancer - Software Engineer
*05/2025 - Present | Remote*
- Built **SoporteML**, an AI-powered multi-tenant CRM for Mercado Libre sellers (React + Vite + TypeScript front-end; Supabase back-end; RAG-based reply suggestions with pgvector; Stripe billing). Delivered the first production client **Pro Motors**.
- Designed SoporteML's design system: semantic tokens (color, type, spacing, radius, shadows, focus ring), a token-to-component map, and WCAG AA rules applied at the system level.
- Created **AI Engineering OS** on OpenClaw: per-project sessions, persistent memory, sub-agents, skill orchestration, and a strict quarantine -> analyze -> verify -> adopt pipeline for all external code.
- Day-to-day environment: macOS on Apple Silicon, VS Code, Terminal (zsh), Git, and npm/pnpm/bun across all projects; CI on GitHub Actions.
- End-to-end product ownership: problem framing, implementation, testing, and production deployment.

### EY (Ernst & Young) - Senior Frontend Engineer, Accessibility Lead
*09/2021-05/2025 | Hybrid*
- Led accessibility for **EY Motif**, an enterprise React component library; remediated **50+ components** to WCAG 2.2 AA using Axe, Lighthouse, JAWS, and NVDA.
- Reviewed components in Storybook before implementation, defined component-level accessibility standards, and authored technical requirements with code examples.
- Coached developers inside their branches and guided remediation in-sprint, explaining what the WCAG failure was and why the fix worked, with code examples against the component in Storybook.
- Led a team of 3 engineers building an AI-powered financial intelligence platform in Next.js, from accessible interfaces to production.

### Super7UI - Accessibility Engineer (Contractor)
*08/2020 - 05/2021 | Remote*
- Audited and remediated **Warner Bros. Screeners** streaming platform, fixing **200+ WCAG violations** across NVDA, VoiceOver, and TalkBack. Validated and expanded a prior third-party audit (Applause) by reproducing each issue in NVDA, VoiceOver, and TalkBack. Produced developer-ready remediation documentation (proposed solutions, implementation guidance, and specifications) and established an axe-core + Playwright testing pipeline in CI/CD.

### Minutentag - Frontend Developer, Accessibility Owner
*02/2016 - 11/2019 | Hybrid*
- Migrated legacy e-commerce sites (Ann Taylor, LOFT, Lou & Grey) to React, supporting **2M+ monthly active users**.
- Reviewed components in Storybook (React) and wrote technical accessibility requirements; grew from junior to team accessibility reference.
- Ran **A/B experiments in production** with Adobe Target, implementing variant code as JavaScript snippets.


## Open Source - Merged Pull Requests

Eleven merged PRs in production component libraries, each reviewed and shipped by maintainers. These are fixes to someone else's code, not greenfield work.

- **adobe/react-spectrum** #10503 - Gated the ComboBox live-region announcement to section changes; it was overwriting VoiceOver's native per-item announcement.
- **adobe/react-spectrum** #10554 - Regression test (test-only) for `aria-posinset` across sections.
- **carbon-design-system/carbon** #22887 - Added explicit `aria-describedby` support to `ComposedModal`, on both the native `<dialog>` and the `div[role="dialog"]` path.
- **carbon-design-system/ibm-products** #9878 - Implemented `CreateFullPage` (issue #9864).
- **carbon-design-system/ibm-products** #9879 - Fixed Datagrid (issue #9839).
- **facebook/astryx** #4605 - Added a non-chromatic indicator (font-weight) to the current breadcrumb item; color alone was the only cue (WCAG 1.4.1).
- **facebook/astryx** #4914 - Fixed `build-storybook` "no merge base" failures on old PRs (shallow clone); fallback to a two-point diff.
- **facebook/astryx** #5419 - Fixed HoverCard with a label exposing as a dialog popup: `aria-haspopup=dialog`, `aria-controls` gated on open, `aria-expanded` kept in sync.
- **facebook/astryx** #5493 - Forwarded `aria-label`/`aria-labelledby` to the underlying `ul[role="tree"]`; a tree without a header could not be named.
- **mui/base-ui** #5551 - Moved `aria-orientation` to the role owners; the grid role does not support it.
- **mui/material-ui** #49003 - Kept carousel links in hidden slides out of the focus order (WCAG 4.1.2).


## Education

- **Universidad de Palermo - Ingenieria en Informatica / Computer Science Engineering (2001-2002, incomplete)**
- **Digital House - React (2018)**
- **Universidad Argentina de la Empresa - Graphic Design (2003-2004, incomplete)**


## Certifications

- **Deque University - Accessibility Specialist Program (2021)**


## Languages

- Spanish - native
- English - B2+ (professional working proficiency). Reading and writing are comfortable: I write technical requirements, PR descriptions, and specs in English daily. Spoken English is my current development area, and I am in an intensive B2+ course.


## Keyword map

| JD Requirement | Coverage |
|---|---|
| macOS development workstation | Mention of macOS workflow throughout; tools are macOS-native (Terminal, VS Code) |
| JavaScript / TypeScript | Core Skills, all roles |
| AI-native product engineering | Freelancer (SoporteML, AI Engineering OS) |
| Design systems & component libraries | EY Motif, 11 merged PRs |
| Explain reasoning while working | Professional Summary & each role highlight developer guidance, PR descriptions, ADRs |
| Remote LATAM aligned to US EST | Profile line |
| 10+ years experience | Headline and facts |
| B2+ English | Languages section |
| Bachelor's degree required | Not met - education marked `(incomplete)`. Satisfied through the experience branch: 10+ years of hands-on software engineering vs. the 2-3 years the JD asks for. |


## Notes / gaps

- **Degree:** No completed university degree; all studies are marked `(incomplete)` as required.
- **Verbal communication:** English speaking level is B2+; oral proficiency is currently being improved via an intensive B2+ course (CUI, Buenos Aires).
- **Hardware:** Owns a MacBook with Apple Silicon (M4) running macOS 27.2 - meets hardware requirement.

