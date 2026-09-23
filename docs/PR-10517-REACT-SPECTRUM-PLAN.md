# PR adobe/react-spectrum #10517 - Plan de correcciones y respuestas

> Estado: OPEN, `reviewDecision: REVIEW_REQUIRED`, CI verde en head `1b4a15c2f`.
> Titulo: `fix: expose input styling on RAC Checkbox and Radio`
> Rama: `gonzoblasco:fix/checkbox-radio-sr-focus-indicator`
> 6 comentarios inline abiertos de @snowystinger (2026-09-23), ninguno respondido.
> Evidencia: medida en Chromium 153 (chrome-headless-shell) con la estructura real del componente.

---

## 1. Contexto: como llego el PR hasta aca

| Ronda | Decision |
|---|---|
| 2026-08-27 | Primer approach: exponer 4 props de estilo (`inputStyle`, `visuallyHiddenStyle`...). Maintainer: no. Abre el riesgo de romper a11y. |
| 2026-09-02 | Prop unica `hiddenInput="stretch-to-label"`. Maintainer: "get rid of the advanced escape hatch". |
| 2026-09-18 | **Direccion nueva**: usar CSS `anchor` / `target`. Sin props nuevas. Default anclado al elemento externo del componente, override-able. |
| 2026-09-21 | Rework con anchor positioning + hook. Review: "where is the test against people providing their own anchor names?" |
| 2026-09-22 | El test que pidio **exponia un bug real**: los estilos inline `anchorName`/`positionAnchor` ganaban por cascada sobre un `anchor-name` puesto por classname. Fix `9047a70`: hook que lee `getComputedStyle`. |
| 2026-09-23 | 6 comentarios nuevos. Son el objeto de este plan. |

---

## 2. Los 6 comentarios, verificacion y decision

### C1 - `stories/RadioGroup.stories.tsx:73` y `stories/Checkbox.stories.tsx:34`
> "you can drop them" / "same question"

No es pregunta: es decision tomada. Con el anclaje por defecto en cada radio y checkbox, las stories ya no demuestran nada opt-in.

**Decision:** borrar `RadioGroupScreenReaderFocusRing` y `CheckboxScreenReaderFocusRing`.

---

### C2 - `src/Checkbox.tsx:519` (y `RadioGroup.tsx:486`)
> "lets not use Math.random / was there a reason you chose to use this over the earlier useId you were using?"

**Tiene razon, y la causa raiz es real pero la conclusion era equivocada.**

1. `React.useId` **no existe antes de React 18**. El paquete declara `react: ^16.8.0 || ^17.0.0-rc.1 || ^18 || ^19.0.0-rc.1`.
2. Eso rompio CI: en `79e3cc9de` fallaron `test-16` y `test-17`. El commit siguiente, `0cf378d7b`, los paso a verde cambiando a `Math.random` (mensaje: "replace useId with random ID to fix CI tests crash").
3. Pero `Math.random` trae dos problemas: (a) rompe SSR (el valor difiere entre server y cliente, el atributo `style` con `anchor-name` hace mismatch en hidratacion); (b) no es la convencion del paquete.
4. **La salida correcta existe**: `useId` de `react-aria/useId`, que resuelve `React.useId` en 18+ y cae a un contador en 16/17. Ya lo usan `Button.tsx:34`, `Dialog.tsx:44`, `Disclosure.tsx:49`, `Tree.tsx:118`.
5. Hace falta mantener el sanitizador: `React.useId` devuelve `_R_0_` en React 19, pero en React 18 devuelve valores tipo `:r0:` con dos puntos, y dos puntos no es un `<dashed-ident>` valido para `anchor-name`.

**Verificado ademas:** el id unico **no se puede eliminar** del diseno (ver Hallazgo A). Un `anchor-name` por instancia es obligatorio.

**Arreglo:** `useId` de `react-aria/useId` + sanitizador, en Checkbox y RadioGroup.

---

### C3 - `src/hiddenInputAnchor.ts:18`
> "does this need to be a function? or can it be determined at module load time and then just be a value that's referenced?"

**Respuesta: la funcion se va con el hook.** Con el approach de CSS variable (C4) el hook desaparece, y `getAnchorSupport` se va con el.

Si por alguna razon queda un check del lado del src, **tiene que seguir siendo lazy**: una constante evaluada a nivel modulo tambien corre en SSR, donde `CSS` no existe, y congelaria un `false` que el cliente reusaria.

En los browser tests el check se queda, como condicion de skip.

---

### C4 - `src/hiddenInputAnchor.ts:66` (el comentario mas importante)
> "it's not great that every time these components re-render they have to getComputedStyle... I think we should have a css variable that's used for the name."

**De acuerdo, es mejor que lo actual.** `position-anchor: var(--override, <default>)` elimina el layout effect y el `getComputedStyle` por render, y **ademas resuelve la objecion del 2026-09-19** ("css can change without any notification") : el nombre ya no depende de un re-render, lo resuelve la cascada.

**Correccion necesaria (medida):** la variable tiene que leerse **en los dos lados**. Con la variable solo en `position-anchor` del input, un consumidor que declare `anchor-name` por classname sigue enmascarado por nuestro default inline:

| Caso medido | `anchor-name` computado | Cubre |
|---|---|---|
| var solo en el input, consumidor por classname | `--default` (el nuestro) | NO |
| var en host + input | `--consumer` | SI |

```
host:  anchor-name:     var(--<prefix>-anchor, --react-aria-checkbox-<id>)
input: position-anchor: var(--<prefix>-anchor, --react-aria-checkbox-<id>)
```

Medido funcionando en los 3 casos: sin override, override por classname, y override sin default del componente.

**Consecuencia a explicitar (tradeoff, no bug):** con este approach el consumidor overriddea **con la variable**, no declarando su propio `anchor-name`. Es decir, el test de "anchor-name por stylesheet class" de la ronda anterior se reemplaza por un test de la custom property. Si se quiere conservar el soporte de `anchor-name` por classname tal cual, hay que quedarse con el `getComputedStyle` (o con una regla en stylesheet + var, que se puede analizar).

**Precedente en el repo:** ya se exponen variables CSS como API publica; convive con esto.
`--trigger-anchor-point` (`Popover.tsx:327`, `Tooltip.tsx:236`), `--trigger-width`, `--table-row-level`, `--tree-item-level`.

**Naming:** queda a su criterio ("can debate the naming after the changes"). Sugerencia: prefijo `--react-aria-`, consistente con las del repo.

---

### C5 - `src/hiddenInputAnchor.ts:37`
> "is position: 'fixed' needed? why?"

**Si, y es la parte que hace que la asociacion tome efecto.** Medido con la estructura real:

| `position` | Containing block | `anchor()` resuelve | Caja final |
|---|---|---|---|
| `absolute` | dentro del componente (cadena del `.vh`) | NO (usa fallback) | 153x21 (la caja de VisuallyHidden) |
| `fixed` | viewport | SI, por nombre contra el ancla | coincide con el componente |

Con `absolute` los valores usados caian al wrapper: used `top` 0px, used `width` 145px. Con `fixed` el input sale de la cadena de containing blocks y el ancla resuelve por nombre.

**Control que aisla la causa:** con el ancla como **hermana** (no ancestro), `absolute` **si** funciona. Es la relacion de ancestro, no `absolute` en si.

**Y es inerte sin soporte (importante para no romper navegadores viejos):** con los valores de ancla descartados (emulando un browser sin anchor positioning) el input conservo su geometria 1x1 previa de VisuallyHidden; no se convirtio en una caja de viewport.

**Nota:** un ancestro con `transform` no lo rompe (la caja siguio coincidiendo).

---

### C6 - `src/hiddenInputAnchor.ts:40`
> "did we test this with RTL? probably better to use logical directions in which case you could just use inset for all of it"

**Correcto que los tests son solo LTR. Medido en RTL:**

| Approach | LTR | RTL |
|---|---|---|
| `left`/`top` fisicos con `anchor()` | OK | OK |
| `inset-inline-start: anchor(left)` | OK | **ROTO** (el input cae a -208px, un ancho entero al otro lado) |
| `inset-inline-start: anchor(right)` | - | 8px corrido |
| `inset` shorthand | OK | **OK** |

**Conclusion: si a `inset`, no a las propiedades logicas.** `anchor()` toma lados **fisicos**; pasarlo por una propiedad logica invierte el lado en RTL.

**Bonus medido (no preguntado):** con `width: anchor-size(width)` la caja salia **8x6 px mas grande** que el componente (`anchor-size` dimensiona el *content box* y el input suma borde y padding del UA style). El shorthand `inset` da la medida exacta; tambien la da `anchor-size` + `box-sizing: border-box`. El test actual pasa igual porque `covers()` tolera hasta 2px de sobra: no es que la caja sea exacta.

**Arreglo:** pasar a `inset` shorthand + agregar un test RTL.

---

## 3. Hallazgos que no preguntaron pero afectan el diseno

### Hallazgo A - el id unico por instancia es obligatorio (no se puede reemplazar por un nombre estatico)

Medido: con **4 hosts usando el mismo `anchor-name`** y sin `anchor-scope`, **los 4 inputs resolvieron al mismo ancla** (dy 585/533/481/429 respecto de su propio host). Ninguno cubrio al suyo. O sea: nombres duplicados colisionan.

`anchor-scope` lo resuelve (medido OK), pero **no es una alternativa confiable**:

| Browser | anchor positioning | `anchor-scope` |
|---|---|---|
| Chrome | 125+ | **131+** |
| Firefox | 147+ | 147+ |
| Safari | 26+ | 26+ |

Hay una ventana **Chrome 125-130** donde el anclaje funciona pero `anchor-scope` no: ahi los duplicados colisionarian. Conclusion: **seguir con nombre unico por instancia** (de ahi viene la necesidad del `useId` de C2, y el `anchor-scope` no reemplaza el id).

### Hallazgo B - el input con `position: fixed` no sigue el scroll de un contenedor interno

Medido: 6 componentes con nombres unicos dentro de un contenedor con `overflow-y: auto`.

| Momento | Resultado |
|---|---|
| antes del scroll | los 6 cubren al componente |
| `scrollTop = 40` | los 6 quedan **40px corridos** (no siguen) |

Es coherente con que `fixed` saca al input de la cadena del ancestro: queda en coordenadas de viewport y no re-resuelve al scrollear un contenedor interno.

**Necesita confirmacion en browser real (no headless)** antes de tratarlo como bug: el headless shell puede no refrescar el anclaje al scrollear. **Dato fuerte:** el `spike-anchor.mjs` que se saco en `cedc9e3` se llamaba literalmente "Spike v5: scroll tracking + clip disambiguation for fixed+anchor hidden input" - o sea, el scroll tracking ya era un problema conocido en este mismo trabajo.

**Accion:** verificar en Chrome real con VoiceOver; si se confirma, decidir si entra aca o se abre como follow-up (el review ya acepto que las limitaciones de `VisuallyHidden` se atacan de a poco).

---

## 4. Plan de arreglos (orden de ejecucion)

| # | Cambio | Archivo(s) | Responde |
|---|---|---|---|
| 1 | `Math.random` -> `useId` de `react-aria/useId` + sanitizador | `Checkbox.tsx`, `RadioGroup.tsx` | C2 |
| 2 | `inset` shorthand en lugar de `top`/`left` + `anchor-size` sueltos | `hiddenInputAnchor.ts` | C6 |
| 3 | Nombre del ancla por CSS variable, leida en host **y** input; eliminar el layout effect y el `getComputedStyle` | `hiddenInputAnchor.ts`, `Checkbox.tsx`, `RadioGroup.tsx` | C4, C3 |
| 4 | Borrar las 2 stories | `stories/*.stories.tsx` | C1 |
| 5 | Tests: reemplazar el de classname por uno de la custom property; agregar test RTL | `test/Checkbox.sr-focus.browser.test.tsx` | C4, C6 |
| 6 | Verificar scroll en browser real y decidir (aca o follow-up) | - | Hallazgo B |

Nota: el paso 3 hace desaparecer `useHiddenInputAnchor` y `getAnchorSupport`. El archivo `hiddenInputAnchor.ts` queda solo con los estilos, o se fusiona en un helper por componente.

Verificacion antes de pushear: `yarn lint`, `vitest` unit, y `test-browser` (`yarn playwright install && vitest run --config=vitest.browser.config.ts`). CI del repo corre `test-16/17/18` y `test-browser`, que es exactamente donde rompio `useId` la primera vez.

---

## 5. Borradores de respuesta (uno por comentario)

Publicar con: `gh api -X POST repos/adobe/react-spectrum/pulls/10517/comments -f body=@<archivo> -F in_reply_to=<comment-id>`

| Comentario | id | Borrador |
|---|---|---|
| stories (can drop) | `4078195640` | `reply-stories.md` |
| Math.random | `4078205366` | `reply-mathrandom.md` |
| support function | `4078219334` | `reply-supportfn.md` |
| CSS var | `4078278886` | `reply-var.md` |
| position fixed | `4078297514` | `reply-fixed.md` |
| RTL / inset | `4078304825` | `reply-rtl.md` |

Drafts en `/tmp/rs10517-replies/` (revisar antes de publicar; `/tmp` no es durable, mover si hace falta).

---

## 6. Pendiente de decision de Gonzo

1. Publicar los borradores ahora, o primero implementar los arreglos y responder con el diff ya verde.
2. Approach de C4: **variable CSS** (recomendado por el maintainer, sin `getComputedStyle`) vs conservar `anchor-name` por classname.
3. Hallazgo B (scroll): confirmar en browser real antes de responder; decidir si entra en este PR o va como follow-up.
