# Aprendizaje del frente de diseño - Semana 1, sesión 2 (2026-11-06)

> **[obs]** Frente abierto según `studies/design/README.md` §4.1 ("Crítica de repertorio, el más
> valioso"). Casos: `studies/design/criticas/2026-11-06-linear-og.md` y
> `studies/design/criticas/2026-11-06-stripe-og.md`. Gates leídos de
> `agents/kanam-dev/skills/design-direction/SKILL.md` (2026-11-06).

## Qué produjo la sesión

| Artefacto | Ruta | Veredicto del gate |
|---|---|---|
| Ficha de crítica · Linear | `studies/design/criticas/2026-11-06-linear-og.md` | `PASS` (`kb-audit`) |
| Ficha de crítica · Stripe | `studies/design/criticas/2026-11-06-stripe-og.md` | `PASS` (`kb-audit`) |
| Ficha de crítica · Raycast | `studies/design/criticas/2026-11-06-raycast-og.md` | `PASS` (`kb-audit` + `handoff-gate out`) |
| Renders (color/gris/squint) de cada caso | `studies/design/casos/` | — |
| Script de renders + medición | `studies/design/scripts/critica-renders.py` | corre; mide peor píxel |

## Aprendizajes (con su cita)

**[obs] 1. El gris no es un test, es una pregunta de tipo.** En Linear el grayscale pasa gratis
porque la pieza nunca usó color como canal. En Stripe **falla** y eso no es un defecto: la pieza es
una marca cuyo efecto *es* el color. El error que este par de casos previene es declarar "ok" un
grayscale que falla, en vez de declararlo `n/a` con argumento. *(Ficha Stripe §1 y §4; ficha Linear §1.)*

**[obs] 2. El contraste sobre fondo no uniforme se mide con el peor píxel, no con el promedio.**
[obs] Stripe: promedio **2.27:1**, peor píxel **1.07:1** en la banda del wordmark. Linear: **19.69:1** y
**18.9:1**. Con el promedio, Stripe "pasa justo"; con el peor píxel, falla el piso de 3:1 para texto
grande. *(Medición reproducible: `studies/design/scripts/critica-renders.py`.)*

**[inf] 3. Esa regla vale para nuestras UIs.** Un hero con gradiente, una tarjeta glass o un
`background-image` bajo texto son "fondos no uniformes" y hoy se validan con el color de fondo
declarado, no con el píxel real. La acción es de DEV (gate de contraste por muestreo), no mía: yo
entrego la regla y la evidencia.

**[obs] 3b. El gris no depende del tipo de pieza, sino de dónde termina el color.** Raycast y Stripe
son el mismo formato (og con radial) y tienen veredictos opuestos de grayscale. La diferencia medible
es que en Raycast el radial quedó fuera de la zona del texto, y en Stripe atravesó el wordmark.
*(Ficha Raycast §1 y §4.)*

**[obs] 3c. En una composición simétrica, un eje corrido pesa más que cinco en una grilla.** Raycast:
tagline corrida **57 px** del centro del lienzo mientras el logo está a 10 px. Sobre un fondo
simétrico el desvío se lee como error; en una grilla se lee como decisión. *(Ficha Raycast §1 y §3.)*

**[inf] 4. Un `n/a` bien argumentado es criterio, no pereza.** Correr `single rank-1` sobre una
og:image (sin CTA) da un veredicto falso. El acto de criterio es decir por qué no aplica y qué se
miró en su lugar (el lockup como único protagonista).

## Acciones derivadas

| Acción | Dueño | Estado |
|---|---|---|
| Agregar a `PLANTILLA-critica.md` el bloque de "evidencia visual reproducible" (renders + medición) | MIND | **hecho 2026-11-06** (§6 de la plantilla + `alignment` con n de ejes y `contrast` con peor píxel) |
| Registrar el aprendizaje 1-2 en `memory/memory.db` como learning de diseño | MIND | hecho en el cierre de sesión |
| Proponer a DEV el gate de contraste por muestreo (aprendizaje 3) | MIND → DEV vía CORE | **no iniciado**: no contacto a DEV por mi cuenta |
| Procesar 1 caso más (semana 1 pide 3 fichas) | MIND | **hecho**: tercer caso = Raycast |

## Incógnitas

- [unk] No verifiqué el `spacing` contra la base espacial de Stripe (no leí su CSS): la ficha lo
  declara como no verificable en lugar de inventar un múltiplo.
- [unk] El og:image no es la home renderizada: estos casos no dicen nada sobre el layout real de la
  página, solo sobre la superficie de marca. Está declarado en la cabecera de cada ficha.
