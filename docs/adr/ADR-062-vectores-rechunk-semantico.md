# ADR-062: Vectores re-cortados por unidad semantica, sin duplicar el texto

**Fecha:** 2026-09-23
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** pedido de Gonzo - "aplicar + vectorizar las secciones"
**Relacionado:** ADR-057 (BLOB float32), ADR-059 (contenido descompuesto), ADR-060 (FK activas), ADR-061 (campos interpretados)

---

## Contexto

Gonzo pregunto que son los vectores y para que sirven. Medido el estado real, la
respuesta tenia un problema: **la busqueda semantica funcionaba mal.**

### Diagnostico medido

Los 136 vectores de `session_vectors` se cortaban con una ventana **ciega de 1500
caracteres** sobre el texto crudo:

```python
raw_chunks = [content[j : j + CHUNK_SIZE] for j in range(0, len(content), CHUNK_SIZE)]
```

| Defecto | Medida |
|---|---|
| Chunks que cortaban a mitad de frase | **29%** (40 de 136) |
| Chunks que eran volcado del harness | **15%** (20 de 136) |
| Fichas cubiertas | 48 de 51 |
| Texto vectorizado | ~3 chunks por sesion, sobre textos de hasta 57.000 chars |

Ejemplo real del dano: un chunk empezaba con `'should be archived to...'` (perdio el
sujeto de la oracion anterior) y terminaba con `'it does'` (corta el verbo). El embedding
de ese fragmento representa mal su contenido, y la busqueda lo devuelve por parecido con
cosas que no tienen que ver.

### Prueba de que era grave

Consulta `"como mantener la confianza del usuario"` (el contenido literal de SOUL.md):

```
0.503  'Decisions Made - 2026-09-22: | Decision | ADR...'
0.494  'ity timeout, marca procesado. At-least-once...'
```

Nada sobre confianza. Con el corte corregido, la misma consulta devuelve fragmentos
pertinentes (0.73 para una consulta sobre TreeList a11y).

---

## Decision 1: cortar por unidad semantica, no por caracteres

Las fronteras ya existian: son las **unidades de nivel 2** de `session_entries`
(ADR-060, 521 unidades) y las **secciones** de ADR-059 (1987). No hay que adivinar donde
cortar.

```
antes:  136 vectores  (ventana ciega de 1500 chars)
ahora:  781 vectores de ficha + 2352 vectores de seccion
```

Cada chunk lleva **su titulo adelante**: `"## Configuracion OpenClaw VPS\n\n..."`. El
titulo da el contexto que el fragmento crudo perdia.

**Se saltan los boilerplate** (`Session End`, `Cierre`, `Self-reflection`,
`Conversation Summary`): 113 unidades que no son contenido de trabajo.

**Se incluyen las 18 fichas sin estructura.** La primera version del script las salteaba
porque no tienen unidades de tema. Medido antes de descartarlas: **17 de esas 18 tienen
contenido propio y 0 estan duplicadas** (26.000 chars de texto unico que se perdia).

---

## Decision 2: el texto NO se guarda, se reconstruye

La primera version guardaba `chunk_text` en `section_vectors` "para simplificar el
display". Medido: **el 75% de esos textos era identico al cuerpo de su seccion**, que ya
vive en el padre y se reconstruye con los offsets de `sections`.

| Concepto | Tamano |
|---|---|
| `chunk_text` duplicado | **2.16 MB** |
| DB con la duplicacion | 20.8 MB |
| DB sin ella | 19.1 MB |

**Por que importa mas de lo que parece: `memory.db` esta trackeada en git.** No es solo
espacio en disco: cada commit lleva la DB, asi que un dato duplicado **crece la historia
del repositorio para siempre**. Verificado en el historial: hay commits con la DB de
12.6 MB y otros de 4.4 MB segun lo que se hubiera migrado.

Es el mismo principio de ADR-059 y ADR-060: **offsets, no copias**.

Para mostrar los 5 resultados de una busqueda no hace falta almacenar 2352 textos: se
recuperan del offset de su seccion al vuelo.

### Correccion de una advertencia previa

En `vector-util.py` esta documentado:

> "LIMITACION CONOCIDA: no hay forma de distinguir un BLOB float32 de un byte-string
> arbitrario cuyo largo sea multiplo de 4 [...] garantizado por migrate-vectors.py"

Al medir aparecio que las **dos columnas de vectores mezclan formatos**: `learnings` usa
JSON (22 KB por vector, el formato viejo) y `session_vectors` usa BLOB (4096 bytes).
Medido: `learnings_enriquecido` no existe, `learnings.learning_vector` es JSON.
**No se corrige ahora** (es migracion de datos, no de esquema) pero queda registrado: la
mitigacion fue por script, no por garantia estructural.

---

## Decision 3: una sola fuente para el corte de texto

`rechunk-vectors.py` **genera** los chunks y `memory-search.py` los **muestra**
reconstruyendolos. Si cortan distinto aunque sea un caracter, el texto que ve el usuario
no es el que se vectorizo, y la busqueda miente en silencio sobre su propio contenido.

La primera version tenia `split_large` y `strip_harness_header` **duplicadas en los dos
scripts**. Ahora viven en `scripts/chunk-util.py`, y un test verifica que ninguno de los
dos las redefina:

```python
def test_no_duplicate_definitions_in_scripts():
    for path in ("scripts/rechunk-vectors.py", "scripts/memory-search.py"):
        assert "def split_large" not in src
```

Es el mismo error que ADR-061 (dos ejes en una columna) y `contributions.tier`. La
diferencia: esta vez lo detecte **antes** de que produjera datos malos, porque el test lo
prohibe.

---

## Verificacion

| Prueba | Resultado |
|---|---|
| Suite de tests | **156 pasan** (23 nuevos de `chunk-util`) |
| Vectores de ficha | 781 (eran 136) |
| Vectores de seccion | 2352 |
| Chunks que empiezan con volcado del harness | **0** |
| Chunks semanticos sin titulo al frente | **0** |
| `section_vectors` huerfanos | 0 |
| Dimensiones | 1024 en las dos tablas |
| `PRAGMA foreign_key_check` | 0 violaciones |
| DB | 20.8 MB -> **19.1 MB** |
| Busqueda real (`"TreeList a11y"`) | 0.733 con el fragmento correcto |

---

## Consecuencias

### Positivas
- **La busqueda devuelve resultados pertinentes.** Antes la consulta sobre "confianza"
  traia decision de releases; ahora trae fragmentos del tema.
- **Cobertura completa:** 51 fichas en vez de 48, y secciones por primera vez.
- **La DB encoge 1.7 MB** y deja de crecer por duplicacion en cada commit.
- **Un corte, una fuente.** Los dos scripts no pueden divergir.

### Negativas
- **2352 vectores nuevos pesan 9.6 MB.** La DB subio de 4.4 a 19.1 MB. Es el costo real
  de vectorizar las secciones; el ahorro fue no duplicar el texto.
- **La reconstruccion es mas lenta que leer una columna.** Para 5 resultados es
  despreciable, pero una busqueda masiva pagaria el costo.
- **`learnings` sigue en JSON** (22 KB por vector). Migrarlo es trabajo pendiente.
- **La busqueda corre en Python, no en SQL.** Con 3133 vectores tarda ~1-2 s; un
  `sqlite-vec` seria el paso natural, pero no se justifica todavia.

---

## Hallazgo: los vectores no son la herramienta principal de la memoria

Medido con pruebas concretas:

| Pregunta | Gana |
|---|---|
| "¿que sesiones tocan accesibilidad?" | **SQL** (`topic_sessions`, exacto y rapido) |
| "¿que TODOs estan abiertos?" | **SQL** (binario) |
| "¿donde se hablo de entrevistas?" | **vectores** (encuentra sinonimos) |
| "¿que dije sobre confianza?" | **vectores**, y recien ahora funciona |

El SQL estructurado sigue siendo la puerta principal; los vectores sirven para el caso
donde no se recuerda la palabra exacta. Queda pendiente estudiar como se enseña esa
distincion (Gonzo propuso una skill antes que un ADR).

---

## Referencias

- ADR-060: las unidades de nivel 2 que ahora son las fronteras de corte
- ADR-059: por que se guardan offsets y no copias
- `docs/architecture/fichas-registro-columnas.md`
