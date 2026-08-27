# Borrador feedback - astryx PR #4690

> fix(Table): drop row tree ARIA outside treegrid - @AKnassa
> Estado: OPEN, CHANGES_REQUESTED de cixzhang (sugiere useTreeGridFocus).

---

## Contexto del debate

- **cixzhang (CHANGES_REQUESTED):** "el fix quizá debería ser aplicar treegrid cuando hay tree data. Necesitaríamos useTreeGridFocus para los behaviors correctos. Es bastante trabajo."
- **AKnassa (defensa en el body):** "Treegrid contrata el modelo grid completo (roving tabindex, arrow-key cell nav, focusable cells), que BaseTable no implementa. Meter ahí a los SR users en un widget innavegable. Construir ese modelo es decisión de feature, no este fix. Para groupedRows es semánticamente incorrecto (group headers son separadores de flat data, no tree parents)."

---

## Comentario propuesto (en inglés, para el PR)

Hi @AKnassa - this is the right call, and I want to add the ARIA-level argument that makes removing the row attributes more than just "axe compliance": an invalid `aria-expanded`/`aria-level` on a `<tr>` inside a native `<table>` isn't merely flagged by axe - it actively degrades the AT experience. Screen readers that honor these attributes on a non-treegrid row will announce expand/collapse state (or depth) that the surrounding semantics don't support, which is more confusing than no announcement at all. Dropping them is the correct degradation - a silent, well-behaved flat row beats a row that tells the user things the widget can't deliver on.

On cixzhang's point about `useTreeGridFocus`: I'd agree it's a legitimate *feature* direction, but I'd push back on it as a *blocker* for this fix. The two are different scales of work:

- This PR is a correctness fix: remove ARIA that's invalid in the current semantics, and stop shipping a broken contract. It makes the shipped state *better* (no false announcements), with a small, reviewable diff.
- `useTreeGridFocus` is a feature: adopting the full APG grid/treegrid keyboard model (roving tabindex, arrow-key cell navigation, focusable cells, `aria-rowcount`/`aria-colcount`) - which, as you note, BaseTable doesn't implement today. That's a design + implementation effort that shouldn't ride along in an a11y cleanup.

Landing the correctness fix first (this PR) and tracking `treegrid` semantics as a follow-up is the right sequence: you ship the non-regression now, and the grid model can be designed properly on top without the pressure of an audit burn-down.

**But I'd elevate one thing you flagged as a "follow-up candidate" to a first-class requirement:** the trade-off that tree depth is now conveyed *only* by indentation, with no programmatic cue. You mention announcing the level through the expander's accessible name. I'd argue that's not optional polish - it's the difference between a usable and an unusable tree for SR users. A two-level tree where the SR user can't tell parent from child is a real functional gap, not a nice-to-have. So I'd frame the follow-up as: "announce depth via the expander's accessible name (or a `role="tree"`-scoped alternative) so hierarchy remains discoverable" - and ideally track it as an issue from this PR, not just a note in the changeset, so it doesn't get lost.

Also confirming the groupedRows call is sound: group headers as flat-data separators (not tree parents) is semantically correct - the removed `aria-expanded` was wrong there for a different reason than in the tree plugin, and the chevron already carries the state.

---

## Notas internas para Gonzo

- **Ángulo que aporto (el que nadie dijo):** el ARIA inválido en un `<tr>` de `<table>` nativo no solo es "axe compliance" - **degrada activamente la experiencia AT** (las SR anuncian expand/depth que el widget no soporta, más confuso que nada). Por eso quitar es la degradación correcta, no solo limpiar un flag.
- **Posición sobre el debate cixzhang vs AKnassa:** no tomo partido por uno - digo que ambos tienen razón a distinta escala: cixzhang tiene razón en que treegrid es la dirección correcta de feature; AKnassa tiene razón en que no debe bloquear este fix de correctitud. La secuencia correcta es landear el fix primero + trackear el feature como follow-up.
- **El punto de mayor valor:** elevar el follow-up de AKnassa (anunciar depth) de "opcional" a "requisito de primera clase" - un tree de 2 niveles donde el SR user no distingue parent de child es un gap funcional real, no polish. Sugerir trackearlo como issue, no solo nota en el changeset.
- **Validación:** el punto de groupedRows (separadores vs tree parents) es correcto.
- **Tono:** apoyo la dirección del autor (el fix es correcto) pero sumo el ángulo ARIA que lo refuerza, y presiono para que el follow-up del depth no se pierda. No desestimo a cixzhang - lo enmarco como feature legítima a distinta escala.
- **Estado:** CHANGES_REQUESTED - este feedback puede ayudar a destrabar el debate (le da al maintainer un argumento de por qué el fix de correctitud debe landear, y al autor la presión para no perder el depth).
