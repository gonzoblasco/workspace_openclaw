# ADR-061: Campos interpretados con revision, y un eje por columna

**Fecha:** 2026-09-23
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** pedido de Gonzo - "aplicar las propuestas aprobadas a las columnas (hoy solo se guardan) y revisar las primeras interpretaciones para calibrar el prompt del interprete"
**Relacionado:** ADR-059 (contenido descompuesto), ADR-060 (FK activas), `docs/architecture/fichas-registro-columnas.md`

---

## Contexto

ADR-060 dejo las fichas desaplanadas en 521 unidades (`session_entries`) y un
interprete que **propone** campos con un LLM. Faltaban dos cosas: **aplicar** lo aprobado, y
**calibrar** el prompt mirando interpretaciones reales.

La primera corrida produjo los datos para calibrar: 8 unidades de la ficha 54.

---

## Decision 1: el campo de actividad se llama `activity`, no `kind`

El primer lote expuso un defecto en mi propio diseno. `kind` terminaba con **dos ejes
distintos en una columna**:

```
400 tema        <- DETERMINISTA (sale del titulo, lo llena migrate-entries.py)
113 boilerplate <- DETERMINISTA
  5 trabajo     <- INTERPRETADO (lo propone el LLM)
  2 estudio     <- INTERPRETADO
  1 reflexion   <- INTERPRETADO
```

Las 8 unidades interpretadas **pisaron su clasificacion determinista**: 408 `tema` pasaron
a 400. Una query `WHERE kind='tema'` dejo de traerlas.

**Es exactamente el defecto documentado en `docs/architecture/fichas-registro-columnas.md`
para `contributions.tier`** (que mezcla numeros 1/2/3 con categorias external/collab/pr).
Documente el error y lo cometi dos horas despues, en una tabla nueva.

### Reparacion

| Columna | Eje | Fuente | Valores |
|---|---|---|---|
| `kind` | determinista | el titulo | `tema` \| `boilerplate` |
| `activity` | interpretado | LLM + revision | `trabajo` \| `estudio` \| `reflexion` \| `cierre` \| `otro` |

Se agrego `activity`, se movio el valor interpretado, y `kind` se **restauro** a `tema` en
esas 8 filas. Las 408 volvieron.

**Regla:** un eje por columna. Si dos valores de una columna responden preguntas distintas,
son dos columnas.

---

## Decision 2: la aplicacion separa destinos, y solo toca lo aprobado

`interpret-entries.py` gana el ciclo completo:

```
--dry-run     propone (no escribe)
--review      muestra lo pendiente
--approve     marca como aprobado      <- paso HUMANO
--reject      marca como rechazado     <- paso HUMANO
--apply-dry-run   simula la aplicacion
--apply       escribe lo aprobado
```

**Nada se aplica sin pasar por `--approve`.** El modelo propone, la persona decide, la DB
recibe solo lo aprobado. Es la diferencia entre interpretar y fabricar.

### Destinos (por que no todo va a la ficha)

| Campo | Destino | Razon |
|---|---|---|
| `project` | `sessions_relacional.project` | Es atributo del **dia**. Si dos unidades del mismo dia proponen proyectos distintos, se toma el primero y se avisa. |
| `topic` | `session_entries.topic` | Una unidad **no** define el resumen de la ficha entera (que tiene varias). |
| `activity` | `session_entries.activity` | Idem: es de la unidad. |
| `summary` | `session_entries.summary` | Idem. |

Una vez aplicada, la propuesta pasa a estado `applied`: deja de estar pendiente porque ya es
dato. La aplicacion es idempotente (una segunda corrida no encuentra aprobadas).

---

## Decision 3: el proyecto debe ser CENTRAL, no una mencion incidental

**Evidencia del primer lote (el falso positivo):** la unidad

```
'Sesion: libros OpenClaw para el puesto + sync workspace + post LinkedIn'
```

recibio `project=soporteml`. Al revisar el cuerpo, `soporteml` aparecia **una sola vez**:

```
"...resuelto preservando AMBOS lados (trabajo astryx + seccion SoporteML del remote)..."
```

Era **parte de resolver un conflicto de git**, no el tema de la unidad. La unidad trataba de
buscar libros, sincronizar el workspace y publicar en LinkedIn.

### Regla agregada

Un proyecto es central si:

1. aparece en el **titulo**, o
2. aparece **2 o mas veces** en el cuerpo.

Una mencion suelta suele ser de paso: una ruta, un remote, un ejemplo.

**Verificado contra el caso y su vecino:** acepta `'Sesion: soporteml-v4 - tags con color'`
(esta en el titulo) y rechaza el de los libros (1 mencion). Dos tests lo cubren.

Esto **no reemplaza** la validacion de vocabulario: el proyecto tambien debe existir en
`projects/`. Son dos filtros distintos.

---

## Correccion de una interpretacion (calibracion)

El lote completo, ya aplicado, para la ficha 54:

| # | kind | activity | topic |
|---|---|---|---|
| 0 | tema | trabajo | Corrección de estilos y taxonomía |
| 1 | tema | trabajo | reorganización de reglas operativas agentes |
| 2 | tema | trabajo | respuesta a review de accesibilidad |
| 3 | tema | trabajo | automatización de rituales de sesión |
| 5 | tema | trabajo | Fix de accesibilidad en astryx |
| 7 | tema | estudio | Investigación OpenClaw y sincronización git |
| 9 | tema | estudio | Arquitectura de OpenClaw AI Production |
| 10 | tema | reflexion | estrategia de personal branding LinkedIn |

**1 de 8 propuestas de proyecto fue un falso positivo (12%).** El resto de los campos
(`topic`, `activity`, `summary`) se leyeron correctos en la revision: describen la unidad sin
repetir el titulo, y las `activity` distinguen bien trabajo / estudio / reflexion.

**El prompt se mantiene; el filtro cambio.** El error no estaba en lo que el modelo leia
(detecto que SoporteML aparecia), sino en no exigir que fuera central. Se arregla en la
validacion, que es determinista y testeable, no en el prompt, que es probabilistico.

---

## Verificacion

| Prueba | Resultado |
|---|---|
| Suite de tests | **111 pasan** (44 del refactor de fichas) |
| `PRAGMA foreign_key_check` | 0 violaciones |
| `kind` determinista | 408 `tema` + 113 `boilerplate` **restaurados** |
| `activity` interpretado | 8 valores en su propia columna |
| Datos aplicados | 8 topics, 8 summaries, 8 activities, 1 project |
| Propuestas por estado | 25 `applied`, 1 `rejected` |
| `--apply` idempotente | segunda corrida aplica 0 |
| Em dash / rutas citadas | OK / 148 OK |

---

## Consecuencias

### Positivas
- **El ciclo completo funciona:** proponer, revisar, aprobar, aplicar, y nada mas.
- **Un falso positivo no contamina:** la propuesta rechazada queda en su tabla, la ficha
  intacta.
- **Los dos ejes son consultables por separado:** `WHERE kind='tema'` da 408 (unidades de
  trabajo real) y `WHERE activity='estudio'` da 2 (sesiones de estudio).
- **La calibracion queda medida, no estimada:** 1 falso positivo de 8.

### Negativas
- **El `project` es del dia, no de la unidad.** Si un dia tiene unidades de dos proyectos
  distintos, la columna guarda uno y avisa por consola. Modelar el proyecto **por unidad**
  seria otra columna en `session_entries`; no se hace hasta que exista un caso real.
- **La revision es manual.** A 8 unidades por corrida es viable; para 408 hace falta un
  criterio de auto-aprobacion, que no se define hasta ver mas falsos positivos.
- **`topic` y `summary` conviven con `kind` en la misma tabla**, y `kind` sigue siendo el
  eje determinista. La distincion esta documentada en el schema, pero es una trampa para
  quien no la lea.

---

## Referencias

- `docs/architecture/fichas-registro-columnas.md`: el estudio donde este defecto (dos ejes
  en una columna) estaba **ya documentado** para `contributions.tier`
- ADR-059: por que se guardan offsets y no copias del texto
