# GONZALO BLASCO

**Senior Full Stack Developer | AI-First Engineering | React, TypeScript, Node | Legacy to Modern Web**

Núñez, Buenos Aires, Argentina | Remote (LATAM), aligned to US EST core hours
+54 11 4937 4656 | gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco

## PROFESSIONAL SUMMARY

Senior full stack engineer with 10+ years building and shipping production web applications, working AI-first since 2025: AI-assisted development is how I work every day, not a side experiment. Frontend is my home ground (React, Next.js, TypeScript), with hands-on backend work in Node, PostgreSQL, REST APIs and Edge Functions since 2025, and I have led full stack migrations from legacy stacks to modern React applications for platforms serving 2M+ monthly active users. I pair hands-on delivery with technical leadership: mentoring engineers, running code review, and coaching teams in-sprint. Python is part of my current AI-assisted toolset and I ramp fast onto new stacks; React and the JS/TS full stack are my home ground. Digital accessibility (WCAG) is a lasting differentiator: the habit of reading structure and semantics that raises the quality of the whole stack.

## CORE SKILLS

- **Frontend:** React, Next.js (SSR), TypeScript, JavaScript (ES6+), HTML5, CSS3, Sass, component architecture, design systems.
- **Backend and data:** Node.js, REST API integrations, webhooks, Supabase (PostgreSQL, Auth, Realtime, Edge Functions, RLS), SQL (PostgreSQL primary; MSSQL working knowledge), Stripe billing.
- **Languages:** TypeScript / JavaScript (primary), Python (working proficiency, AI-assisted), SQL.
- **Testing and quality:** Jest, React Testing Library, Playwright, Vitest, axe-core, automated quality gates in CI/CD, SOLID, clean code.
- **Cloud and DevOps:** Azure (Super7UI, EY), Docker, CI/CD pipelines, Git.
- **Tools and workflow:** Bitbucket, Jira, Biome, agile SDLC.
- **Leadership and collaboration:** code review of PRs and diffs, mentoring and in-sprint coaching, technical requirements and documentation, cross-regional matrixed teams (US / India), proactive communication with product and UX.
- **Accessibility (differential):** WCAG 2.2 A/AA, WAI-ARIA Authoring Practices, screen readers (JAWS, NVDA, VoiceOver, TalkBack).

## PROFESSIONAL EXPERIENCE

### Freelancer & Full Stack Engineer
05/2025 - Present | Remote

- Built and shipped SoporteML, an AI-powered multi-tenant CRM for Mercado Libre sellers, covering the full stack: React + Vite + TypeScript frontend, Supabase (PostgreSQL, Auth, Realtime, Edge Functions, RLS) backend, webhook-driven Stripe billing and REST integrations.
- Work daily with AI-assisted development tools (Cursor, Claude Code, Copilot) as the default way of building and shipping; used the same workflow to ramp onto Python and backend tooling.
- Contribute fixes and reviews to open source React component libraries and frontend frameworks.

### EY (Ernst & Young) - Senior Full Stack / Frontend Engineer, Team Lead
09/2021 - 05/2025 | Hybrid

- Led a team of 3 engineers building an AI-powered financial intelligence platform in Next.js, delivering it end to end from architecture to production.
- Built and maintained EY Motif, an enterprise React component library (design system) consumed across client and internal products: 50+ components covering keyboard navigation, focus management and color contrast.
- Delivered full stack work integrating frontend with backend services and APIs, working across multiple SDLC phases in parallel within agile squads.
- Reviewed components in Storybook before implementation and wrote technical requirements with component guidance and code examples for UI stories; tracked and prioritized defects in Jira.
- Mentored and coached engineers in-sprint, providing code remediation guidance directly inside their branches; recruited into a cross-regional, matrixed team (US / India).
- Worked with Azure services as part of the delivery stack.

### Super7UI - Frontend Engineer (Contractor)
08/2020 - 05/2021 | Remote

- Led the frontend audit and remediation for Warner Bros. Screeners (WBTVD), a private streaming platform used by global distributors to review WB content.
- Built an automated testing pipeline with axe-core and Playwright integrated into CI/CD, preventing non-compliant code from merging.
- Authored developer-ready remediation specs and implementation guidance for core user journeys; worked with Azure in the deployment pipeline.

### Minutentag - Frontend Developer
02/2016 - 11/2019 | Hybrid

- Contributed to migrating legacy interfaces to React and HTML5 for a platform serving 2M+ monthly active users, preserving layout fidelity across breakpoints.
- Implemented and maintained e-commerce flows (Checkout, Cart, Quick View) for three US fashion brands (Ann Taylor, LOFT, Lou & Grey), including dynamic aria-live regions for real-time cart notifications.
- Mentored a junior developer and ran A/B experiments in production with Adobe Target, working in agile squads alongside design and product.
- Worked with Bitbucket and Jira in an agile team, including CI/CD workflows.

## OPEN SOURCE: MERGED PULL REQUESTS

### Merged contributions

- **facebook/astryx** - Four merged fixes covering WCAG 1.4.1 breadcrumb indicators (#4605), a CI fetch-depth fallback for stale PRs (#4914), HoverCard dialog semantics with aria-haspopup/aria-controls/aria-expanded (#5419), and TreeList labelling on the role=tree element (#5493). All shipped with regression tests.
- **mui/base-ui** - Merged #5551: moved aria-orientation to the correct role owners across combobox, menu and select (7 files), preserving keyboard navigation, with regression tests.
- **mui/material-ui** - Merged #49003: removed focusable links from hidden carousel slides (WCAG 4.1.2).
- **adobe/react-spectrum** - Merged #10503: gated the ComboBox live-region announcement to section changes only, so it stops overriding VoiceOver's richer native per-item announcements (selected state, menu item role, item count) while preserving cross-section announcements; verified with real VoiceOver on macOS. Merged with two maintainer approvals.
- **adobe/react-spectrum** - Merged #10554: test-only regression for global aria-posinset across virtualized listbox sections, verified to fail without the fix.
- **carbon-design-system/carbon** - Merged #22887: added explicit aria-describedby prop support to ComposedModal, wired through both the native Dialog path and the div[role=dialog] fallback, with tests covering both render paths.
- **carbon-design-system/ibm-products** - Merged #9878: fixed focus loss in CreateFullPage (the active-step query matched inert-hidden steps), with a regression test validated against the real DOM.
- **carbon-design-system/ibm-products** - Merged #9879: Datagrid sortable headers were announced as toggle buttons (aria-pressed) with no direction; replaced with aria-sort, with a regression test.

### Reviews and analyses that drove fixes to merge

- **carbon-design-system/ibm-products #9868** - First human review on another author's PR: verified the diff against the legacy implementation and the Carbon source, raised two concrete signals (lost role=region props, wrong background token on a variant), and one was adopted before merge.
- **carbon-design-system/ibm-products #9866** - Cross-cluster analysis of four React 19 issues in the same family: traced each to state derived during commit, explained the nestedUpdateCount accumulation, and proposed per-hook fix directions.
- **vercel/next.js #73474** - Separated three conflated causes of a Suspense/loading failure (proxy caching text/html, streaming buffered by the reverse proxy, await before a Suspense boundary) with a per-scenario diagnosis and reproduction; the maintainer closed the issue confirming the analysis.

## LANGUAGES

- **Spanish** - Native.
- **English** - B2. Written work is my strongest channel: documentation, code review, async communication and technical reading, every day. For live meetings I am functional and improving the spoken format.

## CERTIFICATIONS

**Deque University - Accessibility Specialist Program (2021)**

- Accessibility Fundamentals: Disabilities, Guidelines and Laws
- Designing an Accessible User Experience
- Semantic Structure and Navigation
- Images, SVG and Canvas

## EDUCATION

- **Digital House** - React (2018)
- **Universidad Argentina de la Empresa** - Diseño Gráfico (2003 - 2004)
