# ADR-109: La familia Kimi sale de todo slot; auditoría de camino a Nemotron 3 Super, redacción con voz a Muse Spark Open, Gemma 4 como chat trivial con contexto completo

**Fecha:** 2026-11-05
**Estado:** Aceptado (decisión de Gonzo 2026-11-05; pendiente la cata de la auditoría de camino antes de fijar el slot)
**Decisores:** Gonzo (*"K3.1 Pro junto a K3 debe ser una excepción muy exclusiva... debo buscar con cual hacer la auditoría de camino que no sea deepseek para no usar el mismo cerebro que la creación, quiza podemos dejar nemotron-3-super... no suelo usar redacción con voz, estaria bueno, y con su poco uso creo que podemos usar muse-spark-open para ello... lo malo de gemma4 es que inventa, pero creo que si podemos pasarle el contexto completo en cada oportunidad se convierte en el mas barato de todos para charla trivial... que te parece medirlo para ello?"*) / Kanam
**Origen:** panel de uso semanal del 2026-11-05 tras un día de uso real de `kimi-k3.1-pro`, contra la medición del 2026-11-04 en `docs/ecosystem/cata-catalogo-ollama-cloud-2026-11-04.md`
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

### 2. Auditoría de camino → `nemotron-3-super` (cata pendiente)

La auditoría de camino **no puede ser deepseek**: se audita el camino de un agente que ejecuta
en deepseek, y el mismo cerebro que ejecuta no puede además auditar sin sesgo de confianza.

Candidatos: `nemotron-3-super` (medido en la cata de roles del 2026-10-05: **2/2 bugs reales en
3,6 s, 440 tokens**, sin caer en la trampa; `ultra` descartado), `gpt-oss:120b` (el A del pipeline,
ya en el rol `dev`) y `muse-spark-open` (2.648 tok, 4/4, 10,3 s).

**Ninguno de los tres fue medido en la tarea de auditoría de camino.** Antes de fijar el slot se
corre un probe propio con tres recorridos reales -uno con un riesgo real conocido, uno con un
riesgo falso (trampa) y uno limpio- y se mide lo que la auditoría de camino necesita:
**(a)** si encuentra el riesgo real, **(b)** si se inventa el falso, **(c)** cuántas requests
consume para hacerlo.

La propuesta es **`nemotron-3-super`** por costo y por su evidencia de auditoría de código, pero
se ratifica con el probe, no por la analogía con el rol `auditor`.

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

### 4. Gemma 4 como chat trivial con contexto completo (a medir)

**Hecho de entrada:** `gemma4:31b` con **2.083 requests es una línea de barra casi invisible** -
el costo unitario más bajo del plan (`< 0,01 px/req`, más de **10× más barato** que deepseek por
request). El problema no es el costo, es que **inventa** (evidencia medida: alucinó un defecto de
contraste que daba 7,27:1, en el ADR de modelo visual de STUDIO).

**Hipótesis:** si se le pasa **el contexto completo en cada llamada** en vez de pedirle que
complete huecos, la alucinación baja lo suficiente para charla trivial (acuse, ordenar, confirmar,
preguntas de estado). Con 2.083 requests ya medidos, el ahorro de pasarlo a primario de lo trivial
es real: el CORE en deepseek cuesta ~0,103 px/req; gemma4 ~0,007.

**Lo que falta medir, y es el punto - esto es una cata, no una decisión:**

1. **Ratio de alucinación con contexto completo** contra el mismo set de preguntas con contexto
   parcial. La medición de STUDIO fue sobre un caso de análisis visual, no sobre charla.
2. **Costo de mandar el contexto completo.** El ahorro por request se puede comer el beneficio si
   el contexto es largo: gemma4 barato por token × contexto grande puede costar más que deepseek
   con contexto chico. Se mide en **px por conversación**, no por request.
3. **Qué es "charla trivial"** - el borde tiene que quedar escrito, o el slot se filtra a tareas
   con consecuencia (verificar, decidir, escribir código).

**Mientras no esté medido, `utilityModel` sigue en `gemma4:cloud`** (donde ya corre: el Helper,
los heartbeats, el pre-filtro, el scorer local) y el CORE sigue en deepseek. El slot de "chat
trivial" no se crea hasta tener las tres mediciones.

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

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| `nemotron-3-super` no rinde en auditoría de camino (la cata de roles midió auditoría de *código*, no de camino) | Probe de tres recorridos antes de asignar; si falla, `muse-spark-open` o `gpt-oss:120b` |
| `muse-spark-open` baja la calidad de redacción y se nota | Revertir a Kimi como **excepción con OK**, no como slot. El fallback barato ya existe |
| Gemma 4 con contexto completo sigue inventando | El slot no se crea sin las tres mediciones; el CORE no se toca mientras |
| El contexto completo sale más caro que deepseek con contexto chico | Medir por conversación; si no conviene, se descarta la hipótesis y queda documentado |
| Volver a "elegir Kimi por olvido" | Este ADR es el criterio de descarte: > 20× baseline = no slot. `check-adr-supersede.py` vigila que la cata no lo contradiga sin supersede |

## Consecuencias

**Lo que se gana:** una familia entera fuera del presupuesto recurrente, con un criterio de
entrada escrito (excepción declarada, no slot). Auditoría de camino con un cerebro distinto al
de ejecución.

**Lo que se acepta:** pérdida del único modelo que no se rebajó en T3 para redacción con voz.
`nemotron-3-super` se propone por evidencia adyacente (auditoría de código) hasta que el probe
propio confirme.

**Lo que no cambia:** CORE (`deepseek-v4.1-flash`), pipeline A/B/C, `utilityModel` (`gemma4:cloud`),
los slots de dev/ops/auditor/critic/planner/mind/studio, ADR-107 y ADR-090.

**Pendiente antes de cerrar:** correr el probe de auditoría de camino (nemotron vs gpt-oss vs
muse, tres recorridos) y la cata de gemma4 con contexto completo (ratio de alucinación, px por
conversación, definición de "charla trivial"). Hasta entonces el slot de auditoría de camino queda
**propuesto, no aplicado**, y el de chat trivial **no existe**.
