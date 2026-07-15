---
name: "story-writing"
description: "\"Write and version story scenes from chapter beats with git. Collaborative drafting with structured files and decision log.\""
---

# Story Writing

Use when writing a story scene-by-scene from a prepared outline and chapter beats. Covers the drafting workflow: from beats to written scene to versioned files.

## When to use

- User has an `OUTLINE.md` and chapter beats and wants to start writing scenes
- User wants to write a story collaboratively, scene by scene
- User is continuing a story project across sessions and needs to pick up where they left off

Works together with `story-planning` (which creates the outline and beats). This skill handles the writing phase.

## Prerequisites

- A story project directory with `OUTLINE.md` and at least one chapter's beats in `beats/`
- `REGISTRO.md` tracking progress
- Git repo initialized (if the project is inside a workspace repo, commits go there; if standalone, ensure `git init` was done)
- If starting a new session: read `REGISTRO.md` first to know where you are

## Workflow per chapter

### Step 1 — Read context

1. Read `OUTLINE.md` for parameters, characters, and chapter summary
2. Read `REGISTRO.md` for current progress and any notes from last session
3. Read the beats for the chapter you're about to write (`beats/capitulo-XX.md`)
4. Read the last written scene (if continuing) to maintain voice and continuity

### Step 2 — Brief discussion

Before writing, confirm with the user:
- Does anything need adjusting in the beats?
- Any specific idea or image they want in this scene?
- Any concerns about tone or pacing?

Keep this short. Don't over-plan — the beats are already the plan. If the user says "just write it", write it.

### Step 3 — Write the scene

Write the scene following the beats. Guidelines:

1. **Follow the beats in order** — each beat is a unit of the scene
2. **Hit the tone notes** — if beats say "no horror adjectives", respect that
3. **Write in the user's language** — Spanish, English, whatever they write in
4. **Dialogue should sound natural** — read it aloud mentally; if it sounds written, rewrite it
5. **Show don't tell** — actions, sensory details, dialogue over exposition
6. **Respect the POV** — if first person, everything filters through that narrator's perception
7. **Target the estimated word count** from the beats file
8. **Don't over-polish** — first draft energy matters more than perfect prose

### Step 4 — Present and review

1. Present the written scene to the user
2. Ask specific questions (not generic "is this ok?"):
   - Does the tone match what they imagined?
   - Do the characters feel right?
   - Is there anything to adjust before saving?
3. Incorporate feedback. Revise if needed.

### Step 5 — Save, commit, and register

1. Save the scene to `escenas/capitulo-XX.md`
2. **Commit:** `git add -A && git commit -m "escena: capítulo XX — <short description>"`
3. **Push if remote exists:** check `git remote -v` and push after committing
4. Update `REGISTRO.md`:
   - Mark the chapter as written in the progress checklist
   - Log any decisions made during writing (name changes, tone shifts, new ideas)
   - Note any revisions needed for future chapters
5. **Commit registry update:** `git add -A && git commit -m "registro: capítulo XX written"`
6. If the user approves, move to next chapter's beats (or switch to `story-planning` if beats need updating)

## File structure

```
projects/<story-name>/
├── OUTLINE.md          # full outline (from story-planning)
├── REGISTRO.md         # decision log + progress tracker
├── beats/
│   ├── capitulo-01.md
│   └── ...
└── escenas/
    ├── capitulo-01.md  # written scenes
    └── ...
```

## Git versioning rules

- **Commit after every scene save:** `git add -A && git commit -m "escena: capítulo XX — <description>"`
- **Commit after registry updates:** `git add -A && git commit -m "registro: <what changed>"`
- **Commit after revisions:** `git add -A && git commit -m "revisión: capítulo XX — <what changed>"`
- **Commit after final pass:** `git add -A && git commit -m "revisión final: <story name>"`
- **Don't commit empty placeholders** — only commit when there's real content
- **If the story project lives inside the workspace repo**, commits go to the workspace repo (don't create a nested repo)
- **Push if remote exists:** `git push` after each commit
- **Commit message format:** `<type>: <description>` — types: outline, beats, personajes, escena, registro, revisión

## Continuity rules

- **Voice consistency:** always read the last written scene before writing the next one
- **Character consistency:** check how characters were established in earlier scenes
- **Setting consistency:** don't contradict geography, timing, or details already written
- **Plot tracking:** if something unexpected emerges during writing, log it in REGISTRO.md and check if the outline needs updating

## Revision

When the user asks to revise a scene:

1. Read the current version and the beats
2. Identify what needs changing
3. Rewrite preserving what works
4. Save the new version (overwrite — the file IS the current version)
5. **Commit:** `git add -A && git commit -m "revisión: capítulo XX — <what changed>"`
6. Log the revision in `REGISTRO.md`

## Final pass

When all scenes are written:

1. Read the full story from start to finish
2. Check for: continuity errors, pacing, voice drift, unresolved threads
3. Propose specific revisions (not a generic "want me to polish it?")
4. Apply revisions
5. **Commit each revision:** `git add -A && git commit -m "revisión final: capítulo XX — <what>"`
6. **Final commit:** `git add -A && git commit -m "revisión final: <story name> complete"`
7. Compile into a single file if the user wants a clean copy
8. **Commit the compiled version:** `git add -A && git commit -m "compile: <story name> final"`

## Rules

- Never write a scene without reading the beats first
- Never skip the REGISTRO update — it's the continuity lifeline
- Never skip the commit — versioning is the safety net
- If the user wants to deviate from beats, update the beats file, commit, then write
- Don't generate generic prose — every scene should feel specific to this story
- The user is the author. The agent is the copilot. Their calls win.
