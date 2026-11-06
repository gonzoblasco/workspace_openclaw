# BRIEF - Kanam MIND: de investigadora escrita a investigadora ejecutable

**Fecha:** 2026-11-06
**Pregunta:** ¿qué skills, scripts y funciones le faltan a Kanam MIND para ser un rol más demandado dentro de Kanam OS?
**Encargado por:** Gonzo (gateway-owner), en la sesión `agent:kanam-mind:main`.
**Home del artefacto:** `agents/kanam-mind/reports/brief-capacidades-2026-11-06.md`
**Criterio de parada:** (a) el diagnóstico está atado a datos medidos en el filesystem y en las DBs del Gateway; (b) cada propuesta tiene un artefacto concreto y un criterio de listo verificable; (c) lo que no se puede saber queda como incógnita.

---

## 1. La pregunta, desagregada

[inf] No es "¿me faltan skills?" (tengo 10): es "¿por qué el CORE no me invoca, y qué capacidad mía no está construida para que valga la pena invocarla?".

[inf] Mi hipótesis de entrada era la del ROADMAP ("me falta la prueba: los tres gates son prosa"). El dato medido cambia el orden de prioridad: primero demanda, después prueba (ver §3).

---

## 2. Observación (lo medido, no lo recordado)

### 2.1 Uso real por agente

[obs] Tabla `skill_usage` de `~/.openclaw/state/openclaw.sqlite` (copia de solo lectura al 2026-11-06):

| Agente | Skills distintas usadas | Invocaciones | Última |
|---|---|---|---|
| `main` (CORE) | 118 | 375 | 2026-11-06 |
| `kanam-dev` | 6 | 13 | 2026-11-06 |
| `kanam-critic` | 2 | 9 | 2026-11-06 |
| `kanam-auditor` | 5 | 8 | 2026-11-06 |
| `kanam-ops` | 4 | 7 | 2026-11-06 |
| `kanam-planner` | 1 | 2 | - |
| `kanam-studio` | 1 | 1 | - |
| `kanam-mind` | **1** | **1** | **2026-10-22** |

[obs] Mi única entrada es `github`, 1 uso, 2026-10-22. Ninguna de mis 10 skills propias registra una sola invocación (`skill_usage`, fuente ya citada).

### 2.2 Cómo se me usó (la forma del pedido)

[obs] `session_nodes` de `~/.openclaw/agents/kanam-mind/agent/openclaw-agent.sqlite`: 6 sesiones, todas creadas por el CORE como **subagente** (`createdVia: spawn`, `spawnedBy: agent:main:*`):

| Fecha | Label | Modelo | Estado |
|---|---|---|---|
| 2026-10-21 12:50 | Tempo: neto real contractor AR | deepseek-v4.1-flash | done (7 min) |
| 2026-10-21 14:15 | Tempo: qué hace el producto y el rol Growth | deepseek-v4.1-flash | done (2 min) |
| 2026-10-22 19:07 | Escribir los 2 posts faltantes | gpt-oss:120b | done (6 min) |
| 2026-10-24 21:24 | Sudoku UI: tesis cálida (mind) | deepseek-v4.1-flash | **killed** (4 min) |

[obs] La sesión `agent:kanam-mind:main` **se creó recién hoy 2026-11-06 17:41**, con esta conversación. No hay sesión principal previa: al rol se lo usó **solo como caja de herramientas paralela**, nunca como interlocutor propio.

[inf] Eso explica los "13 días": no es que el rol se rompió, es que **no existe una superficie estable donde el CORE me encuentre**. El CORE me trató como una función (`spawn` con un prompt suelto), no como un servicio con contrato de entrada.

### 2.3 Qué se me pidió de verdad

[obs] Los labels de §2.2 muestran tres tipos de pedido: (i) **research de mercado/empresa** ("Tempo: neto real", "qué hace el producto y el rol Growth"), (ii) **redacción de contenido** ("los 2 posts faltantes"), (iii) **crítica de diseño/UI** ("Sudoku UI: tesis cálida").

[inf] El tipo (ii) es de STUDIO y el (iii) es de AUDITOR/DEV: el CORE no tenía (o no conocía) esa capacidad y la ruteó a mí por descarte. [unk] Cuántas veces el CORE decidió *no* invocarme por no conocer mi contrato.

### 2.4 Mi sustrato, re-verificado hoy (el ROADMAP del 2026-10-07 ya no describe la realidad)

[obs] `agents/kanam-mind/memory/` tiene dailies de octubre (108 KB) y el archivo `2026-10-07.md` de 0 bytes: la memoria de rol **no está vacía**, como decía el ROADMAP; está **parcialmente poblada y sin índice**.
[obs] `scripts/semantic-search.js` sigue apuntando a `agents/kanam-mind/memory/memory.db`, que no existe; la DB real está en `workspace/memory/memory.db` (151 dailies, 267 learnings).
[obs] La búsqueda **de verdad** del workspace es `scripts/memory-search.py` y funciona: devolvió 5 fragmentos con 61-69% de similitud para una consulta de prueba (corrida 2026-11-06 sobre `memory/memory.db`).
[obs] `reports/` tiene un artefacto ajeno (`sprint-9-validation.md`: valida skills Hermes). `templates/` tiene `context_handover.md`. Cero briefs propios archivados.
[obs] `scripts/extract_pdfs.py` existe y es la única herramienta de 83 líneas con propósito acotado; no tiene test.
[obs] **Cero tests** en todo el árbol (`find agents/kanam-mind -name '*.test.*'` vacío).

### 2.5 Los tres gates son prosa (confirmado)

[obs] `research-brief-protocol` (97 líneas), `source-verification-gate` (62) y `evidence-chain-audit` (63) son SKILL.md sin script. `knowledge-management` (414 líneas) tiene `scripts/` pero sin tests (dato del ROADMAP 2026-10-07, re-verificado: los directorios siguen igual).

### 2.6 Lo que el sistema ya me da y no uso

[obs] `openclaw.json`: `browser` plugin `enabled: true`; `memory-wiki` `enabled: true`; `web.search` y `web.fetch` en el perfil global de tools; MCP `kanam-fixer` habilitado; 20 modelos en Ollama, incluidos `qwen3-embedding:0.6b` (embeddings) y `gpt-oss:120b-cloud`.
[obs] Ninguno de los 4 cron jobs con sesión aislada ("Memory Dreaming Promotion", "Moltbook Weekly Digest") está asignado a `kanam-mind`; los agentes con cron propio son `main`, `kanam-ops` y `kanam-planner`.

[inf] Mi problema no fue capacidad ausente: fue **capacidad invisible**. Tenía las tools; no tenía una forma de que el CORE supiera cuándo pedirme algo ni de demostrar que lo entregué verificado.

---

## 3. Conclusión

[inf] El cuello de botella es de **demanda y de prueba**, en ese orden:

1. **No hay contrato de invocación.** El CORE no tiene una regla que diga "esto es de MIND". Sin eso, el uso depende de que Gonzo se acuerde. (Evidencia: §2.2, §2.3.)
2. **No hay artefacto que pruebe el método.** Un brief y un veredicto reproducibles valen más que diez SKILL.md nuevos. (Evidencia: §2.5.)
3. **La memoria del rol está desordenada, no ausente.** Recuperar por significado es posible hoy con `memory-search.py`; lo que falta es ingerir mi propio material con citas.

[inf] Corolario: agregar una skill de investigación más **no** sube la demanda (el ROADMAP ya lo había rechazado). Lo que la sube es cerrar el circuito: **invocable → ejecuta → entrega con veredicto → queda en journal → el siguiente pedido cita el anterior.**

---

## 4. Propuesta: qué construir (en orden de retorno)

### A. Ya construido en esta sesión (nace funcionando, no como promesa)

| Artefacto | Qué resuelve | Estado |
|---|---|---|
| `agents/kanam-mind/scripts/kb-audit.py` | gate ejecutable: links, citas `path#Lx-Ly`, etiquetas `[obs]`/`[inf]`/`[unk]`, fechas en datos volátiles | [obs] corre y da veredicto: `FAIL` sobre `agents/kanam-mind/reports/sprint-9-validation.md` (2 afirmaciones sin etiqueta) y `PASS` sobre un brief etiquetado de control |
| `agents/kanam-mind/scripts/kb-ingest.py` | material de estudio → secciones citables en `memory/knowledge.db` (FTS5, idempotente, `--replace`, redacta secretos) | [obs] ingirió 3 secciones de un capítulo de prueba con citas `archivo#L1-L2` |
| `agents/kanam-mind/scripts/kb-search.py` | consulta sin modelo, con **verificación de la cita** contra el disco | [obs] devolvió la sección correcta con `✓ ok`; `--stale` detecta fuente cambiada |
| `agents/kanam-mind/scripts/brief-journal.py` | journal durable de briefs con veredicto y fuentes | listo para su primera entrada real |
| `agents/kanam-mind/skills/evidence-gate-executable/SKILL.md` | hace descubribles y encadenados los 4 scripts | escrito |

[inf] Esto cierra los Hitos 5.1 y 5.2 del ROADMAP con artefacto, no con prosa: el "termómetro" existe y otro lo puede reproducir con el mismo comando.

### B. Lo que sube la demanda (requiere que Gonzo o CORE decida)

| # | Propuesta | Por qué sube la demanda | Criterio de listo |
|---|---|---|---|
| B1 | **Contrato de invocación en `AGENTS.md` del CORE**: una tabla "si el pedido es X → invocar `kanam-mind` con el template Y". X = research de mercado/empresa/tecnología, verificación de una afirmación ajena, ingesta de material de estudio, auditoría de citas de un artefacto. | Sin ruteo escrito, el CORE no me llama aunque exista. | El CORE invoca MIND **sin que Gonzo lo pida** al menos 1 vez en una semana. |
| B2 | **`brief-request` template** (estilo `agents/kanam-mind/templates/context_handover.md`): pregunta, criterio de parada, frescura, homes, fuentes obligatorias, presupuesto. | El pedido llega con forma, no como prompt suelto: menos ida y vuelta, menos "killed". | Un brief sale **sin que el CORE tenga que aclarar el pedido**. |
| B3 | **Cron semanal `mind-study-digest`** (domingo): ingestar un capítulo del libro en curso, extraer 3 aprendizajes formalizados, actualizar `study-tracker`. | Le da a MIND una cadencia propia y produce material que el CORE puede citar. | 4 semanas corridas sin intervención; cada corrida deja ≥1 nota citada en `knowledge.db`. |
| B4 | **Arreglar `semantic-search.js` (handoff a DEV/OPS)**: apuntar a `workspace/memory/memory.db` y usar embeddings por API en vez de `ollama run` (lento, 30 s timeout). | Cierra la deuda del Hito 5.3 con criterio de aceptación de MIND. | `node agents/kanam-mind/scripts/semantic-search.js "<q>"` devuelve una nota propia con cita. |
| B5 | **Pipeline de "afirmación ajena"**: el CORE me pasa la afirmación de otro agente (Dev/Critic) y yo devuelvo veredicto con fuentes abiertas. | Convierte a MIND en gate de calidad que otros roles necesitan, no en servicio opcional. | Kanam DEV o Critic pide la verificación por su cuenta. |

### C. Lo que rechacé (para no inflar el rol)

- [inf] **Una 11ª skill de investigación.** No mueve un eje que hoy no tenga; el ROADMAP ya lo había rechazado y el dato de uso lo confirma.
- [inf] **Dashboard de cobertura de citas.** Métrica de vanidad; el journal ya da la serie mensual con `stats`.
- [inf] **Reescribir `study-tracker`.** Es un placeholder; la capacidad real es `technical-book-processor` + `kb-ingest`.
- [inf] **Absorber el arreglo de la DB / infra.** Es de DEV/OPS; yo defino criterio y verifico.

---

## 5. Riesgos e incógnitas

- [unk] Cuánto del no-uso es ruteo y cuánto es prioridad: no tengo el registro de pedidos que el CORE descartó. Se resuelve con B1 (si el ruteo existe y aun así no se usa, el problema es otro).
- [unk] El check de `labels` es heurístico y puede dar falsos positivos en tablas y bullets; se mitiga reformulando, no apagando el check.
- [obs] Las sesiones `deleted.*.zst` del 2026-11-06 17:41 no pudieron leerse (falta `zstandard` en el Python del sistema); el contenido de esas corridas no se usó en este brief.
- [obs] `openclaw.json` puede haber cambiado después de la lectura (2026-11-06 17:30); los datos de plugins son de ese snapshot.

---

## 6. Cierre

[obs] El gate corrió sobre este mismo brief: ver el veredicto en el journal (`brief-journal.py list`).
[inf] El salto que me falta no es de herramientas: es que el CORE tenga una línea escrita que diga cuándo me llama, y que mi entrega traiga un veredicto que él pueda reproducir.
