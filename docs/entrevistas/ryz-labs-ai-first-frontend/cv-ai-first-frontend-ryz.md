# Gonzalo Blasco

**Senior Frontend Engineer - AI-Native Product Engineering**

Núñez, Buenos Aires, Argentina | Remote LATAM (aligned to US EST) | +54 11 4937 4656 | gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco

## Professional Summary

Frontend engineer with 10+ years building production web applications, and the last 1.5 years building AI-native products. React and TypeScript are the main stack, with design systems and accessibility treated as quality bars rather than polish. AI coding tools (Claude Code, Codex, and a personal agent stack) are part of the daily workflow, not an experiment: the AI Engineering OS I built runs on a strict quarantine → analyze → verify → adopt method, so generated code is audited before it lands. 11 merged pull requests in production component libraries. I review components in Storybook before implementation, prototype quickly, and ship.

## Core Skills

- **Frontend:** React, TypeScript, JavaScript, Vite, Next.js, HTML5, CSS3, Tailwind, Storybook, component architecture, design systems, design tokens, responsive layouts.
- **AI-augmented development:** AI coding agents in the daily loop (Claude Code, Codex), agent orchestration, prompt and context design, evaluating where AI tooling accelerates and where it silently breaks.
- **Accessibility (differential):** WCAG 2.2 AA, ARIA patterns (role, state and property wiring), screen readers (JAWS, NVDA, VoiceOver, TalkBack), Axe DevTools, Lighthouse, automated accessibility gating in CI.
- **Backend and data:** Node.js, REST APIs, Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions), pgvector, Stripe billing, webhooks.
- **Quality and delivery:** Vitest, Playwright, Biome, Zod, CI/CD pipelines, Git/GitHub, Jira, agile SDLC, code review, developer guidance.

## Professional Experience

### Freelancer - Software Engineer
*05/2025 - Present | Remote*

- Built **SoporteML**, an AI-powered multi-tenant CRM for Mercado Libre sellers: React + Vite + TypeScript frontend, Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions) backend, RAG-based reply suggestions with pgvector, Autopilot with confidence guardrails, multi-company and team roles, and webhook-driven Stripe billing. Shipped the first production client, **Pro Motors** (pro-motors.com.ar), with a live Mercado Libre integration.
- Built an **AI Engineering OS** on OpenClaw: per-project sessions, persistent memory, handoffs, subagents, reusable skills, and a pipeline for open source contributions. Its working method is quarantine → analyze → verify → adopt: nothing from outside enters the codebase without being read, analyzed and verified first.
- Own products end to end, from ambiguous problem to shipped and billed: product decisions, implementation, tests and production deployment.

### EY (Ernst & Young) - Senior Frontend Engineer, Accessibility Lead
*09/2021 - 05/2025 | Hybrid*

- Led accessibility for **EY Motif**, an enterprise React component library consumed across client and internal products: remediated **50+ components** to WCAG 2.2 AA (keyboard navigation, screen reader support, focus management, contrast) with Axe DevTools, Lighthouse, JAWS and NVDA.
- Served as the team's accessibility reference across projects: reviewed Storybook components **before** implementation, defined component-level standards and annotations, and wrote technical accessibility requirements with code guidance for UI stories.
- Prioritized accessibility defects by WCAG impact in Jira, with remediation guidance to developers inside the sprint.
- Led a team of 3 engineers building an AI-powered financial intelligence platform in Next.js, with accessible interfaces from architecture to production.
- Worked in a matrixed, cross-regional team (US / India) across multiple SDLC phases in parallel within agile squads.

### Super7UI - Accessibility Engineer (Contractor)
*08/2020 - 05/2021 | Remote*

- Led the frontend audit and remediation for **Warner Bros. Screeners (WBTVD)**, the private streaming platform global distributors use to review content.
- Validated and expanded a prior third-party audit by reproducing each reported issue across **NVDA, VoiceOver and TalkBack**, and used Axe to identify and document WCAG violations in the key flows.
- Resolved **200+ WCAG violations** and produced developer-ready remediation documentation: proposed solutions, implementation guidance, and development-ready specifications.
- Established an accessibility testing pipeline with **axe-core + Playwright integrated into CI/CD**, so non-compliant code could not merge.

### Minutentag - Frontend Developer, Accessibility Owner
*02/2016 - 11/2019 | Hybrid*

- Contributed to migrating legacy interfaces to React and HTML5 on a platform serving **2M+ monthly active users**, and maintained the e-commerce flows (checkout, cart) for Ann Taylor, LOFT and Lou & Grey.
- Grew from junior to the team's accessibility owner.
- Ran **A/B experiments in production with Adobe Target** against live user segments on features and designs, inside agile squads alongside design and product, implementing the variants as JavaScript snippets.

## Open Source - Merged Pull Requests

Merged fixes in production component libraries and design systems, each reviewed and shipped by maintainers.

- **adobe/react-spectrum #10503** - Gated the ComboBox live-region announcement to section changes; it was overwriting the native per-item VoiceOver announcement.
- **adobe/react-spectrum #10554** - Added a regression test for global `aria-posinset` across sections.
- **carbon-design-system/carbon #22887** - Added explicit `aria-describedby` support to `ComposedModal`, across both the native `<dialog>` path and the `div[role=dialog]` path.
- **carbon-design-system/ibm-products #9878** - `CreateFullPage` (issue #9864).
- **carbon-design-system/ibm-products #9879** - Datagrid (issue #9839).
- **facebook/astryx #4605** - Added a non-chromatic indicator (font weight) to the current breadcrumb item; WCAG 1.4.1.
- **facebook/astryx #4914** - `build-storybook` failed with "no merge base" on old PRs (fetch depth); fallback to a two-point diff.
- **facebook/astryx #5419** - HoverCard with a label was exposed as a dialog popup: `aria-haspopup=dialog` + `aria-controls` gated on open, with `aria-expanded` synchronized.
- **facebook/astryx #5493** - `TreeList` now forwards `aria-label`/`aria-labelledby` to the underlying `ul role=tree`; a tree without a header could not be named.
- **mui/base-ui #5551** - Moved `aria-orientation` to the owners of the role; the grid role does not support it.
- **mui/material-ui #49003** - Kept carousel links in hidden slides out of the focus order; WCAG 4.1.2 `aria-hidden-focus`.

## Education and Certifications

- **Deque University - Accessibility Specialist Program (2021)**
- **Digital House - React (2018)**

## Languages

- Spanish - native
- English - B2 (professional working proficiency; reading and writing are comfortable, spoken English is my current development area)

## Keyword map

| JD requirement | Where it is covered |
|---|---|
| Modern frontend (React, TypeScript) | Professional Summary, Core Skills, every role |
| AI coding tools in the daily workflow | Professional Summary, Freelancer (AI Engineering OS) |
| AI-native products | Freelancer (SoporteML, Pro Motors) |
| UI polish and user experience | Professional Summary, EY design review before implementation |
| Design systems and component libraries | EY Motif, the 11 merged PRs |
| Design review | EY (reviewed components in Storybook before implementation) |
| Rapid prototyping | Freelancer (prototype to shipped product) |
| UI polish and eye for detail | EY design review; PRs with ARIA-level detail |
| Startups, fast-moving teams | Freelancer: own product, first client, full cycle |
| Accessibility as a quality bar | Super7UI, EY, the OSS fixes |
