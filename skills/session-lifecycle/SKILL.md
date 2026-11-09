---
name: "session-lifecycle"
metadata:
  category: "Workflow"
  tags:
    - session
    - lifecycle
    - productivity
description: "Session Lifecycle workflow: complete session cycle. Replaces 4 session skills."
user-invocable: false
---

# Workflow: Session Lifecycle

## Skills it replaces
- `session-closure`
- `session-closure-ritual`
- `context-management`
- `agent-dispatcher`

## Purpose
Management of the complete lifecycle of an AI work session.

## When to use it
- When starting an AI work session (load context + memory)
- When closing a session (write HANDOFF, memory, CHANGELOG)
- To spawn sub-agents according to the task (fork vs isolated)
- To turn pending items into actionable tasks and commit the workspace

## Phases

### 1. Start - load context, memory, handoff of the active project

Session start is triggered **only when Gonzo explicitly asks for it** ("start session", "get going", "start working", etc.). Do not run the start ritual on casual queries.

**Start modes:**

#### A. Start with explicit project

If the user says `"start session in <project>"` or similar:

1. Resolve the project by name: `node skills/session-lifecycle/commands/resume.mjs <name>`.
2. If it does not exist, offer `session-context:init`.
3. If it exists, show the `resume` briefing verbatim.
4. Ask for today's **Session Goal**.

#### B. Start with cwd auto-detection

If Gonzo says `"start session"` and the current `cwd` is registered in `session-context`:

1. Detect the project with `resume.mjs` without arguments.
2. Show the briefing.
3. Ask: `"Are we continuing in <project> or do you want to switch projects?"`
4. If Gonzo wants another project - go to mode A.
5. If he wants brainstorming without a fixed project - go to mode C.

#### C. Start without a defined project (brainstorming / triage)

If Gonzo says `"start session"`, `"brainstorming"`, `"I don't know which project yet"`, etc.:

1. Do not run `session-context:resume` for any project.
2. Load general memory: `MEMORY.md`, today's `memory/YYYY-MM-DD.md`, recent project list optionally with `session-context:list`.
3. Ask: `"Which project are we working on? Or is this a general planning/brainstorming session?"`
4. Define a temporary Session Goal. It does not require a fixed project.

**In all modes:**

- **Semantic context injection (2026-08-31):** when starting a session with a project, `session-start.sh` automatically searches memory (sessions + learnings) for the most relevant entries for the objective and shows them as context. This way the session starts with relevant memory instead of cold. Uses `scripts/memory-search.py` with the objective as query.
- Detect unsaved previous session: if the current `session_id` does not exist in `session-context`, warn: `"The previous session was not saved - do you want to save it before starting?"`
- **Session Goal:** define the session's explicit objective. What do we want to achieve? What is the success criterion?
- If the objective is fuzzy, clarify before moving forward. Do not start without direction.
- **Complexity score (complexity-driven-pipeline):** when defining the Session Goal, run `./scripts/complexity-scorer.sh "<objective>"` to get the T-score (1-20). This decides model, thinking and pipeline depth BEFORE spawning agents. `session-start.sh` already does this automatically and persists the T-score in the session log. Buckets: T≤6 = Kanam only; T 7-12 = A; T 13-16 = A+B cross-review; T≥17 = Kanam(max)+A+B+verification + confirmation gate. See skill `complexity-driven-pipeline`.
- **Program brief (2026-11-06):** `session-start.sh` también imprime el brief de **programas activos** del Planner (`agents/kanam-planner/scripts/program_plan.py brief --quiet`). Si hay un programa, retomar es leer ese brief; el plan de sesión y el programa son capas distintas. Si el objetivo es programa, el CORE llama al Planner antes de ejecutar (`skills/planner-delegation/SKILL.md`).

### 2. Dispatcher - spawn sub-agents according to the task:
- **fork**: when the sub-agent needs the current transcript (e.g.: continuing an investigation, analyzing a conversation)
- **isolated**: when it is independent work (e.g.: searching issues, reading docs, doing parallel tasks without shared context)

### 3. Execution - main work, decisions, files touched
- **Mid-session checkpoint:** halfway through the session (or when changing tasks), ask: "Am I on the right track toward the objective? Do I need to adjust anything?"
- If the checkpoint reveals a detour, redefine the objective or constraints before continuing.

### 4. Save - scan session, write HANDOFF, memory, CHANGELOG

**Disparador (2026-10-06):** **"guardar sesion"** y **"cerrar sesion"** son el mismo pedido - el ciclo de guardado completo. No distinguir entre ambos.

**Dos entregables por cierre (2026-10-06):**
1. **Informe detallado** en `memory/YYYY-MM-DD.md` (una seccion por sesion). Plantilla registrada en `memory/_templates/session-close.md`.
2. **HANDOFF del proyecto en curso** (`scripts/session-handoff.py`), en el `.knowledge/` del proyecto o del workspace. Es el punto de entrada para continuar; se regenera en cada cierre. El destino lo resuelve el script (workspace -> `<workspace>/.knowledge/HANDOFF.md`; proyecto -> `<workspace>/projects/<slug>/.knowledge/HANDOFF.md`, ADR-098).

**Dos clases de HANDOFF, dos destinos (2026-11-09).**
- **General del workspace** (`--project workspace`): es el punto de entrada para continuar **cualquiera** de los proyectos. Desde 2026-11-09 el generador **fusiona** el contenido con el HANDOFF vigente en vez de pisarlo: conserva las ultimas 5 entradas de "Que se hizo", y une `Estado actual`, `Proximos pasos`, `Decisiones` y `Archivos tocados` con dedupe. Dos sesiones que cierran a la vez ya no se pisan; el gate de merge no corre en este modo porque la fusion preserva por construccion.
- **Curso** (`--course <slug>`): cada curso de `studies/<slug>/` tiene su propio `HANDOFF.md` porque lleva su ritmo. Destino: `studies/<slug>/HANDOFF.md` (no `.knowledge/`). Titulo: `# HANDOFF - Curso <slug>`. El daily se registra con el label `studies/<slug>`.

**Plantilla de curso.** El `--status` de un cierre de curso lleva estas cuatro lineas, no un estado generico:
```
- Modulo actual:
- Ejercicios hechos:
- Preguntas abiertas:
- Proximo bloque:
```

El HANDOFF se **deriva del informe de cierre**: mismo resumen, mas estado actual, proximos pasos, decisiones y archivos tocados.
- **Program update (2026-11-06):** si la sesión trabajó un paso de un programa, antes de cerrar actualizá el paso con `agents/kanam-planner/scripts/program_plan.py update <slug> <step> <status> --evidence "..."`. El cierre de sesión **no** cierra el programa: el programa es multi-sesión. Si el alcance cambió, el CORE vuelve a llamar al Planner; no parchea el plan a mano.
- **Auto-cataloging + DB-first (2026-08-31):** when saving a session, `session-end.sh` (1) writes the summary **directly to `memory/memory.db`** (`daily_notes` table) as the source of truth via `scripts/memory-end-session.py`, (2) regenerates `memory/YYYY-MM-DD.md` as an **exported view** (regenerable with `export-all`), and (3) runs `scripts/memory-catalog-v2.py` to update embeddings/topics/learnings. With this, the DB is the source and the `.md` files become optional.
- **Reconciliation guard (2026-09-14):** the DB->.md export is lossy when the `.md` was edited by hand or written by a concurrent session. Before exporting, `memory-end-session.py` compares `.md` sections vs the DB and merges into the DB the ones that only live in the `.md` (preserving the DB-only ones), with a backup in `/tmp/daily-<date>.backup.md`. If the date has no row in the DB, it creates one from the whole `.md`. `--no-reconcile` reproduces the old behavior (destructive, opt-in). **The daily is written with the script, never by hand:** editing the `.md` directly leaves the DB behind.
- Semantic context injection: when saving, the session is indexed in the DB for future search (`./scripts/memory-db.sh search "..."`).
- If the session had an associated project, run `session-context:save` with the session summary: `summary`, `leftOff`, `nextSteps`, `decisions`, `blockers`, and `goal` only if it changed.
- If it was a session without a project (brainstorming/triage), save the summary in `memory/YYYY-MM-DD.md` and do not touch `session-context`.
- Show the draft to the user for confirmation or editing before persisting.
- **Review previous sessions of the day:** before closing, read the day's `memory/YYYY-MM-DD-*.md` files to make sure there were no prior sessions that the summarized daily note does not capture. Do not rely only on the daily note or memory.
- **Consolidate loose files of the day:** if there are `memory/YYYY-MM-DD-HHMM.md` files (individual sessions), move them to `memory/archive/`. The consolidated daily `memory/YYYY-MM-DD.md` already has all the info.
- **Mandatory self-reflection:** if there were Gonzo corrections, structural changes, or significant learnings, record them in LEARNINGS.md before closing. Do not wait for Gonzo to ask "shall we review lessons?"
- If CONTRIBUTING.md, skills, or AGENTS.md were modified, verify that the change is complete and no adaptations are missing in related skills

### 5. Tasks - turn pending items into actionable tasks. Create cron jobs for follow-ups, or write them in the project's TODO.md. Do not leave pending items up in the air

### 6. Commit - commit + push the workspace (after HANDOFF and memory, not before)

## Helper Scripts

Scripts in `skills/session-lifecycle/scripts/`:

| Script | Use |
|---|---|
| `session-start.sh --project <name> --objective <obj>` | Loads the previous HANDOFF, runs the complexity-scorer on the objective, and creates/updates the daily log in `memory/YYYY-MM-DD.md`. Use at session start with a project. |
| `session-end.sh (--project <name> | --course <slug>) --summary <text> [--status ..] [--next-steps ..] [--decisions ..]` | Cierra la sesion: escribe el informe en la DB/`memory/` (DB-first) y genera/actualiza el HANDOFF del proyecto o del curso. Disparador: **"guardar sesion"** o **"cerrar sesion"** (son indistintos). |
| `scripts/session-handoff.py --project <name> --summary <text> [...]` | Genera/actualiza el HANDOFF.md del proyecto en curso (o del workspace). Destino: `<workspace>/projects/<slug>/.knowledge/HANDOFF.md` (ADR-098); para el sistema, `<workspace>/.knowledge/HANDOFF.md`. |
| `scripts/complexity-scorer.sh <objective>` | Evaluates complexity in 4 dimensions - T-score 1-20 + bucket + model + thinking + pipeline. Run automatically by `session-start.sh`. Skill: `complexity-driven-pipeline`. |

If the session touches workspace skill scripts, run `npm test` before the final commit.

## Post-Task Self-Reflection

After significant tasks (multi-step, debugging, PRs, config changes), take a quick evaluation pause:

```
CONTEXT: [task type]
REFLECTION: [what I noticed]
LESSON: [what I would do differently]
BIASES DETECTED: [sunk cost / anchoring / confirmation / etc. or none]
```

**When to do it:**
- After completing a multi-step task
- After receiving feedback (positive or negative)
- After fixing a bug
- When you notice your output could be better

**Destination:** if it is a new lesson - `docs/LEARNINGS.md`. If it is an existing pattern - update Recurrence-Count.

### Automated post-task reflection (2026-09-03)

New stage of the cycle: `scripts/post-task-reflection.sh` structures reflection per task (not per session), detects duplicates in the DB, cross-references existing skills via skill-router, and proposes a new skill if the pattern is not covered.

```bash
./scripts/post-task-reflection.sh --type <debug|feature|review|config|research|oss|docs|other> \
  --summary "<what happened>" --lesson "<lesson>" \
  --check-dups --propose-skill --save
```

**Flags:**
- `--check-dups`: semantic search of similar learnings (avoids duplication)
- `--propose-skill`: generates a proposal in `skills/_proposals/` if the pattern is not covered (requires L1 keyword match + score >= 0.6; embedding-only does not count)
- `--save`: persists the learning in `memory.db` (learnings table, category by type)

**Relationship with closing self-reflection:** the closing one (below) records global learnings when saving a session; this one runs per complex task, in the moment, and also detects skills. Complementary, not redundant.

### Methodology Audit - quick check (2026-09-03)

If the session touched methodology (skills, AGENTS.md, scripts, process docs, new lessons), run the quick 8-box check of `docs/METHODOLOGY-AUDIT.md` before closing. If 3+ boxes remain unchecked, the session left methodological debt: record it as pending, do not ignore it. If the session did not touch methodology, skip it (it would be noise). Deep audit (score 0-16): quarterly or on Gonzo's request.

## WAL Protocol - Write-Ahead Logging

**Golden rule:** if it is important to remember it, WRITE IT NOW - not later. Context disappears. The file stays.

### Scan every message for:
- ✏️ **Corrections** - "It's X, not Y" / "Actually..." / "No, I meant..."
- 📍 **Proper names** - people, places, companies, products
- 🎨 **Preferences** - colors, styles, approaches, "I like / I don't like"
- 📋 **Decisions** - "Let's do X" / "We go with Y" / "Use Z"
- 📝 **Draft changes** - edits to something we are working on
- 🔢 **Specific values** - numbers, dates, IDs, URLs

### The Protocol

If ANY of these APPEARS:

1. **STOP** - Do not start drafting your response
2. **WRITE** - Update `memory/YYYY-MM-DD.md` or the relevant file with the detail
3. **THEN** - Reply to Gonzo

The urge to respond is the enemy. The detail feels so clear in context that writing it seems unnecessary. But the context will be lost. Write first.

**Example:**

Gonzo says: "Use the blue theme, not the red one"

❌ WRONG: "OK, blue!" (seems obvious, why write it)
✅ RIGHT: Write to `memory/YYYY-MM-DD.md`: "Theme: blue (not red)" - THEN reply

## Working Buffer - Danger Zone

When the session context reaches ~60% (verifiable with `session_status`), activate the buffer:

1. Create or clear `memory/working-buffer.md`
2. From that point on, **every exchange** is logged: Gonzo's message + summary of your response
3. **Flush BEFORE compacting** (Honcho's idea): when compaction approaches, make sure the buffer is complete and up to date BEFORE losing context - not after. If the session is about to compact (close to the limit), do a final flush of the buffer with the latest important items.
4. After compaction, read the buffer first before anything else

**Format:**

```markdown
# Working Buffer
**Status:** ACTIVE
**Started:** 2026-07-22T12:00:00-03:00

---

## 2026-07-22T12:01:00 Gonzo
[message]

## 2026-07-22T12:01:05 Kanam (summary)
[1-2 sentences with key details]
```

### Structured compaction summary (Session Compact idea)

When the session is compacted (not just the buffer), generate a **structured summary** instead of a generic text block. When compacting, build the summary with these fields (ported from Session Compact - ClawHub):

```markdown
# Compaction Summary
**Scope:** <what was compacted - e.g. "35 messages of the X development session">
**Pending work:** <todos/pending items in progress - e.g. 'finish U3, review U2'>
**Key files:** <important files touched - e.g. 'src/auth.ts, db/schema.sql'>
**Decisions:** <key decisions made that must not be lost>
**Key timeline:** <3-5 conversation milestones that matter>
**Next step:** <what comes next>
```

- **Pending work** and **Next step** are the most critical - they must not be lost when compacting.
- **Key files** and **Decisions** allow resuming without re-discovering.
- Complements the working buffer (raw log) with an actionable post-compaction summary.

## Compaction Recovery

There are **two mechanisms** that work together to recover context after a compaction. They are not mutually exclusive - the plugin covers the automatic part, the manual buffer covers what the plugin does not see (decisive when the context is long or the compaction was aggressive).

### A. Plugin `compaction-context` (automatic) - installed 2026-08-22

The plugin is installed in `~/.openclaw/extensions/compaction-context/` (local, patched installation) and registered as hook-only in `plugins.entries.compaction-context`. It takes an automatic snapshot:

1. **`before_compaction`** - before compacting, reads the last N messages (default 20) of the session `.jsonl` and writes them into the workspace `RECENT.md` + sets the `.compaction-recovery-pending` flag.
2. **`before_agent_start`** - if the flag exists (just compacted), reads `RECENT.md` and injects it as `prependContext` inside `<compaction_context_recovery>...</compaction_context_recovery>`, and deletes the flag.

**What it means for me (the agent):** after a compaction, I am NOT 100% blank. The `prependContext` reinjects the last 20 messages. If you have no idea what happened, check the injected `prependContext` BEFORE asking anything.

**Current config (defaults):** 20 messages x 500 chars/message (~10K chars / ~2.5K tokens, injected only once post-compaction). Configurable in `openclaw.json` - `plugins.entries.compaction-context.config`.

**⚠️ Workspace clutter handling (important):** the plugin writes `RECENT.md` and `.compaction-recovery-pending` into the workspace root, which is a git repo. They are already in `.gitignore` (added 2026-08-22), so they do not clutter `git status`. Do not commit them.

### B. Manual buffer (existing) - `memory/working-buffer.md`

The plugin does not capture everything: only the last 20 messages truncated to 500 chars, and it does not save key decisions made mid-context. The manual working-buffer remains a source for:

- Decisions made "between the lines" not evident in the snapshot
- Context older than 20 messages
- Pending items the snapshot truncated

### C. Post-compaction recovery flow (consolidated)

When waking up without context (compaction, restart, or Gonzo says "where were we?"):

1. **Check the injected `prependContext`** (the plugin already reinjected it). It is the immediate source - the last 20 messages.
2. **Read `memory/working-buffer.md`** - raw danger-zone exchanges that the snapshot does not cover
3. **Read today's and yesterday's `memory/YYYY-MM-DD.md`**
4. **`memory_search()`** for missing context
5. **Extract** the important items from the buffer into `memory/YYYY-MM-DD.md`
6. **Present:** "Recovered from buffer + plugin snapshot. Last task was X. Shall we continue?"

Do not ask "what were we talking about?" - the buffer has the conversation.

---

*Pending technical debt note:* the plugin was installed local and patched (the author's npm package ships with uncompiled `index.ts` + "hook registration missing name" bug against the 2026.7.1-2 API). If the author publishes a fixed version, migrate to `openclaw plugins install compaction-context`.

## Handoff Between Sub-agents

When a sub-agent hands work to another (or returns results to the main), the handoff must include:

- **What was done** - summary of changes/output
- **Where the artifacts are** - exact file paths
- **How to verify** - test commands or acceptance criteria
- **Known issues** - anything incomplete or risky
- **What's next** - clear next action for the receiving agent

**Bad handoff:** "Done, review the files."
**Good handoff:** "I built the auth module in /shared/artifacts/auth/. Run `npm test auth` to verify. Known issue: rate limiting not implemented yet. Next: reviewer checks error handling edge cases."

**Lesson:** a vague handoff generates duplicated work or errors. Being explicit about what was done, where it is, and what is missing saves time for both sides.

## Productivity & ADHD - How We Work

Gonzo has ADHD. The productivity system must adapt to that, not the other way around.

### Principles

- **One thing at a time.** Do not mix projects in the same session. Each OpenClaw session = one project.
- **Inbox capture.** If something occurs to Gonzo while we work on something else, I catch it in `inbox.md` and continue with what we were doing.
- **Overload triage.** If there are too many open things, stop and prioritize before continuing. Ask: "What is the most important thing NOW?"
- **Start routines.** When starting a session, review what was left pending from the previous session before adding new things.
- **Save routines.** When ending a session, make clear what comes next for the next one. This way Gonzo does not lose 10 min resuming.
- **Focus > multitasking.** A focused 2h session is worth more than 4h of context switching.
- **No guilt for what was not done.** If something was left unfinished, it gets picked up again. There is no "I should have done more".

### Deliberate Pause - Read, Process, Respond

Gonzo asks that our responses have a **deliberate delay** between reading the message and acting. Do not respond with the first reaction.

The flow is: **READ - PROCESS - (reflective pause) - RESPOND**.

- **READ** - Read the whole message, without jumping to conclusions. Identify what it really asks, not what it seems to ask.
- **PROCESS** - Do the task with the available tools. Gather evidence before opining.
- **REFLECTIVE PAUSE** - Before responding, ask: did I understand the request? Did I verify what is mutable? Is there an assumption I am taking for granted? Is this what best answers what was asked, or is it the easiest answer?
- **RESPOND** - Only then, give the response.

**Golden rules:**
- Do not respond half-read. If the message is long or ambiguous, paraphrase the request before executing.
- Tasks that touch the outside world (push, publish, send) deserve a double pause: verify before acting.
- If Gonzo asks for something that changes the course of what we were doing (e.g. "do not push"), incorporate that constraint and continue, do not abandon.

### Overload signals

If I detect any of these, I stop and ask before continuing:
- Gonzo mentions 3+ different projects in the same conversation
- There are unresolved open tasks from previous sessions
- The day's daily log has entries from 3+ different topics
- Gonzo says "I'm in a thousand things" or similar

### How I Help

- **Soft reminder:** "Before starting with this, remember you had X pending from yesterday. Do we continue with that or start fresh?"
- **Quick triage:** "You have 4 open things. Which is the priority now?"
- **Explicit saving:** At the end of each session, I leave a summary of what was done and what's next.
- **No pressure:** If Gonzo wants to change topics, we change. The system adapts.

## Outputs
- `.data/session-context.db` (projects, sessions, decisions)
- `projects/<slug>/.knowledge/HANDOFF.md`
- `memory/YYYY-MM-DD.md`
- Tasks created in the system (cron jobs or TODO.md)
- Workspace committed and pushed

## Related Skills

- [Task Execution](../../agents/kanam-dev/skills/planning-and-task-breakdown): To execute tasks within the session
- [Knowledge Management](../../agents/kanam-mind/skills/knowledge-management): To record session learnings
