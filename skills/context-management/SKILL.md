---
name: "context-management"
description: "Strategy to manage OpenClaw context between sessions: clear after handoff vs compress transcripts. Hybrid approach recommended for long-running projects."
---

# Context Management Skill

## Purpose

Strategy to manage OpenClaw context consumption between sessions. Decides when to clear full conversation transcript vs. periodically compress for long-running conversations while maintaining skills and decisions persistence.

## Trigger Conditions (all true)

- [ ] Current session runtime > 20,000 tokens or ~3 hours
- [ ] Session ends with HANDOFF.md complete  
- [ ] Skills created (project-regeneration, adr-framework, workspace-scaffold exist)
- [ ] Decision made about future conversation approach (clear vs compress)

## Strategy Options

### Option 1: Clear Context After Handoff ✅

**Best for:** Long-running projects (weeks/months), individual sessions (4h+)

```
Session starts → Work until HANDOFF.md complete → Clear transcript context
↓
Next day session: Fresh conversation, same skills available via SESSION_KEY
```

**Benefits:**
- Zero token consumption on old transcripts
- Skills persist from `skills/` folder (not conversation)
- Decisions documented in MEMORY.md + ADRs (persistent memory)

### Option 2: Compress Periodically ✅ Also Recommended

**Best for:** Multi-day conversations without session breaks

```
Session starts → Work until ~20,000 tokens → Compress transcript to SUMMARY.md only
↓
Next day: Continue with compressed context + full skills available
```

**Benefits:**
- Maintain conversation flow across days
- Avoid token overflow mid-session
- Skills and ADRs provide persistent reference points

### Option 3: Hybrid (Recommended) 🎯

**Best for:** Mixed workloads (long sessions + some multi-day tracking)

```
Daily session → Clear context after HANDOFF.md complete
Every 3 days → Compress to SUMMARY.md if transcript >20,000 tokens
Skills always available via skills/ folder reference
```

**Implementation:**

At end of session:
1. Check transcript token count (approximate from message length)
2. If >20,000 tokens: compress to `memory/session-summary-X.md` format
3. Always create/update `HANDOFF.md` with current state
4. Skills remain available for next session (reference via skills/ folder)

## Decision Rules (if user not specified preference)

| Condition | Action |
|-----------|--------|
| Session > 3 hours | Clear context after HANDOFF |
| Transcript > 20,000 tokens | Compress to SUMMARY.md first, then clear |
| Skills exist in skills/ folder | Use them as conversation reference instead of full transcript |

## Example Use Case

**Scenario:** Gonzo's accessible-ui regeneration session

```bash
# Day 1: Regeneration (4 hours)
Session starts → Clean slate (no previous context needed)
Work through Phase 0 (regen, ADRs, scaffold)
End session → Clear transcript, save to memory/2026-07-17.md

# Day 2+: Continuation (any length)
Session starts with:
- Current context from HANDOFF.md reference
- Skills available via skill_workshop tool
- No need to re-evaluate decisions (MEMORY.md + skills persist)
```

## Related Skills

- `project-regeneration` — Clean slate pattern for starting fresh
- `adr-framework` — Decision tracking independent of conversation context
- `session-closure` — HANDOFF.md creation ritual

## Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Token consumption/week | <50,000 total (6 sessions/day) | Memory + transcript size |
| Session duration | 2-4h typical | Calendar events |
| Skills persistence rate | 100% available next day | Check skills/ folder exists |

## Constraints

- Cannot override user's explicit memory preferences for session context
- Skills must remain in `skills/` folder (not conversation-dependent)
- HANDOFF.md mandatory before clear action; SUMMARY.md required if compressing

## Output Format

At session close, provide:
```
✅ Handoff complete: skills persisted, context strategy chosen
   - Strategy: clear after handoff / compress periodically
   - Skills available: project-regeneration, adr-framework, workspace-scaffold  
   - Next session reference: MEMORY.md path + HANDOFF.md current state
```
