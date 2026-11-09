# Semana 2 — Hero: decisión entre 3 registros

**Fecha:** 2026-11-07 · **Medición:** `studies/design/scripts/measure_css.py` (contraste por variables CSS, sin render)
**Estado:** [obs] estimación sobre pares declarados en el CSS; el peor píxel bajo gradiente queda **sin medir**.

## Versiones creadas

| Versión | Archivo | Registro | Canales de jerarquía |
|---|---|---|---|
| A | `hero-A-sistema.html` | funcional / monocanal | peso |
| B | `hero-B-editorial.html` | editorial serif | serif itálica + regla |
| C | `hero-C-producto.html` | producto / inertia | gradiente + movimiento |

## Contraste medido (pares de variables, no render)

[obs] Valores de `measure_css.py` contra `#0a0d13` / `#0b0f14` / `#f7f4ee` según cada archivo:

| Versión | fg sobre bg | muted sobre bg | Veredicto WCAG texto normal |
|---|---|---|---|
| A | 17.72:1 | 7.48:1 | AA y AAA |
| B | 15.83:1 | 7.16:1 | AA y AAA |
| C | 16.37:1 | 6.49:1 | AA sí; muted **no** llega a AAA |

## El gradient text de C

[obs] El título de C es `background-clip:text` con `linear-gradient(90deg, #e6ecf5, #bb9af7)`: el texto **es** el gradiente.
[obs] Sus dos extremos sobre `#0a0d13` miden 16.37:1 (inicio) y 8.41:1 (fin): ambos pasan AAA para texto normal.
[unk] El **peor píxel con anti-aliasing** no está medido. `measure_css.py` no rasteriza, así que no puede decidir ese gate; hace falta un render real (`critica-renders.py` con captura).

## Output Gates (estado real, no estimado)

| Gate | A | B | C |
|---|---|---|---|
| Grayscale | [obs] pasa: el color no es canal | [obs] pasa: el serif sostiene la jerarquía | [inf] debería pasar: el gradiente es tinte, no único canal |
| Squint | [obs] 1 rank-1 | [obs] 2 rank-1 | [unk] sin render no se juzga |
| Alignment | [obs] 1 eje | [obs] 1 eje + baseline | [unk] 3 ejes declarados, sin medir |
| Contrast | [obs] 17.72 / 7.48 | [obs] 15.83 / 7.16 | [obs] 16.37 / 6.49 / 8.41; [unk] peor píxel |
| Rank-1 | [obs] "Build. Measure. Ship." | [obs] "Words held to the line." | [obs] "Ship without the noise." |

## Decisión

[inf] **A es el default transferible** para una interfaz data-driven: un solo canal (peso) mantiene el squint sin juicio subjetivo, y las escalas en `rem`/`clamp` sostienen el contraste por variable.
[inf] **C se elige cuando la pieza es memorable y hay render para verificarla**: gana en impacto, pero su gate de alignment y su peor píxel quedan abiertos hasta medirlos.
[inf] **B sirve para registro editorial**: gana en tono y pierde ritmo de grid cuando el baseline serif no se sostiene en todos los bloques.

## Qué se aprende

- [inf] "Un canal por paso" ya lo cubría `design-direction`; la semana 2 no agregó reglas, agregó medición.
- [obs] El contraste por variable alcanza para descartar pares imposibles, no para aprobar un gradiente: sin rasterizar, el peor píxel sigue siendo una incógnita.
- [inf] Para heros de producto corto, peso y tamaño rinden más que un gradiente, y además son medibles.

## Pendiente

- [ ] Render real de los 3 heroes con `critica-renders.py` (requiere navegador headless) para cerrar el peor píxel de C.
- [ ] Ingestar esta decisión en `knowledge.db` cuando el corpus de estudio lo pida.
