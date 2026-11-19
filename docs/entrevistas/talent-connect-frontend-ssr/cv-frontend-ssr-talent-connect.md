# Gonzalo Blasco

**Senior Frontend Engineer - React, Design Systems and Data UI**

Núñez, Buenos Aires, Argentina | Remote or Hybrid (Buenos Aires, GMT-3) | +54 11 4937 4656 | gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco

## Professional Summary

Frontend engineer with **10+ years** building production web interfaces with React, TypeScript and HTML5/CSS3. I build reusable, tested React components and take **ownership** of the product from ambiguous requirement to production: component APIs, state and data-fetching layers, and the tests that keep them honest. Design systems are my home ground - I have audited and remediated **50+ components** of an enterprise React component library to WCAG 2.2 AA, and built a semantic token system for my own product. Daily tooling includes **Jest and React Testing Library** for unit tests, and **Azure DevOps** for pipelines, tickets and user stories. I integrate REST APIs of real complexity and care about accessible interfaces as a baseline, not a polish step. AI coding agents (Claude Code, Codex) are part of the daily loop under a strict quarantine → analyze → verify → adopt method. Merged pull requests in the component libraries of Adobe, IBM Carbon, Meta, MUI, shadcn and TanStack, plus reviews and diagnosis that shaped fixes in other maintainers' PRs.

## Core Skills

- **Frontend:** React, TypeScript, JavaScript, Next.js (SSR), Vite, HTML5, CSS3/SCSS, Tailwind, component architecture, design systems, design tokens, responsive layouts.
- **State and data:** **Redux**, **React Query**, REST API integration, data fetching and caching, paginated and asynchronous UI state, dashboards and data visualization components.
- **Testing:** **Jest**, **React Testing Library**, Playwright, Vitest, regression tests on component contracts, accessibility tests in CI (axe-core).
- **Delivery:** **Azure DevOps** (CI/CD pipelines, tickets, user stories), GitHub Actions, Git/GitHub, Jira, agile squads across the SDLC.
- **Accessibility (quality bar):** WCAG 2.2 AA, ARIA patterns (role, state and property wiring), screen readers (JAWS, NVDA, VoiceOver, TalkBack), Axe DevTools, Lighthouse.
- **AI-augmented development:** Claude Code and Codex in the daily loop, agent orchestration, prompt and context design; generated code is audited before it lands.
- **Backend and data:** Node.js, REST, Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions), pgvector, Stripe billing, webhooks.

## Professional Experience

### Freelancer - Software Engineer
*05/2025 - Present | Remote*

- Built a multi-tenant **design system of semantic tokens** (color, typography, spacing, radius, shadows, focus ring, states) for a production React + Vite + TypeScript application, with a typographic scale and an explicit token-to-component map applied through Tailwind - so every screen came from the same set of primitives instead of ad-hoc styles. WCAG AA rules were the system's criterion, not a final check.
- Built the **chat interface for AI agents**: streaming conversation with a retrieval-backed assistant, confidence-gated replies, and the state layer that keeps a long conversation coherent under network failure and retries.
- Shipped the first production client, **Pro Motors** (pro-motors.com.ar), with a live Mercado Libre integration and webhook-driven billing (Stripe).
- Built an **AI Engineering OS** on OpenClaw: per-project sessions, persistent memory, handoffs, subagents and reusable skills. Its working method is quarantine → analyze → verify → adopt: nothing from outside enters the codebase without being read, analyzed and verified first.
- Own products end to end - product decisions, implementation, tests and production deployment - and take technical ownership of what ships with my name on it.

### EY (Ernst & Young) - Senior Frontend Engineer, Accessibility Lead
*09/2021 - 05/2025 | Hybrid*

- Worked on **EY Motif**, an enterprise React component library consumed across client and internal products: audited and remediated **50+ components** to WCAG 2.2 AA (keyboard navigation, screen reader support, focus management, contrast) with Axe DevTools, Lighthouse, JAWS and NVDA. The component API had to stay stable for every consuming product while the internals changed.
- Served as the team's accessibility reference across projects: reviewed **Storybook** components **before** implementation, defined component-level standards and annotations, and wrote technical requirements with code guidance for UI stories.
- Used **Azure DevOps daily**: CI/CD pipelines, tickets and user stories, keeping delivery and remediation work visible inside the sprint.
- Led a team of **3 engineers** building an AI-powered financial intelligence platform in **Next.js with server-side rendering**, with accessible interfaces from architecture to production.
- Prioritized accessibility defects by WCAG impact in Jira, with remediation guidance to developers inside the sprint.
- Worked in a matrixed, cross-regional team (US / India) across multiple SDLC phases in parallel within agile squads.

### Super7UI - Accessibility Engineer (Contractor)
*08/2020 - 05/2021 | Remote*

- Led the frontend audit and remediation for **Warner Bros. Screeners (WBTVD)**, the private streaming platform global distributors use to review content.
- Validated and expanded a prior third-party audit by reproducing each reported issue across **NVDA, VoiceOver and TalkBack**, and used Axe to identify and document WCAG violations in the key flows.
- Resolved **200+ WCAG violations** and produced developer-ready remediation documentation: proposed solutions, implementation guidance and development-ready specifications.
- Established an accessibility testing pipeline with **axe-core + Playwright integrated into CI/CD**, so non-compliant code could not merge.

### Minutentag - Frontend Developer, Accessibility Owner
*02/2016 - 11/2019 | Hybrid*

- Contributed to migrating legacy interfaces to **React** and HTML5 on an e-commerce platform serving **2M+ monthly active users**, and maintained the checkout and cart flows for Ann Taylor, LOFT and Lou & Grey.
- Wrote and maintained unit tests for the migrated interfaces with **Jest and React Testing Library**, so the migration could land incrementally without breaking live purchase flows.
- Grew from junior to the team's accessibility owner.
- Ran **A/B experiments in production with Adobe Target** against live user segments on features and designs, inside agile squads alongside design and product, implementing the variants as JavaScript snippets.

## Open Source

**Authored - merged** in production component libraries and design systems of Adobe, IBM Carbon, Meta, MUI, shadcn and TanStack, each reviewed and shipped by maintainers.

- **shadcn-ui/ui #11465** - Stopped the released tail spacer from re-anchoring after a manual scroll during an anchored stream.
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

**Collaboration - merged through other authors.** Reviews and technical comments that shaped the fix.

- **meta/astryx #5563, #5373, #5414, #4157** - Technical comments on prop forwarding across BaseProps components, Popover fit and focus behavior, breadcrumb audit pass, and avatar status variants.
- **carbon-design-system/ibm-products #9869** - First human review on another author's PR: corrected the Carbon layer hierarchy in Tearsheet, where the body was elevated instead of the container.
- **TanStack/query #11036** - Commented on the Suspense resolution when query data is set programmatically.
- **openclaw/openclaw #127213, #126714** - Submitted reviews: exposing the active split pane to assistive technology, and softening its visual indication.

**Engaged beyond own PRs.** Reviews and technical comments on issues and pull requests in maintained projects including vercel/next.js and Radix UI, where the diagnosis contributed to a fix authored by someone else.

## Certifications and Training

- **Digital House - React (2018)**
- **Deque University - Accessibility Specialist Program (2021)**

## Languages

- Spanish - native
- English - B2+ (professional working proficiency; reading and writing are comfortable, spoken English is my current development area)

## Notes / gaps

- **Figma:** not declared. Gonzo does not use Figma; design review happened over Storybook components and written specs. If asked: honest answer, no claim.
- **GraphQL:** not declared. The corpus only documents REST. Not confirmed by Gonzo.
- **Zustand:** not confirmed (only Redux and React Query are).
- **Azure Static Web Apps:** not declared. Azure DevOps (pipelines, tickets, stories) is confirmed; hosting the frontend on Azure is not.
- **SSR:** declared through the EY Next.js platform. It is an EY fact, not a freelance one.

## Keyword map

| JD requirement | Where it is covered |
|---|---|
| React in production | Summary, Core Skills, every role since 2016 |
| CSS3 / SCSS and HTML5 | Core Skills; design token system; Minutentag migration |
| REST/GraphQL API integration | Freelancer (REST APIs), Core Skills |
| Jest and React Testing Library | Core Skills; Minutentag unit tests; EY quality work |
| Design implementation from Figma | **Not covered** - see Notes |
| Reusable, tested React components | EY Motif, own design system with semantic tokens, merged PRs |
| Dashboards and complex data visualization | Freelancer (CRM dashboards, agent chat), Core Skills |
| Chat and AI agent interfaces | Freelancer (agent chat interface) |
| Design system, build and document | Freelancer (semantic tokens), EY Motif |
| WCAG basic accessibility | Super7UI, EY Motif, the OSS fixes |
| Ownership | Summary, Freelancer |
| TypeScript | Core Skills, every role |
| Component frameworks (MUI, AntD, Tailwind) | Tailwind in production; merged PRs in MUI and Carbon libraries |
| State management (Redux, Zustand, React Query) | Core Skills (Redux, React Query) |
| Azure DevOps | EY |
| Playwright and Storybook | Super7UI (Playwright CI), EY (Storybook review) |
| Code agents (Claude Code, Codex) | Summary, Freelancer (AI Engineering OS) |
