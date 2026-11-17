# Cata 2026-11-16 (extendida) — nueve modelos cloud/locales, `low` vs apagado

Extensión de la cata del mismo día con cuatro candidatos más: `minimax-m3.1-flash`,
`glm-5.3-flash`, `gemma4:12b-mlx` (local MLX) y `gemma4:cloud`. Fixture idéntico al original
(`tasks.json`, `evaluate.py`, referencia y defectuosas copiados del probado); 54 celdas.

- Corrida: `20261116T231900` aprox. (ver `results.json` → `run_id`).
- Congelado: `/api/chat`, temperatura 0, `num_ctx` 32768, nonce por celda, auto-escalado
  `num_predict` 4096→24576 (no se disparó en ninguna celda), timeout 300 s, warm-up aparte.
- Diferencia con la original: el daemon respondió mucho más lento en varias celdas
  (T3 de `nemotron` en `low`: 52.6 s contra 3.6 s el mismo día). Son dos corridas distintas;
  los tiempos no se comparan entre fixtures, solo dentro de esta.

## 1. Validación de la suite (dos direcciones)

`SELFTEST OK` antes de correr. **Después de la primera pasada hubo que corregir dos asserts**
(ver §5): el regex de T3 no aceptaba "ID 4" ni "fuera del rango" — redacción correcta que no
coincidía con la que usó la referencia. Se corrigió el assert, se re-validó (referencia PASS,
defectuosa FAIL) y se re-evaluaron las celdas desde el `content` guardado; solo cambiaron dos
celdas de `gemma4:cloud` (de FAIL a PASS). El resto del ranking no se movió.

## 2. La perilla, por candidato (medida)

| Modelo | Niveles declarados | Default de la carta | Tanda `low` | Tanda `off` |
|---|---|---|---|---|
| mimo-v2.6-flash | false, true | true | `true` | `false` ✓ |
| mimo-v2.6-pro | false, true | true | `true` | `false` ✓ |
| mistral-large-4 | sin declarar | razona solo | `low` | **no apagable** |
| muse-spark-open | false…xhigh | **xhigh** | `low` | `false` ✓ |
| nemotron-3-super | false, true | true | `true` | `false` ✓ |
| **minimax-m3.1-flash** | no lista niveles | razona | **`false`** (`true` da HTTP 400) | `false` — **y aun así razona** (ver §4) |
| **glm-5.3-flash** | low, high, max | **max** | `low` | **no apagable**: `false` da HTTP 400 |
| **gemma4:12b-mlx** | 12B local, sin capability `thinking` | — | `false` | `false` (idéntico: no hay perilla) |
| **gemma4:cloud** | false, true | **false** | `true` | `false` ✓ |

Tres defaults de carta vuelven a morder: `glm` arranca en `max`, `muse` en `xhigh`. `minimax`
no publica niveles y rechaza el booleano `true`.

## 3. Tanda `low` — el contenido empata en 8 de 9

| Modelo | Pass | Eval prom. | Thinking prom. | Wall prom. (s) |
|---|---|---|---|---|
| **glm-5.3-flash** | 3/3 | **122** | 11 | **1.1** |
| **minimax-m3.1-flash** | 3/3 | **220** | 560 | 6.8 |
| mimo-v2.6-flash | 3/3 | 279 | 215 | 1.9 |
| mimo-v2.6-pro | 3/3 | 397 | 422 | 1.5 |
| muse-spark-open | 3/3 | 431 | 1165 | 3.8 |
| mistral-large-4 | 3/3 | 475 | 1217 | 10.4 |
| nemotron-3-super | 3/3 | 926 | 2381 | 25.7 |
| gemma4:cloud | 3/3 | 989 | 2135 | 2.2 |
| **gemma4:12b-mlx** | **2/3** | 126 | 0 | 5.7 |

`glm-5.3-flash` gana en costo por lejos: **122 eval tokens promedio**, un tercio de
`mimo-flash` y una octava parte de `nemotron`. Además es el más rápido (1.1 s). `minimax`
segundo en costo, pero 6x más lento.

`gemma4:12b-mlx` falla T3 con `TOTAL: 135.74`: restando donde hay que sumar los reembolsos
(−30 contado dos veces) y con la fila EUR dentro. No es truncación: `eval_count` 61, `done=stop`.

## 4. Tanda `off` — tres hallazgos nuevos

**a. `gemma4:cloud` mejora con razonamiento apagado.** En `low` gasta 1364/662/940 eval tokens
para lo mismo que entrega en 267/96/53 con `off`. Con T1 el ahorro es de 5x. Su default de
carta ya es `false`: pedirle thinking es pagar por un razonamiento que no mejora el resultado.

**b. `minimax-m3.1-flash` no obedece el apagado.** Con `think:false` (el único valor que
acepta) devuelve 349/546/357 chars de thinking. Pasa 3/3, pero la columna `off` no es una
columna apagada: es una segunda corrida con la perilla ignorada. Va como observación, no como
evidencia de comportamiento sin razonamiento.

**c. `nemotron-3-super` cambió de resultado entre corridas.** En esta tanda `off` acertó T3
(103 eval, `pass`); el mismo día, en la corrida original, dio 335.73 dos veces. Un pass en una
corrida no borra el fallo reproducido: el veredicto es **inestable con razonamiento apagado**,
y se sostiene el fallo medido dos veces.

`gemma4:12b-mlx` en `off` es idéntico a `low` (no tiene perilla), falla T3 igual.
`glm-5.3-flash` y `mistral-large-4`: no medidos, con motivo.

## 5. Hallazgos del runner (lo que produjo un resultado falso)

1. **Aserts demasiado estrechos.** T3 exigía `\beur\b|fila 4` y `fila 7|fuera del trimestre`.
   `gemma4:cloud` dijo "id 4: moneda no válida (EUR)" y "id 7: fuera del rango de fecha (Q4)":
   correcto en sustancia, FAIL por redacción. **Regla confirmada: el regex valida la verdad, no
   la forma de la referencia.** El kit ahora puede re-evaluar desde `content` guardado sin
   re-correr la cata, que es lo que salvó la corrida.
2. **Latencia no comparable entre corridas.** `nemotron` T3 `low`: 3.6 s en la corrida original,
   52.6 s acá, mismo modelo y prompt. El costo en tokens sí es comparable; el tiempo requiere
   réplica.
3. **`think:true` no es universal.** `minimax` y `glm` devuelven HTTP 400 con el booleano; la
   sonda tiene que mapear por modelo **antes** de la tanda (ya documentado, se aplicó).

## 6. Veredicto

| Rol | Modelo | Motivo |
|---|---|---|
| **Mejor costo** | `glm-5.3-flash` (`low`) | 3/3 con 122 eval promedio y 1.1 s; el más barato de los nueve |
| **Mejor barato con razonamiento visible** | `minimax-m3.1-flash` | 3/3 con 220 eval, pero 6x más lento y no se deja apagar |
| **Mejor local** | `gemma4:12b-mlx` | el único local; 2/3, falla la aritmética de T3; sirve para roles sin cuentas |
| **Evitar para contabilidad** | `gemma4:12b-mlx`, `gemma4:cloud` en `low` | gemma4 12b yerra el neto de reembolsos; gemma4 cloud paga 5x tokens sin ganar |
| **No usar con razonamiento apagado** | `nemotron-3-super`, `mistral-large-4` (no apagable), `minimax` (ignora el apagado) | inestable / imposible / desobedece |

Los nueve empatan en contenido en `low` salvo `gemma4:12b-mlx`. El desempate es costo:
`glm-5.3-flash` primero, `minimax` segundo, `mimo-v2.6-flash` tercero.

## 7. Límites de esta medición

- Tres tareas de una sola llamada: mide respuesta, no agencia (sin tool calling, sin
  multi-turno, sin filesystem).
- Una corrida por celda. La varianza de `nemotron` T3 `off` (fallo reproducido y pass acá)
  muestra que hace falta réplica para cualquier caso de comportamiento apagado.
- `glm-5.3-flash` solo tiene tanda `low`: no se puede evaluar su comportamiento sin razonamiento.
- `gemma4:12b-mlx` corre local: sus tiempos incluyen carga del modelo en la primera celda.

## 8. Reproducir

```bash
cd bench/cata-2026-11-16-extended
python3 /Users/gonzoblasco/.openclaw/workspace/scripts/cata-kit.py check .
python3 /Users/gonzoblasco/.openclaw/workspace/scripts/cata-kit.py run .
python3 /Users/gonzoblasco/.openclaw/workspace/scripts/cata-kit.py analyze .
```

## 9. Validación con evaluador ciego (CONTENT vs CLEANLINESS)

Segundo evaluador: `kanam-mind` (`deepseek-v4.1-flash`), contexto aislado, sin acceso a
`results*.json`, `evaluate.py` ni `analyze.py`. Corrió los bloques T1/T2 de los candidatos en
sus propios casos y recomputó T3 a mano. **Sus afirmaciones se auditaron contra los artefactos
antes de aceptarlas** (dos salieron ciertas, una parcial, una falsa).

**Convergencia:**

- CONTENT: coincide en el único fallo de contenido, `gemma4:12b-mlx` T3 → 1/5, las dos tandas.
  Recomendó 135.74 y dijo por qué está mal: 120.50 − 30.00 + 45.25 = 135.75, y omite el 99.99
  que sí corresponde. Error aritmético más criterio de deduplicación mal aplicado.
- El empate de contenido en `low` es real; el desempate es costo.
- Los tres modelos con problema de perilla (`mistral`, `glm`, `minimax`) quedaron fuera o
  marcados igual que en el análisis propio.

**Divergencia (el dato):**

- **CLEANLINESS**: el análisis mecánico mide prosa fuera del bloque. El ciego encontró residuos
  *dentro*: `muse-spark-open low T1` deja un chequeo `start > end` redundante con `s > e`
  (líneas 7 y 11) y doble parseo; `mimo-v2.6-pro low T1` gasta una docstring de 12 líneas en una
  función de 15 para un pedido de "solo el bloque" (3/5). Ambas verificadas contra el archivo.
- **El ciego sobreconfía en la prosa del modelo**: llamó "exclusiones bien hechas" a las de
  `gemma4:12b-mlx` T3, que lista mal la fila 7 ("fuera del rango de Q3", en realidad es el 1 de
  octubre, fuera de Q3 por arriba). La frase es plausible, el hecho es impreciso. Refuerza la
  regla del step 7: leer el artefacto, no el resumen.
- **Un hallazgo inestable**: reportó que `gemma4:cloud off T1` mete comentarios explicativos
  (líneas 18 y 26). El artefacto guardado no los muestra; puede haber leído una versión de otra
  tanda. No se acredita sin evidencia.

**Consecuencia para el kit:** el evaluador ciego aporta el eje de limpieza semántica que el
runner no mide, pero **no se acredita sin auditar cada frase contra el archivo**. El paso 5 del
`SKILL.md` del kit ya lo pide así ("comparar casilla por casilla"); acá se cumplió y filtró una
afirmación falsa y una imprecisa.

**Ranking final (dos ejes, sin promediar):**

| Eje | Ganador | Motivo |
|---|---|---|
| CONTENT | empate en 8 de 9, con `glm-5.3-flash` primero por costo (122 eval, 1.1 s) | ninguna tarea discriminó al resto |
| CLEANLINESS | `glm-5.3-flash`, `minimax-m3.1-flash`, `gemma4:12b-mlx low` en T3 (5/5) | entregables mínimos |
| Peor | `gemma4:12b-mlx` (T3, 1/5 en las dos tandas) | error aritmético con exclusiones parcialmente correctas |
