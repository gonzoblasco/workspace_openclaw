# Ficha de crítica - [Nombre del artefacto]

> **Cómo usar esta plantilla:** completar en 10-15 min. Lo importante NO es el artefacto - es
> el vocabulario que se gana al nombrar lo que funciona y lo que no. Si una sección no
> aplica, escribir "n/a" y por qué. El "por qué no aplica" también es criterio.

---

## 0. Cabecera

| | |
|---|---|
| **Artefacto** | (URL, archivo, o ruta) |
| **Tipo** | pantalla / documento / componente / flujo |
| **Fecha** | YYYY-MM-DD |
| **Dirección juzgada** | herramienta funcional / pieza memorable / mixto |
| **Por qué esa dirección** | (una línea) |

## 1. Gates: ¿cuáles aplican?

| Gate | Aplica | Veredicto | Evidencia (1 línea, con el número medido) |
|---|---|---|---|
| Grayscale | ✅/❌ | ok / falla / n/a | |
| Squint | ✅/❌ | ok / falla / n/a | |
| Alignment count | ✅/❌ | ok (n ejes, cuáles) / falla / n/a | |
| Spacing audit | ✅/❌ | ok / falla / n/a | |
| Contrast | ✅/❌ | ok (ratio y peor píxel) / falla / n/a | |
| Single rank-1 | ✅/❌ | ok / falla / n/a | |

> **Si un gate no aplica, decirlo y explicar por qué.** Correr un gate de pantalla sobre
> prosa da falso veredicto. Adaptar el gate al artefacto ES el primer acto de criterio.

**Síntesis de gates:** [pasa / pasa parcial / falla] - [1 línea]

## 2. Qué funciona (2-3 ítems, máx)

- **[Aspecto]:** [qué hace bien, concreto. No "es lindo".]
- **[Aspecto]:** [...]

## 3. Qué falla (2-4 ítems)

| Falla | Por qué falla | Fix concreto |
|---|---|---|
| | | |
| | | |

> El "por qué falla" nombra el principio. El "fix" es accionable, no "mejorarlo".

## 4. Qué me llevo (1-3 líneas)

- **Principio que confirma o refuta:** [¿qué regla del sistema se cumple o se rompe acá?]
- **Vocabulario nuevo:** [un término que sirvió para nombrar algo]
- **Acción derivada:** [¿hay algo que arreglar? ¿en este artefacto o en el sistema?]

## 5. Cierre

- **Tiempo usado:** [min]
- **¿El ojo cambió?** [sí / un poco / no - y por qué]

## 6. Evidencia visual (verificable)

Renders del caso, generados con el script del frente (no a mano, no en un editor):

| Render | Archivo | Cómo se generó |
|---|---|---|
| Color | `studies/design/casos/<prefijo>_view.png` | descarga directa de la og:image / captura propia |
| Grayscale | `studies/design/casos/<prefijo>_gray.png` | `Image.convert("L")` |
| Squint | `studies/design/casos/<prefijo>_squint.png` | resize a 1/12 y vuelta (bilinear) |

```bash
cd studies/design && python3 scripts/critica-renders.py --out casos --prefix <prefijo> <URL-o-archivo>
```

**Las mediciones se escriben con números, no con adjetivos.** El veredicto de `Contrast` lleva el ratio
promedio **y** el peor píxel bajo el glifo: si el fondo no es uniforme (gradiente, glow, foto), el
promedio miente y el peor píxel decide. El de `Alignment` lleva cuántos ejes hay y cuáles.
