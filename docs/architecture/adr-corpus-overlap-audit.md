# Auditoría de solapamiento del corpus de ADRs -> una única fuente de verdad

**Fecha:** 2026-10-12
**Estado:** descubrimiento registrado (análisis). Las reparaciones requieren autorización del owner.
**Owner:** Kanam CORE (gobierno del corpus)
**Base:** `docs/adr/` (98 ADRs), `scripts/check-adr-integrity.py`, `scripts/check-adr-supersede.py`, `AGENTS.md`, `MEMORY.md`.
**Origen:** pedido de Gonzo (2026-10-12): *"Analiza los ADR en su totalidad y busca cuáles hablan sobre lo mismo o similar, cuáles se pisan. Hay que priorizar una única fuente de verdad, arranquemos por ver cuáles contradicen esta regla y registrar el descubrimiento."*

---

## 1. Qué dice hoy el sistema (evidencia cruda)

```
$ python3 scripts/check-adr-integrity.py
OK: 98 ADRs, todos indexados, sin duplicados ni refs rotas.

$ python3 scripts/check-adr-supersede.py
OK: el grafo de supersede es consistente (todo superseded esta marcado en su estado).
```

**Los dos guardas dan verde, y eso es precisamente el problema.** Verifican *integridad de forma* (todo ADR indexado, todo superseded con su marca), no *unicidad de decisión*. Ninguno de los dos responde la pregunta del pedido: **¿cuántos ADRs toman la misma decisión, y cuál manda?**

La causa raíz, medida en el código de `check-adr-supersede.py`:

- El grafo se construye **solo desde el campo de header del ADR que reemplaza** (`**Supersede:**` / `**Revierte:**` / `**Reemplaza:**`), y solo si la relación es **total**.
- Una relación declarada **en prosa** (en `Relacionado`, en una "Actualizacion", o dentro del cuerpo del reemplazado) **no entra al grafo** y por lo tanto **no se verifica**.

Resultado: un ADR puede quedar pisado, seguir diciendo `Aceptado`, y los dos guardas no dicen nada. Esto no es hipotético: hay cuatro casos vivos (sección 4).

---

## 2. La regla de la única fuente de verdad

El corpus de ADRs es **doc-only**: no hay tabla `adr` en `memory.db`, el archivo *es* la fuente de verdad (`adr-collection-audit`, step 1). Por lo tanto "una única fuente de verdad" aplica con todo su peso:

1. **Un tema, una decisión vigente.** Si dos ADRs hablan del mismo tema, uno gobierna y el otro está `Superseded` (o el solapamiento es parcial y está acotado por escrito).
2. **La cabecera es el contrato.** El estado se lee primero; un ADR pisado que sigue diciendo `Aceptado` es una segunda ley en circulación (lo dice el propio docstring de `check-adr-supersede.py`).
3. **La relación se declara donde la construye el guard.** Si el reemplazo se declara solo en prosa, el guard es ciego.

---

## 3. Mapa de clusters (los que hablan de lo mismo)

| Tema | ADRs | N | ¿Fuente única hoy? |
|---|---|---|---|
| **Modelos / motor LLM del sistema** | 006, 040, 041, 045, 046, 049, 052, 053, 076, 077, 080, 087, 088, 089, 090 | **15** | ❌ **No.** Ley repartida en 077/087/088/089/090; 040/041/045/046/053 parcialmente pisados pero con header verde. |
| **Memoria / base de datos** | 038, 050, 054, 055, 057, 058, 059, 060, 061, 062, 064, 065 | 12 | ✅ Sí, encadenada (cada una construye sobre la anterior, sin contradicción). |
| **Multi-agente / orquestación** | 007, 043, 073, 074, 077, 081, 083, 086, 088, 093, 094 | 11 | 🟡 Parcial: 073/074 fundan; 083/088 son enforcement. 081 se autodeclara "Parcialmente refutado". |
| **Design System / UI** | 037, 047, 048, 095, 096, 097 | 6 | ✅ Complementarias (047 funda; 095 re-evalúa; 096/097 consumen). |
| **Guardas de gobernanza / formato** | 056, 066, 067, 071, 082, 084, 092 | 7 | 🟡 056/071/082 es una cadena de guion con supersede declarado; el resto son guardas distintas. |
| **Ubicación de proyectos** | 075 (superseded), 098 | 2 | ❌ **No en la práctica:** el bootstrap sigue citando la ley muerta (sección 4, S2). |
| **SoporteML** | 068, 091 | 2 | ⚠️ 091 declara a 068 "superado" en prosa; 068 sigue `Aceptado`. |
| **Skills (publicación)** | 079 | 1 | ✅ |

**El cluster de modelos concentra el 15% del corpus y toda la ambigüedad grave.** Es el que hay que cerrar primero.

---

## 4. Hallazgos: los que PISAN (ordenados por severidad)

### S1 (crítico) - Modelos: nueve ADRs para una decisión, y ninguno la posee entera

La cadena real es: `006 -> 040` (supersede OK) `-> 041` (cambia el default) `-> 045 -> 046 -> 053` (declara pisar secciones de 040), `->` y después **077, 087, 088, 089, 090** redefinen la asignación por rol y el thinking.

- **ADR-053** (titular del tema: "Modelos primario, auxiliar y alternativo") sigue con **`Estado: Aceptado`**, pero su propio cuerpo dice, en la Actualización 2026-10-05: *"La distribucion primario/auxiliar/alternativo de este ADR quedo **superseded** por la distribucion por-agente del 2026-10-05"*.
- **ADR-090** es la ley efectiva (política de thinking + asignación por rol, cata 2026-10-06), pero **no declara `Supersede:` a 053** - solo lo pone en `Relacionado` y adentro del cuerpo de 053.
- **El guard no lo ve** porque la relación vive en prosa, no en el header del reemplazante.
- **ADR-040** dice `Accepted` y gobierna "selección por tipo de tarea" con perfiles que ya no coinciden con la config; **ADR-041** idem ("motor del sistema") con updates sucesivos.
- **`AGENTS.md` resume la ley en un bloque `model-operativo`** que es la superficie que realmente leen CORE y subagentes. Ahí vive una **cuarta copia** de la verdad.

**Por qué es grave:** un agente que cita "el ADR de modelos" puede citar 040, 041, 053 o 090 y obtener cuatro leyes distintas, todas con header verde.

### S2 (crítico) - Ubicación de proyectos: dos leyes vivas en simultáneo

- **ADR-098** (vigente): los proyectos viven en `<workspace>/projects/`.
- **ADR-075** (marcado `Superseded por ADR-098` ✅) dice `~/projects/`.
- **Pero el bootstrap -lo que el CORE y todos sus subagentes leen SIEMPRE- sigue citando la ley muerta:**
  - `AGENTS.md:158-162` nombra *"ADR-075 (los proyectos viven en `~/projects`)"* y describe `~/projects/<slug>/` como ruta de trabajo y de `.knowledge/`.
  - `MEMORY.md:1` y `:65` citan `~/projects/<slug>/.knowledge/ (ADR-075)`.
  - `ADR-093:43` alinea `session-start.sh` contra `~/projects/<slug>/.knowledge/`.
  - `ADR-066`, `ADR-084`, `ADR-085`, `ADR-063` también citan `~/projects/`.

**Por qué es grave:** es la misma clase que el guard de supersede existe para evitar, pero ocurre **fuera** del corpus, donde ese guard no mira. ADR-067 (el corpus no se lee por grep de cuerpo) y ADR-078 (una cita no es un hecho) ya nombraron la disciplina; acá se incumple.

### S3 (alto) - Estados falsos: la cabecera miente aunque el guard diga "consistente"

| ADR | Header dice | La realidad dice | Declarado en |
|---|---|---|---|
| ADR-053 | `Aceptado` | pisado por 090 (2026-10-05) | prosa, cuerpo de 053 |
| ADR-068 | `Aceptado (encuadre)` | "superado" por 091 (2026-10-06) | prosa, `Relacionado` de 091 |
| ADR-040 | `Accepted` | secciones pisadas por 053 | header `Supersede:` de 053 (parcial, OK) pero el resto quedó viejo |
| ADR-041 | `Accepted` | default reemplazado 2 veces | notas en el cuerpo |

**Por qué es grave:** el guard da verde sobre estos cuatro. El patrón "reemplazo declarado en prosa" es exactamente su punto ciego.

### S4 (medio) - SoporteML: 068 vs 091

`ADR-068` (greenfield v1) sigue `Aceptado`; `ADR-091` lo declara "superado" y cierra v4. Un lector de 068 no ve la reversión. Mismo patrón que S3.

### S5 (raíz) - El guard de supersede es ciego a las relaciones en prosa

Los cuatro hallazgos anteriores comparten una causa: **el grafo de supersede solo lee el header del reemplazante**. Cualquier reemplazo declarado en prosa (o dentro del cuerpo del pisado) es invisible. Cerrar S5 convierte a los guardas de "integridad de forma" en guardas de "unicidad de decisión".

---

## 5. Propuesta de consolidación (una fuente de verdad por tema)

Ordenada para que **cada paso cierre una clase de ambigüedad**, no un archivo suelto:

1. **S5 primero - ensanchar el guard.** Hacer que `check-adr-supersede.py` (o un tercero) también recoja:
   - la relación declarada en prosa (`Relacionado`, "Actualizacion ... supersede ..."),
   - y exija que todo ADR con una decisión reemplazada y vigente tenga su **fuente única** declarada.
   Sin esto, las reparaciones de S1-S4 van a recomenzar en el próximo ADR.
2. **S1 - nombrar la fuente única de modelos.** Un ADR (p. ej. "Asignación de modelos: fuente única") que **consolide 077/087/088/089/090 en una tabla**, y marque 040/041/045/046/053 como `Superseded` (o `Aceptado (histórico)`) en cabecera. El bloque `model-operativo` de `AGENTS.md` **se genera** desde ahí (bloques managed, ADR-055) - una sola fuente, tres vistas.
3. **S2 - corregir el bootstrap.** `AGENTS.md` y `MEMORY.md` deben citar ADR-098, no ADR-075; barrer `~/projects/` en `ADR-063/066/084/085/093`. Regla: la ruta se cita a su forma real (`<workspace>/projects/`).
4. **S3/S4 - enmendar cabeceras.** Marcar `Superseded por ADR-090` en 053 y `Superseded por ADR-091` en 068 (y donde corresponda en 040/041). Reparación puntual dentro de una generación (no barrido masivo).
5. **Cerrar con el exit check:** `check-adr-integrity.py` + `check-adr-supersede.py` en verde **y** el nuevo guard de unicidad en verde, con prueba en negativo.

**No** se renumeran ADRs, **no** se borra ninguno: la regla de la casa es preservar el registro de la decisión (ADR-067, `adr-collection-audit`).

---

## 6. Segundo eje - alcance: un ADR de proyecto vive con el proyecto (pedido 2026-10-12)

Regla del owner: *"aquellos relacionados con un proyecto en particular viva con el proyecto y no más en el scope global; los ADR no tienen por qué tener mención a proyectos específicos."*

**Esta regla ya está escrita, en dos lugares, y ninguno la verifica:**

- `docs/adr/README.md:110` - *"Cada ADR sigue el formato estándar ... pero **sin referencias al proyecto que lo originó**"*.
- `ADR-067 §3` - *"Un ADR de alcance de proyecto (stack, runtime, design tokens de esa app) pertenece al repo de esa app. El workspace aloja decisiones de alcance general. Mezclarlos es lo que produjo la confusión que originó este ADR."*

**Precedente aplicado una sola vez:** en 2026-09-22 el `ADR-048` global ("UI de kanam-lab, mantener Gradio") colisionaba con otro 048; se movió a `projects/kanam-lab/.knowledge/adr/0002-ui-framework-gradio.md` y se renumeró. La nota del archivo movido lo dice literalmente. Ese es el procedimiento a repetir.

Se parte en dos sub-reglas distintas, con tratamientos distintos:

### 6a. Sujeto de proyecto → el ADR se muda al proyecto (concreto, pocos casos)

Un ADR **cuyo sujeto es un proyecto** (gobierna la implementación de una app) no va en el corpus global.

**Estado de ejecución (2026-10-12):**

| ADR | Sujeto | Destino | Estado |
|---|---|---|---|
| **ADR-068** | SoporteML (greenfield v1) | `projects/soporteml/.knowledge/adr/` (ADR-0001) | ✅ **movido** |
| **ADR-091** | SoporteML (cierre v4) | `projects/soporteml/.knowledge/adr/` (ADR-0002) | ✅ **movido** |
| **ADR-054** | kanam-os (app local sobre memory.db) | `projects/kanam-os/.knowledge/adr/` | ⛔ **bloqueado**: `.knowledge/` de kanam-os esta git-ignored (`.git/info/exclude`) → mudarlo ahi lo deja SIN historial (peor que dejarlo en el corpus) |
| **ADR-094** | kanam-os (etapa 4) | `projects/kanam-os/.knowledge/adr/` | ⛔ **bloqueado** (misma razon) |
| **ADR-096** | kanam-os adopta el DS | mitad al proyecto, la mitad global (tema oscuro + `check-design-tokens.py`) se queda | ⛔ **bloqueado + entrelazado** |
| **ADR-063** | kanam-insight (Python/LangChain) | `projects/kanam-insight/.knowledge/adr/` | ⛔ **bloqueado**: el repo existe en GitHub (privado) pero el arbol local NO esta clonado |
| **ADR-050** | ambiguo: nombra kanam-os pero gobierna la memoria del workspace | decidir (¿la memoria del sistema es global?) | ⏸️ decidir |
| **ADR-079** | kanam-skills (repo archivado) | repo de skills (archivado) | ⏸️ decidir |

**Criterio de destino (aprendido acá, y es la regla que faltaba):** un ADR de proyecto solo puede mudarse a un arbol **versionado**. La verificación es `git -C projects/<slug> ls-files .knowledge | wc -l` y `git -C projects/<slug> check-ignore .knowledge`. En este workspace esa convención es **inconsistente**: `soporteml` y `kanam-lab` trackean `.knowledge/`; `kanam-os`, `kanam-spec` y `kanam-fixer` lo tienen en `.git/info/exclude` (ignorado). Mover un ADR global a un arbol ignorado viola la regla que lo motiva (ADR-084: la memoria del proyecto viaja con el proyecto, versionada). Los tres casos de kanam-os quedan **bloqueados hasta que su árbol versione `.knowledge/`**.

**Precedente aplicado:** en 2026-09-22 el `ADR-048` global colisionaba con otro 048; se movió a `projects/kanam-lab/.knowledge/adr/0002-ui-framework-gradio.md` y se renumeró. La mudanza de SoporteML siguió ese procedimiento: `git mv` de origen → renumerar en la serie del proyecto (0001/0002) → bajar la fila del índice global → repuntar los consumidores vivos (ADR-042, `NORTH.md`, `ROADMAP.md`, `LANGCHAIN_STRATEGY.md`, `MEMORY.md`).

**Huecos de numeración [68, 91]:** delibidos (un reemplazo declarado que se muda deja un hueco a propósito; documentado en ADR-067).

### 6b. Mención de proyecto como evidencia → masivo, y roza el método (ver tensión)

El propio README lo declara ("sin referencias al proyecto que lo originó"), y se viola a escala. Conteo de menciones de slug de proyecto **en el cuerpo** (excluyendo `Origen`, que es trazabilidad permitida, y las fuentes de libro/estudio: `remix-book`, `testing-react-library`, `fullstack-graphql-react`, `react-18-design-patterns` - esas NO son proyectos):

| ADR | Proyecto(s) citado(s) en el cuerpo | Veces |
|---|---|---|
| ADR-067 | soporteml | 13 |
| ADR-096 | kanam-os | 12 |
| ADR-066 | kanam-os | 11 |
| ADR-098 | a11y-fixer, kanam-tetris, kanam-spec, kanam-os | 5 |
| ADR-091 | soporteml | 7 |
| ADR-063 | kanam-insight (+ langchain-starter) | 15 |
| ADR-088 | ollama-visor | 3 |
| ADR-084 | kanam-lab, kanam-story-bible | 4 |
| ADR-083 | kanam-onwheels | 3 |
| ADR-095 | kanam-os | 5 |
| ADR-047/051 | kanam-lab | 4 / 2 |
| ADR-037/042 | soporteml | 10 / 2 |
| ... | (~70 archivos citan algún slug, la mayoría 1×) | |

### Tensión a decidir (antes de barrer 70 archivos)

**El método del corpus se apoya en la evidencia: el caso real que motivó la decisión.** ADR-067 (cita SoporteML como el caso testigo), ADR-078 (cita el auto-reporte falso), ADR-088 (cita `ollama-visor`, la sesión que motivó el enforcement) - todos *nombran el proyecto como prueba*. Borrar la mención borra la evidencia de por qué la regla nació.

Hay dos salidas, y hay que elegir una:

1. **Genericizar la evidencia:** reemplazar el nombre por la clase ("un proyecto del Crew", "una sesión de delegación"). Preserva la forma, pierde la trazabilidad.
2. **Acotar la regla:** distinguir **sujeto** (lo que 7a mueve) de **cita de evidencia**, y permitir la cita como se permite hoy el campo `Origen`. Es explícitamente lo que el README ya hace con `Origen` ("solo trazabilidad").

**Recomendación:** aplicar 7a (concreto, ~6-8 mudanzas) **ya**; y **7b solo bajo una de las dos salidas elegida por el owner**, porque un barrido de 70 archivos sin criterio falsifica evidencia. El costo de no decidirlo es un corpus que viola su propia regla declarada - pero un barrido a ciegas rompe más de lo que arregla.

### 6c. Raíz: no hay guard de alcance

Ningún script verifica que un ADR global no mencione un proyecto, ni que un ADR de sujeto-proyecto se haya mudado. Es el mismo agujero que S5 (relaciones de supersede solo en header), pero para el eje de alcance. Cerrar cualquiera de los dos sin el otro deja media regla sin enforcement.

---

## 7. Registro

- **Evidencia base:** salida cruda de los dos guardas (sección 1) + lectura de los 98 headers y 15 cuerpos del cluster de modelos + grep de `~/projects` en `AGENTS.md`/`MEMORY.md`/`docs/`.
- **Sin cambios al corpus:** este documento es el análisis; las reparaciones se ejecutan con autorización del owner.
- **Próximo paso propuesto:** abrir el ADR de "fuente única de modelos" y el ensanche del guard (pasos 1-2), que son los que desbloquean el resto.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
