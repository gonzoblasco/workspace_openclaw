# Plantilla de voz - Perfil Card (*Ender's Game*, 1985)

> **Que es esto:** la traduccion del `Eje 5` del caso 04 a reglas de escritura ejecutables.
> No es "escribir como Card" en fan-fiction: es **tomar las decisiones de prosa que sostienen
> ese efecto** y aplicarlas a un material propio.
> **Fuente:** `studies/narrative-engineering/caso-04-enders-game.md` (medido sobre Ch. 1, 2.129
> palabras, texto publicado con permiso del publisher).
> **Estado:** borrador 1 - pendiente de probarlo contra una escena real de Las Tres Sabanas.

---

## 1. Ritmo (lo mas importante)

- **Mediana de frase: 7,5 palabras (9 en la narración sola). 65% de las frases van a 10 palabras o menos.**
- **Distribución por bandas de la NARRACIÓN** (medida 2026-11-17, 155 frases): `<=6: 35% |
  7-15: 47% | 16-30: 16% | 31+: 1%`. Ojo con el 65%: es de ≤10 palabras, **no** de ≤6.
  Si una escena tuya tiene medianas de 20+, no esta en esta voz.
- **Regla de la larga:** una frase larga cada 15-20 cortas, y **solo** cuando hay razonamiento.
  En todo el capitulo 1 hubo **dos** frases de 30+ palabras. No es un estilo de periodo
  subordinado; es un estilo de golpes y de una sola cadena mental.
- **Parrafos: mediana de 13 palabras.** Un parrafo = una idea. Si un parrafo tiene dos ideas,
  son dos parrafos.
- **Frenos de una palabra.** Una linea que sea solo *"THIRD"*, *"Silencio."*, *"Afuera."*
  funciona como cambio de marcha. Card los usa para cortar sin explicar.

## 2. Dialogo

- **Raya de dialogo: SI, aunque Card use comillas.** Las Tres Sabanas tiene convencion propia
  (`STYLE.md`: raya, sin comillas). **Se conserva la convencion del proyecto**, se importa el
  resto: el dialogo es seco y rapido, no se traduce la puntuacion.
- **Atribuciones: "dijo" y "pregunto", casi nada mas.** Nada de "murmuro con desgano". En 15
  atribuciones del capitulo 1, 7 fueron "said".
- **Sin adverbios en la atribucion.** Cero.
- **Sin comentario del narrador sobre lo que se dice.** El narrador no explica la intencion de
  nadie. Si hay que saber que Vera esta mintiendo, se sabe por lo que calla.
- **Respuestas de una palabra.** Permitidas y deseables: bajan el ritmo y dejan el silencio.

## 3. Punto de vista y pensamiento

- **Tercera limitada pegada al POV de la escena** (esto ya esta en `STYLE.md`: POV rotativo, un
  POV por escena). Lo que agrega Card: **el pensamiento interno en primera persona, en presente,
  sin comillas ni cursiva.**
  - Ejemplo de forma: *No contesto. Nada que decir. Si digo algo, empeora.*
  - Frecuencia medida: **1,4 pensamientos por cada 100 palabras.** Ni uno por parrafo (seria
    monologo), ni uno por pagina (seria frialdad).
- **El pensamiento hace trabajo.** Es donde el personaje mide, calcula y decide. Nunca es
  decoracion emocional.
- **El narrador puede saber mas que el personaje** y decirlo en una linea seca, sin
  condescendencia (*"No se le ocurrio que Stilson no se tomaba esa pelea en serio"*).

## 4. Escena

- **Decir el desenlace antes que la pelea.** Card escribe *"Esto no iba a terminar bien"* **antes**
  del combate. La tension no es "que pasara" sino "cuanto va a costar". Ese es el truco mas
  trasplantable al drama sistemico de Las Tres Sabanas: **el lector ya sabe que alguien va a
  perder; el interes esta en el precio**.
- **Violencia y crueldad: rapidas, concretas, sin moralina.** El juicio moral llega despues, en
  el pensamiento del personaje, nunca en el momento.
- **Sensorial reducido:** cuerpo y tacto + objetos. Nada de clima, olores ni paisaje, salvo que
  el objeto este haciendo algo (la sabana doblada, mojada, colgada).

## 5. Lo que Card nunca hace (reglas duras para esta voz)

| Nunca | Por que |
|---|---|
| Parrafo de exposicion del mundo | El mundo se explica cuando estorba |
| Adjetivo emocional sobre el protagonista | La emocion esta en la accion y el pensamiento |
| Adverbio en la atribucion | Cero en 2.129 palabras |
| Explicar lo que el personaje ya entendio | Mata el pensamiento interno |
| Cerrar un capitulo en resolucion | Se cierra agregando el costo |
| Metafora decorativa | Card casi no usa metafora; usa objeto concreto |

## 6. Trasplante a Las Tres Sabanas: que SI y que NO

**SI (compatible con el lore y el STYLE actual):**
- El ritmo corto y el pensamiento interno en primera persona presente. **Encaja perfecto con la
  Regla 1** ("nadie actua por si mismo"): el pensamiento es donde cada primo **calcula como
  reaccionar**. El motor del drama sistemico es exactamente el motor del pensamiento de Ender.
- Decir el costo antes de la escena. La Regla 2 ("toda solucion rompe algo") pide que el lector
  sepa que algo se va a romper.
- Objeto concreto en vez de simbolo: la sabana, ya resuelto en `STYLE.md`.
- Cero adjetivos emocionales: ya es regla del proyecto.

**NO trasplantar:**
- **La asimetria de informacion de Ender no aplica tal cual.** En Ender's Game el sistema le
  oculta todo al protagonista; en Las Tres Sabanas los tres primos **se ocultan entre si y al
  lector**, y el lector tiene que ir un paso adelante. Son asimetrias distintas: la de Card es
  vertical (Estado -> nino), la de Las Tres Sabanas es horizontal (primo -> primo). Copiar la
  vertical convertiria a los primos en victimas de una institucion que el lore no tiene.
- **El tono.** Card es frio y limpio; Las Tres Sabanas es realismo familiar cargado. La
  distancia del narrador se puede tomar; la **frialdad** no.
- **El ritmo de 8 palabras de mediana como regla absoluta.** Es una referencia, no una camisa
  de fuerza: una escena de pelea de Las Tres Sabanas puede necesitar mas respiracion.

## 7. Prueba de validacion (corrida 2026-11-17)

Se escribio `manuscript/capitulo_2.md` (escena E2, POV Adan: Vera viene a buscar la sabana y
Adan se la da) aplicando esta plantilla, y se midio con
`studies/narrative-engineering/scripts/prose-metrics.py`. Tres mediciones: referencia Card,
capitulo 1 previo (baseline de la voz actual del proyecto) y el nuevo capitulo 2.

| Metrica | Card (Ch. 1) | Cap. 1 previo | **Cap. 2 nuevo** |
|---|---|---|---|
| Mediana palabras/frase | 7,5 | 6,5 | **6,0** |
| Frases <=10 palabras | 65% | 67% | **72%** |
| Frases >=30 palabras | 0,9% | **6,8%** | **2,9%** |
| Mediana palabras/parrafo | 13 | 10 | **7** |
| Parrafos de dialogo | 51% | 57%* | **54%** |
| Palabras en dialogo | 25% | 24%* | **25%** |
| Adverbios -ly | 18 (0,8%) | 0 | **0** |

\* El script mide dialogo por comillas (convencion Card) o raya (convencion del proyecto).
Para el capitulo 1 el conteo con raya se hizo aparte y son 32 de 56 parrafos.

**Resultado: la plantilla funciona.** El capitulo 2 queda en el rango de Card en ritmo y en
densidad de dialogo, y **baja a un tercio** la tasa de frases largas del capitulo 1 (6,8% ->
2,9%), que era el unico punto donde el proyecto se alejaba del perfil.

**Donde NO llego: pensamiento interno.** Referencia de Card: 1,4 por 100 palabras. Capitulo 2:
0,7. El capitulo 1: 0,0 (los pensamientos estan escritos en tercera, derivados al narrador:
"y sintio que si decia algo iba a empeorar todo"). El cuello de botella es la convencion, no
la plantilla: el proyecto escribe el pensamiento en tercera persona y, cuando lo pasa a
primera, lo hace en cursiva y como parrafo aparte. Subir la densidad a 1,4 requiere decidir dos
cosas:
1. **Si el pensamiento va en cursiva o crudo** (como Card, que no usa ningun marcador).
2. **Si se permite el pensamiento en medio de un parrafo de accion**, no solo como parrafo propio.

Esa decision es de Gonzo, no de la plantilla: toca `STYLE.md` y el gusto del proyecto.
