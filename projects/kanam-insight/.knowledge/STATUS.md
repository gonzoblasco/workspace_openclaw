# STATUS: kanam-insight

**Versión:** 0.1.0
**Fase:** los tres pilares operativos

## Health

- 🟢 Scanner funcionando: **3 fuentes** (proyectos + `docs/` + `skills/`), 445 archivos, 2.496.240 chars
- 🟢 Índice semántico propio: colección `insight_knowledge` con **4423 vectores** (eran 1243)
- 🟢 Fase 5.2 cerrada: el radar cruza las tres fuentes y trae cruces que antes eran imposibles
- 🟢 Pattern Radar verificado: cruzó 8 proyectos en una consulta de a11y; sus afirmaciones se contrastaron contra los archivos fuente (no alucinó)
- 🟢 Stack confirmado y documentado en **ADR-063** (Python + LangChain, reusa el starter)
- 🟢 Búsqueda semántica con citas de fuente (`radar.py search`)
- 🟢 Debt Detector operativo (análisis estructural, sin vectores): 26 proyectos analizados
- 🟢 **Handoff Synthesizer operativo**: 26 proyectos, 11 con desalineación detectada
- 🟡 Deuda: ingesta incremental (hoy el índice se rearma completo)

## Bloqueos

- Ninguno.

## Próximos pasos

1. ~~Evaluar el Handoff Synthesizer~~ ✅ hecho el 2026-09-24 (tercer pilar, 32 tests).
2. Deuda: ingesta incremental (hoy `index.py --reset` rearma todo).
3. Fase 6 del starter (multi-cliente) cuando haya decisión de negocio.
2. ~~Tests~~ ✅ hechos el 2026-09-24 (18 tests, verificados por mutación).
3. ~~README + repo en GitHub~~ ✅ hechos el 2026-09-24.

## Corrección de spec (2026-09-24)

El spec original (2026-08-30) declaraba TS + Bun + SQLite-vec "confirmado". Ese spec quedó anterior a `langchain-starter` (2026-09-22). Corregido a Python + LangChain; el razonamiento está en ADR-063.

---

## Sesión 2026-09-24 - arranque real (apuesta 1)

Se construyó la capacidad completa de punta a punta, con el stack reusado:

| Pieza | Archivo | Verificación |
|---|---|---|
| Scanner | `scripts/scan.py` | 445 archivos de 3 fuentes (proyectos + docs + skills) |
| Indexador | `scripts/index.py` | 4423 chunks en `insight_knowledge` |
| Pattern Radar | `scripts/radar.py` | Cruzó 8 proyectos; 5 patrones; 2 verificados a mano |

**Hallazgo del radar que vale registrar:** la consulta sobre accesibilidad destapó un patrón real que cruza proyectos - `kanam-fixer` y `kanam-story` coinciden, por vías distintas, en que **los tests verdes no alcanzan para validar el anuncio de un lector de pantalla**. Ese es exactamente el tipo de señal que se perdía en silos y que justifica el proyecto.

**Lección de método:** el spec declaraba un stack "confirmado" que había quedado obsoleto porque se escribió antes de construir `langchain-starter`. Los specs con fecha vencen; hay que revisarlos al arrancar, no confiar en que dicen lo correcto.

---

## Sesión 2026-09-24 (tarde) - Debt Detector operativo

`scripts/debt.py`: análisis estructural puro, sin vectores ni LLM. Reporte guardado en `docs/insights/YYYY-MM-DD.md`.

**Checks:** doc base ausente, doc fuera de `.knowledge/` (no versionado), STATUS viejo o sin fecha, pendientes acumulados, referencias rotas (distinguiendo rotas reales de no verificables local), docs de trabajo sin fecha.

**Hallazgo principal:** el ADR de Lucide fue **renumerado de 030 a 037** (commit `1769ecc1`) y dos docs de `soporteml-v4` siguen apuntando al número viejo. Ese es el tipo de deuda que nadie nota a mano.

**Trabajo de precisión (vale registrar):** la primera corrida reportó 27 hallazgos de severidad alta. Al verificar cada uno contra los archivos reales aparecieron **tres clases de falso positivo** que el detector producía:

1. Docs base en la raíz del proyecto contados como ausentes (existen, pero fuera de `.knowledge/`).
2. Refs con glob (`scripts/*.py`) tratadas como paths concretos.
3. Refs de proyectos sin repo clonado tratadas como rotas (pueden vivir en GitHub).

**Lección:** un detector de deuda que no se verifica a sí mismo produce deuda de credibilidad. La primera versión habría hecho reportar como problema cosas que estaban bien. Regla aplicada: **sin el repo del proyecto clonado no se puede afirmar que un doc falte**; solo la renumeración de ADR es señal inequívocamente nuestra, porque ese cambio ocurrió en el workspace.

---

## Sesión 2026-09-24 (cierre) - Fase 5.2: ingesta real

El scanner pasó de cubrir solo `.knowledge/` de proyectos a **3 fuentes**: proyectos + `docs/` + `skills/`. Índice: de 1243 a **4423 vectores**.

**Incidente (mismo día, más tarde):** el número que se declaró primero (2557) era de un indexado **abortado a la mitad**, no de una corrida completa. El bug: los IDs de chunk se generaban con el **nombre de archivo**, así que archivos homónimos en carpetas distintas (`docs/README.md` vs `docs/adr/README.md`) colisionaban. Chroma rechaza IDs repetidos en un lote y abortaba, dejando el índice a medias. Corregido: IDs por **ruta relativa** (única) + un guard que valida los IDs **antes** de tocar la colección. Reindexado completo y verificado: **4423 vectores**, búsqueda y radar OK.

**Un hallazgo que cambió el plan:** el criterio de éxito de 5.2 (*"preguntar algo de una sesión pasada y que responda con cita de fuente"*) **ya lo cumplía `memory.db`** (1144 secciones `daily` + 843 `session` vectorizadas). Verificado antes de indexar, para no duplicar. Lo que faltaba de verdad eran los docs estratégicos y las skills.

**Excluidos a propósito:** `docs/insights/` (reportes del propio detector: indexarlos es ruido auto-referencial y quedan vencidos) y `docs/archives/` (histórico).

**Bug encontrado por los tests:** el primer refactor de `scan_workspace()` usaba las constantes `DOCS_DIR`/`SKILLS_DIR` del módulo, así que ignoraba el `tmp_path` de los tests y leía los docs reales del workspace. Corregido derivando las rutas de `WORKSPACE` en cada llamada. **Los tests atraparon un bug que en producción habría pasado desapercibido.**

25 tests en verde (eran 18; los 4 nuevos cubren el escaneo multi-fuente y las exclusiones).

---

## Sesión 2026-09-24 (cierre) - Handoff Synthesizer: el tercer pilar

`scripts/handoff.py`: responde la pregunta que hoy se contestaba leyendo 4 archivos a mano - **"dónde está parado este proyecto y qué sigue?"** - y detecta la desalineación entre STATUS (qué pasó), HANDOFF (punto de retorno) y ROADMAP (qué falta).

Estructural, sin vectores ni LLM: comparar fechas, fases y marcadores no requiere semántica.

**Checks:** `SIN_PUNTO_DE_RETORNO` (sin HANDOFF ni ROADMAP: un tercero no puede retomar), `HITO_SIN_ESTADO` (hitos después de uno completado sin marcador), `FASE_FUERA_DE_ORDEN`, `ROADMAP_VIEJO` (roadmap más viejo que el estado).

**Resultado real:** 26 proyectos, **11 con desalineación**. Reporte en `docs/insights/handoff-2026-09-24.md`.

**Dos bugs que encontré al verificar mi propio código:**

1. **`ROADMAP_VIEJO` y `STATUS_VIEJO` eran código muerto.** `parse_date` no matcheaba `ACTUALIZADO` en mayúsculas, y varios docs lo escriben así. El check nunca disparaba. Corregido con `IGNORECASE`; ahora `create-stack` (66 días sin actualizar) aparece como debe.
2. **`HITO_SIN_ESTADO` estaba condicionado a que existiera STATUS/HANDOFF**, pero la consistencia interna del ROADMAP no depende de eso. Lo destapó un test, no la corrida real.

**Un test débil que la mutación destapó:** la aserción `not startswith("Nota")` pasaba igual con el valor mutado, porque el string venía con marcas (`**Nota Fase 0:**`). Reforzado con una aserción que sí discrimina.

32 tests en verde (eran 25).
