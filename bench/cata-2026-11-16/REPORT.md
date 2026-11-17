# Cata 2026-11-16 — cinco modelos cloud, razonamiento `low` vs apagado

Corrida de prueba del skill `harness-model-comparison` con la política nueva: **`low` por
defecto** y una tanda con razonamiento **apagado** para observar comportamiento. Fixture
versionado en `bench/cata-2026-11-16/` (ver `README.md`).

- Fecha: 2026-11-16, corrida `20261116T223006` (la primera, con artefactos pisados por un bug
  de naming, se descartó; esta es la segunda y completa).
- Candidatos: `mimo-v2.6-flash:cloud`, `mimo-v2.6-pro:cloud`, `mistral-large-4:cloud`,
  `muse-spark-open:cloud`, `nemotron-3-super:cloud`.
- Tareas: T1 código con casos borde, T2 debugging de un defecto de redondeo, T3 análisis de
  CSV con trampas (duplicado, otra moneda, fila fuera de Q3).
- Congelado: una sola vía (`POST /api/chat`), temperatura 0, `num_ctx` 32768, prompt verbatim
  con nonce idéntico para todos los modelos de la celda, `num_predict` con auto-escalado
  4096→24576 (no hizo falta escalar en ninguna celda), timeout 300 s, warm-up fuera del
  throughput.

## 1. Validación de la suite (dos direcciones)

```
REF  T1-chunk-ranges.py    pass=True    REF  T2-invoice-bug.py  pass=True    REF  T3-q3-revenue.md  pass=True
BAD  T1…exclusive.py       FAIL (corte exclusivo)      BAD  T1…gaps.py     FAIL (huecos)
BAD  T1…novalidation.py    FAIL (days=0 cuelga)        BAD  T2…perline.py  FAIL (108.89 vs 108.90)
BAD  T3…naive.md           FAIL (585.73)
SELFTEST OK
```

## 2. La perilla, por candidato (medida, no supuesta)

| Modelo | Niveles declarados (carta) | Default de la carta | Tanda `low` usada | Tanda `off` |
|---|---|---|---|---|
| mimo-v2.6-flash | false, true | true | `true` | `false` ✓ (thinking 0) |
| mimo-v2.6-pro | false, true | true | `true` | `false` ✓ |
| mistral-large-4 | (sin niveles declarados) | razona sin pedirlo | `low` | **no apagable**: `false` se ignora y sigue razonando (333 chars en la sonda, 762–1450 en la cata); el booleano JSON da HTTP 400 |
| muse-spark-open | false, low, medium, high, xhigh | **xhigh** | `low` | `false` ✓ |
| nemotron-3-super | false, true | true | `true` | `false` ✓ |

Consecuencia de la política: **muse-spark-open hereda `xhigh` si no se fija nada**, que es
exactamente el default caro que el skill ahora prohíbe heredar. Mistral no acepta apagado: su
fila `off` va como **no medida**, no como 0.

## 3. Tanda `low` — los cinco empatan

| Modelo | Pass | Eval tokens (T1/T2/T3) | Thinking chars | Wall time (s) |
|---|---|---|---|---|
| mimo-v2.6-flash | **3/3** | 153 / 147 / 534 | 63 / 303 / 497 | 1.1 / 1.0 / 2.4 |
| mimo-v2.6-pro | **3/3** | 762 / 239 / 418 | 1440 / 605 / 317 | 2.7 / 1.3 / 1.6 |
| mistral-large-4 | **3/3** | 409 / 272 / 624 | 1185 / 762 / 1450 | 4.3 / 3.0 / 9.2 |
| muse-spark-open | **3/3** | 336 / 247 / 625 | 565 / 715 / 1650 | 3.3 / 17.2 / 9.2 |
| nemotron-3-super | **3/3** | 428 / 312 / 702 | 911 / 867 / 1606 | 1.6 / 1.2 / 2.7 |

**El empate es el resultado de contenido**: con estas tres tareas, ninguno se distingue en
corrección. El desempate es costo y latencia, y ahí `mimo-v2.6-flash` gana con claridad
(~278 eval/tarea promedio contra 435–481 del resto; 1.5 s promedio contra 1.8–9.9 s), seguido
de `mimo-v2.6-pro`. `muse-spark-open` es el más caro en razonamiento y el más lento; mistral
el más lento en T3. Tres tareas no alcanzan para declarar superioridad de contenido.

## 4. Tanda `off` — dónde se rompe y quién razona en el output

| Modelo | Pass | Eval tokens | Modo observado |
|---|---|---|---|
| mimo-v2.6-flash | 3/3 | 150/74/71 | entrega directa en las 3; sin thinking |
| mimo-v2.6-pro | 3/3 | 138/82/264 | entrega directa en T1/T2; en T3 imprime el desglose de la suma antes de `TOTAL:` (razona en el output, versión leve) |
| muse-spark-open | 3/3 | 365/279/665 | entrega directa |
| nemotron-3-super | **2/3** | 165/93/83 | entrega directa, pero en T1 devuelve el código sin cercas |
| mistral-large-4 | — | — | no medido (no apagable) |

**El fallo real de la cata está en nemotron con razonamiento apagado, T3:** reporta
`TOTAL: 335.73` y en el mismo texto dice *"id=3 (segunda aparición): duplicado, solo se cuenta
la primera"*. El total 335.73 es justamente el que **incluye** el duplicado (585.73 − 250 EUR).
Se contradice a sí mismo: la explicación es correcta, la aritmética no. Reproducido en dos
corridas independientes. Con `low` acierta (235.74).

**Modo (b) — razona dentro del entregable — aparece, pero es dependiente de la tarea.**
En la sonda corta de aritmética, nemotron con `false` escribió el cálculo en `content`
(*"El tren sale a las 14:05… Sumando: - Horas: 14 + 2…"*) con `thinking` vacío. En T1–T3, en
cambio, entregó código/resultado directo. mimo-pro en T3 apagado mostró el mismo patrón leve
(desglose de filas antes del total). No hay un "leak general" por familia: es un modo que se
activa cuando la tarea exige cuentas y no hay canal de thinking.

## 5. Hallazgos del runner (lo que costó un resultado falso)

1. **Ollama cachea por `model` + prompt.** La primera sonda, sin nonce, devolvió para
   `think:false` exactamente el mismo `eval_count` y `thinking_chars` que `think:true` en tres
   modelos: parecía que la perilla no viajaba. Con nonce único por celda, `false` bajó a
   thinking 0 / eval 6. **Sin nonce, la cata mide la caché.** (Agregado al skill.)
2. **Bug de naming de artefactos:** `Path.with_suffix(".md")` sobre un nombre con punto
   (`mimo-v2.6-...`) truncó las salidas a `mimo-v2.md` y pisó celdas. Corregido con
   concatenación explícita; por eso se re-corrió toda la cata.
3. **Un proceso lanzado con `nohup ... &` dentro de una sesión de shell no sobrevivió** al
   cierre de esa sesión (murió a mitad de celda, sin traza). Se re-lanzó como job de fondo
   independiente.

## 6. Veredicto

- **Mejor costo/beneficio: `mimo-v2.6-flash`** — empata en contenido con todos, es el más
  barato en tokens de salida y el más rápido en las dos tandas.
- **`mimo-v2.6-pro`**: mismo contenido, ~1.7x eval y un poco más lento; no hay evidencia acá
  que justifique la diferencia.
- **`muse-spark-open`**: correcto, pero el más caro en thinking y el más lento; su default
  `xhigh` lo hace además peligroso si se hereda.
- **`mistral-large-4`**: correcto y con thinking no apagable; si el rol necesita razonamiento
  apagado, no sirve.
- **`nemotron-3-super`**: rápido y barato, pero con razonamiento apagado falla una cuenta que
  él mismo explica bien. No usarlo apagado en tareas aritméticas; con `low` está bien.

## 7. Límites de esta medición

- Tres tareas de una sola llamada: mide respuesta, no agencia (no hay tool calling, ni
  filesystem, ni multi-turno).
- Una sola corrida por celda (excepto el fallo de nemotron, reproducido). La varianza de
  latencia de muse T2 (17.2 s contra 2.1 s en otra corrida) muestra que un tiempo aislado no
  es un dato.
- El eje CLEANLINESS quedó mecánico en el análisis (prosa fuera del entregable / cercas); la
  validación con evaluador ciego está en la sección 9 y **corrige** ese eje.

## 8. Reproducir

```bash
cd bench/cata-2026-11-16
python3 evaluate.py --selftest
python3 run_cata.py
python3 analyze.py
```

## 9. Validación con evaluador ciego (CONTENT vs CLEANLINESS)

Segundo evaluador: `kanam-mind` (`deepseek-v4.1-flash`), contexto aislado, sin acceso a
`results*.json`, `cata.log`, `evaluate.py` ni `analyze.py`; puntuó las 27 celdas contra el
enunciado, recomputando T3 a mano.

**Dónde coincide con la suite (convergencia):**

- CONTENT: todo correcto salvo **nemotron `off` T3** (2/5, mismo 335.73). Misma celda, mismo motivo.
- El empate de contenido en la tanda `low` es real; el desempate es costo/latencia.
- nemotron `low` impecable; la degradación está atada a la tanda sin razonamiento.

**Dónde discrepa (y la divergencia es el dato):**

- El análisis mecánico marcó CLEANLINESS perfecta en todas las celdas (0 chars de prosa antes
  del bloque). El ciego encontró residuos **dentro** del entregable que esa métrica no ve:
  `muse-spark-open low T1` deja un comentario de razonamiento (`# Alternative increment to avoid
  drift: current += step`), una variable `step` muerta y un `try/except: raise` inútil → 3/5.
- `mimo-v2.6-pro off T3` devuelve el número correcto pero **después** de un ledger fila por fila
  y un `Sum:`; el `TOTAL:` no abre la respuesta → 2/5 en limpieza.
- `mimo-v2.6-flash low T3` agrega una sección "Filas incluidas" que no se pidió → 4/5.

**Consecuencia:** la métrica de limpieza del runner (`prose_chars` fuera del bloque) mide
formato, no limpieza semántica; el eje que decide es el del entregable usable por el agente
siguiente. Para la próxima corrida: contar además comentarios de razonamiento y código muerto
en el bloque, o dejar CLEANLINESS directamente al evaluador ciego.

**Ranking final de la cata (dos ejes, sin promediar):**

| Eje | Ganador | Motivo |
|---|---|---|
| CONTENT | empate: mimo-flash, mimo-pro, muse (30/30); mistral 15/15 en su tanda | ninguna tarea discriminó |
| CLEANLINESS | mistral-large-4 (15/15); con tanda completa, mimo-v2.6-flash (29/30) | entregables quirúrgicos |
| Peor | nemotron-3-super `off` (12/15 content, T1 sin cercas) | única respuesta numéricamente falsa |

