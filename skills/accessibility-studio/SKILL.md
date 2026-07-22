---
name: "accessibility-studio"
description: "Accessibility design, audit, autofix, and validation for digital products."
---

# Workflow: Accessibility Studio

## What it does

Design, audit, correction, and validation of accessibility in digital products. Includes autofix loop (audit → correct → verify) and granular WCAG 2.2 checklist.

## Phases

### 1. Discovery
Users with disabilities, needs, usage context.

### 2. Audit — WCAG 2.2
Specify target conformance level (A, AA, AAA) at the start.

**Automated:** axe-core, Lighthouse, WAVE
**Manual:** keyboard navigation, screen reader, cognitive, visual

Checklist by principle:

**Perceivable**
- Text contrast ≥ 4.5:1 (3:1 for large text) — 1.4.3
- Interactive component contrast ≥ 3:1 — 1.4.11
- Descriptive alt text on images — 1.1.1
- Information not conveyed by color alone — 1.4.1

**Operable**
- Full keyboard navigation — 2.1.1
- Visible focus on all interactive elements — 2.4.7
- Logical tab order (left→right, top→bottom) — 2.4.3
- Touch targets ≥ 24×24px (prefer 44×44px) — 2.5.8
- No keyboard traps in modals, dropdowns — 2.1.2

**Understandable**
- Visible labels or aria-label on inputs — 3.3.2
- Clear error messages associated with the field — 3.3.1
- Document language defined — 3.1.1

**Robust**
- Semantic HTML (main, nav, button, a) — 4.1.2
- ARIA only when native HTML is insufficient — 4.1.2

### 3. Autofix (loop audit → edit → verify)
Two modes:

**Report Mode:** audit and generate prioritized report without editing files.

**Fix Mode:** for each identified issue:
1. Correct the code
2. Re-audit to confirm the fix
3. Move to the next issue

Prioritize by severity: Critical → Major → Minor.

### 4. Design System
Verified contrast tokens, accessible components with focus, hover, active, disabled states.

### 5. Implementation
Headless components (WAI-APG), 3 test layers: unit, integration, E2E accessibility.

### 6. Validation
Pre-launch, post-change regression, compliance report. If possible, test with real users with disabilities. If not, document limitations.

## Outputs
- WCAG 2.2 audit report with conformance level and severity per issue
- Corrected issues (automatically and manually) with post-fix verification
- Design system with verified contrast
- Accessible components with tests
- Pre-launch accessibility certification
