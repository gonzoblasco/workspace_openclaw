# LinkedIn Post - astryx #5419 (PUBLISHED)

**Status:** PUBLICADO 25/08/2026
**Idioma:** inglés
**Tono:** pedagógico con sustancia - historia técnica con el qué + el proceso + el porqué. **NO es tutorial paso a paso.**
**Rol:** EJEMPLO CANÓNICO del estilo de marca de Gonzo para posts de LinkedIn (la politica de los 3 nichos vive en `memory/user-profile.md` linea 47).
**Nicho:** a11y
**Resultado:** alcanzó a Darren Denham (CPACC, Assistant Director de Digital Accessibility, Univ. Central Oklahoma, 21 años en a11y) que comentó validando el enfoque.

---

## Post (versión publicada)

I just got a PR merged into **astryx**, Meta's React component library, that fixes a subtle **#a11y** bug in `HoverCard`. 🌿

The problem: when a HoverCard had a label, the trigger used `aria-describedby` to point at the dialog. That flattens structured content into a plain-text description - so a **screen-reader** user on the trigger heard the dialog's contents read as a description, instead of being told "this opens a dialog".

The fix uses the correct **popup contract** when a label is present:
- `aria-haspopup="dialog"` on the trigger
- `aria-controls` pointing at the layer id
- `aria-expanded` synced to the open state

I also exposed `id` and `isOpen` from `useHoverCard` so consumers can wire `aria-controls` / `aria-expanded` themselves, and kept `describedBy` as a deprecated alias for **backwards compatibility**.

One decision worth noting: I considered `aria-details`, but support across **screen readers** is still inconsistent. `aria-haspopup="dialog"` + `aria-expanded` is the most broadly supported contract for a **non-modal dialog** opener.

**38 tests passing.** Typecheck and build green. And the review process was solid - three inline comments, all addressed.

PR: https://github.com/facebook/astryx/pull/5419

I'm not stopping there - I've got a follow-up in review fixing the same class of dropped accessibility attributes in `List` / `TreeList`.

#accessibility #a11y #openaccessibility #assistivetechnology #inclusivedesign #webdev #reactjs #typescript #opensource #frontendengineering #componentlibrary #uiux #screenreader #inclusive #frontend
```

---

## Por qué este post es el modelo canónico (anatomía del estilo)

1. **Abre con el problema desde la perspectiva del usuario** (el screen-reader user que escucha el contenido como descripción, no "esto abre un diálogo"). Relatable, muestra que entendés la a11y de verdad.
2. **Explica el fix con el criterio detrás** - no "agregué aria-haspopup", sino "el fix usa el popup contract correcto". Nivel senior, no tutorial.
3. **Incluye la decisión de ingeniería** (`aria-details` descartado por soporte inconsistente entre screen readers). Esto es lo que demuestra criterio real de a11y, no compliance checkbox. Es EL momento que conectó con el CPACC.
4. **Muestra el proceso** (3 inline review comments, 38 tests) sin convertirlo en instrucciones.
5. **Cierra con trabajo en curso** (#5493) - demuestra constancia, no es un one-hit wonder.
6. **Tags en el cuerpo** (no amontonados al final) para alcance del nicho.

## Notas para futuros posts

- **Formato:** historia técnica con gancho + problema + decisión con criterio + cierre con constancia. ~250-350 palabras.
- **NO** instrucciones paso a paso (eso es tutorial de juniors, no nuestro estilo).
- **Guion comun** en todo el texto (sin em dash), regla dura.
- **Links:** PR + issue relacionados.
- **Enlaces del PR:** https://github.com/facebook/astryx/pull/5419 | Issue: https://github.com/facebook/astryx/issues/5049
```

---

*Referencia del estilo de marca - 2026-08-25. Ver `memory/user-profile.md` (estrategia de 3 nichos) y daily 2026-08-25.*
