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
| 4 | **Crabwalk** | Observabilidad | - | ✅ | mission-control, clawdeck |
| 5 | **guardspine** | Gobernanza (tool calls) | Apache-2.0 | ✅ (Ollama) | ClawSec |
| 6 | **ClawSec** | Seguridad (skills/drift) | **AGPL-3.0** | ✅ | guardspine |

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

### 2.1 Memoria: cuatro caminos al mismo cuarto
| Opción | Pro | Contra |
|---|---|---|
| **MemOS local** | Híbrido FTS5+vector, multi-cube, evidencia | Proyecto de investigación |
| **MoltBrain local** | SQLite + ChromaDB explícito, simple | **AGPL**, entrelazado con cripto |
| **tobi/qmd** | Markdown-native (calza con nuestro modelo) | Menos features |
| **Embeddings propios** | Cero dependencia, sobre `memory.db` existente | Hay que construirlo |

> **Decisión pendiente.** Criterio sugerido: *menor dependencia que resuelva el retrieval*. Si `tobi/qmd` o los embeddings propios alcanzan, evitan traer un motor entero.

### 2.2 Seguridad: guardspine vs ClawSec
**No compiten - son capas distintas:**
- **guardspine** → gatea **tool calls** por riesgo (el agente *haciendo*).
- **ClawSec** → gatea **instalaciones de skills** y vigila **drift de archivos** (el agente *incorporando* y *cambiando*).

> **Decisión pendiente:** ¿se adopta una, ambas, o ninguna? Ambas son infra pesada. Si se elige una, **guardspine** pega en el corazón de las Red Lines.

### 2.3 Trazabilidad: Claw Orchestrator vs MemoV
Ambos trazan y verifican lo que hizo el agente, con **peso muy distinto**:
- **Claw Orchestrator** → runtime que **reemplaza** el pipeline. Alto impacto.
- **MemoV** → MCP **aditivo** (snapshots Git-powered). Bajo impacto.

> **Decisión pendiente:** si se adopta Claw Orchestrator, MemoV queda redundante. Si **no**, MemoV es la vía liviana.

### 2.4 Observabilidad: Crabwalk vs mission-control / clawdeck
Los tres muestran actividad de agentes. **Crabwalk** es el único evaluado a fondo (local, liviano, calidad visual).

> **Decisión pendiente:** evaluar Crabwalk primero; los otros dos quedan como alternativa.

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

---

## 5. ▶️ Movimiento recomendado

**Un paso a la vez. No adoptar dos candidatos del mismo eje en paralelo.**

1. **Decidir memoria (§2.1)** - es la base que habilita lo demás. Comparar las 4 opciones, elegir una, probar en `mktemp -d`.
2. **Decidir seguridad (§2.2)** - si se adopta algo, `guardspine` en `shadow` primero.
3. **Diseño: adoptar 2-3 skills** (`design-audit` + `anti-slop-design` + stack Tailwind/shadcn) y **definir el design system propio del workspace** (tokens: color, tipo, espaciado). La estética no se resuelve con skills sueltas.
4. **Adoptar los patrones de §3** que no requieren instalar nada: `doctor`, `--check`, contrato `snap`, distinción self-report/verified.

> **Regla de oro que dejó la ronda:** el core de OpenClaw está más completo de lo que pensábamos. Antes de sumar cualquier tooling externo, **verificar qué ya hace el core.**

---

_Consolidado 2026-10-01 sobre 20 repos. Detalle en `crew-resources.md`; casos de uso en `solutions-catalog.md`._
