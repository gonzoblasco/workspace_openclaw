# ADR-080: Modelo visual para Kanam STUDIO

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisores:** Gonzo (planteo el problema), Kanam CORE (cata y recomendacion)
**Origen:** sesion 2026-09-28 - Gonzo: "STUDIO deberia correr con un modelo visual, no se cual es el ideal"
**Relacionado:** ADR-053 (modelos primario/auxiliar/alternativo), ADR-076 (ningun agente hereda modelo local), `skills/model-cata`

---

## Contexto

STUDIO es el agente de estetica, arte y comunicacion. Su trabajo depende de **mirar**: una critica de diseño sin ver la pantalla es adivinanza.

Se creia que la pregunta era "cual modelo ve imagenes". Se midio primero y la premisa cambio.

## Medicion (cata, 2026-09-28)

**Prueba 1 - capacidad de vision.** Imagenes generadas localmente con contenido no adivinable (forma + dos colores por caso, 4 casos). Se pregunta forma y colores, temperature 0, via `api/generate` con `images`.

**Prueba 2 - juicio de diseño.** Misma captura real del juego, mismo prompt verbatim (5 preguntas: que ves, 3 problemas, mejora por problema, un ajuste que no se puede decidir por gusto, que borrarias). Temperature 0.

| Modelo | Ve imagenes | Latencia | Juicio |
|---|---|---|---|
| `gpt-oss:120b-cloud` (config actual de STUDIO) | **NO** | - | error: "this model does not support image input" |
| `deepseek-v4.1-flash:cloud` | Si | **6.5 s** | Aporta **conocimiento de dominio**: "el color de los numeros es convencion de facto del buscaminas, el usuario la tiene memorizada". 4 hallazgos distintos |
| `glm-5.3-flash:cloud` | Si | 19.8 s | La mas minuciosa: leyo el texto de la pista, cazo una contradiccion de estado real, conto labels duplicados |
| `kimi-k2.6:cloud` | Si | **151 s** | Correcta, sin hallazgos extra. 23x mas lenta que deepseek |
| `gemma4:cloud` | Si | 1.9 s | Generica. **Alucino** un defecto: afirmo "falta contraste en textos secundarios"; medido, `--muted` sobre `--bg` da **7.27:1** (piso 4.5) |

### Hallazgo que vale mas que la eleccion

Los 4 modelos con vision **vieron bien** la captura. Ninguno encontro la deuda real de accesibilidad que si aparecio **midiendo** (`--line` usado como borde de 9 controles a **1.24:1**, piso 3:1). Peor: uno **invento** un defecto de contraste que no existia.

**Conclusion: la vision complementa la medicion, no la reemplaza.** Un modelo que ve es necesario para el juicio estetico, pero las afirmaciones de accesibilidad se verifican corriendo un chequeo, nunca aceptando lo que el modelo dice que ve.

## Decision

1. **`ollama/deepseek-v4.1-flash:cloud` es el modelo primario de `kanam-studio`.** Ve imagenes, 6.5 s, y su aporte es de producto (convenciones del dominio) y no solo vocabulario de diseño. La latencia baja permite iterar diseño en el ciclo de la conversacion.
2. **`ollama/glm-5.3-flash:cloud` es el segundo modelo (fallback).** Sirve para una pasada profunda sobre un diseño ya cerrado, donde su minuciosidad paga y los 20 s no molestan.
3. **`gemma4` y `kimi-k2.6` no se asignan a STUDIO.** gemma4 por calidad (alucina defectos); kimi-k2.6 por latencia (151 s).

## Consecuencias

- El cambio de config lo aplica **OPS** (infraestructura y config son su dominio, ADR-074), con backup previo y verificacion posterior.
- **Regla de uso:** el modelo visual sirve para juicio estetico. Toda afirmacion **medible** (contraste, tamaño, alineacion) se comprueba con un script; el modelo no es autoridad en eso.
- Aplica tambien a MIND cuando su tarea incluya mirar material visual (capturas, diagramas): el default del agente no debe ser ciego.
- **Pendiente:** re-cata a 30 dias (2026-10-28) y validacion en una tarea real de diseño.

## Rollback

`kanam-studio.model.primary` vuelve a su valor previo. La config queda respaldada por OPS antes del cambio.
