---
name: "ux-a11y-studio"
description: "UX/UI + Accesibilidad end-to-end: auditoría, diseño, implementación y validación WCAG/ARIA en todos los productos."
---

# UX/A11Y Studio

Use when a product needs UX/UI design and/or accessibility work — whether it's a new product that needs an interface, an existing product that needs an audit, or a feature that needs accessible components. This skill is the in-house UX/UI + accessibility team.

This skill is the **eyes and hands of the interface**. It does:
1. **Discovery** — understands users, context, constraints, accessibility requirements
2. **Audit** — finds accessibility and UX problems in existing interfaces
3. **Design** — defines the visual system, interaction patterns, and accessible component specs
4. **Implement** — builds accessible components and UI
5. **Validate** — verifies WCAG compliance, keyboard nav, screen reader support, cognitive load

Accessibility is NOT a phase at the end. It's a constraint from the start. Every design decision passes through an accessibility filter before it ships.

## Scope

### What this skill does
- UX discovery (user context, journeys, pain points, cognitive load)
- Accessibility audit (automated + manual, WCAG 2.2 AA target)
- Design system definition (colors with contrast, typography scale, spacing, focus states)
- Component specs with ARIA patterns (WAI-APG compliant)
- Accessible UI implementation (React + TypeScript)
- Validation (automated axe-core, keyboard testing, screen reader checks, cognitive walkthrough)
- UX review of existing interfaces (heuristics + accessibility)

### What this skill does NOT do
- Product strategy (that's product-orchestrator)
- Scaffold projects (that's web-app-builder)
- Write business logic (that's dev agents)
- Backend/API work

## Prerequisites

- Project exists (scaffolded via web-app-builder or existing)
- React + TypeScript + Tailwind (default stack)
- For audits: Playwright + axe-core available (or use accessibility-auditor project)
- For component testing: Vitest + @testing-library/react + jest-axe
- Reference: `projects/accessible-ui/` — headless component library with ARIA patterns
- Reference: `projects/accessibility-auditor/` — automated audit platform

## Phase 1 — Discovery & Context

Goal: understand who uses the interface, how, and under what constraints.

### 1a — User context

- **Who:** primary users, secondary users, their context (device, environment, expertise)
- **How:** what device, browser, input method (mouse, keyboard, touch, voice, switch)
- **Constraints:** visual impairments, motor limitations, cognitive differences, situational impairments (bright sun, noisy room, one hand)
- **Assistive tech:** do users rely on screen readers, screen magnifiers, voice control, switch devices?

### 1b — Accessibility requirements

Based on context, determine which WCAG 2.2 criteria apply and at what level:

- **Default target: WCAG 2.2 AA** (the standard for most products)
- **AAA for critical flows** (authentication, core value delivery, legal/financial)
- **Additional requirements:** Section 508 (US gov), EN 301 549 (EU), specific client requirements

Document applicable criteria in `design/A11Y-REQUIREMENTS.md`:

```markdown
## Accessibility Requirements: <product>

### Target
WCAG 2.2 Level AA (default), AAA for auth + core flows

### Applicable criteria (key ones)
- 1.1.1 Non-text Content (A) — all images need alt text or decorative marking
- 1.3.1 Info and Relationships (A) — semantic HTML, ARIA where needed
- 1.4.3 Contrast (Minimum) (AA) — 4.5:1 text, 3:1 large text/UI components
- 1.4.11 Non-text Contrast (AA) — 3:1 for borders, icons, focus indicators
- 2.1.1 Keyboard (A) — all functionality available via keyboard
- 2.1.2 No Keyboard Trap (A) — focus can move in and out of components
- 2.4.3 Focus Order (A) — logical tab order
- 2.4.7 Focus Visible (AA) — visible focus indicator
- 2.4.11 Focus Not Obscured (AA, 2.2 new) — focused element not hidden
- 3.2.1 On Focus (A) — no unexpected context changes on focus
- 3.3.1 Error Identification (A) — errors clearly identified
- 3.3.2 Labels or Instructions (A) — inputs have labels
- 4.1.2 Name, Role, Value (A) — all UI components have accessible names
- 4.1.3 Status Messages (AA) — dynamic content announced via aria-live

### Specific needs
- <any product-specific accessibility requirements>
```

### 1c — UX heuristics baseline

Evaluate the current state (if existing product) against Nielsen's 10 heuristics + accessibility-specific heuristics:

1. Visibility of system status (including aria-live announcements)
2. Match between system and real world
3. User control and freedom (including undo, escape from modals)
4. Consistency and standards (including ARIA patterns)
5. Error prevention (including clear validation)
6. Recognition rather than recall
7. Flexibility and efficiency of use (keyboard shortcuts, customization)
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, and recover from errors
10. Help and documentation
11. **Accessibility-specific:** Keyboard equivalence, focus management, semantic structure, contrast, reduced motion support

Output of Phase 1: **Discovery document** — `design/DISCOVERY.md` with user context, a11y requirements, heuristic baseline.

## Phase 2 — Audit (existing interfaces)

Goal: find every accessibility and UX problem in an existing interface. Skip if this is a new product with no UI yet.

### 2a — Automated audit

Run axe-core against the interface. Options:

**Using accessibility-auditor project:**
- Submit URL to the auditor platform
- Get scored report with violations categorized by impact

**Using axe-core directly (for local dev):**
```bash
npx @axe-core/playwright --url http://localhost:3000
```

**Using Storybook a11y addon (for components):**
- Open Storybook, check a11y panel per story

Capture all violations in `design/AUDIT.md`:

```markdown
## Automated Audit: <product>

### Summary
- Score: <X>/100
- Critical: <n> violations
- Serious: <n> violations
- Moderate: <n> violations
- Minor: <n> violations

### Violations
| # | Rule | Impact | Element | WCAG | Fix |
|---|---|---|---|---|---|
| 1 | color-contrast | critical | .btn-primary | 1.4.3 | Increase contrast to 4.5:1 |
| 2 | aria-label | serious | nav menu | 4.1.2 | Add aria-label="Main navigation" |
```

### 2b — Manual audit (the stuff automated tools miss)

Automated tools catch ~30-40% of accessibility issues. The rest needs manual testing:

1. **Keyboard navigation test:**
   - Tab through the entire interface. Is the order logical?
   - Can you reach every interactive element?
   - Can you escape every container (modals, menus, tab groups)?
   - Are focus indicators visible?
   - Does focus management work (modal trap, return focus on close)?

2. **Screen reader test (VoiceOver on macOS, NVDA on Windows):**
   - Navigate by headings, landmarks, links, buttons
   - Are all elements announced correctly?
   - Do dynamic changes get announced (aria-live)?
   - Do forms have associated labels and instructions?
   - Are error messages announced and associated with inputs?

3. **Cognitive walkthrough:**
   - Can a new user figure out what to do without instructions?
   - Is the information hierarchy clear?
   - Are error states understandable and recoverable?
   - Is the language plain and clear?

4. **Visual checks:**
   - Color contrast (use contrast checker)
   - Text resize (zoom to 200% — does it still work?)
   - Reflow (narrow viewport to 320px — does it reflow without horizontal scroll?)
   - Reduced motion (prefers-reduced-motion — does it respect it?)

Document findings in `design/AUDIT.md` under "Manual Audit" section.

### 2c — Prioritized fix list

Combine automated + manual findings into a prioritized list:

```markdown
## Fix Priority

### P0 — Blockers (must fix before any user touches this)
1. <fix> — <why it blocks>
2. <fix> — <why it blocks>

### P1 — High impact (fix in current sprint)
3. <fix> — <impact>
4. <fix> — <impact>

### P2 — Medium impact (fix soon)
5. <fix> — <impact>

### P3 — Polish (fix when convenient)
6. <fix> — <impact>
```

### Gate: Audit review

Present the audit to the person. They confirm priorities. P0 fixes are non-negotiable.

Output of Phase 2: **Audit report** — `design/AUDIT.md` with automated + manual findings + prioritized fix list.

## Phase 3 — Design System

Goal: define the visual and interaction foundation that every component inherits. Accessible by construction, not by patching.

### 3a — Color system

- **Base palette:** primary, secondary, accent, neutral, semantic (success, warning, danger, info)
- **Contrast verification:** every color pair used for text/UI must meet WCAG contrast:
  - Normal text: 4.5:1 minimum
  - Large text (18pt+/14pt bold+): 3:1 minimum
  - UI components and graphics: 3:1 minimum
  - AAA target: 7:1 normal, 4.5:1 large
- **Dark mode:** same contrast rules apply. Don't just invert — verify independently.
- **State colors:** hover, focus, active, disabled — each needs contrast verification
- **Focus indicator:** 3:1 contrast against adjacent colors, minimum 2px thickness (or use `:focus-visible` with custom ring)

Document in `design/COLORS.md` with hex values + contrast ratios verified.

### 3b — Typography scale

- **Font family:** system stack or chosen font. Verify legibility at small sizes.
- **Scale:** defined steps (e.g., 12, 14, 16, 18, 20, 24, 30, 36, 48px)
- **Line height:** 1.5 for body text (WCAG 1.4.12)
- **Paragraph spacing:** 1.5x font size between paragraphs (WCAG 1.4.12)
- **Resizable:** uses rem (not px) so browser zoom works
- **Contrast:** all text colors verified against backgrounds

### 3c — Spacing & layout

- **Spacing scale:** consistent steps (4, 8, 12, 16, 24, 32, 48, 64)
- **Touch targets:** minimum 44x44px (WCAG 2.5.5 AAA, but aim for it at AA)
- **Spacing between interactive elements:** enough to prevent accidental activation

### 3d — Interaction patterns

- **Focus management:** where focus goes on page load, after action, after modal close
- **Keyboard shortcuts:** document any shortcuts (don't conflict with browser/AT shortcuts)
- **Announcements:** what gets announced via aria-live and when
- **Loading states:** what the user sees during async operations
- **Error states:** how errors are displayed, announced, and recovered
- **Empty states:** what the user sees when there's no data

### 3e — Component inventory

List every component the product needs. For each:
- Name
- Purpose
- ARIA pattern (from WAI-APG)
- States (default, hover, focus, active, disabled, error)
- Keyboard interactions
- Accessibility considerations

Reference: `projects/accessible-ui/` has headless implementations of Combobox, Modal, Tabs following WAI-APG.

Output of Phase 3: **Design system** — `design/DESIGN-SYSTEM.md` + `design/COLORS.md` + component inventory.

## Phase 4 — Implementation

Goal: build the accessible UI. This is where specs become components.

### 4a — Component implementation principles

Every component follows these rules (no exceptions):

1. **Semantic HTML first** — use the right element before reaching for ARIA. A `<button>` is better than `<div role="button">`.
2. **ARIA only when needed** — ARIA supplements, doesn't replace, semantics. If HTML does it, don't add ARIA.
3. **Keyboard by default** — every interactive element must be operable by keyboard. Test before shipping.
4. **Focus visible** — every interactive element has a visible focus indicator. Use `:focus-visible` for smart rings.
5. **Labels everywhere** — every input, button, icon, image has an accessible name. No "click here" links.
6. **Live regions for dynamic content** — status messages, errors, loading states use `aria-live` appropriately.
7. **Reduced motion** — respect `prefers-reduced-motion`. No essential information conveyed by motion alone.
8. **Color is not the only signal** — never rely on color alone. Add icons, text, or patterns.

### 4b — Implementation patterns by component type

**Buttons & links:**
- Use `<button>` for actions, `<a>` for navigation. Never swap.
- Disabled state: `aria-disabled` + visual + prevent action. Don't use `disabled` attribute if the button needs to be announced.
- Icon-only buttons: always have `aria-label`.

**Forms:**
- Every input has a `<label>` (visible or sr-only if visual label is impossible).
- Error messages: `aria-describedby` linking input to error, `aria-invalid="true"`, announced via `aria-live`.
- Required fields: `aria-required="true"` + visual indicator (asterisk + text "required").
- Group related fields with `<fieldset>` + `<legend>`.
- Instructions before the input, not after.

**Modals/Dialogs:**
- `role="dialog"` + `aria-modal="true"` + `aria-labelledby` pointing to the title.
- Focus trap: focus stays inside modal while open.
- Focus return: focus returns to trigger element on close.
- Escape key closes.
- Background inert: `inert` attribute on everything behind the modal.

**Navigation:**
- `<nav>` with `aria-label` if there are multiple navs.
- Skip link: "Skip to main content" as the first focusable element.
- Current page indicator: `aria-current="page"`.
- Breadcrumbs: `<nav aria-label="Breadcrumb">` with `<ol>`.

**Data tables:**
- `<table>` with `<caption>`, `<thead>`, `<tbody>`.
- Scope attributes: `scope="col"` / `scope="row"` on headers.
- Sortable columns: `aria-sort` on headers.
- Complex tables: use `headers` attribute to associate cells.

**Dynamic lists/feeds:**
- `aria-live` region for additions.
- `role="feed"` for scrollable content feeds.
- Load more: button at bottom, announced when new content loads.

**Tabs:**
- Follow WAI-APG Tabs pattern (reference: `projects/accessible-ui/src/components/tabs/`).
- `role="tablist"`, `role="tab"`, `role="tabpanel"`.
- `aria-selected`, `aria-controls`, `aria-labelledby`.
- Keyboard: Arrow keys to move between tabs, Tab to move to panel.

**Combobox/Autocomplete:**
- Follow WAI-APG Combobox pattern (reference: `projects/accessible-ui/src/components/combobox/`).
- `role="combobox"`, `aria-expanded`, `aria-controls`, `aria-activedescendant`.
- Listbox with `role="listbox"` + `role="option"` + `aria-selected`.

**Toast/Notifications:**
- `role="status"` or `role="alert"` depending on urgency.
- `aria-live="polite"` for non-urgent, `aria-live="assertive"` for urgent.
- Auto-dismiss with a delay, but provide a manual close button.

### 4c — Test every component

Three layers (same as `projects/accessible-ui/`):

1. **Rendering test:** correct ARIA roles, attributes, DOM structure
2. **Keyboard test:** `@testing-library/user-event` drives the APG keyboard sequences
3. **Axe test:** `jest-axe` asserts zero violations on rendered output

```typescript
// Example test structure
import { render } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe } from 'jest-axe'
import { Modal } from './Modal'

describe('Modal', () => {
  it('renders correct ARIA structure', () => { ... })
  it('traps focus while open', () => { ... })
  it('returns focus on close', () => { ... })
  it('closes on Escape', () => { ... })
  it('has no axe violations', async () => {
    const { container } = render(<Modal open>...</Modal>)
    expect(await axe(container)).toHaveNoViolations()
  })
})
```

### 4d — Page-level implementation

For each page/view:
1. **Landmark structure:** `<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>` — one `<main>` per page
2. **Heading hierarchy:** one `<h1>` per page, logical hierarchy (no skipping levels)
3. **Skip link:** first focusable element, visible on focus
4. **Document title:** meaningful, updated on navigation
5. **Language:** `lang` attribute on `<html>`, `lang` on content in other languages
6. **Viewport meta:** responsive, `user-scalable=yes` (never disable zoom — WCAG 1.4.4)

### Gate: Implementation review

Before marking implementation done:
- [ ] All components have tests (rendering + keyboard + axe)
- [ ] All tests pass
- [ ] Lint passes
- [ ] Build passes
- [ ] Manual keyboard walkthrough done
- [ ] Screen reader spot-check done (at least one flow)
- [ ] No color-only signals
- [ ] All interactive elements have visible focus
- [ ] All images have alt text (or `alt=""` for decorative)

Output of Phase 4: **Accessible UI** — components built, tested, integrated.

## Phase 5 — Validation

Goal: verify the complete interface meets accessibility standards. This is the final gate before launch.

### 5a — Full automated audit

Run axe-core against the complete interface (all pages, all states):
- Use accessibility-auditor for web-based audit
- Use `@axe-core/playwright` for CI integration
- Target: zero critical + zero serious violations

### 5b — Keyboard-only walkthrough

Navigate the entire product using only keyboard:
- Tab through every page. Logical order?
- Activate every interactive element. Works?
- Escape every container. Works?
- Complete the core user flow. Works end-to-end?
- Complete the auth flow. Works end-to-end?

Document any failures. Fix before proceeding.

### 5c — Screen reader walkthrough

Using VoiceOver (macOS) or NVDA (Windows):
- Navigate the core user flow. Can you complete it?
- Are all elements announced correctly?
- Are dynamic changes (loading, errors, success) announced?
- Are form labels and instructions clear?
- Does the page structure make sense when navigated by headings/landmarks?

### 5d — Visual validation

- **Contrast:** check all text/UI color combinations
- **Zoom 200%:** does the layout still work?
- **Reflow 320px:** does content reflow without horizontal scroll?
- **Reduced motion:** does `prefers-reduced-motion` work?
- **High contrast mode:** does `forced-colors` / Windows High Contrast work?

### 5e — Validation report

```markdown
## Accessibility Validation: <product>

### Automated audit
- Score: <X>/100
- Critical: 0 (target: 0)
- Serious: 0 (target: 0)
- Moderate: <n> (documented, scheduled for fix)
- Minor: <n> (documented, scheduled for fix)

### Keyboard walkthrough
- <page>: PASS
- <page>: PASS
- <flow>: PASS

### Screen reader walkthrough
- <flow>: PASS
- <page>: PASS

### Visual validation
- Contrast: PASS (all pairs verified)
- Zoom 200%: PASS
- Reflow 320px: PASS
- Reduced motion: PASS
- High contrast: <PASS/FAIL>

### Verdict: ✅ MEETS WCAG 2.2 AA / ⚠️ MEETS WITH EXCEPTIONS / ❌ DOES NOT MEET

### Exceptions (if any)
- <criterion> — <why it's not met> — <compensatory measure or roadmap>
```

### Gate: Launch readiness

Present the validation report. The person decides:
- **✅ Meets** → clear to launch
- **⚠️ Meets with exceptions** → launch if exceptions are documented and scheduled
- **❌ Does not meet** → fix before launch, no exceptions

Output of Phase 5: **Validation report** — `design/VALIDATION.md`.

## Integration with other skills

### With product-orchestrator

product-orchestrator calls this skill at two points:
1. **After Definition (Phase 2):** UX discovery + a11y requirements feed into the product definition
2. **After Implementation (Phase 4):** validation gate before launch

```
product-orchestrator
  → Phase 2 (Definition)
    → ux-a11y-studio Phase 1 (Discovery) — feeds a11y requirements back
  → Phase 4 (Orchestration)
    → web-app-builder (scaffold)
    → dev agents (build features)
    → ux-a11y-studio Phase 3-5 (design system, implement UI, validate)
  → Phase 5 (Launch) — only after ux-a11y-studio validation passes
```

### With web-app-builder

web-app-builder produces the scaffold. ux-a11y-studio then:
- Adds `design/` directory with all design system files
- Reviews the generated route structure for a11y (landmarks, heading hierarchy, skip link)
- Adds base accessibility setup (skip link, focus management, reduced motion support)

### With sdd-brownfield

For existing products, sdd-brownfield writes specs. ux-a11y-studio:
- Audits the existing interface (Phase 2)
- Writes a11y requirements into the specs
- Reviews delta specs for accessibility implications

### With agent-review

agent-review gates output quality. ux-a11y-studio provides the a11y checklist that agent-review uses when reviewing UI code.

## Design files

All design work lives in `design/` within the project:

- `DISCOVERY.md` — user context, a11y requirements, heuristic baseline (Phase 1)
- `AUDIT.md` — automated + manual audit findings + fix priority (Phase 2)
- `DESIGN-SYSTEM.md` — typography, spacing, interaction patterns, component inventory (Phase 3)
- `COLORS.md` — color palette with verified contrast ratios (Phase 3)
- `COMPONENT-SPECS.md` — per-component ARIA pattern, states, keyboard interactions (Phase 3)
- `VALIDATION.md` — final accessibility validation report (Phase 5)

## Anti-patterns

- **A11y as afterthought:** "let's add accessibility at the end" — no. It's a constraint from Phase 1. Fixing it later costs 10x more.
- **Automated-only audit:** "axe-core says zero violations, we're accessible" — automated catches ~30-40%. Manual testing is mandatory.
- **ARIA overuse:** adding ARIA to everything "to be safe" — ARIA on semantic HTML is noise. Use it only when HTML doesn't cover the case.
- **Color-only signals:** "red means error" — not for colorblind users. Always add text or icon.
- **Disabled zoom:** `maximum-scale=1.0` — never. WCAG 1.4.4 requires zoom support.
- **Invisible focus:** removing `outline` without replacing it — focus must always be visible.
- **Placeholder as label:** using `placeholder` instead of `<label>` — placeholder disappears on input, fails screen readers.
- **No reduced motion:** animations that can't be disabled — respect `prefers-reduced-motion`.
- **Skip gate on "small" changes:** "it's just a button change, no need to re-audit" — small changes break a11y too. Run the gate.
- **Test components in isolation only:** components pass axe in Storybook but fail in context — always test the full page too.

## Reference projects

- `projects/accessibility-auditor/` — automated audit platform (Playwright + axe-core, scoring, PDF reports)
- `projects/accessible-ui/` — headless accessible component library (Combobox, Modal, Tabs — WAI-APG compliant, jest-axe tested)

## Lessons learned

(this section will be populated with real lessons from UX/a11y work)
