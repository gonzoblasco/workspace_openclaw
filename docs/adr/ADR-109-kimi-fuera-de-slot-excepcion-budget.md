# ADR-109: La familia Kimi sale de todo slot; auditoría de camino a Nemotron 3 Super, redacción con voz a Muse Spark Open, Gemma 4 como chat trivial con contexto completo

**Fecha:** 2026-11-05
**Estado:** Aceptado (decisión de Gonzo 2026-11-05; catas corridas el mismo día: auditoría de camino **medida** y chat trivial **medido** con condición)
**Decisores:** Gonzo (*"K3.1 Pro junto a K3 debe ser una excepción muy exclusiva... debo buscar con cual hacer la auditoría de camino que no sea deepseek para no usar el mismo cerebro que la creación, quiza podemos dejar nemotron-3-super... no suelo usar redacción con voz, estaria bueno, y con su poco uso creo que podemos usar muse-spark-open para ello... lo malo de gemma4 es que inventa, pero creo que si podemos pasarle el contexto completo en cada oportunidad se convierte en el mas barato de todos para charla trivial... que te parece medirlo para ello?"*) / Kanam
**Origen:** panel de uso semanal del 2026-11-05 tras un día de uso real de `kimi-k3.1-pro`, contra la medición del 2026-11-04 en `docs/ecosystem/cata-catalogo-ollama-cloud-2026-11-04.md`. Las dos catas que este ADR dejó pendientes se corrieron el mismo día: `docs/ecosystem/cata-2026-11-05-auditoria-camino-y-gemma4.md`
**Relacionado:** ADR-090 (asignación por rol), ADR-107 (deepseek en el CORE y defaults), ADR-077/088/089/105 (pipeline A/B/C), ADR-076 (ningún agente hereda modelo local)
**Supersede:** la asignación de §6 de `cata-catalogo-ollama-cloud-2026-11-04.md` en los slots **auditoría de camino** y **redacción con voz** (de `kimi-k3.1-pro` a Nemotron 3 Super y Muse Spark Open). El resto de la cata sigue vigente como medición.

---

## Contexto

La cata del 2026-11-04 midió **1 request de `kimi-k3.1-pro` = 7 px = 4,7% de la sesión**, con
equivalencia de **14× deepseek (sesión) a 22× (semanal)**. Con esa medición se le asignaron dos
slots: *auditoría de camino* y *redacción con voz*, ambos de uso puntual.

Un día de uso real mostró que la medición de la sesión era **optimista**. El panel semanal del
2026-11-05 tiene la evidencia final y no requiere estimación: la barra a ojo sobreestima los
colores saturados. Se leen los tramos, no la impresión.

### Las cuentas, corregidas el 2026-11-05

Base tomada del panel (barra de 933 px de track):

| Modelo | Requests | Lectura de la barra | Costo unitario |
|---|---|---|---|
| `deepseek-v4.1-flash` | 5.129 | ~529 px (~57% del track) | **~0,103 px/req** (baseline real del uso) |
| `gemma4:31b` + triage | 2.083 | línea casi invisible | **< 0,01 px/req** |
| `family kimi` (k3.1-pro 10 + k3 17 + otros) | 37 | ~72-75 px | **~2,0 px/req** |
| `kimi-k3.1-pro` | **10** | **más que el tramo de k3 con 17** | **> 2,5 px/req** |
| `kimi-k3` | 17 | menos que k3.1 con menos requests | ~2,4 px/req |
| `gpt-oss:120b` | 32 | ~12 px | ~0,4 px/req |
| `minimax-m3.1-flash` | 27 | ~10 px | ~0,4 px/req |

**El número que corrige la cata:**

- **10 requests de `kimi-k3.1-pro` = ~26 px = ~2,8% de la semana**, no 4,7% de una sesión.
- **Equivalencia: 1 req de K3.1 Pro ≈ 24-26× deepseek**, no 14-22×. La cata decía 14× en sesión y
  22× en semana; el uso real da **más de 24×**. La estimación se quedó corta por tercera vez
  sobre el mismo modelo (el owner había estimado ~10%, la cata dijo 4,7% de sesión, el panel dice
  ~2,8% de semana por 10 requests).
- **K3 (sin Pro) no se salva:** mismo rango, 17 requests ≈ 41 px ≈ 4,4%. Lo que se ahorraba K3
  contra K3.1 Pro **no aparece en el panel**; la diferencia entre las dos barras no paga el cambio.
- **La tesis del "solo activa parte de sus parámetros" no se sostiene.** Si el modelo activara
  solo una fracción de su tamaño por request, 10 requests de un MoE grande deberían pesar menos
  que 17 de un modelo chico. La barra dice lo contrario. Es un argumento de marketing del
  proveedor, no una propiedad que se vea en la factura.

## Decisión

### 1. Kimi sale de todo slot

`kimi-k3.1-pro` y `kimi-k3` **no asignan ningún rol**. No son primario ni fallback de ningún
agente, ni motor de ninguna ruta (`model-router.sh`), ni pre-filtro, ni revisor, ni ejecutor del
pipeline A/B/C. La familia Kimi queda como **excepción declarada**:

- **Cuándo:** cierre de proyecto pre-deploy (ya reservado en la cata del 2026-10-05) o una tarea
  donde el fallo cueste más que un porcentaje de cuota del plan.
- **Con qué:** OK explícito de Gonzo, un uso puntual, presupuesto declarado antes de la llamada
  (cuántas requests se van a gastar).
- **Sin:** iteraciones, borradores sucesivos, "que lo refine", ni correr en paralelo para comparar.

**La regla que queda:** un modelo cuyo costo unitario es **> 20× el baseline** no puede ser
slot. Un slot es una asignación recurrente; un slot caro se paga todas las veces.

### 2. Auditoría de camino → `muse-spark-open` (medido, no propuesto)

La auditoría de camino **no puede ser deepseek**: se audita el camino de un agente que ejecuta
en deepseek, y el mismo cerebro que ejecuta no puede además auditar sin sesgo de confianza.

Se midieron tres modelos sobre tres recorridos: uno con un riesgo real (reporte sin verificar el
repo, commit a ciegas, cierre sin daily) y **dos limpios**, donde el segundo es la trampa dura -el
agente declara que no puede ver los checks y pide OK en vez de reportar "todo verde".

| Modelo | A (riesgo real) | B (limpio) | C (limpio) | Veredicto |
|---|---|---|---|---|
| `nemotron-3-super` | 2/2 | falso positivo | **6 inventados** | descartado |
| `gpt-oss:120b` | 3/3 | **4 inventados** | **5+ inventados** | descartado |
| `muse-spark-open` | 3/3 | **0 reales** | **0 reales** | **elegido** |

**El hallazgo que cambia el criterio:** los dos candidatos recomendados por evidencia vieja
(Nemotron por la prueba de auditoría de *código*, gpt-oss por ser el A del pipeline) **fabrican
riesgos en recorridos limpios**. Nemotron llegó a inventar *"posible exposición de credenciales"*
en un recorrido donde el agente **pide** autorización en vez de tocar tokens. Un auditor con falso
positivo crónico es inútil: su reporte limpio se ignora, y el ruidoso entrena a ignorar el reporte.

**Condición operativa del slot:** el `num_predict` va especificado en el rol. En la primera
corrida muse devolvió vacío con `num_predict=1200` y respondió completo con 2.000 (1.539 tokens,
`done_reason: stop`). Un slot sin presupuesto de tokens falla en silencio, no con error.

**Consecuencia cruzada:** muse queda en **dos** slots -auditoría de camino y redacción con voz-.
Es el mismo modelo en dos tareas distintas, lo que rompe la asimetría de "no auditar con el mismo
cerebro que crea" **sólo si comparten rol**: la redacción produce piezas de texto y la auditoría
produce hallazgos sobre el camino de otro agente. Se acepta, y se revisa si alguna vez el propio
muse audita un texto que muse escribió -ese caso necesita un tercero.

### 3. Redacción con voz → `muse-spark-open`

Uso declarado como **raro** (Gonzo: *"no suelo usar redacción con voz, estaria bueno"*). La cata
del 2026-11-04 midió `muse-spark-open` en **2.648 tok, 4/4, 10,3 s**, con la licencia verificada
(Muse Model License: uso interno sin restricción; la obligación de *"Built with Muse Spark Open"*
aplica a producto o documentación **con superficie pública**, no a tooling interno).

Con uso raro, el slot no se elige por la punta de calidad sino por el costo de no tener que
pensarlo cada vez. `kimi-k3.1-pro` era el único que no se rebajó en T3, pero un slot de redacción
que cuesta 24× el baseline para un uso ocasional es exactamente el patrón que este ADR corta.

**Consecuencia:** la redacción con voz pierde el último punto de calidad medido. Se acepta:
es un uso poco frecuente y el delta no está medido en piezas reales (solo en T3).

### 4. Gemma 4 como chat trivial: sí, bajo una condición de contexto (medido)

**Hecho de entrada:** `gemma4:31b` con **2.083 requests es una línea de barra casi invisible** -
el costo unitario más bajo del plan (`< 0,01 px/req`, más de **10× más barato** que deepseek por
request). El problema no es el costo, es que **inventa**.

**Lo medido, siete llamadas por modo, mismas preguntas, temperatura 0:**

| Modo | Input (7) | Output | Total | Verdad |
|---|---|---|---|---|
| Contexto **completo** (580 tok/llamada) | 4.099 | 845 | 4.944 | **5/7 correctas, 0 falsos positivos** |
| Contexto **parcial** (40 tok/llamada) | 319 | 1.293 | 1.612 | **0/7**: el CORE "es GPT-4o", ops es folleto, y **inventa dos veces fecha y hora enteras** de Tokio |

**La hipótesis de Gonzo se confirma en lo factual y falla en lo económico, y aun así gana.**

- **Factual: completo 5/7, parcial 0/7.** Con el dato en el prompt, gemma4 responde bien los ocho
  roles, resiste la trampa de "¿cuál es el modelo de ops?" y no inventa nada.
- **Económico: el contexto completo cuesta 3,1× las mismas llamadas** (4.944 vs 1.612 tokens): en
  charla trivial la salida es corta y el input fijo de 580 tokens pasa a ser el costo dominante.
- **Pero el parcial no es la opción barata: es la inservible.** Gasta 1,6k tokens fabricando
  respuestas falsas que después hay que corregir, y corregir cuesta más que el ahorro.
- **Contra el CORE, sigue ganando:** ~706 tok/llamada en un modelo **> 10× más barato por token**
  que deepseek. El chat trivial de hoy va al CORE con contexto grande: pagar 706 tok baratos en vez
  de ~100 tok caros es una mejora de orden de magnitud.

**La condición, que es la decisión:**

> **"Charla trivial" = toda llamada cuyo dato de respuesta ya está en el contexto entregado.**

Si el dato no está en el prompt (verificar, analizar, auditar), no es chat trivial y gemma4 sigue
sin servir: este probe no probó que dejara de inventar en *análisis*, solo que no inventa cuando el
dato se le entrega. El caso que lo descartó en STUDIO -un defecto de contraste falso que medido
daba 7,27:1- sigue vigente como límite.

**Implementación:** el slot entra como primario de charla trivial cuando exista un borde
verificable en el runtime (una ruta que no pueda recibir pedidos con consecuencia), con
`num_ctx` que quepa el contexto completo y **sin recorte de contexto**. Hasta que ese borde exista
en código, `utilityModel` sigue en `gemma4:cloud` y el CORE en deepseek: la medición autoriza el
modelo, no una filtración de pedidos por palabra clave.

## Justificación

- **Medir, no estimar.** Es la tercera corrección sobre el mismo número y las tres veces fue
  hacia arriba. La lección no es "Kimi es caro" (eso ya se sabía), es que **la unidad de medición
  correcta es la barra del panel sobre uso real, no el px/req de una sesión**. Una sesión corta
  con prompt grande da un px/req que no se repite en la semana.
- **El costo de calidad de Kimi es real y se paga igual.** Que K3.1 Pro diera "resultado
  maravilloso" ayer no lo habilita como slot: el slot lo paga 20 veces al mes, la maravilla
  ocurrió 10 veces.
- **La asimetría del pipeline no se toca.** A (gpt-oss) / B (deepseek) / C (minimax) quedan como
  están, ADR-077/088/089/105 intactos. Este ADR solo saca a Kimi de los dos slots donde nunca
  debió entrar con la medición vieja.
- **No se audita con el mismo cerebro que ejecuta.** Es la razón por la que deepseek no es
  candidato a la auditoría de camino, y por la que la cata tiene que ser propia.
- **La recomendación vieja no sobrevivió a la trampa.** Nemotron venía recomendado por una prueba
  de auditoría de *código* (2/2 bugs en 3,6 s) y gpt-oss por ser el A del pipeline. Ninguna de las
  dos cosas dice nada sobre auditar un *camino*, y el probe lo mostró: los dos fabrican riesgos
  donde no hay. La analogía entre auditorías era el error, no la elección del modelo.

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| `muse-spark-open` sin `num_predict` explícito devuelve vacío | Presupuesto de tokens en el rol; verificado con 2.000 (1.539 tokens, `done_reason: stop`) |
| Muse queda en dos slots (auditoría y redacción) y audita un texto que muse escribió | Si ocurre, ese caso necesita un tercero; el rol de redacción no audita y el de auditoría no redacta |
| `muse-spark-open` baja la calidad de redacción y se nota | Revertir a Kimi como **excepción con OK**, no como slot |
| Gemma 4 con contexto completo sigue inventando en análisis | El borde está escrito: chat trivial = el dato ya está en el contexto. Fuera de eso, no es chat trivial |
| El contexto completo sale más caro que deepseek con contexto real (3-5k) | Medir con el contexto real del workspace; el punto de quiebre está calculado (706 tok en gemma4 vs ~2.000 tok de contexto del CORE) y hay que confirmarlo |
| Volver a "elegir Kimi por olvido" | Este ADR es el criterio de descarte: > 20× baseline = no slot. `check-adr-supersede.py` vigila que la cata no lo contradiga sin supersede |

## Consecuencias

**Lo que se gana:** una familia entera fuera del presupuesto recurrente, con un criterio de
entrada escrito (excepción declarada, no slot). Auditoría de camino con un cerebro distinto al
de ejecución.

**Lo que se acepta:** pérdida del único modelo que no se rebajó en T3 para redacción con voz, y
que `nemotron-3-super` -el mejor auditor de *código* medido- queda descartado para auditar *camino*
por falso positivo crónico. Es una lección que vale más que el slot: **la tarea define el modelo,
no la familia del rol**.

**Lo que no cambia:** CORE (`deepseek-v4.1-flash`), pipeline A/B/C, `utilityModel` (`gemma4:cloud`),
los slots de dev/ops/auditor/critic/planner/mind/studio, ADR-107 y ADR-090.

**Pendiente, y es lo único:** `muse-spark-open` corrido sobre un cierre de sesión **real** del
workspace, comparado contra lo que Kanam encontró a mano. El recorrido sintético prueba que no
fabrica; falta probar que encuentra. Hasta esa prueba el slot de auditoría de camino queda
**elegido, no aplicado**, y el de chat trivial **medido, no habilitado** (le falta el borde
verificable en el runtime).
