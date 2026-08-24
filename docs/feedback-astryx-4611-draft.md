# Borrador feedback - astryx ISSUE #4611 (scoping RFC)

> Table: plugin for grid focus + variant-aware grid semantics - @humbertovirtudes
> Estado: OPEN, 0 comentarios. RFC de scoping explícito (5 decisiones).

---

## Contexto clave que conecta (NO repetir en el comment)

Este RFC es **complementario** al PR #4690 que está en curso (AKnassa implementando treegrid):
- En el #4690, AKnassa ya definió el plan de `useTreeGridFocus` (roving tabindex row focus, role="treegrid" via transformTable, aria-posinset/setsize desde la lista aplanada).
- cixzhang señaló que `useTreeFocus` + `useGridFocus` (hooks públicas con docs y tests) son las referencias a componer.
- Yo aporté en el #4690 el marco AT para row-focus vs cell-navigation (cada opción mapea a contrato ARIA distinto; la pregunta decisiva es si los in-cell widgets son parte del contrato).

El #4611 pregunta cosas que ya tienen respuesta parcial en el #4690. El comentario debe CONECTAR, no duplicar.

---

## Comentario propuesto (en inglés, para el issue)

This RFC overlaps with work already in motion on #4690 (AKnassa's treegrid implementation, with `useTreeGridFocus` planned and `useTreeFocus` + `useGridFocus` identified as the hooks to compose). Worth anchoring the scoping here to that so we don't design in a vacuum. A few decisions that would help close this out:

**1. On "generalize `useGridFocus` vs table-native focus manager" (decision 3):** the #4690 thread already points at composing `useTreeFocus` + `useGridFocus` for the treegrid case. I'd argue the plugin should build on those shared hooks rather than introduce a table-native manager - it keeps the roving-tabindex keyboard logic in one place instead of forking it per component (the Calendar-scoped `useGridFocus` is already the precedent). The plugin then becomes the table-aware *semantics layer* (roles, aria-rowcount/colcount, colindex, the roving state wired to cells), with the keyboard engine staying shared.

**2. On the plugin surface (decision 1):** I'd lean toward one plugin with a `semantics: 'grid' | 'treegrid'` option rather than separate plugins. The two share the core roving-tabindex engine (the #4690 treegrid is "grid plus expand/collapse + hierarchy"), so splitting them would duplicate the focus machinery. The variant switch is where they differ (arrow-key model, aria-level/expanded, setsize/posinset). Worksheet/spreadsheet is the exception - its cell-range selection + type-to-edit model is different enough to warrant its own track (decision 2), so keep it out of this plugin.

**3. The deciding question for the focus model (from the #4690 AT discussion):** whether `grid`/`treegrid` rows carry in-cell interactive widgets (sort headers, chevrons, selection checkboxes) as part of the contract. If yes, the roving model needs to be cell-level (APG grid pattern) so those widgets stay reachable; if v1 rows are plain data cells with the expander as sole interaction, row-focus is simpler. This should be decided *in this RFC* since it determines the keyboard model and the aria-colindex emission - and it's the same decision that's currently queued with maintainers on #4690.

**4. On conformance (decision 4):** tie the acceptance criteria to the APG grid + treegrid patterns explicitly (roving tabindex, arrow navigation, expand/collapse, setsize/posinset), and make the conformance tests reference the WCAG/APG clause by number per the #4475 tracker convention - so the plugin's coverage is traceable to a spec clause like the rest of the program.

This would let the RFC close with a concrete, implementable scope that aligns with the treegrid work already underway instead of running parallel to it.

---

## Notas internas para Gonzo (NO publicar)

- **El valor principal:** conectar el #4611 con el #4690 (el RFC pregunta cosas que ya tienen respuesta en el trabajo en curso de AKnassa). Evita que el scoping se diseñe en el vacío y alinea el RFC con la implementación que ya arrancó.
- **Decisiones que aporto criterio:**
  1. (d3) Generalizar useGridFocus + useTreeFocus (componer hooks compartidas) en vez de focus manager table-native.
  2. (d1) Un plugin con opcion semantics grid/treegrid, no plugins separados (comparten el motor roving).
  3. (d2) Worksheet/spreadsheet = track separado (modelo distinto).
  4. (d4) Conformance atada a APG + convencion del #4475 (traza a clausula WCAG/APG).
- **Conecta con mi comment del #4690:** la pregunta decisiva del focus model (row vs cell, si in-cell widgets son parte del contrato) es la misma que deje queued con maintainers en el #4690 - la traigo aca como decision del RFC.
- **Riesgo a evitar:** NO repetir el plan de AKnassa ni las referencias de cixzhang (ya estan dichas en el #4690) - solo referenciarlas como ancla.
- **Tono:** constructivo, ayuda a cerrar el scoping con algo implementable y alineado al trabajo en curso.
- **Estado:** 0 comentarios - este seria el primero en definir el RFC.
