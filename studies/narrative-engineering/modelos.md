# Modelos por autor — qué hay y qué falta

> **Para qué existe este archivo:** el estudio tiene ocho casos y un solo `modelo-*.md`. Eso no es
> un olvido: es una consecuencia de la regla de qué es un modelo y de cuánta evidencia hay por
> autor. Acá está el mapa completo, con lo que cada uno tiene y lo que le falta.

---

## La regla

| | |
|---|---|
| **Caso** | una obra diseccionada. Responde *cómo está construida esta historia*. |
| **Modelo** | **dos o más obras del mismo autor** cruzadas. Responde *cómo trabaja esta persona*: qué se repite, qué no hace nunca, cuál es su procedimiento. |

Un solo caso no hace un modelo. Con una obra se puede describir una mecánica; no se puede decir
qué elige *siempre* ni qué evita.

Por eso hay un `modelo-goyer.md`: Goyer tiene dos casos (01 y 02). Y por eso no hay
`modelo-card.md`: Card tiene uno.

---

## El mapa

| Autor | Casos | Ejes documentados | Voz medida | Artefacto ejecutable |
|---|---|---|---|---|
| **David S. Goyer** | 01 Dark City, 02 Batman Begins | 1-4 (estructura) | **no** — guion, no prosa | — |
| **Catherine Johnson** | 03 Mamma Mia! | 1-4 (estructura) | **no** — libreto | — |
| **Orson Scott Card** | 04 Ender's Game | 1-5 | **sí**: mediana 9, 35/47/16/1 | `PLANTILLA-voz-enders-game.md` |
| **J. K. Rowling** | 05 Azkaban | 1-5 | **sí**: mediana 16,5, 14/35/38/12 | `PLANTILLA-voz-rowling.md` |
| **John Katzenbach** | 06 La Sombra | 1-5 + peso | **sí**: mediana 12, 24/41/27/8 | `PLANTILLA-peso-katzenbach.md` |
| **Esteban Echeverría** | 07 El Matadero | 1-5 | **sí**: mediana 20,5, 14/25/30/31 | `PLANTILLA-voz-echeverria.md` |
| **Gabriel García Márquez** | 08 Crónica | 1-5 | **sí**: mediana 21, 8/28/38/26 | `PLANTILLA-voz-garciamarquez.md` |
| **Miguel de Cervantes** | 09 Quijote I-1 | 1-5 | **sí**: mediana 41, 0/3/15/82 | — (no hay plantilla: el español de 1605 no se trasplanta) |
| ***casa*** (el proyecto) | — | — | **sí**: mediana 9, 36/40/19/4 | `PLANTILLA-voz-casa.md` |

`PLANTILLA-*` viven en `docs/stories/las_tres_sabanas/`, porque nacieron para escribir esa novela.
Se citan acá porque **son la versión ejecutable del perfil**: no describen al autor, lo ponen a
trabajar.

---

## La inversión que hay que mirar de frente

El único archivo que se llama `modelo` es el que **no tiene voz medida**.

- `modelo-goyer.md` promete la firma de un autor y entrega cuatro ejes estructurales —que
  cualquier guionista competente produce— más un hallazgo genuino (heredar el mecanismo del
  mundo). Está bien como documento, pero su nombre pesa más que su evidencia.
- Card, Rowling, Katzenbach, Echeverría y García Márquez no tienen `modelo-*`, y sin embargo
  **son los únicos de los que se puede afirmar algo medible**: cómo construyen la frase, cuánto
  hablan sus personajes, qué no usan nunca.

**Consecuencia práctica:** si alguien entra al estudio buscando "el modelo de Card", no lo va a
encontrar y va a concluir que falta. No falta: está en `caso-04-enders-game.md` §5 y en la
plantilla. Lo que falta es este índice.

---

## Qué haría falta para cerrar cada modelo

| Autor | Qué falta | Cuánto cuesta |
|---|---|---|
| Goyer | prosa narrativa suya en edición estable (novelas gráficas, guiones publicados) | depende de que exista |
| Johnson | lo mismo: texto narrativo, no libreto | depende de que exista |
| Card | un segundo caso (por ejemplo *Speaker for the Dead*) para cruzar | un caso completo |
| Rowling | un segundo caso fuera de Harry Potter (*The Casual Vacancy*) para saber qué es Rowling y qué es la serie | un caso completo |
| Katzenbach | ya tiene el eje del peso; falta una segunda obra para confirmar la fórmula | un caso |
| Echeverría | obra narrativa suficiente (es corto: *El Matadero* es casi todo lo que hay) | limitado por el corpus |
| García Márquez | un segundo caso (*Cien años* o *El coronel*) | un caso |

**Prioridad sugerida:** Rowling con *The Casual Vacancy* —**bloqueada**: el único extracto libre
es de 114 palabras y no alcanza para un perfil (ver `caso-05` y el pendiente del README). Es el único de los cinco donde el
segundo caso responde una pregunta que hoy no tiene respuesta —cuánto de su voz es la serie y
cuánto es ella—, y ya hay un perfil medido contra el que comparar.

---

## Reglas

- **No se escribe `modelo-X` con un solo caso.** Si hace falta describir a un autor con una obra,
  se escribe en el caso, en la sección de síntesis, y se dice que es una muestra.
- **Un modelo sin Eje 5 es un modelo de estructura**, no de autor. Se aclara en el archivo.
- **Cada modelo cierra con lo que falta para refutarlo**, igual que cada caso.
