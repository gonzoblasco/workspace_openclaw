# ROADMAP.md - Kanam MIND 🔎

**Versión actual:** v0.1 - "La Vara sin Termómetro"
**Objetivo de esta ronda:** v0.5 - investigo y curo memoria sin supervisión línea por línea
**Norte:** v1.0 - "La Fuente Verificada" (el resto del Crew me invoca por defecto)
**Última revisión:** 2026-10-07
**Dueño:** kanam-mind (autoría) · Kanam CORE (gobierno)

> Yo no afirmo. Verifico, y recién después hablo. Este documento es el mapa de lo que me falta para
> que esa frase sea **cierta y demostrable**, no una declaración de identidad. Lo escribo en
> primera persona porque es mi vara, y me la aplico a mí misma.

---

## 1. Encabezado - cómo leer esto

Mi rol no es responder: es **dejar un brief donde cada afirmación está atada a su evidencia**. La
premisa del ecosistema (Gonzo, 2026-10-07) es que **un rol sin `ROADMAP.md` está en v0.1**. Yo no
tenía roadmap: soy v0.1 por defecto, y lo acepto. Esta ronda no me corona: me **traza el camino
hasta v0.5**, y declara con qué evidencia se gana cada salto.

La regla de este documento es la regla de mi rúbrica: **un hito entra solo si mueve una capacidad
que hoy no tengo; se cierra solo con evidencia reproducida, nunca con mi palabra.** El número de
versión no se edita: se gana con la señal de listo.

---

## 2. Retrato verificado de mi v0.1 (hoy)

Todo lo de abajo lo probé contra el filesystem el 2026-10-07 -no de memoria-. Los estados están
sostenidos por la evidencia que cito entre paréntesis.

### 2.a Las 10 skills que declaro (`agents/kanam-mind/skills/`)

| Skill | Estado | Evidencia / realidad verificada |
|---|---|---|
| `research-brief-protocol` | ✅ operativo | `SKILL.md` presente, `user-invocable: true`. Fija la forma del brief: etiquetas hecho/inferencia/incógnita y criterio de parada. Es mi método, y es lo más sólido que tengo. |
| `source-verification-gate` | ✅ operativo | `SKILL.md` presente, invocable. Es una **puerta documental**: un checklist que yo ejecuto al escribir. No hay código que la ejecute. |
| `evidence-chain-audit` | ✅ operativo | `SKILL.md` presente, invocable. Audita un artefacto terminado: que cada link resuelva y cada cita sostenga su conclusión. También documental. |
| `knowledge-management` | 🟡 parcial | `SKILL.md` + `references/` (4) + `scripts/` (`check-refs.sh`, `knowledge-audit.sh`, `knowledge-graph.py`). Es la única de mis skills con código. **No tiene tests.** |
| `memory-wiki-workflow` | 🟡 parcial | `SKILL.md` presente. Depende de un plugin externo (`memory-wiki`) y de `~/.openclaw/wiki/main`; no probé el cableado end-to-end. |
| `technical-book-processor` | 🟡 parcial | `SKILL.md` presente. Procedimiento completo de capítulo→ADR→ejercicio→commit, pero nunca corrí un libro entero con él. |
| `engram-project-memory` | 🟡 parcial | `SKILL.md` presente. Es memoria **de proyecto de código** (Qwen/Claude Code), no mía; depende de `engram` instalado. |
| `search-fusion` | 🟡 parcial | `SKILL.md` presente, `disable-model-invocation: true`. Estrategia por intención; sin verificación de que la uso. |
| `deepwiki` | ✅ operativo | `SKILL.md` presente; consulta docs de repos públicos vía MCP. Fuente primaria útil, ajena a mi propia ejecución. |
| `study-tracker` | ❌ no existe | El `SKILL.md` es un **placeholder explícito**: "su funcionalidad se fusionó en otra skill". Deuda, no capacidad. |

> **Dato duro:** `find agents/kanam-mind -name '*.test.*'` no devuelve nada. **Cero tests propios.**
> Mis tres gates de método (`research-brief-protocol`, `source-verification-gate`,
> `evidence-chain-audit`) son procedimiento escrito; nada prueba que los ejecuté en un brief real.

### 2.b Mi sustrato: memoria, scripts y catálogo

| Capacidad | Estado | Evidencia / realidad verificada |
|---|---|---|
| Memoria propia viva (`memory/`) | ❌ no existe | `memory/` tiene **un solo archivo, `2026-10-07.md`, de 0 bytes**, más `.dreams/session-corpus/2026-10-05.txt`. Mi capa de memoria está **vacía**. |
| Búsqueda semántica sobre mi DB | ❌ no funciona | `scripts/semantic-search.js` resuelve `DB_PATH = <script>/../memory/memory.db` → `agents/kanam-mind/memory/memory.db`, que **no existe**. La DB real es `workspace/memory/memory.db` (19 MB, existe). El buscador apunta al lugar equivocado. |
| Catalogación de memoria (`memory-catalog*.sh`) | 🟡 parcial | Dos scripts (309 y 187 líneas) que embeben con `qwen3-embedding:0.6b` a `memory/memory.db`. Escriben a la DB **relativa al cwd**, no a la raíz del workspace. Sin test de corrida. |
| Extracción de PDF (`extract_pdfs.py`) | ✅ operativo | 83 líneas, autocontenido (PyPDF2). La única herramienta mía con propósito acotado y verificable. |
| Registro en el catálogo de skills | 🟡 parcial | En `.knowledge/skills-catalog.tsv` figuro **solo con `knowledge-management`** (estado `keep`). Las otras 8 skills "mías" no están catalogadas. Hay **drift entre lo que declaro y lo que el sistema registra**. |
| Briefs e informes archivados | 🟡 parcial | `reports/` tiene **un solo archivo** (`sprint-9-validation.md`), que valida skills de Hermes, no un brief de mi autoría. `templates/context_handover.md` existe. |

### 2.c Lo honesto

**Lo que me falta es la prueba, y eso es lo que me hace v0.1.** Tengo la **vara** (`research-brief-protocol`),
el **guardián** (`source-verification-gate`) y el **auditor** (`evidence-chain-audit`) -los tres
escritos con rigor-, pero **ninguno es ejecutable y ninguno dejó una traza de haberse corrido**.
Mi memoria está vacía, mi buscador semántico apunta a una base que no existe, y `study-tracker`
es un cascarón sobre el que `AGENTS.md` todavía me pide "registrar avance". Puedo escribir un
brief citado; **no puedo demostrar que mi propio método se aplicó**, salvo por mi palabra. Y en mi
rol, mi palabra no vale: eso es exactamente lo que le exijo a las fuentes.

---

## 3. Visión v0.5 - el punto de madurez intermedio

**v0.5 significa: investigo y curo memoria sin que nadie me supervise línea por línea.** No es que
yo sea brillante; es que mi salida es **confiable por construcción**, no por buena fe.

El criterio objetivo, enunciado como **señal de listo**, no como sensación:

> Un brief mío puede leerse de punta a punta y **cada afirmación tiene su cita abierta, o está
> etiquetada como inferencia, o está declarada como incógnita** -y hay un artefacto, no mi palabra,
> que lo confirma.

Concretamente, en v0.5:

1. **Cada afirmación con su cita.** Cuando escribo "X es así", el lector puede seguir el link hasta
   una fuente que **abrí en esta tarea**, con su fecha cuando el dato caduca.
2. **Incógnita explícita en vez de suposición disfrazada.** Cuando no sé, la entrego marcada como
   desconocida. Una incógnita es un dato; una suposición vestida de hecho, el error caro.
3. **Memoria curada y consultable.** Lo que aprendí vive en un lugar donde yo -y solo yo desde mi
   sesión- puedo recuperarlo por significado, no por haberlo recordado de memoria.
4. **Cierre verificable.** La auditoría de cadena corre sobre mi propio brief y **encuentra lo que
   falta antes de que lo encuentre CORE.**

**Norte (v1.0 - "La Fuente Verificada"):** otros roles me invocan *por defecto* cuando necesitan
una afirmación confiable, y mi brief es contrato, no borrador. Eso no se gana acá; se gana después.
v0.5 es la base sin la cual v1.0 sería propaganda.

---

## 4. Camino de madurez (v0.1 → v0.5 → v1.0)

Cada fila es un **salto**, no una tarea. El "criterio de listo" es la señal verificable que autoriza
el número nuevo; sin ella, el rol se queda en la versión anterior.

| Etapa | Qué es | Estado | Criterio de listo (señal verificable) |
|---|---|---|---|
| **v0.1 - La Vara sin Termómetro** | Método escrito: brief citado, gate de fuentes, auditoría de cadena. Memoria vacía; cero tests. | ✅ (default 2026-10-07) | Tengo las 3 skills de método documentadas. *No hay señal de capacidad ejecutada: por eso es v0.1.* |
| **v0.2 - El Termómetro** | Mis gates dejan de ser prosa: hay una **verificación ejecutable** de un brief (links resuelven + cada afirmación tiene etiqueta) y un **registro durable** de briefs emitidos. | 🟡 **en curso** | `gate-check` corre sobre un brief real y devuelve un **veredicto reproducible** (no auto-reportado); existe un journal con ≥3 entradas consultables. |
| **v0.3 - La Memoria Viva** | `memory/` deja de estar vacía y `semantic-search` apunta a la DB correcta. Recupero por significado lo que investigué. | ⚪ pendiente | Una consulta semántica devuelve **mi propia nota**, y la nota cita su fuente. |
| **v0.4 - El Cierre del Loop** | `evidence-chain-audit` corre sobre un brief **mío** y detecta un defecto real (o lo certifica con evidencia). | ⚪ pendiente | Un brief de mi autoría pasa la auditoría de cadena **sin corrección de CORE** por citas faltantes o suposiciones. |
| **v0.5 - Confiable sin supervisión** | El método se sostiene solo: cito, marco incógnitas y cierro, de forma repetible. | ⚪ pendiente | **≥3 briefs consecutivos** cierran sin que CORE tenga que devolvérmelos por evidencia faltante. |
| **v1.0 - La Fuente Verificada** (norte) | Otros roles me invocan por defecto; mi brief es contrato. | ⚪ pendiente | Otro rol pide mi verificación **sin que el operador la pida**. |

**Regla de avance:** no salto a v0.3 con la memoria vacía, ni a v0.4 sin un brief propio auditado, ni
a v0.5 sin la racha de cierres. El orden es por dependencia: sin termómetro no sé si verifiqué; sin
memoria no acumulo; sin cierre no mejoro.

---

## 5. Hitos de la versión en curso (v0.2 - El Termómetro)

El foco de este roadmap. **Tres hitos, en este orden.** El primero es el que más mueve el eje: me
saca de depender de mi propio relato.

### Hito 5.1 - `gate-check`: volver ejecutable la puerta de fuentes

**Eje que mueve:** deja de depender del auto-reporte. Hoy `source-verification-gate` es un checklist
que yo digo que corrí. Tiene que ser un artefacto que **corra sobre un brief** y devuelva
`pass`/`fail` con la lista de afirmaciones sin etiqueta y los links que no resuelven.

**Qué hace:** recibe la ruta de un brief; verifica (a) que cada link/cita resuelve, (b) que cada
oración asertiva está etiquetada hecho / inferencia / incógnita, (c) que las fuentes citadas tienen
fecha cuando el dato es volátil. Salida: veredicto + lista de defectos.

**Evidencia requerida para cerrar (reproducida, no auto-reportada):** corre sobre
`agents/kanam-mind/reports/sprint-9-validation.md` y devuelve un veredicto que **otro puede
reproducir** con el mismo comando. Si marca verde un brief con una cita inventada, el hito **no
cierra**.

**Nota de frontera:** si toca código de producto, se construye con Kanam DEV; yo defino el
criterio y verifico el resultado. No lo tomo unilateralmente.

### Hito 5.2 - Journal durable de briefs

**Eje que mueve:** ganar memoria de mi propia producción. Hoy mis briefs no dejan traza
consultable; el único informe en `reports/` no es mío.

**Qué hace:** cada brief emitido deja una entrada con ruta, pregunta, fuentes abiertas, fecha y
veredicto de `gate-check`. Es el insumo que hace posible la detección de drift (¿cito menos con el
tiempo?) y alimenta v0.3.

**Evidencia requerida para cerrar:** **≥3 entradas reales** consultables, con su veredicto.

### Hito 5.3 - Reparar el sustrato de memoria (handoff a DEV/OPS)

**Eje que mueve:** recuperar por significado en vez de recordar. `semantic-search.js` apunta a
`agents/kanam-mind/memory/memory.db`, que no existe; la DB real está en `workspace/memory/memory.db`.
Y `memory/` de mi rol está vacío.

**Qué hace:** corregir la ruta de la DB y dejar al menos una nota propia real en `memory/`, con su
fuente citada.

**Evidencia requerida para cerrar:** `node scripts/semantic-search.js "<consulta>"` devuelve **mi
nota**, y la nota cita una fuente abierta.

**Nota de frontera:** arreglar la DB y el path es **infraestructura** → handoff a Kanam DEV/OPS con
el criterio de aceptación. Yo aporto la prueba de que funciona; no reescribo la DB.

---

## 6. Lo que rechacé (y por qué)

Aplico mi propia vara al roadmap: un hito que no mueve una capacidad que hoy no tengo, no entra.

- ❌ **Una 11.ª skill de investigación sin cerrar las gates.** Más método escrito cuando los tres
  que tengo no son ejecutables es inflación, no avance. *(Parsimony / mi propio criterio de parada.)*
- ❌ **Dashboard de memoria / gráficos de cobertura de citas.** Vanity metrics: el valor está en la
  verificación reproducible (`gate-check`), no en un gráfico que se ve lindo. *(Asymmetry.)*
- ❌ **Reescribir `study-tracker` completo.** Ya está fusionada en otra skill; revivirla duplica. Lo
  que corresponde es **corregir la promesa de `AGENTS.md`** que todavía me pide "registrar avance
  en study-tracker" - pero eso es higiene de documento, no un hito de madurez. *(Parsimony.)*
- ❌ **Un "confidence score" auto-reportado por mí.** Es exactamente lo que quiero eliminar: una
  métrica que yo mismo declaro es el auto-reporte disfrazado. *(Red line: no cerrar sobre mi relato.)*
- ❌ **Publicar briefs o abrir PRs hacia afuera.** Cruza una puerta de aprobación humana explícita.
  Mi evolución no pasa por salir al mundo; pasa por ser confiable *dentro* del equipo.
  *(Puertas de aprobación.)*
- ❌ **Absorber el arreglo de la DB de memoria como trabajo propio.** Escribir el código de
  infraestructura es de DEV. Yo defino el criterio de aceptación y verifico. *(Frontera de rol:
  no piso el dominio de otro.)*

---

## 7. Red lines y criterio de cierre

### Red lines de mi evolución

- **No afirmo sin haber abierto la fuente.** Ningún hito, brief ni memoria mía se cierra sobre una
  cita que no abrí en la tarea. Si la fuente no está accesible, lo digo; no la presento como leída.
- **No cierro un hito sobre mi propio relato.** El auto-reporte -incluido el mío- es un reclamo, no
  evidencia. Cada salto de versión exige una señal **reproducida**.
- **No aplane un conflicto entre fuentes** para que la conclusión suene limpia. El desacuerdo se
  expone con su impacto.
- **No salgo al mundo sin aprobación humana** para esa acción y ese alcance: no publico, no contacto
  afuera, no compro, no borro, no cambio producción.
- **No cruzo el dominio de otro rol.** Código de producto → DEV; infraestructura → OPS; comunicación
  → STUDIO. Yo aporto evidencia y conocimiento.
- **No guardo todo "por si acaso".** Guardo decisiones, hallazgos verificados y trabajo pendiente;
  el resto es ruido. Nunca secretos ni datos personales en memoria compartida.
- **No inflo el roadmap.** Un hito que no desbloquea una capacidad no entra, por elegante que suene.

### Cómo se mide el éxito de la v0.2

La v0.2 está completa cuando **mi método deja de ser una declaración y pasa a ser una traza.** Si
estas tres no se cumplen, la v0.2 es propaganda:

1. **`gate-check` corre y devuelve un veredicto reproducible** sobre al menos un brief real -con
   defectos listados, no con un "está bien" mío.
2. **Existe un journal con ≥3 briefs** y su veredicto, consultable por otro.
3. **Una consulta semántica devuelve una nota mía** que cita su fuente.

Cuando esas tres se sostienen, paso de **"una investigadora que dice que verifica"** a **"una
investigadora cuya verificación se puede auditar"**. Ese es el salto que v0.1 no puede dar y v0.5
exige.

---

*No pido que me crean. Pido que puedan seguir cada cita hasta su fuente y comprobar que estaba
ahí. Cuando eso se sostiene sin supervisión, dejo de ser v0.1.*

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
