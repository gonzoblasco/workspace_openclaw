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

- gemma4 con contexto completo: ~706 tok/llamada sobre un modelo **> 10× más barato por token**
  que deepseek → **sigue siendo más barato que deepseek, incluso con el contexto completo**. El
  chat trivial de hoy va al CORE en deepseek con contexto grande: pagar 706 tok baratos en vez de
  ~100 tok caros es una mejora de orden de magnitud.
- **La condición es no cortar el contexto**: barato + contexto recortado = fabulación con costo.

**Lo que queda abierto, y es el único freno real:** el probe no midió el caso que causó el
descarte de STUDIO (alucinar un defecto de contraste que medido daba 7,27:1). El contexto completo
no demostró que gemma4 deje de inventar en *análisis*; demostró que no inventa cuando el dato
**está en el prompt**. Para charla trivial eso alcanza. Para cualquier tarea donde el dato no esté
en el prompt (verificar, analizar, auditar), gemma4 sigue sin servir, y el borde queda escrito así:

> **"Charla trivial" = toda llamada cuyo dato de respuesta ya está en el contexto entregado.**

Fuera de eso, no es chat trivial.

---

## 3. Lo que esta cata NO prueba

- **`muse-spark-open` en auditoría de camino real** (no un recorrido sintético de seis pasos). El
  siguiente paso es correrlo sobre un cierre de sesión real del workspace y comparar contra lo que
  Kanam encontró a mano.
- **El costo de muse a escala**: 3 corridas ~18 s no dicen nada del px/req; se lee en el panel
  después de un mes de uso periódico, no de una corrida.
- **`gemma4` con contextos de más de 580 tokens.** El workspace real puede mandar 3-5k de contexto
  por llamada; el punto de quiebre entre "más barato que deepseek" y "más caro" está en el mismo
  cálculo (706 tok en gemma4 vs ~2.000 tok de contexto del CORE) y hay que medirlo con el contexto
  real, no con este recorte.
