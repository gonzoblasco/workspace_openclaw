---
name: "ux-a11y-studio"
description: "Equipo de UX/UI + Accesibilidad — discovery de usuarios y requisitos WCAG 2.2, audit (automated axe-core + manual keyboard/screen reader/cognitive/visual), design system con contraste verificado, implementación de componentes accesibles (WAI-APG, 3 capas de tests), validación final antes de launch. Integrado con product-orchestrator y web-app-builder. Design files en `design/`."
---

# UX / A11y Studio — Equipo de Diseño y Accesibilidad

Use when you need to design, audit, or implement accessible user interfaces. This skill covers the full lifecycle: from user research and WCAG requirements to automated audits, manual testing, component implementation, and launch validation.

## When to use

- **Discovery phase:** Define user personas and accessibility requirements for a new feature
- **Audit phase:** Run automated + manual accessibility audits on existing interfaces
- **Design phase:** Create accessible design system components with verified contrast
- **Implementation phase:** Build headless accessible components following WAI-ARIA APG
- **Validation phase:** Final accessibility check before launch

## How to invoke

```
@ux-a11y-studio audit <url> — run full accessibility audit
@ux-a11y-studio design <feature> — design accessible component
@ux-a11y-studio implement <pattern> — implement WAI-ARIA pattern
@ux-a11y-studio validate — final pre-launch accessibility check
```

Or reference in a task prompt:
```
Read @ux-a11y-studio and audit the new modal component before merging.
```

---

## Phase 1: Discovery & Requirements

### 1a — User Research

Define who uses the product and their accessibility needs:

- **Visual impairments:** screen reader users, low vision, color blindness
- **Motor impairments:** keyboard-only users, switch device users, voice control
- **Cognitive impairments:** attention, memory, language processing
- **Hearing impairments:** captions, transcripts for audio/video content

### 1b — WCAG Requirements Mapping

Map each feature to WCAG 2.2 success criteria:

| Feature | WCAG Criteria | Level |
|---|---|---|
| Navigation | 2.4.1 Bypass Blocks, 2.4.3 Focus Order, 2.4.5 Multiple Ways | A-AA |
| Forms | 3.3.1 Error Identification, 3.3.2 Labels, 3.3.3 Error Suggestion | A |
| Modals | 2.4.3 Focus Order, 4.1.2 Name/Role/Value | A |
| Data tables | 1.3.1 Info and Relationships | A |
| Color/contrast | 1.4.1 Use of Color, 1.4.3 Contrast (Minimum) | AA |
| Animations | 2.2.2 Pause/Stop/Hide, 2.3.1 Three Flashes | A |
| Touch targets | 2.5.8 Target Size (Minimum) | AA |
| Keyboard | 2.1.1 Keyboard, 2.1.2 No Keyboard Trap | A |

### 1c — Accessibility Statement

Define the target level (WCAG 2.2 AA minimum) and document known limitations.

---

## Phase 2: Audit

### 2a — Automated Audit (axe-core)

Run axe-core on every page/component:

```bash
npx playwright open <url>
# In the console:
axe.run().then(results => console.table(results.violations.map(v => ({
  id: v.id,
  impact: v.impact,
  description: v.description,
  nodes: v.nodes.length,
}))))
```

**Check for:**
- Missing ARIA attributes (`aria-label`, `aria-describedby`, `aria-expanded`)
- Missing form labels
- Insufficient color contrast
- Missing document language
- Missing skip navigation link
- Images without alt text

### 2b — Manual Keyboard Audit

Navigate the entire interface using **only the keyboard**:

| Key | What to test |
|---|---|
| `Tab` | Focus order follows visual order, no traps |
| `Shift+Tab` | Reverse focus works correctly |
| `Enter` / `Space` | Activates buttons, links, form controls |
| `Escape` | Closes modals, menus, dropdowns |
| `Arrow keys` | Navigation within lists, tabs, grids |
| `F6` / `Shift+F6` | Navigation between panes/regions |

**Check for:**
- Visible focus indicator on all interactive elements
- Logical focus order (top-to-bottom, left-to-right)
- No focus traps (focus gets stuck in a component)
- Skip navigation link present and functional

### 2c — Screen Reader Audit

Test with at least one screen reader:

| Screen Reader | Browser | Platform |
|---|---|---|
| VoiceOver | Safari | macOS |
| NVDA | Firefox | Windows |
| JAWS | Chrome | Windows |

**Check for:**
- All content is announced correctly
- Dynamic content changes are announced (aria-live regions)
- Error messages are associated with form fields
- Modal/dialog focus is trapped and restored on close
- Landmarks are properly labeled

### 2d — Cognitive & Visual Audit

- **Zoom:** Test at 200% and 400% zoom — no content should be cut off
- **Reduced motion:** Test with `prefers-reduced-motion` — animations should be reduced or disabled
- **High contrast mode:** Test with Windows High Contrast Mode or forced-colors
- **Color blindness:** Simulate protanopia, deuteranopia, tritanopia
- **Font scaling:** Increase browser default font to 200% — layout should not break

### 2e — Audit Report Format

```markdown
## 🔍 Accessibility Audit — [Page/Component]

### Automated (axe-core)
- ✅ Passes: [N]
- 🔴 Violations: [N] (Critical: [N], Serious: [N], Moderate: [N], Minor: [N])

### Manual Keyboard
- ✅ Focus order: [PASS/FAIL]
- ✅ Focus indicator: [PASS/FAIL]
- ✅ No focus traps: [PASS/FAIL]
- ✅ Skip nav: [PASS/FAIL]

### Screen Reader (VoiceOver/NVDA/JAWS)
- ✅ Content announced: [PASS/FAIL]
- ✅ Dynamic updates: [PASS/FAIL]
- ✅ Error association: [PASS/FAIL]
- ✅ Modal focus: [PASS/FAIL]

### Visual/Cognitive
- ✅ 200% zoom: [PASS/FAIL]
- ✅ Reduced motion: [PASS/FAIL]
- ✅ Color contrast: [PASS/FAIL]
- ✅ Font scaling: [PASS/FAIL]

### 🔴 Blocking Issues
- [Issue description] — [WCAG SC] — [Fix]

### 🟡 Warnings
- [Issue description] — [WCAG SC] — [Recommendation]

### 🛠️ VERDICT
[PASS / FAIL — list blocking issues]
```

---

## Phase 3: Design System

### 3a — Color Palette with Verified Contrast

Every color pair must pass WCAG AA:

| Usage | Foreground | Background | Ratio | Pass |
|---|---|---|---|---|
| Body text | #1a1a2e | #ffffff | 15.3:1 | ✅ AA+ |
| Muted text | #6b7280 | #ffffff | 4.6:1 | ✅ AA |
| Links | #2563eb | #ffffff | 4.8:1 | ✅ AA |
| Error text | #dc2626 | #ffffff | 4.5:1 | ✅ AA |
| Disabled | #9ca3af | #f3f4f6 | 2.1:1 | ❌ (informational only) |

**Tools:** WebAIM Contrast Checker, axe DevTools, Stark plugin

### 3b — Typography Scale

- Minimum body text: 16px (1rem)
- Line height: 1.5 minimum
- Font weight: 400 for body, 600+ for headings
- Max line length: 70-80 characters

### 3c — Focus Indicators

- Visible focus ring on all interactive elements
- Minimum 2px solid outline with 3px offset
- Color: use `outline-color: var(--color-ring)` with sufficient contrast
- Never use `outline: none` without providing an alternative

### 3d — Spacing & Touch Targets

- Minimum touch target: 44x44px (WCAG 2.5.8)
- Spacing between interactive elements: minimum 4px

---

## Phase 4: Implementation (WAI-ARIA APG)

### 4a — Component Architecture

Follow the **headless component pattern**:

```
src/components/<name>/
├── use-<name>.ts          # State hook (pure logic, no DOM)
├── <name>.tsx             # Compound components (ARIA semantics)
├── <name>.test.tsx        # 3-layer tests
└── <name>.stories.tsx     # Storybook with a11y addon
```

### 4b — State Hook Pattern

Extract state management into a custom hook:

```typescript
// use-modal.ts
export function useModal(options?: UseModalOptions): UseModalReturn {
  // Returns: isOpen, open, close, toggle, triggerProps, dialogProps
  // Pure logic — no DOM, no ARIA
}
```

### 4c — Compound Component Pattern

```typescript
// modal.tsx
export function ModalRoot({ children }: { children: ReactNode }) {
  // Provides context from useModal
}

export function ModalTrigger(props: ButtonHTMLAttributes<HTMLButtonElement>) {
  // Renders as a button with aria-expanded, aria-haspopup
}

export function ModalContent(props: DialogHTMLAttributes<HTMLDivElement>) {
  // Renders with role="dialog", aria-modal, aria-labelledby, aria-describedby
  // Manages focus trap, escape to close, restore focus on close
}

export function ModalClose(props: ButtonHTMLAttributes<HTMLButtonElement>) {
  // Renders as a button that calls close()
}
```

### 4d — Three-Layer Testing

Every component must have:

1. **Rendering tests** — correct ARIA roles, attributes, DOM structure
2. **Keyboard interaction tests** — each row in the APG pattern table has a corresponding test
3. **Accessibility audit** — `jest-axe` runs axe-core against rendered output, asserts zero violations

```typescript
// modal.test.tsx — example
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe } from 'jest-axe'

it('renders with correct ARIA attributes', () => {
  render(<ModalRoot><ModalContent>content</ModalContent></ModalRoot>)
  expect(screen.getByRole('dialog')).toHaveAttribute('aria-modal', 'true')
})

it('traps focus on Tab', async () => {
  const user = userEvent.setup()
  render(<ModalRoot defaultOpen><ModalContent>...</ModalContent></ModalRoot>)
  await user.tab()
  // focus should cycle within the modal
})

it('has no axe violations', async () => {
  const { container } = render(<ModalRoot defaultOpen><ModalContent>...</ModalContent></ModalRoot>)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

### 4e — WAI-ARIA APG Patterns Reference

| Component | APG Pattern | Key Behaviors |
|---|---|---|
| Alert Dialog | [Alert Dialog](https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/) | Focus to first focusable, Escape closes, focus restored on close |
| Combobox | [Combobox](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) | aria-autocomplete, aria-activedescendant, list filtering |
| Dialog (Modal) | [Dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | Focus trap, aria-modal, Escape closes, restore focus |
| Tabs | [Tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/) | aria-selected, aria-controls, roving tabindex or arrow keys |
| Tooltip | [Tooltip](https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/) | aria-describedby, hover/focus show, Escape hides |
| Menu Button | [Menu Button](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/) | aria-expanded, aria-haspopup, arrow navigation |
| Disclosure | [Disclosure](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/) | aria-expanded, toggle on click, Enter/Space |
| Breadcrumb | [Breadcrumb](https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/) | nav with aria-label="Breadcrumb", aria-current="page" |
| Carousel | [Carousel](https://www.w3.org/WAI/ARIA/apg/patterns/carousel/) | aria-roledescription="carousel", pause on focus, next/prev buttons |
| Accordion | [Accordion](https://www.w3.org/WAI/ARIA/apg/patterns/accordion/) | aria-expanded, aria-controls, heading buttons |

---

## Phase 5: Pre-Launch Validation

### Checklist

- [ ] Automated audit (axe-core) — zero violations
- [ ] Manual keyboard audit — full navigation without mouse
- [ ] Screen reader test — VoiceOver (macOS) or NVDA (Windows)
- [ ] 200% zoom — no content cut off
- [ ] `prefers-reduced-motion` — animations disabled
- [ ] Color contrast — all text/background pairs pass WCAG AA
- [ ] Focus indicators — visible on all interactive elements
- [ ] Touch targets — minimum 44x44px
- [ ] Form labels — all inputs have associated labels
- [ ] Error messages — associated with form fields via aria-describedby
- [ ] Skip navigation link — present and functional
- [ ] Page title — descriptive and unique
- [ ] Language attribute — `<html lang="...">` set correctly
- [ ] Landmarks — properly labeled (`<nav aria-label="Main">`, `<main>`, etc.)

### Blocking Rules

- Any **automated violation** with Critical or Serious impact → BLOCKING
- **Keyboard trap** anywhere in the interface → BLOCKING
- **Missing form labels** → BLOCKING
- **Insufficient color contrast** on body text → BLOCKING
- **Missing focus indicator** on interactive elements → BLOCKING

---

## Integration

This skill integrates with:
- **product-orchestrator** — called during Phase 2 (Definition) for accessibility requirements, Phase 4 (Orchestration) for audit gates
- **web-app-builder** — accessibility requirements feed into component scaffold decisions
- **agent-review** — supplements the review checklist with accessibility-specific items
- **sdd-brownfield** — accessibility specs should be documented in delta specs

## Design files

Accessibility-related design artifacts go in `design/`:
- `design/a11y-audit-<feature>.md` — audit reports
- `design/a11y-requirements-<feature>.md` — WCAG requirements mapping
- `design/a11y-statement.md` — accessibility statement for the product
