# GONZALO BLASCO

**Frontend Engineer | Code Evaluation and UI Fidelity | React, TypeScript, Accessibility**

Núñez, Buenos Aires, Argentina | Remote (LATAM) | Full-time or part-time, flexible hours
+54 11 4937 4656 | gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco

## PROFESSIONAL SUMMARY

Frontend engineer with 10+ years building and reviewing production interfaces, and a strong background in
judging whether code is correct, not just renderable. I read HTML, CSS and JavaScript to tell the difference
between a layout that is genuinely correct and one that only looks correct at a single viewport, and I back
every verdict with concrete evidence from DevTools. I spent roughly 5 years with accessibility as the core of
the role, which is exactly the skill of reading structure (ARIA, landmarks, heading hierarchy) that code
evaluation depends on. I also complete structured code-review and preference-comparison tasks, and I write
professional English findings, proven by merged pull requests into Adobe React Spectrum, IBM Carbon, Meta
Astryx and MUI.

## CORE COMPETENCIES

- **Code and layout evaluation:** reading HTML/CSS/JS to assess correctness, semantic structure, flexbox, CSS
  grid, media queries, and legacy layout models including float and table-based layouts. DevTools as muscle
  memory for inspecting DOM, styles and computed layout.
- **Visual fidelity:** pixel-level review of rendered UI against design intent, including Figma design review
  and writing component-level implementation specs before code is written.
- **Accessibility as a structural lens:** WCAG 2.2 A/AA, WAI-ARIA Authoring Practices, ARIA, landmarks, heading
  hierarchy, keyboard navigation, focus management, color contrast.
- **Structured review and evaluation:** code review against a rubric, preference labeling and response
  comparison, model output assessment, defect triage by impact.
- **Assistive technology and testing:** JAWS, NVDA, VoiceOver, TalkBack; axe-core, Axe DevTools, Lighthouse,
  Playwright, manual and automated audits, accessibility gating in CI/CD.
- **Tooling:** Git, CLI (unzip, static file serving, asset path debugging), React, Next.js, JavaScript,
  TypeScript, HTML, CSS, Sass.
- **Communication:** professional written English, technical documentation, in-sprint developer support, and
  collaboration in matrixed teams (US / India).

## PROFESSIONAL EXPERIENCE

### Freelancer & Software Engineer
05/2025 - Present | Remote

- Built kanam-fixer, an automated accessibility engine that maps a browser DOM node back to its exact source
  line in a TypeScript codebase, then applies and re-verifies fixes in a scan-fix-scan loop. This is direct
  DOM-to-code tracing, the same reasoning used when judging whether rendered output matches its source.
- Complete structured evaluation work: code analysis for best practices and time/space efficiency, comparison
  of competing model responses, and DOM/HTML parsing exercises (extracting and reconstructing structured data
  from a published HTML document).

### EY (Ernst & Young) - Senior Frontend Engineer, Accessibility Lead
09/2021 - 05/2025 | Hybrid

- Owned WCAG 2.2 AA compliance for EY Motif, an enterprise React component library consumed across client and
  internal products: audited and remediated 50+ components covering keyboard navigation, screen reader support,
  focus management and color contrast.
- Reviewed Figma designs before implementation to catch structural and compliance issues early, and wrote
  technical requirements with component guidance and code examples for UI stories.
- Tracked and prioritized accessibility defects by WCAG impact and provided code remediation guidance to
  developers in sprint, working directly inside their branches.
- Led a team of 3 engineers building an AI-powered financial intelligence platform in Next.js, delivering
  accessible interfaces from architecture to production.

### Super7UI - Accessibility Engineer (Contractor)
08/2020 - 05/2021 | Remote

- Led the accessibility audit for Warner Bros. Screeners, a private streaming platform used by global
  distributors, validating each reported issue across NVDA, VoiceOver and TalkBack and documenting 200+
  WCAG violations with reproduction steps.
- Authored full remediation documentation: proposed solutions, implementation guidance and developer-ready
  specifications for core user journeys.
- Built an automated testing pipeline with axe-core and Playwright in CI/CD, preventing non-compliant code
  from merging.

### Minutentag - Frontend Developer, Accessibility Owner
02/2016 - 11/2019 | Hybrid

- Worked on legacy Ascena Retail Group sites (Ann Taylor, LOFT, Lou & Grey) built with jQuery and Handlebars,
  including float-based and table-based layouts, maintaining and extending the existing markup and styles.
- Led migration of legacy jQuery/Handlebars interfaces to React, Sass and HTML5 for a platform serving 2M+
  monthly active users, preserving layout fidelity across breakpoints.
- Took ownership of accessibility at month three and self-taught WCAG compliance through hands-on testing on
  physical iOS and Android devices.
- Implemented accessibility across e-commerce flows (Checkout, Cart, Quick View), including dynamic aria-live
  regions, and mentored a junior developer.

## OPEN SOURCE: FRONTEND CODE AND REVIEW

Merged fixes, active reviews and code-review collaborations across the React component libraries and frontend
frameworks that frontend code evaluation targets.

### Merged contributions

- **facebook/astryx** - Four merged fixes covering WCAG 1.4.1 breadcrumb indicators (#4605), a CI fetch-depth
  fallback for stale PRs (#4914), HoverCard dialog semantics with aria-haspopup/aria-controls/aria-expanded
  (#5419), and TreeList labelling on the role=tree element (#5493). All shipped with regression tests.
- **mui/base-ui** - Merged #5551: moved aria-orientation to the correct role owners across combobox, menu and
  select (7 files), preserving keyboard navigation, with regression tests.
- **mui/material-ui** - Merged #49003: removed focusable links from hidden carousel slides (WCAG 4.1.2).
- **adobe/react-spectrum** - Merged #10554: test-only regression for global aria-posinset across virtualized
  listbox sections, verified to fail without the fix.
- **carbon-design-system/ibm-products** - Merged #9878: fixed focus loss in CreateFullPage (the active-step
  query matched inert-hidden steps), with a regression test validated against the real DOM.

### Code review and source analysis

- **carbon-design-system/ibm-products #9868** - First human review on another author's PR: verified the diff
  against the legacy implementation and the Carbon source, raised two concrete signals (lost role=region props,
  wrong background token on a variant), and one was adopted before merge.
- **carbon-design-system/ibm-products #9866** - Cross-cluster analysis of four React 19 issues in the same
  family: traced each to state derived during commit, explained the nestedUpdateCount accumulation, and
  proposed per-hook fix directions.
- **vercel/next.js #73474** - Separated three conflated causes of a Suspense/loading failure (proxy caching
  text/html, streaming buffered by the reverse proxy, await before a Suspense boundary) with a per-scenario
  diagnosis and reproduction; the maintainer closed the issue confirming the analysis.

### Open and in-review pull requests

- **Accessibility semantics and focus management:** adobe/react-spectrum #10503 (gate VoiceOver combobox
  announcements to section changes, CI green) and #10517 (expose input styling on RAC Checkbox and Radio);
  radix-ui/primitives #4109 (announce select option position and total); facebook/docusaurus #12387 (announce
  page title on route change; approach validated by a maintainer).
- **Layout and rendering fixes:** shadcn-ui/ui #11179, #11180, #11187, #11198 and #11465 (input-OTP layout
  shift, message-scroller footer flicker, table scrollbar, keyboard navigation and scroll spacer release).
- **Component and tooling:** carbon-design-system/ibm-products #9879 (Datagrid sortable headers announced as
  toggle buttons instead of using aria-sort); carbon-design-system/carbon #22887 (aria-describedby on
  ComposedModal); t3-oss/create-t3-app #2240 and #2243 (generated-file ignore rules, aria-label on the
  clipboard button).
- **Frontend ecosystem:** TanStack/router #7834 and vercel/ai #17274 (serialization and streaming fixes, both
  mergeable and gated only on maintainer review).

## CERTIFICATIONS

**Deque University - Accessibility Specialist Program (2021)**

- Accessibility Fundamentals: Disabilities, Guidelines and Laws (03/2021)
- Designing an Accessible User Experience (03/2021)
- Semantic Structure and Navigation (04/2021)
- IAAP Certification Quick Guide (04/2021)
- Images, SVG and Canvas (06/2021)
