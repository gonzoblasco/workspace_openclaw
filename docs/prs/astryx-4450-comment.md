<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# meta/astryx#4450 - comentario de corrección de estado

**Fecha:** 2026-11-03
**Issue:** https://github.com/meta/astryx/issues/4450
**Comentario publicado:** (ver abajo el cuerpo exacto)
**Contexto:** corrección del comentario del 2026-07-31 que declaraba el issue arreglado en #4604. #4604 se cerró sin merge.

## Evidencia verificada contra `main` (`aa4bd1d`)

| Dato | Verificación |
|---|---|
| Trigger sin rol con `hasSearch` | `Selector.tsx:2111`, `MultiSelector.tsx:2665`: `role={isEffectivelyReadOnly \|\| !hasSearch ? 'combobox' : undefined}` |
| `aria-required` en el trigger | `Selector.tsx:2012`, `MultiSelector.tsx:2486` - llega, pero Chromium lo descarta en `button` |
| #4604 cerrado sin merge | `state: closed`, `merged: false`, `closedAt: 2026-08-06` |
| El reviewer tenía razón | `imdreamrunner`: el `<label for>` nativo ya da el nombre; el `aria-labelledby` explícito no aportaba |
| Asociación nativa presente | `FieldLabel.tsx:323` `htmlFor={isGroupLabel ? undefined : inputID}`; `triggerId` es el id de la `<button>` |
| `fieldLabelId` en main | `Selector.tsx:1149`, condicionado en `:2227` a `ariaLabelledByProp != null` |
| Decisión de #3402 | `ac17c7fc2` (2026-07-02): *"the trigger is a plain button that opens the listbox - not a second combobox"* |
| Aserciones que la fijan | `Combobox.a11y.states.ts:122`, `Selector.test.tsx:222/:794/:1119/:1635`, `SelectorListboxName.a11y.chromium.spec.ts:43` |
| Handoff de MultiSelector | `MultiSelectorRenderTriggerProps` sin `role` / `aria-required` / `aria-disabled` (ComplexSelector los tiene desde #6991) |

## Cuerpo publicado

> My 31 July comment above said this was fixed. It wasn't, and that comment is wrong. #4604 was closed unmerged: the reviewer's point stands - the native `<label for>` association already names the trigger, so the explicit `aria-labelledby` added nothing - and nothing in that PR ever touched `required` or `value`. The issue should not have been reported as closed. Both effects duytbp lists are still on `main` (`aa4bd1d`), at [Selector.tsx:2111](https://github.com/meta/astryx/blob/aa4bd1d/packages/core/src/Selector/Selector.tsx#L2111) and [MultiSelector.tsx:2665](https://github.com/meta/astryx/blob/aa4bd1d/packages/core/src/MultiSelector/MultiSelector.tsx#L2665), and I can reproduce them from the repro above.
>
> A third one, same root cause, and worth fixing in the same patch: with `renderTrigger`, `MultiSelector` cannot be repaired by the caller at all. `MultiSelectorRenderTriggerProps` hands back `aria-haspopup`, `aria-expanded`, `aria-controls`, `aria-busy` and `aria-readonly` - but no `role`, no `aria-required`, no `aria-disabled`. `ComplexSelectorRenderTriggerProps` gained all three in #6991, so a caller-owned control there can be a combobox; here it has to guess. Whatever you decide about the trigger role, the handoff should carry the same set.
>
> On the fix itself, `role="combobox"` on the search trigger as #6991 did is the right end state, but it is not a one-line change, and I don't think it should be presented as one. #3402 (`ac17c7fc2`) deliberately removed that role - *"the popup's search input is the combobox … the trigger is a plain button that opens the listbox - not a second combobox"* - and the decision is pinned in five places:
>
> - `Selector/__tests__/Combobox.a11y.states.ts:122` - the `Selector trigger with hasSearch` exclusion
> - `Selector/Selector.test.tsx:222`, `:794`, `:1119`, `:1635` - every hasSearch test locates the trigger as `getByRole('button')`, three of them with the comment *"the trigger is a plain button, not a combobox"*
> - `Selector/__tests__/SelectorListboxName.a11y.chromium.spec.ts:43` - *"The searchable trigger is a plain button until the list opens"*
>
> ARIA 1.2 only says the value belongs to the text input in an *editable* combobox; it doesn't forbid a second combobox, but it doesn't bless this one either. So the choice between "make the trigger a combobox" and "keep #3402's model and expose value/required another way" is a design decision for whoever owns that record, not something the bug report settles.
>
> Whichever way it goes, `required` is the one that bites hardest today: under `FormLayout defaultOptionality="required"` the searchable trigger reports nothing at all, while the plain selector beside it reports `required: true`.

## Notas de edición

- Se descartó el registro "ups / my bad": el error no fue un detalle faltante en #4604 sino el cierre del PR y el comentario que lo declaró arreglado, dentro de la misma semana.
- Cuatro líneas explícitas en vez de "around :794": el comentario pide trabajo, debe quedar a un `grep` de distancia.
- Links fijados a `aa4bd1d` (HEAD al momento de escribir) para que las líneas coincidan con lo citado.
- `voz-gonzo.md` no aplica: GitHub es inglés técnico (`USER.md` + `AGENTS.md`), y su registro lo excluye explícitamente.
