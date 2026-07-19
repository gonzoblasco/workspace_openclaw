---
name: "a11y-system-designer"
description: "WCAG 2.2 design system builder with Kanam brand integration, auto-generate WAI-APG compliant components from patterns."
---

# A11y System Designer Skill Proposal

## Summary
Create a skill that auto-generates 100% WCAG 2.2 compliant components with Kanam brand integration, extending accessible-ui from 3 to 10+ WAI-APG pattern components while maintaining headless architecture.

## Problem Statement
Current accessible-ui has Combobox/Modal/Tabs but needs expansion for complete WAI-APG coverage. Developers need systematic WCAG verification, automated ARIA export, design tokens management, and full keyboard test suites beyond 52 existing edge case tests.

## Solution
Skill orchestrates audit-wcag→generate-component→test-accessibility→export-aria workflow automatically. Enables Kanam to auto-generate missing WAI-APG patterns (Navigable/TransferPattern/Listbox/Image/Table) with brand token integration.

## Implementation Pipeline

### Phase 0: Foundation (Week 1)
Define brand tokens (colors, typography, spacing, focus states); create WCAG 2.2 compliance rubric JSON schema; build auto-audit scanner for common violations.

### Phase 1: Expansion (Weeks 2-3)
Auto-generate missing WAI-APG components with Navigable/TransferPattern/Listbox/Image/Table patterns.

### Phase 2: Integration (Weeks 4-5)
Export ARIA semantics to standardized JSON format; create focus management chains between components.

### Phase 3: Production (Weeks 6-8)
Publish @gonzoblasco/accessible-ui v2.0 with 10+ components; integrate as default dep in create-with-ai scaffolding.

## Success Criteria
Zero WCAG 2.2 violations; 100% keyboard-navigable; standardized ARIA export; full WAI-APG coverage implemented.

## Status
PENDING_CREATION — Skill creation pending approval
