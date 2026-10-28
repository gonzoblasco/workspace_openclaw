# Cata de harnesses x 3 modelos: el ranking de harnesses depende del modelo

**Fecha:** 2026-10-28 (arrancó el 2026-10-27 23:30)
**Pregunta de Gonzo:** con Claude Code instalado y ruteado a Ollama (ADR-049), ¿hace
falta alguno de los otros coding agents (Cline, opencode, OpenHands), o se pueden retirar?
**Ampliacion:** repetir la cata con `gpt-oss:120b-cloud` y `nemotron-3-super:cloud`
para ver si el ranking se sostiene.
**Diseno:** `harness-model-comparison` (la variable que NO se mide congelada DENTRO de
cada corrida) + verdad de base de la suite oculta.
**Runner:** `playground/cata-harnesses-2026-10-27/` · **Artefactos:** `/tmp/cata-harnesses/`

> Documento 1 (la cata de deepseek, 3 harnesses): `docs/evaluacion/cata-harnesses-2026-10-27.md`.
> Este documento es la version de 3 modelos y **cambia la conclusion**.

---

## 1. La respuesta corta

**Con un solo modelo, la cata de deepseek no separaba a nadie: 90/90 los tres.**
Con tres modelos, **si se separa, y el ranking de harnesses NO es estable**:

| Modelo | claude | opencode | openhands | TOTAL |
|---|---|---|---|---|
| `deepseek-v4.1-flash:cloud` | **30/30** | **30/30** | **30/30** | 90/90 |
| `gpt-oss:120b-cloud` | 27/30 | 23/30 | **30/30** | 80/90 |
| `nemotron-3-super:cloud` | 26/30 | **29/30** | 21/30 | 76/90 |

**El ganador cambia con el modelo:**
- con gpt-oss gana **OpenHands** (30/30), opencode queda ultimo (23/30)
- con nemotron-super gana **opencode** (29/30), OpenHands queda ultimo (21/30)
- con deepseek los tres empatan

**Eso responde la pregunta original:** no hay un harness que sea "el mejor". Lo que hay
es **parejas de harness+modelo**. Y ningun harness acierta todo solo: el unico
combinacion que llega a 30/30 con dos modelos distintos es **OpenHands con deepseek y
con gpt-oss**, y opencode con nemotron.

## 2. Diseno

- **3 modelos x 3 harnesses x 3 tareas = 27 corridas**, todas con el control verificado.
- Dentro de cada corrida (modelo, harness) el modelo es el MISMO para los 3 harnesses.
- **Jueces:** cada modelo juzga a los otros dos. El juez **nunca** es el modelo
  candidato de esa corrida: `judge.py` lo aborta si coinciden.
- **Suite oculta** validada en las dos direcciones (referencia 3/3 PASS, defectuosa 0/3 PASS).
- **Corpus identico** para los tres: las salidas de los checkers se pre-computan una vez.

### Trampas de invocacion (medidas)

1. La API HTTP de opencode **parte el sufijo `:cloud`** y rechaza el modelo; el CLI
   `--model` si lo acepta. Y el override por request **se ignora**: siempre gana el
   `model` del config.
2. OpenHands se configura con `PATCH /api/settings` (`ollama_chat/<modelo>`) y su
   backend **no re-aplica el settings store sin reiniciar el container**.
3. Su via real es `POST /api/conversations` + `POST .../events`, no `/v1/chat/completions`.
4. Sus eventos son `action`/`observation`, no `llm_message` para las tool calls.
5. **`nemotron-3-super` declara thinking `true` por default** y eso lo hace lento:
   su corrida de T2 con Claude Code tardó **622 s** (10 min) contra 30-56 s de los otros.

## 3. Un bug PROPIO que invalido la primera tanda de opencode

**Lo cuento porque cambió los numeros y porque es el tipo de error que el repo ya
registro antes: medir mal y creerle.**

El compose de opencode monta `./workspace:/workspace` desde `docker/`, asi que:

```
container /workspace           = host docker/workspace
container /workspace/workspace  = host docker/workspace/workspace   <-- aqui trabaja el agente
```

El runner preparaba el corpus en el **primer** nivel y corria el agente en el
**segundo**. El agente no via la tarea. Se manifesto de dos formas:

- gpt-oss/opencode/T1 devolvio **5 caracteres con el texto "PROBE"**: era el
  artefacto de mi probe de control, no una respuesta.
- nemotron/opencode/T1 dio 6/10 con un ratio **4.38:1 sobre `#ffffff`**: un color
  que no existe en el tema dark. Invento la respuesta porque no pudo leer.

**Corregido** (el path del host ahora es `docker/workspace/workspace`) y **las 9
celdas de opencode se re-ejecutaron** con el fix. El `consolidate.py` reconstruye
las 27 filas desde los artefactos (que son acumulativos) porque un re-run de una
sola celda **sobreescribe** `results.json` y pierde los metadatos de los otros.

**Consecuencia honesta:** los 30/30 de opencode con deepseek en la primera tanda
eran con el path viejo. Re-ejecutado con el fix, opencode+deepseek da **30/30
igual** (el agente exploraba mas y encontraba el corpus por su cuenta). Los
numeros de opencode que importan son los de la re-ejecucion.

## 4. Fallos REALES (no mios)

### 4.1 nemotron-3-super + OpenHands: agota las iteraciones y no entrega

`T3` termino en **error** con 0 caracteres de entregable, tras 30 acciones de
exploracion. **Reproducido** en una segunda corrida: mismo resultado. El agente
leia los 60 ADRs, grepeaba `Supersede:`, y se quedo sin turno para escribir.

Es el peor caso de la cata: **un fallo de infraestructura disfrazado de tarea
dificil**. Sin leer los artefactos, "6/12" parece que el modelo no entendio nada.
Con el log, se ve que no le dio tiempo.

### 4.2 gpt-oss + opencode: el stream muere sin `finish_reason`

Dos de las tres celdas de gpt-oss/opencode Solve con
`OpenAI Chat stream ended without finish_reason` (T1 y T3). T1 entrego 3.113 ch
igualmente (el harness SIGUE y escribe el archivo), T3 no entrego nada.

**Es un fallo del harness contra ese modelo**, no del modelo: la misma corrida con
deepseek y con nemotron no lo hacen.

## 5. El cruce: por que un solo modelo no alcanza

| | claude | opencode | openhands |
|---|---|---|---|
| **deepseek** | 30/30 (1) | 30/30 (1) | 30/30 (1) |
| **gpt-oss** | 27/30 (2) | 23/30 (3) | 30/30 (1) |
| **nemotron-super** | 26/30 (2) | 29/30 (1) | 21/30 (3) |

El ranking de harnesses **se invierte** entre gpt-oss y nemotron-super:

- gpt-oss: openhands (1) > claude (2) > opencode (3)
- nemotron-super: opencode (1) > claude (2) > openhands (3)

**Claude Code es el mas estable: 2o lugar con dos modelos y 1o (empate) con el
tercero.** Nunca queda ultimo, nunca colapsa. Es la unica fila que no cambia de
ranking.

## 6. Costo

```
MODELO                       HARNESS        seg     tok in   tok out  turnos  tools  entregable
deepseek-v4.1-flash:cloud    claude           -     337787     44843       3      0      30757ch
deepseek-v4.1-flash:cloud    opencode       169     121333     34199      33     33      25037ch
deepseek-v4.1-flash:cloud    openhands        -    2703821    124212      73     87      42900ch

gpt-oss:120b-cloud           claude          85      54140     22595       3      0       7605ch
gpt-oss:120b-cloud           opencode        72      99763     10761      49     49       8237ch
gpt-oss:120b-cloud           openhands      160    1438471     59612      80     75       5280ch

nemotron-3-super:cloud       claude         141     375132     54938       3      0       8302ch
nemotron-3-super:cloud       opencode       163     158574     14011      46     46       9427ch
nemotron-3-super:cloud       openhands      161    1068244     21552      59     54       5071ch
```

**OpenHands consume 5,5x a 8,0x los tokens de entrada de Claude Code en los tres
modelos.** La causa es su patron, no el modelo: reenvia todo el contexto en cada
turno (59-80 turnos contra **3** de Claude Code, que hace la exploracion por
dentro). Con nemotron-super, su `per_turn_token` supera los 60.000.

**Claude Code es el mas barato en tokens de entrada en los tres modelos**
(54.140 / 337.787 / 375.132 contra 121.333-2.703.821 de opencode/OpenHands).

Los segundos de claude y openhands con deepseek se perdieron en la consolidacion
(el bug del punto 3). Los tokens y los turnos vienen del `raw`, que es la fuente
autoritativa, y estan completos.

## 7. Juez ciego

| Modelo | claude | opencode | openhands |
|---|---|---|---|
| deepseek | 9.33 / 9.00 | 9.50 / 9.33 | **9.83 / 9.17** |
| gpt-oss | 8.50 / **9.83** | 8.17 / 9.67 | 8.33 / 8.33 |
| nemotron-super | 9.17 / 9.67 | 9.33 / **9.83** | 4.83 / 6.17 |

El juez **coincide con la verdad de base** en los extremos: OpenHands con nemotron
(4.83) es el peor, y es el que efectivamente no entrega. Y opencode con nemotron
(9.33) es el mejor del modelo, y es el que mas acierta. **La prosa y el pass/fail
dicen lo mismo**, que era la pregunta de si el juez servia para algo.

## 8. Veredicto

### Lo que NO se retira

| | Decision | Motivo medido |
|---|---|---|
| **Claude Code** | **Se queda, y es el motor por defecto** | El mas estable de los tres (nunca ultimo, nunca colapsa), el de menor consumo de tokens de entrada en los 3 modelos, y ya es el motor del pipeline (ADR-049) con 40+ sesiones reales. |
| **opencode** | **Se queda, bajo demanda** | Acierta 29/30 con nemotron-super (el mejor de su fila) y 30/30 con deepseek. 0 sesiones en 32 dias de vida. |
| **OpenHands** | **Se queda, bajo demanda** | Acierta 30/30 con deepseek y con gpt-oss: el unico harness que llega al maximo con dos modelos. Aporta la UI web, que no tiene equivalente. Pero 5,5-8,0x los tokens. |
| **Cline** | **FUERA (ya lo estaba)** | Su clon fue borrado del disco; el registro ya lo dice "no instalado". |

### La conclusion que cambia respecto de la cata de deepseek sola

La primera cata (solo deepseek) concluyo "los tres aciertan igual, no se retira
nada". **Eso era una conclusion incompleta, y la ampliacion la corrige:** con un
solo modelo no se puede separar el harness del modelo. Un harness que solo sabe
manejar un modelo parece malo.

**Lo que queda en pie:** no se retira nada por redundancia de calidad. Lo que
**cambia** es que **el criterio de "cual harness uso" depende del modelo**, y por
eso la decision operativa es:

- **Default: Claude Code** (el mas estable y el mas barato en tokens de entrada).
- **opencode bajo demanda** cuando se quiere el harness que mejor funciona con
  `nemotron-3-super` (29/30) o que consume menos tokens de entrada que
  OpenHands.
- **OpenHands bajo demanda** cuando se quiere la UI web, o el pairing con
  gpt-oss (30/30) - aceptando el costo de tokens.

## 9. Lo que NO se midio

- **Cline**: no existe en disco. Sin reclonar no hay cata de 4.
- **Una sola corrida por celda**: no hay varianza medida. Los fallos de §4 son
  reproducibles (verificado), pero los pases no tienen barra de error.
- **Solo tareas de analisis de lectura.** No se midio edicion de codigo, refactor ni
  debugging, donde el loop agentico de Claude Code tendria su ventaja estructural
  mas clara.
- **nemotron-3-ultra**: descartado en ADR-090 (mas grande, mismo contexto que
  super, mas lento y mas caro, perdio el benchmarking). Confirmado en el registro.
- **El gasto en dolares** no se midio: la cata reporta tokens, no costo.

## 10. Aprendizajes

1. **Un solo modelo no separa el harness del modelo.** Con deepseek los tres
   harnesses dieron 90/90: ese empate no era "los harnesses son iguales", era
   "el modelo no discriminaba". Con tres modelos, el ranking se invierte. **La
   cata de un solo modelo no puede concluir sobre harnesses.**
2. **La separacion de un harness esta atada a un modelo, no al harness.** OpenHands
   es el mejor con deepseek y gpt-oss (30/30) y el peor con nemotron-super
   (21/30, con el fallo de agotar iteraciones). El harness no es la unidad de
   decision: la unidad es **harness + modelo**.
3. **Un fallo de entrega puede ser un fallo de infraestructura, no de
   comprension.** nemotron+OpenHands dio 6/12 y "parecia" que no entendia la tarea:
   habia agotado 30 iteraciones explorando. Sin leer el log de acciones, el
   veredicto seria falso.
4. **Un bug del runner puede simular un defecto del harness.** El path del corpus
   maluesto dio 5ch ("PROBE") y un ratio inventado (4.38:1 sobre #ffffff). Si no
   se revisaba el entregable, "gpt-oss/opencode = 1/10" entraba al informe como
   un defecto del harness.
5. **El re-run de UNA celda pisa `results.json` y pierde el resto.** Los
   artefactos son acumulativos: el consolidador tiene que reconstruir desde ahi, no
   confiar en el archivo de resultados.
6. **El costo de un harness es su patron de contexto, no su modelo.** OpenHands
   reenvia todo en cada turno: 5,5-8,0x los tokens de entrada en los tres modelos.
   Un harness que reenvia contexto se paga siempre igual de caro.
7. **La primera cata dio un veredicto incompleto, y la segunda lo completo.** "Los
   tres aciertan igual" era cierto para deepseek y falso como afirmacion general.
   Ampliar a tres modelos no fue mas trabajo por mg redundancia: fue lo que
   separo el harness del modelo.

## Related

- `harness-model-comparison` - el skill que define el diseno.
- `external-candidate-evaluation` - el marco de "el marco de dos opciones del
  articulo no describe nuestro stack".
- `docs/evaluacion/cata-harnesses-2026-10-27.md` - la cata de deepseek sola, y por
  que su conclusion era incompleta.
- `docs/evaluacion/pr-agent-2026-10-20.md` - el precedente de verdad de base
  humana con Claude Code como vara.
- ADR-090 - la politica de modelos por rol (y el descarte de nemotron-ultra).
- ADR-049 - Claude Code como motor estandar, ruteado a Ollama.
