# ADR-116: La voz del audiolibro es Chatterbox clonando una referencia barítona de 100 Hz

**Status:** Accepted (2026-11-18)
**Supersedes:** ADR-115
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-11-18
**Origen:** instrucción directa de Gonzo tras escuchar las muestras ("-4, usemos ese", "quiero la voz profunda")

---

## Contexto

ADR-115 (seis horas antes) fijó Kokoro `em_alex` como voz del audiolibro. La decisión se tomó
midiendo limpieza —Kokoro no puede alucinar cola porque no es autoregresivo— y sobre una muestra de
**una sola frase sin diálogo ni preguntas**. Ese fue el error de método: la muestra no contenía lo
que el libro tiene 1.432 veces.

Al escuchar el libro completo, Gonzo reportó dos cosas: el diálogo suena plano ("viste a vera" en
vez de una pregunta) y "ruidos raros". Medido:

**1. Kokoro no hace preguntas.** Es no autoregresivo: calcula la entonación de la estructura del
texto, no la decide al generar. Contornos medidos, misma voz, mismo texto:

| Frase | Inicio | Fin |
|---|---|---|
| `Viste a Vera.` | 154 Hz | 103 Hz |
| `Viste a Vera?` | 154 Hz | 105 Hz |

Idénticos. Siempre cae. En una novela con 1.432 líneas de diálogo, todas las preguntas suenan a
afirmación. **Un motor que no puede entonar una pregunta no sirve para narrar ficción dialogada**,
por limpio que sea.

**2. El −3 semitonos se llevaba los agudos.** El corte de banda medido: 10.185 Hz crudo, 8.564 Hz
procesado. Bajar el tono del audio final cuesta 1,6 kHz de aire. Eso es lo que sonaba apagado.

**3. El "demonio" de Chatterbox era un bug de corte, no del motor.** El script anterior partía el
texto a 240 caracteres y cortaba a mitad de palabra ("porq"). El modelo recibía texto truncado y
seguía generando: 7,6 s de respiraciones y chasquidos al final del capítulo 1. Con corte por
párrafo, la cola medida es **0,13 s**.

## Decision

**La voz del audiolibro es Chatterbox clonando una referencia barítona, con el corte corregido.**

| Parámetro | Valor |
|---|---|
| Motor | Chatterbox multilingual (autoregresivo, local, MPS) |
| Referencia | `audio/voz/referencia-baritono-4st.wav` — `em_alex` de Kokoro bajado 4 semitonos |
| F0 resultante | 100–104 Hz (barítono) |
| Agudos | ~11.400 Hz (sin pérdida) |
| exaggeration | 0.5 |
| Corte | por párrafo; recorte de cola por energía (350 ms de gracia) |
| Formato | AAC 96k, normalizado −17 LUFS |

### Por qué bajar el tono de la referencia y no del resultado

Bajar el audio final con `asetrate`+`atempo` cuesta 1,6 kHz de banda y suena apagado. Bajar la
**referencia** y dejar que el modelo genere de cero a 24 kHz da un resultado grave **y** con 11,4 kHz
de agudos. La misma voz profunda, 3 kHz más nítida. Es la diferencia entre filtrar una foto y volver
a sacarla con otra lente.

### Por qué −4 semitonos

Probado a −4, −5 y −6 sobre la referencia. A −4: 100 Hz, 11.550 Hz de banda, cola 0,02 s. A −5 el
resultado perdió contenido (11,3 s de audio contra 14,9 s con el mismo texto) y la banda cayó a
9.337 Hz. **−4 es el punto donde la voz es grave sin que el modelo empiece a perder texto.**

### Correcciones al pipeline que son parte de la decisión

1. **Corte por párrafo, nunca por caracteres.** Un tramo termina en punto, no en medio de una
   palabra. Es la causa raíz de la cola alucinada.
2. **Recorte de cola por energía:** se corta en el último punto con energía real + 350 ms.
3. **Las notas de producción no se narran.** `*POV: ...*`, `*Fin del capítulo.*` y `*Escrito con ...*`
   son metadata del autor. Se filtran antes de sacar el markdown, único momento en que se
   distinguen del pensamiento interior. (El primer render las narró en 14 capítulos.)
4. **Las rayas se traducen por función, no se borran.** Llegaban al fonemizador como carácter
   desconocido y metían ~60 ms de sonido fantasma antes de cada vocal ("Ah" sonaba "nahh"). En este
   manuscrito: inicio de línea → se descarta (el párrafo ya separa turnos); antes de punto → cierra
   la cita; antes de minúscula → coma (atribución: "—dijo"); antes de mayúscula → punto.
   El `¿` también se descarta: medido, da la misma curva de entonación con y sin él.

## Consecuencias

- **El render del libro tarda ~10-13 horas** (~1.186 tramos a ~28 s). Corre desatendido con
  `scripts/render-libro-baritono.sh` y deja log con la duración de cada capítulo.
- Los 17 audios de Kokoro (`capitulo-N-kokoro.m4a`) quedan **obsoletos** aunque estén completos:
  tienen el diálogo plano y el −3 semitonos. Se conservan como historia del proceso.
- Los 2 audios de Chatterbox viejo (`capitulo-1-profunda`, `capitulo-14-profunda`) también quedan
  obsoletos: tienen la cola alucinada del corte por caracteres.
- **Kokoro no se tira.** Sigue siendo el motor para pruebas rápidas de texto (57 s por capítulo
  contra 20 min) y para cualquier cosa donde la entonación no importe.
- El pipeline de registros (pensamiento más lento y con silencio alrededor) **no se aplicó** a este
  motor: Chatterbox entona solo, y agregar variación por tramo encima multiplica el riesgo de
  costuras. Queda como deuda si el resultado pide más.
