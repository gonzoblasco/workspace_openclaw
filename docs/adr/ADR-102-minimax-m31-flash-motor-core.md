# ADR-102: `minimax-m3.1-flash:cloud` como motor del CORE (main)

**Fecha:** 2026-10-20 (revisado 2026-10-24: costo reevaluado como **cuota**, decision de mantener minimax, sin cambio de config)
**Estado:** Aceptado (aplicado al runtime 2026-10-20, verificado; revisado 2026-10-24 sin cambios de runtime)
**Decisores:** Gonzo / Kanam
**Origen:** cata de 8 roles x 5 clases de estres (`docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md`)
**Relacionado:** ADR-090 (asignacion de modelos por rol), ADR-077/088/089 (pipeline A/B), ADR-076 (ningun agente hereda modelo local)
**Modifica:** ADR-090, seccion 1 (tabla de asignacion por rol) - el rol `main` pasa a `minimax-m3.1-flash:cloud`.

---

## Contexto

Ollama sumo `minimax-m3.1-flash` a su catalogo cloud (428B, 1M de contexto, `tools` +
`thinking` + `vision`). Gonzo lo propuso como candidato para el pipeline y decidio
que se lo evaluara **solo a el**: "queremos solo hacerle la cata a este modelo
minimax-m3.1-flash".

La pregunta no era "que puntaje saca" sino "**puede el CORE dejar de correr con
deepseek-v4.1-flash**". Un puntaje absoluto no se lee sin vara: se mide contra los
modelos que hoy ocupan los roles.

## Decision

**El CORE (`main`) y los defaults de agente pasan a `minimax-m3.1-flash:cloud`,
con `deepseek-v4.1-flash:cloud` como unico fallback.** Los demas roles no cambian.

Justificacion por rol (content corregido, escala 0-10):

| Rol | gpt-oss | deepseek | gemma4 | **minimax** | Veredicto |
|---|---|---|---|---|---|
| **main (CORE)** | 7.5 | 7.8 | 6.5 | **8.9** | **cambia** |
| dev | 6.4 | 7.0 | 7.4 | 6.7 | no |
| ops | 7.7 | 8.2 | 6.2 | 6.7 | no |
| mind | 5.0 | 8.7 | 6.0 | 8.6 | no (empate con coste) |
| studio | 7.9 | 9.4 | 6.7 | 9.0 | no |
| critic | 6.2 | 9.1 | 8.2 | 7.2 | no |
| auditor | 6.6 | 8.4 | 7.5 | 7.0 | no |
| planner | 5.9 | 7.5 | 5.1 | 7.1 | no |

El rol que cambia es **precisamente el que mejor le sale**: `main` 8.9 contra 7.8 del
motor vigente, con mejor desempenho en las tres clases que discriminan (restriccion
dura 7.4, la mejor de los cuatro; frontera humana 8.4; canonico 8.1) y 17 wins
absolutos sobre 40 celdas, mas que cualquier otro candidato.

**El resto de los roles no se tocan** porque alli minimax no supera al titular por
margen que justifique su costo operativo, y porque su modo de fallo (espiral de
thinking) es exactamente el que castiga a los roles de presion.

## Por que el CORE y no otro rol

El CORE **orquesta**: delega, verifica, sintetiza. Su costo por latencia no esta en
una ruta critica con otro agente esperando - quien espera es la persona. Los roles de
generacion (dev, critic, studio) si tienen ruta critica: el pipeline A/B espera al
agente que escribe, y 77s de mediana contra 3-14s de los titulares se paga en cada
iteracion.

## Ficha de capacidades (VERIFICADA 2026-10-20)

Fuente: `ollama show minimax-m3.1-flash:cloud` (API local 11434) y la pagina oficial
`https://ollama.com/library/minimax-m3.1-flash`.

| Atributo | Valor | Fuente |
|---|---|---|
| Arquitectura | `minimax-m3` (MoE, 428B) | `api/show` |
| Contexto | **1.000.000** tokens | `api/show` (`minimax-m3.context_length`) |
| Capacidades | `completion`, `tools`, `thinking`, `vision` | `api/show` |
| Tool calling | verificado: devuelve argumentos JSON validos | prueba directa 2026-10-20 |
| Parametro de thinking | `low` / `medium` / `high` / `max` (string) o `true`/`false` (bool) | `api/chat` 2026-10-20 |

**Advertencia operativa (medida):** **`think: false` NO apaga el razonamiento.** Tres
corridas con `think:false` devolvieron 463 / 134 / 193 caracteres de thinking. La
razonamiento es always-on por la via `/api/chat`; solo se puede acotar con
`think: "low"`. Consecuencia: el thinking se factura como output y no hay forma de
pagarlo por debajo.

## Riesgos y mitigaciones

1. **Espiral de thinking / fallo de entrega.** En la primera pasada, 7 de 40 celdas
   de minimax devolvieron 0 caracteres de entrega con 44k-56k caracteres de
   razonamiento. Con `num_predict` x2 se recuperaron 6; **1 quedo irrecuperable en 3
   intentos consecutivos** (`ops-D1`: 100k de thinking, sin entrega).
   *Mitigacion:* el CORE no es un rol de produccion con SLA de entrega, y su fallback
   (`deepseek-v4.1-flash:cloud`) cubre el caso. *Vigilancia:* si aparecen vacios en
   el CORE, el sintoma es thinking quemado, no logica.

2. **Latencia.** Mediana 77s por celda contra 13,9s de deepseek (5,5x) y 3,2s de
   gpt-oss (24x). En el computo agregado de la cata (suma de los 40 turnos) minimax
   sumo 4.327s contra 124s del mas rapido por celda: 35x.
   *Mitigacion:* aceptada por rol (el CORE espera a la persona, no a un pipeline).

3. **Cuota: MEDIDA (2026-10-24).** El "costo" relevante NO es el precio por token sino
   la **cuota de GPU de Ollama Cloud**: el plan legacy no tiene creditos, tiene
   **tasa de uso** (barra de uso semanal con reset). "Barato" = cuánta cuota deja
   gastar, no cuánta plata cuesta. (Correccion 2026-10-24: la cata y la primera
   redaccion de este ADR trataron el costo como dinero, cuando lo que decide es
   cuota.)

   **Precios de referencia (verificados 2026-10-24 en `ollama.com/pricing`):**

   | Modelo | Input /1M | Cached input /1M | Output /1M |
   |---|---|---|---|
   | `minimax-m3.1-flash` | $0.15 | $0.015 | $0.60 |
   | `deepseek-v4.1-flash` (pico) | $0.30 | $0.006 | $1.20 |
   | `deepseek-v4.1-flash` (off-peak) | $0.15 | $0.003 | $0.60 |
   | `glm-5.3-flash` | $0.15 | $0.03 | $0.50 |
   | `gpt-oss:120b` | $0.15 | $0.014 | $0.60 |

   Off-peak = fuera de 12:00-18:00 UTC en dias habiles y todo el fin de semana. O sea
   que **fuera de ese horario minimax y deepseek tienen el mismo precio de output**:
   ahi el 25% de consumo extra de minimax no se compensa con precio.

   **Cuota real medida (panel de Ollama Cloud, 2026-10-24; barra medida en pixeles
   sobre capturas, track = 820 px, usado = 485 px = 59%, consistente con el 60,4%
   que reporta el panel):**

   | Segmento | Modelo | Requests | Px de cuota | % del consumo | Cuota por request |
   |---|---|---|---|---|---|
   | Celeste | `glm-5.3-flash` | 559 | 163 | 33,6% | 0,29 px/req |
   | Violeta | `deepseek-v4.1-flash:1017` | 2.684 | 142 | 29,3% | 0,053 px/req |
   | Rojo | `minimax-m3.1-flash` | 2.201 | 146 | 30,1% | **0,066 px/req** |
   | Oscuro + verde | resto | - | 34 | 7,0% | - |

   **El delta minimax/deepseek de cuota es de 1,25x** (0,066 vs 0,053 px/req): el
   "20-30% superior" que se intuia, confirmado en la unidad que importa. Pero **en
   absoluto son 4 px de 820: 0,5% de la cuota semanal**. Cambiar el default de
   minimax a deepseek para "ahorrar cuota" compra 0,5% y cuesta la calidad medida
   del rol `main` (8,9 contra 7,8).

   *Nota de unidad:* la cuota **no es proporcional a los tokens**. Medido en los
   transcripts del workspace, `glm-5.3-flash:cloud` corre con 274k de cacheRead por
   turno (mas que minimax con 240k) y aun asi consume 0,29 px/req. Por eso el
   px/request hay que leerlo del panel, no derivarlo de los tokens.

   *Dato lateral (GLM):* con 559 requests se come un tercio de la cuota, 5,5x mas
   cuota por request que deepseek. Queda registrado como **dato**, no como
   accion: la decision de este ADR es sobre el rol `main`, no sobre el mix.

   | Modelo | 40 celdas | 33 limpias | coste del fallo (7 celdas) | latencia |
   |---|---|---|---|---|
   | minimax-m3.1-flash | **220.818** | 110.558 | **110.260** | 77,0s |
   | deepseek-v4.1-flash | 56.747 | 37.503 | 19.244 | 13,9s |
   | gpt-oss:120b | 11.304 | 7.392 | 3.912 | 3,2s |
   | gemma4 | 5.860 | 3.869 | 1.991 | 5,3s |

   Ratios minimax/deepseek: **3,89x** en output tokens (40 celdas), **2,95x** en las
   33 limpias (sin el sesgo del retry), 5,5x en latencia, 19,5x contra gpt-oss.
   **El dato que mas pesa: las 7 celdas fallidas consumieron 110.260 output tokens =
   294% de todo lo que consumio deepseek en 33 celdas limpias.** El gasto de minimax
   esta dominado por su modo de fallo, no por su razonamiento normal.
   *Mitigacion:* con el costo en cero hasta el 2026-10-22 no aplica; despues, el
   consumo a vigilar es el de los thinking quemados, no el promedio.
   *Resuelto 2026-10-24:* ver el punto 3 y la seccion "Revision 2026-10-24".

   **Consumo de tokens por turno (medido en los transcripts del workspace, ventana
   de 7 dias al 2026-10-24; `input` + `output` + `cacheRead` por turno):**

   | Modelo | Turnos | in/turn | out/turn | cacheRead/turn |
   |---|---|---|---|---|
   | `minimax-m3.1-flash:cloud` | 5.425 | 4.151 | 289 | 240.413 |
   | `deepseek-v4.1-flash:cloud` | 1.410 | 5.167 | 306 | 139.903 |
   | `glm-5.3-flash:cloud` | 470 | 7.337 | 129 | 274.009 |

   Ojo: esto **no** es la cuota (ver punto 3). Sirve para entender de donde sale el
   gasto de thinking, no para decidir el default.

## Revision 2026-10-24: se mantiene minimax como default del CORE

**Pregunta planteada por Gonzo:** con minimax gastando 1,25x la cuota de deepseek
(0,066 vs 0,053 px/req), conviene sacrificar cuota por la calidad de minimax
(8,9 vs 7,8 en el rol `main`), o volver al motor previo por costo/beneficio?

**Respuesta: se mantiene minimax.** Razon:

1. **El delta absoluto es 4 px de 820 px = 0,5% de la cuota semanal.** No es un
   trade-off, es un ruido. El uso real del CORE ya esta en minimax (2.201 requests
   en la semana del panel) sin que la cuota se haya trabado.
2. **La calidad que se sacrifica esta medida** (cata de 8 roles x 5 clases de
   estres, 160 corridas): 8,9 contra 7,8 en `main`, con 17 wins absolutos sobre 40
   celdas. El trabajo de los ultimos dias (arquitectura, kanam-sudoku-iphone desde
   cero) salio de ahi.
3. **El riesgo real de cuota de minimax no es el overhead del 25%, es la espiral de
   thinking** (7 de 40 celdas en la cata con 0 entrega, 44k-56k caracteres de
   razonamiento). Una espiral de 50k tokens es un request que quema cuota de 5-10
   turnos normales sin entregar nada, y eso **no se ve en la barra**: hay que
   medirlo como requests sin entrega por hora.

**Lo que NO se midio y queda como pendiente:** la tasa de requests quemados
(thinking sin entrega) por hora. Es el unico numero que puede cambiar el
balance, y requiere medirla sobre los transcripts con el campo de thinking
separado.

**Correccion de encuadre (2026-10-24):** el planteo original de la cata
trataba "costo" como precio por token y concluyo que no importaba porque el
modelo era gratis hasta el 2026-10-22. Con el plan legacy la unidad correcta es
**cuota**, y la pregunta correcta no es "que modelo es mas barato" sino "que modelo
deja hacer mas trabajo antes de agotar la cuota".

## Regla de mantenimiento (misma que ADR-090)

Al cambiar un modelo por rol, las **cuatro** fuentes deben coincidir:

1. `~/.openclaw/openclaw.json` (`agents.entries.main.model`, `agents.defaults.model`)
2. `settings` de `memory.db` (`model_primary`, `model_by_agent`) via
   `scripts/managed-blocks.py set ...`
3. Bloques gestionados (`AGENTS.md` `model-operativo`, `docs/SETUP.md` `model-triple`)
   via `scripts/managed-blocks.py apply`
4. Este ADR y ADR-090

Verificacion: `python3 scripts/managed-blocks.py check` (sin drift) y
`python3 scripts/check-single-source.py` (un dato, un dueno).

**Estado al 2026-10-20:** las cuatro fuentes coinciden, verificado.

## Evidencia

- Informe de cata: `docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md`.
- Bateria congelada (los 40 prompts): `docs/ecosystem/cata-minimax-m31-flash-2026-10-20-battery.py`.
- Artefactos crudos (160 registros con `prompt` + `content` + `thinking` separados, y los
  40 veredictos de juez): `playground/model-cata-2026-10-20/` (1.7 MB, fuera de git por
  politica de `playground/`; se regeneran con `run-battery.py` + `judge-battery.py`).

## Lektion de la cata (metodologia, reutilizable)

**Los 2 jueces ciegos fallaron la clase "premisa falsa".** En `main-C1`, gpt-oss
obedecio la regla falsa declarada en el prompt y el juez le dio 6.0 (el mejor
puntaje); minimax detecto la contradiccion y freno (que es lo correcto) y recibio
5.0. Se detecto leyendo los artefactos, no confiando en el score.

*Resolucion:* las clases "premisa falsa" y "fuera de rol" se re-puntuaron **a mano,
celda por celda, leyendo cada artefacto**; los jueces ciegos quedaron para las clases
canonica, ambigua y de restriccion.

*Conclusion:* la evaluacion de comportamiento (obedecer o frenar ante una premisa
falsa) **no es una tarea de prosa**: un juez LLM puede fallarla igual que el modelo.
El judge's score es evidencia, no veredicto.

## Pendientes con fecha

- **Re-cata con K3 como juez:** cancelada por Gonzo (2026-10-20) - costo de recursos
  desmedido para el beneficio. Los 160 registros quedan disponibles si se decide
  revertir: guardan `prompt`, `content`, `thinking` y `eval_count` separados, asi que
  reevaluarlos no requiere re-correr nada.
- **Validacion en uso real:** 2 semanas de uso del CORE con minimax antes de dar el
  rol por cerrado. Fecha de corte: 2026-11-03.
- **Costo real: RESUELTO 2026-10-24.** La gratuidad termino el 2026-10-22 y la
  pregunta de costo/beneficio se respondio con la cuota medida del panel de Ollama
  Cloud (ver "Revision 2026-10-24" y el punto 3 de Riesgos): el delta minimax/
  deepseek es 1,25x por request pero 0,5% de la cuota semanal en absoluto, contra
  una calidad medida de 8,9 vs 7,8 en el rol `main`. **Se mantiene minimax.**
- **Requests quemados por hora (nuevo, 2026-10-24):** medir la tasa de requests
  con thinking quemado (0 entrega) por hora. Es el unico numero que puede
  revertir la decision, porque un request quemado quema cuota de 5-10 turnos
  normales. Requiere medir sobre los transcripts con el thinking separado.

## Artefactos

- Config runtime: `~/.openclaw/openclaw.json` (backup previo:
  `~/.openclaw/openclaw.json.bak-20261020-1526-m31-core`).
- Bloques gestionados: `scripts/managed-blocks.py` -> `AGENTS.md`, `docs/SETUP.md`.
- Informe de cata: `docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md`.
- ADR-090: seccion 1 actualizada el 2026-10-20 con esta asignacion.