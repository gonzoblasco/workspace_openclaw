# Sondas de anchor positioning - PR #10517

Scripts de diagnostico usados para medir el comportamiento de CSS Anchor Positioning
en el input hidden de Checkbox/Radio. Sacados de `/tmp` (no durable) el 2026-09-24.

Son reproducibles: cada uno levanta Chrome o WebKit con Playwright, inyecta HTML con
la estructura real del componente y mide con `getBoundingClientRect()`.

## Como correrlas

```bash
cd <clone del repo react-spectrum>
NODE_PATH=$PWD/node_modules node <sonda>.js chromium   # o webkit / firefox
```

Requieren el clone con `node_modules` y el browser de Playwright instalado.

## Sondas

| Script | Que mide |
|---|---|
| `sizing-matrix.js` | 8 variantes de declaraciones (`inset` vs longhands, `anchor-size`, `box-sizing`) en chromium y webkit. Aisla cual dimensiona. |
| `checkbox-hypothesis.js` | Confirma la causa raiz: `input type=checkbox/radio` (control reemplazado) con `inset` solo queda en 12x12 en WebKit; un `type=text` si estira. Incluye el control con `appearance: none`. |
| `real-geometry.js` | Reproduce la geometria real (label host con tamano natural, no host con tamano fijo) x nombre literal vs `var()` x host static vs relative. |
| `isolate-vars.js` | Separa las dos variables del cambio: nombre literal vs `var()` con fallback, y longhands vs `inset`. |
| `verify-override-paths.js` | Los 4 caminos de override del anchor name: sin override, por classname en el host, en un ancestro, por style inline. |
| `scroll-definitive.js` | Scroll tracking con espera de frames. Cierra la falsa alarma del "no sigue el scroll". |

## Hallazgos (detalle en `docs/PR-10517-REACT-SPECTRUM-PLAN.md`)

- `inset` **posiciona pero no dimensiona**: en WebKit un control reemplazado queda en su caja intrinseca (12x12). Chromium si lo estira. Hacen falta `width`/`height: anchor-size()`.
- `position: absolute` no resuelve el ancla porque el containing block queda dentro de `VisuallyHidden`; `fixed` sale de esa cadena. Es la relacion de ancestro, no `absolute` en si.
- El nombre debe ser por instancia: un `anchor-name` compartido resuelve a UN ancla.
- El scroll tracking **si** funciona: el desvio inicial era medir sincronicamente sin esperar un frame.

## Nota

`probe*.html` (del 23/09) son los experimentos previos de la sesion anterior, corridos
con `chrome-headless-shell --dump-dom` en vez de Playwright.
