---
name: "umbrawriter-oss-v01-ai-copilot-structure"
description: "Primer OpenSpec para UmbraWriter OSS, estructura limpia desde cero eliminando legacy. Abordaje OpenSpec-first con documentación primero."
---

# UmbraWriter OSS v0.1 — AI Copilot Structure

## 🎯 Executive Summary

**UmbraWriter OSS (Open Source)** representa la primera iteración limpia de nuestra plataforma de escritura asistida por IA, eliminando completamente el legacy code del ecosistema comercial previo (@replit, Vite, Lovable). Este proyecto nace con una filosofía clara: **OpenSpec-first architecture**, donde cada decisión se documenta antes que cualquier implementación.

## 📐 Scope & Vision

### Vision
Crear un sistema de escritura asistida por IA para desarrolladores y creativos que integre profundamente el flujo de trabajo del desarrollador con copilotos contextuales, mientras mantiene la capacidad narrativa esencial.

### Target Audience
- **Primary:** Productores técnicos y devs fullstack que necesitan documentar historias técnicas mientras escriben
- **Secondary:** Escritores criativos que trabajan con terminología técnica (sci-fi tech, cyberpunk)
- **Tertiary:** Equipos de desarrollo que necesitan narración como herramienta de colaboración

## 🏗 Architecture Decision Record (ADR-001: Clean Start)

| Field | Value |
|-------|--------|
| Status | approved |
| Decision | Start from zero with OpenSpec structure |
| Driver | Gonzo's critical validation decision |
| Date | 2026-07-17 |

### ADR-001: Clean Workspace First

**Context:**
Legacy code de UmbraWriter (v0.0 - v0.4) contaba con deuda técnica acumulada desde plataformas comerciales. Gonzo decidió eliminar todo el legacy para construir desde cero con estructura OpenSpec-ready.

> "umbrawriter-oss es un asco" → Clean start, no legacy baggage

**Decision:**
1. Eliminar TODO legacy code (@replit/Vite/Lovable artifacts)
2. Estructura de carpetas basica pero documentada desde el dia uno
3. Cada feature inicia con spec-as-built antes del implementation
4. Git history como registro histórico de decisiones, no solo de commits

**Alternatives Considered, Rejected:**
- **Option A (Keep & Refactor):** Mantener estructura existente y refactorizar → 6 meses de work, deuda técnica persiste
- **Option B (Incremental Migration):** Migrar modulo a modulo → Deuda acumulada en transición, no resuelto
- **Option C (Start Clean):** Decisión actual — cero legacy, todo documentado desde el principio

**Consequences:**
- ✅ Ventajas: Arquitectura limpia, decisiones bien documentadas, history legible
- ⚠️ Desafíos: Tiempo inicial mayor (W0 = 45min), curva de aprendizaje para team si se multiplica
- 🎯 Trade-off: Short-term time for long-term clarity

## 📂 Proposed Structure

```
umbrawriter-oss/
├── docs/                           # OpenSpec source of truth
│    ├── ADRs/                     # Architecture Decision Records
│    │   └── ADR-001-canvas-clean-start.md
│    ├── BRIEF.md                   # Producto vision & scope
│    ├── OPENSTRUCTURE.md           # OpenSpec structure definition
│    └── LEARNINGS.md               # Session lessons
│
├── spec/                          # Active specs (as-built)
│    ├── 00-canvas-clean-start.md   # Canvas structure
│    └── [future-specs]/             # New specs as they're created
│
├── src/                            # Implementation (spec-first approach)
│    ├── core/                      # Core engine layers
│    │   ├── canvas/                # React canvas system
│    │   ├── editor/                  # WYSIWYG + Markdown support
│    │   └── copilot/                 # AI interaction layer
│    ├── features/                    # Feature modules
│    │   ├── markdown-export/        # DOCX, MD export
│    │   ├── co-writing/              # Multi-user session sharing
│    │   └── analytics/               # Usage insights
│    └── shared/                     # Shared types, utils
│
├── templates/                       # Starter kits for new features
│    └── openspec-init-template/
│        ├── .hbs                    # Spec template
│        └── package.json            # Spec metadata
│
├── tests/                           # Test suite
│    ├── unit/                       # Unit tests (Vitest)
│    ├── integration/                 # Integration specs
│    └── e2e/                        # E2E scenarios
│
├── packages/                        # Peer dependencies
│    ├── @umbra/canvas-core/         # Core canvas engine
│    └── @umbra/editor-utils/        # Editor utilities
│
├── scripts/                         # Build & CI scripts
│    ├── build.spec.js               # Spec generation
│    └── lint.docs.ts                # Docs validation
│
└── README.md                       # Project overview
```

## 🔑 Key Principles

1. **Spec First, Code Second**: Every feature starts with documented spec before implementation
2. **ADR as Commit**: Architecture decisions logged in docs/ADRs/ before code changes
3. **Clean History**: Git commits describe DECISIONs, not just CHANGES
4. **No Silent Tech Debt**: Every decision tracked, every trade-off documented

## 🚀 Implementation Plan (Phased)

### Phase 0 (Today - W0)
- [ ] Create OpenSpec structure (docs/, spec/, src/)
- [ ] Write ADR-001-canvas-clean-start.md (this spec as-built)
- [ ] Set up basic Git structure with proper commits
- [ ] Establish OpenSpec workflow in team

**Status:** 🟢 In Progress — Current Session (2026-07-17)

### Phase 1 (W1 - Next Sync)
- [ ] Implement 00-canvas-clean-start spec
- [ ] Add AI Copilot integration skeleton
- [ ] Set up testing infrastructure (Vitest, E2E)
- [ ] Document first feature fully as spec

**Dependencies:** ADR-001 structure established

### Phase 2+ (Ongoing)
- [ ] PRs to Tier 0 repos (TBD after community adoption)
- [ ] Community feedback integration via OpenSpec reviews
- [ ] Multi-user session features
- [ ] Advanced copilot workflows

## 📊 Metrics & Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Specs Created / Docs | 1 per feature before code | docs/ADRs count |
| Clean Commits (no "fix" commits) | >95% of history | Git log analysis |
| Feature completion time | -30% vs legacy approach | Sprint tracking |

## 🎓 Lessons Learned

1. **Clean workspace first > legacy code** — Gonzo confirmed 10/10 confidence
2. **Document before coding** — OpenSpec-first reduces rework by eliminating unclear decisions
3. **Git history as decision log** — Commits describe WHY, not just WHAT

## 📅 Next Steps

- [ ] Current session: Finish ADR-001 documentation
- [ ] Gonzo validation: Confirm architecture decision
- [ ] W1 meeting: Implement first spec (canvas structure)

---

*Created: 2026-07-17 by Kanam AI*  
*Status: pending review — Gonzo to confirm ADR-001*
