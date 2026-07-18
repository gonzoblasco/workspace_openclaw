# accessible-ui — Roadmap

## Timeline (v1.0 → v2.0)

| Phase | Target | Duration | Status |
|-------|--------|----------|--------|
| F0 | Scaffold + ADRs base | 2h | ✅ Done |
| F1 | Components core | 4-6h | In Progress |
| F2 | Testing layer | 3h | Pending |
| F3 | Docs | 1h | Pending |
| F4 | CI/CD + npm publish | 2h | Pending |

## Phase Milestones

### Phase 0: Foundation (✅)

- [x] ADR-001: Regeneración completa decision documentada
- [x] BRIEF.md: Product definition
- [x] EVALUATION.md: Competitor analysis + positioning
- [x] DEFINITION.md: Technical specs + API contracts
- [x] Clean code/ scaffold (React 19 + TS + Vite)

### Phase 1: Core Components (Next)

#### Combobox Priority
- [ ] Full implementation with ARIA compliance
- [ ] Focus management: Enter/Space toggle, ArrowUp wrap
- [ ] Debounced filter (300ms)
- [ ] Tests: rendering, keyboard, axe violations

#### Modal Priority
- [ ] Focus trap implementation
- [ ] ESC + click outside close
- [ ] ARIA roles: role="dialog", aria-modal="true"
- [ ] Tests with user-event

#### Tabs Priority
- [ ] Manual activation (arrows only move focus)
- [ ] Keyboard navigation: Home/End/Switch direction
- [ ] Live region announcements
- [ ] Tests with axe-core audit

### Phase 2: Testing Integration

| Test Layer | Tool | Target Coverage |
|------------|------|-----------------|
| rendering | Vitest + @testing-library/react | ARIA attributes 100% |
| keyboard | user-event | WAI-APG sequences 100% |
| axe audit | jest-axe | Zero violations |

### Phase 3: Documentation

- [ ] Full component docs (Storybook)
- [ ] Accessibility guidelines per APG pattern
- [ ] Keyboard navigation deep dive
- [ ] ARIA reference card

### Phase 4: CI/CD & Release

| Task | Status |
|------|--------|
| GitHub Actions workflows | Pending |
| npm publish (@gonzoblasco/) | Pending |
| Storybook deploy (storybook.dev.sh) | Pending |

## v1.1.0: Auto-Reflection (Next After v1.0)

| Feature | Desc | Priority |
|---------|------|----------|
| Self-documenting components | Components that generate their own docs from source | Low |
| Theme integration hooks | Dark mode, color contrast helpers | Medium |
| Storybook auto-examples | Generate stories from component API | High |

## v2.0.0: Ecosystem (3 months out)

| Feature | Desc | Status |
|---------|------|--------|
| Plugin system | Extend with new WAI-APG patterns | New |
| Shared test utilities |axe-core assertions library | Pending |
| Storybook adapter 2.0 | Native integration story blocks | In Scope |

## Success Metrics (v1.0)

- ✅ **Zero axe violations** on core components
- ✅ **100% keyboard tested** per WAI-APG pattern table
- ✅ **npm publish ready** (@gonzoblasco/accessible-ui scope)
- ✅ **Docs 1:1** with source code (Storybook matches implementation)

## Notes

This roadmap is generated as part of the Phase 0 regeneration effort. The timeline is realistic for one developer (2-3h per phase). Actual dates TBD once first component shipped.

---

Generated: 2026-07-17  
By: ADR-001 regeneration process  
Status: **Phase 0 Complete, Phase 1 Ready**
