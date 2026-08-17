# LEARNINGS — kanam-story

## 2026-08-16 — U3 chat-assisted global outline (v0.10.0 → v0.10.2)

CONTEXT: Implementing a chat-assisted global outline replacement where the agent proposes a full new chapter+beat structure.

REFLECTION: I initially wanted to avoid touching existing scenes, assuming an outline replacement could be pure metadata. The DB schema and `chaptersDB.delete` cascade proved otherwise: deleting a chapter also deletes its scenes. To preserve manuscript, I had to explicitly orphan scenes (`chapterId: ''`) before deleting old chapters.

LESSON: When an action crosses entity boundaries (chapters → scenes), check cascade behavior in the DB layer early. Pure-state undo also needs key preservation; use `put` with original ids instead of `create` when restoring snapshots.

BIASES DETECTED: Anchoring on "don't touch scenes" delayed the cascade check. The constraint came from the data model, not from user intent, and should have been validated sooner.

## 2026-08-16 — Self-review U4 + botones (v0.11.1 → v0.11.2)

CONTEXT: Después de cerrar U4 y v0.11.1, hicimos un code review propio y revisamos la deuda técnica.

FINDINGS:
1. `OutlineView` definía `orphanScenes` como "escenas sin beats", no "escenas sin capítulo". El panel global de huérfanas mostraba escenas que tenían capítulo pero no beat, duplicando el concepto local de `ChapterSection`. Corregido a `chapterId === ''`.
2. `btn-outline-danger` (Bootstrap default) sobre fondo blanco del tema claro no cumple WCAG AA (2.78:1). Es un problema global, no solo del outline; hay que decidir si se customiza el danger o se acepta el default de Bootstrap.
3. Botones de icono con label (`btn-icon-label`) no tenían `type="button"` explícito. Agregado.
4. El test `lib/db.test.ts` que estaba marcado como "flaky / beforeEach a medias" ahora pasa establemente en 5 corridas; probablemente se resolvió en commits anteriores. Verificación directa lo confirma.

LESSON: Nombres como "orphan" son cargados; hay que validar la condición real (`chapterId === ''` vs `beats.length === 0`) antes de renderizar UI. Un self-review inmediatamente después de mergear atrapa estos errores de modelado.

BIASES DETECTED: Reutilicé el nombre "orphan" sin verificar la condición exacta, asumiendo que coincidía con el caso post-`replace_outline`.
