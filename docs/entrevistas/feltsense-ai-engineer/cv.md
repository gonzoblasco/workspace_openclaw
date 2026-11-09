# Gonzalo Blasco

**AI Engineer - Agent Systems, LLM Backends**

Núñez, Buenos Aires, Argentina | Remote (LATAM, aligned to US EST) | +54 11 4937 4656 | gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco

## Professional Summary

AI-first software engineer with 10+ years shipping production web applications, 4+ of them leading front-end work in cross-regional teams, and the last 1.5 years of applied AI (70/30 frontend/backend split). I run my own engineering practice on OpenClaw: per-project sessions, persistent memory, handoffs, subagents, reusable skills, and an open-source pipeline, governed by a strict quarantine → analyze → verify → adopt method, so anything generated or adopted gets read and verified before it ships. That same practice includes an MCP server that exposes accessibility semantics to AI coding agents. On the product side I built **SoporteML**, a multi-tenant CRM with RAG-based reply suggestions, confidence-guarded autopilot, multi-company roles and Stripe billing, shipped to its first production client, **Pro Motors**. Stack: TypeScript/React on the front end, Supabase (PostgreSQL, Edge Functions, pgvector, Realtime, RLS) on the back end. 11 merged pull requests in production component libraries. Daily AI coding on **Claude Code** and **OpenAI Codex**; I delegate, review, and verify rather than trust generated code.

## Core Skills

- **Agentic systems (own practice):** per-project sessions, persistent memory, handoffs, subagents, reusable skills, OSS pipeline; quarantine → analyze → verify → adopt. MCP server (`kanam-fixer`) exposing screen-reader semantics to agents.
- **LLM-based backends:** prompt engineering, structured outputs, embeddings, retrieval (pgvector), confidence guardrails, feedback-style loops in production flows (SoporteML reply suggestions + autopilot).
- **Backend:** Node.js/TypeScript, REST APIs, Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions), pgvector, Stripe billing and webhooks, webhook-driven flows.
- **Frontend:** React, TypeScript, JavaScript, Vite, Next.js (SSR), Tailwind, Storybook, component architecture, design systems, design tokens.
- **Quality and standards:** Vitest, Playwright, Biome, Zod, CI/CD (GitHub Actions, Azure DevOps pipelines), code review, technical requirements with code examples, accessibility as a gating criterion.
- **Leadership:** led 3 engineers (EY); matrixed US/India squads; standards across code review, testing, and release.
- **Accessibility (differential):** WCAG 2.2 AA, ARIA patterns (role / state / property wiring), screen readers (JAWS, NVDA, VoiceOver, TalkBack), Axe DevTools, Lighthouse.

**Not claimed (not in my stack):** GCP Cloud Run, Inngest / Pub-Sub background job systems, Vercel AI SDK, Claude Agent SDK, Cursor, Vercel deployment. I work with Codex and Claude Code; never Cursor.

## Professional Experience

### Freelancer - Software Engineer
*05/2025 - Present | Remote (Argentina)*

- Built **SoporteML**, an AI-powered multi-tenant CRM for Mercado Libre sellers: React + Vite + TypeScript front end, Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions) back end, RAG-based reply suggestions with pgvector, confidence-guarded autopilot, multi-company and team roles, and Stripe billing. Shipped the first production client, **Pro Motors** (pro-motors.com.ar), with a live Mercado Libre integration.
- Designed and runs an **AI Engineering OS** on OpenClaw: per-project sessions, persistent memory, handoffs between agents, subagents with scoped context, reusable skills, and an open-source contribution pipeline, under a quarantine → analyze → verify → adopt method. This is the system I use to do the work; nothing external is adopted without being read and verified first.
- Built and maintains an **MCP server** (`kanam-fixer`) that exposes to AI agents what a screen reader announces for an HTML fragment (MCP over stdio, two tools). Used as part of the agent workflow above.
- Owns products end to end, from ambiguous problem to shipped and billed: product decisions, implementation, tests, production deployment.
- Daily tooling on macOS: VS Code, Terminal/zsh, Git, Docker, npm/pnpm/bun, CI via GitHub Actions; Node.js, TypeScript, Playwright, Vitest, Biome.

### EY (Ernst & Young) - Senior Frontend Engineer, Accessibility Lead
*09/2021 - 05/2025 | Hybrid*

- Led a team of **3 engineers** building an AI-powered financial intelligence platform in Next.js, with accessible interfaces from architecture to production. (SSR work lives here.)
- Owned accessibility for **EY Motif**, an enterprise React component library consumed by client and internal products: remediated **50+ components** to WCAG 2.2 AA (keyboard navigation, screen reader support, focus management, contrast) with Axe DevTools, Lighthouse, JAWS and NVDA.
- Served as the team's accessibility reference across projects: reviewed Storybook components **before** implementation, defined component-level standards and annotations, wrote technical accessibility requirements with code guidance for UI stories.
- Prioritized accessibility defects by WCAG impact in Jira, with remediation guidance to developers inside the sprint.
- Worked in a matrixed, cross-regional (US/India) team across multiple SDLC phases in parallel within agile squads; daily use of Azure DevOps (pipelines, tickets, user stories), Jest + React Testing Library, Redux and React Query.
- Tooling (verified): TypeScript, React, Vitest, Playwright, Biome, Tailwind, Storybook, Zod.

### Super7UI - Accessibility Engineer (Contractor)
*08/2020 - 05/2021 | Remote*

- Led the front-end audit and remediation for **Warner Bros. Screeners (WBTVD)**, the private streaming platform global distributors use to review content.
- Validated and expanded a prior third-party audit by reproducing each reported issue across NVDA, VoiceOver and TalkBack; used Axe to identify and document WCAG violations in key flows.
- Resolved **200+ WCAG violations** and produced developer-ready remediation documentation: proposed solutions, implementation guidance, development-ready specifications.
- Established an accessibility testing pipeline with **axe-core + Playwright integrated into CI/CD**, so non-compliant code could not merge.

### Minutentag - Frontend Developer, Accessibility Owner
*02/2016 - 11/2019 | Hybrid*

- Contributed to migrating legacy interfaces to React and HTML5 on a platform serving **2M+ monthly active users**, and maintained the e-commerce flows (checkout, cart) for **Ann Taylor, LOFT and Lou & Grey**.
- Grew from junior to the team's accessibility owner.
- Ran A/B experiments in production with Adobe Target against live user segments, inside agile squads, implementing variants as JavaScript snippets.

## Open Source - Merged Pull Requests (11)

Merged fixes in production component libraries and design systems, each reviewed and shipped by maintainers.

- **adobe/react-spectrum #10503** - gated the ComboBox live-region announcement to section changes so it stops overriding the native per-item VoiceOver announcement.
- **adobe/react-spectrum #10554** - regression test for global `aria-posinset` across sections.
- **carbon-design-system/carbon #22887** - explicit `aria-describedby` support on `ComposedModal`, across both the native `<dialog>` path and the `div[role=dialog]` path.
- **carbon-design-system/ibm-products #9878** - `CreateFullPage` (issue #9864).
- **carbon-design-system/ibm-products #9879** - Datagrid (issue #9839).
- **facebook/astryx #4605** - non-chromatic indicator (font weight) on the current breadcrumb item; WCAG 1.4.1.
- **facebook/astryx #4914** - `build-storybook` failed with "no merge base" on old PRs (fetch-depth); fallback to a two-point diff.
- **facebook/astryx #5419** - HoverCard with a label exposed as a dialog popup: `aria-haspopup=dialog` + `aria-controls` gated on open, `aria-expanded` synchronized.
- **facebook/astryx #5493** - `TreeList` forwards `aria-label`/`aria-labelledby` to the underlying `ul role=tree`.
- **mui/base-ui #5551** - moved `aria-orientation` to the owners of the role; the grid role does not support it.
- **mui/material-ui #49003** - kept carousel links in hidden slides out of the focus order (WCAG 4.1.2 `aria-hidden-focus`).


### Contributions without a merged PR (diagnostics, review notes, verified resolutions)

- **ibm-products #9868** - first human review of an external PR; the two raised signals were addressed by the author and the PR merged. Comment: issuecomment-5609797683.
- **ibm-products #9866** - cross-issue diagnosis (React 19 state-during-commit cluster across #9865/#9866/#9867) at source level, with per-hook fix directions. Comment: issuecomment-5609873985.
- **next.js #73474** - diagnostic separation of three conflated failure scenarios; maintainer accepted it and closed the issue as "downstream response buffering, not a Next.js failure".
- **carbon #16031** - verified-resolution of an issue, confirmed by the maintainer via #22751.
- **react-spectrum #9556 / #10220** - evidence-based review comments on AI-assisted PRs: test expectations and scope narrowing without claiming VoiceOver access.
- **astryx #4871** - comparative review of two competing PRs (focus retention vs. anchor identity) with test guidance.

## Training & Certifications

- **Digital House — React (2018, completed bootcamp)**
- **Deque University — Accessibility Specialist Program (2021, training program, not a professional certification)**
## Languages

- Spanish - native
- English - B2+ (professional working proficiency; reading and writing are comfortable, spoken English is the current development area)


## Keyword map (JD Feltsense - AI Engineer)

| JD requirement | Where it is covered | Gap / honesty note |
|---|---|---|
| 4+ years professional software engineering | 10+ years (2016-) | Meets |
| Technical leadership at early-stage company | Led 3 engineers at EY; own freelance practice; no titled Founding Engineer/Tech Lead role at an early-stage company | Gap - frame as leadership without overstating title |
| Build/ship multi-agent systems and orchestration to production | Own AI Engineering OS with subagents/handoffs/memory; SoporteML AI flows | Own system, not a customer-facing multi-agent product - stated as such |
| Self-improving/self-evolving agent harnesses | Confidence-guarded autopilot + feedback loops in SoporteML; verify/adopt method in own OS | Evolving today via guardrails and verification, not a finished self-improving harness |
| Strong backend (APIs, services, data flows) | Supabase/Postgres/Edge Functions/Stripe RAG back end, 1.5 yr | Meets for the 1.5-yr scope; not a 4-yr backend career |
| LLM systems: prompt engineering, model config, structured outputs, embeddings, retrieval, evaluation | SoporteML RAG reply suggestions + autopilot; MCP semantics server | No named provider (Anthropic/OpenAI/Gemini/GCP) claimed |
| Daily AI coding agents, delegation + review + verification | Claude Code + OpenAI Codex in daily loop; quarantine→verify→adopt | No Cursor in my stack |
| TypeScript + Node.js (nice-to-have) | TypeScript daily; Node.js/TypeScript back end 1.5 yr | Meets |
| Vercel AI SDK / Claude Agent SDK (nice-to-have) | Not used | Not claimed |
| PostgreSQL / Supabase / pgvector (nice-to-have) | Supabase + pgvector in SoporteML | Meets |
| Background jobs Inngest / Pub-Sub (nice-to-have) | Not used | Not claimed |
| Zod / Vitest / GCP Cloud Run (nice-to-have) | Vitest + Zod daily; no GCP Cloud Run | Partial - honest |
| Growing/restructuring distributed teams (nice-to-have) | Cross-regional EY squads | Adjacent, not reorg leadership |
| AI eval / safety / observability (nice-to-have) | Confidence guardrails, CI gating, Axe/Lighthouse | Adjacent interest, not a formal eval program |
| Remote from Argentina, USD 60k-110k | Argentina remote, contractor setup | Meets geography |
