# LEARNINGS — kanam-story

## 2026-08-16 — U3 chat-assisted global outline (v0.10.0 → v0.10.2)

CONTEXT: Implementing a chat-assisted global outline replacement where the agent proposes a full new chapter+beat structure.

REFLECTION: I initially wanted to avoid touching existing scenes, assuming an outline replacement could be pure metadata. The DB schema and `chaptersDB.delete` cascade proved otherwise: deleting a chapter also deletes its scenes. To preserve manuscript, I had to explicitly orphan scenes (`chapterId: ''`) before deleting old chapters.

LESSON: When an action crosses entity boundaries (chapters → scenes), check cascade behavior in the DB layer early. Pure-state undo also needs key preservation; use `put` with original ids instead of `create` when restoring snapshots.

BIASES DETECTED: Anchoring on "don't touch scenes" delayed the cascade check. The constraint came from the data model, not from user intent, and should have been validated sooner.

## 2026-08-16 — U4 orphan scene panel (v0.11.0)

CONTEXT: Scenes orphaned by `replace_outline` had `chapterId: ''` and were not visible anywhere in the outline.

REFLECTION: The existing ChapterSection already had a local "orphan" concept for scenes inside a chapter that had no beats. That was a different problem. The real orphan after outline replacement is the scene with no chapter. A dedicated global panel avoids silent data loss and gives the user a recovery surface.

LESSON: Reuse component names and concepts carefully. "Orphan" can mean different things in different contexts (no beat vs no chapter). Clarify the entity relationship before naming the UI.

BIASES DETECTED: I assumed the existing orphan UI already covered the post-replacement case because the prop was named `onLinkOrphan`. The name primed me to think the work was partially done.
