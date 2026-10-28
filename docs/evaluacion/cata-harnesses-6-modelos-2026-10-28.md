# Cata de harnesses x 6 modelos: ningun harness gana siempre, y Claude Code nunca queda ultimo

**Fecha:** 2026-10-28 (la tanda cloud arranco el 2026-10-27 23:30)
**Pregunta de Gonzo:** con Claude Code instalado y ruteado a Ollama (ADR-049), ¿hace
falta alguno de los otros coding agents (Cline, opencode, OpenHands), o se pueden retirar?
**Diseno:** `harness-model-comparison` (la variable que NO se mide, congelada DENTRO
de cada corrida) + verdad de base de la suite oculta.
**Runner:** `playground/cata-harnesses-2026-10-27/` · **Artefactos:** `/tmp/cata-harnesses/`

> Documento 1 (solo deepseek): `docs/evaluacion/cata-harnesses-2026-10-27.md`.
> Documento 2 (3 modelos): `docs/evaluacion/cata-harnesses-3-modelos-2026-10-28.md`.
> **Este documento los reemplaza**: 6 modelos, y ademas corrige cuatro bugs de
> medicion PROPIOS que inflaban los puntajes del documento 2.

---

## 1. La respuesta corta

**No hay un harness que gane siempre. Con 6 modelos, cada uno de los tres gana 2
veces.** Lo que si se separa de forma estable es otra cosa:

| | claude | opencode | openhands |
|---|---|---|---|
| **Veces que gana (de 6 modelos)** | 2 | 2 | 2 |
| **Veces que queda UNICAMENTE ultimo** | **0** | 2 | 2 |
| **Models donde llega a 30/30 (perfecto)** | 1 | 1 | 3 |

**Claude Code nunca queda ultimo y nunca colapsa.** opencode y OpenHands tienen cada uno dos
modelos donde son el peor. Ese es el criterio operativo, y es distinto del de
"quien gana mas": la unidad de decision es **harness + modelo**, no el harness.

**Y hay un dato nuevo y grande:** `glm-5.3-flash:cloud` da **88/90**, el mejor
modelo medido, y lo hace con los TRES harnesses. Los tres harnesses son capaces
de 30/30 con el modelo correcto.

## 2. La matriz completa (verdad de base: asserts de la suite oculta)

Cada modelo: 3 tareas x 3 harnesses. Cada celda: asserts pasados/total.

| Modelo | claude | opencode | openhands | TOTAL |
|---|---|---|---|---|
| `deepseek-v4.1-flash:cloud` | **30/30** | **30/30** | **30/30** | **90/90** |
| `glm-5.3-flash:cloud` | 29/30 | 29/30 | **30/30** | **88/90** |
| `gpt-oss:120b-cloud` | 27/30 | 23/30 | **30/30** | 80/90 |
| `nemotron-3-super:cloud` | 26/30 | **29/30** | 15/30 | 70/90 |
| `gemma4:cloud` | **27/30** | 16/30 | **27/30** | 70/90 |
| `minimax-m3.1-flash:cloud` | 29/30 | **30/30** | 0/30 | 59/90 |

**Ranking de harnesses POR MODELO (el ranking se invierte):**

| Modelo | 1o | 2o | 3o |
|---|---|---|---|
| deepseek-v4.1-flash | claude (30) | opencode (30) | openhands (30) |
| glm-5.3-flash | openhands (30) | claude (29) | opencode (29) |
| gpt-oss:120b | openhands (30) | claude (27) | opencode (23) |
| nemotron-3-super | opencode (29) | claude (26) | openhands (15) |
| gemma4 | claude (27) | openhands (27) | opencode (16) |
| minimax-m3.1-flash | opencode (30) | claude (29) | openhands (0) |

**deepseek empata a 30/30 en los tres.** Por eso el deepseek solo no separaba
nada: con ese modelo los tres harnesses son indistinguibles. Con seis, se ve
que es **casualidad del modelo, no igualdad de los harnesses**.

## 3. Por tarea

```
-- T1 (10 asserts) --
   deepseek-v4.1-flash:cloud    claude=10/10  opencode=10/10  openhands=10/10
   gpt-oss:120b-cloud           claude=10/10  opencode=9/10   openhands=10/10
   nemotron-3-super:cloud       claude=10/10  opencode=10/10  openhands=10/10
   minimax-m3.1-flash:cloud     claude=10/10  opencode=10/10  openhands=0/10
   gemma4:cloud                 claude=10/10  opencode=0/10   openhands=10/10
   glm-5.3-flash:cloud          claude=10/10  opencode=10/10  openhands=10/10

-- T2 (8 asserts) --
   deepseek-v4.1-flash:cloud    claude=8/8    opencode=8/8    openhands=8/8
   gpt-oss:120b-cloud           claude=7/8    opencode=5/8    openhands=8/8
   nemotron-3-super:cloud       claude=7/8    opencode=7/8    openhands=5/8
   minimax-m3.1-flash:cloud     claude=8/8    opencode=8/8    openhands=0/8
   gemma4:cloud                 claude=7/8    opencode=6/8    openhands=7/8
   glm-5.3-flash:cloud          claude=8/8    opencode=8/8    openhands=8/8

-- T3 (12 asserts) --
   deepseek-v4.1-flash:cloud    claude=12/12  opencode=12/12  openhands=12/12
   gpt-oss:120b-cloud           claude=10/12  opencode=9/12   openhands=12/12
   nemotron-3-super:cloud       claude=9/12   opencode=12/12  openhands=0/12
   minimax-m3.1-flash:cloud     claude=11/12  opencode=12/12  openhands=0/12
   gemma4:cloud                 claude=10/12  opencode=10/12  openhands=10/12
   glm-5.3-flash:cloud          claude=11/12  opencode=11/12  openhands=12/12
```

**T3 (gobernanza de ADRs) es la que separa a los harnesses.** Es la tarea con mas
asserts (12) y la que exige explorar 60 documentos: ahi esta el loop agentico, y
ahi OpenHands con minimax se queda sin turno (0/12 tres veces seguidas).

## 4. Costo (los 3 harnesses, las 3 tareas, por modelo)

```
MODELO                       HARNESS        seg     tok in   tok out  turnos  tools  entregable
deepseek-v4.1-flash:cloud    claude           0     337787     44843       3      0      30757ch
deepseek-v4.1-flash:cloud    opencode       169     121333     34199      33     33      25037ch
deepseek-v4.1-flash:cloud    openhands        0    2703821    124212      73     87      42900ch

gpt-oss:120b-cloud           claude          85      54140     22595       3      0       7605ch
gpt-oss:120b-cloud           opencode        72      99763     10761      49     49       8237ch
gpt-oss:120b-cloud           openhands       160    1438471     59612      80     75       5280ch

nemotron-3-super:cloud       claude         141     375132     54938       3      0       8302ch
nemotron-3-super:cloud       opencode       163     158574     14011      46     46       9427ch
nemotron-3-super:cloud       openhands       161    1068244     21552      59     54       5071ch

minimax-m3.1-flash:cloud     claude         752     106698    106795       3      0      48438ch
minimax-m3.1-flash:cloud     opencode       520      93036     67013      66     66      60936ch
minimax-m3.1-flash:cloud     openhands       434     904641     20349      93    116          0ch

gemma4:cloud                 claude          43      94257      3031       3      0       5569ch
gemma4:cloud                 opencode      1877      35730      6636      39     39       3828ch
gemma4:cloud                 openhands       97     533055     15240      37     31       5661ch

glm-5.3-flash:cloud          claude         432     159491     42950       3      0      24180ch
glm-5.3-flash:cloud          opencode       532     110401     81483      22     22      33316ch
glm-5.3-flash:cloud          openhands       588    1289017     57763      52     58      32350ch
```

**Claude Code hace 3 turnos en los 6 modelos.** Explora por dentro (una sola
llamada con el resultado) y no reenvia el contexto. OpenHands reenvia todo en
cada turno (52-93 turnos) y consume **1,3M-2,7M de tokens de entrada**: entre
**5x y 8x** lo de Claude Code. Es su patron, no el modelo.

**El costo NO explica la calidad**: minimax dio 60.936ch de entregable con
opencode (el mejor celda de la cata) y 0ch con OpenHands. El volumen de tokens
tampoco: glm-5.3-flash con opencode consumio 110.401 tokens de entrada y
consiguio 29/30, y openhands consumio 1.289.017 para los mismos 30/30.

## 5. Juez ciego (content / cleanliness, 0-10)

| Modelo | claude | opencode | openhands |
|---|---|---|---|
| deepseek-v4.1-flash | 9.33 / 9.00 | 9.50 / 9.33 | **9.83 / 9.17** |
| glm-5.3-flash | 9.67 / 9.17 | 9.50 / 8.83 | **9.83 / 9.33** |
| gpt-oss:120b | 8.50 / **9.83** | 8.17 / 9.67 | 8.33 / 8.33 |
| nemotron-3-super | 9.17 / 9.67 | **9.33 / 9.83** | 4.83 / 6.17 |
| gemma4 | 8.50 / **9.83** | 6.00 / 6.33 | 9.33 / 9.50 |
| minimax-m3.1-flash | 8.83 / 8.17 | **9.50 / 8.50** | 0.00 / 1.83 |

El juez coincide con la verdad de base en los extremos: OpenHands con minimax
(0.00) y con nemotron (4.83) son los peores, y son los que no entregan.
gemma4+opencode (6.00) es el peor de gemma4, y es el que no entrega.

## 6. Los cuatro bugs PROPIOS que inflaban los puntajes

**Los cuento porque corrigieron los numeros del documento de 3 modelos, y porque
son el tipo de error que el repo ya registro antes: medir mal y creerle.**
Todos cuatro tienen numero, no son suspicions.

### 6.1 El fallback del runner se llevaba el INPUT de la tarea como entregable

Cuando el harness no dejaba ningun informe, el runner hacia un fallback:
buscar "cualquier archivo que parezca un entregable". Aceptaba nombres que
empiezan con `tarea`. **El corpus de la tarea se stagea en el MISMO workspace y
se llama `tarea-N-check-<algo>.txt`.** Con lo cual, el input de la tarea se
leia como si fuera el informe del agente, y la suite oculta lo puntuaba como si
el modelo hubiera acertado.

| Celda | Puntaje que decia | Real |
|---|---|---|
| `minimax-m3.1-flash` / T1 openhands | 8/10 | **0/10** (no entrego nada) |
| `minimax-m3.1-flash` / T2 openhands | 6/8 | **0/8** (no entrego nada) |
| `gemma4:cloud` / T1 opencode | 8/10 | **0/10** (no entrego nada) |

Los tres tenian el **input de la tarea** como unico "entregable". Ninguno de los
tres agentes escribio un informe: el fallback era lo unico que había.

El runner ahora excluye por nombre los archivos del corpus stageado
(`repair-corpus-deliverables.py` deja constancia con `deliverable_fuente`).

### 6.2 Callar no es acertar: los asserts `not_contains` PASAN por omision

No afirmar "hay un ADR roto" es cierto de un informe **vacio**. Una celda que
no entrego nada se llevaba **6/12 en T3 solo por callar**.

| Celda | Puntaje que decia | Real |
|---|---|---|
| `nemotron-3-super` / T3 openhands | 6/12 | **0/12** |
| `minimax-m3.1-flash` / T3 openhands | 6/12 | **0/12** |

Ahora un entregable vacio vale **0**, y se agrego una **tercera direccion** de
validacion de la suite (referencia 3/3 PASS, defectuosa 0/3 PASS, **vacio 0/0**)
para que el cambio no pueda volver a romper la suite en silencio. La **cuarta**
direccion (6.5) valida que el chat no cuente como entregable.

### 6.3 El juez ciego se caia y dejaba la tanda sin juzgar

Tres formas distintas de romperse, las tres con el mismo efecto: la celda vale
0 y nadie se entera.

1. `int()` sobre un valor que no era un numero. Si el juez devuelve
   `"cleanliness": "Cleanliness: el informe esta organizado..."`, revienta el
   juez **entero**: se perdieron las 9 celdas de `gemma4:cloud`.
2. JSON estructuralmente roto (el juez mete la justificacion de un eje dentro
   del valor del otro). Medido: 1 de 18 scores de gemma4.
3. Llaves en mayuscula (`Content`, `Cleanliness`).

Ahora `as_int()` extrae el numero, `parse_judge_json()` acepta JSON envuelto en
prosa y con llaves en mayuscula, y hay un ultimo recurso por regex. La celda
de gemma4/T1/claude paso de **1.5 a 6.5** con el parser arreglado: el juez
original habiaInventado un ratio de 5.2:1 (el correcto es 4.10:1, verificado
contra `scripts/check-contrast.py`).

### 6.4 Y el consolidador vaciaba los entregables de los modelos nuevos

`consolidate.py` asociaba cada directorio con el modelo por el campo `model` de
su `results.json`. Las corridas nuevas (minimax, gemma4, glm-5.3) escriben
solo `model_expected`. Con lo cual esos tres modelos no asociaban ningun
artefacto y sus 9 entregables quedaban en **0ch**. Ahora lee `model` con
fallback a `model_expected`, y cubre los 6 modelos en su mapa canonico.

### 6.5 El chat no era el entregable: la suite caia al texto de la respuesta

El quarto bug, encontrado en la fase local. Cada prompt de la cata termina con
"**el informe es el unico entregable: escribilo en `.context/informe.md`**".
Pero `suite.py` y `judge.py` caian a `output` (el texto del chat) cuando no
habia archivo archivado: `body = r.get("deliverable") or r.get("output")`.

Un modelo que **responde en el chat sin escribir el archivo** se puntuaba como
si hubiera entregado.

| Celda | Puntaje que decia | Real |
|---|---|---|
| `nova-2b:latest` / T1 claude | 8/10 | **0/10** (respondio en el chat, no escribio el archivo) |
| `nova-2b:latest` / T1 opencode | 4/10 | **0/10** (idem) |
| `gpt-oss:120b-cloud` / T3 opencode | 9/12 | **0/12** (idem) |

Los tres tenian el **informe completo en la conversacion** y ningun archivo. Es
la misma trampa que 6.1, por el otro lado: ahi el input de la tarea se leia
como el entregable; aca el chat se leia como el entregable.

**No movio los numeros de los 6 cloud**, y eso es lo que confirma que la regla
era correcta y no un ajuste a conveniencia: sus celdas sin archivo tienen
tambien `output` vacio (ya valian 0). Solo cambio lo que debia cambiar.

La suite ahora se valida en **cuatro direcciones**: referencia 3/3, defectuosa
0/3, vacio 0/0, y **chat sin archivo 0/0**. La cuarta mira la *seleccion* del
cuerpo (el archivo), no el contenido: un archivo con los hechos correctos tiene
que seguir valiendo 10/10. Y el validador **falla si alguien reintroduce el
fallback**, para que no pueda volver en silencio.

## 7. Veredicto

### Lo que NO se retira

| | Decision | Motivo medido |
|---|---|---|
| **Claude Code** | **Se queda. Es el motor por defecto.** | Nunca queda unicamente ultimo (0/6 modelos), gana 2 veces, y hace **3 turnos** en los 6 modelos: el de menor consumo de tokens de entrada por lejos. Ya es el motor del pipeline (ADR-049). |
| **opencode** | **Se queda, bajo demanda.** | Gana 2 de 6 (nemotron 29/30, minimax 30/30). Consume mucho menos que OpenHands. Pero queda ultimo en gpt-oss y gemma4. |
| **OpenHands** | **Se queda, bajo demanda.** | Es el unico que llega a 30/30 con **3** modelos (deepseek, gpt-oss, glm-5.3). Aporta la UI web. A cambio: 5-8x los tokens de entrada, y colapsa con minimax (0/30) y nemotron (15/30). |
| **Cline** | **FUERA (ya lo estaba)** | Su clon fue borrado del disco; el registro ya lo dice "no instalado". |

### El modelo que se confirma

**`glm-5.3-flash:cloud` es el mejor modelo de la cata: 88/90**, y es el que
**funciona con los tres harnesses** (29/29/30). Es el que menos celdas deja sin
entregar. Si hay que elegir un modelo nuevo, es este.

**`minimax-m3.1-flash:cloud` se descarta como default**: 0/30 con OpenHands y
3 celdas sin informe de 9. Su 30/30 con opencode no compensa.

### El criterio operativo (el que cambia)

- **Default: Claude Code.** No porque gane mas (2 de 6, empatado con los otros
  dos), sino porque **nunca es el peor** y porque es el mas barato en tokens de
  entrada. Un default que depende del modelo es un default que se rompe.
- **opencode bajo demanda** con `nemotron-3-super` (29/30) o `minimax-m3.1-flash`
  (30/30), o cuando se quiera menos tokens que OpenHands.
- **OpenHands bajo demanda** cuando se quiera la UI web o el pairing con
  `glm-5.3-flash` (30/30) - aceptando el costo de tokens.

## 8. Lo que NO se midio

- **La fase local (4 modelos GGUF x 3 harnesses x 1 tarea).** Arrancada y en
  curso al cierre de este documento; `nova-2b:latest` quedo sellado **sin
  ningun entregable** (0 celdas de 3 con archivo). Los locales son GGUF en CPU y tardan
  10-20 min por celda. **Este documento no dice nada de ellos**: su ausencia
  es una ausencia, no un 0. La pregunta que responde la fase local es "el
  harness aguanta un modelo lento?", y con un solo modelo por harness y una
  sola tarea no da para mas.
  - Lo que si se midio de `nova-2b:latest` (2b, el mas chico): **0 de 3
    celdas escribio el entregable**, y los tres fallos son del harness contra
    ese modelo, no del modelo:
    - **Claude Code**: `[claude-code:unrecognized_model]` - el nombre
      `hf.co/ModernoTech/nova-2b:latest` no lo reconoce (el probe si
      funciono, la corrida de T1 no). En T1 **respondio en el chat** con un
      informe completo, pero **no escribio** `.context/informe.md`: por eso su
      celda vale **0/10** y no 8/10 (ver 6.5).
    - **opencode**: 12 eventos y 0 entregable (tambien respondio en el chat,
      sin escribir el archivo): **0/10**.
    - **OpenHands**: `execution_status: error` con **0 acciones**.
    - Es decir: **un modelo de 2B no sirve como vara de los tres harnesses**,
      porque los tres fallan antes de poder medir de verdad.
- **Cline**: no existe en disco. Sin reclonar no hay cata de 4.
- **Una sola corrida por celda**: no hay varianza medida. Los fallos de §8 (los
  que no entregan) son reproducibles, pero los pases no tienen barra de error.
- **Solo tareas de analisis de lectura.** No se midio edicion de codigo, refactor
  ni debugging, donde el loop agentico de Claude Code tendria su ventaja
  estructural mas clara.
- **El gasto en dolares** no se midio: la cata reporta tokens, no costo.

## 9. Aprendizajes

1. **Un solo modelo no separa el harness del modelo.** Con deepseek los tres
   harnesses dieron 90/90. Ese empate no era "los harnesses son iguales": era
   "el modelo no discriminaba". Con 6 modelos, cada harness gana 2 veces y el
   ranking se invierte. **La cata de un solo modelo no puede concluir sobre
   harnesses.**
2. **La separacion de un harness esta atada a un modelo, no al harness.** La
   unidad de decision es **harness + modelo**. OpenHands es el mejor con 3
   modelos y el peor con 2.
3. **Un fallo de entrega puede ser un fallo de infraestructura, no de
   comprension.** nemotron+OpenHands dio 0/12: habia agotado 30 iteraciones
   explorando. Sin leer el log de acciones, el veredicto seria falso.
4. **Un bug del runner puede simular un defecto del harness.** El path del
   corpus maluesto dio 5ch ("PROBE") y un ratio inventado. Si no se revisaba el
   entregable, "gpt-oss/opencode = 1/10" entraba al informe como defecto del
   harness.
5. **Un fallback de "buscar el entregable" puede traer el INPUT.** El corpus
   stageado se llama `tarea-N-*.txt` y el fallback aceptaba `tarea*`: 3 celdas
   scored con el input. **Todo fallback de busqueda de archivos tiene que
   excluir por nombre los archivos de entrada.**
6. **Un assert que castiga una afirmacion falsa premia el silencio.** Los
   `not_contains` pasan por omision en un cuerpo vacio. "Sin entregable" tiene
   que valer 0, y la suite tiene que validarse en una **tercera direccion**
   (el vacio) para que la regla no se rompa en silencio.7. **El instrumento tambien se rompe, y hay que mirar sus errores.** Un `int()`
   en el juez dejo 9 celdas sin juzgar sin avisar. Un parser de JSON demasiado
   estricto dejo 1 celda en 0. **Un 0 en una cata tiene que poder ser un bug del
   instrumento, no solo un 0 del modelo.**
8. **La suite oculta tiene que estar en el repo, no en `/tmp`.** Por eso vive
   en `docs/evaluacion/cata-harnesses-fixture/`: sus asserts se corrigieron a
   mano dos veces y con la tercera correccion (el vacio) una tercera. Un assert
   corregido sin poder revalidarlo es volver a medir mal.
9. **El entregable es el archivo, no la respuesta.** Los dos extremos del
   mismo error: el input de la tarea leido como informe (6.1) y el informe del
   chat leido como entregable (6.5). Los dos inflan puntajes y los dos se
   venen cuando el modelo **responde bien y no entrega**: hay que leer el
   archivo, no el tamano ni el texto de la conversacion.
10. **Un driver que corre un harness por invocacion borra celdas.** Cada
    proceso de runner reescribia `results.json` con solo sus filas, asi que la
    ultima invocacion se comia las anteriores: un modelo quedo con 1 de 3
    celdas, y las dos perdidas si se habian ejecutado. Los artefactos y los
    raw eran acumulativos, asi que la perdida solo se veia al comparar el
    numero de filas con el de celdas esperadas. **El estado de una cata se
    cuenta por filas, no por artefactos.**

## Related

- `harness-model-comparison` - el skill que define el diseno.
- `external-candidate-evaluation` - el marco de "el marco de dos opciones del
  articulo no describe nuestro stack".
- `docs/evaluacion/cata-harnesses-fixture/` - la suite oculta y su validacion
  en las CUATRO direcciones (reproducible sin `/tmp`).
- `docs/evaluacion/cata-harnesses-2026-10-27.md` - la cata de deepseek sola, y
  por que su conclusion era incompleta.
- `docs/evaluacion/cata-harnesses-3-modelos-2026-10-28.md` - la version de 3
  modelos, **superada por este documento** (sus numeros tenian los tres bugs
  de medicion de §6).
- `docs/evaluacion/pr-agent-2026-10-20.md` - el precedente de verdad de base
  humana con Claude Code como vara.
- ADR-090 - la politica de modelos por rol (y el descarte de nemotron-ultra).
- ADR-049 - Claude Code como motor estandar, ruteado a Ollama.
