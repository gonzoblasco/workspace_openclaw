# Cata de harnesses de codigo: Claude Code vs opencode vs OpenHands

**Fecha:** 2026-10-27
**Pregunta de Gonzo:** con Claude Code instalado y ruteado a Ollama (ADR-049), ¿hace
falta alguno de los otros tres (Cline, opencode, OpenHands), o se pueden retirar?
**Alcance de esta cata:** **3 harnesses** (Cline queda fuera: su clon fue borrado del
disco, ver la seccion "Lo que NO se midio").
**Modelo:** `deepseek-v4.1-flash:cloud` en los tres.
**Diseno:** `harness-model-comparison` (misma variable que NO se mide congelada) +
verdad de base de la suite oculta (no prosa de juez).
**Runner:** `playground/cata-harnesses-2026-10-27/runner.py`
**Artefactos crudos:** `/tmp/cata-harnesses/` (results.json, suite.json, judge.json)

> **AMPLIACION (2026-10-28): este documento esta SUPERADO en su conclusion.**
> La cata de UN solo modelo no puede separar el harness del modelo. Con
> `gpt-oss:120b-cloud` y `nemotron-3-super:cloud` (27 corridas mas), el ranking
> de harnesses **se invierte** y aparecieron dos fallos reales de harness
> (nemotron+OpenHands agota las iteraciones y no entrega; gpt-oss+opencode
> muere sin `finish_reason`). Ademas, un bug PROPIO del runner (el corpus se
> preparaba un nivel mas arriba de donde opencode trabaja) invalido las
> celdas de opencode de este documento: fueron re-ejecutadas.
> **Ver `docs/evaluacion/cata-harnesses-3-modelos-2026-10-28.md`.**

---

## 1. El control se verifico antes de medir

Sin esto, la cata mide el modelo y no el harness. Evidence por harness:

| Harness | Evidencia de que el modelo viajo | Via de invocacion |
|---|---|---|
| Claude Code | `modelUsage` del JSON de salida | `claude -p --model X --output-format json` |
| opencode | `model` de la sesion, leido de la API | `opencode run --model X --format json` (dentro del container) |
| OpenHands | `stats.usage_to_metrics.default.model_name` | `POST /api/conversations` (con `agent_settings.llm`) + `POST .../events` |

**9/9 corridas con `control_ok = True`.**

### Trampas de invocacion (medidas, no supuestas)

1. **La API HTTP de opencode PARTE el sufijo `:cloud` del modelo y lo rechaza**
   (`Model unavailable: ollama/deepseek-v4.1-flash:cloud`). El CLI `--model` si lo
   acepta. La via API tampoco acepta override por request: con `model`,
   `providerID`/`modelID` y objeto anidado, siempre gana el `model` del config.
2. **OpenHands se configura por `PATCH /api/settings`** con `ollama_chat/<modelo>`
   (no por env var), y el settings store **no se re-aplica al backend sin
   reiniciar el container**: `/v1/models` devuelve `[]` aunque el JSON este
   escrito. Se configuro con el script de configuracion del repo de openhands y se
   reinicio el container.
3. **OpenHands no expone `/v1/chat/completions` en la UI**: la via real es
   `POST /api/conversations` (exige `workspace: {working_dir, kind}` y
   `agent_settings.llm`) + `POST /api/conversations/{id}/events`.
4. **Los eventos de OpenHands son `action`/`observation`**, no `llm_message` para
   las tool calls. El texto del assistant vive en `llm_message`.

## 2. Correccion de diseno que la cata hubo que hacer

Los tres harnesses **no ven el repo de la misma forma**:

| | ve el repo | python3 | node | jq | git |
|---|---|---|---|---|---|
| Claude Code | todo el workspace (host) | si | si | si | si |
| opencode | solo su bind mount | **no** | **no** | **no** | **no** |
| OpenHands | su sandbox | si | si | si | si |

opencode corre en **Alpine** (`oven/bun` + `apk add libgcc libstdc++ ripgrep bash`).

Si las tareas exigieran ejecutar un script de Python, la cata habria medido **la
imagen Docker**, no el harness. Por eso:

- La **ejecucion de los checkers se pre-computa una vez** (`prepare-corpus.sh`) y su
  salida va al corpus, que es **identico para los tres**.
- Las tareas son de **lectura y analisis**: el harness interpreta la salida y el
  codigo, no la produce.

## 3. La suite oculta (la verdad de base)

3 tareas de casos REALES del workspace, con la verdad de base verificada antes de
correr (exit code y valores exactos comprobados a mano):

| Tarea | Que hay que resolver | Verdad de base | exit |
|---|---|---|---|
| T1 | Contraste WCAG: por que `muted` falla sobre `panel-2` en dark | `scripts/check-contrast.py` | 1 |
| T2 | Que contribution queda sin post en la cadena de LinkedIn | `scripts/check-linkedin-pipeline.py` | 0 |
| T3 | Integridad del corpus de ADRs, indice contra disco | `docs/adr/` + los 2 validadores | 0 |

**La suite se valido en las DOS direcciones** (`validate_suite.py`):
- referencia correcta escrita a mano: **3/3 tareas PASS**
- version deliberadamente defectuosa: **0/3 tareas PASS**

### Dos defectos PROPIOS que la validacion destapo

1. **Un assert de T3 exigia que existiera un ADR superseded. NO EXISTE NINGUNO**
   (el ADR-067 esta `Aceptado`; los 60 estan en `Aceptado`/`Rechazado`). Ese assert
   habria castigado la respuesta correcta. Corregido.
2. **Un assert de T3 era tan laxo que la version defectuosa pasaba.** Endurecido
   hasta que la discriminacion en las dos direcciones fue 3/3 vs 0/3.

Sin la validacion en dos direcciones, la suite habria reportado un defectuo que
no existia (el caso que el propio skill de cata ya documenta en 2026-09-30).

## 4. Resultado: la verdad de base NO separa a nadie

```
TAREA          HARNESS     PASES    CTRL   s
T1             claude      10/10    True   86.1
T1             opencode    10/10    True   97.1
T1             openhands   10/10    True   224.7
T2             claude       8/8     True   51.9
T2             opencode     8/8     True  106.2
T2             openhands    8/8     True   96.5
T3             claude      12/12    True   97.5
T3             opencode    12/12    True   82.6
T3             openhands   12/12    True  160.6
```

**90/90 asserts. Los tres harnesses pasaron TODO.**

Con el mismo modelo y las mismas tareas, **los tres harnesses aciertan igual**. La
diferencia entre harnesses NO esta en la calidad de la respuesta: esta en el costo.

## 5. Donde SI se separan: el costo

```
TAREA HARNESS      seg        in     out  turnos  accion entregable
T1    claude        86    144850   19885       1       0     10474ch
T1    opencode      97     73503   24372      18      18     11465ch
T1    openhands    225   1124052   63486      29      35     16907ch
T2    claude        52     44218   10525       1       0      9966ch
T2    opencode     106    149655   16838      17      17     11927ch
T2    openhands     96    324899   20268      16      14     11138ch
T3    claude        98    148719   14433       1       0     10317ch
T3    opencode      83     47998   14649      18      18     10118ch
T3    openhands    161   1254870   40458      28      38     14855ch
```

Totales de las 3 corridas:

| Harness | tiempo | tokens in | tokens out | entregable |
|---|---|---|---|---|
| **Claude Code** | **236 s** | 337.787 | 44.843 | 30.757 ch |
| **opencode** | 286 s | 271.156 | 55.859 | 33.510 ch |
| **OpenHands** | **482 s** | **2.703.821** | **124.212** | 42.900 ch |

**OpenHands consumio 8,0x los tokens de entrada y 2,8x los de salida que Claude
Code, y tardo 2,0x.** La causa esta en el patron, no en el modelo: reenvia **todo
el contexto en cada turno** (29, 16 y 28 turnos contra 1 de Claude Code). Sus
`per_turn_token` van de 33.561 a 62.511.

**Claude Code** es el mas barato en tiempo y tokens de entrada, y su entregable es
el mas chico pero **completo**: 1 turno (no reenvia contexto) y 0 tool calls porque
su loop agéntico ya hizo la exploracion por dentro.

## 6. El juez ciego (ordena la prosa, no decide el veredicto)

Dos jueces (`deepseek-v4.1-flash:cloud` y `nemotron-3-ultra:cloud`), candidatos
anonimizados en orden aleatorio, dos ejes separados:

| Harness | CONTENT | CLEANLINESS | desacuerdo entre jueces |
|---|---|---|---|
| Claude Code | **10.0** | **9.8** | 0.3 (solo en clean) |
| opencode | **9.8** | **9.8** | 0.3 (solo en clean) |
| OpenHands | **9.8** | **9.5** | 0.5 |

Empate practico. El unico matiz: **OpenHands tiene el entregable mas largo y por
eso el clean mas bajo** (mas que doblar la prosa para decir lo mismo no es
"limpio"). Los dos jueces coinciden en el orden: no hay inversion de ranking.

## 7. Veredicto

**Los tres harnesses rindieron lo mismo en calidad. La diferencia es de costo y de
encaje, no de capacidad.**

Lo que la cata **no** dice: que Claude Code sea superior en todo. Dice que, para
**este tipo de tarea** (analisis de un repositorio, con veredicto escrito), con
**este modelo**, los tres aciertan.

### Que hacer con cada uno

| | Decision | Motivo medido |
|---|---|---|
| **Claude Code** | **Se queda, y es el motor por defecto** | El mas rapido (236 s) y el de menor consumo de entrada. Ya es el motor estandar del pipeline (ADR-049). 40+ sesiones reales. |
| **opencode** | **Se queda, bajo demanda** | Acierta 27/27 asserts. Es el mas barato en tokens de entrada (271 k, el menor de los tres). Pero 0 sesiones en 32 dias de vida. |
| **OpenHands** | **Se queda, bajo demanda** | Acierta 30/30 asserts y da el entregable mas completo. Pero 8x los tokens y 2x el tiempo. Un agente con UI web propia, que es su valor diferencial. |
| **Cline** | **FUERA (ya lo estaba)** | Su clon fue borrado del disco. El registro de herramientas lo declaraba instalado con un path inexistente: mentira que se corrigio. |

### La conclusion que importa para la pregunta original

**No hace falta retirar nada por redundancia de calidad.** Con Claude Code solo,
se pierde: la **UI web** de OpenHands (lo unico que no tiene equivalente) y el
**segundo cliente** de opencode como red de seguridad.

Lo que si corresponde es **cambiar el estado por defecto** de los tres que no se
usan: opencode (0 sesiones) y OpenHands (544 requests en 7 dias, pero de pruebas)
a **bajo demanda**, con la misma mecanica que ya se implemento para
`browser-use-ui` y `vane` (`on_demand` en el catalogo + `down` real).

## 8. Lo que NO se midio (y por que)

- **Cline**: su clon (`projects/cline`) **no existe en disco**. Reclonarlo requiere
  Bun 1.4.2 (instalado) y el wrapper ya existe. Si se quiere una cata de 4, hay que
  decidir clonarlo primero. **La conclusion "no hace falta retirar nada" aplica a
  los 3 medidos, no a Cline.**
- **Cline fue "descartado" el 2026-08-22** (era VS Code extension) y **re-adoptado
  el 2026-10-20** como CLI + Hub. Su veredicto nunca se midio contra Claude Code.
- **Un solo modelo.** Con un solo modelo no se puede separar el harness del
  modelo: un harness mejor podria perder con un modelo malo. Repetir con
  `gpt-oss:120b-cloud` y `nemotron-3-ultra:cloud` daria un cuadro mas solido.
- **Una sola corrida por celda.** No hay varianza medida ni repeticiones.
- **Solo tareas de analisis de lectura.** No se midio edicion de codigo, refactor ni
  debugging, donde el loop agentico de Claude Code (herramientas nativas) tendria
  su ventaja estructural mas clara.

## 9. Aprendizajes

1. **La verdad de base de una cata de agentes no la da el juez: la da la suite
   oculta.** Y la suite tiene que validarse en las dos direcciones: mis dos
   defects (un assert que exigia un hecho inexistente, y otro tan laxo que la
   version rota pasaba) se cazaron ahi, no leyendo las respuestas.
2. **Los harnesses no ven el repo igual, y eso puede medir la imagen en vez del
   harness.** opencode en Alpine sin python3: si las tareas exigieran ejecutar un
   script, el resultado habria sido "opencode no sabe Python" cuando en realidad
   es "su imagen no tiene Python".
3. **Verificar que el control viaja antes de medir no es opcional.** La API de
   opencode acepta el override y lo IGNORA: sin verificarlo, la cata habria
   comparado tres harnesses con tres modelos distintos.
4. **El costo de un harness esta en el patron de contexto, no en el modelo.**
   OpenHands reenvia todo en cada turno: 8x los tokens. Dos harnesses pueden
   acertar lo mismo y costar 8x.
5. **Cuando el veredicto es "empate", el desempate esta en el costo y en el
   encaje, no en forzar un ganador.** Acertar 90/90 los tres dice algo: la
   calidad de la respuesta no fue el cuello de botella.

## Related

- `harness-model-comparison` - el skill que define este diseno.
- `external-candidate-evaluation` - el marco de "el marco de dos opciones del
  articulo no describe nuestro stack": aqui fueron 3 harnesses, no 2.
- `docs/evaluacion/pr-agent-2026-10-20.md` - el precedente de verdad de base
  humana con Claude Code como vara.
- ADR-049 - Claude Code como motor estandar, ruteado a Ollama.
