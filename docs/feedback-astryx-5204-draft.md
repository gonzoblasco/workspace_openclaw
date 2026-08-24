# Borrador feedback - astryx PR #5204

> fix(richtext): close all 8 RichTextEditor audit BLOCKs - @AKnassa
> Estado: OPEN, sin reviews humanos.

---

## Comentario propuesto (en inglés, para el PR)

Hi @AKnassa, this is a model audit-close-out - fixing the root cause (lint coverage) rather than just the symptoms is exactly the right instinct, and the mutation probes give real confidence the tests guard the load-bearing behaviours. A few observations:

**1. The read-only vs disabled split (BLOCK 3) is exactly the model that should be the norm - worth calling out as the pattern.**
Separating read-only (stays in the tab order, `aria-readonly`, full opacity, keyboard-reachable) from disabled (leaves the tab order, `aria-disabled`, dimmed) is the correct ARIA contract, and the fact that `contenteditable` now follows prop changes post-mount (`initialConfig.editable` only being read at mount was the subtle bug) closes the gap where the announcement could contradict actual editability. That's the kind of detail that makes an a11y fix trustworthy - a SR user is told one thing while the control behaves differently. The tests pinning `contenteditable` to `aria-readonly`/`aria-disabled` consistency are the right guard. This is the model worth propagating to the rest of the library (it's the same distinction some other components blur between busy and disabled).

**2. The hit-target fix (BLOCK 4) correctly distinguishes the two WCAG bars - good.**
Moving the block padding onto the combobox button (the element hit-target audits actually measure) with `align-self: stretch` is the right structural fix, and keeping 24px for fine pointers (2.5.8 AA) while applying 44px only on `@media (pointer: coarse)` respects the fact that 44px is a touch-target best practice, not a universal floor. Worth confirming the 44px floor also applies to the toolbar controls you mention (the body says they follow the Slider precedent) - the toolbar's the place where a keyboard/touch user actually reaches for formatting controls.

**3. The "close all 8 BLOCKs" framing undersells the axe cleanup.**
You note the audit estimated ~10 axe baseline entries and a fresh run resolved 13 (including the Markdown Serializers story's unlabeled textarea). That's a good sign the audit underestimates - but it also means there may be more components in the same state (audited, graded, but with more baseline entries than the audit predicted). Worth a note in the follow-up that the baseline-vs-audit delta should be checked across other audited components, not just richtext.

**4. Small thing: the projected 78/C after closing the BLOCKs leaves a lot of headroom.**
The audit graded 62.3/D and closing the BLOCKs projects ~78/C. That's a big jump but still a C - which is the honest place to park it, since the remaining gap (whatever isn't a BLOCK) may include contrast/perf/robustness items that are a different scale. Just flagging that "closed the BLOCKs" is a milestone, not the finish line - worth an explicit follow-up issue for the path from C to A rather than letting it linger.

Overall: a strong, well-tested close-out. The BLOCK 3 read-only/disabled model and the root-cause lint coverage are the standout pieces, and they're the ones with the most library-wide leverage.

---

## Notas internas para Gonzo

- **Punto 1 (el de mayor valor):** BLOCK 3 es exactamente el modelo que Gonzo defendió en #4871 (busy/disabled no es lo mismo que disabled). Y el detalle fino: `contenteditable` sigue props post-mount, cerrando el gap donde el anuncio contradecía la editabilidad real. Es el patrón a propagar. Valido con sustancia porque es mi terreno.
- **Punto 2:** el fix de hit target distingue bien 24px (fine, 2.5.8) vs 44px (coarse, best practice). DESCARTÉ la falsa inconsistencia que sospeché (el body dice "44px floor" y el código usa ambos correctamente - no era bug). Sí pregunto si el 44px cubre también los toolbar controls.
- **Punto 3:** el delta baseline-vs-audit (13 vs 10 estimados) sugiere que otros componentes auditados podrían estar subestimados - vale un check en el follow-up.
- **Punto 4:** el 78/C proyectado deja mucho headroom - "closed the BLOCKs" es un milestone, no el finish line. Sugerir follow-up explícito C→A.
- **Tono:** muy positivo (es un PR fuerte), con sustancia en los puntos donde el trabajo conecta con expertise previo (read-only/disabled) y presión suave para no perder el follow-up del path C→A.
- **Estado:** sin reviews humanos aún.
