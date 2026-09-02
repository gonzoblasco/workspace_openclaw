# Mini Drill - Ritz-Carlton First Round (02/09 2:00 PM)

**Goal:** 30-40 min before the call. Architecture stories + answers to "how do you work?".
**Context:** Principal Full Stack (React/Next.js, Node, ADRs explicitly in JD, OSS preferred, lean high-ownership, ~50% hands-on / 50% technical direction). $95k-$105k.
**Language rule:** the whole process is in English. All communication (LinkedIn, email, interviews) in English. No Spanish slips - that already happened once (31/08, "ahí desactivé mi proxy").

---

## Part 1 - The 3 architecture stories (10 min)

Compressed STAR format: **Context (1 line) -> Decision (2 lines) -> Why (1 line) -> Result (1 line)**.
Don't tell code. Tell decisions.

### Story 1: SoporteML - Mercado Pago billing audit

- **Context:** multi-tenant CRM for Mercado Libre sellers. The MP billing "was written but never tested".
- **Decision:** audit the 4 Edge Functions against the official MP docs before touching anything. Found 4 real bugs: corrupted token (`***` instead of `Deno.env.get`), `userData` undefined in test mode, missing `notification_url` on preapproval creation (without it the webhook never receives events), and `data.id` from the webhook coming in a query param, not the body.
- **Why:** the rule is to verify against the real source (API/Docs), never assume written code works.
- **Result:** all 4 Edge Functions pass `deno check`, setup guide documented. Billing that actually works, not pretend billing.
- **What it shows:** audit judgment, not trusting existing code, documenting the setup.

### Story 2: react-spectrum #10517 - rework with an Adobe maintainer

- **Context:** my own PR fixing the focus ring on Checkbox/Radio (RAC). Rob Snow (2nd contributor of the repo) asked to replace 4 style props with a named prop and remove the escape hatch.
- **Decision:** full rework: `hiddenInput="stretch-to-label"` across 7 files (+81/-209), tests updated, real browser tests (Chromium + Firefox) as evidence.
- **Why:** the maintainer asked for a cleaner API; iterating with maintainers is part of the job, not an exception.
- **Result:** PR alive, waiting for re-review. Sister lesson: I closed #10487 as unnecessary after verifying against main that the bug was already fixed upstream - and offered the regression test as a separate PR.
- **What it shows:** you can iterate with senior people at Adobe, you take feedback, you verify with evidence (real browser), and you know when a fix is unnecessary (technical honesty).

### Story 3: The work system (the one that matters most)

- **Context:** 9 years frontend, now fullstack. I use AI as infrastructure, not as a chat.
- **Decision:** I built a system: A/B pipeline (one agent writes, another reviews with a critical eye, I verify against the real source), a complexity scorer that decides model and depth before each task, ADRs for every architecture decision, pre-commit hooks (lint -> test -> build) in every project.
- **Why:** AI multiplies output only if there is technical judgment behind it. The model spits out code; the judgment is mine.
- **Result:** merged PRs in MUI, astryx (Facebook), react-spectrum (Adobe); active reviewer in TanStack Query; complete products (SoporteML, kanam-pulse with 118 tests and gated CI).
- **What it shows:** this IS the Principal role. Optimizing a team's output is not "using AI" - it is process engineering.

---

## Part 2 - Answers to "how do you work?" (10 min)

### Question: "How do you use AI in your day to day?"

**Answer (30 sec):**
> "AI is my main tool, but there is a system behind it. For every task I evaluate complexity across 4 dimensions - scope, abstraction, risk, ambiguity - and that decides how I approach it. For code, one agent writes and another reviews with a critical eye, and I verify the result against the real source: the docs, the tests, the browser. The model accelerates; the judgment is mine."

**Trap to avoid:** don't say "AI does the work". Say "AI multiplies my output, the judgment is mine".

### Question: "How do you make architecture decisions?"

**Answer (30 sec):**
> "I document every decision in an ADR: the context, the decision, the alternatives I discarded and why. That forces me to think before coding and gives the team a history of why things are the way they are. If a decision is already documented, it is not reopened without new evidence."

**Why it works here:** the Ritz-Carlton JD explicitly asks for ADRs. It is literally your system.

### Question: "What do you expect from a Principal?"

**Answer (30 sec):**
> "A Principal is ~50% hands-on and 50% technical direction: defining standards, unblocking the team, and making decisions others can execute. My work system - ADRs, review pipeline, pre-commit hooks - is exactly that: infrastructure for a team to produce better."

### Question: "Why Ritz-Carlton?"

**Answer (30 sec):**
> "It is the role I want: real seniority, high ownership, and a team where code quality matters. The JD asks for exactly what I already do - ADRs, standards, OSS - so this is not a leap, it is a fit."

---

## Part 3 - Questions for them (5 min)

Pick 2-3, no more. They show seniority:

1. **"What do you expect from a Principal in the first 90 days?"** - shows you think about impact, not tasks.
2. **"What is the biggest project the team has right now?"** - shows interest in the business.
3. **"How do you make architecture decisions today?"** - opens the door to talk about your system without being asked.
4. **"What hurts the most in the current stack?"** - shows you come to solve, not to add.

---

## Part 4 - Closing (5 min)

**Before the call:**
- [ ] Read the JD once more (React/Next.js, Node, ADRs, OSS, lean high-ownership)
- [ ] Pick the 2 stories you will tell (recommended: #2 and #3)
- [ ] Pick 2 questions for them
- [ ] Water, headphones, quiet place

**During the call:**
- If they ask about the retest (69%): "the retest was a good reminder that preparation matters. The classic JS is solid - event loop, promises, algorithms - and it is now." Don't apologize, don't over-explain.
- If they ask about AI: use the Part 2 answer, short version.
- If they ask about salary: don't give a number first. Ask for their budgeted range. If pushed: "$95k-$105k, which is what a Principal with my profile is worth."

**After the call:**
- Log the result in `docs/entrevistas/ritz-carlton-retest-seguimiento.md`
- Tell me and I update the daily
