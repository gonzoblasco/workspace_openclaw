---
name: "session-lifecycle"
description: "Complete session lifecycle management: start, execute, close, and persist."
---

# Workflow: Session Lifecycle

## What it does

Manages the full lifecycle of an AI-assisted work session: loading context, executing work, closing with documentation, and persisting state.

## Phases

### 1. Start
- Load project context, memory, handoff from previous session
- Understand current state, active tasks, pending decisions

### 2. Dispatch
- Spawn sub-agents based on task type:
  - **fork**: when the sub-agent needs the current transcript (e.g., continuing an investigation, analyzing a conversation)
  - **isolated**: when it's independent work (e.g., searching issues, reading docs, parallel tasks without shared context)

### 3. Execution
- Main work, decisions, files modified
- Follow the appropriate workflow for the task

### 4. Close
- Scan session for decisions, changes, pending items
- Write handoff document for next session
- Update memory and changelog

### 5. Tasks
- Convert pending items into actionable tasks
- Create follow-ups or write to project TODO
- Never leave pending items unresolved

### 6. Commit
- Commit and push workspace changes (after handoff and memory, not before)

## Outputs
- Handoff document for next session
- Daily session log
- Tasks created (follow-ups or TODO)
- Workspace committed and pushed
