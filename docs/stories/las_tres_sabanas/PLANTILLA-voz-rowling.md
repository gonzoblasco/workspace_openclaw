# Plantilla de voz - Perfil Rowling (*Prisoner of Azkaban*, 1999)

> **Que es esto:** la traduccion ejecutable del Eje 5 del caso 05. Escrita **despues** de medir un
> intento propio (`manuscript/capitulo_1-rowling.md`), y corrigiendo los tres errores que ese
> intento cometio. Las reglas de abajo no son lo que creo que hace Rowling: son lo que hacen sus
> numeros.
> **Fuente:** `studies/narrative-engineering/caso-05-harry-potter-azkaban.md`.
> **Estado:** v1. **No validada todavia.** La version de `capitulo_1-rowling.md` no cumple estas
> reglas: ver la seccion 6, que documenta por que.

---

## 1. La trampa principal (leer esto primero)

Cuando alguien intenta imitar a Rowling, hace **exactamente** lo que hice yo y falla del mismo
modo: escribe frases largas, pero **deja las cortas en el medio**. El resultado es un texto
bimodal -mitad Card, mitad Rowling- que no se parece a ninguno.

Medido en mi intento:

| | Rowling real | Mi intento (v0) |
|---|---|---|
| Frases <=6 palabras | **19%** | **46%** |
| Frases de 7 a 15 palabras | **35%** | **16%** |
| Frases 16-30 | **36%** | 11% |
| Frases 31+ | **11%** | **26%** |
| Mediana | **15** | 8 |

(Distribucion real de Rowling medida por bandas sobre las 180 frases del Ch. 1, recontada despues
de la primera version de esta plantilla, que traia 15/45/25/13 de memoria. Los datos corregidos
estan abajo.)

**La firma de Rowling no esta en la frase larga: esta en que casi no hay frases cortas.** El
medio (7 a 15 palabras) esta **lleno**. Si tu texto tiene muchas frases de tres palabras y algunas
de cincuenta, no es Rowling: es Rowling mal imitada.

**Regla dura #1:** el texto que aspire a esta voz tiene que tener **alrededor del 20% de frases de
6 palabras o menos**, **alrededor del 35% entre 7 y 15**, y **alrededor del 35% entre 16 y 30**.
El error tipico no es "escribir corto": es **dejar el tramo 7-15 vacio**. Si las cortas pasan del
30%, o si el tramo 7-15 baja del 25%, se esta escribiendo otra cosa.

---

## 2. Ritmo (medido)

| Metrica | Objetivo | Tolerancia |
|---|---|---|
| Mediana palabras/frase | **15** | 13-18 |
| Media palabras/frase | **16,5** | 14-20 |
| Frases <=6 palabras | **19%** | 12-28% |
| Frases de 7 a 15 | **35%** | 28-42% |
| Frases de 16 a 30 | **36%** | 28-42% |
| Frases de 31+ | **11%** | 6-18% |
| Frase mas larga | **60** | 45-70 |
| Parrafos de dialogo | **13%** | solo en capitulos expositivos |
| Palabras en dialogo | **5%** | idem |

**Como se arma la frase larga de Rowling (y no como la arme yo):**
- **Por subordinacion encadenada**, no por acumulacion de "y". *"Ron was yelling so loudly that
  Uncle Vernon jumped and held the receiver a foot away from his ear, staring at it with an
  expression of mingled fury and alarm."* Tres acciones encadenadas por `that`, participio y
  preposicion.
- **Por inciso con rayas**: *"...in the front garden to admire Uncle Vernon's new company car (in
  very loud voices, so that the rest of the street would notice it too)..."*
- **Nunca por yuxtaposicion con comas.** Si la frase larga se puede cortar en tres por comas y
  sigue funcionando, no es Rowling: es una lista.

## 3. Dialogo

- **Comillas tipograficas (curvas) o raya segun el proyecto.** Rowling usa comillas; en Las Tres
  Sabanas manda `STYLE.md` (raya). **No se traduce la puntuacion**: se importa lo otro.
- **Verbos de atribucion variados y con carga**: *bellowed, roared, whispered, muttered, said*. El
  opuesto de la regla de Card. **Aca si se puede.**
- **Adverbios en la atribucion: permitidos.** Rowling no tiene pudor.
- **Dialogo escaso en capitulos expositivos.** Ojo: 13% de parrafos en el Ch. 1 de Azkaban **no
  significa que Rowling escriba poco dialogo**; significa que ese capitulo expone. En escenas de
  accion el dialogo sube. **No usar el 13% como regla general.**

## 4. Narrador y pensamiento

- **El narrador existe, tiene voz y opina.** *"prolijo de un modo casi ofensivo, penso Nestor"* -
  este es el gesto central. El narrador **puede juzgar** lo que describe.
- **Pensamiento en estilo indirecto libre**: la voz del personaje en tercera, **sin marca**.
  *"Perhaps he'd finish this essay tomorrow night..."*
- **Tasa baja de pensamiento: ~0,2 por 100 palabras.** No es un monologo interno.
- **Contraste obligatorio con el caso 04:** Card entra en la cabeza en primera persona; Rowling
  **se queda afuera y comenta**. Si escribis primera persona cruda, no es esta voz.

## 5. Lo que Rowling hace y otras voces no

1. **Frase tesis al abrir**: *"Harry Potter was a highly unusual boy in many ways."* Define por lo
   que el personaje **no** es, y despues lo prueba.
2. **La enumeracion ternaria**: *"For one thing... For another... And he also happened to be..."*
   Patron ritmico que se repite todo el libro.
3. **El detalle absurdo como textura**: Wendelin la Rara se dejo quemar **47 veces**. No sirve a
   la trama. Hace que el mundo exista.
4. **El humor dentro del horror**: los Dursley, la lechuza que se desmaya, el libro que muerde. El
   humor **no alivia** la tension: la hace tolerable.
5. **Adverbios e intensificadores sin culpa**: *really, particularly, extremely, very*. **17,8 por
   1000 palabras**, el doble que Card.
6. **Exposicion disfrazada de accion**: la historia del telefono se cuenta **como pelea en
   presente**, no como resumen.

## 6. Lo que mi intento fallo (evidencia propia)

`manuscript/capitulo_1-rowling.md` fue escrito **sin esta plantilla**, aplicando impresiones. Lo
que salio mal, medido:

| Error | Sintoma | Causa |
|---|---|---|
| **Frase corta de mas** | 46% de frases <=6 contra 15% real | Mantengo el ritmo de Card y le cuelgo frases largas **encima**, en vez de reemplazarlo |
| **Medio vacio** | 16% entre 7-15 contra ~45% real | Las frases intermedias desaparecen: o cuatro palabras o cincuenta |
| **Frase mas larga de 80** | Rowling tope 60 | Escribi por acumulacion de "y", no por subordinacion |
| **Mediana 8 vs 17** | El texto se lee corto | Consecuencia de los dos primeros |

**Lo que si funciono** (y por eso la version se puede rescatar): el narrador con voz propia, la
textura del hilo verde de la merceria, el humor del auto mal estacionado, y el cierre con juicio.
La **voz** estaba; la **distribucion** no.

**Regla de uso:** esta plantilla se aplica **antes** de escribir, no despues. Escribir primero y
medir despues da exactamente el resultado de arriba.

## 7. Trasplante a Las Tres Sabanas: que SI y que NO

**SI:**
- **El narrador que comenta.** *"prolijo de un modo casi ofensivo"* - ese juicio del narrador sobre
  un gesto de Adan es lo que la novela no tiene y le vendria bien.
- **El detalle de textura sin funcion.** El hilo de una merceria de la calle Rivadavia. No explica
  nada; hace que Elvira haya existido.
- **El humor dentro de lo triste.** Vera estacionando sobre la vereda. Adan contestando con una
  frase seca en el peor momento. Sin humor, el drama sistemico es asfixiante.
- **El estilo indirecto libre** como alternativa al pensamiento en primera persona: *"Si decia
  algo, empeoraba"* ya es medio camino; la version Rowling lo hace *"y los dos lo sabian"*.

**NO:**
- **La mediana de 15 palabras.** Las Tres Sabanas esta medida en 7 y ese ritmo es su firma. Subir a
  17 no es "usar Rowling": es reescribir el proyecto.
- **El dialogo al 5-13%.** En tres primos encerrados en una pieza, el silencio y el habla son el
  material. Bajarlo a 5% vacia la escena.
- **La enumeracion ternaria** ("por un lado, por el otro, y ademas"). Es un recurso de narrador
  omnipotente para lectores de 10 anos; en un drama adulto suena a guia.
- **La exposicion disfrazada de accion.** Las Tres Sabanas **no** necesita explicar el mundo: el
  mundo ya es una casa y una herencia.

## 8. Prueba de validacion (pendiente)

Para cerrar esta plantilla hace falta **una** cosa: reescribir una escena corta con las tres
reglas duras puestas desde el principio, y medir.

Criterio de aprobacion:
- frases <=6 palabras: **entre 12% y 28%**
- frases de 7 a 15: **entre 28% y 42%**
- frases de 16 a 30: **entre 28% y 42%**
- mediana de frase: **13 a 18**
- frase mas larga: **menos de 70**

Si el texto pasa esos cuatro y suena bien, la plantilla sirve. Si cumple los cuatro y suena mal, el
problema no es la plantilla: es que la voz de Rowling no le sirve a este material, y eso tambien es
un resultado.
