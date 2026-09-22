---
name: "session-context"
metadata:
  category: "Workflow"
  tags:
    - sesion
    - contexto
    - memoria
    - proyecto
    - ck
  author: "Kanam (adapted from sreedhargs89/context-keeper)"
  origin: "workspace"
description: "Persistent per-project session context for OpenClaw. Adapted from Context Keeper (ck) for OpenClaw's skill system, SQLite memory, and .knowledge/ handoffs."
user-invocable: false
---

# Skill: session-context

Persistent per-project session context for OpenClaw.

Adapted from **Context Keeper (ck)** by sreedhargs89, re-built for OpenClaw:
- Uses OpenClaw's `db_query` / `db_execute` (namespace: `session_context`) instead of `~/.claude/ck/` JSON files.
- Generates `HANDOFF.md` inside `projects/<slug>/.knowledge/` instead of `~/.claude/projects/<encoded>/memory/`.
- Integrates with `session-lifecycle`: auto-load context on `iniciar sesión`, auto-save on `cerrar sesión`.

## Data Layout

```
~/.openclaw/workspace/.data/session-context.db  ← local SQLite (not versioned)
projects/<slug>/.knowledge/
├── HANDOFF.md              ← generated portable human-readable view
└── session-context.json    ← generated portable machine-readable snapshot
```

**Portability model:**
- `.data/session-context.db` is local-only and ignored by git. It provides fast queries.
- `.knowledge/session-context.json` is versioned. It is the portable source of truth.
- On first run in a fresh machine, if the local DB has no projects but `session-context.json` exists, it is imported automatically.
- `HANDOFF.md` is also regenerated and is the human-readable portable view.

Never hand-edit any of these generated files.

## Commands

All commands are Node.js scripts in `skills/session-context/commands/`.
They read/write the `session_context` SQLite namespace via OpenClaw's DB tools.

### `init` - Register a Project

```bash
node skills/session-context/commands/init.mjs
```

Auto-detects project info from `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `README.md`, and existing `.knowledge/` files.

Outputs a JSON draft. Present it as a confirmation form:

```
Project:     <name>
Description: <description>
Stack:       <stack>
Goal:        <goal>
Do-nots:     <constraints or "None">
Repo:        <repo or "none">
```

After user approval, pipe confirmed JSON to `save.mjs --init`:

```bash
echo '<confirmed-json>' | node skills/session-context/commands/save.mjs --init
```

Confirmed JSON schema:
```json
{
  "name": "...",
  "path": "...",
  "description": "...",
  "stack": ["..."],
  "goal": "...",
  "constraints": ["..."],
  "repo": "..."
}
```

### `save` - Save Session State

Analyze the current conversation and produce:

```json
{
  "summary": "one sentence, max 10 words",
  "leftOff": "what was actively being worked on",
  "nextSteps": ["ordered concrete next steps"],
  "decisions": [{"what": "...", "why": "..."}],
  "blockers": ["..."],
  "goal": "updated goal only if it changed this session"
}
```

Show a draft to the user: `"Session: '<summary>' - save this? (yes / edit)"`.

After confirmation:

```bash
echo '<json>' | node skills/session-context/commands/save.mjs
```

The script:
1. Inserts/updates the project row.
2. Inserts a session row (or updates if the same `session_id` already exists).
3. Inserts linked decision rows.
4. Regenerates `HANDOFF.md` in the project's `.knowledge/` directory.

### `resume [name|number]` - Full Briefing

```bash
node skills/session-context/commands/resume.mjs [arg]
```

Display output verbatim, then ask: `"Continue from here? Or has anything changed?"`
If the user reports changes → run `save` immediately.

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `session-lifecycle/scripts/session-start.sh` | Ritual de inicio de sesion que carga `resume.mjs`. |
| `session-lifecycle/scripts/session-end.sh` | Cierre de sesion que invoca `save.mjs` y genera HANDOFF.md. |
| `knowledge-management/scripts/check-refs.sh` | Verificar links en HANDOFF.md generado. |

### `info [name|number]` - Quick Snapshot

```bash
node skills/session-context/commands/info.mjs [arg]
```

Display output verbatim. No follow-up question.

### `list` - Portfolio View

```bash
node skills/session-context/commands/list.mjs
```

Display output verbatim. If the user replies with a number or name → run `resume`.

### `forget [name|number]` - Remove a Project

First resolve the project name (run `list` if needed).
Ask: `"This will permanently delete context for '<name>'. Are you sure? (yes/no)"`
If yes:

```bash
node skills/session-context/commands/forget.mjs [name]
```

Removes the project, its sessions, its decisions, and regenerates/cleans `HANDOFF.md`.

## Integration with session-lifecycle

### On session start (`iniciar sesión`)

The `session-lifecycle` skill should:

1. Detect the active project from `cwd`.
2. If registered, run `node skills/session-context/commands/resume.mjs` without argument and display the briefing.
3. If not registered, run `list` and show recent projects.
4. Detect unsaved previous session by checking whether the current `session_id` exists in `sessions`.

### On session close (`cerrar sesión`)

The `session-lifecycle` skill should:

1. Run `save` with the LLM-analyzed session summary.
2. Consolidate daily memory files (`memory/YYYY-MM-DD-*.md` → `memory/archive/`).
3. Commit workspace changes.

## Rules
- Always use the scripts. Never hand-edit `HANDOFF.md`.
- Commands are deterministic and use only Node.js stdlib.
- If a script exits with code 1, display its stdout as an error message.
- Stack is stored as comma-separated text in SQLite; render as arrays in UI/handoffs.
- `constraints` are stored as JSON array text in SQLite.
