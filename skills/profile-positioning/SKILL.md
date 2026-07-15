---
name: "profile-positioning"
description: "\"Audit a developer's skills, methodology, and differentiation to build a positioning strategy for job search and professional visibility.\""
---

# Profile Positioning

Use when a developer needs to define, refine, or update their professional positioning — for job search, CV/LinkedIn, interviews, or strategic decisions about what to learn next.

## When to trigger

- "¿Cómo me vendo?" / "¿Cómo me posiciono?"
- Before a job search sprint
- After significant growth (new PRs merged, new project shipped, new skill acquired)
- Before updating CV, LinkedIn, or portfolio
- When feeling stuck about "what makes me different"

## Phase 1 — Audit (what you actually have)

1. **Read context files:**
   - `MEMORY.md` — long-term memory, profile, methodology
   - `CONTRIBUTING.md` — OSS pipeline, visibility plan
   - `projects/PROYECTOS.md` — active and shipped projects
   - Any `HANDOFF.md` from recent work
   - Recent `memory/YYYY-MM-DD.md` files for latest activity

2. **Inventory hard skills:**
   - Languages, frameworks, tools (what you use daily vs. what you've touched)
   - Backend vs frontend depth (be honest)
   - Infrastructure/deployment experience

3. **Inventory soft/methodology skills:**
   - How do you work? (not just what you know)
   - What systems/processes have you built around your work?
   - What do you document? (ADRs, AGENTS.md, ROADMAPs, CHANGELOGs)
   - How do you use AI? (chat vs. structured methodology)

4. **Inventory evidence:**
   - Shipped projects (with links, users, revenue if any)
   - OSS PRs (merged, open, repos they're in)
   - npm packages, CLI tools, templates
   - Public writing, talks, demos

5. **Brutal honesty check:**
   - What do you claim to know but haven't built anything real with?
   - What do you know well but undervalue?
   - Where is the gap between "I can do this" and "I can prove it"?

## Phase 2 — Differentiation (what makes you scarce)

1. **List all devs with the same stack** — "React + Next.js + TS" is common. What's NOT common?
2. **Find the intersections:**
   - Skill A + Skill B where most people have one but not both
   - Example: "Fullstack + accessibility specialization" is less common than "Fullstack"
   - Example: "Uses AI as infrastructure (not chat) + documents decisions" is rare
3. **Identify the methodology differentiator:**
   - Do you have a way of working that most devs don't?
   - Can you articulate it in one sentence?
   - Can you prove it with artifacts (repos, PRs, docs)?
4. **Rate scarcity honestly:**
   - Common (most devs have this)
   - Uncommon (some devs have this)
   - Rare (few devs have this)
   - Scarce (almost nobody has this combination)

## Phase 3 — Pitch construction

1. **Write 3 versions:**
   - **One-liner** (for LinkedIn headline, elevator pitch): 15-20 words
   - **Paragraph** (for CV summary, cover letter): 3-4 sentences
   - **Full story** (for interviews, "tell me about yourself"): 1-2 minutes spoken

2. **Pitch structure:**
   - What you are (role)
   - What makes you different (methodology + specialization)
   - What you can prove (evidence: PRs, projects, packages)
   - What you're looking for (the match)

3. **Avoid:**
   - Buzzword lists ("React, Node, AWS, Docker, Kubernetes...")
   - Generic claims ("passionate developer", "team player")
   - Things you can't prove with artifacts

4. **Do include:**
   - Specific evidence (repo links, PR links, npm packages)
   - Methodology if it's real ("I work with AI as a structured copilot, not as chat")
   - Opinionated positions if they're defensible ("I prefer curated stacks over default choices")

## Phase 4 — Strategy alignment

1. **Map pitch to job search channels:**
   - CV: which version goes where
   - LinkedIn: headline + about section
   - GitHub: profile README, pinned repos
   - Cover letters: adapt per company

2. **Map pitch to OSS strategy:**
   - Which repos prove the claims in the pitch?
   - Which PRs would be most visible to the companies you're targeting?
   - Update `CONTRIBUTING.md` pipeline if needed

3. **Map pitch to learning priorities:**
   - What gaps does the audit reveal?
   - What's the next skill that would increase scarcity?
   - What evidence do you need to build next?

## Phase 5 — Artifacts

1. **Update `MEMORY.md`** — "Perfil profesional / Metodología" section
2. **Create/update a profile document** if useful (e.g., `PROFILE.md` or section in CV)
3. **Update LinkedIn/CV** — user does this themselves, but generate the text
4. **Commit + push workspace:**
   ```bash
   cd /Users/gonzoblasco/.openclaw/workspace
   git add -A && git commit -m "profile: <description of update>" && git push
   ```

## Red flags

- Don't claim skills you can't prove with artifacts
- Don't copy generic pitch templates — the point is differentiation
- Don't skip the brutal honesty step — overclaiming hurts in interviews
- Don't write the pitch for the dev — draft it, let them react and refine
- Don't forget to update after growth — a stale pitch is worse than no pitch

## Periodic review

Re-run this skill every 2-3 months, or after major milestones:
- N PRs merged in notable repos
- New project shipped
- New skill acquired
- Job search starting
