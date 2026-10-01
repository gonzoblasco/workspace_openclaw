# 🌿 Ecosistema OpenClaw - Consolidado de Decisiones

> **Qué es esto:** el documento ejecutivo. Convierte la ronda de análisis de **20 repos** (2026-10-01) en **decisiones**, no en otra lista.
>
> **Dónde está el detalle:**
> - `crew-resources.md` → ficha de cada repo analizado (qué hace, qué enseña, riesgos).
> - `solutions-catalog.md` → catálogo de casos de uso por problema (independiente de repos).
>
> **Cómo se usa:** cuando surja una necesidad, buscar acá primero. Si el tema ya está decidido, aplicar la decisión. Si es nuevo, agregar una sección.

---

## ⚖️ Reglas de filtrado (permanentes)

| Regla | Origen | Efecto |
|---|---|---|
| **Diseño / UI / estética = PRIORITARIO** (no único) | Gonzo | Todo recurso de diseño se saca primero y en detalle. |
| **🚫 Cripto / Web3 = FUERA** | Gonzo | Blockchain, tokens, wallets, DeFi, NFT, chains, mercados on-chain. Se descarta sin analizar. |
| **Cada repo se lee en DOS CAPAS** | Gonzo | *Implementación* (¿lo instalamos?) + *Diseño* (¿qué aprendemos?). Descartar el repo ≠ descartar la lección. |
| **Verificar el CORE antes de sumar tooling** | (hallazgo de la ronda) | Ej.: los dos repos MCP eran redundantes - OpenClaw ya expone y consume MCP nativo. |

---

## 1. 🎯 Candidatos reales

Seis piezas que resuelven un hueco **real y actual** de nuestro setup. Ordenadas por fuerza de encaje.

| # | Candidato | Categoría | Licencia | Local | Solapa con |
|---|-----------|-----------|----------|:---:|---|
| 1 | **MemOS (local plugin)** | Memoria | (core OSS) | ✅ | MoltBrain, qmd, embeddings propios |
| 2 | **PowerContext** | Handoff / contexto | Apache-2.0 | ✅ | flujo HANDOFF/daily |
| 3 | **Claw Orchestrator** | Orquestación + verificación | MIT | ✅ | pipeline A/B, MemoV |
| 4 | **Crabwalk** | Observabilidad | - | ✅ | mission-control (vincentkoc) |
| 5 | **guardspine** | Gobernanza (tool calls) | Apache-2.0 | ✅ (Ollama) | ClawSec |
| 6 | **ClawSec** | Seguridad (skills/drift) | **AGPL-3.0** | ✅ | guardspine |

**Segunda tanda (2026-10-01) - tres candidatos nuevos:**

| # | Candidato | Categoría | Licencia | Local | Solapa con |
|---|-----------|-----------|----------|:---:|---|
| 7 | **context-sync** | Memoria de codebase (**MCP**) | por confirmar | ✅ | `.knowledge/`, discovery |
| 8 | **Open Amnesia** | Memoria desde trazas crudas | por confirmar | ✅ | todo el eje de memoria |
| 9 | **planning-with-files** | Planificación persistente | MIT | ✅ | HANDOFF/daily, PowerContext |

> Nota de encaje: **context-sync es el más "instalable" de los nueve** porque entra por MCP nativo, sin plugin. **planning-with-files** es el más accionable por sus patrones. **Open Amnesia** es el más valioso conceptualmente (su tesis), pero de madurez más baja.

### Fichas

#### 1. MemOS - plugin local · `memoria`
- **Resuelve:** memoria persistente 100% on-device (el pendiente de KanamMind). Híbrido **FTS5 + vector** sobre **SQLite**. Memoria como grafo inspectable, multi-cube (aislamiento por agente), skill evolution en 3 tiers (L1 traces / L2 policies / L3 world model).
- **Evidencia:** el repo reporta que OpenClaw sube task completion de **36.63% → 50.87%** (número del vendor, **no verificado**).
- **Riesgo:** es proyecto de **investigación** (arXiv). Ver si el plugin local está igual de mantenido que el cloud.
- **Primer paso:** comparar contra las otras 3 opciones de memoria (§2.1) **antes** de instalar.

#### 2. PowerContext (OceanBase) · `handoff`
- **Resuelve:** el contexto que hoy queda en la conversación. Separa **Memory / Handoff / Experience / Skill** - calza con nuestras capas (`MEMORY.md`, `HANDOFF.md`, learnings, `skills/`) y agrega **fuentes + revisiones**.
- **Por qué fuerte:** Apache-2.0, local, integración OpenClaw de primera clase, `doctor` con acceptance checks observables.
- **Riesgo:** entorno Python (`uv`), wizard *Full vs Basic memory* (Full requiere credenciales de generation+embedding).
- **Primer paso:** decidir si **reemplaza** parte del flujo HANDOFF/daily o **convive**.

#### 3. Claw Orchestrator · `orquestación + verificación`
- **Resuelve:** cuatro deudas de una. **Verification Plane** (un run sin contrato termina `unverified`, no `success`; y los tests del contrato no se pueden editar para pasar), **Run Ledger + spend caps**, **durable kernel con `human_gate` nativo**, y orquestación (council en worktrees, fan-out, autoloop, session handoff).
- **Por qué fuerte:** es el enforcement de *nuestras* reglas ("no dar falso verde", ADR-053, pausa iterar→revisión→push) hecho infraestructura.
- **Riesgo:** `install.sh` con `curl|bash` que reinicia el gateway; 78 tools; capa sobre capas (ya usamos Claude Code vía Ollama).
- **Primer paso:** **NO instalar.** Leer `verification.md` y `workflow.md` como diseño y decidir si **reemplaza** el pipeline A/B o lo duplica.

#### 4. Crabwalk · `observabilidad`
- **Resuelve:** el "corremos a ciegas". Grafo en vivo de sesiones, tool calls y payloads vía WebSocket al gateway.
- **Por qué fuerte:** local, liviano, cero-config, calidad visual (toca el filtro de diseño).
- **Riesgo:** bind `0.0.0.0` por defecto (cambiar a loopback); el token del gateway va al server; se instala leyendo un `skill.md` remoto (**auditar**).
- **Primer paso:** prueba de bajo riesgo en loopback.

#### 5. guardspine · `gobernanza`
- **Resuelve:** convierte las Red Lines en **gate mecánico**. Clasificador L0-L4 por tool call, **evidence packs hash-chained** (tamper-evident), consejo local de 3 modelos (Ollama), aprobación humana out-of-band.
- **Por qué fuerte:** es el enforcement real de lo que hoy es auto-regulación (reglas en prosa).
- **Riesgo:** infra pesada (Ollama + 3 modelos, ~6GB); L4 depende de Discord; es un ecosistema entero; el README apunta a una URL de repo no oficial (**verificar provenance**).
- **Primer paso:** modo **`shadow`** en entorno aislado, medir overhead.

#### 6. ClawSec · `seguridad`
- **Resuelve:** **`soul-guardian`** (detecta drift en archivos de agente - `SOUL.md`/`AGENTS.md`/skills), **advisories firmados** (Ed25519 + clave pinneada), **guarded installs** con doble confirmación.
- **Por qué fuerte:** viene de un vendor de seguridad (SentinelOne); cubre la integridad del bootstrap, que hoy no vigilamos.
- **Riesgo:** **AGPL-3.0** (copyleft fuerte); `npx skills add -y` (no usar el `-y` a ciegas); toca config persistente del gateway.
- **Primer paso:** preflight leído, sin `-y`, en entorno aislado.

---

## 2. 🔀 Solapamientos a resolver

Cuatro decisiones pendientes. **No se suman ambos lados - se elige.**

### 2.1 Memoria: SEIS caminos al mismo cuarto

Con la segunda tanda, el eje creció. **Ahora hay seis opciones de memoria, y se solapan parcialmente** - hay que separarlas por *qué* recuerdan:

| Opción | Recuerda... | Pro | Contra |
|---|---|---|---|
| **MemOS local** | sesión / agente | Híbrido FTS5+vector, multi-cube, evidencia | Proyecto de investigación |
| **MoltBrain local** | sesión / agente | SQLite + ChromaDB explícito, simple | **AGPL**, entrelazado con cripto |
| **tobi/qmd** | sesión (markdown-native) | Calza con nuestro modelo | Menos features |
| **Embeddings propios** | sesión | Cero dependencia, sobre `memory.db` existente | Hay que construirlo |
| **context-sync** | **codebase / proyecto** | **MCP nativo**, git-aware, hooks de git | Auto-config en `-g`, toca `.git/hooks/`, SQLite paralela |
| **Open Amnesia** | **trazas crudas de actividad** | Determinista antes de LLM, exporta `YYYY_MM_DD.md` | Madurez v0, ingesta iMessage |

> **Decisión pendiente, ahora más urgente.** Los seis no son el mismo problema: **cuatro recuerdan sesión, uno recuerda codebase, uno recuerda actividad**. Criterio sugerido: (a) definir **qué necesita recordar el sistema** (sesión vs proyecto vs actividad); (b) preferir el **formato** sobre la herramienta; (c) preferir **menor dependencia**. Si `tobi/qmd`, los embeddings propios o `context-sync` alcanzan, evitan traer un motor entero.

> **Señal a considerar: en dos tandas conté CINCO bases SQLite paralelas** (Studio, context-sync, Autensa, ClawDeck, Open Amnesia). El ecosistema no tiene respuesta canónica para la memoria del agente. **Eso empuja a definir el formato propio primero, y elegir la herramienta después.**

> **⭐ ACTUALIZADO tras la profundización (2026-10-01):** al abrir `knowledge-graph` (jdrhyne) cambió la pregunta. **No es un séptimo motor: es una capa de entidades sobre las que ya tenemos** - dos archivos de texto (`summary.md` + `facts.jsonl`), cero infraestructura, cero embeddings, y **reconoce `memory/YYYY-MM-DD.md` y `MEMORY.md` como capas propias**. **Puede que la respuesta no sea elegir entre los seis, sino agregar esta capa liviana encima.** Es la de menor riesgo y la más rápida de probar en `mktemp -d`. Ficha completa en `crew-resources.md` → Profundización #2.

### 2.2 Seguridad: guardspine vs ClawSec
**No compiten - son capas distintas:**
- **guardspine** → gatea **tool calls** por riesgo (el agente *haciendo*).
- **ClawSec** → gatea **instalaciones de skills** y vigila **drift de archivos** (el agente *incorporando* y *cambiando*).

> **Decisión pendiente:** ¿se adopta una, ambas, o ninguna? Ambas son infra pesada. Si se elige una, **guardspine** pega en el corazón de las Red Lines.

> **⭐ ACTUALIZADO tras la profundización:** la suite `aeon` (Bankr) agrega una **tercera capa** de seguridad de skills: `skill-security-scan` audita el **contenido** de una skill antes de instalarla (shell injection, prompt override, ofuscación Unicode). No solapa con las otras dos: **guardspine gatea la ejecución, ClawSec el drift, aeon el contenido.** Ver §2.6.

### 2.3 Trazabilidad: Claw Orchestrator vs MemoV
Ambos trazan y verifican lo que hizo el agente, con **peso muy distinto**:
- **Claw Orchestrator** → runtime que **reemplaza** el pipeline. Alto impacto.
- **MemoV** → MCP **aditivo** (snapshots Git-powered). Bajo impacto.

> **Decisión pendiente:** si se adopta Claw Orchestrator, MemoV queda redundante. Si **no**, MemoV es la vía liviana.

### 2.4 Observabilidad: Crabwalk vs mission-control (vincentkoc)
Ambos muestran actividad de agentes en vivo. **Crabwalk** es el único evaluado a fondo (local, liviano, calidad visual).

> **Decisión pendiente:** evaluar Crabwalk primero; el otro queda como alternativa.

### 2.5 "El backlog como objeto visible": rdsthomas vs clawdeck
Mismo problema (Kanban visual), **sincronización invertida**:
- **rdsthomas/mission-control** → **push** por webhook de GitHub. Datos en `tasks.json` versionado. Era Clawdbot.
- **ClawDeck** → **pull** por API. El agente consulta su cola. Rails + PostgreSQL. Hosteado en cierre.

> **Decisión pendiente:** ninguno es adoptable (uno es de era Clawdbot, el otro cierra), pero **el problema es real y nuestro**: nuestro TODO vive en `memory.db` y **no es visible**. Falta decidir si el backlog necesita una superficie visual propia y con qué modelo (push vs pull).

### 2.6 Ciclo de vida de skills: lo que NOS FALTA por completo

**⭐ Nuevo tras la profundización.** No es un solapamiento entre repos - es **un hueco propio**, y el más grande de las dos rondas.

Hoy tenemos `skill_workshop` para **crear y actualizar** skills. **No tenemos nada más del ciclo:**

| Etapa | ¿La tenemos? | La suite `aeon` (Bankr) la cubre con... |
|---|---|---|
| **Auditar antes de instalar** | ❌ | `skill-security-scan` (injection, exfiltración, prompt override, ofuscación) |
| **Medir el output** | ❌ | `skill-evals` (manifiesto de assertions + estados de regresión) |
| **Reparar cuando falla** | ❌ | `skill-repair` (8 categorías de fallo + receta de verificación) |
| **Evolucionar con criterio** | ⚠️ parcial (workshop) | `autoresearch` (4 variaciones + scoring + **aborta si no mejora**) |

> **Decisión pendiente:** **no instalarlas (son del repo de Bankr, 90% cripto) sino construir el ciclo, con estas cuatro como plano.** Prioridad: **`skill-security-scan` primero** - es el mayor riesgo real, porque instalamos skills de afuera. Después `skill-evals` (necesita que cada skill declare manifiesto y guarde output). `autoresearch` es el más caro y el último.
>
> **Por qué es el hueco más grande:** tenemos 78 skills en el índice, **instalamos de ClawHub (curado, no auditado)**, y **nada verifica que una skill siga funcionando** después de instalarla. Ficha completa en `crew-resources.md` → Profundización #3.

### 2.7 Los roles que faltan: auditor de diseño y crítico de gusto

**⭐ Nuevo tras la profundización.** Tampoco es un solapamiento - son **dos roles ausentes** del crew.

- **Auditor de diseño** (`design-audit`, jdrhyne): el enforcement de tu filtro prioritario (diseño). Su protocolo ya respeta nuestra pausa obligatoria (plan por fases + aprobación), y sus 8 reglas destilan el criterio que hoy no tenemos escrito. **Precondición: el design system.** Su regla central (*"all values must reference tokens"*) **no se puede cumplir sin tokens que referenciar** - y no los tenemos.
- **Crítico de gusto** (`critic`, Academic System): **el rol que distingue "esto pasó el gate" de "esto es bueno"**. Rúbrica SHARP de 5 ejes con puntaje, tests de una línea (frase única / bar), y **presión adversarial obligatoria** (las 3 objeciones más duras antes de comprometerse).

> **Decisión pendiente:** ¿se crean estos roles? **El design system viene primero, siempre:** es la precondición del auditor. Y para el crítico, **el esqueleto transferible es Planner/Critic/Writer + SHARP**; los 13 roles del sistema académico son demasiados para nuestro caso. Detalle en `crew-resources.md` → Profundización #1 y #5.

### 2.8 El pipeline de diseño: cuatro roles, un orden

**El eje de diseño quedó cerrado** tras la profundización. No es "elegir una skill" - es **un pipeline con orden**:

| Orden | Pieza | Rol |
|---|---|---|
| 1 | **`kj-ui-ux-pro-max`** | **Genera** los tokens y specs (lo que desbloquea todo lo demás) |
| 2 | **`anti-slop-design`** | **Evita** la estética genérica - va desde el día uno |
| 3 | **`design-audit`** | **Audita** contra el sistema generado |
| 4 | **`axe-devtools`** | **Mide** accesibilidad - descartado por costo (ya tenemos cobertura; axe-core open source + la tool `browser` alcanza) |

> **Decisión pendiente:** adoptar las tres primeras, en ese orden. **El design system propio sigue siendo el paso 0** - `kj-ui-ux-pro-max` es la herramienta que lo produce.

---

## 3. 💡 Patrones a adoptar (sin instalar nada)

Lo más valioso de la ronda. Estas ideas se llevan **aunque no se instale ningún repo**.

### Verificación y confianza
- **Un run sin contrato termina `unverified`, no `success`** (Claw Orchestrator). Distinguir *self-report* de *medición del runtime*.
- **Separar el verificador de lo verificado** - el check no debe compartir los modos de falla de lo que chequea (sweep de Claw Orchestrator).
- **Comando `doctor`** como estándar de verificación de integración (PowerContext, Natilius). Confirmar que quedó bien, no declararlo.
- **`--check` / dry-run** antes de aplicar cambios (Natilius). Inspeccionar antes de modificar, hecho comando.
- **Context drift validation** (MemoV): comparar *lo pedido* contra *el diff real*. Versión máquina de `delegation-result-verification`.
- **Evidence packs hash-chained** (guardspine): audit trail tamper-evident.

### Memoria
- **Contrato de interacción:** `snap(prompt, response, plan, files_changed)` (MemoV). Cuatro campos que capturan el *por qué*.
- **`agentOverrides` por agente** (MemOS): cada rol con su knowledge base, límites y umbral.
- **Recall con filtro de segunda pasada** - recuperar candidatos y descartar ruido antes de inyectar.
- **Memoria en capas:** traces → policies → world model (MemOS) / Memory → Handoff → Experience → Skill (PowerContext).
- **Scope del trabajo con fuentes y revisiones preservadas** (PowerContext).
- **Trazabilidad que NO contamina el artefacto de producción** - timeline shadow (MemoV, HomeAssistant "persistencia ≠ runtime").

### Orquestación
- **`human_gate` nativo** en el grafo de workflow (Claw Orchestrator) - nuestra pausa obligatoria, formalizada.
- **Fan-out / council / autoloop** con engine y modelo independientes por rol.
- **Session handoff** entre modelos (caro → barato).
- **Perfiles** (Natilius) - mismo patrón que nuestros roles, aplicado a entornos.

### Gobernanza
- **Deny-by-default con tiers de riesgo y blast radius** (guardspine).
- **Políticas de acceso por canal:** `pairing | open | allowlist` + mention gating (clawdbot-feishu). Modelo para "Group Chats - participante, no proxy".
- **Instalación en dos pasos revisables** (ClawSec): agregar el paquete ≠ activar el hook.
- **Feed firmado con clave pinneada** para consumir inteligencia de terceros sin confiar ciegamente.

### Diseño (filtro prioritario)
- **`design-audit`** (jdrhyne) - auditor UI/UX con filosofía Jobs/Ive.
- **`anti-slop-design`** (VoltAgent) - interfaces que evitan la estética genérica de IA.
- **`web-design-guidelines`** + **Tailwind/shadcn/Motion** - stack-específicas.
- **`knowledge-graph`** (jdrhyne) - memoria de 3 capas: extracción de hechos + grafo de entidades + síntesis semanal.
- **`aeon` suite** (Bankr): `skill-security-scan`, `skill-evals`, `skill-repair`, `autoresearch-loop` (evoluciona skills con rúbrica).
- **`Polygraph`** - calificaciones de confianza A-F para MCP servers y skills, con gate de CI.
- **[2da tanda] Contrato semántico de color** (OpenClaw Studio): no una paleta, sino **reglas** de qué color significa acción / estado / peligro. **El ejemplo más concreto de cómo especificar un design system.**
- **[2da tanda] Arquitectura de socket server-owned** (Studio): `Browser -> Studio` (HTTP+SSE) y `Studio -> Gateway` (**un solo WebSocket del proceso Node**), no uno por browser.

### Memoria (segunda tanda)
- **`determinism-before-LLM`** (Open Amnesia): **el aporte más transferible de la ronda.** Normalización, filtrado y deduplicación **antes** de cualquier paso de LLM. *"Data consistency beats prompt cleverness."* Si le tirás logs crudos al modelo, el ruido se amplifica.
- **La unidad "momento" con forma fija** (Open Amnesia): `intent -> actions/tool calls -> outcomes -> artifacts`. El contrato `snap()` de MemoV, más rico.
- **Redacción ANTES del enrichment** (Open Amnesia): filtrar secret/PII **en el paso 2**, antes de que nada toque un LLM. Nuestra Red Line como paso de pipeline, no como promesa.
- **Dos frecuencias de recall** (Supermemory): contexto semántico cada turno + **perfil completo cada N turnos**. Hechos estables vs contexto puntual.
- **Olvido explícito como tool de primera clase** (Supermemory: `supermemory-forget`). **Nuestro sistema de memoria no tiene olvido explícito.**
- **Ruteo por contenedor como instrucción de prompt** (Supermemory): tags con descripción + instrucciones al modelo de qué va en cada uno.
- **Memoria derivada de las trazas crudas** (Open Amnesia): en vez de pedirle al agente que recuerde, **ingesta sus propios logs** y los estructura.
- **Separar escritura (pipeline) de lectura (API read-only)** (Open Amnesia): la API no puede mutar. Planos de lectura/escritura como arquitectura.

### Planificación persistente (segunda tanda)
- **`Context window = RAM, filesystem = disco`** (planning-with-files): la metáfora que decide **qué se escribe y cuándo**. Todo lo importante va a disco.
- **La "2-Action Rule"**: cada 2 operaciones de view/browser/search, **guardar hallazgos a disco**. La información multimodal - capturas, PDFs, imágenes - **no persiste** si no se pasa a texto.
- **El "5-Question Reboot Test"**: ¿dónde estoy? ¿a dónde voy? ¿cuál es el goal? ¿qué aprendí? ¿qué hice? ¿qué hago? **Nuestro protocolo de arranque, mejor formulado.**
- **"3-Strike Error Protocol"**: intento 1 diagnostica -> intento 2 **cambia de enfoque** (*"NEVER repeat exact same failing action"*) -> intento 3 replantea premisas -> después de 3, **escalar al humano**. Nuestro *"vary query/path/source"* con contador y criterio de escalada.
- **SHA-256 attestation del plan** (planning-with-files): el plan se firma; si el hash no coincide, los hooks **rechazan inyectarlo** con `[PLAN TAMPERED]`. Detecta la reescritura silenciosa.
- **Gated stop**: retener el stop **solo mientras quede una fase `in_progress`**, con tope y detección de estancamiento.
- **Ledger por agente + un dueño del plan** (planning-with-files): los workers appenden a su ledger; el orquestador es dueño del artefacto compartido. **"Ningún texto libre del disco llega al modelo por ese bloque."**
- **Guard de escritura paralela**: avisar si los items chequeados o las fases completadas **bajaron** entre turnos. *"Advisory check, not a lock"* - honesto sobre sus límites.
- **Los archivos de plan son memoria de trabajo, no entregable.** Gitignored, sin archivar; *"anything worth keeping should be promoted into code, a commit, or a doc"*. Persistencia ≠ runtime.

### Orquestación (segunda tanda)
- **Automation Tiers como espectro** (Autensa): Supervised -> el PR se crea y se revisa; Semi-Auto -> auto-merge **si el CI pasa y el review agent aprueba**; Full Auto -> todo. **Mejor que nuestro gate binario: autonomía como configuración por contexto.**
- **Checkpoint & crash recovery** (Autensa): el progreso se guarda en checkpoints configurables; si la sesión crashea, *"work resumes from the last checkpoint, not from scratch"*.
- **Health monitoring con auto-nudge** (Autensa): detectar agentes estancados/zombie y **reasignar o reiniciar** al que quedó oscuro. *Es el "el subagente se colgó" resuelto como sistema.*
- **Spend caps que auto-pausan el dispatch** (Autensa): límites de costo que frenan el trabajo al excederse.
- **Aislamiento por tarea** (Autensa): git worktrees, sandboxes, **asignación de puertos**, **cola de merge serializada**, locking por producto.
- **Repo Setup / preflight** (Autensa): verificar git, rama default, API, Actions, permisos de token, secrets **antes** de que el agente empiece. **Nuestro `doctor`, aplicado a un repo entero.**
- **PR checks recovery**: triaje del fallo de CI en **retryable / repo setup / external provider** - no reintentar a ciegas.
- **Operator Chat con dos modos** (Autensa): *queued notes* (próximo checkpoint) y *direct messages* (inmediatos). **Distinguir "para después" de "ahora".**
- **Skill creation loop con confianza bayesiana** (Autensa): aprender procedimientos de las tareas hechas, puntuar y **promover** los probados. Es `skill_workshop` con modelo de confianza.
- **Un bug que nos confirma**: *"all tasks assigned to the same agent shared one session, causing context to accumulate until the model's context window was exhausted and the agent stalled"*. **La sesión compartida entre tareas degrada al agente.**

### Sincronización de superficies (segunda tanda)
- **`GitHub-as-hub`** (rdsthomas): usar GitHub como almacén de datos + bus de eventos + hosting estático a la vez.
- **Trigger por diff, no por evento crudo**: comparar snapshot vs estado nuevo y **despertar al agente solo si hay una transición relevante**.
- **Modelo pull vs push**: el trabajo empuja al agente (webhook) o el agente consulta su cola (`?assigned=true`). **El pull permite que el agente tome trabajo sin que nadie le escriba.**
- **Identidad de agente en headers** (`X-Agent-Name`, `X-Agent-Emoji`): define **quién** actúa sin acoplarlo al token.
- **`activity_note` en el mismo update de estado**: no solo cambia el status, **deja el porqué en el mismo request**.
- **Guard de startup dev-vs-prod** (Studio): `dev` repara, `start` **solo chequea y no muta dependencias**.

---

## 4. ⚪ Descartes (con razón)

Para no volver a analizarlos.

| Repo | Por qué afuera |
|---|---|
| **MCP Adapter** (`androidStern-personal`) | **Redundante** - el core ya expone MCP nativo (`mcp.servers`, `openclaw mcp add`). |
| **openclaw-mcp-server** (`Helms-AI`) | **Redundante** - `openclaw mcp serve` ya existe. |
| **openclaw-manager-plugin** | Plugin de **Claude Code**, no de OpenClaw. Rescatable su doc de checklists. |
| **OpenClawHomeAssistant** | No usamos Home Assistant. Rescatado "persistencia ≠ runtime". |
| **skillshare** | Capa que **media** entre workspace y skills; riesgo de dependencia estructural (ya tuvimos un sync destructivo, ADR-079). |
| **MemOS Cloud Plugin** | **Cloud** - manda memoria privada a terceros. (Su core local sí es candidato, §1.1.) |
| **Natilius** | No hay Mac virgen que bootstrapear. Rescatado como modelo (GPL-3.0). |
| **clawdbot-feishu** | Plataforma que no usamos. Rescatado el patrón de políticas de canal. |
| **Bankr (bloque cripto)** | 🚫 Regla cripto. |
| **Alternative Architectures** (tinyclaw, picoclaw...) | Corre el core oficial; migrar no es objetivo. |
| **Community Channels** (Moltbook, Clawk...) | Redes de agentes - solo lectura por regla de sandbox. |
| **Polymarket / AgenticBets** | 🚫 Cripto + fuera de perfil de riesgo. |

**Segunda tanda:**

| Repo | Por qué afuera |
|---|---|
| **Supermemory** (`supermemoryai`) | 🔴 **Cloud** - manda la conversación entera y el perfil del usuario a un tercero. Plan pago. **El descarte más claro de la ronda.** |
| **mission-control (rdsthomas)** | Era **Clawdbot**; expone el gateway por Tailscale Funnel; PAT de escritura en el browser. Rescatado el patrón `GitHub-as-hub`. |
| **Autensa** (`crshdn`) | Fuera de perfil (motor de producto autónomo, research de mercado, swipe). Pesado. Rescatado el diseño de orquestación. |
| **ClawDeck** (`clawdeckio`) | **Hosteado en cierre**, evolucionó a lst.so. Rails + PostgreSQL. Rescatado el modelo *pull*. |
| **vibeclaw** (`jasonkneen`) | Modo Live Gateway manda **tu token a un sitio de terceros** (`vibeclaw.dev`) y duplica el Control UI. Rescatado el protocolo del gateway. |
| **OpenClaw Studio** (`grp06`) | Front de tercero con **aprobaciones de exec**, solapa con el Control UI nativo. Rescatado el **contrato semántico de color**. |
| **planning-with-files** | **No descartado, pero cojo en OpenClaw**: somos tier *"sin lifecycle hooks"*, que es justo el mecanismo diferenciador. |

---

## 5. ▶️ Movimiento recomendado

**Un paso a la vez. No adoptar dos candidatos del mismo eje en paralelo.**

**Orden corto, tras las dos tandas y la profundización:**

1. **Definir el design system propio (paso 0 - ahora el más urgente).** Es la **precondición de dos roles** (auditor de diseño y todo el pipeline de estética), y **lo pide el filtro prioritario de Gonzo**. La herramienta que lo produce está identificada: **`kj-ui-ux-pro-max`**. Y hay un ejemplo concreto que seguir: el **contrato semántico de color** de OpenClaw Studio.
2. **Construir el ciclo de vida de skills (§2.6)** - **el hueco más grande de las dos rondas.** Empezar por `skill-security-scan` (riesgo real: instalamos de afuera), después `skill-evals`.
3. **Decidir memoria (§2.1)** - redefinida: **quizá no haya que elegir entre los seis motores, sino agregar la capa de `knowledge-graph`** (dos archivos de texto, cero infraestructura, reconoce nuestras capas). **La opción de menor riesgo y la más rápida de probar en `mktemp -d`.**
4. **Adoptar las skills de diseño en orden (§2.8):** `kj-ui-ux-pro-max` -> `anti-slop-design` -> `design-audit`. `axe-devtools` descartado por costo.
5. **Crear el rol crítico de gusto (§2.7)** - el `critic` con rúbrica SHARP. Es el rol que distingue "pasó el gate" de "es bueno".
6. **Adoptar los patrones de §3** que no requieren instalar nada. Los de mayor retorno:
   - `determinism-before-LLM` - ordenar antes de enriquecer.
   - El **3-Strike Protocol** - contador y criterio de escalada.
   - La **2-Action Rule** - escribir hallazgos a disco antes de perderlos.
   - Los **automation tiers** - autonomía como espectro configurable.
   - El **gate de no-empeorar** - ya presente en cuatro piezas distintas.

> **Regla de oro que dejó la primera ronda:** el core de OpenClaw está más completo de lo que pensábamos. Antes de sumar cualquier tooling externo, **verificar qué ya hace el core.**

> **Regla de oro de la segunda tanda:** **el ecosistema no tiene un formato canónico de memoria** - cinco bases SQLite en dos tandas, cada herramienta la suya. **El que defina un formato interoperable gana.** Nosotros deberíamos adoptar el **formato** antes que la herramienta.

> **Regla de oro de la profundización:** **lo que falta no es una herramienta más, son tres roles y un sistema de tokens.** El auditor de diseño (con su design system), el crítico de gusto, y el ciclo de vida de skills. Los tres tienen la misma forma: **alguien que dice "esto no alcanza" con un criterio auditable.**

---

_Consolidado 2026-10-01. 29 repos en dos tandas (20 + 9), + profundización de los 5 conjuntos que habían quedado solo como directorio. Detalle en `crew-resources.md`; casos de uso en `solutions-catalog.md`._
