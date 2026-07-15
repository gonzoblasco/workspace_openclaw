---
name: "story-planning"
description: "\"Discover and plan a story — premise, subgenre, characters, setting, structure, chapter beats. Collaborative planning with git versioning before writing.\""
---

# Story Planning

Use when planning a story before writing — any genre, any length. Covers the collaborative discovery process from blank page to chapter beats.

## When to use

- User wants to write a story (short, novella, novel) and needs to plan it
- User has a vague idea and wants to develop it into a structure
- User wants to define characters, setting, tone, or plot beats

## Prerequisites

- A workspace directory for the story project (create one if needed: `projects/<story-name>/`)
- The user is ready to collaborate interactively (this is not autonomous generation)
- Git repo initialized in the story project directory (if not, `git init` on first save)

## Phase 1 — Calibrate

Ask focused questions. Few at a time, not a questionnaire. The goal is to narrow down enough to start planning.

1. **Premise check:** Does the user have a seed idea? If yes, work from it. If no, propose options based on their taste.
2. **Format:** Short story (<7000), novelette (7000-15000), novella (15000-40000), novel (40000+)?
3. **Tone/subgenre:** Within the broad genre, which register? (Horror: suburban, psychological, cosmic, slasher. Sci-fi: hard, social, cyberpunk. Literary: coming-of-age, family saga, etc.)
4. **Protagonist & POV:** Who is the story about? First person, third limited, third omniscient?
5. **Setting:** Where and when? Specific places the user knows add texture — ask for real locations they have a connection to.
6. **Collaboration style:** How does the user want to work? (User pitches idea → agent develops. Write together alternating. Agent proposes structure → user writes → agent edits. Mixed.)

Do NOT ask all at once. Ask 3-5, let the user answer, then move on. Adapt based on their answers — skip what they already defined.

## Phase 2 — Outline

Build the chapter-by-chapter structure. Present it as beats, not a dry list.

1. **Propose chapter count and structure** based on format:
   - Short story: 5-8 chapters, 1 scene each
   - Novelette: 8-15 chapters, 1-2 scenes each
   - Novella: 15-30 chapters
   - Novel: 30+ chapters
2. **Write a one-line summary per chapter** — what happens, what it accomplishes in the arc
3. **Identify key beats:** turning points, escalation moments, resolution
4. **Present outline and ask for feedback** — adjust before moving on
5. **Save to `OUTLINE.md`** in the story project directory
6. **Commit:** `git add -A && git commit -m "outline: <story name>"`

## Phase 3 — Chapter Beats

For each chapter, define internal beats before writing.

1. **Break the chapter into 4-7 internal beats** — what happens moment by moment
2. **Include per beat:** a short title, 1-2 sentence description, estimated paragraph count, tone notes
3. **Add chapter-level notes:** POV, tone, what the reader should feel, what to avoid
4. **Save each chapter's beats** to `beats/capitulo-XX.md` (or `beats/chapter-XX.md`)
5. **Ask for approval** before moving to writing
6. **Commit per chapter:** `git add -A && git commit -m "beats: capítulo XX"`

## Phase 4 — Characters

If not fully defined in Phase 1, develop characters now:

1. **For each major character:** name, age, one-line essence, key trait, how they talk, what they want
2. **Show don't tell:** define characters by behavior and speech patterns, not biography dumps
3. **Plant dynamics:** how do they relate to each other? Tensions, alliances, friction points
4. **Save to `OUTLINE.md`** (characters section) or a separate `PERSONAJES.md`
5. **Commit:** `git add -A && git commit -m "personajes: <description of what was defined>"`

## Phase 5 — Register

Keep a running log of all decisions made during planning:

1. **Create `REGISTRO.md`** in the story project directory
2. **Log every decision** with a short rationale (why this subgenre, why this setting, why this structure)
3. **Track progress** with a checklist of chapters: beats done, scene written, revised
4. **Update after each session** so any new session can pick up where the last one left off
5. **Commit when updating:** `git add -A && git commit -m "registro: update after <what changed>"`

## File structure

```
projects/<story-name>/
├── OUTLINE.md          # full outline: parameters, characters, chapter summaries
├── REGISTRO.md         # decision log + progress tracker
├── PERSONAJES.md       # optional: character sheets (if complex)
├── beats/
│   ├── capitulo-01.md  # internal beats for chapter 1
│   ├── capitulo-02.md
│   └── ...
└── escenas/            # created by story-writing skill
    ├── capitulo-01.md
    └── ...
```

## Git versioning rules

- **Init repo on first save:** if `projects/<story-name>/.git` doesn't exist, run `git init`
- **Commit after every save:** outline, beats, characters, registry — each save gets a commit
- **Commit messages:** `<type>: <description>` (e.g., `outline: El verano que no pasa nada`, `beats: capítulo 3`, `personajes: viejo de Alvear`)
- **Don't commit empty placeholders** — only commit when there's real content
- **If the story project lives inside the workspace repo**, commits go to the workspace repo (don't create a nested repo)
- **Push if remote exists:** check `git remote -v` and push after committing

## Rules

- Never write the story during planning. Planning and writing are separate phases.
- Ask before assuming. If the user didn't specify something, ask.
- Keep tone notes practical — "no horror adjectives in chapter 1" is better than "establish a ominous undertone".
- Adapt chapter naming to the user's language (capítulo / chapter / chapitre).
- The outline is a living document. Adjust it if the story evolves during writing.
- Save everything and commit. The whole point is continuity across sessions.
