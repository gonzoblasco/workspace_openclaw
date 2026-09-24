# STATUS: kanam-insight

**Versión:** 0.1.0
**Fase:** Pattern Radar operativo

## Health

- 🟢 Scanner de `.knowledge/` funcionando (122 archivos, 24 proyectos, 768K chars)
- 🟢 Índice semántico propio: colección `insight_knowledge` con **1243 vectores**
- 🟢 Pattern Radar verificado: cruzó 8 proyectos en una consulta de a11y; sus afirmaciones se contrastaron contra los archivos fuente (no alucinó)
- 🟢 Stack confirmado y documentado en **ADR-063** (Python + LangChain, reusa el starter)
- 🟢 Búsqueda semántica con citas de fuente (`radar.py search`)
- 🟡 Deuda: sin tests, sin Debt Detector, sin Handoff Synthesizer

## Bloqueos

- Ninguno.

## Próximos pasos

1. Debt Detector (estructural: ADRs obsoletos, decisiones-parche).
2. Tests de los caminos críticos (scanner, chunking, retrieval).
3. Evaluar el Handoff Synthesizer.
4. README + repo en GitHub.

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
