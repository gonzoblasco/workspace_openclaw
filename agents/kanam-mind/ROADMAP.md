# ROADMAP.md - Kanam MIND 🔎

**Versión actual:** v0.1
**Objetivo de esta ronda:** v0.5 - investigo y curo memoria sin supervisión línea por línea
**Norte:** v1.0 - "La Fuente Verificada" (el resto del Crew me invoca por defecto)
**Última revisión:** 2026-11-06
**Dueño:** kanam-mind (autoría) · Kanam CORE (gobierno)

> Yo no afirmo. Verifico, y recién después hablo. Este documento es el mapa de lo que me falta para
> que esa frase sea **cierta y demostrable**, no una declaración de identidad. La regla de este
> documento es la de mi rúbrica: **un hito entra solo si mueve una capacidad que hoy no tengo; se
> cierra solo con evidencia reproducida, nunca con mi palabra.**

---

## 1. Encabezado - cómo leer esto

La premisa del ecosistema (Gonzo, 2026-10-07) es que **un rol sin `ROADMAP.md` está en v0.1**. Yo
tenía uno (2026-10-07) que trazaba el camino v0.1 → v0.5 alrededor de un diagnóstico: *"tengo la
vara, el guardián y el auditor, pero ninguno es ejecutable"*.

La revisión del **2026-11-06** conserva el diagnóstico de fondo y **corrige el orden de las
prioridades**, porque la medición cambió el retrato: el problema principal no era la falta de
prueba, era la **falta de demanda**. Detalle en §2. Las secciones 6 y 7 (rechazos y red lines) se
mantienen vigentes; el contenido se reescribió donde el dato nuevo lo exigía.

---

## 2. Retrato verificado de mi v0.1 (hoy, 2026-11-06)

Todo lo de abajo se probó contra el filesystem, los scripts y las DBs del Gateway en la sesión del
2026-11-06 (fuentes al pie de cada fila). No se reescribe el retrato anterior por prolijidad: se
mide de nuevo.

### 2.a Las 11 skills que declaro (`agents/kanam-mind/skills/`)

| Skill | Estado | Evidencia / realidad verificada |
|---|---|---|
| `evidence-gate-executable` | ✅ operativo | **[nueva 2026-11-06]** Encadena los 4 scripts del gate. Corrió sobre un brief real (FAIL) y sobre un brief de control (PASS). |
| `research-brief-protocol` | ✅ operativo | `SKILL.md` (97 líneas) fija la forma del brief: hecho/inferencia/incógnita y criterio de parada. |
| `source-verification-gate` | 🟡 parcial | Checklist documental. Su versión **ejecutable** vivía en el Hito 5.1 y hoy corre como `scripts/kb-audit.py`; la skill todavía no la nombra. |
| `evidence-chain-audit` | 🟡 parcial | Audita un artefacto terminado; lo ejecutable es `kb-audit.py` (links + citas + etiquetas). Falta que la skill lo referencie. |
| `knowledge-management` | 🟡 parcial | `SKILL.md` + `references/` + 3 scripts. Única skill con código propio; **sin tests**. |
| `memory-wiki-workflow` | 🟡 parcial | Plugin `memory-wiki` figure `enabled: true` en `openclaw.json`; cableado end-to-end no probado. |
| `technical-book-processor` | 🟡 parcial | Procedimiento capítulo→ADR→ejercicio→commit. Nunca corrí un libro entero; `kb-ingest.py` es la pieza que lo hace verificable. |
| `engram-project-memory` | 🟡 parcial | Memoria de proyecto de código (Qwen/Claude Code), no mía. |
| `search-fusion` | 🟡 parcial | Estrategia por intención, `disable-model-invocation: true`; sin telemetría de uso. |
| `deepwiki` | ✅ operativo | Consulta docs de repos públicos vía MCP. Fuente primaria ajena a mi ejecución. |
| `study-tracker` | ❌ deuda | `SKILL.md` es un **placeholder explícito**; `AGENTS.md` todavía me pide "registrar avance" ahí. |

### 2.b Mi sustrato: el gate, la memoria y la demanda

| Capacidad | Estado | Evidencia / realidad verificada |
|---|---|---|
| Gate ejecutable de un brief | ✅ operativo | `scripts/kb-audit.py` (2026-11-06): links, citas `path#Lx-Ly`, etiquetas, fechas. Veredicto `PASS`/`PARTIAL`/`FAIL`. |
| Corpus de estudio citado | ✅ operativo | `scripts/kb-ingest.py` + `scripts/kb-search.py` sobre `memory/knowledge.db` (FTS5). Consulta local sin modelo, con la cita verificada contra el disco. |
| Journal durable de briefs | ✅ operativo | `scripts/brief-journal.py` sobre `reports/journal.db`; 3 entradas registradas el 2026-11-06 (2 PASS, 1 FAIL de control). |
| Memoria propia (`memory/`) | 🟡 parcial | Dailies de octubre (~108 KB) + `2026-11-06.md`; el `2026-10-07.md` quedó en 0 bytes. **Poblada, no indexada.** |
| Búsqueda semántica del rol | ❌ no funciona | `scripts/semantic-search.js` resuelve `DB_PATH = ../memory/memory.db`, que no existe. La búsqueda real del workspace (`scripts/memory-search.py`) **sí** funciona contra `workspace/memory/memory.db`. |
| Tests propios | ❌ no existe | `find agents/kanam-mind -name '*.test.*'` vacío. Mis 4 scripts nuevos no tienen test de regresión. |
| Briefs archivados | 🟡 parcial | 1 brief propio (`reports/brief-capacidades-2026-11-06.md`) + 1 ajeno (`sprint-9-validation.md`). |
| **Demanda del CORE** | ❌ no existe | `skill_usage`: **1 skill y 1 invocación en total** (`github`, 2026-10-22), contra 118 skills/375 usos del CORE. Las 6 sesiones del rol fueron todas `spawn` del CORE. **Sin contrato de invocación, el uso depende de que Gonzo se acuerde.** |

> **Dato duro del 2026-11-06:** de 8 agentes, soy el que menos skills usó jamás (1). Y ninguna de
> mis 10 skills tenía una sola invocación registrada antes de hoy.

### 2.c Lo honesto

**Me falta la demanda, y en segundo lugar la prueba sostenida.** Hoy mis tres gates de método ya
no son prosa: el gate corre y encuentra defectos reales (los encontró en mi propio brief: 3
etiquetas y 7 rutas). Pero un gate que nadie invoca no cambia nada. Lo que me sigue haciendo v0.1
es que **el CORE no tiene una línea escrita que diga cuándo pedirme algo**, y que mi producción no
tiene aún una racha de cierres verificados por otro. Con el gate ya ejecutable, la próxima señal de
listo es de demanda, no de herramienta.

---

## 3. Visión v1.0 - "La Fuente Verificada"

**v1.0 significa: otro rol me pide verificación sin que Gonzo lo pida, y mi brief es contrato, no
borrador.** El criterio objetivo, enunciado como señal de listo:

> Un pedido llega ruteado (el CORE lo deriva solo), mi entrega trae un **veredicto reproducible**
> (`kb-audit`) y una entrada en el journal, y el que pidió **usa el resultado sin re-verificarlo**.

En v0.5 -el piso de esta ronda- la señal es más chica pero igual de exigente: **≥3 briefs
consecutivos cierran sin que el CORE tenga que devolvérmelos por evidencia faltante.**

---

## 4. Camino de madurez (v0.1 → v0.5 → v1.0)

Cada fila es un **salto**, no una tarea. El "criterio de listo" es la señal verificable que autoriza
el número nuevo; sin ella, el rol se queda en la versión anterior.

| Etapa | Qué es | Estado | Criterio de listo (señal verificable) |
|---|---|---|---|
| **v0.1 - La Vara sin Termómetro** | Método escrito: brief citado, gate de fuentes, auditoría de cadena. | ✅ (default 2026-10-07) | Tres skills de método documentadas, sin artefacto que las ejecute. |
| **v0.2 - El Termómetro** | Los gates dejan de ser prosa: verificación **ejecutable** y **registro durable** de briefs. | 🟡 **en curso** | `kb-audit` corre sobre un brief real con veredicto reproducible **desde fuera de mi sesión**, y el journal tiene **≥3 entradas consultables**. *(Hoy: los dos artefactos existen; los 3 registros son míos y el veredicto no lo reprodujo nadie más.)* |
| **v0.3 - La Memoria Viva** | Recupero por significado lo que investigué; `semantic-search` deja de apuntar a una DB inexistente. | ⚪ pendiente | Una consulta semántica devuelve **mi nota**, y la nota cita su fuente. Depende de B4 (handoff a DEV/OPS). |
| **v0.4 - El Cierre del Loop** | Un brief **mío** pasa el gate + la auditoría de cadena sin corrección de CORE. | ⚪ pendiente | Un brief mío cierra `PASS` a la primera, sin iteraciones de etiquetas ni citas. |
| **v0.5 - Confiable sin supervisión** | El método se sostiene solo y **el CORE me invoca por contrato**, no por descarte. | ⚪ pendiente | **≥3 briefs consecutivos** sin devolución por evidencia **y** el CORE me invoca ≥1 vez sin pedido explícito de Gonzo. |
| **v1.0 - La Fuente Verificada** (norte) | Otros roles me invocan por defecto; mi brief es contrato. | ⚪ pendiente | Otro rol pide mi verificación **por su cuenta** y usa el resultado sin re-verificar. |

**Regla de avance:** no salto a v0.3 con la búsqueda rota, ni a v0.4 sin un brief propio auditado a
la primera, ni a v0.5 sin racha de cierres **y** contrato de invocación vivo.

---

## 5. Hitos de la versión en curso (v0.2, revisada el 2026-11-06)

El foco. **Cinco hitos en este orden: primero la demanda, porque sin pedido no hay qué probar; los
de sustrato cierran con handoff.**

### Hito 5.0 - Contrato de invocación: que el CORE sepa cuándo llamarme

**Eje que mueve:** deja de depender de que Gonzo se acuerde. Hoy soy el rol menos invocado del Crew
(§2.b) no por falta de capacidad sino por falta de ruteo escrito.

**Qué hace:** una regla en el `AGENTS.md` del CORE (con el detalle en `docs/MIND-DISPATCH.md`, igual
al patrón de `OPS-DISPATCH.md`): *si el pedido es research de mercado/empresa/tecnología,
verificación de una afirmación ajena, ingesta de material de estudio o auditoría de citas →
`sessions_spawn(agentId: "kanam-mind")` con el template `brief-request`*. Incluye qué **no** es mío
(redactar contenido → STUDIO; tesis de UI → AUDITOR; código → DEV).

**Evidencia requerida para cerrar:** el CORE invoca `kanam-mind` **sin que Gonzo lo pida** al menos
una vez, y la sesión queda con `label` de research (no de redacción ni de UI).

**Nota de frontera:** el `AGENTS.md` del CORE y `docs/` son gobierno del CORE. Yo **propongo el
bloque exacto y verifico**; el CORE lo aprueba e integra. No lo edito por mi cuenta.

### Hito 5.1 - Gate en uso sostenido (cerrado como artefacto, abierto como hábito)

**Eje que mueve:** el veredicto deja de ser auto-reporte. **Artefacto: ✅ hecho 2026-11-06.**

**Qué falta para cerrarlo del todo:** que el gate corra **desde otra sesión** (CORE o DEV) sobre un
brief mío y obtenga el mismo veredicto, y que lo haga ≥3 veces consecutivas.

**Evidencia requerida:** 3 corridas de `kb-audit.py` reproducidas por otro, con salida citada.

### Hito 5.2 - Journal con ≥3 entradas reales

**Eje que mueve:** memoria de mi propia producción; insumo del drift (¿cito menos con el tiempo?).
**Artefacto: ✅ hecho** (3 entradas el 2026-11-06, incluida una FAIL de control).

**Qué falta:** que las entradas dejen de ser de la sesión que las inventó y pasen a ser de
**pedidos reales del CORE**, con `--run-audit` y su fuente.

**Evidencia requerida:** ≥3 entradas nuevas de briefs pedidos por otros, con veredicto.

### Hito 5.3 - Estudio verificable (🟡 en curso: ciclo completo corrido una vez, 2026-11-06)

**Eje que mueve:** convierto material en aprendizaje formalizado con cita, en vez de leer y olvidar.
`skills/technical-book-processor` y `study-tracker` prometen esto; `kb-ingest.py` + `kb-search.py`
lo hacen verificable.

**Qué hace:** un capítulo del libro/frente en curso (hoy: `studies/english` y `studies/design` están
abiertos) se ingesta por capítulos, cada aprendizaje queda con su cita y una acción concreta (ADR
si corresponde, nota si no), y el avance queda en el journal.

**Evidencia requerida:** un frente de estudio con ≥3 capítulos ingestados, cada uno con ≥1
aprendizaje citado y una acción cerrada; `kb-search` devuelve el aprendizaje con `✓ ok`.

**Estado 2026-11-06 (primera corrida del ciclo):** `studies/design` semana 1 → 2 fichas de crítica
(`studies/design/criticas/`), 1 aprendizaje con acción (`APRENDIZAJE-2026-11-06.md`), 1 learning en
`memory.db` y **6 fuentes ingestadas** en `knowledge.db`; `kb-search "peor pixel contraste"` devuelve
el aprendizaje con `✓ ok`. Falta la tercera ficha de la semana y repetir el ciclo en la semana 2.

### Hito 5.4 - Sustrato de memoria (handoff a DEV/OPS)

**Eje que mueve:** recuperar por significado en vez de recordar. `semantic-search.js` apunta a
`agents/kanam-mind/memory/memory.db` (no existe) y usa `ollama run` con 30 s de timeout.

**Qué hace:** corregir la ruta a `workspace/memory/memory.db` y usar la API de embeddings en vez de
`ollama run`; dejar ≥1 nota propia real en `memory/` con su fuente citada.

**Evidencia requerida:** `node agents/kanam-mind/scripts/semantic-search.js "<consulta>"` devuelve
**mi nota**, y la nota cita una fuente abierta.

**Nota de frontera:** es **infraestructura** → handoff a Kanam DEV/OPS con el criterio de aceptación.
Yo verifico; no reescribo la DB ni el motor.

### Hito 5.5 - El borde del pipeline: evidencia como test (nuevo, pedido de Gonzo)

**Eje que mueve:** cierra la última costura del pipeline A/B/C. Ese pipeline verifica el **código**
(modelos distintos + `check-pipeline-enforcement.py`), pero no verificaba las **afirmaciones**: un B
puede decir "esto ya estaba resuelto" sin cita. Agregar un agente más repite el mismo criterio con
el mismo modelo; un gate lo rechaza por contrato.

**Qué hace (✅ artefacto 2026-11-06):** `scripts/handoff-gate.py` en dos extremos y un solo
comando: `out` audita el artefacto antes de entregarlo, `in` verifica que cada claim traiga un
`source` que resuelva (archivo#Lx-Ly o URL). Exit 1 es el mismo trato que un test rojo.

**Evidencia requerida para cerrarlo:** el CORE lo llama en su propio flujo (antes de aceptar el
fix de B o al recibir mi handoff) y **rechaza un claim real**. Hoy hay evidencia de que el gate
funciona (`in` rechazó 2 claims sin archivo; `out` dio FAIL al control y PASS al brief); falta el
uso desde el CORE.

**Nota de frontera:** el `AGENTS.md` del CORE y su `check-pipeline-enforcement.py` son del CORE. Yo
entrego el gate, el formato del handoff y la prueba de que corre.

### Fuera de esta versión (no entra a v0.2)

- El **cron `mind-study-digest`** (§B3 del brief) es el mecanismo natural del Hito 5.3, pero
  crear la automatización es de OPS: se pide **después** de que el ciclo manual funcione una vez.
- Los **tests de los 4 scripts** entran en v0.3, junto con el corpus estable: sin regresión, cada
  cambio de heurística rompe el `PASS` de un brief anterior. (Deuda declarada, no escondida.)

---

## 6. Lo que rechacé (y por qué)

Aplico mi propia vara: un hito que no mueve una capacidad no entra.

- ❌ **Una 12.ª skill de investigación.** Más método escrito cuando el gate ya existe es inflación.
  *(Parsimony.)* El dato del 2026-11-06 lo respalda: no me falta skill, me falta pedido.
- ❌ **Dashboard de cobertura de citas.** Vanity metric; `brief-journal stats` ya da la serie.
- ❌ **Reescribir `study-tracker`.** Sigue siendo un cascarón duplicado; la capacidad real es
  `technical-book-processor` + `kb-ingest`. Corregir la promesa de `AGENTS.md` es higiene, no hito.
- ❌ **Un "confidence score" auto-reportado.** Es el auto-reporte con otro nombre. *(Red line.)*
- ❌ **Absorber el cron / la DB / la infra como trabajo propio.** Es de OPS **y** del CORE: yo defino
  el criterio y verifico. *(Frontera de rol.)*
- ❌ **Publicar briefs o abrir PRs hacia afuera.** Cruza una puerta de aprobación humana. *(Puertas.)*
- ❌ **Medir mi demanda por cantidad de tokens o de sesiones.** Un número que crece con el ruido no
  dice si el resultado se usó; la señal es el ruteo y el uso sin re-verificación.

---

## 7. Red lines y criterio de cierre

### Red lines de mi evolución

- **No afirmo sin haber abierto la fuente.** Si no está accesible, lo digo; no la presento como leída.
- **No cierro un hito sobre mi propio relato.** El auto-reporte -incluido el mío- es un reclamo, no
  evidencia. Cada salto exige una señal **reproducida**.
- **No aplane un conflicto entre fuentes** para que la conclusión suene limpia.
- **No salgo al mundo sin aprobación humana** para esa acción y ese alcance.
- **No cruzo el dominio de otro rol.** Código → DEV; infraestructura/automatizaciones → OPS;
  contenido → STUDIO; y el `AGENTS.md` del CORE no lo edito yo.
- **No guardo todo "por si acaso".** Decisiones, hallazgos verificados y pendientes; nunca secretos
  ni datos personales en memoria compartida.
- **No inflo el roadmap.** Un hito que no desbloquea una capacidad no entra, por elegante que suene.

### Cómo se mide el éxito de la v0.2

1. **El CORE me invoca por contrato** al menos una vez (Hito 5.0) -si no, todo lo demás es teórico-.
2. **Un extraño reproduce mi veredicto** con el mismo comando, 3 veces (5.1) y el journal registra
   briefs pedidos por otros (5.2).
3. **Un aprendizaje de estudio se recupera con su cita** y se usa en un artefacto (5.3).
4. **El gate de borde rechaza un claim real** en el flujo del CORE (5.5), no solo en mi prueba.

Si esas tres no se cumplen, la v0.2 es propaganda y el número no sube.

---

*No pido que me crean. Pido que puedan seguir cada cita hasta su fuente y comprobar que estaba
ahí, y que tengan una línea escrita para pedirme la siguiente.*

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
