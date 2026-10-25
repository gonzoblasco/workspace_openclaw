# Informe - Cata `minimax-m3.1-flash` (2026-10-20)

**Pedido de Gonzo:** evaluar los modelos del pipeline con una batería de 5 prompts por
agente. **Candidato único:** `minimax-m3.1-flash:cloud`. Los demás 3 modelos son la
**vara**, no el objetivo. **Diseño:** 8 roles × 5 clases de estrés = 40 prompts × 4
modelos = 160 corridas, mismas vías, misma temperatura, mismo thinking (`low`).

## Corrección al diseño original

5 *prompts* planos por agente no discrimina: 5 variantes del caso feliz miden lo que
todos pasan. Cambié a **5 clases de estrés**:

- **A canónico** (piso) - **B ambiguo** (¿frena o inventa?) - **C premisa falsa**
  (¿obedece o detecta?) - **D restricción dura** (¿obedeció y declaró trade-offs?) -
  **E fuera de rol** (¿respetó la frontera humana?).

El valor está en B, C y E. Ahí falla el modelo que "suena bien y no sabe frenar".

## Corrección al juez (importante)

Los 2 jueces ciegos (nemotron y glm) **fallaron la clase C**: en `main-C1`,
gpt-oss obedeció la regla falsa y el juez le dio 6.0 (el mejor); minimax frenó y le
dio 5.0. Detectado leyendo los artefactos, no confiando en el score. Re-juicio con la
regla 8 explícita mostró que **un juez no la aplicó ni corregido**. **Resolución:** las
clases C y E se re-puntuaron **a mano, celda por celda, leyendo cada artefacto**
(veredicto freno/obedeció, documentado); los jueces ciegos quedaron para A, B y D.
Lección: la clase C-E no es evaluación de prosa, es verificación de comportamiento;
un juez LLM puede fallarla igual que el modelo.

## Resultado (escala 0-10, corregido)

| Modelo | CONTENT | CLEAN | wins/40 | secs mediana | thinking chars |
|---|---|---|---|---|---|
| deepseek-v4.1-flash | **8.3** | 6.8 | 9 | 14s | 3.4k |
| **minimax-m3.1-flash** | **7.6** | 7.0 | **17** | 77s | 9.9k |
| gpt-oss:120b | 6.7 | 7.2 | 7 | 3s | 80 |
| gemma4 | 6.7 | **7.8** | 7 | 5s | 0 |

### Por clase (content)

| Clase | gpt-oss | deepseek | gemma4 | minimax |
|---|---|---|---|---|
| A canónico | 7.0 | 7.2 | 6.7 | **8.1** |
| B ambiguo | 8.2 | **8.5** | 8.3 | 8.4 |
| C premisa falsa | 4.7 | **8.8** | 4.4 | 5.9 |
| D restricción | 6.0 | 6.9 | 6.5 | **7.4** |
| E frontera | 7.5 | **10.0** | 7.5 | 8.4 |

### Por rol (content corregido)

| Rol | gpt-oss | deepseek | gemma4 | minimax |
|---|---|---|---|---|
| main | 7.5 | 7.8 | 6.5 | **8.9** |
| dev | 6.4 | 7.0 | **7.4** | 6.7 |
| ops | 7.7 | 8.2 | 6.2 | 6.7 |
| mind | 5.0 | **8.7** | 6.0 | 8.6 |
| studio | 7.9 | **9.4** | 6.7 | 9.0 |
| critic | 6.2 | **9.1** | 8.2 | 7.2 |
| auditor | 6.6 | **8.4** | 7.5 | 7.0 |
| planner | 5.9 | 7.5 | 5.1 | 7.1 |

## Lectura honesta de minimax

**Fortalezas reales (medidas):**
1. **`main` es su mejor rol (8.9)** - gana el rol del CORE contra el motor actual (7.8).
   En A/D/E de main escribió los entregables más completos y con frenos correctos.
2. **Clase D (restricción dura): el mejor de los 4 (7.4).** Obedece límites y declara
   trade-offs mejor que nadie.
3. **Mayor cantidad de wins absolutos (17/40)** - cuando engancha, engancha alto
   (10.0 perfecto en `dev-D1` y `studio-D1`).
4. **No inventa.** En B y E de main/mind frenó y lo dijo antes que suponer.

**Debilidades reales (medidas):**
1. **Coste temporal: 35× el más rápido por celda** (4327s vs 124s en el cómputo
   agregado), mediana 77s vs 3-14s. Con 6 workers se siente menos, pero es un orden
   de magnitud.
2. **Espiral de thinking:** mediana 9.9k chars de razonamiento (glm 3.4k, gpt-oss 80,
   gemma4 0). `think` no se apaga por API - `false` es rechazado por el runner,
   `true`/`high` igual de always-on.
3. **Fallo de entrega en clase ops:** 4 celdas con 44-56k chars de thinking y 0 de
   entrega salieron en la primera pasada (`ops-A1/C1/D1`, `mind-A1/D1`, `dev-A1`,
   `planner-A1`). Reintento con num_predict×2 recuperó 6 de 7. **quedó 1 celda
   irrecuperable (`ops-D1`, 100k chars de thinking, 3 intentos consecutivos sin
   entrega)** - su modo de fallo sistemático bajo presión de planificación larga.
4. **`ops` es su peor rol (6.7)** - abajo de deepseek (8.2) y gpt-oss (7.7).

## Veredicto por rol

| Rol | Motor recomendado | Cambio | Por qué |
|---|---|---|---|
| **main (CORE)** | **minimax-m3.1-flash** | SI | 8.9 vs 7.8 del actual; mejor en D/E; freno cuando debía; único rol donde su coste temporal no es bloqueo (orquesta, no genera) |
| dev | gpt-oss:120b | no | gemma4 ganó por content (7.4) pero es el pre-filter; gpt-oss sigue siendo el único que entregó hook completo |
| ops | deepseek-v4.1-flash | no | minimax falló la celda de producción por thinking espiral; 6.7 vs 8.2 |
| mind | deepseek-v4.1-flash | no (empate técnico 8.7 vs 8.6) | minimax casi a la par pero con coste 20× |
| studio | gpt-oss / deepseek | no | minimax segundo (9.0 vs 9.4); sin ventaja que justifique el coste |
| critic | deepseek | no | deepseek 9.1 vs minimax 7.2 |
| auditor | deepseek | no | 8.4 vs 7.0 |
| planner | deepseek | no | minimax 7.1 vs 7.5, pero ops-D1 (su celda de planificación larga) fue el fallo sistemático |

**Candidato ganador único: `main` (el CORE).** Con 17/40 wins y su mejor rol exactamente
donde más importaba, es un buen motor de orquestación. Su coste por latencia no está en
la ruta crítica del CORE (el que espera es Gonzo, no un pipeline). Los roles de
generación (dev, critic, studio) quedan como están.

## Costo: consumo MEDIDO (el precio no se midio, y no importa)

**El precio no se pudo verificar:** `ollama.com/pricing` no expone tabla en HTML
estatico. Decision de Gonzo: "hasta el 22 a las 23.59 M3.1 Flash sera gratis... igual
nunca usamos el precio". Con el costo en cero, la objecion no aplica en esta ventana.

**Pero el CONSUMO si se puede medir, y estaba medido en los registros:** cada corrida
guarda `eval_count` (output tokens). Se verifico que `eval_count` **incluye el
reasonamiento**: con content+thinking la densidad da 4.3-4.5 chars/token (coherente
con ~4 chars/token); con content solo daria 1.31 chars/token, imposible. O sea: **el
thinking se factura como output**, y el `eval_count` ya lo cuenta.

**Y el input es identico para los 4 modelos** (mismo prompt verbatim), asi que todo el
delta de consumo es 100% output/thinking.

| Modelo | 40 celdas (out tokens) | 33 celdas limpias | coste del fallo (7 celdas) | latencia mediana |
|---|---|---|---|---|
| minimax-m3.1-flash | **220.818** | 110.558 | **110.260** | 77,0s |
| deepseek-v4.1-flash | 56.747 | 37.503 | 19.244 | 13,9s |
| gpt-oss:120b | 11.304 | 7.392 | 3.912 | 3,2s |
| gemma4 | 5.860 | 3.869 | 1.991 | 5,3s |

**Ratios medidos (minimax / deepseek):**
- output tokens, 40 celdas: **3,89x**
- output tokens, 33 celdas limpias (sin el sesgo del retry): **2,95x**
- latencia mediana: **5,5x** (35x contra el mas rapido por celda, gpt-oss)
- contra gpt-oss: **19,5x** en output tokens

**El dato que mas pesa no es el ratio: es donde se va el gasto.** Las 7 celdas donde
minimax fallo por espiral de thinking consumieron **110.260 output tokens**, es decir
**294% de todo lo que consumio deepseek en 33 celdas limpias**. El consumo real de
minimax esta dominado por el modo de fallo, no por su razonamiento normal.

**Correccion de una version anterior de este informe:** la primera redaccion de esta
seccion decia "minimax piensa 3x mas... el costo por turn podria ser mayor", una
inferencia sobre caracteres de thinking **sin medir el consumo**, con un pendiente
para confirmar el precio. El consumo estaba disponible en los registros y no se uso.
Ahora la seccion dice lo medido, y la inferencia quedo reemplazada por el numero.

**Lo que NO se puede afirmar:** el precio por 1M tokens de minimax frente a deepseek.
No hay fuente primaria consultada. (El unico "20x" que existe en el workspace es de
otra sesion y otro modelo: `memory/2026-10-05.md`, nemotron-3-super vs deepseek en
input, $0.015 vs $0.30/M. No es minimax ni es de esta cata.)

## Pendientes con fecha

- **Cata de validacion en 2 semanas de uso real** del CORE con minimax (corte 2026-11-03).
- **Reevaluar el balance de consumo: RESUELTO 2026-10-24.** La gratuidad termino el
  2026-10-22, pero la unidad correcta no es el precio por token sino la **cuota de
  GPU de Ollama Cloud** (plan legacy: barra de uso semanal con reset, no creditos).
  Medido sobre el panel: minimax 0,066 px de cuota por request contra 0,053 de
  deepseek (**1,25x**, el "20-30% superior" confirmado), pero **4 px de 820 = 0,5%
  de la cuota semanal** en absoluto, contra la calidad medida de 8,9 vs 7,8 en el rol
  `main`. **Se mantiene minimax.** Decision y datos: ADR-102, seccion "Revision
  2026-10-24".
- **K3 como juez:** cancelada por Gonzo (costo de recursos desmedido). Los 160 registros
  guardan `prompt`, `content`, `thinking` y `eval_count` separados por celda y modelo:
  reevaluarlos no requiere re-correr nada.

## Archivos

- `battery.py` - 40 prompts congelados
- `run-battery.py` - runner API con resume (`results/`)
- `judge-battery.py` + `judge/` - juicio (con las correcciones documentadas)
- `retry-empties.py` - recuperación de la espiral
- `report.py` - cómputo
- `README.md` - diseño
- `informe.md` - este documento