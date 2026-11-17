# Long-form: The Quieter Announcement

**Status:** BORRADOR, no publicado
**Fecha:** 2026-11-16
**Idioma:** inglés (materia a11y)
**Nicho:** a11y (diferenciador)
**Destino propuesto:** blog propio o dev.to; los posts de LinkedIn ya publicados (#10503 y #10554) pasan a ser los cortos que apuntan acá.
**Por qué existe:** los dos posts de LinkedIn sobre react-spectrum son notas de 300 palabras. No hay pieza larga que un comprador pueda leer en cinco minutos y que sostenga una landing.
**Reglas aplicadas:** sin em-dash (`scripts/check_em_dash.py`), historia técnica con criterio, sin tutorial paso a paso, hechos copiados de `memory/career-facts.md` §5.1.

---

## The Quieter Announcement

I once fixed a screen reader bug by deleting an announcement.

That sounds backwards, and it is the point. On the surface, the change was small: 41 lines added, 80 removed, one hook, two test files, merged into Adobe's React Spectrum in October. What it revealed is that most accessibility work is aimed at the wrong target.

### What the user heard

A ComboBox with sections. You open it, you arrow down through the options. VoiceOver, on macOS and iOS, speaks each item as you move through it: the label, the role, the position, and whether it is currently selected.

That is a rich announcement. It is also, in a very literal sense, a gift. The browser and the screen reader cooperated to produce it.

Then React Spectrum overwrote it.

The `useComboBox` hook carried a workaround, and the comment above it explained why it existed:

```ts
// VoiceOver has issues with announcing aria-activedescendant properly on change
// (especially on iOS). We use a live region announcer to announce focus changes
// manually.
```

An `aria-activedescendant` pattern moves focus in the accessibility tree without moving real focus. Some screen readers historically did not follow that movement reliably, so the library announced each change by hand, through a live region, to be safe.

The workaround was correct when it was written. It stopped being correct when VoiceOver started announcing per item details natively. And once both things were happening at the same time, they did not cooperate. They competed.

The live region fired on every focused item change and replaced the native speech with a single string: the item name. So instead of hearing "Pricing, menu item, 3 of 12, selected", a user heard "Pricing", and then moved on.

Less information, delivered more urgently. Which is the definition of a regression that hides.

### Why nothing caught it

Run that page through axe. Everything passes.

The combobox has the right role. `aria-expanded` is synced. `aria-controls` points at the right listbox. The options carry `aria-selected` and `aria-posinset`, and the `aria-setsize` matches. The live region exists, is not hidden, and is not empty. Every attribute a linter knows how to check is either present or not applicable.

The bug lived somewhere no linter looks: in the collision between two things that were each individually correct.

Accessibility, at that layer, is not a property of the markup. It is a property of the runtime, and more specifically it is a property of what a person actually hears. Markup is the input to that. It is not the thing itself.

### The fix

The announcement was still needed for one narrow case: moving into a new section, where VoiceOver stays quiet and the section title and option count would otherwise be lost. So the gate became the section, not the item.

```ts
if (isGroupChange) {
  const announcement = stringFormatter.format('focusAnnouncement', {
    isGroupChange: true,
    groupTitle: sectionTitle,
    groupCount: section ? [...getChildNodes(section, state.collection)].length : 0,
    optionText: focusedItem['aria-label'] || focusedItem.textValue || '',
    isSelected
  });

  announce(announcement);
}
```

Everything else stays silent and lets the platform speak. Arrowing through a section: native speech, intact. Arrowing to the selected item: native speech, intact. Entering a section: one manual announcement with the section title and the option count, then out of the way.

The review was the hard part, and it was the interesting part. I had updated the combobox tests to assert that per item navigation no longer triggers a manual announcement. The maintainer pushed back twice. The first version, in their reading, was `not.toHaveBeenCalled` wearing a costume. The second round asked what those tests covered that nothing else did. The answer, eventually, was nothing. Once the announcement moved to section changes, the tests had nothing left to assert, and they were removed. The suite ended at 259 tests across two packages.

I shipped a smaller diff than I opened, and the PR was better for it. That is not the instinct most people have.

### The second failure, which was mine

A month earlier I had merged a test only PR into the same repository, locking in that `aria-posinset` stays global across menu sections. Four items across two sections must count 1 through 4, matching `aria-setsize=4`. If a section restarts the count, a screen reader announces "item 1 of 2" when the truth is "item 1 of 4".

React Spectrum was already doing it right. Nothing guaranteed it. So the test was there to make sure a future refactor could not quietly break it.

My first version of that test was worthless.

The helper I used to build the fixture flattened the sections into a plain list of items. The DOM that the test rendered never contained the sectioned structure the test claimed to cover. It went green. It was decoration. A maintainer spotted it in seconds.

The corrected version renders each section through the real hook, including labelled groups and their headings, and also covers the section without a heading, where the accessible name comes from `aria-label`.

Two PRs, two different mistakes, and the same root cause: I was reasoning about the model in my head instead of the artifact that ships. In the first case I trusted the attribute over the announcement. In the second I trusted the fixture over the DOM.

### The rule I kept

If you want to know whether a component is accessible, do not ask what attributes it has. Ask what a screen reader says when a person uses it. Those are different questions, and only one of them is the product.

Most tooling answers the first question, because the first question is cheap. It can be answered by parsing HTML, and parsing HTML scales. The second question requires running the thing, in a browser, with an assistive technology attached, and reading the output. It does not scale nearly as well. It also happens to be the only one that predicts what a blind user experiences.

That gap is what I ended up building a tool around. Preflight loads a page in a browser, reads its accessibility output the way a screen reader consumes it, and reports what is actually announced rather than what is merely declared.

The demo page in its README has every attribute in place, and two unnamed images and an unnamed button. Valid HTML, clean lint, unusable.

PRs: [adobe/react-spectrum#10503](https://github.com/adobe/react-spectrum/pull/10503) and [#10554](https://github.com/adobe/react-spectrum/pull/10554).
