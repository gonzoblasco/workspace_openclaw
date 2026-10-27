# Gonzalo Blasco

**Senior Software Engineer - Growth & Engagement**

Núñez, Buenos Aires, Argentina | Remote LATAM (aligned to US EST) | +54 11 4937 4656 | gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco

## Professional Summary

Software engineer with 10+ years building production software and the last 1.5 years shipping AI-native products. I have run experiments in production: at Minutentag I ran A/B experiments with Adobe Target against live user segments; today I own product, implementation, tests, billing and client support for products I ship. Strong in React and TypeScript, with design systems, accessibility and AI-assisted delivery as quality bars. 11 merged pull requests in production component libraries.

## Core Skills

- **Frontend:** React, TypeScript, JavaScript, Vite, Next.js, HTML5, CSS3, Tailwind, Storybook, component architecture, design systems, responsive layouts.
- **Experimentation:** A/B testing in production (Adobe Target), variant implementation as client-side JavaScript.
- **AI-augmented development:** AI coding agents in the daily loop (Claude Code, Codex), agent orchestration, evaluating where AI tooling accelerates and where it silently breaks.
- **Backend and data:** Node.js, REST APIs, Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions), pgvector, Stripe billing, webhooks.
- **Quality and delivery:** Vitest, Playwright, Biome, Zod, CI/CD pipelines, Git/GitHub, Jira, agile SDLC, code review, developer guidance.
- **Accessibility (differential):** WCAG 2.2 AA, ARIA patterns (role, state and property wiring), screen readers (JAWS, NVDA, VoiceOver, TalkBack), Axe DevTools, Lighthouse.

## Professional Experience

### Freelancer - Software Engineer
*05/2025 - Present | Remote*

- Built **SoporteML**, an AI-powered multi-tenant CRM for Mercado Libre sellers: React + Vite + TypeScript frontend, Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions) backend, RAG-based reply suggestions with pgvector, Autopilot with confidence guardrails, multi-company and team roles, and webhook-driven Stripe billing. Shipped the first production client, **Pro Motors** (pro-motors.com.ar), with a live Mercado Libre integration.
- Own the product end to end: decide what to build from an ambiguous brief, implement it, test it, put it in production, and support it. No handoff to another team between the idea and the shipped feature.
- Built an **AI Engineering OS** on OpenClaw: per-project sessions, persistent memory, handoffs, subagents, reusable skills, and a pipeline for open source contributions. Its working method is quarantine → analyze → verify → adopt: nothing from outside enters the codebase without being read, analyzed and verified first.
- Delivered internal AI solutions for Pro Motors.

### EY (Ernst & Young) - Senior Frontend Engineer, Accessibility Lead
*09/2021 - 05/2025 | Hybrid*

- Led accessibility for **EY Motif**, an enterprise React component library consumed across client and internal products: remediated **50+ components** to WCAG 2.2 AA (keyboard navigation, screen reader support, focus management, contrast) with Axe DevTools, Lighthouse, JAWS and NVDA.
- Served as the team's accessibility reference across projects: reviewed Storybook components **before** implementation, defined component-level standards, and wrote technical requirements with code guidance for UI stories.
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
- **carbon-design-system/carbon #22887** - Added explicit `aria-describedby` support to `ComposedModal`, across both the native `<dialog>` path and the `div[role=dialog]` path.
- **mui/material-ui #49003** - Kept carousel links in hidden slides out of the focus order; WCAG 4.1.2 `aria-hidden-focus`.
- Eight more merged PRs across IBM Carbon (product components), Meta Astryx (breadcrumb semantics, CI on old PRs, HoverCard popup contract, TreeList labelling) and MUI Base UI (ARIA ownership on unsupported roles).

## Education and Certifications

- **Deque University - Accessibility Specialist Program (2021)**
- **Digital House - React (2018)**

## Languages

- Spanish - native
- English - B2+ (professional working proficiency; reading and writing are comfortable, spoken English is my current development area)

## Notes / gaps

- **Feature flags** - I have not built or operated a feature flag service. My rollout work was implementing experiment variants directly in the client, not gating them behind a flag service.
- **Funnel analysis and activation/retention metrics** - not direct exposure. I ran the experiments and read their results; I did not own the metrics or the event pipeline.
- **Event instrumentation pipelines** - not my direct work; my backend is PostgreSQL/Supabase with RLS and webhooks, not an analytics stack.
- **MongoDB** - my backend work is PostgreSQL (Supabase); I read the requirement and would need to ramp up on it.
- **MCP (Model Context Protocol)** - I built and maintain an MCP companion server (kanam-fixer) that lets an agent query what a screen reader announces for a snippet of HTML, spoken over stdio. I have not operated an MCP server as a production service for a product.
- **Observability** - no direct ownership of a tracing or metrics stack; my own product runs with production monitoring at the level of its own telemetry.
- **On-call rotation** - the role lists on-call; I have run production services with monitoring, and I would take it on as part of the role.

## Keyword map

| JD requirement | Where it is covered |
|---|---|
| 5+ years building production software | Professional Summary (10+ years), all four roles |
| React, TypeScript, Node.js | Core Skills, every role |
| Customer-facing product in partnership with product and design | Freelancer (end to end), EY (design review before implementation) |
| A/B testing and experimentation | Minutentag (Adobe Target, production experiments) |
| AI-assisted development tools | Professional Summary, Freelancer (AI Engineering OS) |
| Ownership of ambiguous problems, concept to delivery | Freelancer (own product end to end) |
| Mentoring and technical leadership | EY (led 3 engineers, in-sprint guidance), OSS reviews |
| Performance, reliability, accessibility of user journeys | Super7UI (CI gate), EY (50+ components), OSS fixes |
| Feature flags | **Gap** |
| Activation / engagement / retention metrics | **Gap** |
| Analytics instrumentation pipelines | **Gap** |
| MongoDB | **Gap** (PostgreSQL) |
