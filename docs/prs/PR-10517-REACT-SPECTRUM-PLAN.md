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

### Hallazgo B - el scroll tracking funciona (falsa alarma, corregida)

En una primera medicion, 6 componentes con nombres unicos dentro de un contenedor con `overflow-y: auto` parecian no seguir el scroll: medidos de forma **sincrona** justo despues de `scrollTop = 40`, los 6 quedaban 40px corridos.

Al re-medir esperando frames, el resultado se invierte:

| Momento | Antes (sync) | Despues (+50ms) |
|---|---|---|
| `scrollTop = 40`, medicion inmediata | 40px corridos | 40px corridos |
| 50ms despues | - | **0px (siguen el componente)** |
| 350ms y 650ms despues | - | 0px |
| tras scroll de ventana (200px) | - | 0px |

Reproducido igual en headless y en Chrome real (con ventana): el offset vuelve a 0 solo. **Es un artefacto de medicion:** la posicion del ancla la recalcula el compositor, y `getBoundingClientRect()` en el mismo tick devuelve el valor viejo. El input **si** sigue el scroll.

**Conclusion: no hay bug de scroll. No hace falta reportarlo ni abrir follow-up.** Leccion aplicable: las mediciones de layout con anchor positioning necesitan esperar al menos un frame antes de leerse.

---

### Hallazgo C - el `inset` solo no dimensiona el input: regresion real, atrapada por CI

Al pasar los offsets al shorthand `inset` saque los `width`/`height: anchor-size()`. Eso **rompio WebKit**, y no se veia en Chromium (el unico browser que tenia instalado).

Un `input` de checkbox o radio es un **control reemplazado con tamano intrinseco**. Medido en WebKit 26:

| Declaracion sobre el input | Resultado (WebKit) |
|---|---|
| `inset` solo (mi version) | input **12x12**, no cubre el componente |
| `inset` + `anchor-size` | input = componente, exacto |
| `top`/`left` + `anchor-size` (version vieja) | input = componente, exacto |
| `input type=text` + `inset` solo (control) | input = componente |
| `radio` + `inset` solo | input **12x12**, no cubre |

Chromium estira el control desde `inset` solo; WebKit no. Por eso los browser tests pasaban en local y fallaron en CI en `test-browser` (7 fallos: 6 webkit + 1 firefox).

**Evidencia A/B que lo cerro:** con el codigo viejo (`1b4a15c`) + test viejo, WebKit pasa 4/4. Con el codigo nuevo, falla. Regresion nuestra, no test fragil.

**Arreglo:** `inset` (offsets, correcto en RTL) **+** `width`/`height: anchor-size()` (dimension). Con ambos la caja coincide exacta (delta 0x0 medido).

#### El otro fallo: assertion fuera del guard (Firefox)

`expect(new Set(names).size).toBe(labels.length)` estaba **fuera** del `if (supportsAnchorPositioning())`. Firefox 144 no soporta anchor positioning, el `anchor-name` inline se descarta y los 3 labels computan al mismo valor vacio -> Set de tamano 1 vs 3 labels. Movido adentro del guard.

**Leccion operativa:** no declarar comportamiento cross-browser medido en un solo motor. `test-browser` del repo corre chromium + firefox + webkit, y los tres hacen falta antes de pushear.

---

## 4. Plan de arreglos (ejecutado)

| # | Cambio | Archivo(s) | Responde | Estado |
|---|---|---|---|---|
| 1 | `Math.random` -> `useId` de `react-aria/useId` + sanitizador | `Checkbox.tsx`, `RadioGroup.tsx` | C2 | Hecho |
| 2 | `inset` para los offsets **+ `anchor-size` para el tamano** | `hiddenInputAnchor.ts` | C6, Hallazgo C | Hecho (`6996f68`) |
| 3 | Nombre del ancla por CSS variable, leida en host **y** input; eliminar el layout effect y el `getComputedStyle` | `hiddenInputAnchor.ts`, `Checkbox.tsx`, `RadioGroup.tsx` | C4, C3 | Hecho |
| 4 | Borrar las 2 stories | `stories/*.stories.tsx` | C1 | Hecho |
| 5 | Tests: test de la custom property + RTL + por-instancia; assertion movida al guard | `test/Checkbox.sr-focus.browser.test.tsx` | C4, C6, Hallazgo C | Hecho (`6996f68`) |
| 6 | Verificar scroll | - | Cerrado: era artefacto de medicion | Hecho |

**Commits pusheados a la rama del fork:**

| sha | Mensaje |
|---|---|
| `0c48f75` | `fix: resolve hidden input anchor via CSS custom property` |
| `6996f68` | `fix: size the hidden input explicitly for WebKit` |

**Verificacion final (head `6996f68`):** CI CircleCI **success** en todos los checks, incluido `test-browser` (chromium + firefox + webkit). Local: jest del paquete RAC 1637 passed (antes del fix de sizing, que no toca unit tests), browser tests 6/6 en chromium y webkit, oxlint 0 errores, oxfmt OK, typecheck 0 errores en RAC.

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
3. ~~Hallazgo B (scroll)~~: cerrado. Verificado que el input si sigue el scroll (el desvio inicial era medicion sincrona sin esperar frame).
