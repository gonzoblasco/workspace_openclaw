# Las Tres Sabanas - Convenciones de escritura

## Diálogos
- **Raya (—) para los diálogos.** Misma decisión que en `quienes_quedan` (2026-09-24): en los proyectos narrativos de `docs/stories/` se usa el guion largo como raya de diálogo. Es una excepción explícita a la regla global de guion comun; no "corregir".
- Sin comillas en los diálogos. Atribución por acción, no por verbo declarativo cuando se pueda.
- Cada personaje miente por omisión: nunca dice lo que la ficha marca como "lo que nunca dice".

## Voz narrativa
- Tercera persona, **POV rotando entre Néstor, Adán y Vera**. Un POV por escena, sin mezclar cabezas dentro del mismo bloque.
- El POV de una escena es quien *reacciona* en ella (Regla 1: nadie actúa por sí mismo).

### Pensamiento del POV (decidido 2026-11-17)

- **Primera persona, presente, sin cursiva y sin comillas.** El pensamiento va suelto en el
  texto, igual que la narración: *Si digo algo, empeora.*
- **Puede ir al final de un párrafo de acción**, pegado a lo que el personaje acaba de ver o
  hacer. No hace falta abrirle un párrafo propio: separarlo lo convierte en monólogo.
- **Si el pensamiento necesita aire, va en su propio párrafo, sin marcas.** Ninguna marca
  tipográfica: el lector distingue voz narrada de voz pensada por el salto de persona, no por
  el formato.
- **Frecuencia de referencia:** 1 a 1,4 pensamientos por cada 100 palabras (perfil Card,
  medido en `studies/narrative-engineering/caso-04-enders-game.md`). Menos, el personaje se
  vuelve opaco; más, se vuelve monólogo.
- **El pensamiento hace trabajo:** mide, calcula, decide. Nunca decora la emoción.

## Estándar de prosa (regla dura)
- **Show, don't tell.** Prohibido el análisis psicológico y los adjetivos emocionales ("tensa", "resignado", "culpable"). Si hay tensión, se muestra en el ruido de la silla contra el piso.
- **Acciones, objetos y sensaciones.** Solo eso.
- **No adelantar el sistema.** El lector tiene que sentir la trampa antes de que alguien la nombre. Nada de explicar lo que un personaje deduce.
- **La sábana es el objeto, no el símbolo.** Aparece concreta: doblada, remendada, colgada, mojada. Su estado cuenta el paso del tiempo.

## Ficha de proyecto
- **Título:** Las Tres Sábanas
- **Género:** Drama sistémico / realismo con carga familiar.
- **Estructura:** 3 actos, 17 escenas, escaleta en `outline_las_tres_sabanas.md`. Elenco: Néstor, Adán, Vera (primos segundos).

## Ritmo de analisis (decidido 2026-11-17)

**El analisis de voz corre cada DOS capitulos, no cada uno.**

- **Se escribe hacia adelante.** Dos capitulos seguidos sin medir y sin editar. La secuela entre
  uno y el siguiente se protege no interrumpiendola: un capitulo editado contra un vecino que
  todavia no existe se corrige dos veces, y la segunda correccion siempre le gana a la primera.
- **Al cerrar el par, se mide el par.** `studies/narrative-engineering/scripts/prose-metrics.py`
  sobre los dos textos juntos, contra el perfil Card (`PLANTILLA-voz-enders-game.md`).
- **Lo que se compara es el par, no cada capitulo suelto.** Un capitulo puede apartarse del
  perfil y estar bien -la escena de pelea respira distinto, el dialogo de Vera corre mas largo-
  siempre que el par, en promedio, se mantenga cerca de la referencia.
- **La decision de editar se toma sobre el par.** Si los dos se van del rango en la misma
  direccion, es un problema de voz y se corrige. Si se van en direcciones opuestas, es una
  escena haciendo su trabajo y se deja.

**Rangos de referencia del par** (mediana de frase 6-8; frases <=10 palabras 60-75%; frases
>=30 palabras <2%; pensamiento 1 a 1,4 por 100 palabras).

**Estado hoy:** capitulos 1 y 2 cerrados como **primer par**, ya medidos y editados
(`EVALUACION-cap1-cap2.md`). El siguiente analisis cae **al cerrar el capitulo 4**, con los
capitulos 3 y 4 escritos de corrido.

## Plantillas disponibles (2026-11-17)

Cada autor analizado deja una plantilla ejecutable. **Ninguna se aplica de memoria: se leen antes
de escribir.**

| Plantilla | Que aporta | Estado |
|---|---|---|
| `PLANTILLA-voz-enders-game.md` | Ritmo corto, pensamiento en primera persona crudo, dialogo seco | **validada** (cap. 1 y 4 medidos) |
| `PLANTILLA-voz-rowling.md` | Narrador con voz propia, textura sin funcion, humor dentro de lo triste | **sin validar** (el intento v0 no cumplio sus propias reglas) |
| `PLANTILLA-peso-katzenbach.md` | Las cinco condiciones para que un objeto cargue | **aplicada** en `capitulo_1-peso.md`, falta validacion de lectura |

**Regla de proceso:** una plantilla se escribe **antes** de escribir la escena, no despues de
medirla. El caso Rowling es la prueba: se escribio la escena sin plantilla, salio bimodal, y hubo
que reconstruir las reglas desde el error.

## Perfil medido de la novela (narracion)

Medido con `studies/narrative-engineering/scripts/prose-metrics.py` sobre los cuatro capitulos escritos. **Estos son los numeros
reales del proyecto**, y son mas largos que la referencia Card historicamente usada:

| Capitulo | Mediana narracion | <=6 | 7-15 | 16-30 | 31+ |
|---|---|---|---|---|---|
| 1 (Card) | 10 | 33% | 37% | 28% | 2% |
| 1 (peso) | **11** | 34% | 34% | 31% | 1% |
| 2 (puente) | 9 | 40% | 34% | 20% | 6% |
| 3 (E2) | 10 | 31% | 47% | 21% | 2% |
| 4 (E3) | 7 | 45% | 35% | 19% | 1% |

**Promedio del proyecto: mediana ~9-10, bandas ~35/37/24/2.** Es un punto propio, entre Card
(mediana 9) y Katzenbach (12), y **no es un defecto**: el proyecto no esta en ninguno de los tres
autores, esta en su casa.

**Lo que esto cambia:** dejar de tratar a Card como el objetivo a alcanzar. Card fue el primer
perfil medido y por eso se tomo como vara; con tres perfiles en la mano, la vara es **la
consistencia interna del proyecto**, no el numero de un autor.

**Observacion util:** el capitulo con peso (mediana 11) es el mas cercano a Katzenbach (12), y no
por imitacion deliberada: agregar procedencia y costo alarga las frases. **El peso trae su propio
ritmo.**
