# ADR-095: Re-evaluación de las decisiones de diseño - el contraste se verifica, el sistema existe

**Fecha:** 2026-10-06
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** sesión 2026-10-06 - Gonzo: *"lo que ya está hecho de decisiones de diseño deben ser revaluadas"*. Re-evaluación de ADR-047 y de `docs/ecosystem/DECISIONS.md` §2.8.
**Relacionado:** ADR-047 (Kanam Design System), ADR-088 (enforcement). Dos ADRs de Kanam OS (medir accesibilidad y adoptar el design system) se retiraron el 2026-10-18 por ADR-067: su sujeto era un proyecto, no una regla del corpus.

---

## Contexto

Gonzo pidió **re-evaluar lo ya decidido** sobre diseño, no construir más. La re-evaluación se hizo contra fuentes reales (los tokens, el build, el CSS generado, los consumidores), no contra lo que los documentos afirmaban.

### Lo que la re-evaluación encontró

**1. El design system EXISTE y funciona (falso pendiente).** `DECISIONS.md` §2.8 y `docs/NORTH.md` repetían que "el design system propio sigue siendo el paso 0" - como si faltara construirlo. **Es falso.** El Kanam Design System está construido desde el 2026-09-14 (ADR-047): `design/tokens/kanam.tokens.json` (3 capas: primitivas, semántica, componente) + dos temas de producto (Plaza, Terrario) + `build-tokens.py` + `dist/` generado. El build corre limpio: *"5 hojas generadas, todas las referencias resueltas"*. Es el **mismo patrón** que el Tablero de la Etapa 4: algo hecho que los documentos seguían pidiendo.

**2. El principio no-negociable #1 era FALSO.** El `design/README.md` y el ADR-047 declaran: *"Contraste verificado, no sentido"* y *"cada tema documenta su matriz de contraste en el JSON ($contrast)"*. Ambas afirmaciones eran falsas:

- **El sistema base no tenía `$contrast`** - la excepción silenciosa a la regla que el propio README enunciaba.
- **Las matrices de Plaza y Terrario eran prosa escrita a mano, nunca medida.** Decían *"state.danger on cream: 4.9:1"* y el valor real era **4.70**. Decían *"text.primary 15.4:1"* y el real era **15.86**. Números inventados con formato de dato.
- **Nada medía el contraste de los tokens.** `check-contrast.py` cubre el CSS de un proyecto (kanam-os), no el sistema. El build solo verifica que las referencias se resuelvan, no que el color sea legible.

**La medición (verificada, no estimada) encontró 10 pares bajo el piso WCAG** en los tres temas: el teal de marca como texto (3.74:1), el ámbar de warning (3.45-3.64:1), los `muted` de Plaza y Terrario (3.33-3.94:1), y el `info` de Terrario (4.32:1). Un sistema que se declara accesible y falla en su propio principio #1.

**3. La adopción es ~cero.** Solo **kanam-lab** consume el sistema (Terrario, vía adapter Gradio). **kanam-os tiene su propio tema hecho a mano** (`globals.css` con `--bg`, `--text`, `--accent`...) que no deriva del sistema. Los productos no usan la identidad única que el ADR-047 instituyó.

## Decisión

### 1. El contraste se vuelve verificable (el principio deja de ser prosa)

**`scripts/check-design-tokens.py`:** mide el contraste WCAG de los tokens de cada tema y lo compara contra el piso que corresponde por **rol** (no por color):

- texto (4.5:1): `text.*` sobre `surface.*`, `onBrand` sobre `brand.primary`, `link`, y `state.*` (se usan como texto en badges).
- componente (3:1): `brand.primary` como superficie, `border.strong`.
- **`border.subtle`/`border.base` NO se exigen** - son decorativos y WCAG 1.4.11 no los cubre; exigirlos sería un falso positivo (la misma disciplina que ya aplica `check-a11y-trigger.py`).
- **Modo reporte** (default, no bloquea mientras haya deuda) y **`--check`** (bloqueante, exit 1). Cableado al pre-commit (ante cambios en `design/`) y al CI.

**Los 10 pares se corrigieron** preservando la identidad visual (cada fix es un paso más oscuro del mismo tono, usando primitivas que ya existían):

| Par | Antes | Después | Fix |
|---|---|---|---|
| `text.onBrand` sobre `brand.primary` | 3.74 | **5.25** | `brand.primary` teal.600 → teal.700 |
| `text.link` | 3.74 | **5.25** | teal.600 → teal.700 |
| `state.warning` (3 temas) | 3.45-3.64 | **4.96-5.23** | amber.500 → amber.600 |
| Plaza `text.muted` | 3.73 | **5.69** | #8A7F6B → #6B6253 (mismo oliva, más oscuro) |
| Terrario `text.muted` | 3.33 | **5.23** | #7A8B99 → #5A6B78 (mismo gris azulado) |
| Terrario `state.info` | 4.32 | **6.33** | blue.500 → navy.500 |

**Las matrices `$contrast` se reemplazaron por valores medidos** (con la nota de que los anteriores eran a mano, nunca verificados). El sistema base ahora **declara la suya** (antes no existía).

### 2. El build se gatea

El pre-commit (ante cambios en `design/`) regenera el `dist/` y corre el guard. Antes, un token podía romper el contraste o dejar una referencia sin resolver en silencio (el `dist/` está gitignored, así que el drift era invisible). Ahora no entra.

### 3. La re-evaluación corrige los documentos, no solo el código

- `design/README.md`: la afirmación "*cada tema declara su matriz en el JSON*" pasa a ser **verdadera** (el base la tiene) y se anota que se **verifica** con el script.
- `DECISIONS.md` §2.8: el "paso 0" (design system) se marca **HECHO** - el pipeline de diseño arranca desde ahí, no desde cero.
- `docs/NORTH.md`: el design system deja de figurar como pendiente; **lo que queda es aplicarlo** (adopción), que es una tarea de las obras (OnWheels, kanam-os), no del sistema.
- `ADR-047`: se anota que su principio #1 no tenía enforcement hasta esta revisión.

### 4. Lo que NO se decide acá (queda como decisión de Gonzo o de las obras)

- **La adopción.** Migrar kanam-os (y OnWheels) para que consuman `design/tokens/` en vez de temas a mano es una decisión de producto: cada adopción es refactor de la obra. Se recomienda, no se ejecuta desde acá. El CORE no escribe código de proyecto (ADR-083).
- **La adopción de las 3 skills de diseño** (`kj-ui-ux-pro-max` → `anti-slop-design` → `design-audit`, §2.8). Con el design system existente, la precondición del auditor de diseño (`design-audit`, regla "todo valor referencia tokens") **ya se cumple** - la decisión de adoptarlas sigue siendo de Gonzo, ahora sin el bloqueo que se creía.

## Consecuencias

- **Positivas:** el principio #1 del design system pasa de prosa a hecho verificado. La identidad de marca se corrigió hacia accesible **sin abandonar la identidad** (mismos tonos, un paso más oscuros). Dos falsos pendientes (el sistema, la precondición del auditor) se resuelven.
- **Positivas (método):** confirmado dos veces en la misma sesión -lo que un documento declara "pendiente" o "verificado" hay que medirlo antes de creerlo. El Tablero, y ahora el design system y su contraste.
- **Coste:** bajo. Cero dependencias; el guard es Python puro.
- **Deuda declarada:** la **adopción (~0)** es el hueco real que queda. kanam-os usa un tema paralelo.
- **Riesgo de mal uso:** correr el guard solo cuando alguien recuerde. Mitigado con el gate en pre-commit y CI.

## Alternativas consideradas

1. **Creer el README y construir "el design system faltante".** Rechazada: ya existe; reconstruirlo sería duplicar un sistema vivo (el precedente no es motivo, pero **esto sí se verificó**: tokens, build y consumidor reales).
2. **Bajar el par del conjunto (excluir `state.warning` del guard).** Rechazada: el ámbar de warning se usa como texto en badges; 3.45:1 es ilegible. Se corrige el token, no el estándar.
3. **Exigir contraste también a los bordes decorativos.** Rechazada: falso positivo (WCAG no los cubre). El guard exige por rol, no por color.
