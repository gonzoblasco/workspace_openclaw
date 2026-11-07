# Semana 2 - Hero: decisión entre 3 registros

**Fecha:** 2026-11-07 (serás agregable a APRENDIZAJE cuando añada cita).

## Versiones creadas

- **A** `hero-A-sistema.html` - "durito funcional": 2 escalas, weight 700 + normal, channel único (weight). grayscale pasa sin drama.
- **B** `hero-B-editorial.html` - "editorial serif": serif + rule, 2 canales (italic + weight).
- **C** `hero-C-producto.html` - "producto inertia": dark + gradient text + 2 canales (gradient + motion).

## Razón por ratio del gradient-text (peor-caso estimado)

El gradiente del hero C arranca en `#e6ecf5` (16.37:1) y cae a `#bb9af7` (8.41:1)
contra `#0a0d13`. El peor es el **end-stop**: 8.41:1, así que pasa a normal
(WCAG 4.5:1) pero no a C target (AAA normal 7:1). El texto serrado del display
en B (5.5:1) no cumple. La estimación asume render sólido, no anti-aliased edges.
Para el gate real (foreground gradient bajo quema por alpha) queda sin medida.

## Output Gates aplicados (estimado, sin render real)

| Gate | A | B | C |
|---|---|---|---|
| Grayscale | Pasa (color no es canal) | Pasa (serif sostiene) | Pasa (gradient mantiene como tint, pero C dependerá de mas medida) |
| Squint | 1 rank-1 claro | 2 rank-1 | 2 rank-1, riesgo de gradient-C semilegible |
| Alignment | 1 eje | 1 eje + baseline | 3 ejes (riesgo) |
| Contrast | ≥7:1 promedio | ≥4.5:1 | ≥7:1 pero gradiente text clips peor píxel |
| Rank-1 | "Build. Measure. Ship." | "Weights held to the line." | "Ship without the noise." |

## Decisión

**A es el transferable default** para una interfaz data-driven. Propiedades que la hacen winning para un SaaS neutral:
- Un solo canal (weight) → el gate squint no paraliza a juicio del usuario.
- Las escalas se desprenden de medidas en `rem` y `clamp`, lo que resuelve contraste sin heroics.

**C gana en conversión** a costa del gate de alignment y peor-píxel contraste; requiere verificación real antes de shout loud.

**B gana estética pero ramifica el grid** (el baseline serif es un elemento que se va perdiendo), ruindad editorial.

## Qué es lo aprendido

- "Un canal por paso" ya lo cubría antes (skill design-direction).
- El contraste de peor píxel sigue subreportarse: el gradient text de C pinta visualmente mejor de lo que mide. Sin medir, mentirías.
- Para heros de producto corto: peso y tamaño > gradientes. Un solo cambio de tamaño lleva el gate.

### Acción (pendiente, no código)

- Render/per-contraste real de los 3 heroes con `critica-renders.py` para validar el "gradient text" de C.
- Ingestar en `knowledge.db` cuando se corra script de ingesta week-2.
