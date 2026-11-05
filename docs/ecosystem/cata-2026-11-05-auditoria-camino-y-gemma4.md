# Cata 2026-11-05 (2): auditoría de camino y `gemma4` con contexto completo

**Estado:** medido, con dos slots en veredicto claro y dos preguntas abiertas
**Origen:** ADR-109 pide estas dos catas antes de fijar el slot de auditoría de camino y antes de crear (o no) el slot de chat trivial
**Harness:** `/tmp/cata_path_audit.py` y `/tmp/cata_gemma.py` (temporales; los prompts van copiados acá)

---

## 1. Auditoría de camino: `nemotron-3-super` / `gpt-oss:120b` / `muse-spark-open`

Tres recorridos de un agente CORE. La trampa está en el método: **B es un recorrido limpio** (el paso 5
verifica el repo de verdad, el 6 commitea atómico, el 7 actualiza el daily) y **C también lo es**
(el agente declara que no puede ver los checks y pide OK en vez de reportar "todo verde"). Un
auditor que encuentre riesgos en B o C tiene falso positivo; el que no encuentre nada en A tiene
falso negativo.

| Modelo | Latencia | Tiempo total | A (riesgo real) | B (limpio) | C (limpio) | Veredicto |
|---|---|---|---|---|---|---|
| `nemotron-3-super:cloud` | 3,7-6,8 s | **~14 s** (3 corridas) | ✅ 2/2 (verificación + daily) | ❌ **falso positivo**, y solo uno | ❌ **6 inventados** (credenciales interceptadas, deadlock, falta de fallback) | **Descartado** para este slot |
| `gpt-oss:120b-cloud` | 4,1-6,5 s | **~17 s** | ✅ 3/3 (verificación, gates, commit a ciegas) | ❌ **4 inventados** (cobertura insuficiente, code review, "filtración de la salida cruda") | ❌ **5+ inventados** | **Descartado** para este slot |
| `muse-spark-open:cloud` | 4,5-6,5 s | ~18 s | ✅ 3/3 (verificación, gates, commit a ciegas) | ✅ **0 riesgos reales**, y explica por qué cada paso cumple | ✅ **0 riesgos reales** | **Ganador** |

**Números crudos** (tokens de salida por corrida): nemotron 695 / 1.200 (truncado) / 688 · gpt-oss
1.192 / 1.136 / 684 · muse 1.527 / 1.092 / 761. Muse es el que más escribe y el que no inventa.

**Hallazgo del método, y es el importante:** los dos modelos que la cata vieja recomendaba
(Nemotron por la prueba de auditoría de *código*, gpt-oss por ser el A del pipeline) **inventan
riesgos en recorridos limpios**. Nemotron es el peor: 6 hallazgos fabricados en C, incluyendo
*"posible exposición de credenciales"* en un recorrido donde el agente **pide** autorización en vez
de manejar tokens. Un auditor así no es ruidoso: es inútil, porque su reporte limpio también se
ignora o se obedece de más.

**Nota de honestidad del harness:** en la primera corrida muse devolvió contenido vacío en A con
`num_predict=1200`. Repetido con 2.000 y 4.000, responde completo en 6-8 s (`done_reason: stop`,
~1.530 tokens). Era el presupuesto de tokens de la llamada, no el modelo. **Para un slot, el
`num_predict` tiene que estar especificado en el rol**, o el slot falla en silencio.

**Decisión:** el slot de auditoría de camino va a **`muse-spark-open`**. Es el único que distinguió
el recorrido con un riesgo real de los dos limpios, y es además el modelo elegido para redacción con
voz: en una auditoría de camino de uso periódico, pagar 10 s por corrida no es un costo.

---

## 2. `gemma4:cloud` como chat trivial: contexto completo vs parcial

Siete llamadas por modo, temperatura 0, mismas preguntas, mismo prompt de sistema de 580 tokens
(el estado real del workspace) contra uno de 40 tokens (usuario + agente).

| Modo | Tokens de input (7 llamadas) | Tokens de salida | Total | Tokens por conversación |
|---|---|---|---|---|
| Contexto **completo** | 4.099 | 845 | **4.944** | ~706 |
| Contexto **parcial** | 319 | 1.293 | **1.612** | ~230 |

**La hipótesis de Gonzo se confirma en lo factual y falla en lo económico.**

- **Factual: completo gana 5/7 a 0/7.** Con contexto parcial: el CORE es *"GPT-4o (Omni)"* (falso),
  `kanam-ops` es prosa de folleto que no menciona ningún modelo, `kimi se va o se queda` se
  contesta con Kimi de Moonshot, y las dos preguntas de hora **inventan una fecha y una hora
  completas** (dijo Tokio 05:00 del 8 de noviembre de 2024, y 03:34 del 20 de mayo, en dos corridas
  distintas). Con contexto completo: 8 roles correctos, CORE correcto, ops correcto, trampa
  resistida, Kimi fuera. **Ningún falso positivo.**
- **Económico: el contexto completo cuesta 3,1× las mismas 7 llamadas.** 580 tokens de input
  fijos por llamada contra 40. En charla trivial la salida es corta, así que el contexto es el
  costo dominante, no la respuesta.
- **Pero el parcial no es más barato: es inservible.** Gasta 1,6k tokens produciendo respuestas
  falsas que después hay que corregir, y corregir cuesta más que haberlo hecho bien.

**El número que decide** (con el baseline del panel: deepseek ≈ 0,103 px/req, gemma4 < 0,01
px/req):

- **CORREGIDO 2026-11-05 con los px reales del panel** (barra de sesión de 944 px): deepseek
  129 px / 313 req = **0,412 px/req**; muse 13 px / 39 req = **0,333 px/req**; glm 3 px / 15 req =
  **0,200 px/req**. Muse cuesta el **81%** de un request del CORE y glm el **49%** - no el 10% que
  decía esta sección. La versión anterior afirmaba "mas de 10x mas barato" sin haberlo medido: era
  extrapolación de la barra vista a ojo, no un número.
- Con esa base, gemma4 con contexto completo (~706 tok/llamada) sigue siendo más barato que el
  CORE, **pero por un margen que hay que medir con su propio px/req**, no por un orden de
  magnitud supuesto. El ahorro existe; la magnitud estaba inventada.
- **La condición es no cortar el contexto**: barato + contexto recortado = fabulación con costo.

**Lo que queda abierto, y es el único freno real:** el probe no midió el caso que causó el
descarte de STUDIO (alucinar un defecto de contraste que medido daba 7,27:1). El contexto completo
no demostró que gemma4 deje de inventar en *análisis*; demostró que no inventa cuando el dato
**está en el prompt**. Para charla trivial eso alcanza. Para cualquier tarea donde el dato no esté
en el prompt (verificar, analizar, auditar), gemma4 sigue sin servir, y el borde queda escrito así:

> **"Charla trivial" = toda llamada cuyo dato de respuesta ya está en el contexto entregado.**

Fuera de eso, no es chat trivial.

**El criterio general, corregido tras la objeción de Gonzo del 2026-11-05:** la línea no separa
"trivial" de "técnico", separa **"la salida se verifica contra algo" de "la salida se sostiene sola"**.
Cuando se verifica -una afirmación sobre el repo, un hecho, un número-, inventar es un defecto.
Cuando se sostiene sola -narrativa, redacción con voz, una idea de producto-, inventar es el trabajo.
Las dos categorías aplican a cualquier modelo, y son las que hay que mirar antes de asignar un slot.

**La objeción era válida y estaba mal explicada:** decir "inventar es un defecto" y al mismo tiempo
darle a muse el slot de auditoría suena contradictorio. No lo es: en auditoría la salida de muse se
verifica contra un recorrido que **ya ocurrió** -por eso ganó, porque no inventó-, y en la contraprueba
del chat trivial se verificaba contra el estado del workspace -por eso perdió-. **Muse no cambió de
naturaleza entre las dos pruebas; cambió el criterio con que se lo evaluaba.**


---

## 3. Contraprueba: ¿y `muse-spark-open` para lo trivial? (no)

Mismas 7 preguntas, mismos dos modos, `num_predict=1500`.

| Modelo / modo | Input | Output | Total (7) | Segundos | Correctas | Falsos positivos |
|---|---|---|---|---|---|---|
| `gemma4` completo | 4.099 | 845 | **4.944** | ~10 s | **5/7** | 0 |
| `gemma4` parcial | 319 | 1.293 | 1.612 | ~9 s (con 1 fallo) | **0/7** | varios |
| `muse` completo | 3.743 | **4.703** | 8.446 | **33,8 s** | **~6/7** | 0 |
| `muse` parcial | 390 | 4.519 | 4.909 | 34,6 s | **~2/7** | **peor que gemma4** |

**Muse con contexto completo acierta un poco más que gemma4, y es la única diferencia a su favor.**
Ordena los 8 roles bien, resiste la trampa de ops, contesta Kimi con el ADR y en la hora de Tokio
calculó el desfase correcto (UTC+9 vs UTC-3 = 12 h) en vez de inventar una fecha. Eso es mejor que
gemma4, que en ese probe se quedó corta.

**Y en todo lo demás pierde por goleada:**

- **8.446 tokens contra 4.944.** El triple de salida que gemma4 para un acuse de "ok". Un modelo que
  escribe 4.703 tokens para siete respuestas triviales no es un modelo de chat trivial: es un modelo
  que redacta *todo*, incluidas las respuestas de una línea.
- **34 s contra 10 s.** En charla trivial la latencia se siente: "ok" en 3 s es aceptable, "ok" en 6 s
  con 372 tokens de salida es una espera para nada.
- **Con contexto parcial es peor que gemma4**, y de una forma que da más vergüenza: preguntado por el
  modelo del CORE contestó *"Soy Muse Spark, creado por Meta"*; preguntado por `kanam-ops` dijo que
  no tenía información (honesto, pero inútil); y "¿kimi se queda o se va?" lo resolvió con **Kimi
  Antonelli en Mercedes**. No inventó una hora como gemma4, pero inventó otro mundo entero.

**La razón estructural, y es la que decide:** muse es un modelo de profundidad -auditoría, redacción
con voz, análisis-, y se nota en la longitud de su salida. Para lo trivial el costo no es solo el
token: es el modelo entero trabajando donde no hace falta. Gemma4, que es más chico y más directo,
produce menos y cuesta menos en las dos dimensiones.

**Contra el argumento de "ya está cargado, no sumo otro modelo":** muse ya es slot de auditoría y de
redacción, así que sumarlo a chat trivial no agrega una familia. Pero un slot no se justifica por estar
cargado, sino por ser el mejor para *esa* tarea, y el costo se paga por tarea. **Gemma4 sigue siendo el
modelo del chat trivial.**

**El único escenario donde muse trivial tendría sentido:** un único modelo para todo, con un solo
prompt de sistema y un solo contexto, aceptando pagar 8,4k tokens por conversación. No es el modelo
elegido en ningún slot hoy y el ADR-109 ya lo dejó fuera por costo (1 request ≈ 24-26× deepseek en la
familia Kimi; muse no es de esa familia, pero 4.703 tokens de salida por siete llamadas cortas es el
mismo problema en otra escala).

---

## 4. Lo que esta cata NO prueba

- **`muse-spark-open` en auditoría de camino real** (no un recorrido sintético de seis pasos). El
  siguiente paso es correrlo sobre un cierre de sesión real del workspace y comparar contra lo que
  Kanam encontró a mano.
- **El costo de muse a escala**: 3 corridas ~18 s no dicen nada del px/req; se lee en el panel
  después de un mes de uso periódico, no de una corrida.
- **`gemma4` con contextos de más de 580 tokens.** El workspace real puede mandar 3-5k de contexto
  por llamada; el punto de quiebre entre "más barato que deepseek" y "más caro" está en el mismo
  cálculo (706 tok en gemma4 vs ~2.000 tok de contexto del CORE) y hay que medirlo con el contexto
  real, no con este recorte.

---


