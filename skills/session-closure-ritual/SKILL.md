---
name: "session-closure-ritual"
description: "Ends main session. Writes HANDOFF/memory/CHANGELOG, commits git, shows summary. Follows MEMORY.md for durable persistence."
---

## Session Closure Ritual

**When:** End of main session (not chat/sub-agent turns)

**Flow:**

1. Scan conversation → Summarize key topics, decisions, unresolved items
2. Write files: HANDOFF.md, memory/YYYY-MM-DD.md, CHANGELOG.md
3. Commit git → Stage and commit with descriptive message
4. Display summary

**Guidelines:**
- Only close main sessions
- Capture lessons learned
- Preserve context for continuation
- Commit before ending

**Trigger:** User says "cerrar sesión" or "end session" in main context
