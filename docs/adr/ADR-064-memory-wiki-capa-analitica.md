# ADR-064: memory-wiki como capa analitica de memoria (modo isolated)

**Fecha:** 2026-09-24
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** workspace (verificacion de deuda del 2026-09-24; la skill `memory-wiki-workflow` lo asumia activo y el daily del 2026-09-22 lo registraba como pendiente de verificar)
**Relacionado:** ADR-050 (memoria de Kanam OS en SQLite), ADR-038 (learnings con mirror en DB), ADR-065 (DB-first vs doc-only)

---

## Contexto

El plugin `memory-wiki` (bundled, v2026.9.5) estaba **instalado pero deshabilitado** (`enabled: false`). Dos senales lo convertian en deuda:

1. La skill del workspace `memory-wiki-workflow` documenta un flujo completo que asume el plugin activo, con una config recomendada en su seccion Setup. Una skill que describe algo que no corre es deuda.
2. El daily del 2026-09-22 registraba explicitamente: "memory-wiki plugin: health status unknown. Need to verify if plugin is active and functional".

La skill `gateway-config` lo listaba como candidato legitimo a **activar** ("solo si una skill existente del workspace lo justifica, ej. `memory-wiki` con la skill `memory-wiki-workflow`"). El caso se cumplia: la skill existia.

**El problema que ataca:** durante la auditoria de ADRs del 2026-09-22 se encontraron contradicciones **a mano**, una por una (ADR-040 excluia `minimax-m2.7` y el config lo corria; ADR-041 declaraba GLM y corria otra cosa; `AGENTS.md` decia thinking MAX y estaba en high). Detectar esa clase de divergencia entre lo documentado y el estado real de forma manual no escala y depende de que alguien sospeche.

---

## Decision

**Se activa `memory-wiki` como capa analitica de memoria, en modo `isolated`.**

1. **Via de activacion:** `openclaw plugins enable memory-wiki` (no edicion manual del JSON, por la regla de `gateway-config`). Aplico sin restart (`restartRequired: false`).
2. **Config:** `vaultMode: isolated`, `search.backend: shared` + `corpus: all`, `render.createDashboards` + `createBacklinks`, `context.includeCompiledDigestPrompt: false`. Es la config que recomienda la skill `memory-wiki-workflow`.
3. **Alcance:** el vault vive en `~/.openclaw/wiki/main`, **fuera del workspace git**. No versiona.
4. **Fuente de verdad:** no cambia. `memory.db` sigue siendo la fuente de verdad de la memoria; `MEMORY.md` y el corpus de ADRs siguen siendo documentos. El wiki es la **capa analitica encima**, no un reemplazo.

### Diferencia con memory-core (para no confundirlos)

| | memory-core | memory-wiki |
|---|---|---|
| Que hace | `memory_search` sobre markdown | compila conocimiento durable aparte |
| Corpus | memoria activa (dailies, MEMORY.md, docs) | vault propio (sources, entities, claims) |
| Analisis | busqueda | detectores (contradicciones, stale, evidencia) |

Con `search.backend: shared` y `corpus: all`, `memory_search` y `wiki_search` **se conectan**: una sola pasada de recall cubre memoria durable + wiki compilado.

---

## Verificacion (2026-09-24)

Probado end-to-end, no solo habilitado:

- `wiki doctor` -> healthy. `wiki lint` -> 0 issues.
- `wiki search` -> devuelve hits de `MEMORY.md` y `todos.md` (el corpus compartido funciona).
- **Pipeline completo:** 3 fuentes ingestadas (`docs/adr/README.md`, `docs/learnings/README.md`, `docs/OSS-TRACKER.md`) + 1 entity con 4 claims y provenance.
- **Detectores ejercitados con una sonda deliberada** (claim sin evidencia, confianza 0.2, estado `contested`, fecha vieja). Resultado: `claim-health` reporto 1 sin evidencia + 1 contested, `low-confidence` 1 claim, `stale-pages` 1 pagina, y `lint` paso de 0 a 3 issues. Despues de borrar la sonda, los reports **se limpiaron solos**.

**Hallazgo de operacion (importante):** la ingesta sola **no** alimenta los reports. `provenance-coverage` lo dijo explicito: "No *structured claims* with provenance coverage yet". El analisis opera sobre la capa de **claims**, no sobre el texto crudo. O sea: el flujo real es `ingest` (evidencia) -> `entities con claims` (conocimiento) -> `compile/lint` (analisis). Sin el paso intermedio, el vault es evidencia inerte.

---

## Consecuencias

### Positivas
- Existe una capa que **detecta** contradicciones, claims sin evidencia y paginas stale, en vez de depender de que alguien las note a mano.
- Los ADR (doc-only, fuera del ciclo de la DB) tienen por fin un camino a consulta semantica via ingesta explicita.
- Un solo recall con `corpus: all` cubre memoria + wiki.

### Negativas / riesgos aceptados
- **El plugin pide acceso amplio:** los grants declarados incluyen `allowConversationAccess` y `allowPromptInjection`. Es bundled y de la casa, pero conviene saberlo: no es un plugin pasivo.
- **El vault arranca vacio.** Activar da la capacidad, no el contenido. Requiere ingesta deliberada.
- **`~/.openclaw/wiki/main` no esta en el workspace git** -> no tiene backup por versionado. El conocimiento compilado ahi no viaja entre maquinas. Solo el **material de origen** (que si es workspace) es recuperable.
- **Duplicacion potencial:** un dato puede vivir en `memory.db`, en un doc y ahora tambien en el vault. Se mitiga con la regla de que el wiki es capa analitica, nunca fuente de verdad.

### Politica de ingesta (decidida)
- **Arranca por `docs/`** (material tecnico). `memory/` y `docs/entrevistas/` contienen datos personales y de busqueda laboral: **no se ingestan** sin decision explicita de Gonzo.
- El plugin viene con `bridge` y `unsafe-local` **apagados** por defecto; esos son justamente los canales por los que podria chupar archivos privados. Se dejan asi.

---

## Alternativas consideradas

1. **Dejarlo deshabilitado.** Costo cero, pero deja la skill `memory-wiki-workflow` describiendo algo que no corre y la deuda abierta desde el 2026-09-22. Rechazada: la skill existente justifica activarlo segun el criterio de `gateway-config`.
2. **Modo `bridge`** (leer memoria activa directamente). Da mas alcance sin ingesta, pero acerca datos personales al vault sin control explicito. Rechazada: `isolated` con ingesta deliberada es el default conservador.
3. **No adoptar el plugin y seguir detectando contradicciones a mano.** Es el statu quo; la auditoria del 2026-09-22 demostro que a mano se encuentran, pero solo cuando alguien mira. Rechazada.
