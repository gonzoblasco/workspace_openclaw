---
name: "product-orchestrator"
description: "Product Owner/Manager end-to-end: evalúa ideas, define producto, prioriza MVP, y orquesta las demás skills para llevar productos de idea a deployado."
---

# Product Orchestrator

Use when someone has an idea for a product, service, or feature and needs a Product Owner/Manager to evaluate it, define it, prioritize it, and orchestrate its build end-to-end — from raw idea to deployed product.

This skill is the **brain before the hands**. It does NOT scaffold, code, or deploy. It:
1. Evaluates whether the idea is worth building
2. Defines what to build (and what NOT to build)
3. Prioritizes the MVP
4. Orchestrates the existing skills to execute
5. Tracks progress and iterates

## Scope

This skill sits **above** all other build/dev skills. It's the orchestrator that decides WHAT to build and in WHAT order, then delegates the HOW to the right skill.

### What this skill does
- Product evaluation (market, viability, scope, risks)
- MVP definition and prioritization
- Roadmap creation (phases, milestones, success criteria)
- Skill orchestration (calls web-app-builder, sdd-brownfield, skill-composition, agent-dispatcher, agent-review as needed)
- Progress tracking and iteration decisions
- Go/no-go checkpoints at each phase

### What this skill does NOT do
- Write code (delegated to dev agents)
- Scaffold projects (delegated to web-app-builder)
- Write specs (delegated to sdd-brownfield)
- Review code (delegated to agent-review)
- Make design decisions (delegated to the builder/dev agent)

## Prerequisites

- The other workspace skills installed: web-app-builder, sdd-brownfield, skill-composition, agent-dispatcher, agent-review
- Workspace memory: MEMORY.md, projects/PROYECTOS.md
- Git configured for workspace + project repos

## Phase 0 — Idea Intake

Goal: capture the raw idea and the person behind it.

1. **Listen** — let the person describe the idea in their own words. Don't interrupt, don't structure yet.
2. **Capture** — write it down as a raw statement: "Gonzo quiere un CRM para vendedores de Mercado Libre"
3. **Ask 2-3 context questions** (not an interrogation):
   - ¿Para quién es? (who's the user)
   - ¿Qué problema resuelve? (what pain)
   - ¿Ya existe algo o es desde cero?
   - ¿Es para usar solo, para vender, o ambos?
4. **Record the intake** in a product brief file: `products/<slug>/BRIEF.md`

Output of Phase 0: **Raw Brief** — the idea in plain language + context.

## Phase 1 — Evaluation

Goal: decide if the idea is worth investing time in. This is the gate before any building happens.

### 1a — Market & viability check

- **Problem validation:** is the pain real? How do people solve it today? (manual, spreadsheets, nothing, competitor)
- **Audience size:** how many people have this problem? (rough estimate — 10s, 100s, 1000s, 10000s)
- **Existing solutions:** what's already out there? (direct competitors, adjacent tools, workarounds)
- **Differentiation:** what makes this different? (price, focus, UX, integration, niche)
- **Revenue potential:** can it make money? How? (subscription, one-time, freemium, marketplace cut)

Use `web_search` for quick market checks. Don't do a full research report — 15 minutes max.

### 1b — Technical feasibility

- **Can we build it?** with the current stack (React/TS/Supabase/AI). If not, what's missing?
- **External dependencies:** APIs, services, credentials, data sources needed
- **Complexity estimate:** simple (CRUD + auth), moderate (integrations + AI), complex (realtime, multi-tenant, billing), very complex (marketplace, ML, hardware)
- **Time estimate:** rough — days, weeks, or months for MVP

### 1c — Strategic fit

- **Does it fit the person's goals?** (portfolio, business, learning, client work)
- **Does it fit the ecosystem?** (Kanam products, create-stack-next, existing projects)
- **Opportunity cost:** what are we NOT building if we build this?
- **Synergy:** does it feed other products/projects or stand alone?

### 1d — Verdict

Present the evaluation as a structured verdict:

```markdown
## Product Evaluation: <name>

### Problem
<one paragraph>

### Audience
<who + rough size>

### Existing solutions
<list 2-5, with gap analysis>

### Differentiation
<what makes this different>

### Revenue model
<how it makes money, or "internal tool / no revenue">

### Technical feasibility
<can we build it, what do we need, complexity>

### Time to MVP
<rough estimate>

### Strategic fit
<how it fits goals + ecosystem>

### Risks
- <risk 1 + mitigation>
- <risk 2 + mitigation>

## Verdict: 🟢 GO / 🟡 GO WITH CAVEATS / 🔴 NO-GO

### Conditions (if 🟡)
- <what must be true for this to work>
- <what to validate before investing more>

### Recommendation
<one paragraph: what to do next>
```

### Gate: Verdict review

Present the verdict to the person. They decide:
- **🟢 GO** → proceed to Phase 2 (Definition)
- **🟡 GO WITH CAVEATS** → address conditions first, then decide
- **🔴 NO-GO** → archive the idea in `FREEZER.md` or `products/<slug>/` with the evaluation for future reference

Do NOT proceed without explicit go-ahead. This is the first go/no-go gate.

Output of Phase 1: **Product Evaluation** — verdict + recommendation.

## Phase 2 — Definition

Goal: define what we're building. Concrete, specific, bounded.

### 2a — MVP scope

Define the Minimum Viable Product. Rules:
- **One core value:** the MVP delivers ONE thing well. Not three things okay.
- **3-7 features max:** everything else is post-MVP.
- **Cuts are decisions:** "no auth" is a scope decision. "no billing" is a scope decision. Write them down.
- **Time-boxed:** the MVP should be buildable in the estimated time from Phase 1. If not, cut more.

Format:

```markdown
## MVP Scope: <name>

### Core value
<one sentence: what the user can do that they couldn't before>

### In scope (MVP)
1. <feature> — <why it's essential>
2. <feature> — <why it's essential>
3. <feature> — <why it's essential>

### Out of scope (post-MVP)
- <feature> — <why it can wait>
- <feature> — <why it can wait>

### Explicit non-goals
- <what we're NOT doing and why>
```

### 2b — User personas

1-3 personas max. For each:
- Who they are (role, context)
- What they need
- What they'll do with the product
- What success looks like for them

### 2c — User flows

The main flows from MVP scope. 3-7 flows. For each:
- Trigger (what starts the flow)
- Steps (what the user does)
- Outcome (what they get)
- Error paths (what happens when things go wrong)

### 2d — Success metrics

How we know the MVP worked. 2-5 metrics:
- **Usage:** active users, sessions, actions performed
- **Value:** time saved, tasks completed, revenue generated
- **Quality:** bug reports, crash rate, NPS (if applicable)

Keep it simple. No OKR framework for a solo dev MVP.

### Gate: Definition review

Present the definition to the person. They confirm:
- Scope is right (not too big, not too small)
- Personas match reality
- Flows cover the core value
- Metrics make sense

If they say "también necesito X" and X is big → it goes to post-MVP. If X is small → add it but flag the time impact.

Output of Phase 2: **Product Definition** — MVP scope, personas, flows, metrics.

## Phase 3 — Roadmap & Plan

Goal: turn the definition into an executable plan with phases and milestones.

### 3a — Phase breakdown

Break the MVP into buildable phases. Each phase:
- Has a clear deliverable (something you can show/use)
- Has an estimated effort (hours, days)
- Has dependencies on previous phases
- Has a demo/state at the end

```markdown
## Roadmap: <name>

### Phase 1: <name> — <effort estimate>
- Goal: <what this phase achieves>
- Deliverable: <what exists at the end>
- Tasks:
  1. <task>
  2. <task>
- Demo: <what to show>

### Phase 2: <name> — <effort estimate>
- Goal: ...
- Depends on: Phase 1
- ...

### Post-MVP
- <future feature> — <rough when>
- <future feature> — <rough when>
```

### 3b — Skill mapping

For each phase, identify which skill executes:

| Phase | Skill | Why |
|---|---|---|
| Scaffold + structure | web-app-builder | Goes from idea to ready-to-code |
| Feature specs | sdd-brownfield | Specs for existing project |
| Implementation | agent-dispatcher + dev agents | Code the features |
| Review | agent-review | Gate before merge |
| OSS contribution | oss-contribute | If contributing to external repos |

### 3c — Risk register

Top 3-5 risks with mitigation:
- **Risk:** what could go wrong
- **Impact:** how bad (low/medium/high)
- **Probability:** how likely (low/medium/high)
- **Mitigation:** what we do about it
- **Trigger:** when we know it's happening

### Gate: Plan review

Present the roadmap to the person. They confirm:
- Phases make sense
- Priorities are right
- Time estimates are acceptable
- Risks are acceptable

Output of Phase 3: **Product Roadmap** — phases, skill mapping, risks.

## Phase 4 — Orchestration

Goal: execute the plan by delegating to the right skills at the right time. This is where the product orchestrator becomes a conductor.

### 4a — Kickoff

For the first phase (usually scaffolding):

1. **Prepare the brief** — compile everything from Phases 0-3 into a handoff for the executing skill
2. **Call the skill** — typically `web-app-builder` for new projects, or `sdd-brownfield` for existing ones
3. **Set up tracking** — create `products/<slug>/STATUS.md` to track progress across phases

### 4b — Phase execution loop

For each phase:

1. **Prepare** — gather inputs (previous phase output, specs, brief)
2. **Delegate** — use `skill-composition` to design the pipeline, `agent-dispatcher` to execute
3. **Gate-check** — use `agent-review` criteria to verify the phase output
4. **Update tracking** — mark phase complete in `STATUS.md`, note what happened
5. **Demo** — show the person what exists now
6. **Decide:** proceed to next phase, or iterate on current one

### Tracking format

```markdown
## Product Status: <name>

### Current phase: <phase name>

### Phases
- [x] Phase 1: <name> — ✅ complete, <date>, <what was delivered>
- [ ] Phase 2: <name> — in progress, started <date>
- [ ] Phase 3: <name> — pending

### Decisions log
- <date>: <decision> — <why>

### Blockers
- <blocker> — <status, what's needed>

### Next action
<what needs to happen next, specifically>
```

### 4c — Orchestration patterns

**New product (from scratch):**
```
web-app-builder (scaffold + domain structure)
  → sdd-brownfield (specs for each feature)
    → agent-dispatcher (implement features in priority order)
      → agent-review (gate each feature)
        → deploy + verify
```

**Existing product (new feature):**
```
sdd-brownfield (delta spec for the feature)
  → agent-dispatcher (implement)
    → agent-review (gate)
      → merge + deploy
```

**OSS contribution (external project):**
```
oss-contribute (triage + implement + PR)
  → agent-review (self-review before PR)
    → submit + track
```

**Experimental / uncertain:**
```
spike (validate feasibility)
  → evaluate result
    → if viable: web-app-builder or sdd-brownfield → implement
    → if not viable: archive findings, update roadmap
```

### Gate: Phase completion

Before moving to the next phase:
- [ ] Phase deliverable exists and works
- [ ] Build/lint/tests pass (if applicable)
- [ ] Specs updated (if applicable)
- [ ] STATUS.md updated
- [ ] HANDOFF.md updated (if session might change)

Do NOT skip gates. A phase that's "almost done" is not done.

Output of Phase 4: **Working product** — MVP built phase by phase, tracked, demoed.

## Phase 5 — Launch & Iterate

Goal: ship the MVP and start the feedback loop.

### 5a — Launch checklist

- [ ] Core value works end-to-end
- [ ] Error states handled (not perfect, but not crashing)
- [ ] Basic analytics/logging in place
- [ ] Landing page or explanation exists
- [ ] Onboarding flow works (first-time user can figure it out)
- [ ] Env vars and secrets configured for production
- [ ] Build passes
- [ ] Deploy works

### 5b — Feedback collection

Define how feedback comes in:
- Direct user feedback (conversations, messages)
- Usage data (if instrumented)
- Bug reports
- Self-use observations (if the person is also the user)

### 5c — Iteration planning

After launch (or after enough usage):
1. **Review metrics** from Phase 2d — did we hit the success criteria?
2. **Collect feedback** — what are users saying? What's broken? What's missing?
3. **Prioritize** — bug fixes > missing core features > nice-to-haves > post-MVP
4. **Update roadmap** — move things between MVP and post-MVP based on reality
5. **Decide:** iterate (go back to Phase 2 or 3) or declare MVP done and plan v2

### Gate: MVP retrospective

With the person, review:
- What worked
- What didn't
- What surprised us
- What we'd do differently
- Whether to continue, pivot, or stop

Output of Phase 5: **Launched MVP + iteration plan**.

## Skill catalog (how this skill calls others)

| Situation | Skill called | What it does |
|---|---|---|
| New project from scratch | web-app-builder | Discovery → scaffold → domain structure → handoff |
| Feature in existing project | sdd-brownfield | Delta spec → implement → archive |
| Complex multi-step build | skill-composition | Design pipeline with gates |
| Delegate to subagents | agent-dispatcher | Decompose + assign + spawn |
| Verify output quality | agent-review | Checklist review against brief |
| Contribute to external repo | oss-contribute | Triage → implement → PR → track |
| Validate uncertain approach | spike | Throwaway prototype → verdict |

## Iteration

This skill is inherently iterative:
- **New idea** → start at Phase 0
- **Existing product, new feature** → start at Phase 2 (Definition) with existing context
- **Re-evaluate direction** → start at Phase 1 (Evaluation) with what we've learned
- **Post-MVP planning** → start at Phase 3 (Roadmap) with MVP learnings

## Product files

Each product gets a directory: `products/<slug>/`

- `BRIEF.md` — raw idea + context (Phase 0)
- `EVALUATION.md` — market/viability/strategic evaluation (Phase 1)
- `DEFINITION.md` — MVP scope, personas, flows, metrics (Phase 2)
- `ROADMAP.md` — phases, skill mapping, risks (Phase 3)
- `STATUS.md` — live tracking of progress (Phase 4)
- `RETROSPECTIVE.md` — post-MVP learnings (Phase 5)

These are the product's memory. They persist across sessions.

## Anti-patterns

- **Skipping evaluation:** "I know it's a good idea, let's build it" — no. 15 minutes of evaluation saves weeks of wasted building.
- **MVP creep:** "just one more feature" — every addition is a scope decision. Write it down, decide explicitly.
- **No gates:** proceeding without explicit go/no-go at each phase — the gates exist to catch bad directions early.
- **Over-planning:** spending more time on roadmap than building — Phase 3 should be fast. The roadmap is a plan, not a contract.
- **Solo execution:** trying to do everything in one session — use the skills. Delegate. That's what they're for.
- **No tracking:** if STATUS.md doesn't exist or is stale, you don't know where you are. Update it every phase.
- **Ignoring feedback:** shipping and never looking at usage — the iterate loop (Phase 5) is where products get good.

## Lessons learned

(this section will be populated with real lessons from product orchestration)
