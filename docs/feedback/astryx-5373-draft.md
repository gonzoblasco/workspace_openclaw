# Borrador feedback - astryx PR #5373

> Improve Popover responsive fit and focus behavior - @rubyycheung
> Estado: OPEN, sin reviews humanos.

---

## Comentario propuesto (en inglés, para el PR)

Hi @rubyycheung, this is a thorough PR - the decision table in the body makes the responsive trade-offs legible, and the positive *and* negative tests (fitting content is not clipped, overflowing content scrolls) are the right shape.

The focus work is the part I'd want to pressure-test hardest, since it changes how a dialog-style Popover announces itself. A few things:

**1. The `tabIndex={-1}` dialog container is exactly the case that needs a real AT pass - worth tightening the "Blocked" note before merge.**
Your own readiness table flags iOS VoiceOver/top-layer as *Blocked / not verified*. That's the honest call to make, but this specific pattern (focus a `role="dialog"` container with `tabIndex={-1}` + `aria-modal` when there are no content controls) is where screen readers diverge most. In practice: when a user Tabs into a programmatically-focused dialog container, some SR/AT combos announce the `aria-label` ("dialog, [name]"), but others try to announce the full content region or announce nothing meaningful on a focus that landed on a container rather than a control. Since the whole point of this change is a predictable initial-focus target for read-only content, I'd suggest validating at minimum: NVDA + Chrome, and VoiceOver + Safari, on the "Read only" story - confirming (a) the dialog name is announced on open, and (b) the first Tab moves into the cycle rather than being announced as a jump to an unrelated region. If VoiceOver can't be run before merge, that's fine, but I'd flag it as a follow-up rather than a silent "not verified", because a wrong announcement here is a worse outcome for the user than the previous behaviour.

**2. The new `useFocusTrap` branch relies on `focusable` being non-empty - worth an explicit guard.**
The added block (`if (document.activeElement === container)`) runs after `const first = focusable[0]; const last = focusable[focusable.length - 1];`. If `focusable` can be empty at that point (the trap container focused with no tabbable descendants - the read-only case this PR targets, since the fallback close control is retained but the container is the focused element), then `last` is `undefined` and the Shift+Tab branch calls `last.focus()`. There's an existing test for "trap has no tabbable controls" so there may be an early return above - but if so, an explicit `if (!focusable.length) return;` right before the new block would make that dependency obvious to the next reader instead of implicit.

**3. Measurement cost: two observers + window listeners on every open.**
The `PopoverSurface` registers a `ResizeObserver` + `MutationObserver` (subtree) + `load`/`resize`/`visualViewport` listeners, and re-measures on every `children` change. For a Popover that's fine on open, but if a Popover's content re-renders frequently while open (live-updating lists, form validation state), the mutation observer on `subtree: true` fires on every DOM change inside it. Worth a quick check that this doesn't add measurable jank on a fast-updating Popover - and if it's a concern, throttling `measureOverflow` with `requestAnimationFrame` (coalescing multiple observer callbacks into one measure) is a cheap guard.

**4. Consistency with the HoverCard/popup contract - good to see the `aria-haspopup="dialog"` preserved.**
The trigger still signals `aria-haspopup="dialog"` and the `FOCUSABLE_SELECTOR` is reused - coherent with how a dialog-style popup should be exposed. One nit: the read-only dialog container gets `tabIndex={-1}` only when `role === 'dialog'`. If a Popover uses `role="none"` with a menu inside (the story you added), the container won't get the programmatic focus target - which is correct, since the menu has focusable items. Just confirming that's the intended split and not a case where `role="group"`-style content with no controls could still lose its initial focus.

Overall: strong work on the sizing/overflow, and the focus fix addresses a real loss-of-place bug. The main ask is to tighten the AT-verification story for the container-focus case and make the empty-`focusable` dependency explicit.

---

## Notas internas para Gonzo

- **Punto 1 (el de mayor peso):** el PR declara "iOS VoiceOver/top-layer: Blocked - not verified". El patrón de enfocar un container dialog con `tabIndex={-1}` + `aria-modal` es donde las SR más divergen (algunas anuncian el aria-label, otras intentan anunciar todo el contenido, otras nada útil). Sugerencia: validar NVDA+Chrome / VoiceOver+Safari en la story "Read only", o al menos marcarlo como follow-up explícito en vez de "not verified" silencioso.
- **Punto 2:** el nuevo branch en useFocusTrap corre después de `const first/last = focusable[...]`. Si `focusable` está vacío (caso read-only, que es justo el que introduce este PR), `last.focus()` con `last === undefined` explotaría en Shift+Tab. Hay un test "trap has no tabbable controls" que sugiere early-return previo, pero no tengo el código base completo (no tengo el repo clonado) para confirmarlo - por eso lo planteo como "worth an explicit guard" honesto, no como bug afirmado. Podría verificar clonando el repo si Gonzo quiere certeza.
- **Punto 3:** 2 Observers + listeners + re-measure en cada `children` change - costo en Popovers con contenido que re-renderiza seguido. Sugerencia: rAF-throttle. Sanity check, no blocker.
- **Punto 4:** el split role="dialog" (con container focusable) vs role="none"/menu (sin container focusable) es correcto - solo confirmar que es intencional.
- **Tono:** reconociendo que el PR es fuerte en sizing/overflow, presión focalizada en el focus/AT que es lo que cambia el contrato. Punto 1 es el de mayor valor (el autor mismo dejó la puerta abierta con "Blocked").
- **Estado:** sin reviews humanos aún.
