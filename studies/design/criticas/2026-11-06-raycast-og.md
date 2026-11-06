# Ficha de crítica - Raycast, og:image (home)

> **[obs]** Fuente de los gates: `agents/kanam-dev/skills/design-direction/SKILL.md` §"Los 6 gates",
> leída el 2026-11-06. El método del frente: `studies/design/README.md` §4.1.

## 0. Cabecera

| | |
|---|---|
| **Artefacto** | `https://www.raycast.com/opengraph-image-pwu6ef.png` (og:image de `raycast.com`, descargada 2026-11-06 18:08 GMT-3) |
| **Tipo** | mezcla: pieza de marca **con** captura de producto (1200×630 renderizado a 2400×1260) |
| **Fecha** | 2026-11-06 |
| **Dirección juzgada** | mixto |
| **Por qué esa dirección** | La mitad es marca (logo + tagline) y la otra mitad es una captura funcional de la búsqueda de archivos. Un veredicto de herramienta ignoraría la tagline; uno de marca ignoraría que la captura tiene jerarquía propia. |

## 1. Gates: ¿cuáles aplican?

| Gate | Aplica | Veredicto | Evidencia (1 línea) |
|---|---|---|---|
| Grayscale | ✅ | **ok y con sorpresa** | En `ray_gray.png` la pieza **no pierde nada**: la captura estaba diseñada en neutros y el rojo del fondo es puro ambiente. Es el contraejemplo exacto de Stripe: mismo tipo de fondo radial, resultado opuesto. |
| Squint | ✅ | **ok, sin ambigüedad** | En `ray_squint.png` el orden aparece en 3 bloques: tagline (masa gris más grande), logo, caja del buscador. No hay dos candidatos a rank-1. |
| Alignment count | ✅ | **falla (medido)** | La tagline está corrida **57 px a la derecha** del centro del lienzo (bbox 741-1773 sobre 2400; centro 1257 vs 1200) mientras el lockup del logo está a **10 px** del centro: dos ejes que deberían ser uno. La caja y el panel derecho son ejes propios legítimos (grid del producto). |
| Spacing audit | ✅ | ok | Márgenes laterales de la caja iguales; aire superior (logo→tagline→caja) en progresión creciente. La base espacial no es verificable sin CSS: se mide la cadencia, no el múltiplo. |
| Contrast | ✅ | **ok medido (16.1:1 el peor)** | Texto del headline: promedio `(246,245,245)` sobre fondo `(11,6,8)`. Peor par texto/fondo en la banda de la tagline: **16.13:1** (píxel de texto `(231,230,230)` a `x=760,y=323`). Piso 4.5:1: sobra margen. |
| Single rank-1 | ✅ | **ok** | El rank-1 es la tagline (único elemento de nivel 1). El buscador es nivel 2: es el sujeto de la demostración, no el foco que se le vende al usuario. |

**Síntesis de gates:** pasa parcial - 5 de 6 pasan con margen; **alignment count falla** en un punto
medible (el centro del logo no coincide con el centro de la tagline).

## 2. Qué funciona (2-3 ítems, máx)

- **La captura es el argumento, no la decoración.** El buscador muestra `.heic` escrito, con una lista
  filtrada y la metadata del archivo: la pieza *demuestra* el atajo en lugar de describirlo.
- **Fondo que se rinde.** El rojo radial de las esquinas no compite: la masa de la tagline y la caja
  de la captura están sobre negro casi puro. En gris sobrevive intacto (a diferencia de Stripe).
- **Un solo canal por paso.** Logo (tamaño chico + peso) → tagline (tamaño grande + gris casi blanco) →
  captura (contenedor con borde y superficie). Tres niveles por tamaño y superficie, sin apilar tweaks.

## 3. Qué falla (2-4 ítems)

| Falla | Por qué falla | Fix concreto |
|---|---|---|
| **Alignment count: la tagline no está centrada** | Bbox 741-1773 (centro 1257) contra lienzo 2400 (centro 1200): **57 px de desvío**, mientras el logo está a 10 px. La pieza se lee simétrica, así que el desvío aparece como error, no como decisión | Centrar la tagline (o alinear todo a un eje izquierdo declarado). Dos centros a 47 px de distancia no son dos ejes: son un error |
| La captura no tiene fondo propio | La caja flota sobre el radial; abajo a la izquierda, el borde compite con la luz roja del fondo | Bajar el radial por debajo de la caja o subir el contraste del borde: hoy el contorno se pierde justo donde el rojo es más intenso |
| Tagline en gris, no en blanco | `(246,245,245)` pasa holgado, pero frente a un logo en blanco puro la tagline parece "apagada" sin razón funcional | Si el gris no cumple un rol (estado, énfasis), subirlo a blanco; si lo cumple, decirlo con peso, no con luminosidad |

> El "por qué falla" nombra el principio. El fix es accionable, no "mejorarlo".

## 4. Qué me llevo

- **Principio que confirma o refuta:** confirma que **el grayscale gate mide una decisión, no un tipo
  de pieza**. Raycast y Stripe son el mismo formato (og con radial) con veredictos opuestos, y la
  diferencia es dónde cayó la luz: Raycast la sacó de la zona del texto, Stripe la dejó detrás.
- **Vocabulario nuevo:** *captura como argumento* - la imagen demuestra el uso en vez de prometerlo; y
  *eje huérfano* - un elemento desalineado sobre una composición simétrica, donde la simetría vuelve
  visible cada desvío.
- **Acción derivada:** agregar a la plantilla un campo "número de ejes y cuáles", porque `alignment
  count` (≤3 líneas) se lee mejor como lista que como número.

## 5. Cierre

- **Tiempo usado:** ~6 min.
- **¿El ojo cambió?** Sí: con tres casos ya puedo decir que el gris no depende del artefacto sino de
  dónde termina el color; y un eje corrido pesa más en una pieza simétrica que cinco en una de grilla.

## 6. Evidencia visual (verificable)

[obs] Los tres renders del caso, generados el 2026-11-06 desde la imagen descargada:

| Render | Archivo | Cómo se generó |
|---|---|---|
| Color | `studies/design/casos/ray_view.png` | descarga directa de la og:image (2400×1260) |
| Grayscale | `studies/design/casos/ray_gray.png` | `Image.convert("L")` |
| Squint | `studies/design/casos/ray_squint.png` | resize a 1/12 y de vuelta a tamaño original (bilinear) |

[inf] Regenerar los tres y re-medir: `cd studies/design && python3 scripts/critica-renders.py --out casos --prefix ray <URL>`.
[obs] La medición de contraste de esta ficha se hizo por fila (texto contra el fondo de su propia fila),
que es el método correcto cuando el fondo es radial y no uniforme.
