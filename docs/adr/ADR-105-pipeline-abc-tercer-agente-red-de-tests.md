# ADR-105: El pipeline pasa de A/B a A/B/C: el tercer agente es la red de tests

**Fecha:** 2026-10-25
**Estado:** Aceptado
**Decisores:** Gonzo (pregunta explicita: "dejamos el pipeline AB o pasamos al ABC que creo hizo exactamente lo que se requeria... y en el caso de tener que corregir algo se manda de nuevo a A y se repite o hace cada agente sus correcciones? creo mejor repetir") / Kanam
**Origen:** sesion 2026-10-25 - cata de `beam:cloud` (modelo nuevo de Reflection en Ollama Cloud) que derivo en un head-to-head de revisores y despues en un pipeline ABC de tres casos extremos.
**Relacionado:** ADR-077 (asimetría A/B), ADR-088 (enforcement del pacto), ADR-089 (pre-filtro), ADR-090 (modelos por rol), ADR-102 (minimax como motor del CORE)

---

## Contexto

El 2026-10-25 se cato `beam:cloud` (Reflection Beam 501B-A23B MoE, 1M de contexto) contra `minimax-m3.1-flash:cloud`, el motor del CORE (ADR-102). La cata derivo en dos preguntas que no tenian respuesta medida:

1. **Que revisor conviene en el slot B?** Se armo un bench con ground truth: A (`gpt-oss:120b-cloud`) escribia un modulo, se le sembraban 4 bugs (2 visibles en su propia suite, 2 ocultos) y tres revisores distintos los cazaban sobre el **mismo** codigo.
2. **Que hace la cadena completa cuando hay que corregir?** Se probo el pipeline ABC sobre tres casos extremos (cache con concurrencia, aritmetica de fechas, token bucket) y despues una variante de "rework": A recibe el reporte de hallazgos de B y corrige el.

Los tres experimentos estan en `bench/`, con su ground truth y su verificador, y son reproducibles.

### Lo que se midio

**Head-to-head de revisores** (mismo artefacto, 4 bugs sembrados, mismo prompt):

| Revisor B | Recall | Bugs reportados | Hallazgos extra | Duracion | Veredicto |
|---|---|---|---|---|---|
| `deepseek-v4.1-flash:cloud` | **4/4** | 9 | si | 52s | RECHAZADO |
| `minimax-m3.1-flash:cloud` | **4/4** | 10 | si | 180s | RECHAZADO |
| `beam:cloud` | **3/4** | 3 | **no** | 17s | **APROBADO (incorrecto)** |

`beam` no corrigio BUG-4 (sigue devolviendo la lista interna del cache, contaminable) y **se auto-aprobo con el defecto vivo**. Su salida fue ademas en ingles, contra el formato pedido. La conclusion de este bench es que **el slot B no es "el mas rapido" ni "el mas nuevo": es el que mas encuentra**, y que un revisor que se auto-aprueba sin mirar es peor que uno lento.

**Pipeline ABC sobre 3 casos extremos** (A escribe, B revisa y corrige, C escribe la red de tests):

| Caso | Tests de A | Bugs que cazaron B | Tests de C | Suite final |
|---|---|---|---|---|
| 1 `ResilientCache` (concurrencia, LRU, TTL) | 5 | 1 (MEDIO) | 28 | **49** |
| 2 `daterange` (bisiestos, fin de mes) | 15 | 2 (perf/higiene) | 37 | **69** |
| 3 `TokenBucket` (reloj, refill) | 7 (1 rojo) | **1 CRITICO** + arbitraje | 22 | **29** |

Todos los bugs que aparecieron eran de **invariantes que el spec declaraba explicitamente** (fin de mes, inclusividad, TTL, reloj inyectado). A no los veia porque no tenia a nadie que le dijera "aca hay un reloj que retrocede".

El caso 3 tiene el resultado mas importante: **A escribio un test que fallaba y no lo escondio** - reporto "el codigo esta bien, el test esta mal". B arbitro contra el spec ("tras 1.0s hay 1 token, no recarga total") y le dio la razon a A, dejando el test en rojo sin tocarlo. C confirmo el arbitraje y corrigio **solo ese assert**. La suite cerro verde sin que nadie "arreglara" el codigo para satisfacer un test erroneo. Ese comportamiento no existe en un pipeline de dos modelos.

**Rework (A corrige con el reporte de B)**:

| Metrica | Rework (A corrige) | B corrige directo |
|---|---|---|
| Recall final | 4/4 | 4/4 |
| Findings de B cubiertos | **7/9** | 9/9 |
| Iteraciones | 2 | 1 |
| Agentes involucrados | 3 (A, B, A) | 2 (A, B) |

A cubrio 7 de los 9 findings de B. El que se le escapo -`filter_by_date` descarta fechas que son objetos `datetime` reales o strings ISO con hora, porque `date.fromisoformat` falla y el `except` las ignora en silencio- **tampoco quedo como test en la red**, asi que se perdio dos veces: B lo reporto pero no lo testeo, y A no lo vio. Verificado: la suite completa da `OK` con ese bug vivo.

**Costo en requests** (medido, porque en Ollama Cloud la unidad de costo son requests, no dollars):

- El rate limit de 429 es **compartido por cuenta, no por modelo**: saturar `beam` hace fallar tambien a `minimax` (28/40) y a `deepseek` (27/40). Cambiar de modelo no abre presupuesto.
- Secuencial: 30/30 OK. Concurrencia 2 y 4: 100% OK. Concurrencia 6: 100%. **Concurrencia 20: 429 en ~70% de las requests.**
- Throughput @par=6: beam 2.27, minimax 1.73, deepseek 2.34 req/s.
- req/min con requests triviales y bucket limpio: beam 27, minimax 25, gpt-oss 16.
- Como pre-filtro, `beam` **no ahorra ni un request** respecto de `gemma4` (1 request por tarea en ambos) y gasta 478 tokens de eval contra 18: 26x mas, con la misma accuracy (6/6). Como triage no sirve.

---

## Decision

**El pipeline pasa de A/B a A/B/C.** El tercer rol es la **red de tests de regresion**, y el rework vuelve a A.

```
pipeline_abc -> gpt-oss:120b-cloud / deepseek-v4.1-flash:cloud / minimax-m3.1-flash:cloud
                 ^ A (escribe)          ^ B (revisa y corrige)        ^ C (red de tests)
```

### 1. Que hace cada rol

- **A (escribe):** implementa la unidad desde el spec. No decide el modelo: lo decide el CORE.
- **B (revisa y corrige):** revision adversarial. Busca defects reales, escribe la evidencia que los demuestra (un test o un script que falla) y corrige con cambios quirurgicos. **No relaja asserts.**
- **C (red de tests):** escribe los tests que faltan para que el invariante no se rompa mas. Valida sus propios tests **por mutacion**: aplica una mutacion concreta del codigo, muestra que su test falla, y que vuelve a pasar al revertir.

### 2. El rework vuelve a A, con una condicion

Cuando B reporta un defecto, **A corrige** (no B). El rework se midio y da el mismo recall (4/4) con +50% de requests.

**La condicion:** todo finding de B tiene que convertirse en un test de C. Es la unica forma de que el hallazgo no se pierda dos veces, que es exactamente lo que se midio: el finding que A no cubrio en el rework tampoco estaba testteado, asi que sobrevivio a la suite completa.

Es decir: **A corrige el codigo, C testea el defecto.** Si B reporto un bug y nadie lo testea, ese bug vuelve.

### 3. C no reemplaza a B, y el pre-filtro no autoriza solo

C escribe tests sobre codigo ya revisado por B. **No es un revisor**: su alcance es la red de regresion, no el juicio sobre el diseno. La asimetria del pacto se mantiene: A != B, B != C, A != C. Pedir "otro ojo" con el mismo modelo no es un segundo ojo (ADR-077).

El pre-filtro barato (`gemma4:cloud`, ADR-089) corre antes del gate B y **NO autoriza solo**: lo que toca logica o semantica pasa SIEMPRE por B. Con el ABC, la cadena completa es pre-filtro -> A -> B -> (A corrige) -> C.

### 4. Enforcement

El pacto ABC tiene el mismo tratamiento mecanico que el A/B (ADR-088): `scripts/check-pipeline-enforcement.py` verifica que la ruta `pipeline_abc` declare los tres modelos, que las fuentes sean consistentes entre si, que los tres sean **distintos entre si**, y que coincidan con el canon. Los tests del gate **siembran cada defecto** en arboles falsos y exigen que el check lo distinga de un arbol limpio.

La ruta `pipeline_ab` **se conserva**: el ABC agrega un rol, no reemplaza el pacto. Para trabajo donde la red de regresion no aporta (cambios mecanicos, docs, scripts de un solo uso), A/B alcanza.

### 5. Donde queda `beam:cloud`

**No entra al pipeline.** Los tres datos lo descartan:

- Como revisor B: recall 3/4, cero hallazgos extra, y se auto-aprobo con un defecto vivo. Es la velocidad de no mirar.
- Como pre-filtro: 1 request por tarea, igual que `gemma4`, pero 26x mas tokens de eval. No aporta.
- Como modelo de contexto largo: **si aporta**. Clavo el needle a 233k tokens donde `minimax` fallo con HTTP 500 a 140k y se comio un guion a 225k. Y usa 3.1x menos tokens de razonamiento que `minimax` en la misma tarea (169 vs 524).

Su lugar es donde el cuello de botella real es **tokens de razonamiento y contexto**, no requests: revision de artefactos grandes, analisis de codebase, contexto de 1M. Es un modelo de tarea, no un rol del pipeline.

### 6. El limite de requests es compartido y es un presupuesto

El 429 de Ollama Cloud es **por cuenta**. Un pipeline de tres agentes multiplica las requests por unidad de trabajo (el rework agrega un 50%). Con concurrencia alta (20 en vuelo) el limite castiga fuerte. La concurrencia efectiva del pipeline tiene que quedar en el rango 2-6, donde no hubo un solo 429.

---

## Consecuencias

- **El covenant de calidad sube.** La red de C es lo que convierte "el bug no lo vio nadie" en "el bug no puede volver". Sin C, el rework de A pierde findings: se midio 7/9.
- **Cuesta mas requests.** El ABC son 3 agentes y el rework agrega un cuarto pase. Es el precio de la red, y hay que pagarlo con concurrencia baja (2-6), no alta.
- **El arbitraje de tests en conflicto es parte del pipeline.** Un test que falla puede estar mal el test, no el codigo. B arbitra contra el spec; C confirma; solo despues se toca el assert. En el caso 3 ese ciclo evito que se "arreglara" un codigo correcto.
- **La asimetria se verifican con tres modelos distintos.** El gate comprueba A != B, B != C y A != C.
- **El bench queda en el repo** (`bench/`) con ground truth, seeder y verificador, para que estas mediciones se puedan repetir.

## Artefactos

- `bench/` - el bench head-to-head de revisores, el pipeline ABC de 3 casos y el caso de rework, con `GROUND_TRUTH.md`, `seed_bugs.py` y `verify_recall.py`.
- `scripts/check-pipeline-enforcement.py` - el gate, extendido al pacto ABC.
- `scripts/model-router.sh` - ruta `pipeline_abc`.
- `scripts/managed-blocks.py` - setting `model_pipeline_c` y bloque `pipeline-abc` en AGENTS.md.
