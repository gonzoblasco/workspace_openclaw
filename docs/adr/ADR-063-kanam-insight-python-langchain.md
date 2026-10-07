# ADR-063: kanam-insight en Python sobre LangChain, no en TypeScript con Bun

> **Estado del sujeto: DESCONTINUADO (2026-10-06).** `kanam-insight` salió del roadmap: no existe como proyecto (no está en `~/projects/`) y Gonzo confirmó que no recuerda haberlo querido. Este ADR se conserva como **registro histórico** de la decisión de stack (Python+LangChain sobre el starter, en vez de TS+Bun), que reusa la capacidad de `langchain-starter`. Si algún día se retoma un motor de insights cross-`knowledge/`, esta es la decisión a revisar.

**Fecha:** 2026-09-24
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** arranque de la que era la apuesta 1 (registro `APUESTAS.md`, retirado 2026-10-06). El spec de kanam-insight (2026-08-30) declaraba TS + Bun, pero quedó anterior a la capacidad construida.
**Relacionado:** ADR-062 (vectores rechunk semántico), ADR-057 (embeddings BLOB), `LANGCHAIN_STRATEGY.md`

---

## Contexto

`kanam-insight` tenía su spec cerrado el **2026-08-30**, con el stack declarado dos veces como "confirmado" en `BRIEF.md` y `STATUS.md`:

| Declarado en el spec | Estado real al 2026-09-24 |
|---|---|
| TypeScript + Node CLI | El starter construido es Python |
| **Bun** (runtime + tests) | **No instalado en el Mac Mini** (verificado con `which bun`) |
| SQLite-vec o LanceDB | ChromaDB ya funcionando en `langchain-starter` |
| Ollama `glm-5.3-flash:cloud` | Disponible, sin conflicto |

La secuencia importa: el spec eligió TS + Bun **antes** de que existiera `langchain-starter` (construido el 2026-09-22). Y la razón por la que kanam-insight quedó como apuesta 1 fue, textualmente, que ya tenemos ingesta, chunking y retrieval funcionando y solo hay que apuntarlos a los `.knowledge/`.

Dato adicional: el stack de memoria del workspace **ya es Python con vectores funcionando**. El ADR-062 (2026-09-23) lo reparó - chunking por unidad semántica, 3133 vectores, búsqueda que devuelve resultados pertinentes. Construir kanam-insight en TypeScript duplicaría, en otro lenguaje, una capacidad que existe dos veces.

Precedente del propio workspace: la regla *"el precedente no es un motivo"* (2026-09-14). El spec no es un ADR, pero aun siéndolo, cita un stack cuya justificación hay que poder repetir hoy. No se puede.

---

## Decision

**kanam-insight se construye en Python, reusando `langchain-starter` (LangChain + ChromaDB + Ollama local).**

1. **Reuse del entorno:** se usa el `venv` del starter. No se duplica ~1 GB de dependencias ni se instala Bun.
2. **Colección propia:** `insight_knowledge` en Chroma, separada de `starter_knowledge`. Mezclar corpus degrada el retrieval; colecciones separadas mantienen la calidad y son el mismo mecanismo que después sirve para multi-tenant.
3. **Chunking por unidad semántica (ADR-062):** se corta por secciones de markdown, con el título al frente del chunk. No ventana ciega de caracteres.
4. **El spec se actualiza, no se ignora:** `BRIEF.md` y `STATUS.md` de kanam-insight se corrigen para reflejar el stack real. Un spec desactualizado que dice "confirmado" es peor que no tener spec.

---

## Consecuencias

### Positivas
- **Camino más corto:** el scanner, el índice y el radar se escribieron y verificaron el mismo día. En TS habría que reconstruir el indexado primero.
- **Un solo stack de IA en el ecosistema.** Menos superficie que mantener, menos divergencia.
- **Compatibilidad con la memoria existente:** Chroma, Ollama y los embeddings son los mismos que ya usa `memory.db`.
- **Verificado en vivo:** 122 archivos de 24 proyectos indexados en 1243 vectores; el radar cruzó 8 proyectos y sus afirmaciones se contrastaron contra los archivos fuente (no alucinó).

### Negativas
- **El spec queda reescrito.** Quien lea el histórico verá TS + Bun y este ADR explicando por qué cambió.
- **Se pierde la cercanía con el ecosistema TS/Node** donde viven la mayoría de los proyectos de producto (kanam-pulse, soporteml-v4, create-stack).
- **Dependencia del `venv` del starter:** si ese venv se recrea o se muda, kanam-insight lo sigue. Se documenta el acoplamiento; un `requirements.txt` propio queda como deuda.
- **~~Python 3.9 en el venv~~ CERRADO (2026-09-24):** el venv migro a **3.12.14**. Era deuda real: el 3.9 lo arrastraba el starter y varias libs modernas requieren 3.10+.

---

## Alternativas consideradas

1. **TypeScript + Bun, como decía el spec.** Requiere instalar Bun y reconstruir en TS el indexado y la búsqueda que ya existen en Python. Se descarta por costo sin beneficio técnico: el valor del radar está en el cruce, no en el lenguaje.
2. **Python standalone (Ollama + sqlite-vec directo).** Se alinea con el stack de vectores de `memory.db`, pero implica escribir más código propio y descartar el chunking ya probado de LangChain.
3. **Esperar y no construir el radar.** Descartada: es la apuesta 1 justamente porque valida la capacidad con riesgo cero.

---

## Implementacion

| Pieza | Path |
|---|---|
| Scanner de `.knowledge/` | `projects/kanam-insight/scripts/scan.py` |
| Indexador (chunking semántico) | `projects/kanam-insight/scripts/index.py` |
| Pattern Radar + búsqueda | `projects/kanam-insight/scripts/radar.py` |
| Índice local | `projects/kanam-insight/config/chroma_db/` (colección `insight_knowledge`) |

**Medición de la primera corrida:** 122 archivos, 24 proyectos, 768.465 caracteres, 1243 chunks. Radar sobre "validación de accesibilidad": 14 fragmentos de 8 proyectos, 5 patrones cross-project, 2 verificados contra archivo fuente.

## Referencias

- `docs/ROADMAP.md` §2.1 - apuestas de producto vivas (kanam-insight salió)
- ADR-062 - el chunking por unidad semántica que este proyecto reusa
- `projects/kanam-insight/.knowledge/BRIEF.md` - spec actualizado a este stack
