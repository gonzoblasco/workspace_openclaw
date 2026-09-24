# STATUS: kanam-insight

**Versión:** 0.1.0
**Fase:** Pattern Radar + Debt Detector operativos

## Health

- 🟢 Scanner de `.knowledge/` funcionando (122 archivos, 24 proyectos, 768K chars)
- 🟢 Índice semántico propio: colección `insight_knowledge` con **1243 vectores**
- 🟢 Pattern Radar verificado: cruzó 8 proyectos en una consulta de a11y; sus afirmaciones se contrastaron contra los archivos fuente (no alucinó)
- 🟢 Stack confirmado y documentado en **ADR-063** (Python + LangChain, reusa el starter)
- 🟢 Búsqueda semántica con citas de fuente (`radar.py search`)
- 🟢 Debt Detector operativo (análisis estructural, sin vectores): 26 proyectos analizados
- 🟡 Deuda: sin tests, sin Handoff Synthesizer

## Bloqueos

- Ninguno.

## Próximos pasos

1. Tests de los caminos críticos (scanner, chunking, retrieval, detector).
2. Evaluar el Handoff Synthesizer.
3. README + repo en GitHub.

## Corrección de spec (2026-09-24)

El spec original (2026-08-30) declaraba TS + Bun + SQLite-vec "confirmado". Ese spec quedó anterior a `langchain-starter` (2026-09-22). Corregido a Python + LangChain; el razonamiento está en ADR-063.

---

## Sesión 2026-09-24 - arranque real (apuesta 1)

Se construyó la capacidad completa de punta a punta, con el stack reusado:

| Pieza | Archivo | Verificación |
|---|---|---|
| Scanner | `scripts/scan.py` | 122 archivos, 24 proyectos, 768.465 chars |
| Indexador | `scripts/index.py` | 1243 chunks vectorizados en `insight_knowledge` |
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
