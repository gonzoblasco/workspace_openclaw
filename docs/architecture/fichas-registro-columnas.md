# Estudio: el registro de fichas (`sessions_relacional`)

**Fecha:** 2026-09-22
**Estado:** propuesta, sin implementar
**Origen:** pedido de Gonzo - "columnas reales basadas en un registro de las fichas, estudiar como quedaria"
**Relacionado:** ADR-058 (taxonomia), ADR-059 (contenido descompuesto)

---

## El problema, en una linea

Las fichas se llaman "registros" pero **la mitad de sus columnas estan muertas**. El
schema tiene 11 columnas y solo **6 tienen datos reales**.

## 1. Estado actual medido (51 fichas)

| Columna | Dato real | Que contiene | Veredicto |
|---|---|---|---|
| `id` | 51/51 | id | **queda** |
| `date` | 51/51 | fecha | **queda** |
| `title` | 51/51 | fecha (48 de 51 son solo la fecha) | **queda**, pero es debil |
| `summary` | 51/51 | resumen (22 con boilerplate del harness) | **queda** |
| `content_bare` | 51/51 | el markdown | **queda** |
| `created_at` | 51/51 | timestamp | **queda** |
| `model_used` | **1/51** | 50 dicen `'unknown'` (el DEFAULT) | default, no dato |
| `thinking_level` | **1/51** | 50 dicen `'high'` (el DEFAULT) | default, no dato |
| `complexity_score` | **1/51** | 50 ceros, uno con T17 | casi muerta |
| `tags` | **3/51** | strings con coma, no JSON | casi muerta |
| `session_duration` | **0/51** | 51 ceros | **MUERTA** |

**La distincion que importa:** `model_used` y `thinking_level` parecen llenas al 100% en
un `COUNT(*)`, pero **50 de 51 filas tienen el valor por defecto**. Un `COUNT` con
`IS NOT NULL` las da por buenas; mirar los valores distintos revela que no hay dato. Cualquier
filtro por modelo hoy devuelve "unknown" 50 veces.

**`session_duration`: 0 de 51.** Es una columna que nunca se poblo. Es exactamente la
columna muerta que se limpio dos veces en ADR-058 (`agent_id`, `query_vector`).

## 2. El principio: capturar, no inferir

Un campo justifica ser columna si **el dato existe al momento de escribir**. Si solo se
puede adivinar despues mirando el texto, no es un campo: es una inferencia, y las
inferencias sobre prosa fabrican datos falsos (medido en ADR-059: de 5143 matches de
`owner/name`, la mayoria eran rutas de archivo).

Aplicado a las fichas:

| Fuente del dato | Confiable? | Puede ser columna? |
|---|---|---|
| El script que escribe **lo tiene en la mano** | si | **si** |
| Esta en un patron **regular** de cabecera | si | **si** |
| Solo se puede **adivinar** del texto libre | no | **no** |

## 3. Las columnas con evidencia

### 3.1 `project` - el dato que ya existe y se descarta

**Evidencia:** `scripts/project-closure.sh` **tiene el nombre del proyecto** en la variable
`$NAME`. Lo usa en el titulo y en el daily, y **lo tira**: nunca lo guarda como columna.

```
INSERT INTO sessions_relacional (date, title, tags, ...)   <- sin project
```

Es el caso mas limpio de "capturar": el dato esta, solo hay que escribirlo.

**Precedente que funciona:** `todos.project` tiene 50% de fill y 8 proyectos distintos.
Es util y se usa.

**Limite medido:** de las 51 fichas historicas, **28 no tienen proyecto identificable en el
texto**. Esas quedan en `NULL`. No se infieren: se aceptan vacias. El beneficio esta en las
23 que si lo tienen y en las futuras.

**Vocabulario:** hay **20 proyectos** en `projects/`. `project` debe validarse contra esa
lista, no ser texto libre (el error de `topics.category` en ADR-058).

### 3.2 `daily_id` - el link real que la FK espuria pretendia ser

**Evidencia:** 20 fichas corresponden a un documento diario de la misma fecha; 3 coinciden
por contenido exacto. **28 no tienen correspondencia.**

**Contexto:** en ADR-058 se elimino una FK `sessions_relacional.id -> daily_notes.id`
porque era **espuria**: de 47 vinculos que resolvian, **0 compartian fecha**. Los escritores
pasaban `id=None` y las dos secuencias coincidian por numeracion.

**Esa FK estaba mal, pero la relacion existe.** `daily_id` como columna explicita (nullable,
con FK real) modela el vinculo correcto: una ficha **puede** pertenecer a un documento diario.
Se llena cuando el escritor lo sabe (20 casos), queda NULL cuando no (28).

Diferencia clave: la FK espuria **afirmaba** que el id coincidia. `daily_id` **declara** a
que diario pertenece, y puede ser NULL sin mentir.

### 3.3 `session_key` / `session_id` - linkear a la sesion de OpenClaw

**Evidencia:** ya se extrajeron en `daily_notes` (65 de 114, 57%) porque estan en los dumps
del harness con **100% de parseabilidad**. `session_key` tiene 16 valores distintos
(`agent:main:main` en 43 casos).

**Para que sirve en una ficha:** hoy no hay forma de ir de una ficha a la sesion de OpenClaw
que la produjo. Con `session_key` se puede.

### 3.4 `model_used` / `thinking_level` - quedan, pero hay que decidir

La columna existe y esta vacia de hecho. Dos caminos:

1. **Poblarlas de verdad** capturando el dato al escribir (el harness lo sabe).
2. **Borrarlas** si se decide que el dato no vale la pena.

Dejarlas como estan es lo peor: parecen llenas y no lo estan. Si se pueblan, permiten
comparar modelos por ficha, que es la pregunta del pipeline A/B.

## 4. Lo que NO se agrega

| Candidato | Por que no |
|---|---|
| `repo` / `pr` / `commit` en fichas | Se pueden extraer del texto, pero con ruido (medido en ADR-059). Ya viven modelados en `contributions`, donde el dato es regular |
| `glosario` / `conceptos` | Los `- **X**: valor` del markdown son **apuntes de estudio**, no campos. Extraerlos convertiria un glosario en 20 campos falsos (ficha 54: 'Hub-and-spoke', 'Bulkhead pattern'...) |
| `duration` (poblar la muerta) | No hay de donde sacar el dato hoy. Si no se captura, sigue muerta |

## 5. Como quedaria el registro

```
sessions_relacional
  id                 INTEGER PK
  date               TEXT     NOT NULL     <- llena
  title              TEXT     NOT NULL     <- llena
  summary            TEXT                  <- llena
  content_bare       TEXT     NOT NULL     <- llena
  created_at         TEXT     NOT NULL     <- llena
  ------------------------------------------ columnas nuevas, nullable
  project            TEXT                  <- capturado por el escritor
  daily_id           INTEGER               <- FK real a daily_notes(id)
  session_key        TEXT                  <- de la cabecera del harness
  session_id         TEXT                  <- de la cabecera del harness
  ------------------------------------------ decisiones pendientes
  model_used         TEXT                  <- poblar o borrar (hoy: default)
  thinking_level     TEXT                  <- poblar o borrar (hoy: default)
  complexity_score   INTEGER               <- poblar o borrar (1 de 51)
  tags               TEXT                  <- poblar o borrar (3 de 51)
  session_duration   INTEGER               <- borrar (0 de 51)
```

**Ninguna columna nueva es `NOT NULL`.** Todas las fichas existentes siguen validas sin
tocar una fila: es puramente aditivo.

## 6. Costo

| Paso | Costo | Riesgo |
|---|---|---|
| `ALTER TABLE ADD COLUMN` x4 | trivial | ninguno (nullable) |
| Capturar `project` en los escritores | chico | bajo |
| Backfill de `project` (23 fichas) | chico | medio: revisar que no invente |
| Backfill de `daily_id` (23 fichas) | chico | bajo: la fecha es verificable |
| Borrar columnas muertas | requiere rebuild de tabla | medio (mismo patron que ADR-058) |

## 7. Hallazgo aparte: `contributions` tiene el mismo problema, peor

Al medir el registro de fichas aparecio que **`contributions`** -el mejor modelado de la DB-
tiene sus propias fugas:

| Campo | Doc del schema dice | Valores reales |
|---|---|---|
| `status` | 4 valores (`open\|merged\|closed\|waiting_review`) | **8** (`+ active, collab, comment, verified`) |
| `tier` | `1 \| 2 \| 3` | **7**, mezclando numeros con categorias (`external`, `collab`, `pr`) |
| `tipo` | (sin comentario) | `colab` (15) y `colaboracion` (1): **el mismo concepto, dos grafias** |

**`tier` mezcla dos ejes:** es a la vez una prioridad (1/2/3) y una categoria
(external/collab/pr). Son dos campos, no uno. Mismo error que `category` en ADR-058, y la
misma reparacion (separar los ejes).

No se toca en este estudio, pero queda registrado con evidencia.

---

## Resumen para decidir

1. **Columnas nuevas que se justifican (4):** `project`, `daily_id`, `session_key`,
   `session_id`. Todas nullable, todas aditivas, todas con el dato disponible al escribir.
2. **Columnas a decidir (4):** `model_used`, `thinking_level`, `complexity_score`, `tags`.
   Hoy parecen llenas y no lo estan. Se pueblan o se borran.
3. **Columna a borrar (1):** `session_duration`, 0 de 51.
4. **No se infiere nada del texto.** Los glosarios no son campos.
