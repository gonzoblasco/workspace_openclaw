# Kanam Product Pipeline

> **Pipeline real para los 5 skills de Grupo 1: Product Management & Strategy**
> 
> *Ejecución secuencial - Cada skill feedea la siguiente*

## 📊 Visualización del Pipeline

```mermaid
graph TD
    A[Idea / Opportunity] --> B{profile-positioning}
    B -->|Audit perfil/prod | C{Product-Feasibility?}
    
    C -->|Go| D[product-orchestrator: Evaluate]
    D -->|Evaluate market/viability/fit| E{Go/No-Go Gate 1}
    
    E -->|Go| F[sdd-brownfield: Define Specs]
    F -->|OpenSpec as-built| G[umbrawriter-oss-v01-ai-copilot-structure: Structure Docs]
    G -->|Structure docs (BRIEF/DEF/EVAL/ROADMAP)| H{Go to Build?}
    
    H -->|Yes| I[adr-framework: ADRs iniciales]
    I --> J[product-reset: Start Foundation Phase]
    J --> K[Execute Product with full stack]
    
    L{Post-Launch?} -->|No| J
    L -->|Yes| M[product-orchestrator: Growth/Reset Phase]
    M --> N[product-reset: Growth/Sustainability]
    N --> O[adr-sync: Sync decisions]
```

---

## 🎯 Skill Roles en el Pipeline

### 1️⃣ **profile-positioning** — Fase 0: Discovery & Audit
**Entrada:** Idea, opportunity, o feedback del mercado  
**Output:** Evaluación de viabilidad y fit estratégico  
**Decision Gate:** ¿Vale la pena invertir tiempo?

```bash
gh pr list --author gonzoblasco --state open <repo>
# Example: Check OSS contributions as market signal
```

---

### 2️⃣ **product-orchestrator** — Fase 1: Evaluation
**Entrada:** Producto potencial (ya sea internal o externo)  
**Output:** Evaluación completa con Go/No-Go gates  
**Workflow:**
1. Evaluar idea contra mercado actual
2. Definir MVP mínimo viable (10 features max)
3. Priorizar roadmap en 11 fases (~30 días/fase)
4. Establecer go/no-go gates

```bash
# Example: Evaluate new product for SoporteML v2
azd ai agent create --name "Product Eval"
```

---

### 3️⃣ **sdd-brownfield** — Fase 2: Definition & Specs
**Entrada:** Approved from product-orchestrator  
**Output:** OpenSpec specs as-built documentando lo que vamos a construir  
**Key Deliverables:**
- `BRIEF.md` — Requirements del producto
- `DEFINITION.md` — Arquitectura técnica y decisiones
- `EVALUATION.md` — Competitive analysis + diferenciales
- `ROADMAP.md` — 11 fases con ~30 días cada una

```bash
# Example: Define specs for BrainWeb v2
create-openspec --mode as-built --file "docs/BRIEF.md"
```

---

### 4️⃣ **ai-copilot-structure** (ex: umbrawriter-oss-v01-...) — Fase 3: Structure Docs
**Entrada:** Specs from sdd-brownfield  
**Output:** Estructura documentada formal con OpenSpec  
**Deliverables:**
- `BRIEF.md` (formal)
- `DEFINITION.md` (architected)
- `EVALUATION.md` (competitive analysis)
- `ROADMAP.md` (phased rollout plan)

```bash
# Example: Structure BrainWeb docs
create-with-ai --mode structure --input BRIEF.md
```

---

### 5️⃣ **adr-framework** — Fase 4: ADRs Foundation
**Entrada:** Technical decisions from specs  
**Output:** ADR series documentando decisiones técnicas  
**Workflow:**
1. Leer decisiones de sdd-brownfield y ai-copilot-structure
2. Crear ADRs para decisiones técnicas críticas
3. Establecer baseline para future changes

```bash
# Example: Create ADR for Biome vs ESLint choice
cat > docs/ADR-001.md << EOF
# ADR 001: Use Biome instead of ESLint

**Status:** Accepted  
**Deciders:** Gonzo  
**Date:** 2026-07-19  

## Decision
Use Biome for all code formatting and linting in CreateStackNext.

## Context
ESLint is slow, especially on large codebases. We need faster iteration.

## Consequences
- Faster CI/CD
- Better DX
- Single toolchain
EOF
```

---

### 6️⃣ **product-reset** — Fase 5: Execution & Reset
**Entrada:** Full product definition ready  
**Output:** Foundation phase execution plan + growth strategy  
**Phases (5 fases):**
1. **Fundación**: Scaffold base, core features, auth flow
2. **Visibilidad**: Deploy MVP, basic marketing, PR showcase
3. **Adopción**: User feedback loop, feature unlock based on usage
4. **Comunidad**: Open source contributions, maintainer relationships
5. **Sostenibilidad**: Scale infrastructure, revenue model

```bash
# Example: Start Foundation phase for BrainWeb v2
product-reset --mode foundation --plan "docs/ROADMAP.md"
```

---

### 7️⃣ **product-orchestrator** (Phase 2) — Post-Launch: Growth & Strategy
**Entrada:** Product launched, metrics collected  
**Output:** Growth strategy or reset pivot decision  
**Workflow:**
1. Analyze post-launch metrics
2. Evaluate user feedback
3. Decide: continue growth or pivot (use product-reset)
4. Prioritize next 5 phases

---

### 8️⃣ **product-reset** (Phase 6) — Growth & Sustainability
**Entrada:** Product matured, metrics stable  
**Output:** Sustaining operations plan + sustainability strategy  
**Workflow:**
1. Scale infrastructure based on usage patterns
2. Implement retention features
3. Plan for revenue/sustainability
4. Prepare for product evolution

---

### 9️⃣ **adr-sync** — Continuous: Sync Decisions
**Entrada:** Product changes, feature additions, resets  
**Output:** Updated ADRs reflecting current state  
**Workflow:**
1. Monitor all previous ADRs
2. Detect context changes
3. Create sync ADRs for new decisions/decisions not made
4. Archive obsolete ADRs

```bash
# Example: Sync ADR after BrainWeb v2 feature addition
adr-sync --mode sync --file "docs/ADR-015.md"
```

---

## 🔄 Feedback Loops

### Loop 1: Product Reset Trigger
```
product-reset detected → adr-framework update → adr-sync create sync ADR → resume pipeline at phase N+1
```

### Loop 2: OSS Contribution Signal
```
profile-positioning detect high-engagement project → feed back to product-orchestrator for evaluation
```

---

## 📝 Next Steps

[ ] **Create initial ADR series** (ADR-001 to ADR-010) covering:
    - Biome vs ESLint choice
    - OpenSpec integration pattern
    - Product reset criteria
    - Growth strategy triggers

[ ] **Define 11-phase template** for product-reset with configurable phases

[ ] **Create orchestration prompt** combining all 5 skills in sequence

[ ] **Test pipeline live** on BrainWeb v2 or SoporteML v2

---

## 🧩 Integration Summary

| Pipeline Stage | Skills Involved | Primary Output |
|----------------|-----------------|----------------|
| Discovery & Audit | `profile-positioning` | Viability assessment |
| Evaluation | `product-orchestrator` | MVP definition + Go/No-Go gates |
| Definition | `sdd-brownfield` | OpenSpec specs as-built |
| Structure | `ai-copilot-structure` | Formal structure docs |
| Foundation | `adr-framework`, `product-reset` | ADRs + foundation plan |
| Growth Strategy | `product-orchestrator`, `product-reset`, `adr-sync` | Multi-phase strategy + sync updates |

---

## 🎯 Pipeline en Acción — BrainWeb v2 Caso

```bash
# Step 1: profile-positioning audit for BrainWeb v2 opportunities
profile-positioning --target "BrainWeb" --analyze oss-contributions

# Step 2: product-orchestrator evaluates viability
product-orchestrator --evaluate "BrainWeb v2" --mvp features=10 --phases=11

# Step 3: sdd-brownfield defines specs as-built
sdd-brownfield --mode as-built --project "BrainWeb-v2" --output "docs/specs/"

# Step 4: ai-copilot-structure formalizes structure
ai-copilot-structure --input "$(path docs/specs/BRIEF.md)" --output "docs/structure/"

# Step 5: adr-framework creates technical decisions
adr-framework --create --source "$(path docs/structure/DEFINITION.md)"

# Step 6: product-reset starts foundation execution
product-reset --mode foundation --trigger "spec-complete" --plan "docs/ROADMAP.md"

# Phase 7, 8, 9: Post-launch strategy and syncs as needed...
```

---

*Last Updated: 2026-07-19*  
*Maintainer: Kanam Pipeline Team*  
*Status: 🟢 Ready for Execution*
